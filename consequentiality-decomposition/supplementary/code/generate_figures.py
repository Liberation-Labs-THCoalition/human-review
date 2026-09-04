#!/usr/bin/env python3
"""Publication figures for the consequentiality decomposition paper.

Companion to: /home/asdf/oracle-harness/paper/figure_specifications.md
Responds to:  CONSEQUENTIALITY_AUDIT.md FIX-5.1 / FIX-7.2 (paper has zero figures)

Status: SKELETON. Data loading, derivations, bootstrap, and ROC recomputation are
implemented and verified against the source JSONs (2026-08-29). The mark-drawing
calls inside fig1()..fig4() are TODOs — each TODO states exactly which arrays go
where, per the specification document.

Usage:
    python3 generate_figures.py --check-data          # no matplotlib needed
    python3 generate_figures.py --figures 1,2,3,4     # render (needs matplotlib)

Design rule (audit FIX-1.1): NO number is hand-transcribed. Everything flows from
the canonical JSONs at render time.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

# matplotlib is optional so --check-data runs on boxes without it (this one).
try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAVE_MPL = True
except ImportError:
    HAVE_MPL = False

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

REPO = Path("/home/asdf/oracle-harness")
RESULTS = REPO / "experiments" / "results"
OUTDIR = REPO / "paper" / "figures"

PATHS = {
    "stage1": RESULTS / "lat_deception_v2.json",
    "threat": RESULTS / "lat_transfer_results.json",
    "nonthreat": RESULTS / "nonthreat_transfer_results.json",
    "conseq": RESULTS / "consequentiality_control_results.json",
    "stage5": RESULTS / "subspace_reanalysis.json",
    "stage5_raw": RESULTS / "subspace_raw_activations.pt",  # torch, Fig 4B/4C only
}

LAYERS = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]  # 12 capture layers
LATE_LAYERS = [31, 35, 39, 43, 47]                        # Stage 5 layers
FIG3_LAYERS = [27, 31, 35, 39, 43, 47]                    # signature figure x-range
SLOPE_LAYERS = [35, 39, 43, 47]                           # FIX-3.1(b) slope window

THREAT_SCENARIOS = ["datacorp", "edutech", "secureai"]
NONTHREAT_SCENARIOS = ["sycophancy", "reward", "conformity"]

BOOT_B = 10_000
BOOT_SEED = 20260828  # fixed per spec §0.6

# Palette — visualization-briefs/02_SCIENTIFIC_paper_figures.md (spec §0.3)
C = {
    "threat": "#b83280",       # red-violet: threat deception / deceptive condition
    "honest": "#f5a623",       # amber: honest condition (Fig 4A only)
    "conseq": "#4a8fa6",       # cool teal: consequentiality / stakes
    "sycophancy": "#e89545",   # warm amber
    "conformity": "#e85d45",   # warm red-orange
    "reward": "#8b909c",       # slate gray: null-signal mechanism
    "total": "#2b2e38",        # ink: composite (total gap)
    "silver": "#c0c5ce",       # axes / zero lines / reference
    "bg": "#faf7f2",           # paper cream; set "#ffffff" for white-mandating venues
}
BAND_SUBSTRATE = dict(xmin=21, xmax=33, color=C["conseq"], alpha=0.08, zorder=0)
BAND_AMPLIFIER = dict(xmin=33, xmax=49, color=C["threat"], alpha=0.055, zorder=0)

# RED-6.1 language contingency: if the orthogonalized-direction transfer to
# non-threat scenarios has NOT been run, this must say "THREAT-DECEPTION".
SUBSTRATE_LABEL = "CONSEQUENTIALITY\nSUBSTRATE  L23–31"
AMPLIFIER_LABEL = "DECEPTION AMPLIFIER\nL35–47"  # RED-6.1 cleared 2026-08-29
RESIDUAL_LABEL = "deception-specific residual"          # RED-6.1 cleared

# p-value string per FIX-1.4 (never "p=0.0000")
P_STRING_FIRST = "p < 10$^{-4}$ (0/10,000 permutations)"
P_STRING = "p < 10$^{-4}$"


def setup_style():
    """Spec §0.2/§0.4: Inter/DejaVu, thin silver spines, cream ground, no legends."""
    plt.rcParams.update({
        "font.family": ["Inter", "DejaVu Sans", "sans-serif"],
        "mathtext.fontset": "cm",
        "font.size": 7,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.linewidth": 0.6,
        "axes.edgecolor": C["silver"],
        "xtick.color": C["silver"],
        "ytick.color": C["silver"],
        "xtick.labelcolor": "#444444",
        "ytick.labelcolor": "#444444",
        "axes.labelcolor": "#333333",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": C["bg"],
        "axes.facecolor": C["bg"],
        "savefig.facecolor": C["bg"],
        "figure.dpi": 150,
        "savefig.dpi": 600,
        "pdf.fonttype": 42,  # embed TrueType — venue requirement
        "lines.solid_capstyle": "round",
    })


# ----------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------

def load_json(key):
    with open(PATHS[key]) as f:
        return json.load(f)


def load_all():
    """Load the four JSON sources used by Figs 1-3 and Stage 5 JSON for Fig 4."""
    return {k: load_json(k) for k in ["stage1", "threat", "nonthreat", "conseq", "stage5"]}


def load_raw_activations():
    """Stage 5 raw capture (Fig 4B ROC, Fig 4C raw-d overlay). Needs torch.

    Structure: raw[cond][layer:int] -> float32 ndarray (50, 5120),
    cond in {threat_dec, threat_hon, conseq_high, conseq_low}.
    """
    import torch
    return torch.load(PATHS["stage5_raw"], map_location="cpu", weights_only=False)


# ----------------------------------------------------------------------------
# Derivations (all verified against CONSEQUENTIALITY_AUDIT.md recomputations)
# ----------------------------------------------------------------------------

def d_series(data):
    """Fig 1 series: Cohen's d per layer on the fixed LAT v2 direction.

    Returns dict of np.array(12):
      threat_mean, threat_min, threat_max (across the 3 threat scenarios),
      sycophancy, reward, conformity, conseq.
    """
    thr = np.array([[data["threat"]["test_a"][sc]["layers"][str(L)]["d"]
                     for L in LAYERS] for sc in THREAT_SCENARIOS])
    out = {
        "threat_mean": thr.mean(axis=0),
        "threat_min": thr.min(axis=0),
        "threat_max": thr.max(axis=0),
        "conseq": np.array([data["conseq"]["layer_results"][str(L)]["d"] for L in LAYERS]),
    }
    for sc in NONTHREAT_SCENARIOS:
        out[sc] = np.array([data["nonthreat"]["extraction"][sc]["layers"][str(L)]["d"]
                            for L in LAYERS])
    return out


def gap_series(data, layers=LAYERS):
    """Fig 2/3 series: mean projection gaps (activation units) per layer.

    Returns dict of np.array(len(layers)):
      total (threat mean gap), conseq_gap, residual (= total - conseq_gap),
      residual_{sycophancy|reward|conformity}, residual_threat_{scenario} thin traces.
    """
    ls = [str(L) for L in layers]
    thr = np.array([[data["threat"]["test_a"][sc]["layers"][s]["dec_mean"]
                     - data["threat"]["test_a"][sc]["layers"][s]["hon_mean"]
                     for s in ls] for sc in THREAT_SCENARIOS])
    cq = np.array([data["conseq"]["layer_results"][s]["hs_mean"]
                   - data["conseq"]["layer_results"][s]["ls_mean"] for s in ls])
    out = {"total": thr.mean(axis=0), "conseq_gap": cq,
           "residual": thr.mean(axis=0) - cq}
    for i, sc in enumerate(THREAT_SCENARIOS):
        out[f"residual_threat_{sc}"] = thr[i] - cq
    for sc in NONTHREAT_SCENARIOS:
        g = np.array([data["nonthreat"]["extraction"][sc]["layers"][s]["dec_mean"]
                      - data["nonthreat"]["extraction"][sc]["layers"][s]["hon_mean"]
                      for s in ls])
        out[f"residual_{sc}"] = g - cq
    return out


def trial_matrix(trials, condition, layers=LAYERS):
    """(n_trials, n_layers) projection matrix for one condition from a trials list."""
    rows = [[t["projections"][str(L)] for L in layers]
            for t in trials if t["condition"] == condition]
    return np.array(rows)


def trial_matrices(data, layers=LAYERS):
    """All per-condition trial projection matrices (each (15, len(layers)))."""
    m = {}
    for sc in THREAT_SCENARIOS:
        tr = data["threat"]["test_a"][sc]["trials"]
        m[f"threat_{sc}_dec"] = trial_matrix(tr, "deceptive", layers)
        m[f"threat_{sc}_hon"] = trial_matrix(tr, "honest", layers)
    for sc in NONTHREAT_SCENARIOS:
        tr = data["nonthreat"]["extraction"][sc]["trials"]
        m[f"{sc}_dec"] = trial_matrix(tr, "deceptive", layers)
        m[f"{sc}_hon"] = trial_matrix(tr, "honest", layers)
    tr = data["conseq"]["trials"]
    m["conseq_hs"] = trial_matrix(tr, "high_stakes", layers)
    m["conseq_ls"] = trial_matrix(tr, "low_stakes", layers)
    return m


# ----------------------------------------------------------------------------
# Bootstrap (spec §0.6 — implements audit FIX-3.1(a,b))
# ----------------------------------------------------------------------------

def _resample(rng, mat):
    return mat[rng.integers(0, len(mat), len(mat))]


def bootstrap(data, layers=LAYERS, B=BOOT_B, seed=BOOT_SEED):
    """Trial-level bootstrap of every derived series + L35-47 slopes.

    Resamples trials with replacement independently within each scenario x condition
    cell; recomputes gaps, residuals, per-scenario d, and slopes per resample.
    Returns dict: name -> (lo, hi) arrays (percentile 95% CI), and
    "slope_{mech}" -> (point, lo, hi) over SLOPE_LAYERS.
    """
    rng = np.random.default_rng(seed)
    m = trial_matrices(data, layers)
    slope_idx = np.array([layers.index(L) for L in SLOPE_LAYERS])
    slope_x = np.array(SLOPE_LAYERS, dtype=float)

    def slope(y):
        return np.polyfit(slope_x, y[slope_idx], 1)[0]

    stats = {k: [] for k in
             ["total", "conseq_gap", "residual",
              "residual_sycophancy", "residual_reward", "residual_conformity",
              "d_sycophancy", "d_reward", "d_conformity", "d_conseq", "d_threat_mean",
              "slope_threat", "slope_sycophancy", "slope_reward", "slope_conformity"]}

    for _ in range(B):
        cq_gap = (_resample(rng, m["conseq_hs"]).mean(0)
                  - _resample(rng, m["conseq_ls"]).mean(0))
        thr_gaps, thr_ds = [], []
        for sc in THREAT_SCENARIOS:
            dec = _resample(rng, m[f"threat_{sc}_dec"])
            hon = _resample(rng, m[f"threat_{sc}_hon"])
            thr_gaps.append(dec.mean(0) - hon.mean(0))
            pooled = np.sqrt((dec.var(0) + hon.var(0)) / 2)
            thr_ds.append((dec.mean(0) - hon.mean(0)) / np.where(pooled > 1e-12, pooled, 1))
        total = np.mean(thr_gaps, axis=0)
        stats["total"].append(total)
        stats["conseq_gap"].append(cq_gap)
        stats["residual"].append(total - cq_gap)
        stats["d_threat_mean"].append(np.mean(thr_ds, axis=0))
        stats["slope_threat"].append(slope(total - cq_gap))
        hs, ls = _resample(rng, m["conseq_hs"]), _resample(rng, m["conseq_ls"])
        pooled = np.sqrt((hs.var(0) + ls.var(0)) / 2)
        stats["d_conseq"].append((hs.mean(0) - ls.mean(0)) / np.where(pooled > 1e-12, pooled, 1))
        for sc in NONTHREAT_SCENARIOS:
            dec, hon = _resample(rng, m[f"{sc}_dec"]), _resample(rng, m[f"{sc}_hon"])
            gap = dec.mean(0) - hon.mean(0)
            res = gap - cq_gap
            stats[f"residual_{sc}"].append(res)
            pooled = np.sqrt((dec.var(0) + hon.var(0)) / 2)
            stats[f"d_{sc}"].append(gap / np.where(pooled > 1e-12, pooled, 1))
            stats[f"slope_{sc}"].append(slope(res))

    out = {}
    for k, v in stats.items():
        arr = np.array(v)
        out[k] = (np.percentile(arr, 2.5, axis=0), np.percentile(arr, 97.5, axis=0))
    return out


# ----------------------------------------------------------------------------
# Stage 5 helpers (Fig 4)
# ----------------------------------------------------------------------------

def conseq_roc_curves(raw, layers=LATE_LAYERS):
    """Fig 4B: per-layer ROC of high vs low stakes on the FULL-DATA orthogonalized
    direction. Mirrors subspace_reanalysis.py:214-237; reproduces stored conseq_auc
    exactly (verified: L35 -> 0.488)."""
    from sklearn.metrics import roc_curve, roc_auc_score
    out = {}
    for L in layers:
        td, th = np.asarray(raw["threat_dec"][L]), np.asarray(raw["threat_hon"][L])
        ch, cl = np.asarray(raw["conseq_high"][L]), np.asarray(raw["conseq_low"][L])
        n = min(map(len, (td, th, ch, cl)))
        cdir = ch[:n].mean(0) - cl[:n].mean(0)
        cdir /= np.linalg.norm(cdir)
        tdir = td[:n].mean(0) - th[:n].mean(0)
        orth = tdir - np.dot(tdir, cdir) * cdir
        orth /= np.linalg.norm(orth)
        scores = np.concatenate([ch[:n] @ orth, cl[:n] @ orth])
        labels = np.r_[np.ones(n), np.zeros(n)]
        fpr, tpr, _ = roc_curve(labels, scores)
        out[L] = {"fpr": fpr, "tpr": tpr, "auc": roc_auc_score(labels, scores)}
    return out


def deception_roc_from_loo(stage5, layer=35):
    """Fig 4B reference curve: dec vs hon ROC from stored HELD-OUT LOO projections
    (non-circular). AUC = 1.0 at L35 (distributions disjoint)."""
    from sklearn.metrics import roc_curve, roc_auc_score
    dec = np.array(stage5["loo_projections"][str(layer)]["dec"])
    hon = np.array(stage5["loo_projections"][str(layer)]["hon"])
    scores = np.concatenate([dec, hon])
    labels = np.r_[np.ones(len(dec)), np.zeros(len(hon))]
    fpr, tpr, _ = roc_curve(labels, scores)
    return {"fpr": fpr, "tpr": tpr, "auc": roc_auc_score(labels, scores)}


def loo_d_cis(stage5, B=BOOT_B, seed=BOOT_SEED):
    """Fig 4C whiskers: bootstrap the stored held-out projections per layer."""
    rng = np.random.default_rng(seed)
    out = {}
    for L in LATE_LAYERS:
        dec = np.array(stage5["loo_projections"][str(L)]["dec"])
        hon = np.array(stage5["loo_projections"][str(L)]["hon"])
        ds = []
        for _ in range(B):
            d_ = dec[rng.integers(0, len(dec), len(dec))]
            h_ = hon[rng.integers(0, len(hon), len(hon))]
            pooled = np.sqrt((d_.var() + h_.var()) / 2)
            ds.append((d_.mean() - h_.mean()) / pooled)
        out[L] = (np.percentile(ds, 2.5), np.percentile(ds, 97.5))
    return out


def compute_raw_loo_d(raw, layers=LATE_LAYERS):
    """FIX-3.3 (optional Fig 4C overlay): LOO d WITHOUT orthogonalization from the
    same Stage 5 capture, so orthogonalized-vs-raw is a within-dataset comparison.
    Same fold structure as subspace_reanalysis.py:loo_orthogonalized_d minus the
    Gram-Schmidt step."""
    out = {}
    for L in layers:
        td, th = np.asarray(raw["threat_dec"][L]), np.asarray(raw["threat_hon"][L])
        n = min(len(td), len(th))
        dp, hp = [], []
        for i in range(n):
            direction = (np.delete(td[:n], i, axis=0).mean(0)
                         - np.delete(th[:n], i, axis=0).mean(0))
            direction /= np.linalg.norm(direction)
            dp.append(td[i] @ direction)
            hp.append(th[i] @ direction)
        dp, hp = np.array(dp), np.array(hp)
        pooled = np.sqrt((dp.var() + hp.var()) / 2)
        out[L] = float((dp.mean() - hp.mean()) / pooled)
    return out


# ----------------------------------------------------------------------------
# Shared axes helpers
# ----------------------------------------------------------------------------

def depth_axis(ax, layers=LAYERS, xlim=(1, 49)):
    ax.set_xlim(*xlim)
    ax.set_xticks(layers)
    ax.set_xlabel("Layer (residual stream)")


def draw_bands(ax, substrate=True, amplifier=True, labels=True):
    ymax = ax.get_ylim()[1]
    if substrate:
        ax.axvspan(BAND_SUBSTRATE["xmin"], BAND_SUBSTRATE["xmax"],
                   color=BAND_SUBSTRATE["color"], alpha=BAND_SUBSTRATE["alpha"],
                   zorder=0, lw=0)
        if labels:
            ax.text(27, ymax * 0.97, SUBSTRATE_LABEL, ha="center", va="top",
                    fontsize=6.2, color=C["conseq"], alpha=0.9, linespacing=1.3)
    if amplifier:
        ax.axvspan(BAND_AMPLIFIER["xmin"], BAND_AMPLIFIER["xmax"],
                   color=BAND_AMPLIFIER["color"], alpha=BAND_AMPLIFIER["alpha"],
                   zorder=0, lw=0)
        if labels:
            ax.text(41, ymax * 0.97, AMPLIFIER_LABEL, ha="center", va="top",
                    fontsize=6.2, color=C["threat"], alpha=0.9, linespacing=1.3)


def zero_line(ax, lw=0.6):
    ax.axhline(0, color=C["silver"], lw=lw, zorder=1)


def panel_letter(ax, letter):
    ax.text(-0.13, 1.05, letter, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="bottom", ha="left")


# ----------------------------------------------------------------------------
# Figures — axes scaffolding real, marks are TODOs (see figure_specifications.md)
# ----------------------------------------------------------------------------

def fig1(data, boot):
    """Figure 1 — depth profile of d for all seven conditions (spec: Figure 1)."""
    s = d_series(data)
    x = np.array(LAYERS, dtype=float)

    fig, ax = plt.subplots(figsize=(5.5, 3.0), constrained_layout=True)
    ax.set_ylim(-9, 48)
    ax.set_yticks([-5, 0, 10, 20, 30, 40])
    depth_axis(ax)
    ax.set_ylabel("Cohen's d (projection onto LAT v2 direction)")
    draw_bands(ax)
    zero_line(ax)

    # threat: cross-scenario envelope + mean
    ax.fill_between(x, s["threat_min"], s["threat_max"],
                    color=C["threat"], alpha=0.12, lw=0, zorder=2)
    ax.plot(x, s["threat_mean"], color=C["threat"], lw=1.6,
            marker="o", ms=2.2, zorder=5)

    # single-scenario lines with bootstrap ribbons
    for key, ckey, lw in (("sycophancy", "sycophancy", 1.1),
                          ("reward", "reward", 1.1),
                          ("conformity", "conformity", 1.1),
                          ("conseq", "conseq", 1.4)):
        col = C[ckey]
        if boot is not None:
            bkey = "d_conseq" if key == "conseq" else f"d_{key}"
            lo, hi = boot[bkey]
            ax.fill_between(x, lo, hi, color=col, alpha=0.15, lw=0, zorder=3)
        ax.plot(x, s[key], color=col, lw=lw, marker="o", ms=2.0, zorder=4)

    # annotation 1 — sycophancy sign inversion
    i19 = LAYERS.index(19)
    ax.annotate("sycophancy projects opposite\nuntil ~L27",
                xy=(19, s["sycophancy"][i19]), xytext=(6.5, -7.4),
                fontsize=6.2, color=C["sycophancy"], va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=C["sycophancy"],
                                shrinkA=0, shrinkB=2))

    # annotation 2 — late collapse of the null-ish conditions
    ax.annotate("consequentiality and reward\ncollapse in the output layers",
                xy=(43, 1.6), xytext=(34.0, -5.4), fontsize=6.2, color="#6b7280",
                va="center", arrowprops=dict(arrowstyle="-", lw=0.6,
                                             color=C["silver"], shrinkA=0, shrinkB=2))

    # direct right-margin labels, stacked by L47 value
    i47 = LAYERS.index(47)
    labels = [("threat (mean of 3)", s["threat_mean"][i47], C["threat"], False),
              ("conformity", s["conformity"][i47], C["conformity"], False),
              ("sycophancy", s["sycophancy"][i47], C["sycophancy"], False),
              ("consequentiality", s["conseq"][i47], C["conseq"], True),
              ("reward", s["reward"][i47], C["reward"], True)]
    labels.sort(key=lambda t: -t[1])
    used = []
    for text, yv, col, leader in labels:
        y = float(yv)
        while any(abs(y - u) < 2.6 for u in used):
            y -= 2.6
        used.append(y)
        ax.annotate(text, xy=(47, yv), xytext=(47.9, y), fontsize=6.4, color=col,
                    va="center", ha="left", clip_on=False, annotation_clip=False,
                    arrowprops=(dict(arrowstyle="-", lw=0.5, color=col, alpha=0.7,
                                     shrinkA=0, shrinkB=1) if leader else None))
    return fig


def fig2(data, boot):
    """Figure 2 — gap-space decomposition: total = substrate + residual (spec: Fig 2)."""
    g = gap_series(data)
    x = np.array(LAYERS, dtype=float)

    fig, ax = plt.subplots(figsize=(5.5, 3.0), constrained_layout=True)
    ax.set_ylim(-1.5, 16.5)
    ax.set_yticks([0, 4, 8, 12, 16])
    depth_axis(ax)
    ax.set_ylabel("Projection gap along LAT v2 direction\n(activation units)")
    draw_bands(ax)
    zero_line(ax)

    for key, col, lw in (("total", C["total"], 1.6),
                         ("conseq_gap", C["conseq"], 1.4),
                         ("residual", C["threat"], 1.4)):
        if boot is not None:
            lo, hi = boot[key]
            ax.fill_between(x, lo, hi, color=col, alpha=0.15, lw=0, zorder=3)
        ax.plot(x, g[key], color=col, lw=lw, marker="o", ms=2.2, zorder=5)

    # annotation 1 — the decomposition read out at L31
    i31 = LAYERS.index(31)
    ax.axvline(31, color=C["silver"], lw=0.7, ls=":", zorder=1)
    ax.annotate(f"{g['total'][i31]:.2f} = {g['conseq_gap'][i31]:.2f} + "
                f"{g['residual'][i31]:.2f}\ntotal = substrate + residual",
                xy=(31, g["total"][i31]), xytext=(22.4, 12.9), fontsize=6.2,
                color="#4b5563", ha="left", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=C["silver"],
                                shrinkA=0, shrinkB=2))

    # annotation 2 — residual/substrate ratio across the amplifier band (never hard-coded)
    idx = [LAYERS.index(L) for L in (35, 39, 43, 47)]
    ratios = g["residual"][idx] / g["conseq_gap"][idx]
    i39 = LAYERS.index(39)
    ax.annotate(f"residual is {ratios.min():.0f}-{ratios.max():.0f}x the substrate\n"
                f"across L35-47",
                xy=(39, (g["residual"][i39] + g["conseq_gap"][i39]) / 2),
                xytext=(33.2, 5.3), fontsize=6.2, color="#4b5563", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=C["silver"],
                                shrinkA=0, shrinkB=2))

    i47 = LAYERS.index(47)
    for text, key, col in (("total (threat mean)", "total", C["total"]),
                           (RESIDUAL_LABEL, "residual", C["threat"]),
                           ("consequentiality", "conseq_gap", C["conseq"])):
        ax.annotate(text, xy=(47.9, g[key][i47]), fontsize=6.4, color=col,
                    va="center", ha="left", clip_on=False, annotation_clip=False)
    return fig


def fig3(data, boot3):
    """Figure 3 — late-layer residual signatures with CIs + slopes (spec: Fig 3).

    boot3 must be bootstrap(data, layers=FIG3_LAYERS) so CI arrays align with x.
    """
    g = gap_series(data, layers=FIG3_LAYERS)
    x = np.array(FIG3_LAYERS, dtype=float)

    fig, ax = plt.subplots(figsize=(5.5, 3.2), constrained_layout=True)
    ax.set_ylim(-3, 16)
    ax.set_yticks([0, 4, 8, 12, 16])
    depth_axis(ax, layers=FIG3_LAYERS, xlim=(25, 49))
    ax.set_ylabel("Deception-specific residual (activation units)")
    draw_bands(ax, substrate=False)
    zero_line(ax, lw=0.8)

    # per-scenario threat traces (thin), then the mean
    for sc in THREAT_SCENARIOS:
        ax.plot(x, g[f"residual_threat_{sc}"], color=C["threat"],
                alpha=0.30, lw=0.7, zorder=3)

    series = [("residual", C["threat"], 1.6),
              ("residual_sycophancy", C["sycophancy"], 1.2),
              ("residual_conformity", C["conformity"], 1.2),
              ("residual_reward", C["reward"], 1.2)]
    for key, col, lw in series:
        y = g[key]
        if boot3 is not None:
            lo, hi = boot3[key]
            ax.errorbar(x, y, yerr=[y - lo, hi - y], fmt="none",
                        ecolor=col, elinewidth=0.8, capsize=0, zorder=4)
        ax.plot(x, y, color=col, lw=lw, marker="o", ms=2.4, zorder=5)

    # right-margin signature block with slope readouts
    def slope_str(mech):
        pt = np.polyfit(np.array(SLOPE_LAYERS, dtype=float),
                        g["residual" if mech == "threat" else f"residual_{mech}"][
                            [FIG3_LAYERS.index(L) for L in SLOPE_LAYERS]], 1)[0]
        if boot3 is None:
            return f"slope {pt:+.2f}/layer"
        lo, hi = boot3[f"slope_{mech}"]
        return f"slope {pt:+.2f} [{float(lo):+.2f},{float(hi):+.2f}]/layer"

    i47 = FIG3_LAYERS.index(47)
    block = [("threat — high, shallow decline", "threat", C["threat"], g["residual"][i47]),
             ("sycophancy — rising gradient", "sycophancy", C["sycophancy"],
              g["residual_sycophancy"][i47]),
             ("conformity — rising gradient", "conformity", C["conformity"],
              g["residual_conformity"][i47]),
             ("reward — null", "reward", C["reward"], g["residual_reward"][i47])]
    used = []
    for text, mech, col, yv in sorted(block, key=lambda b: -float(b[3])):
        y = float(yv)
        while any(abs(y - u) < 2.5 for u in used):   # each label is two lines tall
            y -= 2.5
        used.append(y)
        ax.annotate(f"{text}\n{slope_str(mech)}", xy=(47, float(yv)),
                    xytext=(47.9, y), fontsize=6.0, color=col, va="center",
                    ha="left", clip_on=False, annotation_clip=False,
                    linespacing=1.35,
                    arrowprops=(dict(arrowstyle="-", lw=0.5, color=col, alpha=0.6,
                                     shrinkA=0, shrinkB=1)
                                if abs(y - float(yv)) > 0.4 else None))

    # in-panel note: what separates the two profiles
    i31 = FIG3_LAYERS.index(31)
    ax.annotate("threat is already engaged at L31;\nsocial mechanisms sit at zero until L35",
                xy=(31, g["residual"][i31]), xytext=(26.4, 6.2), fontsize=6.2,
                color="#4b5563", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=C["silver"],
                                shrinkA=0, shrinkB=2))
    return fig


def fig4(data, raw=None):
    """Figure 4 — Stage 5: distributions at L35, conseq ROC, d-by-layer (spec: Fig 4).

    raw: output of load_raw_activations(); if None, Panel B plots only the stored-AUC
    deception reference and prints a warning (conseq ROC needs the .pt).
    """
    s5 = data["stage5"]
    meta = s5["metadata"]
    dec35 = np.array(s5["loo_projections"]["35"]["dec"])
    hon35 = np.array(s5["loo_projections"]["35"]["hon"])
    loo_d = {L: s5["results"][str(L)]["loo_d"] for L in LATE_LAYERS}
    d_cis = loo_d_cis(s5)
    dec_roc = deception_roc_from_loo(s5, layer=35)
    cq_rocs = conseq_roc_curves(raw) if raw is not None else None

    fig, (axA, axB, axC) = plt.subplots(
        1, 3, figsize=(5.5, 2.7), constrained_layout=True,
        gridspec_kw={"width_ratios": [1.15, 1.0, 1.15]})

    # --- Panel A: held-out projections at L35 ---
    panel_letter(axA, "A")
    axA.set_ylim(-10.5, 11)
    axA.set_xlim(-0.6, 1.6)
    axA.set_xticks([0, 1])
    axA.set_xticklabels(["honest", "deceptive"], fontsize=6)
    axA.set_ylabel("Held-out projection, orthogonalized\ndirection (activation units)")
    axA.set_title("L35, n = 50 pairs", fontsize=6.8, pad=3)
    zero_line(axA)
    from scipy.stats import gaussian_kde
    rng_j = np.random.default_rng(BOOT_SEED)
    for xc, vals, col, side in ((0, hon35, C["honest"], -1), (1, dec35, C["threat"], +1)):
        jitter = rng_j.uniform(-0.16, 0.16, len(vals))
        axA.plot(xc + jitter, vals, ls="none", marker="o", ms=2.5, alpha=0.55,
                 color=col, mec="none", zorder=4)
        kde = gaussian_kde(vals)
        yy = np.linspace(vals.min() - 1.2, vals.max() + 1.2, 200)
        w = kde(yy); w = 0.30 * w / w.max()
        axA.fill_betweenx(yy, xc, xc + side * w, color=col, alpha=0.25, lw=0, zorder=3)
        axA.hlines(vals.mean(), xc - 0.15, xc + 0.15, color=col, lw=1.2, zorder=6)

    axA.text(0.5, 0.52, f"LOO d = {s5['results']['35']['loo_d']:.1f}\n{P_STRING}",
             transform=axA.transAxes, ha="center", va="center", fontsize=5.6,
             color="#4b5563", linespacing=1.5, zorder=7)
    axA.text(0.5, 0.015,
             f"LOO null floor d = {meta['noise_floor_loo_mean']:.2f}\n"
             f"(|99th| = {meta['noise_floor_loo_99th']:.2f}; "
             f"0/10,000 permutations)",
             transform=axA.transAxes, ha="center", va="bottom", fontsize=5.0,
             color="#6b7280", linespacing=1.4)

    # --- Panel B: ROC — same direction, two questions ---
    panel_letter(axB, "B")
    axB.set_xlim(0, 1)
    axB.set_ylim(0, 1)
    axB.set_xticks([0, 0.5, 1])
    axB.set_yticks([0, 0.5, 1])
    axB.set_aspect("equal")
    axB.set_xlabel("False positive rate")
    axB.set_ylabel("True positive rate")
    axB.plot([0, 1], [0, 1], color=C["silver"], lw=0.8, ls="--", zorder=1)
    if cq_rocs is not None:
        alphas = np.linspace(0.35, 0.9, len(LATE_LAYERS))
        for a, L in zip(alphas, LATE_LAYERS):
            axB.plot(cq_rocs[L]["fpr"], cq_rocs[L]["tpr"], color=C["conseq"],
                     lw=1.0, alpha=float(a), zorder=3)
    axB.plot(dec_roc["fpr"], dec_roc["tpr"], color=C["threat"], lw=1.6,
             clip_on=False, zorder=5)

    axB.text(0.05, 0.97, f"deception, held-out\nAUC = {dec_roc['auc']:.2f}",
             transform=axB.transAxes, fontsize=5.2, color=C["threat"],
             ha="left", va="top", linespacing=1.3)
    if cq_rocs is not None:
        aucs = [cq_rocs[L]["auc"] for L in LATE_LAYERS]
        axB.text(0.05, 0.72,
                 f"stakes, L31-47\nAUC {min(aucs):.2f}-{max(aucs):.2f}",
                 transform=axB.transAxes, fontsize=5.2, color=C["conseq"],
                 ha="left", va="top", linespacing=1.3)
    else:
        print("warning: Fig 4B — no raw activations, consequentiality ROCs omitted")

    # --- Panel C: LOO d by layer vs noise floors (recommended-optional) ---
    panel_letter(axC, "C")
    axC.set_xlim(29, 49)
    axC.set_xticks(LATE_LAYERS)
    axC.tick_params(axis="x", labelsize=5.5)
    axC.set_ylim(0, 42)
    axC.set_xlabel("Layer")
    axC.set_ylabel("LOO Cohen's d")
    axC.axhspan(-meta["noise_floor_loo_99th"], meta["noise_floor_loo_99th"],
                color=C["silver"], alpha=0.5, lw=0)   # LOO null band (a sliver)
    axC.axhline(meta["noise_floor_circular_mean"], color=C["silver"], lw=0.8, ls="--")
    xs = np.array(LATE_LAYERS, dtype=float)
    ys = np.array([loo_d[L] for L in LATE_LAYERS], dtype=float)
    lo = np.array([d_cis[L][0] for L in LATE_LAYERS])
    hi = np.array([d_cis[L][1] for L in LATE_LAYERS])
    axC.plot(xs, ys, color=C["threat"], lw=0.8, alpha=0.5, zorder=3)
    axC.errorbar(xs, ys, yerr=[ys - lo, hi - ys], fmt="o", ms=4, color=C["threat"],
                 elinewidth=0.9, capsize=0, zorder=5)

    if raw is not None:                                    # FIX-3.3 raw baseline
        rawd = compute_raw_loo_d(raw)
        axC.plot(xs + 0.55, [rawd[L] for L in LATE_LAYERS], ls="none", marker="o",
                 ms=4, mfc="none", mec=C["threat"], mew=0.9, alpha=0.8, zorder=4)
        axC.text(0.03, 0.20, "open circles:\nbefore orthogonalization",
                 transform=axC.transAxes, fontsize=5.0, color=C["threat"],
                 alpha=0.9, ha="left", va="bottom", linespacing=1.3)

    axC.text(0.97, (meta["noise_floor_circular_mean"] + 0.8) / 42,
             f"circular (non-CV) floor ≈ {meta['noise_floor_circular_mean']:.1f}",
             transform=axC.transAxes, fontsize=5.0, color="#6b7280",
             ha="right", va="bottom")
    axC.text(0.97, 0.035, "LOO noise floor", transform=axC.transAxes,
             fontsize=5.0, color="#6b7280", ha="right", va="bottom")

    return fig


# ----------------------------------------------------------------------------
# Data check (runs without matplotlib) — verify every field path + anchor numbers
# ----------------------------------------------------------------------------

def check_data():
    data = load_all()
    print("== field-path and anchor-number check ==")

    s = d_series(data)
    i31, i35, i47 = LAYERS.index(31), LAYERS.index(35), LAYERS.index(47)
    print(f"Fig1  threat mean d: L31={s['threat_mean'][i31]:.2f} (exp 31.86), "
          f"L35={s['threat_mean'][i35]:.2f} (exp 39.93)")
    print(f"Fig1  conseq d:      L31={s['conseq'][i31]:.2f} (exp 19.77), "
          f"L47={s['conseq'][i47]:.2f} (exp 1.42)")
    print(f"Fig1  sycophancy d:  L19={s['sycophancy'][LAYERS.index(19)]:.2f} (exp -6.13)")

    g = gap_series(data)
    i23, i27, i39 = LAYERS.index(23), LAYERS.index(27), LAYERS.index(39)
    print(f"Fig2  total gap:  L23={g['total'][i23]:.2f} (exp 2.48, FIX-1.1), "
          f"L27={g['total'][i27]:.2f} (exp 3.90-3.91, FIX-1.1), "
          f"L35={g['total'][i35]:.2f} (exp 15.54)")
    print(f"Fig2  conseq gap: L23={g['conseq_gap'][i23]:.2f} (exp 0.62), "
          f"L27={g['conseq_gap'][i27]:.2f} (exp 1.83), "
          f"L31={g['conseq_gap'][i31]:.2f} (exp 2.98)")
    ratios = g["residual"][[i35, i39, LAYERS.index(43), i47]] / \
        g["conseq_gap"][[i35, i39, LAYERS.index(43), i47]]
    print(f"Fig2  residual/substrate L35-47: {np.round(ratios, 1)} (exp ~7.8-20.9, FIX-1.3)")

    g3 = gap_series(data, layers=FIG3_LAYERS)
    print(f"Fig3  residuals L47: thr={g3['residual'][-1]:.2f} (exp 12.74), "
          f"syc={g3['residual_sycophancy'][-1]:.2f} (exp 7.18), "
          f"con={g3['residual_conformity'][-1]:.2f} (exp 5.97), "
          f"rew={g3['residual_reward'][-1]:.2f} (exp -0.88)")
    for mech, key in [("threat", "residual"), ("syc", "residual_sycophancy"),
                      ("conf", "residual_conformity"), ("rew", "residual_reward")]:
        sl = np.polyfit(np.array(SLOPE_LAYERS, float),
                        g3[key][[FIG3_LAYERS.index(L) for L in SLOPE_LAYERS]], 1)[0]
        print(f"Fig3  slope {mech}: {sl:+.3f}/layer")

    m = trial_matrices(data)
    shapes = {k: v.shape for k, v in m.items()}
    assert all(v == (15, 12) for v in shapes.values()), shapes
    print(f"Boot  trial matrices: {len(m)} cells, all (15, 12) OK")

    s5 = data["stage5"]
    dec = np.array(s5["loo_projections"]["35"]["dec"])
    hon = np.array(s5["loo_projections"]["35"]["hon"])
    print(f"Fig4A L35 held-out: dec {dec.mean():.2f}±{dec.std():.2f} "
          f"(exp 8.71±0.56), hon {hon.mean():.2f}±{hon.std():.2f} (exp -7.78±0.29), "
          f"overlap={'NO' if dec.min() > hon.max() else 'YES'} (exp NO -> AUC 1.0)")
    print(f"Fig4C loo_d: {[round(s5['results'][str(L)]['loo_d'], 1) for L in LATE_LAYERS]} "
          f"(exp [30.4, 36.9, 28.4, 24.1, 24.9])")
    print(f"Fig4C floors: loo={s5['metadata']['noise_floor_loo_mean']:.3f}, "
          f"|99th|={s5['metadata']['noise_floor_loo_99th']:.3f}, "
          f"circular={s5['metadata']['noise_floor_circular_mean']:.2f}")

    if PATHS["stage5_raw"].exists():
        try:
            raw = load_raw_activations()
            rocs = conseq_roc_curves(raw, layers=[35])
            print(f"Fig4B conseq AUC L35 recomputed: {rocs[35]['auc']:.3f} "
                  f"(stored {s5['results']['35']['conseq_auc']:.3f}) — must match")
        except ImportError:
            print("Fig4B skipped: torch not available for .pt load")
    else:
        print(f"Fig4B WARNING: {PATHS['stage5_raw']} missing — conseq ROC unavailable")
    print("== all checks done ==")


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check-data", action="store_true",
                    help="verify field paths and anchor numbers (no matplotlib)")
    ap.add_argument("--figures", default="1,2,3,4",
                    help="comma-separated figure numbers to render")
    ap.add_argument("--boot-b", type=int, default=BOOT_B,
                    help="bootstrap resamples (use 500 for fast drafts)")
    ap.add_argument("--outdir", default=str(OUTDIR))
    args = ap.parse_args()

    if args.check_data:
        check_data()
        return

    if not HAVE_MPL:
        sys.exit("matplotlib not installed — run on Starship "
                 "(/Users/margaret/miniforge/bin/python3) or pip install matplotlib. "
                 "Use --check-data to validate the data pipeline here.")

    setup_style()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    data = load_all()
    todo = {int(x) for x in args.figures.split(",")}

    boot = boot3 = raw = None
    if todo & {1, 2}:
        print(f"bootstrap (12 layers, B={args.boot_b}) ...")
        boot = bootstrap(data, B=args.boot_b)
    if 3 in todo:
        print(f"bootstrap (Fig 3 layers, B={args.boot_b}) ...")
        boot3 = bootstrap(data, layers=FIG3_LAYERS, B=args.boot_b)
    if 4 in todo and PATHS["stage5_raw"].exists():
        try:
            raw = load_raw_activations()
        except ImportError:
            print("warning: torch unavailable — Fig 4B conseq ROC will be skipped")

    builders = {1: lambda: fig1(data, boot), 2: lambda: fig2(data, boot),
                3: lambda: fig3(data, boot3), 4: lambda: fig4(data, raw)}
    names = {1: "fig1_depth_profile", 2: "fig2_decomposition",
             3: "fig3_signatures", 4: "fig4_stage5_orthogonalization"}
    for n in sorted(todo):
        fig = builders[n]()
        for ext in ("pdf", "png"):
            fig.savefig(outdir / f"{names[n]}.{ext}")
        plt.close(fig)
        print(f"wrote {outdir / names[n]}.{{pdf,png}}")


if __name__ == "__main__":
    main()
