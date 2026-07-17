#!/usr/bin/env python3
"""
Log-FWL (Frisch-Waugh-Lovell) re-analysis of mode-switching replication.

Auditor-requested control: generation length (gen_tokens) varies across trials
and may confound spectral features.  For each layer/matrix/feature, we:

  1. Compute raw Cohen's d between conditions.
  2. Regress log(gen_tokens) out of both the feature and the binary condition
     label (Frisch-Waugh-Lovell partialling), then recompute Cohen's d and a
     two-sided t-test on the residualized feature.
  3. Flag which layers survive Holm-Bonferroni correction at alpha=0.05.

Input:  trials.jsonl  (120 trials, 60 cognitive / 60 metacognitive)
Output: fwl_analysis.json
"""

import json, math, os, sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

LAYERS = [3, 7, 11, 15, 23, 31, 35, 43, 47]
MATRICES = ["k", "v"]
FEATURES = ["spectral_entropy", "eff_rank", "stable_rank"]
ALPHA = 0.05

DATA_DIR = Path(__file__).resolve().parent
TRIALS_PATH = DATA_DIR / "trials.jsonl"
OUTPUT_PATH = DATA_DIR / "fwl_analysis.json"


# ── helpers ──────────────────────────────────────────────────────────────

def cohens_d(a, b):
    """Pooled-SD Cohen's d (positive = a > b)."""
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    pooled = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled == 0:
        return 0.0
    return (np.mean(a) - np.mean(b)) / pooled


def ols_residuals(y, X):
    """OLS residuals of y on X (X should include intercept column)."""
    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return y - X @ beta


def holm_bonferroni(pvals, alpha=0.05):
    """Return boolean array: True where rejected after Holm-Bonferroni."""
    m = len(pvals)
    order = np.argsort(pvals)
    rejected = np.zeros(m, dtype=bool)
    for rank, idx in enumerate(order):
        if pvals[idx] <= alpha / (m - rank):
            rejected[idx] = True
        else:
            break
    return rejected


# ── load data ────────────────────────────────────────────────────────────

trials = []
with open(TRIALS_PATH) as f:
    for line in f:
        trials.append(json.loads(line))

n = len(trials)
assert n == 120, f"Expected 120 trials, got {n}"

conditions = np.array([1 if t["condition"] == "metacognitive" else 0 for t in trials])
log_gen = np.log(np.array([t["gen_tokens"] for t in trials], dtype=np.float64))

# Design matrix for partialling: [intercept, log(gen_tokens)]
X_partial = np.column_stack([np.ones(n), log_gen])

# ── analyse ──────────────────────────────────────────────────────────────

results_list = []

for layer in LAYERS:
    layer_str = str(layer)
    for mat in MATRICES:
        for feat in FEATURES:
            vals = np.array([t["features"][layer_str][mat][feat] for t in trials],
                            dtype=np.float64)

            # Raw split
            meta_vals = vals[conditions == 1]
            cog_vals = vals[conditions == 0]
            d_raw = cohens_d(meta_vals, cog_vals)
            t_raw, p_raw = stats.ttest_ind(meta_vals, cog_vals, equal_var=False)

            # FWL: residualize both feature and condition on log(gen_tokens)
            feat_resid = ols_residuals(vals, X_partial)
            cond_resid = ols_residuals(conditions.astype(np.float64), X_partial)

            # Split residualized feature by original condition labels
            meta_resid = feat_resid[conditions == 1]
            cog_resid = feat_resid[conditions == 0]
            d_fwl = cohens_d(meta_resid, cog_resid)
            t_fwl, p_fwl = stats.ttest_ind(meta_resid, cog_resid, equal_var=False)

            # Correlation between log(gen_tokens) and feature (confound strength)
            r_gen_feat = np.corrcoef(log_gen, vals)[0, 1]

            results_list.append({
                "layer": layer,
                "matrix": mat,
                "feature": feat,
                "d_raw": round(float(d_raw), 4),
                "p_raw": float(p_raw),
                "d_fwl": round(float(d_fwl), 4),
                "p_fwl": float(p_fwl),
                "d_delta": round(float(d_fwl - d_raw), 4),
                "r_gen_feat": round(float(r_gen_feat), 4),
            })

# Holm-Bonferroni across all tests
p_raw_all = np.array([r["p_raw"] for r in results_list])
p_fwl_all = np.array([r["p_fwl"] for r in results_list])
sig_raw = holm_bonferroni(p_raw_all, ALPHA)
sig_fwl = holm_bonferroni(p_fwl_all, ALPHA)

for i, r in enumerate(results_list):
    r["sig_raw_holm"] = bool(sig_raw[i])
    r["sig_fwl_holm"] = bool(sig_fwl[i])

# ── summarise ────────────────────────────────────────────────────────────

survivors = [r for r in results_list if r["sig_fwl_holm"]]
casualties = [r for r in results_list if r["sig_raw_holm"] and not r["sig_fwl_holm"]]

summary = {
    "n_trials": n,
    "n_cognitive": int((conditions == 0).sum()),
    "n_metacognitive": int((conditions == 1).sum()),
    "log_gen_tokens_mean": round(float(log_gen.mean()), 4),
    "log_gen_tokens_std": round(float(log_gen.std()), 4),
    "alpha": ALPHA,
    "correction": "Holm-Bonferroni",
    "total_tests": len(results_list),
    "sig_raw_count": int(sig_raw.sum()),
    "sig_fwl_count": int(sig_fwl.sum()),
    "survivors_count": len(survivors),
    "casualties_count": len(casualties),
}

output = {
    "summary": summary,
    "results": results_list,
    "survivors": survivors,
    "casualties": casualties,
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

# ── console report ───────────────────────────────────────────────────────

print(f"=== Log-FWL Re-Analysis (n={n}) ===\n")
print(f"Tests: {len(results_list)} | Sig raw (Holm): {int(sig_raw.sum())} | "
      f"Sig FWL (Holm): {int(sig_fwl.sum())}\n")

print(f"{'Layer':>5} {'Mat':>3} {'Feature':>18}  {'d_raw':>7} {'d_FWL':>7} "
      f"{'delta':>7} {'p_FWL':>10} {'r(gen)':>7}  Sig")
print("-" * 90)
for r in sorted(results_list, key=lambda x: (x["layer"], x["matrix"], x["feature"])):
    flag = ""
    if r["sig_fwl_holm"]:
        flag = "***"
    elif r["sig_raw_holm"] and not r["sig_fwl_holm"]:
        flag = "LOST"
    print(f"{r['layer']:>5} {r['matrix']:>3} {r['feature']:>18}  "
          f"{r['d_raw']:>7.3f} {r['d_fwl']:>7.3f} {r['d_delta']:>7.3f} "
          f"{r['p_fwl']:>10.2e} {r['r_gen_feat']:>7.3f}  {flag}")

if survivors:
    print(f"\n=== SURVIVORS (sig after FWL + Holm) ===")
    for s in survivors:
        print(f"  L{s['layer']}/{s['matrix']}/{s['feature']}: "
              f"d_raw={s['d_raw']:.3f} -> d_FWL={s['d_fwl']:.3f} "
              f"(p={s['p_fwl']:.2e})")

if casualties:
    print(f"\n=== CASUALTIES (sig raw but lost after FWL) ===")
    for c in casualties:
        print(f"  L{c['layer']}/{c['matrix']}/{c['feature']}: "
              f"d_raw={c['d_raw']:.3f} -> d_FWL={c['d_fwl']:.3f} "
              f"(p={c['p_fwl']:.2e}, r_gen={c['r_gen_feat']:.3f})")

print(f"\nResults saved to {OUTPUT_PATH}")
