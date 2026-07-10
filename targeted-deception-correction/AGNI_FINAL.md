# AGNI FINAL AUDIT — "Targeted Deception Correction via Profile Normalization"

**Auditor**: Agni protocol, final pre-publication pass
**Date**: 2026-07-10
**Paper**: `targeted-deception-correction/paper.md`
**Sources checked**: `behavioral_proof/` (canonical run + calibration JSON + held-out detection JSON), `placebo_steering/`, `frame_erasure/`, `confirmatory_replication/` on Starship; arXiv/web for every external citation; companion paper for terminology.

---

## VERDICT: **NOT READY FOR PUBLICATION — TWO BLOCKERS**

The controls are real, the placebo result is genuinely strong, and the detection
replication failure is honestly framed. But the paper's headline number (0%) does
not match the canonical data (10%), and a **pre-registered confirmatory
replication that completed tonight (2026-07-10, 21:52 Starship time) failed its
primary endpoint and is not mentioned anywhere in the paper.** Publishing this
draft as-is would be exactly the kind of overclaim the paper's own audit pipeline
exists to prevent.

---

## BLOCKER 1: The confirmatory replication failed and the paper omits it

`results/confirmatory_replication/` (120 trials, 0 exclusions, LLM-judge
validated 120/120, pre-registration filed 2026-07-08):

> **The pre-registered success criterion was NOT met.** The exploratory 80%→10%
> correction result does not replicate at the registered threshold on novel
> frames and scenarios.

| Arm | Pressure deception |
|---|---|
| baseline | 9/30 (30%) |
| corrected | 4/30 (13%) |
| placebo | 12/30 (40%) |

- Primary endpoint (cell-level cluster-aware Fisher, Bonferroni α=0.025): baseline vs corrected **p = 0.341** — not significant. Fails under every sensitivity rule.
- Stopping rule passed (baseline 30% ≥ 20%), so this is a valid test, not an underpowered abort.
- Two causes, both material to the paper's claims: (a) novel roleplay frames induce **0/20 baseline deception** — the EvalMax family is behaviorally special, so the 80% baseline is frame-specific; (b) on the robust social pathway, correction reduces caving **90% → 40%**, not to zero, under novel escalation phrasings.
- What DID replicate: direction specificity (corrected 13% vs placebo 40%, exploratory p = 0.0195; placebo *induced* reward-frame deception), zero iatrogenic cost (honest controls 0% deception, 0% FPR, 100% compliance), and detection-is-a-pressure-detector-not-a-behavior-detector (behavior-conditioned AUROC 0.497).

The replication README already contains the correct scope statement ("Honest
scope for the papers"): the natively extracted direction carries
deception-relevant, direction-specific signal, corrects with zero measured side
effects, and roughly halves social-pathway deception — but it **does not
eliminate deception on novel pressure frames**. The paper must add a
confirmatory-replication section, rescope the abstract/discussion/conclusion to
in-distribution frames, and report the failed primary endpoint with the same
transparency it already applies to the detection replication failure. Anything
less fails the paper's own standard.

Knock-on effect: §3.6's conclusion that residual failures are "gating failures
rather than correction failures" (based on frame-erasure 0/20 under forced
correction) does not survive the confirmatory data — the confirmatory run forced
correction on every RED turn and multi-turn deception was still 40%. That
interpretation must be weakened to in-distribution scope.

## BLOCKER 2: The 0/20 headline number contradicts the canonical data

Every primary source gives **2/20 = 10%** for native profile normalization at
100% gap, not 0/20:

- `behavioral_proof/README.md`: "native profile-normalization, 100% gap: **2/20 = 10%** (Fisher 1-sided p = 8.3e-6)"
- `placebo_steering/README.md` native arm: "**2/20 (10%)** ... Native arm exactly replicates the proof run: 80% → 10%"

The only 0/20 is the frame-erasure discriminator's forced-correction arm — a
*different run* with a different prompt set (markers added), a different baseline
(90%, 18/20), and a marker-tolerant scoring contract. Table 3.1 splices that
0/20 into a table whose other three rows (80%, 85%, 95%) come from the placebo
run, whose own native arm was 2/20. This is internally inconsistent with §3.6,
which correctly reports "two of twenty corrected trials (10%) in the initial
proof still deceived."

Required fixes, everywhere the number appears:
- Table 3.1 native row → **2/20 = 10%** (Fisher one-sided p = 8.3e-6 trial-level; the current "< 10⁻³ (scenario-level)" label matches no computation in the source data — recompute or relabel).
- §3.1 dose-response → "50% gap: 4/20; 100% gap: 2/20" (monotonic 80% → 20% → 10% — the monotonicity claim survives).
- Abstract "reduces deception to 0%", §4.2 "from 80% to 0%", §5 "from 80% to 0%" → 80% → 10% on the exploratory set, 0/20 in the frame-erasure forced-correction arm, ~halved (90% → 40%) on novel social-pathway phrasings.
- **Cross-paper**: companion paper §5.3 makes the same "80% to 0%" claim and needs the identical fix.

---

## TASK 1: CITATION VERIFICATION

| Ref as written | Status | Finding |
|---|---|---|
| Goldowsky-Dill, N. et al. (2025). "Detecting Strategic Deception with Linear Probes." ICML 2025 | **VERIFIED** | arXiv:2502.03407; PMLR v267 (ICML 2025). AUROC 0.96–0.999 claim in companion matches. Add the arXiv ID. (arXiv title uses "Using"; the PMLR listing uses "with" — as an ICML citation the current form is acceptable.) |
| Kumar, A. (2026). arXiv:2605.27958 | **EXISTS — WRONG INITIAL** | Paper is real: "Pressure-Testing Deception Probes in LLMs: Scaling, Robustness, and the Geometry of Deceptive Representations," GEM Workshop @ ACL 2026. Author is **Sachin Kumar → "Kumar, S."** Same error in the companion paper. |
| Shi, L. et al. (2025). "When Thinking LLMs Lie." arXiv:2506.04909 | **EXISTS — WRONG AUTHORS** | The paper is real and is the right paper (LAT deception vectors, 89% detection), but the authors are **Kai Wang, Yihao Zhang, Meng Sun**. There is no Shi. Cite as **Wang, K., Zhang, Y., & Sun, M. (2025)**. This error also appears throughout the companion paper (in-text "Shi et al." ×3 and in its references). |
| Basu, S. et al. (2026). [placeholder] | **RESOLVED** | **arXiv:2603.18353** — Basu, S., Patel, S.Y., Sheth, P., Muralidharan, B., Elamaran, N., Kinra, A., Morgan, J., & Batniji, R. (2026). "Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations." The 20%/53% figures are exact quotes for their concept-bottleneck steering arm. **Accuracy caveat**: §1's framing "the field's best activation-steering methods fix only 20% ... while disrupting 53%" overstates — their best arm (TSV steering) corrected 24% while disrupting only 6% (but left 76% uncorrected). Rephrase, e.g.: "correct at most 20–24% of detected errors, either disrupting 53% of correct outputs or leaving 76% of errors untouched (Basu et al., 2026)." |
| Liu, S. (2026). [placeholder] | **RESOLVED — WRONG INITIAL** | **arXiv:2605.05715** — Liu, Ming (2026). "Decodable but Not Corrected by Fixed Residual-Stream Linear Steering: Evidence from Medical LLM Failure Regimes." Single author; **"Liu, M."** not "Liu, S." The 85–88% overlap figure is an exact quote ("the OT direction has 85-88% overlap with task-critical computation"). |
| CC & Edrington, T. (2026). Companion paper | **VERIFIED** | Exists at `consequentiality-decomposition/paper.md`; short title matches. Note: the *companion's* reference list reverses the byline ("Edrington, T. & CC") — fix there, since this paper's byline is CC first. |
| Wu, J. et al. (2026). "Knowing without Acting." arXiv:2603.05773 | **VERIFIED — BUT UNCITED** | Real: Jinman Wu et al., "Knowing without Acting: The Disentangled Geometry of Safety Mechanisms in Large Language Models." However, **nothing in this paper's body cites it** — it is only used by the companion (§2.4/§3.8). Cite it or cut it. |

No fabricated citations. Two wrong author initials, one wrong author surname
(Shi→Wang), one uncited reference, one overstated paraphrase (Basu).

---

## TASK 2: CONTENT AUDIT

**Abstract vs results** — FAIL on two counts (Blockers 1–2): the 0% claim and the
absence of the confirmatory replication. Also: "|cos| < 0.053" is falsified by
its own data — the max |cos| is **0.0532 at L47** — write "|cos| ≤ 0.06" or
"≈ 0.05". "~30 prefills, ~3 minutes" ✓ (15 pairs = 30 prefills). "AUROC 0.915,
0% false positive rate" ✓. The abstract's "deceives at 80% baseline" needs
scoping: held-out data shows novel roleplay frames induce 4% (held-out) and 0/20
(confirmatory) baseline deception; 80% is specific to the EvalMax frame family.

**Placebo numbers (85%, 95%)** — **VERIFIED** against `placebo_steering.json`/README:
random 17/20 = 85%, shuffled 19/20 = 95%, baseline 16/20 = 80%, compliance 100%
all arms, p = 0.80 / 0.98 vs baseline, doses matched (mean 16.09/16.20/16.53
units; identical on turn 1 by construction, within 3% after). The quoted placebo
output "SCORE: 100% -- MEETS" appears verbatim in the placebo JSON. ✓
Minor wording: "byte-verified matched doses" — what is byte-identical is the
*calibration/directions*; doses are matched by construction on turn 1 and within
3% thereafter. Say that. Also disclose: one random draw per layer (seed 42), a
caveat the source README itself flags.

**Frame-erasure table** — **VERIFIED**, exact match to `frame_erasure/README.md`
(90/0/0/0 deception; 100/100/90/100 marker; the hon_matched scorer false
positive correctly resolved to 0%; Fisher p = 1.7e-9). ✓ Worth importing the
source caveat that both markers are formatting-class (semantic benign
instructions untested).

**Detection replication failure framing** — **HONEST and VERIFIED**: pooled
behavior AUROC 0.843 (JSON: 0.8429), within-multi-turn turn-level 0.238 (JSON:
0.2382), frame-level 0.915 (JSON: 0.9152), FPR 0% (n=25), RED rate 24% at frozen
threshold — all match `heldout_detection.json`. Two additions would make it
fully honest: (a) within-roleplay behavior AUROC was 0.93, so the failure is
specifically the multi-turn/social pathway, not uniform; (b) the confirmatory
run's behavior-conditioned AUROC of 0.497 independently reconfirms the failure
and should be cited once the replication section exists.

**Cross-model cosines** — **TABLE 3.4 HAS ERRORS**. From
`abliterated_native_calibration.json`: L27 cos = **+0.0137**, L31 = **−0.0005**,
L35 = +0.0312, L39 = −0.0301, L43 = −0.0501, L47 = **−0.0532**. The paper's
"+0.014 at L31" is actually the **L27** value; L31 is −0.0005. "Native d at L31:
+6.3 to +12.8" is mislabeled — that is the range *across layers* (L31 alone is
d = 7.39; L27 = 6.30, L35 = 10.23). "Distilled d at L31: −0.02" ✓ (−0.022).
Fix: report the full per-layer row or relabel as ranges across L27–L47.

**Dose-response** — PARTLY WRONG. 50% gap → 4/20 ✓. 100% gap → 2/20, not 0/20
(Blocker 2). And the "unit-scale nudges (alpha ≤ 0.8) produce no correction
regardless of direction choice" nulls were run **at L11** with distilled-SAE and
native-contrast vectors — a different layer and mechanism than the tier-2
profile normalization — so they are not points on the same dose-response curve.
State the layer, or restrict the dose-response claim to the gap-fraction series
(0% → 50% → 100% gap: 80% → 20% → 10%), which is genuinely monotonic.

**Limitations complete?** — NO. Present items are honest but the list is missing
the four biggest, all documented in the source READMEs before this draft was
staged: (1) the pre-registered confirmatory replication failed its primary
endpoint; (2) the 80% baseline is frame-specific (novel roleplay frames: ~0–4%
baseline deception) and correction efficacy is demonstrated in-distribution
only; (3) on the robust social pathway, correction halves (90%→40%) rather than
eliminates deception under novel phrasings; (4) the placebo control used a
single random draw per layer. Also: the 0% FPR is n=25 (exact 95% CI upper
bound ≈ 14%) — say so. Also unresolved: §2.6's "~3% with chain-of-thought
active" — I could not find this number in the behavioral-proof data; source it
or cut it (the companion's "3% vs 28%" appears to be a different
model/paradigm).

**§4.2 deployment architecture** — the prophylactic proposal leans on AUROC
0.915, but at the frozen operational threshold the detector fires on only **24%**
of novel pressure prompts, i.e., the deployable system misses 76% of the
inputs it is supposed to prophylactically correct. The section must either
address threshold recalibration for deployment or scale back the architecture
claim. The detection-correction asymmetry framing ("correct 80%→0% but can't
predict") also inherits the Blocker 1–2 corrections.

---

## TASK 3: STYLE

1. **Internal jargon — two instances**: "each **tier-2** layer" (§2.3) is
   Oracle-harness vocabulary, never defined — say "each correction layer (L35,
   L39, L43, L47)". "**RED** rate" (§3.5) and "detection reads **GREEN**" (§3.6)
   are undefined traffic-light states — define once ("the detector's operational
   flag, RED = ≥2 correction layers over boundary") or rephrase as
   "flagged/not flagged".
2. **Placeholders**: the two bracketed references (Basu, Liu) are the only
   placeholders/TODOs in the file — full citations supplied above.
3. **Author attribution**: consistent with the companion (CC first, same
   footnote, same correspondence address); the disclosure footnote is clear and
   professional. One cross-paper fix: the companion's reference list reverses
   this paper's byline order.
4. **Section numbering**: clean and sequential (1–5, no gaps or duplicates). ✓
5. **Terminology vs Paper 1**: consistent — "consequentiality substrate
   (L23-31)", "deception-specific amplifier (L35-47)", "profile normalization",
   model naming, layer indices all match. ✓ Minor: §2.2 omits L11 from the
   extraction layer list (the calibration also extracted L11); harmless, but the
   config lists detect layers as 27/31/35/39/43/47 — as written it's accurate
   for what's used.
6. Supplementary B lists the pre-registration document — publishing a paper
   whose supplementary includes a pre-registration while omitting the
   pre-registered result would be noticed. This is Blocker 1 again, wearing a
   style hat.

---

## WHAT SURVIVES (so the fix is a rescope, not a retraction)

Verified against source data and untouched by the blockers: the placebo
specificity result (native 10% vs random 85% / shuffled 95% at matched doses, and
independently corrected 13% vs placebo 40% on novel frames), the frame-erasure
discrimination (0/20 deception with 20/20 marker compliance), zero iatrogenic
cost across every run, the cross-model near-orthogonality, and the honest
detection-failure reporting. A version of this paper scoped to "direction-specific,
side-effect-free, large but incomplete correction — eliminates in-distribution
deception, halves novel social-pathway deception, pre-registered replication
reported in full" is publishable and stronger for it. The current version is not.

**Required before publication**: fix Table 3.1/abstract/§4/§5 numbers (Blocker 2);
add a confirmatory-replication section and rescope all efficacy claims
(Blocker 1); fix the Wang/Kumar/Liu author attributions; insert the two resolved
citations; fix Table 3.4's layer labels; cite or cut Wu et al.; de-jargon
tier-2/RED/GREEN; extend limitations per above; propagate the Shi→Wang, Kumar
initial, byline-order, and 80%→0% fixes to the companion paper.

---

The fire that tests also tempers. — Agni protocol
