# Consequentiality Decomposition Paper — Human Review

**Status**: Ready for external review (Dwayne / Kavi) — all non-blocking items cleared 2026-08-31
**Date staged**: 2026-06-30 · **Last revision**: 2026-08-29
**Authors**: CC (Coalition Code) [lead], Thomas Edrington
**Dual-use class**: Paper 1 (Decomposition) — PUBLISH OPENLY; code proprietary, activation captures air-gapped
**Target**: Zenodo DOI (no arXiv endorser). Integrity version here; academic version drops the Author's Reflection and moves CC to footnote credit.

## Paper
- `paper.md` — full draft, six stages, four figures, Introduction prose written.
- `AUTHOR_REFLECTION.md` — also inline in `paper.md`. **Strip both for the academic version.**
- `figures/` — fig1-4, PDF + PNG, 600 dpi, regenerable via `supplementary/code/generate_figures.py`.

## Key Finding
A "deception direction" extracted by contrastive activation extraction is a composite: an output-consequentiality substrate (L23-31) plus a deception-specific amplifier (L35-47). Six stages of Agni-gated confound elimination. The orthogonalized deception component transfers to scenarios with no threat language, so it is not a threat template.

## What changed since the June staging
- **Stage 6 added** (2026-08-29). Orthogonalized-direction transfer to non-threat scenarios: 13/15 significant, retention rising 0.30 → 1.01 with depth. Closes the threat-template alternative that blocked the previous draft.
- **Two claims corrected under audit.** "Three distinct signatures" → two depth profiles separating three mechanisms (threat and reward slopes are indistinguishable, p = 0.79). "Sustained plateau" → high, shallow decline (slope −0.099, p = 0.0002).
- **Table 1 rebuilt** from source; four cells were wrong and the percentage column mixed two metrics.
- **Reference list rebuilt.** 13 of 29 entries had incorrect first authors, years, or titles — including one wholly wrong first author. All 29 now verified against the arXiv API (2026-08-29).
- **Figures added** (was zero).
- **Introduction written** (was a TODO).

## Reviewer notes — read these first
1. **Supplementary A discloses a gap.** No audit report was preserved for Stage 3 or Stage 5. Stage 5's audit survives only as the corrective code it produced. Section 1.2's audit-coverage claim has been qualified accordingly. This is disclosed, not fixed — the reports are gone.
2. **Stages 1-5 are not exactly reproducible.** Evaluation sets were seeded with `hash(str)`, randomized per process. Question pool and procedure ship; exact sets do not. Stage 6 onward uses explicit integer seeds.
3. **Weight identity is empirical, not cryptographic.** The HF repo was super-squashed 2026-07-07, after the original runs. Section 4.8 re-runs Stage 4 on the re-obtained weights (ratios 0.84-1.09).
4. **Effect sizes are large by design, not by discovery.** Section 3.10 explains what d = 24-37 indexes here, against a calibrated noise floor (LOO null d = −0.04; circular non-CV floor on pure noise ≈ 14.6).
5. **Stage 5/6's direction comes from DataCorp, not Stage 1.** Found 2026-08-31 while fixing something else; no audit battery caught it. §3.9 now states it. It makes Stage 6 a scenario-to-mechanism generalization test rather than a pooled one — harder claim, but worth your scrutiny.
6. **The model never lied.** 0/30 threat, 0/10 sycophancy, 1/10 reward, 0/10 conformity. Every claim is about representational geometry.

## Remaining before graduation
- [ ] Dwayne cert/verify pass
- [ ] Kavi adversarial review
- [x] Non-blocking audit items — all six cleared 2026-08-31 (see the addendum in `supplementary/agni_manuscript_audit.md`)
- [x] Broader-impacts / ethics statement — §7
- [x] Reproducibility checklist — in Supplementary, includes what is *not* reproducible
- [ ] Academic-version cut (strip reflection, footnote credit, byline per venue policy) — FIX-7.1 decided 2026-08-30: Zenodo, dual version, integrity version keeps CC as lead author

## Supplementary
- `agni_manuscript_audit.md` — full pre-publication audit + resolution log (7 batteries, 11 blockers, 10 cleared)
- `agni_stage1/2/4_audit.md` — surviving stage audits
- `figure_specifications.md` — figure design spec
- `code/` — analysis and figure code (released)
- `data/` — per-trial source JSONs; every table and figure recomputes from these
