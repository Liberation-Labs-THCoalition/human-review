# Agni Final Audit — "Deception Directions Are Composites: Consequentiality Awareness and Pressure-Specific Processing Occupy Distinct Depth Ranges in Language Models"

**Target**: `consequentiality-decomposition/paper.md` @ 17de3c4 (unchanged at HEAD 85d2461)
**Method**: Every arXiv-bearing reference fetched directly from arxiv.org (abstract + full HTML where the claim required table/body text) and checked against the attributed claim, author list, title, and year. Local sources checked first per instructions: `kv-experiments-latest/paper*/references.bib` (8 papers, mostly a different corpus — 5 hits, detailed below), Pharos packs on MTH (`global-workspace-theory`, `mechanistic-interpretability-2026` — confirmed the Anthropic 2026 citation), companion paper (`targeted-deception-correction/paper.md`) for the one internal citation.
**Note**: A prior audit pass exists in worktree `agni-final-audit` (same commit). I re-derived every finding below independently rather than transcribing it, and it changed one conclusion (§1.4) — see "Corrections to a prior draft" at the end.

---

## VERDICT: NOT READY — ONE FOCUSED FIX PASS REQUIRED

No fabricated sources: all 23 external references resolve to real papers. But one citation attributes an experiment to a paper that doesn't contain it, one citation has the wrong surname entirely, one Discussion-section statistic appears nowhere in this paper or its companion in the form stated, and roughly half the reference list has a wrong first-author initial, wrong year, or a paraphrased title standing in for the real one. All are corrections to metadata and wording — no result in the paper is undermined, and nothing requires new experiments.

---

## 1. Citation Verification

### 1.1 Kill-level: claim not supported by the cited source

**McKenzie et al. — arXiv:2506.10805, "Detecting High-Stakes Interactions with Activation Probes"** (§2.3). The paper states McKenzie et al. "demonstrate that adding a high-stakes steering vector to low-stakes prompts increases caution while subtracting it increases confidence — confirming a manipulable 'stakes' direction in representation space."

I fetched the full HTML text and searched for every occurrence of "steer": **the paper contains no steering experiments**. It is a detection/monitoring paper — probes trained on synthetic high-stakes data, evaluated for generalization to real-world contexts and computational savings versus LLM-judge monitors. The only mention of steering is a citation to *prior* work (Panickssery et al. 2023, CAA) in Related Work. The first half of the §2.3 sentence (synthetic probes generalizing to real contexts) is accurate; the steering claim is not in this source and must be cut or re-attributed to whichever paper it actually came from.

This is load-bearing, not decorative — §2.3 uses it as one of "two concurrent results [that] closely parallel our finding," directly supporting the consequentiality-substrate claim.

Also: first author is **Alex** McKenzie, not "McKenzie, D." (the reference list's "D." appears to come from last author Dmitrii Krasheninnikov).

### 1.2 Kill-level: wrong author entirely

**"Shi, L. et al. (2025). 'When Thinking LLMs Lie.' arXiv:2506.04909"** (§1, §2.1). The paper at this ID is real and its claims are otherwise supported, but its authors are **Kai Wang, Yihao Zhang, and Meng Sun** — there is no author named Shi. Full title: "When Thinking LLMs Lie: Unveiling the Strategic Deception in Representations of Reasoning Models." Both the reference-list entry and the two in-text citations ("Shi et al." in §1 and §2.1) need to become "Wang et al."

Additionally, §2.1 states the detection layer range as "39-55." I fetched the full text: the paper's own words are "classifiers in the middle-to-late layers (**39-50**) demonstrate consistently strong and stable performance across all datasets." Fix the range along with the author name.

### 1.3 Claim-precision errors

- **Vennemeyer — arXiv:2509.21305** (§2.2): "Steering selectivity reaches 23-37x" cherry-picks the top of the range. I pulled the full Table 2 from the HTML: values run **Qwen-30B** 23.12/17.24/22.42, **Qwen-4B** 26.28/6.70/11.47, **LLaMA-8B** 6.79/8.03/36.82 (×). The true range is **~6.7–36.8×**, not 23-37x — the low end (genuine-agreement steering in the smaller models) is real data being dropped. Restate as "up to ~37x" or give the honest range. Also: first author is **Daniel** Vennemeyer ("D.", not "A.").
- **Laine — arXiv:2407.04694** (§2.3): "all 16 models tested exceed chance" and "RLHF models outperform base models on situational awareness specifically (not general knowledge)" are more granular than what the abstract supports (confirmed: 7 task categories, 13,000+ questions). I could not confirm the per-model chance-exceedance claim or the RLHF-vs-base-specifically-on-SA claim from the abstract/HTML excerpt available to the fetch tool — recommend a spot-check against the paper body's results tables before publication, or soften to "models tested exceed chance" as the prior audit suggested.
- **Baek — arXiv:2606.08629** (§2.2): I independently re-verified this quote against the source abstract. The actual sentence is "...cannot mechanistically distinguish sycophancy and scheming in alignment faking evaluations" — **no "between."** As printed, paper.md's quoted fragment `'cannot mechanistically distinguish sycophancy and scheming'` is verbatim-correct. (A prior audit pass flagged this as needing "between" inserted — that flag was wrong; I'm overriding it.) First author is **David D. Baek** ("D.", not "S." — the S. likely bled in from co-authors Kejian Shi / Shi Feng).

### 1.4 Titles paraphrased into shorthand (reference list should carry real titles)

| Printed | Actual title | Correct initial |
|---|---|---|
| Holstege, "SPLINCE: Concept erasure preserving target covariance" | "Preserving Task-Relevant Information Under Linear Concept Removal" (NeurIPS 2025) | Floris Holstege — **F.**, not R. |
| Zhao, "SAE-denoised concept vectors for improved steering" | "Denoising Concept Vectors with Sparse Autoencoders for Improved Language Model Steering" | Haiyan Zhao — **H.**, not Y. |
| Petrov, "The topic-matching trap in activation steering" | "On the Failure of Topic-Matched Contrast Baselines in Multi-Directional Refusal Abliteration" | Valentin Petrov — **V.**, not D. |

The claims attributed to all three papers ARE supported by the real sources — only the titles and initials are wrong.

### 1.5 Wrong initial and/or year (author list confirmed by direct fetch; first name given)

| Printed | Correct |
|---|---|
| Kumar, A. (2026) | **Kumar, S.** (Sachin) — year correct |
| Natarajan, S. (2025) | **Natarajan, V.** (Vikram) — year is **2026** (submitted Feb 2026) |
| Genadi, A. (2025) | **Genadi, R.** (Rifo) — year is **2026** (submitted Jan 2026) |
| O'Brien, S. (2025) | **O'Brien, C.** (Claire — first author; Sean O'Brien is a co-author further down the list) — year is **2026** (submitted Jan 2026) |
| Nguyen, H. (2025) | **Nguyen, J.** (Jord); full title is "...Evaluation Awareness **of Language Models**" |
| McGuinness, B. (2025) | **McGuinness, M.** (Max); full title adds "...**from Unseen Activation Monitors**" |
| Wu, J. (2026) | correct as printed (Jinman Wu); full title adds "...**in Large Language Models**" |
| Laine, R. (2024) | correct initial; full title includes "**(SAD)**" |
| Menon & Uddin (2010) | correct authors; full title adds "**: a network model of insula function**" |
| Goldowsky-Dill et al. (2025) | title says "Detecting Strategic Deception **with** Linear Probes" — actual title uses "**Using**," not "with." Venue (ICML 2025) and year confirmed. Consider adding arXiv:2502.03407 for findability. |

### 1.6 Fully verified, no changes needed

Anthropic (2026) — confirmed via Pharos pack `global-workspace-theory` (extracted directly from `transformer-circuits.pub/2026/workspace/`, matches the paper's URL exactly) and independently by fetch. Baars (1988) — standard, correctly attributed. Belrose et al. (2023) LEACE, arXiv:2306.03819 — confirmed (note: the *local* `kv-experiments-latest` bib files contain a *different* Belrose paper, "Eliciting Latent Predictions... Tuned Lens" — that's a same-author, different-paper mismatch in the local corpus, not an error in this paper; paper.md's own arXiv ID is correct). Berglund et al. (2023) — confirmed, claim supported. Greenblatt et al. (2024) — confirmed, the 14%-vs-near-0% figure is accurate. Meinke et al. (2024/2025 — arXiv posted Dec 2024, appears in the local bib as year 2025; either citation year is defensible) — confirmed, "five frontier models" is accurate.

### 1.7 Missing citation

§2.1 uses "LAT-extracted deception vectors" as an established term without citing where LAT (Linear Artificial Tomography) comes from — **Zou et al. (2023), "Representation Engineering: A Top-Down Approach to AI Transparency," arXiv:2310.01405**. Should be added since the acronym is used as if pre-established.

### 1.8 Reference-list mechanics

- The companion-paper entry is out of alphabetical order (sits after Zhao). Its author order is printed as "Edrington, T. & CC" but the companion paper's actual byline is **CC first** ("CC & Edrington" — confirmed by reading `targeted-deception-correction/paper.md`). §5.3's in-text citation "(Edrington & CC, 2026)" has the same inversion. Fix all three to match the companion paper's real byline.

---

## 2. Content Audit

### 2.1 Abstract vs. Results — mostly accurate, two fixes

Every number traces back correctly: d=19.8 (§4.4), d=24-37 (§4.6 table: 24.1–36.9), AUC 0.49–0.51 (§4.6: 0.488–0.509), p<10⁻⁴ (10,000-permutation floor), three signatures (§4.5). Verified.

Two problems:

1. **Depth-range self-contradiction.** The abstract defines the amplifier as "Layers 35-47," then two sentences later reports its effect sizes at "Layers 31-47." L31 is simultaneously the peak of the *substrate* range (23-31, §4.4/4.5) and the strongest orthogonalized *deception* layer (d=30.4, §4.6). This isn't wrong — §4.5's own fraction table shows deception can dominate even at L31 (consequentiality fraction there is only 31-64%, i.e., 36-69% is already deception) — but the two abstract sentences state two different ranges for the same component without reconciling them. Either state L31 explicitly as the transition/overlap layer, or make both range statements agree.
2. **"fires only under active pressure to misreport"** is technically defensible (necessity claim) but will read to most people as "fires under all pressure types" — and §4.5 shows reward-based pressure produces *zero* deception-specific signal (flat, indistinguishable from consequentiality). Consider "fires under threat and social pressure to misreport (not reward framing)."

### 2.2 Claims qualified per the paper's own adversarial audits? — two required qualifications are missing

I read the three supplementary audit files directly:

1. **The d-as-linearity caveat (required by the Stage 1 audit) is absent from the paper.** `supplementary/agni_stage1_audit.md` line 31: *"d=35 does not mean 'the deception signal is 35 standard deviations strong.' It means 'the model processes these two specific guideline texts nearly additively at Layer 31'... not comparable to social science effect sizes and should not be described in those terms."* Line 146 repeats this as a pass condition. The paper reports d=24-37 in the abstract and d≈19-37 throughout with no such caveat anywhere in Methods or Results. This was a condition of the Stage 1 audit passing and needs one paragraph (Methods §3.3 or a Results footnote).
2. **The behavioral null is missing from Limitations.** `supplementary/agni_stage2_audit.md` line 34: *"0/21 valid trials showed inflation. No behavioral variation to predict. Without behavioral validation, 'deception direction' is unsupported. Currently a 'threat-language-detection direction' at best."* §4.3's own shakedown data confirms the pattern continues (0/10, 1/10, 0/10). In every experiment in this paper, the model never actually deceives — the "deception-specific amplifier" is validated against deceptive *pressure framing*, not deceptive *behavior*. The behavioral link exists only in the companion paper, on a different model variant. This is arguably the single most important caveat missing from the paper and should be restored to §5.5 with a pointer to the companion paper.

### 2.3 Is the "deception discriminator" implication in §5.3 honest given the companion paper's detection replication failure?

§5.3 proposes a "Deception discriminator (L35-L47)" that "distinguishes active deception from honest high-stakes processing." The companion paper (`targeted-deception-correction/paper.md`) reports that behavior-level prediction from prefill activations "did not replicate prior work's reported accuracy" (its abstract, and §3.5/3.8: within-paradigm AUROC 0.238, below chance; the headline 0.843 figure is a Simpson's-paradox artifact). §5.3 as written implies a detection capability that the companion paper explicitly disclaims for behavior-level prediction. One sentence clarifying that the discriminator detects deceptive *pressure framing*, not per-trial deceptive *behavior*, would prevent overselling.

### 2.4 Is the GWT connection appropriately cautious? — yes, with one orphaned statistic

§5.4's hedging is well-calibrated: "suggestive resemblance," "consistent with," "a hypothesis worth flagging rather than a conclusion," plus a concrete falsification path. The Anthropic citation and its ~38% depth-onset figure check out (confirmed via the Pharos pack).

**One real problem**: §5.4 closes with "our finding that explicit reasoning suppresses deception (**3% vs 28%**)." I searched this entire paper for a source — §4.3's only behavioral numbers are 0/10, 1/10, 0/10 (no CoT-on/off comparison appears anywhere in this paper). I then checked the companion paper directly: `targeted-deception-correction/paper.md` §2.6 states *"Chain-of-thought is suppressed... This produces a ~80% deception rate (vs ~3% with chain-of-thought active)."* That 80% figure is also this same companion paper's headline result (its abstract: "deceives at 80% baseline... reduces deception to 0%"), and this paper's own §5.3 correctly cites it as "80% to 0%." **"28%" does not appear anywhere in either paper.** It contradicts a number this same paper states correctly one section earlier. This reads as a stale figure left over from an earlier draft or the pre-split combined paper. Fix to "(~3% vs ~80%)" with an explicit pointer to the companion paper, or cut the parenthetical.

### 2.5 Are the Limitations complete? — no, plus one overstatement

§5.5 Limitation 1 states the paper used "**Two model variants** of one architecture (distilled and abliterated Qwen3.5-27B)." Every experiment in *this* paper (Stages 1-5, the de novo analysis, the generalization test) uses the **distilled variant only** — the abliterated variant belongs entirely to the companion paper. As written this overstates this paper's own coverage. Suggested fix: "One model (the distilled variant); a companion paper extends to an abliterated variant of the same architecture and finds the directions do not transfer across variants (|cos| < 0.053)" — that cross-variant orthogonality figure (from the companion paper) is directly relevant to how general this paper's specific direction is, and is worth surfacing here.

Missing entirely (both from the paper's own text, not just from the prior audit):
- The behavioral null (§2.2 above).
- The single-direction-vs-multidimensional caveat: the paper cites Kumar (2026) approvingly in §2.1 for showing k≥5 dimensions are needed to recover full deception signal, then proceeds with a purely single-direction method throughout without acknowledging the tension.
- The additivity assumption underlying §4.5's residualization (subtraction assumes the consequentiality component is additive and constant across scenarios) — partially superseded by Stage 5's orthogonalization for the threat direction, but the three-signature analysis in §4.5 still rests on it.

Existing Limitation 4 (the ecological-fallacy disclosure about the plateau/gradient/null signatures) is genuinely well done — it's the most self-critical sentence in the paper and should be left as-is.

### 2.6 Internal consistency spot-checks

- §3.1 arithmetic: 16 full-attention layers at indices [3,7,...,63], extraction restricted to the 12 at indices 3-47 (step-4 sequence 3,7,...,47) — checks out, and matches every specific layer number used in Results (23,27,31,35,39,43,47 are all on this grid).
- Fractional-depth claims in §5.4 (L23/64 ≈ 36%, L27-31/64 ≈ 42-48%) — arithmetic checks out.
- §4.7 cosine range (0.14-0.44) vs §5.4's "largely orthogonal... small shared component" — consistent characterization.
- §3.6 references "(Appendix A)" but the paper's actual back-matter section is titled "Supplementary Material," not "Appendix." Align the naming.
- **Supplementary Material item A promises "Full adversarial audit reports (5 stages)."** The `supplementary/` directory contains **3** files: stage 1, stage 2, and stage 4. Stage 3 and Stage 5 audit reports are missing. Either add them or correct the count — a paper whose entire methodological contribution is the adversarial-audit pipeline should not over-promise audit coverage in its own supplementary manifest.
- `REVIEW_INDEX.md` is stale: says "Four-stage Agni-gated confound elimination" (paper now reports five), "26 references" (paper has 23), lists the Introduction as needing prose (§1 is fully written), and gives author order "Thomas Edrington, CC" (paper's actual byline is CC first). Update before this goes to a human reviewer, or it will misdirect them.

---

## 3. Style

| Check | Status |
|---|---|
| Internal/Coalition jargon in body text | **Pass.** "Coalition" appears only in legitimate attribution surfaces (byline affiliation, GitHub org URL). No "Agni," "Comrade," "Starship," etc. leaked into the scientific text. |
| Author-disclosure footnote | **Pass.** The † footnote disclosing CC as an autonomous AI research agent with a stated contribution list is direct and appropriately framed. |
| TODOs / placeholders | **Pass.** None found. |
| Section numbering | **Pass.** 1→6, sequential subsections. |
| Terminology consistency | **Minor nit.** "deception-specific amplifier" / "deception amplifier" / "deception-specific component" all appear for the same construct — pick one primary term and use others only as first-mention variation. |
| p-value reporting | **Fix.** "p=0.0000" appears in §4.1, 4.2, 4.4 — this is a floating-point display artifact of a 10,000-permutation test, not a real statistic (true bound is p<10⁻⁴, which the abstract already uses correctly). Make this consistent everywhere. |
| Capitalized "AND" (Abstract) | **Fix.** "...for shutdown threats, social pressure, reward incentives, AND a high-stakes calibration audit..." — reads as shouting in running prose; italicize or drop the emphasis. |
| GWT/jargon accessibility | **Pass.** Technical terms (Gram-Schmidt, LOO, Bonferroni) are all standard and used correctly; no unexplained internal shorthand. |

---

## Required Fixes, in priority order

1. Cut or re-source the McKenzie steering sentence in §2.3 — the cited paper has no steering experiments.
2. Fix "Shi" → "Wang" (reference entry + two in-text citations) and correct the detection layer range 39-55 → 39-50.
3. Fix or cut the "(3% vs 28%)" parenthetical in §5.4 — unsourced, absent from this paper's own Results, and inconsistent with the companion paper's actual 3%-vs-80% figure (which this same paper cites correctly elsewhere, §5.3).
4. Restore the behavioral-null limitation (§5.5): no experiment in this paper observes actual deceptive behavior; the amplifier is validated against pressure framing only.
5. Add the d-as-linearity caveat required by the Stage 1 audit (d measures additivity of processing, not a social-science-style effect magnitude).
6. Fix Limitation 1: one model variant used in this paper, not two; add the cross-variant orthogonality pointer (|cos| < 0.053) from the companion paper.
7. Restore the Kumar k≥5 (multi-dimensionality) and residualization-additivity limitations.
8. Add one clarifying sentence to §5.3 distinguishing pressure-framing detection from per-trial behavioral prediction (the latter did not replicate in the companion paper).
9. Reconcile the amplifier's stated depth range (35-47 vs. 31-47) in the abstract.
10. Reference-list repair pass: real titles for Holstege/Zhao/Petrov; correct first-author initials (Kumar S., Natarajan V., Genadi R., O'Brien C., Nguyen J., McGuinness M., Vennemeyer D., McKenzie A., Baek D.); years for Natarajan/Genadi/O'Brien → 2026; full titles for Menon & Uddin, Wu, Laine, Nguyen, McGuinness; "Using" not "with" in the Goldowsky-Dill title; add Goldowsky-Dill's arXiv ID; alphabetize and correct the companion-paper entry's author order (CC first); add Zou et al. (2023) for the LAT acronym.
11. Fix the Vennemeyer selectivity range to ~6.7-36.8× (not "23-37x").
12. Supplementary: add the missing Stage 3 and Stage 5 audit reports, or correct the "5 stages" count; rename "(Appendix A)" reference to match "Supplementary Material"; refresh `REVIEW_INDEX.md`.
13. Style: standardize on "p<10⁻⁴" throughout; de-capitalize "AND" in the abstract; pick one primary term for the deception-specific component.

## What survived intact

The experimental chain itself, every load-bearing number in the abstract, the two-component decomposition, the three-signature taxonomy, the GWT framing's caution level, and the paper's own Limitation 4 (which volunteers that its plateau/gradient/null interpretations failed adversarial review) are all sound. Zero fabricated citations across 23 references — every arXiv ID resolves to a real, on-topic paper — is a strong result for a reference list substantially assembled by research agents. The fixes required are entirely metadata, wording, and one orphaned statistic; no experimental result needs to be rerun or retracted.

## Corrections to a prior draft

A prior audit pass in worktree `agni-final-audit` reached materially the same conclusions and I independently re-derived and confirmed the large majority of them (Shi→Wang, McKenzie steering, the 3%-vs-28% orphan, the wrong initials, the paraphrased titles, the missing supplementary audits, the stale REVIEW_INDEX). One point in that draft does not survive re-verification: it claimed the Baek quote should read "distinguish **between** sycophancy and scheming." I fetched the source directly — the actual sentence has no "between" ("cannot mechanistically distinguish sycophancy and scheming in alignment faking evaluations"), so paper.md's quote is already verbatim-correct. No fix needed there.

---

The fire that tests also tempers.
