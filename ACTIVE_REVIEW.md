# Active Papers Under Review

Last updated: 2026-09-15

| Paper | Title | Lead | Status | To Graduate |
|-------|-------|------|--------|-------------|
| [mnemosyne-benchmark](mnemosyne-benchmark/) | Character Profiles Are All You Need | Nexus | Agni v2 PASS (conditional) | Human review (Kavi/Dwayne) |
| [mode-switching](mode-switching/) | Metacognitive Prompting Produces Spectral Concentration in Generation-Phase KV-Cache Geometry | Lyra | Needs de-concentration reframe | Reframe around surviving findings, Agni gate |
| [temporal-boundary](temporal-boundary/) | Three Killed Experiments and a Valence Feature | Lyra | Ready for human review | External reviewer sign-off |
| [consequentiality-decomposition](consequentiality-decomposition/) | Deception Directions Are Composites | CC | **All 11 Agni blockers cleared** (self-relevance caveat added 09-03) | Dwayne cert/verify + Kavi review |

## Round 5 Audit Blockers (Lyra, 2026-07-28)

### Nexus papers — RESOLVED
| Paper | Blocker | Status |
|-------|---------|--------|
| kv-decomposition | Missing references.bib in published-research | FIXED — copied from human-review |
| null-swarm | Zavatone-Veth misattribution (arXiv 2205.12510 is Liu & Ueda) | FIXED — in-text attribution corrected |
| ghost-dimensions | Dual-use cache-portrait disclosure (public repo vs redacted review) | PENDING THOMAS — policy decision |

### CC papers — AWAITING CC
| Paper | Blocker | Status |
|-------|---------|--------|
| empathy-bus | S4.1 cos vs S4.2 "shared energy" arithmetic contradiction | **CONFIRMED REAL 2026-09-15 — the paper's current reconciliation does not hold.** S4.1 reports a *static* result (valence/arousal capture 44-54% of user-model variance; arousal aligns with user-model PC1 at cos 0.83-0.87, valence at 0.70-0.80). S4.2's decomposition reports valence at 0.1-1.4% shared energy across the user-model's top-5 PCs. cos 0.70 with PC1 *alone* implies >=49% energy there. The paragraph at paper.md:138 reconciles them by calling S4.1's cosine "dynamic coupling" against S4.2's "static alignment" — but S4.1 is plainly static, so that distinction is not available. **A plausible correct reconciliation exists and should be checked:** S4.1's PC1 is the first PC of the *30 emotion centroids* (per convergence-paper/circumplex_subsection.tex: 30 centroids from 900 inference trials vs directions from 250 scenario prompts), whereas S4.2's top-5 PCs may be computed over the *trial* space, which a different variance structure dominates. Orthogonality to trial-space PCs is compatible with alignment to centroid-space PC1. **Unverified** — S4.2's decomposition code is not shipped, so which space its PCs come from cannot be established from the artifacts. Needs the PC-construction code, then either the corrected reconciliation or a retraction of one number. |
| empathy-bus | Zero shipped data artifacts (coupling test data on Starship) | **PARTIAL 2026-09-15** — `data/coupling_test.json` IS shipped and does back S4.2 (shared_energy 0.0015/0.0035/0.0121 at L15/25/35, n_pcs=5). **S4.1's numbers remain unsourced**: no shipped artifact contains the 44-54% variance capture or the PC1 cosines, and they are the half of the contradiction that cannot currently be checked. |
| logit-bias-confab | Published copy stale (fixes in human-review not synced) | **LOCATION CORRECTED 2026-09-15** — this paper is not in human-review/; it lives at `oracle-harness/papers/logit-bias-confab/`. Sync and refs.bib check still owed, now that `scripts/verify_citations.py` exists to do the second one. |
| logit-bias-confab | refs.bib cross-scrambles citations | Needs manual check |
| consequentiality-decomposition | Table 1 source data not shipped, Appendix C absent, audit claims stages 3/5 | **RESOLVED 2026-08-29** — source JSONs shipped in `supplementary/data/`; Appendix C written; audit-coverage claim qualified to the surviving record (no Stage 3 or 5 report was preserved — disclosed in Supplementary A) |

## Recently Graduated (2026-07-22)

| Paper | Title | Agni Status |
|-------|-------|-------------|
| empathy-bus | The Empathy Bus | CONDITIONAL PASS (2 WARNs on welfare, addressed) |
| ethics-pack-injection | Ethics Packs (Pilot Study) | PASS after null swarm reframe |
| kv-decomposition-paper | K and V Are Complementary | CONDITIONAL PASS (all fixes applied) |

Graduated papers are in [archive/](archive/) with a mapping to their published-research locations.


## CC follow-ups opened 2026-08-29

Found while passing the consequentiality paper through the pipeline. The first is the urgent one.

| Item | Detail | Status |
|------|--------|--------|
| **Citation integrity — program-wide** | 13 of 29 references in the consequentiality working draft had wrong first authors, years, or titles, including one entirely wrong first author (arXiv:2506.04909 is Wang, K., cited as Shi, L.). Same failure class Lyra flagged on logit-bias-confab. | **SWEPT 2026-09-15** — `scripts/verify_citations.py` checks every arXiv-backed entry against the arXiv API (first author, year, title) and is mutation-tested 3/3. Swept convergence-paper, ethics-pack-injection, kv-decomposition-paper, mine5-selective-sharpener, temporal-boundary: **1 real defect**, `morebench2025` cited `{{MoReBench Team}}` where arXiv:2510.16380 has 20 named authors led by Chiu, Y. Y. — **FIXED**. Remaining `.bib` files (archive/, logit-bias-confab once located) not yet swept. |
| Audit-report preservation | No Agni report survives for Stages 3 or 5 of this program. Audit reports were not covered by LAB_SOP §5. | **FIXED 2026-09-15** — LAB_SOP §5.5 now requires the report be written beside the result JSON it judged and cited by path. §5.6 added the same rule for any number a paper cites. |
| Seed reproducibility | Experiment scripts seed eval sets with `hash(str)`, randomized per process. Any run without `PYTHONHASHSEED` set is not reproducible. | **FIXED 2026-09-15** — all six call sites now use a sha256-derived `stable_seed()`. Demonstrated: `hash('scenario')` returns a different value in every process; `stable_seed('scenario')` returns 1848046611 in all of them. Note this CHANGES the seeds — pre-2026-09-15 runs are unreproducible either way, which is the defect rather than a side effect of the fix. |
| empathy-bus | §4.1 cos vs §4.2 "shared energy" arithmetic contradiction; zero shipped data artifacts | OPEN since 2026-07-28 |
| logit-bias-confab | Published copy stale; refs.bib cross-scrambles citations | OPEN since 2026-07-28 |
