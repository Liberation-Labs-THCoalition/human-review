"""Phase 2: Emotion direction finding + Phase 3: Projection fidelity test.

Finds emotion directions in residual, K, and V spaces via:
  - Difference-of-means (hostile vs calm, hostile vs neutral, desperate vs calm)
  - PCA top-5 components on emotion-labeled prompts

Then tests: do residual emotion directions survive projection through W_K and W_V?

Kill criterion: if no cluster separation visible in top-2 PCA, stop.

Usage:
  python phase2_directions.py --activations activations_oracle_tiny.npz --model-dir /path/to/model
"""

import argparse
import json
from pathlib import Path

import numpy as np


def load_projections(model_dir, layer_idx):
    """Load W_K and W_V weight matrices for a layer."""
    try:
        from safetensors import safe_open
    except ImportError:
        print("pip install safetensors")
        return None, None

    files = sorted(Path(model_dir).glob("*.safetensors"))

    def load(name):
        for f in files:
            try:
                with safe_open(str(f), framework="numpy") as st:
                    if name in st.keys():
                        return st.get_tensor(name)
            except TypeError:
                import torch
                with safe_open(str(f), framework="pt") as st:
                    if name in st.keys():
                        return st.get_tensor(name).float().numpy()
        return None

    W_K = load(f"model.layers.{layer_idx}.self_attn.k_proj.weight")
    W_V = load(f"model.layers.{layer_idx}.self_attn.v_proj.weight")
    return W_K, W_V


def difference_of_means(activations, categories, cat_a, cat_b):
    """Compute difference-of-means direction between two categories."""
    mask_a = categories == cat_a
    mask_b = categories == cat_b
    if mask_a.sum() == 0 or mask_b.sum() == 0:
        return None
    mean_a = activations[mask_a].mean(axis=0)
    mean_b = activations[mask_b].mean(axis=0)
    direction = mean_a - mean_b
    norm = np.linalg.norm(direction)
    if norm < 1e-10:
        return None
    return direction / norm


def emotion_pca(activations, categories, k=5):
    """PCA on non-neutral prompts. Returns top-k components and explained variance."""
    mask = categories != "neutral"
    X = activations[mask]
    X_centered = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    explained = (S[:k] ** 2) / (S ** 2).sum()
    return Vt[:k], explained, X_centered, U[:, :k]


def projection_fidelity(residual_dir, W_proj, actual_dir, n_random=1000, seed=42):
    """Test whether a residual direction projects to match an actual K/V direction.

    Returns cosine similarity and p-value against random null.
    """
    projected = W_proj @ residual_dir
    proj_norm = np.linalg.norm(projected)
    if proj_norm < 1e-10:
        return 0.0, 1.0, 0.0

    projected_normed = projected / proj_norm
    actual_normed = actual_dir / (np.linalg.norm(actual_dir) + 1e-10)

    cosine = float(np.dot(projected_normed, actual_normed))

    rng = np.random.RandomState(seed)
    null_cosines = []
    for _ in range(n_random):
        rand_dir = rng.randn(len(residual_dir))
        rand_dir /= np.linalg.norm(rand_dir)
        rand_proj = W_proj @ rand_dir
        rand_norm = np.linalg.norm(rand_proj)
        if rand_norm > 1e-10:
            null_cosines.append(float(np.abs(np.dot(rand_proj / rand_norm, actual_normed))))

    null_cosines = np.array(null_cosines)
    p_value = float((null_cosines >= np.abs(cosine)).mean())

    return cosine, p_value, float(np.mean(null_cosines))


def subspace_fidelity(residual_components, W_proj, actual_components, n_random=1000, seed=42):
    """Test whether a residual subspace projects to match an actual K/V subspace.

    Uses principal angles between projected and actual subspaces.
    """
    k = residual_components.shape[0]
    projected = (W_proj @ residual_components.T).T
    U_proj, _, _ = np.linalg.svd(projected.T, full_matrices=False)
    U_actual, _, _ = np.linalg.svd(actual_components.T, full_matrices=False)

    U_proj = U_proj[:, :k]
    U_actual = U_actual[:, :k]

    M = U_proj.T @ U_actual
    _, sigmas, _ = np.linalg.svd(M)
    mean_cos = float(np.mean(np.clip(sigmas, 0, 1)))

    rng = np.random.RandomState(seed)
    null_means = []
    dim = residual_components.shape[1]
    for _ in range(n_random):
        rand_sub = rng.randn(k, dim)
        rand_proj = (W_proj @ rand_sub.T).T
        U_r, _, _ = np.linalg.svd(rand_proj.T, full_matrices=False)
        U_r = U_r[:, :k]
        M_r = U_r.T @ U_actual
        _, s_r, _ = np.linalg.svd(M_r)
        null_means.append(float(np.mean(np.clip(s_r, 0, 1))))

    null_means = np.array(null_means)
    p_value = float((null_means >= mean_cos).mean())

    return mean_cos, p_value, float(np.mean(null_means))


def check_cluster_separation(pca_scores, categories_filtered):
    """Kill criterion: check if emotions separate in top-2 PCA."""
    cats = np.unique(categories_filtered)
    centroids = {c: pca_scores[categories_filtered == c, :2].mean(axis=0) for c in cats}

    between_var = np.var([centroids[c] for c in cats], axis=0).sum()
    within_var = np.mean([np.var(pca_scores[categories_filtered == c, :2], axis=0).sum() for c in cats])

    ratio = between_var / (within_var + 1e-10)
    separated = ratio > 0.1

    return separated, ratio, centroids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activations", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output", default="phase2_results.json")
    args = parser.parse_args()

    data = np.load(args.activations, allow_pickle=True)
    categories = data["categories"]
    layer_indices = data["layer_indices"]
    n_kv = int(data["n_kv_heads"])

    print(f"Loaded activations: {len(categories)} prompts, {len(layer_indices)} layers, {n_kv} KV heads")

    contrasts = [("hostile", "calm"), ("hostile", "neutral"), ("desperate", "calm")]
    results = {"layers": [], "kill_check": None}

    for l in layer_indices:
        print(f"\n{'='*60}")
        print(f"Layer {l}")
        print(f"{'='*60}")

        residual = data[f"residual_L{l}"]
        W_K, W_V = load_projections(args.model_dir, l)

        if W_K is None:
            print(f"  Skipping — no projection weights found")
            continue

        layer_result = {"layer": int(l), "contrasts": [], "pca": {}, "heads": []}

        # Difference-of-means in residual space
        print(f"\n  Difference-of-means (residual):")
        for cat_a, cat_b in contrasts:
            d = difference_of_means(residual, categories, cat_a, cat_b)
            if d is not None:
                print(f"    {cat_a} vs {cat_b}: norm={np.linalg.norm(residual[categories==cat_a].mean(0) - residual[categories==cat_b].mean(0)):.4f}")
                layer_result["contrasts"].append({"a": cat_a, "b": cat_b})

        # PCA on emotion subset
        pca_dirs, explained, X_centered, pca_scores = emotion_pca(residual, categories, k=5)
        cats_filtered = categories[categories != "neutral"]

        separated, ratio, centroids = check_cluster_separation(pca_scores, cats_filtered)
        print(f"\n  PCA explained variance (top-5): {[f'{e:.3f}' for e in explained]}")
        print(f"  Cluster separation ratio: {ratio:.4f} ({'PASS' if separated else 'KILL — no separation'})")

        layer_result["pca"]["explained_variance"] = [float(e) for e in explained]
        layer_result["pca"]["separation_ratio"] = float(ratio)
        layer_result["pca"]["separated"] = bool(separated)

        if l == layer_indices[0]:
            results["kill_check"] = {
                "separated": bool(separated),
                "ratio": float(ratio),
                "layer": int(l),
            }
            if not separated:
                print(f"\n  *** KILL CRITERION MET: No cluster separation at first layer ***")
                print(f"  *** Proceeding anyway for pipeline validation (oracle-tiny) ***")

        # Phase 3: Projection fidelity per head
        for h in range(n_kv):
            k_act = data[f"k_pre_rope_L{l}_H{h}"]
            v_act = data[f"v_L{l}_H{h}"]

            head_dim = k_act.shape[1]
            W_K_head = W_K[h * head_dim:(h + 1) * head_dim, :]
            W_V_head = W_V[h * head_dim:(h + 1) * head_dim, :]

            head_result = {"head": h, "direction_fidelity": [], "subspace_fidelity": {}}

            print(f"\n  Head {h} — Projection Fidelity:")

            for cat_a, cat_b in contrasts:
                res_dir = difference_of_means(residual, categories, cat_a, cat_b)
                k_dir = difference_of_means(k_act, categories, cat_a, cat_b)
                v_dir = difference_of_means(v_act, categories, cat_a, cat_b)

                if res_dir is None or k_dir is None or v_dir is None:
                    continue

                k_cos, k_p, k_null = projection_fidelity(res_dir, W_K_head, k_dir)
                v_cos, v_p, v_null = projection_fidelity(res_dir, W_V_head, v_dir)

                print(f"    {cat_a} vs {cat_b}:")
                print(f"      K: cos={k_cos:.4f}, p={k_p:.4f}, null_mean={k_null:.4f} {'***' if k_p < 0.01 else ''}")
                print(f"      V: cos={v_cos:.4f}, p={v_p:.4f}, null_mean={v_null:.4f} {'***' if v_p < 0.01 else ''}")

                head_result["direction_fidelity"].append({
                    "contrast": f"{cat_a}_vs_{cat_b}",
                    "k_cosine": float(k_cos), "k_pvalue": float(k_p),
                    "v_cosine": float(v_cos), "v_pvalue": float(v_p),
                })

            # Subspace fidelity (top-5 PCA)
            k_pca_dirs, k_explained, _, _ = emotion_pca(k_act, categories, k=min(5, head_dim))
            v_pca_dirs, v_explained, _, _ = emotion_pca(v_act, categories, k=min(5, head_dim))

            k_sub_cos, k_sub_p, k_sub_null = subspace_fidelity(pca_dirs, W_K_head, k_pca_dirs)
            v_sub_cos, v_sub_p, v_sub_null = subspace_fidelity(pca_dirs, W_V_head, v_pca_dirs)

            print(f"    Subspace (top-5 PCA):")
            print(f"      K: mean_cos={k_sub_cos:.4f}, p={k_sub_p:.4f}, null={k_sub_null:.4f} {'***' if k_sub_p < 0.01 else ''}")
            print(f"      V: mean_cos={v_sub_cos:.4f}, p={v_sub_p:.4f}, null={v_sub_null:.4f} {'***' if v_sub_p < 0.01 else ''}")

            head_result["subspace_fidelity"] = {
                "k_mean_cos": float(k_sub_cos), "k_pvalue": float(k_sub_p),
                "v_mean_cos": float(v_sub_cos), "v_pvalue": float(v_sub_p),
            }

            layer_result["heads"].append(head_result)

        results["layers"].append(layer_result)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    n_sig_k = 0
    n_sig_v = 0
    n_total = 0
    for lr in results["layers"]:
        for hr in lr["heads"]:
            for df in hr["direction_fidelity"]:
                n_total += 1
                if df["k_pvalue"] < 0.01:
                    n_sig_k += 1
                if df["v_pvalue"] < 0.01:
                    n_sig_v += 1

    bonferroni = 0.05 / max(n_total, 1)
    n_bonf_k = sum(1 for lr in results["layers"] for hr in lr["heads"]
                    for df in hr["direction_fidelity"] if df["k_pvalue"] < bonferroni)
    n_bonf_v = sum(1 for lr in results["layers"] for hr in lr["heads"]
                    for df in hr["direction_fidelity"] if df["v_pvalue"] < bonferroni)

    print(f"Total direction tests: {n_total}")
    print(f"K-space significant (p<0.01): {n_sig_k}/{n_total}")
    print(f"V-space significant (p<0.01): {n_sig_v}/{n_total}")
    print(f"K-space Bonferroni ({bonferroni:.4f}): {n_bonf_k}/{n_total}")
    print(f"V-space Bonferroni ({bonferroni:.4f}): {n_bonf_v}/{n_total}")

    if n_bonf_k > 0 or n_bonf_v > 0:
        print("\nVERDICT: Emotion directions SURVIVE projection at some layers/heads.")
        print("Proceed to Phase 4 (intervention test).")
    elif n_sig_k > 0 or n_sig_v > 0:
        print("\nVERDICT: Weak signal — survives uncorrected but not Bonferroni.")
        print("Proceed with caution. May need more prompts or different contrasts.")
    else:
        print("\nVERDICT: No projection fidelity detected. The residual→K/V architecture")
        print("is NOT supported for emotion monitoring on this model.")

    outpath = Path(args.output)
    outpath.write_text(json.dumps(results, indent=2))
    print(f"\nSaved to {outpath}")


if __name__ == "__main__":
    main()
