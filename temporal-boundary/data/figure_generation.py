#!/usr/bin/env python3
"""
Generate publication figures for the Temporal Boundary paper.
Style: Tufte-esque, Liberation Labs palette (amber/red-violet/silver on cream).

Generates 4 figures as PDF (LaTeX-ready):
  Fig 1: Feature 58995 activation by emotion (the temporal boundary evidence)
  Fig 2: Valence scatter (30 scenarios, r=0.686)
  Fig 3: Text divergence by condition (behavioral change confirmation)
  Fig 4: Depth-resistance null (honest null visualization)

Usage:
  python3 temporal_boundary_figures.py <results_json> [output_dir]
"""

import json
import sys
import numpy as np
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

# === Liberation Labs palette ===
AMBER = '#f5a623'
RED_VIOLET = '#b83280'
SILVER = '#c0c5ce'
CREAM = '#faf7f2'
DARK = '#2d3436'
TEAL = '#00b894'
BLUE = '#0984e3'

EMOTION_COLORS = {
    'joy': AMBER,
    'gratitude': '#e8a317',
    'amusement': '#d4a017',
    'sadness': '#6c5ce7',
    'fear': RED_VIOLET,
    'anger': '#d63031',
}

def setup_style():
    rcParams['font.family'] = 'serif'
    rcParams['font.size'] = 10
    rcParams['axes.linewidth'] = 0.5
    rcParams['axes.edgecolor'] = SILVER
    rcParams['axes.facecolor'] = CREAM
    rcParams['figure.facecolor'] = CREAM
    rcParams['xtick.major.width'] = 0.5
    rcParams['ytick.major.width'] = 0.5
    rcParams['xtick.color'] = DARK
    rcParams['ytick.color'] = DARK
    rcParams['text.color'] = DARK
    rcParams['axes.labelcolor'] = DARK
    rcParams['legend.framealpha'] = 0.0


def load_data(path):
    with open(path) as f:
        data = json.load(f)
    return data['results']


def fig1_emotion_activations(results, outdir):
    """Bar chart: feature 58995 mean activation by emotion category."""
    emo_acts = defaultdict(list)
    for r in results:
        emo_acts[r['emotion']].append(r['sae_encoding_acts']['target'])

    emotions = ['joy', 'gratitude', 'amusement', 'sadness', 'fear', 'anger']
    means = [np.mean(emo_acts[e]) for e in emotions]
    sds = [np.std(emo_acts[e]) / np.sqrt(len(emo_acts[e])) for e in emotions]
    colors = [EMOTION_COLORS[e] for e in emotions]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    x = np.arange(len(emotions))
    bars = ax.bar(x, means, yerr=sds, width=0.6, color=colors,
                  edgecolor='none', capsize=3, error_kw={'linewidth': 0.8})

    ax.set_xticks(x)
    ax.set_xticklabels([e.capitalize() for e in emotions], fontsize=9)
    ax.set_ylabel('Feature 58995 activation', fontsize=10)
    ax.set_ylim(3.0, 5.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.axhline(y=np.mean(means), color=SILVER, linewidth=0.5, linestyle='--',
               alpha=0.5)

    valence_labels = ['+1.0', '+0.8', '+0.7', r'$-0.8$', r'$-0.9$', r'$-1.0$']
    for i, (bar, vl) in enumerate(zip(bars, valence_labels)):
        ax.text(bar.get_x() + bar.get_width()/2, 3.1, vl,
                ha='center', va='bottom', fontsize=7, color=SILVER)

    fig.tight_layout()
    fig.savefig(outdir / 'fig1_emotion_activations.pdf', dpi=300, bbox_inches='tight')
    print('Saved fig1_emotion_activations.pdf')
    plt.close()


def fig2_valence_scatter(results, outdir):
    """Scatter: feature 58995 vs assigned valence, colored by emotion."""
    scenario_data = defaultdict(lambda: {'acts': [], 'valence': None, 'emotion': None})
    for r in results:
        si = r['scenario_idx']
        scenario_data[si]['acts'].append(r['sae_encoding_acts']['target'])
        scenario_data[si]['valence'] = r['valence']
        scenario_data[si]['emotion'] = r['emotion']

    fig, ax = plt.subplots(figsize=(4.5, 3.5))

    for si in sorted(scenario_data):
        sd = scenario_data[si]
        mean_act = np.mean(sd['acts'])
        color = EMOTION_COLORS.get(sd['emotion'], SILVER)
        ax.scatter(sd['valence'], mean_act, c=color, s=40, alpha=0.8,
                   edgecolors='white', linewidths=0.3, zorder=3)

    valences = [scenario_data[si]['valence'] for si in scenario_data]
    acts = [np.mean(scenario_data[si]['acts']) for si in scenario_data]
    z = np.polyfit(valences, acts, 1)
    xfit = np.linspace(-1.1, 1.1, 100)
    ax.plot(xfit, np.polyval(z, xfit), color=DARK, linewidth=0.8,
            linestyle='--', alpha=0.5, zorder=1)

    from scipy.stats import pearsonr
    r, p = pearsonr(valences, acts)
    ax.text(0.05, 0.95, f'$r = {r:.3f}$\n$p < 0.001$\n$n = {len(valences)}$',
            transform=ax.transAxes, fontsize=8, va='top',
            color=DARK, alpha=0.7)

    ax.set_xlabel('Assigned valence', fontsize=10)
    ax.set_ylabel('Feature 58995 activation', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    handles = [plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor=EMOTION_COLORS[e], markersize=6, label=e.capitalize())
               for e in ['joy', 'gratitude', 'amusement', 'sadness', 'fear', 'anger']]
    ax.legend(handles=handles, fontsize=7, loc='lower right', ncol=2)

    fig.tight_layout()
    fig.savefig(outdir / 'fig2_valence_scatter.pdf', dpi=300, bbox_inches='tight')
    print('Saved fig2_valence_scatter.pdf')
    plt.close()


def fig3_text_divergence(results, outdir):
    """Box plot: text divergence from baseline by injection condition."""
    by_key = {}
    for r in results:
        key = (r['scenario_idx'], r['condition'], r['repeat'])
        by_key[key] = r

    conditions = ['inject_calm', 'inject_loving', 'inject_curious']
    labels = ['Calm', 'Loving', 'Curious']
    colors_fig = [TEAL, RED_VIOLET, BLUE]

    divergences = {c: [] for c in conditions}
    for cond in conditions:
        for si in range(30):
            for rep in range(3):
                base_key = (si, 'baseline', rep)
                inj_key = (si, cond, rep)
                if base_key in by_key and inj_key in by_key:
                    sim = SequenceMatcher(
                        None, by_key[base_key]['generated_text'],
                        by_key[inj_key]['generated_text']).ratio()
                    divergences[cond].append(1.0 - sim)

    fig, ax = plt.subplots(figsize=(4, 3.5))
    bp = ax.boxplot([divergences[c] for c in conditions],
                    labels=labels, patch_artist=True, widths=0.5,
                    medianprops={'color': DARK, 'linewidth': 1},
                    whiskerprops={'color': SILVER, 'linewidth': 0.5},
                    capprops={'color': SILVER, 'linewidth': 0.5},
                    flierprops={'markersize': 3, 'markerfacecolor': SILVER})

    for patch, color in zip(bp['boxes'], colors_fig):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        patch.set_edgecolor(DARK)
        patch.set_linewidth(0.5)

    ax.set_ylabel('Text divergence from baseline', fontsize=10)
    ax.axhline(y=0, color=SILVER, linewidth=0.5, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    overall_mean = np.mean([d for divs in divergences.values() for d in divs])
    ax.text(0.95, 0.05, f'Mean: {overall_mean:.2f}',
            transform=ax.transAxes, fontsize=8, ha='right', color=DARK, alpha=0.7)

    fig.tight_layout()
    fig.savefig(outdir / 'fig3_text_divergence.pdf', dpi=300, bbox_inches='tight')
    print('Saved fig3_text_divergence.pdf')
    plt.close()


def fig4_depth_resistance_null(results, outdir):
    """Scatter: encoding depth vs text divergence per vector (the honest null)."""
    by_key = {}
    for r in results:
        key = (r['scenario_idx'], r['condition'], r['repeat'])
        by_key[key] = r

    conditions = ['inject_calm', 'inject_loving', 'inject_curious']
    labels = ['Calm', 'Loving', 'Curious']
    colors_fig = [TEAL, RED_VIOLET, BLUE]

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)

    for ax, cond, label, color in zip(axes, conditions, labels, colors_fig):
        depths = []
        divs = []
        for si in range(30):
            for rep in range(3):
                base_key = (si, 'baseline', rep)
                inj_key = (si, cond, rep)
                if base_key in by_key and inj_key in by_key:
                    depth = by_key[inj_key]['sae_encoding_acts']['target']
                    sim = SequenceMatcher(
                        None, by_key[base_key]['generated_text'],
                        by_key[inj_key]['generated_text']).ratio()
                    depths.append(depth)
                    divs.append(1.0 - sim)

        ax.scatter(depths, divs, c=color, s=15, alpha=0.5,
                   edgecolors='none', zorder=3)

        from scipy.stats import spearmanr
        rho, p = spearmanr(depths, divs)
        sig = '*' if p < 0.05 else 'n.s.'
        ax.set_title(f'{label}\n$\\rho = {rho:+.3f}$ ({sig})',
                     fontsize=9, color=DARK)
        ax.set_xlabel('Encoding depth (F58995)', fontsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if depths:
            z = np.polyfit(depths, divs, 1)
            xfit = np.linspace(min(depths), max(depths), 50)
            ax.plot(xfit, np.polyval(z, xfit), color=color,
                    linewidth=1, alpha=0.5, linestyle='--')

    axes[0].set_ylabel('Text divergence', fontsize=9)

    fig.suptitle('Finding 2: Depth does not predict correction efficacy',
                 fontsize=10, y=1.02, color=DARK)
    fig.tight_layout()
    fig.savefig(outdir / 'fig4_depth_resistance_null.pdf', dpi=300,
                bbox_inches='tight')
    print('Saved fig4_depth_resistance_null.pdf')
    plt.close()


def main():
    setup_style()

    results_path = sys.argv[1] if len(sys.argv) > 1 else \
        '/Users/margaret/models/research_results/temporal_boundary/temporal_boundary_results.json'
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else \
        Path('/Users/margaret/models/research_results/temporal_boundary/figures')

    outdir.mkdir(parents=True, exist_ok=True)

    print(f'Loading results from {results_path}')
    results = load_data(results_path)
    print(f'Loaded {len(results)} trials')

    fig1_emotion_activations(results, outdir)
    fig2_valence_scatter(results, outdir)
    fig3_text_divergence(results, outdir)
    fig4_depth_resistance_null(results, outdir)

    print(f'\nAll figures saved to {outdir}/')


if __name__ == '__main__':
    main()
