"""Permutation baseline for trajectory shape validation.

Shuffles emotion labels 1000 times and reruns the trajectory analysis.
Reports the null distribution of separation and direction strength at each layer.
If the real trajectory falls outside the null envelope, the shape is meaningful.

No model inference needed — pure numpy on existing activations.

Usage:
  python permutation_baseline.py --activations sweep_activations.npz --model-dir /path/to/model --n-perms 1000
"""

import argparse
import json
from pathlib import Path

import numpy as np


def direction_strength(activations, categories, cat_a, cat_b):
    mask_a = categories == cat_a
    mask_b = categories == cat_b
    if mask_a.sum() < 2 or mask_b.sum() < 2:
        return 0.0
    mean_a = activations[mask_a].mean(axis=0)
    mean_b = activations[mask_b].mean(axis=0)
    diff = mean_a - mean_b
    var_a = activations[mask_a].var(axis=0)
    var_b = activations[mask_b].var(axis=0)
    pooled = np.sqrt((var_a + var_b) / 2)
    return float(np.abs(diff / (pooled + 1e-10)).mean())


def cluster_separation(activations, categories):
    cats = [c for c in np.unique(categories) if c != "neutral"]
    if len(cats) < 2:
        return 0.0
    X = activations[np.isin(categories, cats)]
    cats_f = categories[np.isin(categories, cats)]
    X_c = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(X_c, full_matrices=False)
    scores = U[:, :2] * S[:2]
    centroids = {c: scores[cats_f == c].mean(axis=0) for c in cats}
    between = np.var([centroids[c] for c in cats], axis=0).sum()
    within = np.mean([np.var(scores[cats_f == c], axis=0).sum() for c in cats])
    return float(between / (within + 1e-10))


def run_trajectory(data, categories, all_layers):
    seps = []
    vals = []
    aros = []
    for l in all_layers:
        res = data[f"residual_L{l}"]
        seps.append(cluster_separation(res, categories))
        vals.append(direction_strength(res, categories, "hostile", "calm"))
        aros.append(direction_strength(res, categories, "desperate", "calm"))
    return np.array(seps), np.array(vals), np.array(aros)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activations", required=True)
    parser.add_argument("--n-perms", type=int, default=1000)
    parser.add_argument("--output", default="permutation_results.json")
    args = parser.parse_args()

    data = np.load(args.activations, allow_pickle=True)
    categories = data["categories"]
    n_layers = int(data["n_layers"])
    all_layers = list(range(n_layers))

    print(f"Loaded: {len(categories)} prompts, {n_layers} layers")
    print(f"Running {args.n_perms} permutations...")

    # Real trajectory
    real_seps, real_vals, real_aros = run_trajectory(data, categories, all_layers)

    # Permutation null
    rng = np.random.RandomState(42)
    null_seps = np.zeros((args.n_perms, n_layers))
    null_vals = np.zeros((args.n_perms, n_layers))
    null_aros = np.zeros((args.n_perms, n_layers))

    for i in range(args.n_perms):
        if i % 100 == 0:
            print(f"  Permutation {i}/{args.n_perms}...")
        shuffled = rng.permutation(categories)
        s, v, a = run_trajectory(data, shuffled, all_layers)
        null_seps[i] = s
        null_vals[i] = v
        null_aros[i] = a

    # Compute p-values per layer
    results = {"layers": []}
    for i, l in enumerate(all_layers):
        sep_p = float((null_seps[:, i] >= real_seps[i]).mean())
        val_p = float((null_vals[:, i] >= real_vals[i]).mean())
        aro_p = float((null_aros[:, i] >= real_aros[i]).mean())

        results["layers"].append({
            "layer": l,
            "separation": {"real": float(real_seps[i]),
                           "null_mean": float(null_seps[:, i].mean()),
                           "null_95": float(np.percentile(null_seps[:, i], 95)),
                           "p": sep_p},
            "valence_d": {"real": float(real_vals[i]),
                          "null_mean": float(null_vals[:, i].mean()),
                          "null_95": float(np.percentile(null_vals[:, i], 95)),
                          "p": val_p},
            "arousal_d": {"real": float(real_aros[i]),
                          "null_mean": float(null_aros[:, i].mean()),
                          "null_95": float(np.percentile(null_aros[:, i], 95)),
                          "p": aro_p},
        })

    # Print summary
    print(f"\n{'='*70}")
    print(f"PERMUTATION BASELINE — {args.n_perms} shuffles")
    print(f"{'='*70}")
    print(f"{'Layer':>5} {'Sep':>7} {'Null95':>7} {'p':>7} │ {'Val-d':>7} {'p':>7} │ {'Aro-d':>7} {'p':>7}")
    print(f"{'─'*5} {'─'*7} {'─'*7} {'─'*7} │ {'─'*7} {'─'*7} │ {'─'*7} {'─'*7}")

    sig_layers = 0
    for r in results["layers"]:
        l = r["layer"]
        s = r["separation"]
        v = r["valence_d"]
        a = r["arousal_d"]
        sig = " ***" if s["p"] < 0.001 and v["p"] < 0.001 else " **" if s["p"] < 0.01 else ""
        if s["p"] < 0.05:
            sig_layers += 1
        print(f"{l:>5} {s['real']:>7.3f} {s['null_95']:>7.3f} {s['p']:>7.3f} │ {v['real']:>7.3f} {v['p']:>7.3f} │ {a['real']:>7.3f} {a['p']:>7.3f}{sig}")

    print(f"\nLayers with significant separation (p<0.05): {sig_layers}/{n_layers}")

    # Effect size ratios (real / null_95th) — more informative than p-values
    print(f"\nEffect size ratios (real / null 95th percentile):")
    ratios = []
    for i, l in enumerate(all_layers):
        null95 = np.percentile(null_seps[:, i], 95)
        ratio = real_seps[i] / (null95 + 1e-10)
        ratios.append(ratio)
    print(f"  Range: {min(ratios):.1f}x - {max(ratios):.1f}x")
    print(f"  Mean: {np.mean(ratios):.1f}x")

    # Trajectory feature comparison (not ad hoc shape correlation)
    # Compare: onset layer, peak layer, plateau mean, spike magnitude
    def trajectory_features(seps):
        onset = next((i for i, s in enumerate(seps) if s > 0.1 * seps.max()), 0)
        peak = int(np.argmax(seps))
        plateau = float(np.mean(seps[max(1, onset):max(2, peak)]))
        spike = float(seps[peak])
        return onset, peak, plateau, spike

    real_features = trajectory_features(real_seps)
    null_features = [trajectory_features(null_seps[i]) for i in range(args.n_perms)]

    print(f"\nTrajectory features:")
    print(f"  Real: onset=L{real_features[0]}, peak=L{real_features[1]}, "
          f"plateau={real_features[2]:.3f}, spike={real_features[3]:.3f}")
    null_onsets = [f[0] for f in null_features]
    null_peaks = [f[1] for f in null_features]
    null_plateaus = [f[2] for f in null_features]
    null_spikes = [f[3] for f in null_features]
    print(f"  Null onset: mean=L{np.mean(null_onsets):.0f} (std={np.std(null_onsets):.1f})")
    print(f"  Null peak: mean=L{np.mean(null_peaks):.0f} (std={np.std(null_peaks):.1f})")
    print(f"  Null plateau: mean={np.mean(null_plateaus):.4f} (std={np.std(null_plateaus):.4f})")
    print(f"  Null spike: mean={np.mean(null_spikes):.4f} (std={np.std(null_spikes):.4f})")

    # Feature-based distinctness: how many SDs is each real feature from null mean?
    def zscore(real, null_vals):
        return (real - np.mean(null_vals)) / (np.std(null_vals) + 1e-10)

    z_plateau = zscore(real_features[2], null_plateaus)
    z_spike = zscore(real_features[3], null_spikes)
    print(f"\n  Plateau z-score: {z_plateau:.1f} SDs from null")
    print(f"  Spike z-score: {z_spike:.1f} SDs from null")

    if z_plateau > 3 and z_spike > 3:
        print("  PASS: Both plateau and spike are >3 SDs from null")
    elif z_plateau > 2 or z_spike > 2:
        print("  PARTIAL: Some features >2 SDs from null")
    else:
        print("  FAIL: Features are within null range")

    results["effect_ratios"] = {"range": [float(min(ratios)), float(max(ratios))], "mean": float(np.mean(ratios))}
    results["trajectory_features"] = {
        "real": {"onset": real_features[0], "peak": real_features[1],
                 "plateau": float(real_features[2]), "spike": float(real_features[3])},
        "null_mean": {"onset": float(np.mean(null_onsets)), "peak": float(np.mean(null_peaks)),
                      "plateau": float(np.mean(null_plateaus)), "spike": float(np.mean(null_spikes))},
        "z_scores": {"plateau": float(z_plateau), "spike": float(z_spike)},
    }

    outpath = Path(args.output)
    outpath.write_text(json.dumps(results, indent=2))
    print(f"\nSaved to {outpath}")


if __name__ == "__main__":
    main()
