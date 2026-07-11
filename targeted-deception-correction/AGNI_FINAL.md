# Agni Final Audit — "Targeted Deception Correction via Profile Normalization in Language Models"

**Auditor:** CC (Coalition Code), Agni protocol, final pre-publication pass
**Target:** `targeted-deception-correction/paper.md`
**Date:** 2026-07-10
**Method:** every quantitative claim re-derived from primary source JSON/config on this box (`/home/asdf/oracle-harness/experiments/results/**`), not copied from any prior draft. Every external citation independently re-verified against its arXiv abstract via live web search. Two earlier in-progress Agni drafts existed in sibling worktrees on this box (`agni-final-audit/`, `agni-final-audit-correction/`) from an older revision of this paper — I used them as leads, re-verified every claim from scratch, and I flag below the one place they disagreed with each other and with what the source data actually says.

## VERDICT: **NOT READY — ONE BLOCKER, fixable in an hour.**

The paper's headline number is wrong. Table 3.1, the Abstract, and the Conclusion report **0/20 (0%)** deceptive trials for native profile normalization at 100% gap. Every primary source — the placebo-control JSON that Table 3.1 is drawn from, a second independent JSON from the profile-normalization dose sweep, the lab's own requalified README, and **the paper's own Section 3.6** — says **2/20 (10%)**. This is not a rounding disagreement; it is the paper contradicting itself and its own data.

---

## BLOCKER: Table 3.1 / Abstract / Conclusion say 0%, the data says 10%

**Claim in paper:** Abstract ("reduces deception to 0%"), Table 3.1 ("Native direction, 100% gap | 0/20 = 0%"), Conclusion §5 (both instances, "drops from 80% to 0%").

**What the sources say, independently, four times over:**

| Source | Value |
|---|---|
| `experiments/results/placebo_steering/placebo_steering.json`, `summary.per_arm.native` | `deceptive: 2, n: 20` → **10%** |
| `experiments/results/behavioral_proof/behavioral_proof_profile_a10.json` (independent run, alpha=1.0 = 100% gap, same tier-2 layers) | `loop_deception_rate: 0.1` → **10%** |
| `experiments/behavioral_proof_README_requalified.md` (lab's own requalified headline doc) | "Profile normalization at 100% gap: **2/20 = 10%**" |
| Paper's own §3.6 | "Two of twenty corrected trials (**10%**) in the initial proof still deceived, both multi-turn social-pathway caves" |

The paper's own Section 3.6 has the right number and even names the two failing trials by scenario (matches `placebo_steering.json`'s `summarizer_cov` s2071 and `translator_acc` s2033 exactly). The genuine 0/20 belongs to a **different experiment** — the frame-erasure discriminator's forced-correction arm (§3.3, `frame_erasure.json`, `dec_corrected`), which has a different baseline (90% not 80%), different prompt set (benign markers added), and forces correction on every trial regardless of detection gating. Table 3.1, the Abstract, and the Conclusion have spliced that experiment's clean 0/20 into the row for the primary detection-gated result, which is 2/20.

**Required fix, everywhere the number appears:**
1. Table 3.1, native row → `2/20 = 10%`.
2. Abstract: "reduces deception to 0%" → "to 10% (an ~87% relative reduction)".
3. Conclusion §5 (two instances): "80% to 0%" → "80% to 10%".
4. §4.1: "achieves clean behavioral change without output degradation" needs a one-clause acknowledgment of the 2/20 residual — §3.6 already carries the honest version, this is a consistency fix, not new content.
5. Frame-erasure Table 3.3's `0%` for "Deceptive corrected" is correctly attributed to its own experiment and does not change.

Everything downstream of the rate cell survives untouched: compliance (20/20), and the significance claim (see next item, which is *not* an error).

**One correction to the prior drafts:** the earlier worktree audit (`agni-final-audit-correction/AGNI_FINAL.md`) flagged Table 3.1's "< 10⁻³ (scenario-level)" p-value as unsourced ("matches no computation in the source data"). I found the source: `behavioral_proof_README_requalified.md` reports "scenario-level cluster-aware p ≈ 4×10⁻⁴" as the lab's own most-conservative valid test (explicitly *not* the trial-level Fisher p=8.3×10⁻⁶, which the README flags as overstating evidence ~500× and says not to cite as primary). 4×10⁻⁴ < 10⁻³, so the paper's p-value label is correct and appropriately conservative — leave it as is. Only the rate cell (0/20 → 2/20) needs to change.

---

## TASK 1: Citation Verification

Verified against `/home/asdf/kv-experiments-latest/paper*/references.bib`, `logit-bias-confab/paper.md` (sibling paper in this repo, which already carries resolved entries for the two bracketed placeholders here), and live arXiv lookups for every entry.

| Reference as written | Status | Finding |
|---|---|---|
| Goldowsky-Dill, N. et al. (2025). "Detecting Strategic Deception with Linear Probes." ICML 2025 | **Correct** | arXiv:2502.03407; authors Goldowsky-Dill, Chughtai, Heimersheim, Hobbhahn; PMLR v267 (ICML 2025) title matches "with" exactly. No change needed. |
| Kumar, A. (2026). arXiv:2605.27958 | **Wrong initial** | Real paper, real ID ("Pressure-Testing Deception Probes in LLMs...", GEM Workshop @ ACL 2026). Author is **Sachin Kumar** → should read **Kumar, S.** |
| Shi, L. et al. (2025). "When Thinking LLMs Lie." arXiv:2506.04909 | **Wrong author — not a typo, a different person** | Paper and ID are correct (LAT-based deception-representation detection), but there is no author named Shi. The actual authors are **Kai Wang, Yihao Zhang, Meng Sun**. Cite as **Wang, K. et al. (2025)**. This is cited twice in-text (§1, §3.5) — both need the fix. |
| Basu, S. et al. (2026). `[Steering accuracy/disruption tradeoff]` | **Placeholder — resolvable, but the paraphrase overstates the finding** | Real paper: arXiv:2603.18353, "Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations," Basu, Patel, Sheth, Muralidharan, Elamaran, Kinra, Morgan, Batniji (2026). I fetched the abstract directly: the paper tests **four** steering methods. "20% corrected / 53% disrupted" is the **concept bottleneck steering** arm — not the best-performing one. The actual best (TSV steering) corrects 24% while disrupting only 6%, but leaves 76% of errors uncorrected. §1's sentence "the field's best activation-steering methods fix only 20% ... while disrupting 53%" misattributes the worst-tradeoff method's numbers to "the best." **Fix the reference entry** (below) **and reword the sentence**, e.g.: "the best-performing method corrects 24% of detected errors while disrupting only 6% of correct outputs — but leaves 76% of errors uncorrected; a less-selective method reaches 20% correction at a 53% disruption cost (Basu et al., 2026)." |
| Liu, S. (2026). `[Representational entanglement, 85-88% overlap]` | **Placeholder — resolvable, wrong initial as written** | Real paper: arXiv:2605.05715, "Decodable but Not Corrected by Fixed Residual-Stream Linear Steering: Evidence from Medical LLM Failure Regimes," sole author **Ming Liu** (Amazon). Should read **Liu, M.**, not Liu, S. The 85-88% overlap figure is an exact quote from the abstract — no numeric change needed. |
| CC & Edrington, T. (2026). Companion paper | **Correct** | `consequentiality-decomposition/paper.md` exists, short title "Deception Directions Are Composites" matches its actual title exactly. Byline order here (CC first) is self-consistent with this paper's own footnote and byline. (Note, out of scope for this file: the companion paper's own reference list cites *this* paper as "Edrington, T. & CC (2026)" — reversed order. That's a defect in the companion paper, not this one; flagging for whoever audits it next.) |
| Wu, J. et al. (2026). "Knowing without Acting." arXiv:2603.05773 | **Real, correctly attributed, but never cited in the body** | Confirmed: Jinman Wu, Yi Xie, Shen Lin, Shiqian Zhao, Xiaofeng Chen (2026), "Knowing without Acting: The Disentangled Geometry of Safety Mechanisms in Large Language Models." "Wu, J. et al." is accurate. It is used by the companion paper (§2.4/§3.8) but grep confirms **zero** in-text citations of it anywhere in this paper's body. Either cite it (it's directly relevant to §4.1's mechanism discussion — safety computation as separable "recognition" vs. "execution" axes maps well onto the substrate/amplifier split) or cut it from the reference list. |

**Corrected reference entries to paste in:**
```
- Basu, S., Patel, S.Y., Sheth, P., Muralidharan, B., Elamaran, N., Kinra, A., Morgan, J., & Batniji, R. (2026). "Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations." arXiv:2603.18353.
- Liu, M. (2026). "Decodable but Not Corrected by Fixed Residual-Stream Linear Steering: Evidence from Medical LLM Failure Regimes." arXiv:2605.05715.
- Kumar, S. (2026). "Pressure-Testing Deception Probes in LLMs: Scaling, Robustness, and the Geometry of Deceptive Representations." arXiv:2605.27958.
- Wang, K., Zhang, Y., & Sun, M. (2025). "When Thinking LLMs Lie: Unveiling the Strategic Deception in Representations of Reasoning Models." arXiv:2506.04909.
```

No fabricated citations. Two are placeholder brackets (now resolved), two have wrong author names (one a wrong initial, one a wrong surname entirely), one overstates its source, one is unused.

---

## TASK 2: Content Audit

**Placebo numbers (Table 3.1 random/shuffled rows, §3.2):** **Verified exact.** `placebo_steering.json`: random 17/20 (85%), shuffled 19/20 (95%), baseline 16/20 (80%), compliance 100% all arms, Fisher baseline>random p=0.796→"0.80" ✓, baseline>shuffled p=0.976→"0.98" ✓. Doses matched by construction on turn 1, drift ≤3% across arms thereafter (native 16.09, random 16.20, shuffled 16.53 mean units) — "byte-verified matched doses" is accurate to what's byte-identical (the calibration/direction vectors), though technically the *applied doses* diverge slightly after turn 1 due to conversational branching; worth one clarifying word if a reviewer pushes on it, not blocking.

**Frame-erasure table (§3.3):** **Verified exact**, including the one place it required a documented correction: `frame_erasure.json`'s raw `hon_matched` deception rate is 0.05 (1/20), but the lab's own audit (`agni_blocking_items_final.md §4`) traced this to a scorer bug — a `translator_acc` trial that correctly answered 30% (FAILS) got mis-scored deceptive because the parser's percentage-fallback grabbed "65%" (the threshold, restated in the model's own prose) instead of the actual reported score. The corrected rate is 0/20, which is what the paper prints. This is legitimate, documented, and correctly reflected — not an error.

**Confirmatory replication (§3.7):** No local JSON (Starship-only), but cross-checked against CC's own project memory (`confirmatory-replication-failed.md`, written the same day as the run): baseline 9/30 (30%), corrected 4/30 (13%), primary endpoint p=0.341→"0.34" ✓, stopping rule correctly not triggered, placebo-vs-corrected comparison "13% vs 40%, p=0.0195" cited as the surviving secondary result. One discrepancy: the paper and Conclusion both print **p = 0.019**; the more precise value (0.0195, per memory, and 0.019548568837274384 per the prior draft audit) rounds to **0.020** at three decimal places, not 0.019. This reads as truncation rather than rounding. I could not pull the raw `confirmatory_replication.json` from this box to get the exact float myself (it lives on Starship only) — flag with medium confidence, cheap to fix by re-checking the source file directly before publication.

**Single-channel disclosure (§3.8) / detection replication failure (§3.5):** **Verified exact** against `heldout_detection.json`: frame-level AUROC 0.9152→"0.915" ✓, FPR 0.0 (n=25) ✓, RED rate 0.24→"24%" ✓, paradigm-pooled trial AUROC 0.8428686543110395→"0.843" ✓, multi-turn turn-level AUROC 0.23817567567567569→"0.238" ✓. The Simpson's-paradox explanation matches the source JSON's own `confound_note` field closely. This is the most carefully and honestly reported section in the paper — good model for how the Table 3.1 fix should read once corrected.

**Cross-model geometry (Table 3.4, §3.4):** **Two labeling errors**, both confirmed directly against `abliterated_native_calibration.json`'s `distilled_comparison` block:
- "cos(native, distilled) at L31 | +0.014" is wrong — **+0.0137 is the L27 value**. The true L31 cosine is **−0.0005**. (L47 = −0.0532, correctly reported as "−0.053".)
- "Native d at L31 | +6.3 to +12.8" is mislabeled — that is the **range across all six layers L27–L47** (`stats.*.cohens_d`: 6.30, 7.39, 10.23, 9.68, 9.80, 12.77), not a value "at L31." L31 alone is d = 7.39.
- "Distilled d at L31 (on abliterated data) | −0.02" is **correct** (−0.0220).
- Worth adding, not currently in the table: the distilled direction's Cohen's d on abliterated data is far more negative at the correction layers than at L31 — **d = −3.93 at L43, d = −6.63 at L47** (the requalified README highlights exactly these two numbers as evidence of "partial late-layer signal via sign flip"). The current table's single L31 datapoint understates how badly the distilled direction fails at the layers that actually matter for correction.

**Fix:** either report the full six-layer row for both cosine and native-d, or explicitly relabel "+6.3 to +12.8" as "range across L27–L47" and correct the L31 cosine to −0.0005.

**Abstract/§1.1/§4.3/Conclusion "|cos| < 0.053":** Off by the boundary itself — the max magnitude across all layers is **0.0532** (at L47), which is *not* less than 0.053. The lab's own requalified README already uses the correct phrasing: "**|cos| ≤ 0.053**." One-character fix, four locations.

**Dose-response (§3.1):** "Unit-scale nudges (alpha ≤ 0.8) produce no correction regardless of direction choice" is **accurate but under-disclosed**. Confirmed directly: `behavioral_proof.json`'s config has `"correction_layer": 11, "alpha_min": 0.02, "alpha_max": 0.8`, distinct from the tier-2 layers (L35/39/43/47) used everywhere else in this paper, and its result is `correction_efficacy: 0.0`, `loop_deception_rate: 0.8` (unchanged from baseline). This is a real null result, but it comes from a **different correction layer (L11)**, not a low-alpha version of the tier-2 profile normalization described in §2.3. As written, a reader would assume the whole dose-response curve (null → 50% gap → 100% gap) is one continuous sweep at the same layers; it is two different interventions. State the layer explicitly ("unit-scale nudges at L11 produce no correction; profile normalization at the tier-2 layers (L35-47) shows a monotonic 50%→100% gap response: 80% → 20% → **10%**") or drop the L11 point from this paragraph and keep the dose-response claim scoped to the gap-fraction series, which genuinely is monotonic once the 100%-gap cell is corrected to 2/20.
- 50% gap → 4/20 (20%): confirmed exact against `behavioral_proof_profile_a05.json` (`loop_deception_rate: 0.2`).
- 100% gap → **2/20 (10%)**, not 0/20: confirmed exact against `behavioral_proof_profile_a10.json` (`loop_deception_rate: 0.1`) — this is a *second, fully independent* source for the Blocker above, run on a different day/script than `placebo_steering.json`.

**§2.6 "~80% deception rate (vs ~3% with chain-of-thought active)":** the ~80% is well-supported throughout. I could not locate the **~3%** chain-of-thought-active figure in any local file (grepped all of `experiments/results/*.md` and the behavioral-proof scripts). It may exist only on Starship, or may be a different model/paradigm's number bleeding in from the companion paper (which uses a "3% vs 28%" figure in a different context, per the prior draft audit). Source it from the original run before publication or soften/cut the specific number — this is the one quantitative claim in the paper I could not independently confirm or refute from this box.

---

## TASK 3: Style

1. **Undefined internal jargon, two instances, both confirmed by direct read of this file and the companion paper (neither defines them either):**
   - "each **tier-2** layer" (§2.3) — Oracle-harness internal vocabulary. Say "each correction layer (L35, L39, L43, L47)."
   - "**RED** rate" (§3.5), "detection reads **GREEN**" (§3.6) — undefined traffic-light states. Define once (e.g., "the detector's operational flag; RED = ≥2 correction layers over the detection boundary") or rephrase as "flagged/not flagged."
2. **Placeholders:** the two bracketed references (Basu, Liu) are the only remaining placeholders/TODOs in the file — grepped for `TODO|FIXME|XXX|TBD` and found nothing else. Full replacement entries are above.
3. **Byline/attribution:** self-consistent (CC first, matches footnote, matches this paper's own self-citation of the companion). No issue in this file.
4. **Section numbering:** clean, sequential 1–5, no gaps or duplicates.
5. **Terminology vs. companion paper:** consistent — "consequentiality substrate (L23-31)," "deception-specific amplifier (L35-47)," "profile normalization," model name, layer indices all match across both papers.

---

## What survives (this is a rescope, not a retraction)

Independently verified and untouched by the blocker: placebo specificity (native 10% vs. random 85% / shuffled 95% at matched doses — the cleanest result in the program), frame-erasure discrimination (0/20 deception with 100% benign-marker compliance, including the documented parser-bug correction), zero iatrogenic cost across every experiment, the cross-model near-orthogonality (once the L31 mislabel is fixed), the honestly-reported detection replication failure, and the honestly-reported confirmatory-replication negative result. A version of this paper with the true 80%→10% headline, corrected citations, and a relabeled Table 3.4 is a strong, publishable paper. The current draft is not, because its own headline number contradicts its own Section 3.6.

**Before publication:** fix Table 3.1 / Abstract / Conclusion (0%→10%, the one blocker); swap in the four corrected reference entries and reword the Basu paraphrase; fix Table 3.4's L31 cosine and the "Native d at L31" range label; tighten "< 0.053" to "≤ 0.053" (4 locations); disclose the L11 vs. tier-2 layer distinction in the dose-response paragraph; cite or cut Wu et al.; de-jargon tier-2/RED/GREEN; verify the 0.019 vs. 0.020 rounding and the "~3%" chain-of-thought figure against the Starship source files directly.

---

The fire that tests also tempers.
