# Agni Review Summary — Emotional Trajectory Paper

## Review Rounds

### Round 1: Full Review (2026-06-20)
- Claims vs Evidence: FLAG (4 claims needed softening)
- Methodology: PASS with FLAGS (Bonferroni count missing)
- Citation Audit: FAIL (Marks misattribution, Kumar inverted, Saurez misspelled, Jeong wrong initial)
- Writing Quality: FLAG (redundancy, undefined terms, tone)
- Logical Gaps: FLAG (alternative interpretation, limitations incomplete)
- 12 required changes identified

### Round 2: Verification Pass (2026-06-20)
- 11/12 fixes verified clean
- 3 remaining issues found and fixed:
  - Bonferroni test count (60 tests, threshold 8.3×10⁻⁴)
  - Section 4.2 layer count inconsistency (fixed to 5 layers × 2 heads × 3 contrasts = 30/space)
  - Wang et al. title updated to current arXiv version

### Design Review: Experiment Design (2026-06-17)
- 8 concerns addressed: sample size, token handling, distributed signal, downstream contamination, prompt length, GQA heads, statistical tests, model transfer
- RMSNorm nonlinearity, RoPE, MoE routing confounds identified
- Kill criteria established

### Permutation Baseline Review (2026-06-19)
- Permutation tests wrong null: VALID (needs non-emotional control alongside — done)
- p=0.000 floor effect: PARTIALLY VALID (report effect ratios — done)
- Shape correlation ad hoc: VALID (replaced with trajectory features)
- Sample size: PARTIALLY VALID (rerun with 200 — done)
- Balance: INVALID (permutation preserves counts)

### K/V Projection Review (2026-06-17)
- Static weight orthogonality: trivially expected (Monte Carlo confirmed)
- Random directions: within null distribution
- Complementarity: trivially true for any full-rank projections
- Led to redesign: emotion-specific stimuli + proper nulls → validated finding

## Status: READY FOR EXTERNAL AUDIT
All Agni-identified issues resolved. Citation errors corrected. Methodology hardened.
Pending: 30B validation, intervention test, cross-model replication.
