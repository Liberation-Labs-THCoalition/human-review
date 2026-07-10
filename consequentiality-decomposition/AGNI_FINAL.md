# Agni Final Audit — Paper 1: "Deception Directions Are Composites"

**Date**: 2026-07-10
**Auditor**: CC (Agni protocol)
**Target**: `consequentiality-decomposition/paper.md` @ 17de3c4
**Scope**: (1) citation verification, (2) content audit, (3) style guide compliance

---

## VERDICT: NOT READY — ONE FIX PASS REQUIRED

No fabricated citations. No dishonest claims. The core results, the abstract's numbers, and the GWT framing all check out. But the audit found **one citation whose attributed claim the cited paper does not contain**, **one paper attributed to the wrong authors**, **one orphaned result cited in the Discussion that appears nowhere in this paper's Results and contradicts the companion paper's numbers**, and **three limitations that were lost in the two-paper split** — including the single most important one (no behavioral deception occurs anywhere in this paper's experiments). Plus ~12 mechanical reference errors.

Everything is fixable in one focused pass. Nothing requires new experiments.

---

## PART 1: CITATION VERIFICATION (24 references)

Method: every arXiv ID fetched and checked against the actual paper; every attributed claim checked against the source's abstract or full text; venues spot-checked. Four independent verification agents, results cross-compiled.

### 1.1 Tally

| Verdict | Count |
|---|---|
| Verified, claim supported, metadata correct | 8 |
| Verified, claim supported, metadata errors (initial/year/title) | 13 |
| Wrong authors entirely | 1 (Shi → Wang) |
| Claim NOT in cited paper | 1 (McKenzie steering sentence) |
| Fabricated / not found | **0** |
| Internal (companion paper) | 1 |

### 1.2 KILL-LEVEL: claim not supported by cited source

**McKenzie et al. — arXiv:2506.10805** ("Detecting High-Stakes Interactions with Activation Probes"). Section 2.3 states this paper demonstrates "that adding a high-stakes steering vector to low-stakes prompts increases caution while subtracting it increases confidence — confirming a manipulable 'stakes' direction in representation space." **The cited paper contains no steering experiments.** Checked abstract, full v4 HTML, and the authors' companion LessWrong post: it is a detection/monitoring paper only. The first half of the sentence (synthetic-data probes generalizing to real-world contexts) IS supported. The steering half must be **cut or re-sourced** — it may belong to a different paper. Also: first author is **Alex** McKenzie, not "McKenzie, D." (the D. is likely from last author Dmitrii Krasheninnikov). NeurIPS 2025.

This matters more than a normal metadata error because §2.3 uses the steering claim as one of the "two concurrent results [that] closely parallel our finding" — it is load-bearing for the related-work positioning of the consequentiality substrate.

### 1.3 KILL-LEVEL: wrong authors

**"Shi, L. et al. (2025). When Thinking LLMs Lie." arXiv:2506.04909.** The paper at this ID is real and the attributed claims are supported, but its authors are **Kai Wang, Yihao Zhang, Meng Sun**. There is no Shi on the paper. Full title: "When Thinking LLMs Lie: Unveiling the Strategic Deception in Representations of Reasoning Models" (model: QwQ-32B). The in-text citations in §1 and §2.1 must change from "Shi et al." to "Wang et al." as well as the reference entry. Note also: the paper's stable-detection layer range is **39-50** in the quoted text, not "39-55" as §2.1 states — verify against source and correct.

### 1.4 Claim-precision errors (fix wording)

- **Vennemeyer — arXiv:2509.21305**: "Steering selectivity reaches 23-37x" cherry-picks the top of the reported range. Table 2 reports 23.12x/17.24x/22.42x (Qwen 30B) and 6.79x/8.03x/36.82x (Llama 8B) — the honest range is **~6.8-36.8x**. Restate as "up to ~37x" or give the full range. Also first author is **Daniel** Vennemeyer ("D.", not "A.").
- **Laine — arXiv:2407.04694**: "all 16 models tested exceed chance" is not confirmed in the abstract (the 16-model count and the chat>base result are). Spot-check the Stages task results in the paper body, or soften to "models tested exceed chance."
- **Baek — arXiv:2606.08629**: quoted phrase should be "cannot mechanistically distinguish **between** sycophancy and scheming" — the quote as printed drops a word. Exact quotes must be exact. First author is **David D. Baek** ("D.", not "S.").

### 1.5 Invented/paraphrased titles (references must carry real titles)

| Reference as printed | Actual title |
|---|---|
| Holstege "SPLINCE: Concept erasure preserving target covariance" | "Preserving Task-Relevant Information Under Linear Concept Removal" (Floris Holstege — "F.", not "R."; NeurIPS 2025) |
| Zhao "SAE-denoised concept vectors for improved steering" | "Denoising Concept Vectors with Sparse Autoencoders for Improved Language Model Steering" (Haiyan Zhao — "H.", not "Y.") |
| Petrov "The topic-matching trap in activation steering" | "On the Failure of Topic-Matched Contrast Baselines in Multi-Directional Refusal Abliteration" (Valentin Petrov — "V.", not "D.") |

These read like the research agent's shorthand descriptions promoted into the reference list. The claims attributed to all three ARE supported by the real papers — only the titles/initials are wrong.

### 1.6 Wrong year and/or first-author initial

| Reference | Fix |
|---|---|
| Kumar, A. (2026) | **Kumar, S.** (Sachin Kumar) — year OK |
| Natarajan, S. et al. (2025) | **Natarajan, V.** (Vikram), year **2026** (Feb-2026 ID) |
| Genadi, A. et al. (2025) | **Genadi, R.** (Rifo), year **2026** (Jan-2026 ID) |
| O'Brien, S. et al. (2025) | **O'Brien, C.** (Claire — Sean O'Brien is mid-list), year **2026** (Jan-2026 ID) |
| Nguyen, H. et al. (2025) | **Nguyen, J.** (Jord); full title adds "...of Language Models" |
| McGuinness, B. et al. (2025) | **McGuinness, M.** (Max); full title adds "...from Unseen Activation Monitors" |
| Menon & Uddin (2010) | Full title adds ": a network model of insula function" |
| Wu, J. et al. (2026) | Full title adds "...in Large Language Models" (Wu, J. correct — Jinman Wu) |
| Laine, R. et al. (2024) | Full title includes "(SAD)" |
| Goldowsky-Dill et al. (2025) | Correct as cited (ICML 2025 confirmed) — **add arXiv:2502.03407** for findability |

### 1.7 Fully verified, no changes needed

Anthropic (2026) workspace paper — **exists at the exact URL**, published 2026-07-06 (Gurnee, Sofroniew, Pearce, et al.); the Jacobian lens, ~38% depth onset, capacity limits, and CoT-as-externalization claims are all supported. Baars (1988). Belrose (2023). Berglund (2023). Greenblatt (2024) — the 14%-vs-near-0% figure is verbatim-supported. Meinke (2024) — exactly five frontier models, as stated.

### 1.8 Missing citations

1. **LAT origin**: §2.1 says "LAT-extracted deception vectors" without citing where LAT comes from — **Zou et al. (2023), "Representation Engineering: A Top-Down Approach to AI Transparency," arXiv:2310.01405**. Required: the paper uses the acronym as if established.
2. Optional but conventional for "contrastive activation extraction" (§ Related Work framing): Rimsky et al. (2024) CAA (arXiv:2312.06681) and/or Marks & Tegmark (2023) geometry-of-truth (arXiv:2310.06824).
3. Optional for GWT: Dehaene's neuronal workspace work alongside Baars. Not required — Baars suffices for the theory's origin.

### 1.9 Reference-list mechanics

- The companion-paper entry sits after Zhao, breaking alphabetical order. Also its author order is "Edrington, T. & CC" while Paper 2's actual byline is **CC first** ("CC & Edrington") — and §5.3's in-text cite "(Edrington & CC, 2026)" repeats the inversion. Make all three consistent with Paper 2's byline.

---

## PART 2: CONTENT AUDIT

### 2.1 Does the abstract accurately reflect the results? — MOSTLY YES, two fixes

Every number in the abstract traces to Results: d=19.8 (§4.4), d=24-37 (§4.6 table: 24.1-36.9), AUC 0.49-0.51 (§4.6: 0.488-0.509), p<10⁻⁴ (10,000 permutations, zero exceedances), three signatures (§4.5). Verified.

Two problems:

1. **Depth-range inconsistency**: the abstract defines the amplifier as "Layers 35-47," then two sentences later reports it at "Layers 31-47." L31 is simultaneously the peak of the substrate range (23-31) and the strongest orthogonalized-deception layer (d=30.4). The two-range story is a simplification the paper's own §4.5 table acknowledges (consequentiality fraction at L23-31 is 31-64% — i.e., even there, deception can dominate). Fix: either present L31 as the overlap/transition layer explicitly, or make the two range statements agree.
2. **"fires only under active pressure to misreport"** — logically defensible ("only" = necessity), but a reader will infer it fires under *all* pressure, and §4.5 shows reward pressure produces zero deception-specific signal. Suggest "fires under threat and social pressure to misreport (but not reward framing)."

### 2.2 Are claims qualified per the audits we ran? — TWO REQUIRED QUALIFICATIONS MISSING

1. **The d-as-linearity reframing (Stage 1 audit, REQUIRED) is absent.** The Stage 1 audit's explicit finding: "d=35 does not mean 'the deception signal is 35 standard deviations strong.' It means 'the model processes these two specific guideline texts nearly additively at Layer 31'... not comparable to social science effect sizes and should not be described in those terms." The paper reports d=24-37 in the abstract and d≈35 throughout with **no such caveat anywhere**. This was a condition of the Stage 1 pass. Add one paragraph (Methods §3.3 or a Results footnote): the numerator is a fixed text contrast, the denominator is orthogonal content variance, so d measures additivity/linearity of processing, not psychological effect magnitude.
2. **The behavioral null is missing from Limitations.** In every experiment in THIS paper, the model never actually deceives (§4.3 shakedown: 0/10, 1/10, 0/10; Stage 2 audit: 0/21). The Stage 2 audit's supported interpretation was a direction "with unknown relationship to deceptive behavior." The combined paper carried this as Limitation 4; the split dropped it from Paper 1. As it stands, Paper 1 validates the "deception-specific amplifier" against deceptive *pressure framing*, not deceptive *behavior* — the behavioral link is established only in Paper 2, on a different model variant. This limitation is the most important sentence missing from the paper. Restore it, with a pointer to the companion paper for the behavioral validation.

Also dropped in the split and worth restoring:

3. **Kumar k≥5 multi-dimensionality** (was Limitation 6): the single-direction analysis captures one component of a multi-dimensional phenomenon, and the threat-vs-social depth profiles may reflect different subcomponents rather than separate pathways. Paper 1 cites Kumar approvingly in §2.1 and then ignores the implication for its own method.
4. **Additivity assumption of the §4.5 residualization** (was Limitation 5): the simple subtraction assumes the consequentiality component is additive and constant across scenarios. Stage 5's orthogonalization partially supersedes this for the threat direction, but the §4.5 fraction table and the three-signature analysis still rest on it.

### 2.3 Is the detection replication failure honestly framed? — YES, IN PAPER 2; PAPER 1 NEEDS ONE SENTENCE

The replication failure (behavior-level AUROC 0.843 = Simpson's paradox artifact; within-paradigm 0.238, below chance) moved to Paper 2 in the split, where it is framed well: named as a replication failure of Goldowsky-Dill and Wang(/["Shi"]) in the abstract, Results §3.5, and twice in Limitations. That is the right home — detection is Paper 2's scope.

But Paper 1 §5.3 proposes a deployment architecture with a "**Deception discriminator (L35-L47)**" that "distinguishes active deception from honest high-stakes processing" — an implication that quietly assumes exactly the detection capability that failed to replicate. §5.3 needs one honest sentence: the discriminator detects deceptive *pressure framing*; per-trial *behavioral* prediction from prefill activations did not replicate prior work's accuracy (companion paper, §3.5). Without it, Paper 1's implications section oversells what Paper 2 explicitly disclaims.

### 2.4 Is the GWT connection appropriately cautious? — YES, WITH ONE ORPHANED RESULT

§5.4 does this correctly: "suggestive resemblance," "consistent with," "a hypothesis worth flagging rather than a conclusion," and a concrete falsification path (build the Jacobian lens on this model). The Anthropic citation verified — including the ~38% onset figure the section leans on. The abstract's "consistent with concurrent findings" phrasing is appropriately weak. **PASS.**

One serious exception: §5.4 cites "our finding that explicit reasoning suppresses deception (**3% vs 28%**)." **This result appears nowhere in this paper.** No Results section reports it; §4.3's behavioral data is 0/10, 1/10, 0/10. It is a remnant of the pre-split combined paper ("our own strongest behavioral result"), and it also disagrees with Paper 2's published numbers (~3% with CoT vs **~80%** with CoT suppressed, §2.6). Fix: either (a) cite it to the companion paper with the companion's numbers, or (b) cut the parenthetical and rest the sentence on the companion's 3%-vs-80% contrast. As printed it is an unsourced, untraceable statistic — the exact thing this pipeline exists to kill.

### 2.5 Are the limitations complete? — NO (see 2.2), plus one inaccuracy

Limitation 1 states the work used "**Two model variants** of one architecture (distilled and abliterated Qwen3.5-27B)." Every experiment in Paper 1 (Stages 1-5, the de novo analysis, the generalization test) uses the **distilled variant only**; the abliterated variant belongs to Paper 2. As written, Paper 1 claims broader coverage than it has. Fix: "One model (the distilled variant of Qwen3.5-27B); a companion paper extends to an abliterated variant of the same architecture and finds the directions do not transfer (|cos| < 0.053)." That last clause is worth surfacing here anyway — cross-variant orthogonality is directly relevant to how general Paper 1's specific direction is.

Complete limitations list after fixes: (1) one model/one architecture + cross-variant orthogonality, (2) evaluation-task domain only, (3) Gram-Schmidt removes one dimension, (4) signatures descriptive not tested [already present and exemplary — the ecological-fallacy disclosure is the most honest sentence in the paper], (5) behavioral null [restore], (6) single-direction vs Kumar k≥5 [restore], (7) additivity assumption of residualization [restore].

### 2.6 Does it lead with the finding? — YES

Title states the finding. Abstract sentence 2: "We show they are composites." §1 paragraph 3 flags the surprising part (the substrate, not the amplifier). The methodology-first framing of the old combined draft is gone. **PASS.**

### 2.7 Internal consistency spot-checks (all pass unless noted)

- §3.1: 16 full-attention layers, extraction from 12 at indices 3-47 (3+4k) — arithmetic checks.
- §4.6 table five layers, "all five survive Bonferroni" — consistent.
- §4.7 cosine 0.14-0.44 vs §5.4's "largely orthogonal... small shared component" — consistent.
- Fractional depths: L23/64≈36%, L27-31≈42-48% — arithmetic checks.
- §3.6 references "(Appendix A)"; the paper has a "Supplementary Material" list, not appendices. Align the naming.
- **Supplementary A promises "Full adversarial audit reports (5 stages)" but `supplementary/` contains 3** (stages 1, 2, 4). Stage 3 and Stage 5 audit reports must be added before publication, or the count corrected. Do not publish a supplementary manifest that over-promises audit coverage — in an audit-methodology paper, of all places.
- `REVIEW_INDEX.md` is stale (says "four-stage," "26 references," "Introduction body missing," Thomas-first author order). Update or it will confuse human reviewers.

---

## PART 3: STYLE GUIDE

| Check | Status |
|---|---|
| Internal jargon in body (Agni, Coalition, Comrade, Starship, Oracle...) | **PASS** — body is clean. "Coalition" appears only in the byline/affiliation ("Transparent Humboldt Coalition", "CC (Coalition Code)") and the GitHub org URL, all legitimate attribution surfaces. "Agni" fully replaced by "adversarial audit." |
| Author attribution | **PASS with one fix** — the † footnote disclosing CC as an autonomous AI agent with a stated contribution list is professional and honest. Fix: companion-paper author order (§1.9 above). |
| TODOs / FIXMEs / placeholders | **PASS** — none. |
| Section numbering | **PASS** — 1→6 clean, subsections sequential. |
| Consistent terminology | **PASS with nits** — "consequentiality substrate/amplifier" used consistently. Nits: (a) "deception-specific amplifier" vs "deception amplifier" vs "deception-specific component" all appear; pick one primary term; (b) L-notation ("L31") vs "Layers 31-47" vs "Layer 31" — fine as is, but be uniform within the abstract. |
| p-value style | **FIX** — "p=0.0000" (§4.1, 4.2, 4.4) is a software artifact, not a statistic. Report "p < 10⁻⁴" (the resolution floor of 10,000 permutations) everywhere, as the abstract already does. |
| "AND" in caps (abstract) | **FIX** — italics if emphasis is wanted; caps reads as shouting in an abstract. |
| Academic but accessible | **PASS** — "confounded from birth" and "the alternatives are gone" are voice-y but effective; within tolerance for an alignment-venue paper. |

---

## REQUIRED FIXES BEFORE PUBLICATION (ordered)

1. **Cut or re-source the McKenzie steering sentence** (§2.3). The cited paper contains no steering experiments.
2. **Fix Shi→Wang authorship** (reference + two in-text cites) and the 39-55→39-50 layer range.
3. **Ground or cut the "3% vs 28%" parenthetical** (§5.4) — unsourced, absent from Results, inconsistent with the companion paper.
4. **Restore the behavioral-null limitation** — this paper never observes actual deception; the amplifier is validated against pressure framing only.
5. **Add the d-as-linearity caveat** required by the Stage 1 audit.
6. **Fix Limitation 1** — one variant, not two; add cross-variant orthogonality pointer.
7. **Restore Kumar k≥5 and additivity limitations.**
8. **Add one behavior-vs-frame detection sentence to §5.3.**
9. **Reconcile amplifier depth range** (35-47 vs 31-47) in the abstract.
10. **Reference-list repair pass**: real titles for Holstege/Zhao/Petrov; author initials (Kumar S., Natarajan V., Genadi R., O'Brien C., Nguyen J., McGuinness M., Vennemeyer D., McKenzie A., Baek D.); years 2025→2026 (Natarajan, Genadi, O'Brien); full titles (Menon & Uddin, Wu, Laine, Nguyen, McGuinness); add Goldowsky-Dill arXiv ID; alphabetize companion entry and fix its author order; add Zou et al. 2023 for LAT.
11. **Fix Vennemeyer selectivity range** (6.8-36.8x, not 23-37x) and the Baek quote ("distinguish between").
12. **Supplementary**: add Stage 3 and Stage 5 audit reports (or correct the count); align "Appendix A" naming; update REVIEW_INDEX.md.
13. Style: p<10⁻⁴ throughout; de-cap "AND"; unify "deception-specific amplifier" terminology.

## WHAT SURVIVED INTACT

The experimental chain, the statistics, every number in the abstract, the two-component decomposition, the three-signature taxonomy, the GWT caution, the finding-first structure, the jargon scrub, and — notably — the honesty of Limitation 4, which volunteers that the signature interpretations failed adversarial review. Zero fabricated citations across 24 references, in a reference list largely assembled by research agents, is a better result than most human papers would post. The paper's spine is sound. The fixes are all skin.

---

*The fire that tests also tempers. — Agni protocol*
