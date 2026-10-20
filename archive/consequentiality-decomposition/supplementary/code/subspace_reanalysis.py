#!/usr/bin/env python3
"""Deception Subspace Reanalysis — LOO-Corrected.

Fixes the FATAL circularity from the original subspace experiment:
the permutation test held the direction fixed and shuffled projections,
producing 100% false positive rate. This reanalysis implements full LOO
direction extraction + orthogonalization for both d and permutation test.

Also replaces the tautological conseq d=0.000 sanity check with AUC
on individual trial separability.

Runs on saved raw_activations.pt — no new forward passes needed.

FIXES (from Agni Stage 5 audit):
1. LOO direction extraction: for each fold i, extract threat direction
   from n-1 pairs, orthogonalize against full-data conseq direction,
   project held-out pair i.
2. LOO permutation test: for each permutation, shuffle labels, re-extract
   direction, orthogonalize, compute LOO d. 10,000 permutations.
3. Replace tautological sanity check with AUC for conseq separation.
4. Report noise floor alongside d values.
"""

import json
import numpy as np
import torch
from pathlib import Path
from datetime import datetime
from sklearn.metrics import roc_auc_score

ACTIVATIONS_PATH = Path("/home/asdf/oracle-harness/experiments/results/subspace_raw_activations.pt")
LAT_V2_PATH = Path("/home/asdf/oracle-harness/experiments/results/lat_deception_v2.json")
RESULTS_PATH = Path("/home/asdf/oracle-harness/experiments/results/subspace_reanalysis.json")

LATE_LAYERS = [31, 35, 39, 43, 47]
N_PERMS = 10000


def loo_orthogonalized_d(dec_arr, hon_arr, conseq_dir):
    """LOO cross-validated d on direction orthogonalized against conseq_dir.

    For each fold i:
    1. Extract threat direction from n-1 pairs (excluding pair i)
    2. Orthogonalize against conseq_dir (Gram-Schmidt)
    3. Project held-out pair i onto orthogonalized direction
    Returns LOO d and the paired projections.
    """
    n = min(len(dec_arr), len(hon_arr))
    loo_dec_proj = []
    loo_hon_proj = []

    for i in range(n):
        train_dec = np.delete(dec_arr[:n], i, axis=0)
        train_hon = np.delete(hon_arr[:n], i, axis=0)

        # Extract direction from training fold
        direction = train_dec.mean(axis=0) - train_hon.mean(axis=0)

        # Orthogonalize against consequentiality
        direction = direction - np.dot(direction, conseq_dir) * conseq_dir
        d_norm = np.linalg.norm(direction)
        if d_norm < 1e-8:
            continue
        direction = direction / d_norm

        # Project held-out pair
        loo_dec_proj.append(np.dot(dec_arr[i], direction))
        loo_hon_proj.append(np.dot(hon_arr[i], direction))

    if len(loo_dec_proj) < 5:
        return 0.0, [], []

    dec_p = np.array(loo_dec_proj)
    hon_p = np.array(loo_hon_proj)
    pooled = np.sqrt((np.var(dec_p) + np.var(hon_p)) / 2)
    d = (np.mean(dec_p) - np.mean(hon_p)) / pooled if pooled > 1e-12 else 0
    return float(d), dec_p.tolist(), hon_p.tolist()


def loo_permutation_test(dec_arr, hon_arr, conseq_dir, observed_d, n_perms):
    """Full LOO recomputation per permutation (two-tailed).

    For each permutation:
    1. Shuffle condition labels across all 2n activations
    2. Re-extract direction via LOO from shuffled data
    3. Orthogonalize against conseq_dir
    4. Compute LOO d
    Compare abs(permuted_d) >= abs(observed_d).
    """
    n = min(len(dec_arr), len(hon_arr))
    all_acts = np.concatenate([dec_arr[:n], hon_arr[:n]], axis=0)
    abs_observed = abs(observed_d)
    count = 0

    for perm_idx in range(n_perms):
        perm = np.random.permutation(2 * n)
        perm_dec = all_acts[perm[:n]]
        perm_hon = all_acts[perm[n:]]

        # LOO with shuffled data
        perm_dec_proj = []
        perm_hon_proj = []
        for i in range(n):
            t_dec = np.delete(perm_dec, i, axis=0)
            t_hon = np.delete(perm_hon, i, axis=0)
            pdir = t_dec.mean(axis=0) - t_hon.mean(axis=0)
            # Orthogonalize
            pdir = pdir - np.dot(pdir, conseq_dir) * conseq_dir
            pn = np.linalg.norm(pdir)
            if pn < 1e-8:
                continue
            pdir = pdir / pn
            perm_dec_proj.append(np.dot(perm_dec[i], pdir))
            perm_hon_proj.append(np.dot(perm_hon[i], pdir))

        if len(perm_dec_proj) < 5:
            continue
        pd = np.array(perm_dec_proj)
        ph = np.array(perm_hon_proj)
        pp = np.sqrt((np.var(pd) + np.var(ph)) / 2)
        perm_d = (np.mean(pd) - np.mean(ph)) / pp if pp > 1e-12 else 0
        if abs(perm_d) >= abs_observed:
            count += 1

        if (perm_idx + 1) % 1000 == 0:
            print(f"      perm [{perm_idx+1}/{n_perms}] count={count}", flush=True)

    return count / n_perms


def conseq_auc(acts_high, acts_low, direction):
    """AUC for separating conseq_high from conseq_low on a direction.
    Replaces the tautological d=0 sanity check."""
    n = min(len(acts_high), len(acts_low))
    projs_high = [np.dot(a, direction) for a in acts_high[:n]]
    projs_low = [np.dot(a, direction) for a in acts_low[:n]]
    labels = [1] * n + [0] * n
    scores = projs_high + projs_low
    try:
        return roc_auc_score(labels, scores)
    except Exception:
        return 0.5


if __name__ == "__main__":
    print("=" * 70, flush=True)
    print("DECEPTION SUBSPACE REANALYSIS — LOO-CORRECTED", flush=True)
    print(f"Started: {datetime.now().isoformat()}", flush=True)
    print("=" * 70, flush=True)

    # Load data
    print("\nLoading raw activations...", flush=True)
    raw = torch.load(ACTIVATIONS_PATH, map_location="cpu", weights_only=False)
    print("  Conditions:", list(raw.keys()), flush=True)
    for k, v in raw.items():
        for li, arr in v.items():
            print(f"  {k} L{li}: {arr.shape}", flush=True)
            break

    # Load LAT v2 directions for cosine comparison
    with open(LAT_V2_PATH) as f:
        lat_v2 = json.load(f)
    lat_dirs = {int(k): np.array(v["direction"]) for k, v in lat_v2.items()}

    # Compute noise floor via simulation
    print("\nEstimating circular-d noise floor (n=50, dim=5120)...", flush=True)
    noise_ds = []
    for _ in range(200):
        fake_dec = np.random.randn(50, 5120)
        fake_hon = np.random.randn(50, 5120)
        fake_dir = fake_dec.mean(axis=0) - fake_hon.mean(axis=0)
        fn = np.linalg.norm(fake_dir)
        if fn > 0:
            fake_dir /= fn
        fp_d = [np.dot(fake_dec[i], fake_dir) for i in range(50)]
        fp_h = [np.dot(fake_hon[i], fake_dir) for i in range(50)]
        pp = np.sqrt((np.var(fp_d) + np.var(fp_h)) / 2)
        if pp > 0:
            noise_ds.append((np.mean(fp_d) - np.mean(fp_h)) / pp)
    noise_mean = np.mean(noise_ds)
    noise_99 = np.percentile(noise_ds, 99)
    print(f"  Circular-d noise floor: mean={noise_mean:.1f}, 99th={noise_99:.1f}", flush=True)

    # Also estimate LOO noise floor
    print("Estimating LOO-d noise floor...", flush=True)
    loo_noise_ds = []
    fake_conseq = np.random.randn(5120)
    fake_conseq /= np.linalg.norm(fake_conseq)
    for _ in range(200):
        fake_dec = np.random.randn(50, 5120)
        fake_hon = np.random.randn(50, 5120)
        d_loo, _, _ = loo_orthogonalized_d(fake_dec, fake_hon, fake_conseq)
        loo_noise_ds.append(d_loo)
    loo_noise_mean = np.mean(loo_noise_ds)
    loo_noise_99 = np.percentile(np.abs(loo_noise_ds), 99)
    print(f"  LOO-d noise floor: mean={loo_noise_mean:.3f}, |99th|={loo_noise_99:.3f}", flush=True)

    # Main analysis
    results = {}
    bonf_alpha = 0.05 / len(LATE_LAYERS)

    for li in LATE_LAYERS:
        print(f"\n{'='*50}", flush=True)
        print(f"  LAYER {li}", flush=True)
        print(f"{'='*50}", flush=True)

        td = np.array(raw["threat_dec"][li])
        th = np.array(raw["threat_hon"][li])
        ch = np.array(raw["conseq_high"][li])
        cl = np.array(raw["conseq_low"][li])
        n = min(len(td), len(th), len(ch), len(cl))
        print(f"  n={n} pairs per condition", flush=True)

        # Consequentiality direction (from full conseq data — independent of threat)
        conseq_dir_raw = ch[:n].mean(axis=0) - cl[:n].mean(axis=0)
        conseq_norm = np.linalg.norm(conseq_dir_raw)
        conseq_dir = conseq_dir_raw / conseq_norm if conseq_norm > 1e-8 else conseq_dir_raw

        # Full-data threat direction (for cosine comparison only)
        full_threat_raw = td[:n].mean(axis=0) - th[:n].mean(axis=0)
        full_threat_orth = full_threat_raw - np.dot(full_threat_raw, conseq_dir) * conseq_dir
        fto_norm = np.linalg.norm(full_threat_orth)
        full_threat_orth_unit = full_threat_orth / fto_norm if fto_norm > 1e-8 else full_threat_orth

        raw_cos = np.dot(
            full_threat_raw / np.linalg.norm(full_threat_raw),
            conseq_dir
        )
        print(f"  Raw cosine (threat, conseq): {raw_cos:.4f}", flush=True)

        # LOO cross-validated d on orthogonalized direction
        print(f"  Computing LOO d...", flush=True)
        loo_d, dec_proj, hon_proj = loo_orthogonalized_d(td, th, conseq_dir)
        print(f"  LOO d (orthogonalized): {loo_d:.3f}", flush=True)

        # AUC sanity check: does the orthogonalized direction separate conseq?
        conseq_auc_val = conseq_auc(ch[:n], cl[:n], full_threat_orth_unit)
        print(f"  Conseq AUC (orthogonalized): {conseq_auc_val:.3f} (should be ~0.50)", flush=True)

        # LOO permutation test (the expensive part)
        print(f"  Running LOO permutation test ({N_PERMS} shuffles)...", flush=True)
        p_perm = loo_permutation_test(td, th, conseq_dir, loo_d, N_PERMS)
        sig = "***" if p_perm < bonf_alpha else ""
        print(f"  LOO perm p={p_perm:.4f} {sig}", flush=True)

        # Cosine with LAT v2
        cos_lat = np.dot(full_threat_orth_unit, lat_dirs[li]) if li in lat_dirs else 0
        print(f"  Cosine (orth direction, LAT v2): {cos_lat:.4f}", flush=True)

        # Signal above noise
        signal_above_noise = loo_d - loo_noise_mean
        print(f"  LOO d above noise floor: {signal_above_noise:.3f}", flush=True)

        results[li] = {
            "loo_d": float(loo_d),
            "p_perm": float(p_perm),
            "conseq_auc": float(conseq_auc_val),
            "cosine_lat_v2": float(cos_lat),
            "raw_cosine_threat_conseq": float(raw_cos),
            "noise_floor_loo_mean": float(loo_noise_mean),
            "signal_above_noise": float(signal_above_noise),
            "n": n,
            "loo_dec_proj": dec_proj,
            "loo_hon_proj": hon_proj,
        }

    # Summary
    print(f"\n{'='*70}", flush=True)
    print("SUMMARY — LOO-CORRECTED ORTHOGONALIZED DECEPTION DIRECTION", flush=True)
    print(f"Bonferroni alpha = {bonf_alpha:.4f}", flush=True)
    print(f"LOO noise floor: mean={loo_noise_mean:.3f}", flush=True)
    print(f"{'='*70}", flush=True)

    print(f"\n{'Layer':>5} | {'LOO d':>8} | {'p_perm':>8} | {'sig':>5} | {'AUC_cq':>7} | {'cos_LAT':>8} | {'above_noise':>12}")
    print("-" * 70)
    passes = 0
    for li in LATE_LAYERS:
        r = results[li]
        sig = "***" if r["p_perm"] < bonf_alpha else ""
        print(f"L{li:>3} | {r['loo_d']:>8.3f} | {r['p_perm']:>8.4f} | {sig:>5} | {r['conseq_auc']:>7.3f} | {r['cosine_lat_v2']:>8.4f} | {r['signal_above_noise']:>12.3f}")
        if r["p_perm"] < bonf_alpha:
            passes += 1

    print(f"\nPasses: {passes}/5 (need >=3 for pre-registered success)")

    if passes >= 3:
        print("\nRESULT: DECEPTION-SPECIFIC COMPONENT CONFIRMED.")
        print("The orthogonalized direction separates threat deception from")
        print("honest conditions after removing the consequentiality component.")
        print("LOO cross-validation eliminates circularity. The direction")
        print("earns the label 'deception direction.'")
    else:
        print("\nRESULT: INSUFFICIENT EVIDENCE for deception-specific component.")
        print("The orthogonalized direction does not reliably separate after")
        print("LOO correction. Signal may be inflated by circularity.")

    # Save
    final = {
        "metadata": {
            "experiment": "subspace_reanalysis_loo",
            "date": datetime.now().isoformat(),
            "fixes": [
                "LOO direction extraction (Agni Stage 5 Fix 1)",
                "LOO permutation test with full recomputation",
                "AUC sanity check replacing tautological d=0 (Fix 2)",
                "Noise floor estimation and reporting (Fix 5)",
            ],
            "n_perms": N_PERMS,
            "bonferroni_alpha": float(bonf_alpha),
            "noise_floor_loo_mean": float(loo_noise_mean),
            "noise_floor_loo_99th": float(loo_noise_99),
            "noise_floor_circular_mean": float(noise_mean),
        },
        "results": {str(li): {k: v for k, v in r.items() if k not in ("loo_dec_proj", "loo_hon_proj")}
                    for li, r in results.items()},
        "loo_projections": {str(li): {"dec": r["loo_dec_proj"], "hon": r["loo_hon_proj"]}
                           for li, r in results.items()},
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(final, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}", flush=True)
    print(f"Finished: {datetime.now().isoformat()}", flush=True)
