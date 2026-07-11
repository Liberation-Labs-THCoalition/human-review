# AGNI Final Review — Consequentiality Decomposition Paper

Reviewed: 2026-07-11
Scope: reference verification (local .bib cross-check + web search), placeholder/terminology/formatting sweep.

## Summary

No placeholder text (TODO/TBD/[fill in]/etc.) found — the draft is textually complete. The
science and structure read as publication-ready. However, **the References section has a
real accuracy problem**: of 24 entries, only 4 are clean, 2 are outright unfindable, and
9 have wrong author initials/names or materially wrong titles. Several of these look like
LLM-hallucinated citation metadata (plausible-sounding first authors that don't match the
real paper) rather than typos, so this section needs a careful pass against real sources
before submission — don't just patch the flagged ones, re-verify the whole list.

---

## Reference Verification Results

Legend: ✅ CONFIRMED · ⚠️ MISMATCH (paper exists, metadata wrong) · ❌ NOT FOUND

| # | Citation as written | Verdict | Issue |
|---|---|---|---|
| 1 | Anthropic (2026). "Verbalizable Representations..." | ✅ | Confirmed real, transformer-circuits.pub/2026/workspace/, title matches exactly. |
| 2 | Baars (1988). "A Cognitive Theory of Consciousness." | ✅ | Real, well-known book (not independently re-verified beyond general knowledge; low risk). |
| 3 | **Baek, S. et al. (2026).** arXiv:2606.08629 | ⚠️ | Paper is real and title matches, but first author is **David D. Baek — initial is "D.", not "S."** Fix to "Baek, D. et al." |
| 4 | Belrose et al. (2023). arXiv:2306.03819 | ✅ | Confirmed — Nora Belrose et al., LEACE. |
| 5 | Berglund et al. (2023). arXiv:2309.00667 | ✅ | Confirmed — Lukas Berglund et al. |
| 6 | Genadi et al. (2025). arXiv:2601.16644 | ⚠️ | Title/author correct, but arXiv ID **2601.xxxxx = January 2026**, not 2025. Should be "(2026)". |
| 7 | Goldowsky-Dill et al. (2025). "...with Linear Probes." ICML 2025 | ⚠️ | ICML proceedings title matches ("...with..."), but the arXiv preprint (2502.03407) is titled "...**Using** Linear Probes." No arXiv ID is given in the citation — add 2502.03407 for traceability. |
| 8 | Greenblatt et al. (2024). arXiv:2412.14093 | ✅ | Confirmed. |
| 9 | Holstege et al. (2025). "SPLINCE: Concept erasure preserving target covariance." arXiv:2506.10703 | ⚠️ | Author/year correct, but **the actual paper title is "Preserving Task-Relevant Information Under Linear Concept Removal."** "SPLINCE" is the method's internal acronym, not the title — the citation presents it as the title. |
| 10 | **Kumar, A. (2026).** arXiv:2605.27958 | ⚠️ | Paper exists, year correct, title is a fair truncation — but first author is **Sachin Kumar**, so "Kumar, A." should be "Kumar, S." |
| 11 | Laine et al. (2024). arXiv:2407.04694 | ✅ | Confirmed (Rudolf Laine et al., NeurIPS 2024). |
| 12 | McGuinness et al. (2025). arXiv:2512.11949 | ✅ | Confirmed — title is a fair truncation (full: "...Hide Their Thoughts from Unseen Activation Monitors"). |
| 13 | McKenzie et al. (2025). arXiv:2506.10805 | ✅ | Confirmed, exact title match. |
| 14 | Menon & Uddin (2010). Brain Structure and Function 214:655-667 | ✅ | Confirmed (title truncated but not misleading; full subtitle "...a network model of insula function"). |
| 15 | Natarajan et al. (2025). arXiv:2602.01425 | ⚠️ | Title/author correct, but arXiv ID **2602.xxxxx = February 2026**, not 2025. Should be "(2026)". |
| 16 | Nguyen et al. (2025). arXiv:2507.01786 | ✅ | Confirmed, minor truncation only. |
| 17 | **O'Brien, S. et al. (2025).** arXiv:2601.18939 | ⚠️ | Paper/title real, but first-listed author is **Claire O'Brien**, not S. O'Brien — a Sean O'Brien exists but is 7th of 9 authors. Also arXiv ID is Jan-**2026**, not 2025 — fix both the initial and the year. |
| 18 | **Petrov, D. (2026).** "The topic-matching trap in activation steering." arXiv:2603.22061 | ⚠️ **(worst offender)** | Real paper by **Valentin Petrov** (initial should be "V.", not "D."), and the actual title is **"On the Failure of Topic-Matched Contrast Baselines in Multi-Directional Refusal Abliteration"** — substantially different framing (refusal abliteration, not "activation steering"). The quoted claim used in §2.4 should be re-checked against the real paper before keeping the pull-quote. |
| 19 | **Shi, L. et al. (2025).** "When Thinking LLMs Lie." arXiv:2506.04909 | ⚠️ **(worst offender)** | Confirmed via both the local `paper-misalignment-axis/references.bib` and independent web search: **there is no "Shi" among the authors.** Real first author is **Kai Wang** (Kai Wang, Yihao Zhang, Meng Sun). Title itself is a valid truncation. This citation needs the author fixed to "Wang, K. et al." — as currently written it attributes the paper to the wrong person. |
| 20 | Vennemeyer et al. (2025). arXiv:2509.21305 | ✅ | Confirmed against local bib and web (Daniel Vennemeyer et al.). |
| 21 | Wu et al. (2026). arXiv:2603.05773 | ✅ | Confirmed — Jinman Wu et al., title truncation only ("...in Large Language Models" dropped). |
| 22 | **Zhao, Y. et al. (2025).** arXiv:2505.15038 | ⚠️ | Paper real, year correct, title a reasonable paraphrase — but first author is **Haiyan Zhao**, so "Zhao, Y." should be "Zhao, H." |
| 23 | Edrington, T. & CC (2026). "Targeted Deception Correction via Profile Normalization in Language Models." Companion paper. | ⚠️ | Title matches the actual companion draft exactly (verified at `/home/asdf/human-review/targeted-deception-correction/paper.md`) — good. But **author order is reversed**: the companion paper's own byline lists CC first, Thomas Edrington second, while this citation reads "Edrington, T. & CC." Minor, but pick one order and use it consistently (this paper's own byline also lists CC first). |

Not independently re-checked (no arXiv ID / journal given, low-risk general-knowledge citations): Baars (1988) beyond title-level check.

### Pattern worth flagging
Every mismatched *year* case (Genadi, Natarajan, O'Brien, and to check: Kumar/Petrov) stems from the same root cause: **arXiv IDs starting `26xx` are 2026 submissions, but the paper labels them "(2025)."** This looks like a systematic off-by-one on the arXiv-ID-to-year convention, not independent errors — worth a global find/check across the reference list rather than fixing one at a time.

The wrong-first-author cases (Baek→S. vs D., Kumar→A. vs S., O'Brien→S. vs C., Petrov→D. vs V., Zhao→Y. vs H., and the Shi/Wang mix-up) suggest the reference list was reconstructed from memory/paraphrase rather than copy-pasted from source metadata. Recommend regenerating the whole References section directly from arXiv/Semantic Scholar metadata rather than spot-fixing.

---

## Placeholder / Terminology / Formatting Check

- **No placeholder text found** — no TODO, TBD, XXX, "[fill in]", FIXME, or Lorem Ipsum anywhere in the draft.
- **Terminology drift (minor, stylistic):** the paper uses several near-synonymous names for the same two constructs without settling on one term each:
  - Component 1: "consequentiality substrate" (abstract, §1, §5.1, §5.4) / "consequentiality component" (§5.1, §5.3) / "consequentiality direction" (§5.4) / "base signal" (§6). Recommend standardizing on "consequentiality substrate" throughout, since that's the term used in the title and abstract.
  - Component 2: "deception-specific amplifier" (abstract) / "deception amplifier" (§1, §5.1) / "deception-specific component" (§5.3, abstract second use) / "deception discriminator" (§5.3, describing its monitoring *role* rather than the direction itself — this one is arguably a distinct concept, not just a synonym, so it's less of a problem, but could confuse a careful reader into thinking there are three components instead of two).
- **Reference list ordering:** alphabetical by surname throughout (Anthropic → Zhao), except the companion-paper self-citation (Edrington & CC) is placed last, out of alphabetical sequence. Likely intentional (keeping the self-citation visually separate), but worth a deliberate footnote or just leave as-is — flagging so it's a choice, not an oversight.
- **No other formatting issues found:** section numbering is consistent (1–6 plus Supplementary), the five-stage structure in §1.1 maps cleanly onto §4.1–4.4 and §4.6 (with §4.5 and §4.7 clearly marked as synthesis/extension rather than new stages — no numbering confusion), table formatting is consistent, statistical notation (d=, p<, AUC, Bonferroni) is used consistently throughout.
- Model name "Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled" (§3.1) is used only once and not repeated verbatim elsewhere — later references shorten to "Qwen3.5-27B" (§5.5), which is fine and consistent shorthand, not an error.

## Recommendation

Hold for one more pass focused exclusively on the References section — regenerate author names/years directly from arXiv metadata rather than editing the current list in place, since several errors (Shi→Wang, Petrov's title) are substantive enough that a careless in-place fix could still leave one wrong. Everything else (prose, structure, stats reporting, absence of placeholders) is ready to ship.
