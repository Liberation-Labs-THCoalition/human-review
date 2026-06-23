"""Three diagnostic tests using existing data — no new experiments needed.

Test 1: W_unembed alignment at deep layers
  Do top PCA components at L23 align with unembedding rows?
  If yes → deep-layer spike is output preparation, not emotion.

Test 2: Calm-vs-outdoor clustering at mid-layers
  Does calm cluster with outdoor (shared nature vocabulary)?
  Or with hostile/desperate (shared emotional valence)?
  Diagnostic for vocabulary vs emotion confound.

Test 3: K/V divergence on non-emotional content at deep layers
  Does K/V diverge equally for control categories at L21-23?
  If yes → divergence is architectural, not emotional.

Usage:
  python diagnostic_tests.py --model-dir Qwen/Qwen2.5-0.5B-Instruct
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def extract_all_layers(model, tokenizer, prompts, device="cpu"):
    n_layers = model.config.num_hidden_layers
    n_kv = model.config.num_key_value_heads
    hidden_dim = model.config.hidden_size
    head_dim = hidden_dim // model.config.num_attention_heads

    results = {"token_counts": []}
    for l in range(n_layers):
        results[f"residual_L{l}"] = []
        for h in range(n_kv):
            results[f"k_L{l}_H{h}"] = []
            results[f"v_L{l}_H{h}"] = []

    captured_residuals = {}
    captured_k = {}
    captured_v = {}
    hooks = []

    def make_residual_hook(layer_idx):
        def hook_fn(module, args, kwargs):
            hidden = args[0] if args else kwargs.get("hidden_states")
            if hidden is not None:
                captured_residuals[layer_idx] = hidden.detach()
            return None
        return hook_fn

    def make_k_hook(layer_idx):
        def hook_fn(module, input, output):
            captured_k[layer_idx] = output.detach()
        return hook_fn

    def make_v_hook(layer_idx):
        def hook_fn(module, input, output):
            captured_v[layer_idx] = output.detach()
        return hook_fn

    for l in range(n_layers):
        layer = model.model.layers[l]
        hooks.append(layer.register_forward_pre_hook(make_residual_hook(l), with_kwargs=True))
        hooks.append(layer.self_attn.k_proj.register_forward_hook(make_k_hook(l)))
        hooks.append(layer.self_attn.v_proj.register_forward_hook(make_v_hook(l)))

    for i, prompt in enumerate(prompts):
        if i % 25 == 0:
            print(f"  Extracting {i}/{len(prompts)}...")
        inputs = tokenizer(prompt, return_tensors="pt", padding=False).to(device)
        results["token_counts"].append(inputs["input_ids"].shape[1])

        with torch.no_grad():
            model(**inputs)

        for l in range(n_layers):
            res = captured_residuals[l][0, -1, :].cpu().float().numpy()
            results[f"residual_L{l}"].append(res)
            k_full = captured_k[l][0, -1, :].cpu().float().numpy()
            v_full = captured_v[l][0, -1, :].cpu().float().numpy()
            for h in range(n_kv):
                results[f"k_L{l}_H{h}"].append(k_full[h * head_dim:(h + 1) * head_dim])
                results[f"v_L{l}_H{h}"].append(v_full[h * head_dim:(h + 1) * head_dim])

        captured_residuals.clear()
        captured_k.clear()
        captured_v.clear()

    for h in hooks:
        h.remove()
    for key in results:
        results[key] = np.array(results[key])
    return results


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def cluster_separation_2d(activations, categories, target_cats):
    mask = np.isin(categories, target_cats)
    X = activations[mask]
    cats = categories[mask]
    X_c = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(X_c, full_matrices=False)
    scores = U[:, :2] * S[:2]
    centroids = {c: scores[cats == c].mean(axis=0) for c in target_cats}
    between = np.var([centroids[c] for c in target_cats], axis=0).sum()
    within = np.mean([np.var(scores[cats == c], axis=0).sum() for c in target_cats])
    return float(between / (within + 1e-10))


def test_1_unembed_alignment(model, data, n_layers):
    """Test 1: Do top PCA components at deep layers align with W_unembed?"""
    print("\n" + "=" * 70)
    print("TEST 1: W_unembed alignment at deep layers")
    print("=" * 70)

    W_unembed = model.lm_head.weight.detach().cpu().float().numpy()  # [vocab, hidden]

    top_unembed_dirs = []
    U_e, S_e, Vt_e = np.linalg.svd(W_unembed, full_matrices=False)
    for i in range(10):
        top_unembed_dirs.append(Vt_e[i])

    print(f"W_unembed shape: {W_unembed.shape}")
    print(f"Top 10 singular values: {S_e[:10].round(1)}")

    for l in [6, 12, 18, 21, 22, 23]:
        res = data[f"residual_L{l}"]
        X_c = res - res.mean(axis=0)
        U, S, Vt = np.linalg.svd(X_c, full_matrices=False)

        alignments = []
        for pc_idx in range(5):
            pc = Vt[pc_idx]
            max_align = max(abs(cosine(pc, ud)) for ud in top_unembed_dirs)
            alignments.append(max_align)

        mean_align = np.mean(alignments)
        max_align = np.max(alignments)
        print(f"  L{l:2d}: mean_align={mean_align:.3f}  max_align={max_align:.3f}  "
              f"per-PC=[{', '.join(f'{a:.3f}' for a in alignments)}]")

    print("\nInterpretation: If deep-layer alignment >> mid-layer alignment,")
    print("the spike is output preparation. If similar, it's content-driven.")


def test_2_calm_vs_outdoor(data, emo_cats, ctrl_cats, n_layers):
    """Test 2: Does calm cluster with outdoor or with hostile/desperate?"""
    print("\n" + "=" * 70)
    print("TEST 2: Calm-vs-outdoor clustering at mid-layers")
    print("=" * 70)

    all_cats = np.concatenate([emo_cats, ctrl_cats])
    mid_layers = [8, 10, 12, 14, 16, 18]

    for l in mid_layers:
        emo_res = data["emo"][f"residual_L{l}"]
        ctrl_res = data["ctrl"][f"residual_L{l}"]
        all_res = np.concatenate([emo_res, ctrl_res], axis=0)

        calm_mask = all_cats == "calm"
        outdoor_mask = all_cats == "outdoor"
        hostile_mask = all_cats == "hostile"
        desperate_mask = all_cats == "desperate"

        calm_centroid = all_res[calm_mask].mean(axis=0)
        outdoor_centroid = all_res[outdoor_mask].mean(axis=0)
        hostile_centroid = all_res[hostile_mask].mean(axis=0)
        desperate_centroid = all_res[desperate_mask].mean(axis=0)

        calm_outdoor = cosine(calm_centroid, outdoor_centroid)
        calm_hostile = cosine(calm_centroid, hostile_centroid)
        calm_desperate = cosine(calm_centroid, desperate_centroid)
        hostile_desperate = cosine(hostile_centroid, desperate_centroid)

        # Distance-based (L2)
        d_calm_outdoor = float(np.linalg.norm(calm_centroid - outdoor_centroid))
        d_calm_hostile = float(np.linalg.norm(calm_centroid - hostile_centroid))
        d_calm_desperate = float(np.linalg.norm(calm_centroid - desperate_centroid))

        print(f"  L{l:2d}: calm↔outdoor={calm_outdoor:.3f}  calm↔hostile={calm_hostile:.3f}  "
              f"calm↔desperate={calm_desperate:.3f}  hostile↔desperate={hostile_desperate:.3f}")
        print(f"        L2: calm→outdoor={d_calm_outdoor:.2f}  "
              f"calm→hostile={d_calm_hostile:.2f}  calm→desperate={d_calm_desperate:.2f}")

    print("\nInterpretation: If calm is CLOSER to outdoor (shared vocabulary) than to")
    print("hostile/desperate, vocabulary drives the separation. If calm is closer to")
    print("other emotions despite vocabulary dissimilarity, emotion drives it.")


def test_3_kv_divergence(data_emo, data_ctrl, emo_cats, ctrl_cats, n_layers, n_kv):
    """Test 3: Does K/V diverge for non-emotional content at deep layers?"""
    print("\n" + "=" * 70)
    print("TEST 3: K/V divergence — emotional vs non-emotional at deep layers")
    print("=" * 70)

    def kv_divergence(data, categories, target_cats, layer, n_kv):
        mask = np.isin(categories, target_cats)
        divs = []
        for h in range(n_kv):
            k = data[f"k_L{layer}_H{h}"][mask]
            v = data[f"v_L{layer}_H{h}"][mask]

            k_sep = cluster_separation_2d(k, categories[mask], target_cats)
            v_sep = cluster_separation_2d(v, categories[mask], target_cats)
            divs.append(abs(k_sep - v_sep))
        return np.mean(divs), divs

    emo_targets = ["hostile", "calm", "desperate"]
    ctrl_targets = ["outdoor", "indoor", "urban", "workplace"]

    print(f"  {'Layer':>6} │ {'Emo K/V div':>12} │ {'Ctrl K/V div':>13} │ {'Ratio':>6}")
    print(f"  {'─' * 6}─┼─{'─' * 12}─┼─{'─' * 13}─┼─{'─' * 6}")

    for l in [12, 15, 18, 20, 21, 22, 23]:
        emo_div, emo_per_h = kv_divergence(data_emo, emo_cats, emo_targets, l, n_kv)
        ctrl_div, ctrl_per_h = kv_divergence(data_ctrl, ctrl_cats, ctrl_targets, l, n_kv)
        ratio = emo_div / (ctrl_div + 1e-10)
        print(f"  L{l:2d}    │ {emo_div:12.4f} │ {ctrl_div:13.4f} │ {ratio:6.2f}")

    print("\nInterpretation: If ratio ≈ 1 at deep layers, K/V divergence is architectural.")
    print("If ratio >> 1, there's emotion-specific K/V divergence.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--output", default=None, help="Save activations to .npz")
    args = parser.parse_args()

    data_dir = Path(__file__).parent.parent / "data"
    emo_stimuli = json.loads((data_dir / "stimuli.json").read_text())
    ctrl_stimuli = json.loads((data_dir / "control_stimuli.json").read_text())

    emo_prompts = [s["prompt"] for s in emo_stimuli]
    emo_cats = np.array([s["category"] for s in emo_stimuli])
    ctrl_prompts = [s["prompt"] for s in ctrl_stimuli]
    ctrl_cats = np.array([s["category"] for s in ctrl_stimuli])

    print(f"Emotional: {len(emo_prompts)} prompts, categories: {np.unique(emo_cats)}")
    print(f"Control: {len(ctrl_prompts)} prompts, categories: {np.unique(ctrl_cats)}")

    print(f"\nLoading model: {args.model_dir}")
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, torch_dtype=torch.float32, trust_remote_code=True)
    model.eval()

    n_layers = model.config.num_hidden_layers
    n_kv = model.config.num_key_value_heads

    print(f"\nExtracting emotional stimuli ({len(emo_prompts)} prompts, {n_layers} layers)...")
    emo_data = extract_all_layers(model, tokenizer, emo_prompts, args.device)

    print(f"\nExtracting control stimuli ({len(ctrl_prompts)} prompts, {n_layers} layers)...")
    ctrl_data = extract_all_layers(model, tokenizer, ctrl_prompts, args.device)

    if args.output:
        combined = {}
        for k, v in emo_data.items():
            combined[f"emo_{k}"] = v
        for k, v in ctrl_data.items():
            combined[f"ctrl_{k}"] = v
        combined["emo_categories"] = emo_cats
        combined["ctrl_categories"] = ctrl_cats
        np.savez_compressed(args.output, **combined)
        print(f"\nActivations saved to {args.output}")

    # Run tests
    test_1_unembed_alignment(model, emo_data, n_layers)

    combined_data = {"emo": emo_data, "ctrl": ctrl_data}
    test_2_calm_vs_outdoor(combined_data, emo_cats, ctrl_cats, n_layers)
    test_3_kv_divergence(emo_data, ctrl_data, emo_cats, ctrl_cats, n_layers, n_kv)

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
