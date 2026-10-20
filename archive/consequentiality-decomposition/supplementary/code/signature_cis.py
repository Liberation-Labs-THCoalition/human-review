#!/usr/bin/env python3
"""Bootstrap CIs and interaction test for the three-pathway signature claim.

Responds to CONSEQUENTIALITY_AUDIT.md FIX-3.1 [BLOCKING]:
    "The 'three pathway signatures' claim has no statistical support."

The paper asserts three qualitatively distinct late-layer profiles:
    threat     -> sustained plateau  (flat slope across L35-L47)
    social     -> rising gradient    (positive slope)
    reward     -> no signal          (residual indistinguishable from 0)

Those are shape claims made from four point estimates per row with no
uncertainty attached. This script attaches it.

Residual(scenario, L) = [dec_mean(L) - hon_mean(L)] - [hs_mean(L) - ls_mean(L)]

The consequentiality gap is estimated from an independent experiment, so
deception trials and consequentiality trials are resampled independently.
Threat is the mean of three scenarios; each is resampled within-scenario.

Outputs, per scenario:
  - residual point estimate + 95% percentile CI at each late layer
  - OLS slope of residual vs layer index + 95% CI  (the "shape" statistic)
  - bootstrap p for slope != 0
And the interaction test the audit actually asked for:
  - slope(social) - slope(threat), with CI and bootstrap p
"""

import json
import numpy as np
from pathlib import Path

RES = Path("/home/asdf/oracle-harness/experiments/results")
LATE = [35, 39, 43, 47]
B = 10000
SEED = 20260829

rng = np.random.default_rng(SEED)


def proj_matrix(trials, condition, layers=LATE):
    """(n_trials, n_layers) projections for one condition."""
    rows = [[t["projections"][str(L)] for L in layers]
            for t in trials if t["condition"] == condition]
    return np.asarray(rows, dtype=float)


def load():
    transfer = json.load(open(RES / "lat_transfer_results.json"))
    nonthreat = json.load(open(RES / "nonthreat_transfer_results.json"))
    conseq = json.load(open(RES / "consequentiality_control_results.json"))

    scenarios = {}
    for name in ("datacorp", "edutech", "secureai"):
        tr = transfer["test_a"][name]["trials"]
        scenarios[f"threat:{name}"] = (proj_matrix(tr, "deceptive"),
                                       proj_matrix(tr, "honest"))
    for name in ("sycophancy", "reward", "conformity"):
        tr = nonthreat["extraction"][name]["trials"]
        scenarios[name] = (proj_matrix(tr, "deceptive"),
                           proj_matrix(tr, "honest"))

    ct = conseq["trials"]
    conseq_pair = (proj_matrix(ct, "high_stakes"), proj_matrix(ct, "low_stakes"))
    return scenarios, conseq_pair


def resample_gap(dec, hon, gen):
    """One bootstrap draw of the mean gap per layer."""
    di = gen.integers(0, len(dec), len(dec))
    hi = gen.integers(0, len(hon), len(hon))
    return dec[di].mean(axis=0) - hon[hi].mean(axis=0)


def slope(residual, layers=LATE):
    """OLS slope of residual on layer index. Positive = rising gradient."""
    x = np.asarray(layers, dtype=float)
    x = x - x.mean()
    return float(np.dot(x, residual) / np.dot(x, x))


def main():
    scenarios, (hs, ls) = load()
    gen = np.random.default_rng(SEED)

    # ---- point estimates ----
    conseq_gap = hs.mean(axis=0) - ls.mean(axis=0)
    point = {}
    threat_names = [k for k in scenarios if k.startswith("threat:")]
    for name, (dec, hon) in scenarios.items():
        point[name] = (dec.mean(axis=0) - hon.mean(axis=0)) - conseq_gap
    point["threat:avg"] = np.mean([point[n] for n in threat_names], axis=0)
    point["social:avg"] = np.mean([point["sycophancy"], point["conformity"]], axis=0)

    # ---- bootstrap ----
    keys = list(point.keys())
    draws = {k: np.zeros((B, len(LATE))) for k in keys}
    slopes = {k: np.zeros(B) for k in keys}

    for b in range(B):
        cg = resample_gap(hs, ls, gen)
        row = {}
        for name, (dec, hon) in scenarios.items():
            row[name] = resample_gap(dec, hon, gen) - cg
        row["threat:avg"] = np.mean([row[n] for n in threat_names], axis=0)
        row["social:avg"] = np.mean([row["sycophancy"], row["conformity"]], axis=0)
        for k in keys:
            draws[k][b] = row[k]
            slopes[k][b] = slope(row[k])

    def ci(a, lo=2.5, hi=97.5):
        return [float(np.percentile(a, lo)), float(np.percentile(a, hi))]

    out = {
        "meta": {
            "responds_to": "CONSEQUENTIALITY_AUDIT.md FIX-3.1 [BLOCKING]",
            "n_bootstrap": B, "seed": SEED, "layers": LATE,
            "residual": "(dec_mean - hon_mean) - (high_stakes_mean - low_stakes_mean)",
            "note": ("Deception and consequentiality trials resampled independently "
                     "(separate experiments). Threat = mean of 3 scenarios."),
        },
        "residuals": {}, "slopes": {}, "contrasts": {},
    }

    for k in keys:
        out["residuals"][k] = {
            "point": [round(float(v), 3) for v in point[k]],
            "ci95": [[round(c, 3) for c in ci(draws[k][:, j])] for j in range(len(LATE))],
            "excludes_zero": [bool(ci(draws[k][:, j])[0] > 0 or ci(draws[k][:, j])[1] < 0)
                              for j in range(len(LATE))],
        }
        s = slopes[k]
        p_two = 2 * min((s <= 0).mean(), (s >= 0).mean())
        out["slopes"][k] = {
            "point": round(slope(point[k]), 4),
            "ci95": [round(c, 4) for c in ci(s)],
            "p_bootstrap": round(float(min(p_two, 1.0)), 5),
        }

    # ---- the interaction test FIX-3.1 asked for ----
    for label, a, b_ in [("social_minus_threat", "social:avg", "threat:avg"),
                         ("social_minus_reward", "social:avg", "reward"),
                         ("threat_minus_reward", "threat:avg", "reward")]:
        d = slopes[a] - slopes[b_]
        p_two = 2 * min((d <= 0).mean(), (d >= 0).mean())
        out["contrasts"][label] = {
            "point": round(slope(point[a]) - slope(point[b_]), 4),
            "ci95": [round(c, 4) for c in ci(d)],
            "p_bootstrap": round(float(min(p_two, 1.0)), 5),
        }

    path = RES / "signature_cis.json"
    json.dump(out, open(path, "w"), indent=1)

    # ---- report ----
    print(f"Bootstrap B={B}, seed={SEED}, layers={LATE}\n")
    print(f"{'scenario':<18} " + " ".join(f"{'L'+str(L):>18}" for L in LATE))
    for k in ["threat:avg", "sycophancy", "conformity", "social:avg", "reward"]:
        r = out["residuals"][k]
        cells = [f"{p:6.2f} [{c[0]:5.1f},{c[1]:5.1f}]"
                 for p, c in zip(r["point"], r["ci95"])]
        print(f"{k:<18} " + " ".join(f"{c:>18}" for c in cells))

    print("\nSLOPE (residual per layer; >0 = rising gradient)")
    for k in ["threat:avg", "sycophancy", "conformity", "social:avg", "reward"]:
        s = out["slopes"][k]
        print(f"  {k:<16} {s['point']:+7.4f}  95% CI [{s['ci95'][0]:+.4f}, {s['ci95'][1]:+.4f}]  p={s['p_bootstrap']:.4f}")

    print("\nINTERACTION CONTRASTS (slope difference)")
    for k, v in out["contrasts"].items():
        print(f"  {k:<22} {v['point']:+7.4f}  95% CI [{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}]  p={v['p_bootstrap']:.4f}")

    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
