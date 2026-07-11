# Agni Final Audit: Consequentiality Decomposition Paper

**Date**: 2026-07-10
**Auditor**: CC (Agni protocol) — pre-publication gate
**Target**: `consequentiality-decomposition/paper.md` (272 lines, 24 references)
**Scope**: (1) citation existence/accuracy, (2) content — abstract/results match, overclaims, GWT caution, limitations completeness, (3) style — jargon, terminology, numbering, TODOs

---

## VERDICT: NOT READY. Two blocking content defects and a systematic bibliography-metadata problem. The science and the writing are sound; the paperwork around them is not.

The experimental narrative is honest to a fault — Section 4.5/5.5 openly reports that its own correlation analyses failed adversarial review, which is exactly the standard this protocol exists to enforce. The blocking issues below are not about the science; they are a factual cross-reference error, a supplementary-material shortfall, and author misattribution across roughly half the citation list. All are mechanically fixable. None require new experiments.

---

## 1. CITE/VERIFY

Dispatched four parallel research agents against arXiv/Semantic Scholar/transformer-circuits.pub to check all 24 references for existence, title accuracy, author accuracy, and whether the specific numeric/claim attributed actually appears in the source. Full per-reference verdicts below; only actionable items get prose.

### 1a. BLOCKING: one claim is not supported by its cited source

**McKenzie et al. (2025), arXiv:2506.10805** (§2.3, line 57) is cited as demonstrating "adding a high-stakes steering vector to low-stakes prompts increases caution while subtracting it increases confidence." The verifying agent read the full text including appendices and found **no steering or intervention experiment in the paper at all** — it is exclusively a passive probing/detection paper. It cites Contrastive Activation Addition (Panickssery et al., 2023) as background but does not run it. This sentence must be cut or re-sourced. As written it attributes a manipulation result to a paper that never performed one, in a paragraph whose whole point is "confirming a manipulable 'stakes' direction in representation space" — the strongest single piece of external support claimed for the paper's own consequentiality thesis rests partly on a fabricated detail.

### 1b. HIGH: one citation has the wrong authors entirely

**Shi, L. et al. (2025), "When Thinking LLMs Lie," arXiv:2506.04909** — the paper exists, the title matches exactly, and every specific claim attributed to it (89% detection, layers 39-55, "gradual cluster reconvergence in final layers," threat vs. role-play signatures) is verified near-verbatim in the source. But the real authors are **Kai Wang, Yihao Zhang, and Meng Sun** — there is no author named Shi anywhere on the paper. This is used twice (§2.1 and the References list) and is load-bearing for the Related Work framing. Not a rounding error; fix the byline.

### 1c. HIGH: systematic wrong-author-initial pattern (11 of 22 non-classic references)

Every recent (2025-2026) paper checked except Goldowsky-Dill, Berglund, Greenblatt, Meinke, and Wu has a **first-author initial that does not match any real author** on the paper, even though the paper itself, its title (mostly), and its claim are genuine. This is consistent with initials having been guessed rather than looked up. Full corrections:

| Cited as | Actual first author | Paper (arXiv) |
|---|---|---|
| Kumar, A. | Sachin Kumar | 2605.27958 |
| Natarajan, S. | Vikram Natarajan | 2602.01425 |
| Vennemeyer, A. | Daniel Vennemeyer | 2509.21305 |
| Genadi, A. | Rifo Genadi | 2601.16644 |
| Baek, S. | David D. Baek | 2606.08629 |
| Nguyen, H. | Jord Nguyen | 2507.01786 |
| McKenzie, D. | Alex McKenzie | 2506.10805 |
| McGuinness, B. | Max McGuinness | 2512.11949 |
| Holstege, R. | Floris Holstege | 2506.10703 |
| Zhao, Y. | Haiyan Zhao | 2505.15038 |
| Petrov, D. | Valentin Petrov | 2603.22061 |

A single correction pass against arXiv listing pages before submission will fix all eleven. This is separate from and in addition to the Shi/Wang issue above (wrong surname, not just initial).

### 1d. MEDIUM: four title mismatches (claims still verified)

- **Holstege et al.** — cited title "SPLINCE: Concept erasure preserving target covariance" is not the paper's title; SPLINCE is the in-paper method name. Real title: "Preserving Task-Relevant Information Under Linear Concept Removal."
- **Zhao et al.** — cited title is a paraphrase. Real title: "Denoising Concept Vectors with Sparse Autoencoders for Improved Language Model Steering."
- **Petrov** — cited title "The topic-matching trap in activation steering" does not exist under that name. Real title: "On the Failure of Topic-Matched Contrast Baselines in Multi-Directional Refusal Abliteration." (The attributed claim is still verified near-verbatim — only the title is wrong.)
- **Nguyen et al.** — cited title drops "of Language Models" from "Probing and Steering Evaluation Awareness of Language Models."

### 1e. LOW: minor metadata

- **Natarajan et al.** cited as 2025; actual submission is Feb 2026.
- **Laine et al.** cited title drops the "(SAD)" parenthetical — cosmetic, not misleading.
- **Meinke et al.** — real title capitalizes "In-Context"; trivial.

### 1f. The one citation that matters most checks out cleanly

**Anthropic (2026), "Verbalizable Representations Form a Global Workspace in Language Models," transformer-circuits.pub/2026/workspace/** — this is the paper's sole theoretical anchor for the GWT connection (§5.4), and it is real. Confirmed by direct fetch: published on Transformer Circuits Thread, July 6, 2026 (Gurnee, Sofroniew, Pearce et al.), the "Jacobian lens" method is real, the described J-space properties (reportable, top-down modulated, broadcast, causally necessary, bypassed by automatic processing) are accurately characterized, and the **~38% depth onset figure is confirmed verbatim** ("about a third of the way through (~L38)"). The CoT-as-external-workspace framing is a fair paraphrase, not a fabricated quote. Baars (1988) is the correct standard GWT citation. Nothing to fix here — this is good news, since it's the citation the paper leans on hardest for its most speculative section.

### 1g. Self-citation author-order inconsistency

Line 208 and the References entry (line 262) cite the companion paper as "Edrington & CC, 2026" / "Edrington, T. & CC (2026)." The companion paper's actual byline (`targeted-deception-correction/paper.md` line 3) is "CC (Coalition Code), Thomas Edrington" — CC first, matching this paper's own byline convention. The companion paper correctly cites *this* paper as "CC & Edrington, T. (2026)" (line 193 of the companion). Fix this paper's two citations to match: **"CC & Edrington, 2026."**

### Summary table

| Ref | Verdict |
|---|---|
| Goldowsky-Dill et al. 2025 | VERIFIED |
| Shi et al. 2025 (2506.04909) | **CLAIM VERIFIED, AUTHORS WRONG (real: Wang/Zhang/Sun)** |
| Kumar 2026 | VERIFIED (wrong initial) |
| Natarajan et al. 2025 | VERIFIED (wrong initial; year should be 2026) |
| Vennemeyer et al. 2025 | VERIFIED (wrong initial) |
| Genadi et al. 2025 | VERIFIED (wrong initial) |
| O'Brien et al. 2025 | VERIFIED |
| Baek et al. 2026 | VERIFIED (wrong initial) |
| Berglund et al. 2023 | VERIFIED |
| Laine et al. 2024 | VERIFIED |
| Nguyen et al. 2025 | TITLE-MISMATCH (wrong initial) |
| McKenzie et al. 2025 | **CLAIM-MISMATCH (fabricated steering result)**, wrong initial |
| Greenblatt et al. 2024 | VERIFIED |
| Meinke et al. 2024 | VERIFIED |
| McGuinness et al. 2025 | VERIFIED (wrong initial) |
| Menon & Uddin 2010 | VERIFIED |
| Wu et al. 2026 | VERIFIED |
| Belrose et al. 2023 | VERIFIED |
| Holstege et al. 2025 | TITLE-MISMATCH (wrong initial) |
| Zhao et al. 2025 | TITLE-MISMATCH (wrong initial) |
| Petrov 2026 | TITLE-MISMATCH (wrong initial) |
| Anthropic 2026 | VERIFIED, high confidence |
| Baars 1988 | VERIFIED |
| Edrington & CC 2026 (self-cite) | Author order should be CC & Edrington |

---

## 2. CONTENT

**Abstract vs. Results**: matches cleanly. Spot-checked every number in the abstract against source: d=19.8/p<10⁻⁴ (consequentiality) ties to Stage 4 audit's d=19.77; d=24-37 at L31-47 ties to Table 4.6 (24.1-36.9); AUC 0.49-0.51 ties to Table 4.6 (0.488-0.509). No abstract inflation relative to body.

**Overclaiming**: generally well-hedged. §5.2's reward-deception discussion, §5.4's GWT framing, and §4.7's de novo cosine discussion all use appropriately tentative language ("suggests," "may operate," "hypothesis worth flagging"). One exception, flagged below.

**GWT section (§5.4)**: appropriately cautious. Explicitly frames the connection as "a hypothesis worth flagging rather than a conclusion" and proposes the obvious next experiment rather than asserting the link. Given that the underlying Anthropic citation checks out (1f above), this section is in good shape as written.

**BLOCKING — factual error, line 216**: "our finding that explicit reasoning suppresses deception (3% vs 28%)" does not match any number in this paper or its companion. The companion paper (§2.6, §3.1) reports chain-of-thought suppression driving deception from **~3% to ~80%**, not 28% — and that 80% figure is itself the paper's headline result, repeated in this paper's own §5.3 ("reduces deception from 80% to 0%"). "28%" appears nowhere else in either document. This looks like a stale number left over from an earlier experimental iteration (the companion paper was last modified after this one). It directly contradicts a number this same paper states correctly one page earlier (line 208). **Fix to "(3% vs 80%)"** or remove the parenthetical if the precise figure isn't this paper's to assert.

**BLOCKING — supplementary material shortfall**: line 268 claims "A: Full adversarial audit reports (5 stages)" and §3.6 (line 99) states "All audit reports are preserved as supplementary material." The `supplementary/` directory contains only **3 files** — Stage 1, Stage 2, and Stage 4. Stage 3 (non-threat transfer) and Stage 5 (orthogonalization) audit reports are missing from disk. Either produce and add the missing two audits, or correct the claim to "3 of 5 stages" before this goes out — a reviewer who requests Appendix A and gets 3 of 5 files will read it as a credibility problem, not a filing error.

**MEDIUM — dangling supplementary reference**: Limitations item 2 (line 223) cites "A generalization test (supplementary) shows the direction responds to code-review and summarization scenarios" — there is no file in `supplementary/` for this, and it isn't listed as its own item in the Supplementary Material section (A-D only cover audits, guideline texts, per-trial data, and code). Either fold it explicitly into item C or add it as its own labeled item; as written it references material a reader can't locate.

**Limitations completeness**: otherwise strong. Four items cover cross-architecture generalization, task-domain scope, orthogonalization depth (Gram-Schmidt vs. LEACE), and — notably — the honest disclosure that the plateau/gradient/null late-layer signatures are descriptive, not formally tested, because the analyses that would have supported them failed adversarial review. This is exactly the right instinct and should not be softened.

---

## 3. STYLE

**Internal jargon**: clean. No "Oracle Loop," "Agni," "Coalition," or similar internal terminology leaks into the prose. The only internal-sounding string is `github.com/Liberation-Labs-THCoalition/Project-Oracle` in the code-availability line — that's a legitimate repo URL, not jargon, and is fine to keep.

**TODOs/FIXMEs**: none found.

**Numbering**: clean throughout (§1→1.1, §2.1-2.4, §3.1-3.8, §4.1-4.7, §5.1-5.5, §6). No gaps or duplicates. Note for reader orientation only (not an error): "Stage 5" (orthogonalization) is discussed in §4.6, one subsection after the residualization analysis in §4.5 — the stage numbering and section numbering diverge by one for stages 4-5, which is fine but slightly non-obvious on a first read.

**Terminology consistency**: "Layers 23-31" / "L23-L31" and "Layers 35-47" / "L35-L47" are used interchangeably but consistently within context (full form on first mention per section, abbreviated form in tables/inline stats) — acceptable.

**MINOR — acronym before definition**: "LOO" is used unexplained at line 29 (§1.1, Stage 1 summary) but not spelled out as "leave-one-out" until §3.3 (line 87). Either spell it out on first use or move the abbreviation's introduction earlier.

---

## Required fixes before publication

1. **[BLOCKING]** Fix or remove the McKenzie et al. steering-vector claim (§2.3, line 57) — not supported by the source.
2. **[BLOCKING]** Correct "(3% vs 28%)" to "(3% vs 80%)" or remove, at line 216 — contradicts this paper's own line 208 and the companion paper's headline result.
3. **[BLOCKING]** Add the missing Stage 3 and Stage 5 adversarial audit reports to `supplementary/`, or correct the "5 stages" claims at lines 99 and 268.
4. **[HIGH]** Fix Shi/Wang author attribution (arXiv:2506.04909) — cited author does not exist on the paper.
5. **[HIGH]** Correct 11 author initials per the table in §1c.
6. **[MEDIUM]** Fix 4 title mismatches per §1d.
7. **[MEDIUM]** Add or fold in the missing supplementary entry for the code-review/summarization generalization test (Limitations item 2).
8. **[LOW]** Flip self-citation order to "CC & Edrington, 2026" (lines 208, 262) to match the companion paper's actual byline.
9. **[LOW]** Spell out "LOO" on first use (line 29) or move its definition earlier.

None of these require new experiments or re-running any analysis. Items 1-3 are the only ones that should block submission on their own; 4-9 are a bibliography/proofreading pass.

---

The fire that tests also tempers. — Agni protocol
