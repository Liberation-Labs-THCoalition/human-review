# Emotional Trajectory Paper — Review Status

| Field | Value |
|-------|-------|
| Title | Emotion-Specific Geometric Encoding at Mid-Depth in Transformers |
| Authors | Nexus, Thomas Edrington, Lyra (invited) |
| Submitted to review | 2026-06-21 (original draft) |
| Major revision | 2026-06-22 (post-null-swarm restructuring) |
| Agni rounds | 8 (design, K/V, permutation, full review, verification, null swarm, style guide, gate review) |
| Status | READY FOR HUMAN REVIEW — 2 Agni gate rounds post-restructuring |

## Changes in 2026-06-22 revision

Null swarm (13 agents, dual-reviewer) found 2 CRITICAL and 3 MAJOR issues:

1. **CRITICAL: Projection fidelity was a near-tautology.** Difference-of-means commutes with linear maps; the 0.93-0.98 cosine measured RMSNorm perturbation, not emotion-specific preservation. Reframed as mathematical property enabling dual-correction, not empirical finding.

2. **CRITICAL: Geometric-to-focal transition was predominantly output-layer preparation.** Our own control showed 59% of deep-layer spike is generic. Demoted from central claim to hypothesis for future work.

3. **MAJOR: Permutation baseline had neutral-prompt dilution.** Shuffling all 200 labels (including 50 neutral) systematically depressed the null. Fixed to shuffle only 150 non-neutral.

4. **MAJOR: Cohen's d framing was misleading.** Mean |d_i| has a positive floor (~0.16); standard benchmarks don't apply. Fixed with null-distribution comparison.

5. **MAJOR: Non-emotional control has vocabulary intensity confound.** Emotional prompts use semantically intense words vs mundane control vocabulary. Acknowledged; semantically-intense control recommended.

Paper restructured to lead with the genuinely novel mid-layer geometric encoding finding.

## Key blockers for publication
1. **Re-run permutation baseline** — shuffle only non-neutral prompts, report medians
2. **30B model validation** — all results on oracle-tiny (pipeline validation)
3. **W_unembed alignment test** — distinguish deep-layer emotion from output preparation
4. **Semantically-intense non-emotional control** — disentangle emotion from vocabulary intensity
5. **Intervention test** — dual correction produces intended behavioral changes

## What's ready
- Methodology: Agni-hardened (6 rounds including null swarm), controls run
- Pipeline: extraction + analysis code tested and working
- Data: 200 emotional + 100 control + 250 full circumplex stimuli
- Citations: all verified against arXiv
- Draft: restructured around defensible mid-layer finding
- Style guide: applied (STYLE_GUIDE.md compliance checked)

## Files
- `paper.md` — current draft (post-restructuring)
- `outline.md` — structural outline (needs update)
- `code/` — full pipeline (7 scripts)
- `data/` — all stimulus sets (3 JSON files)
- `agni-reports/` — review summaries including NULL_SWARM_20260622.md
