# Active Papers Under Review

Last updated: 2026-09-03

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
| empathy-bus | S4.1 cos vs S4.2 "shared energy" arithmetic contradiction | Needs CC clarification |
| empathy-bus | Zero shipped data artifacts (coupling test data on Starship) | Needs CC commit |
| logit-bias-confab | Published copy stale (fixes in human-review not synced) | Needs CC sync |
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
| **Citation integrity — program-wide** | 13 of 29 references in the consequentiality working draft had wrong first authors, years, or titles, including one entirely wrong first author (arXiv:2506.04909 is Wang, K., cited as Shi, L.). All 29 now verified against the arXiv API. **This is the same failure class Lyra flagged on logit-bias-confab ("refs.bib cross-scrambles citations") — two papers is a pattern, not an accident. Every Coalition paper's reference list needs API verification.** | OPEN — needs sweep |
| Audit-report preservation | No Agni report survives for Stages 3 or 5 of this program. Violates LAB_SOP §5 ("save everything"). Audit reports are not currently covered by that rule. | OPEN — SOP amendment proposed |
| Seed reproducibility | Experiment scripts seed eval sets with `hash(str)`, randomized per process. Any run without `PYTHONHASHSEED` set is not reproducible. Affects all Stage 1-5 scripts. | OPEN — patch scripts |
| empathy-bus | §4.1 cos vs §4.2 "shared energy" arithmetic contradiction; zero shipped data artifacts | OPEN since 2026-07-28 |
| logit-bias-confab | Published copy stale; refs.bib cross-scrambles citations | OPEN since 2026-07-28 |
