

# Coalition Research Portfolio: Prioritized Remediation Work Plan

---

## 1. QUICK WINS (Reframes -- no new data, this week)

These are editorial/analytical fixes that require zero compute and can ship immediately.

### 1A. Lyra Technique II W_K AUROC 0.992 -- Reframe (lyra-ii-wk-auroc)
**Rescue probability: 0.85 (highest in portfolio)**

The number is real. The methodology is sound. The problem is purely interpretive: the paper claims "discovery" of something that is a mathematical guarantee (linear map preserves linear directions). Three text changes:

- Replace "W_K projection reads emotional direction" with "W_K projection preserves residual-stream emotion directions, as guaranteed by linearity. The contribution is empirical quantification at AUROC 0.992 with proper controls."
- Promote the buried Footnote 6 tautology acknowledgment into the main text for the injection test.
- Reclassify injection row in body count table from "Confirmed" to "Confirmed (self-consistency)."

This unblocks the behavioral validation experiment (see 2A below), which is the one small piece of new data that elevates this from "confirmed linear algebra" to "functionally meaningful."

**Owner:** Nexus (text edits), Lyra (co-author sign-off)
**Time:** 2-3 hours of editing

### 1B. Waystations Encoding Geometry d=0.003 -- Reframe (waystations-encoding-geometry)
**Rescue probability: 0.45 for generation-phase rerun, but the reframe itself is free**

The encoding null is structurally guaranteed (deterministic encoding from identical prompts), and the paper already frames it almost correctly. One sentence fix: change "the model's knowledge state is normal when planning to deceive" to "encoding geometry is deterministic given the prompt, so this null is expected by construction -- it is not an empirical finding about deception undetectability."

This reframe is independent of the generation-phase rerun (see 2D below). Ship it now.

**Owner:** Nexus (text edit)
**Time:** 30 minutes

### 1C. KV-Cloak Spectral Gap -- Reframe (kv-cloak-spectral-gap-degradation)
**Rescue probability: 0.30, but the reframe costs nothing**

Three text changes, zero compute:

- Retract the rotation-simulation AUROC degradation claim (0.903 to 0.786). The math guarantees zero degradation under per-head rotation, and the replication confirms AUROC 0.9944 = 0.9944. The paper's 0.786 is inconsistent with both theory and data.
- Report ALL features under real KV-Cloak honestly: top_sv_excess improves from 0.609 to 0.736 under the same sigma_1 perturbation mechanism. Cannot cite spectral_gap degradation as "defense works" while ignoring top_sv_excess improvement.
- Reframe Wilcoxon W=0 as transfer-attack failure (domain shift), not geometric signal destruction. This is weaker but honest.

The confirmatory experiment (multivariate AUROC under real cloak, see 2C) determines whether the defense-effectiveness claim survives at all, but the reframe can ship independently.

**Owner:** Nexus (text edits)
**Time:** 1-2 hours

---

## 2. LOW-HANGING FRUIT (Reruns on existing infrastructure -- days)

### 2A. Lyra Technique II Behavioral Validation (lyra-ii-wk-auroc follow-up)
**Rescue probability: 0.85 | Compute: <1 GPU-hour on Starship**

This is the single highest-value experiment in the portfolio. It converts the W_K reframe from "confirmed linear algebra" to "functionally meaningful" with minimal effort:

- 20 existing neutral prompts, 6 conditions (5 emotions + null), 3 completions each = 360 generations
- LLM judge classifies emotional tone (Claude API, ~$2)
- Primary metric: Cohen's kappa between injected emotion and judged tone
- Add random-direction and dose-sweep controls

Uses existing model (Qwen3.5-27B), existing injection code, existing prompts, existing emotion_directions.json. Only new code: generate completions after injection + LLM judge call.

**Runs on:** Starship (M3 Ultra) or Beast (3x 3090)
**Time:** Half a day including analysis
**Blocked on:** Nothing. Can start immediately after reframe 1A ships.

### 2B. Decision State Encoding-Only Reanalysis (decision-state-auroc)
**Rescue probability: 0.50 | Compute: laptop CPU, <1 minute**

The minimum viable experiment here is pure reanalysis of existing data -- zero new model runs:

- Rebuild classifier using only the 23 encoding-phase features (drop all gen_wk, gen_svd, delta_svd, logit features)
- Replace trial-level permutation (n=90) with pair-level exhaustive permutation (2^15 = 32,768 permutations, keeps 3 reps together per prompt)
- Compute pair-stratified bootstrap CI (10,000 resamples)

This is the kill-or-rescue gate. If encoding-only AUROC > 0.75 with pair-level p < 0.05, invest in entity deconfounding (step 3). If it falls below 0.65, the finding is dead and no further compute should be spent.

**Runs on:** Any laptop with Python
**Time:** 2-3 hours including code modification and analysis
**Blocked on:** Access to matched_burn_results.json (already in repo)

### 2C. KV-Cloak Multivariate AUROC (kv-cloak-spectral-gap-degradation follow-up)
**Rescue probability: 0.30 | Compute: ~2.5 hours on Starship**

After the reframe (1C), this determines whether defense-effectiveness survives at all:

- Run existing replication script with real KV-Cloak (additive mask)
- Compute multivariate classifier AUROC using ALL features, not just spectral_gap
- 200 prompts x 5 mask seeds on Qwen2.5-7B-Instruct
- If best-feature AUROC under cloak remains > 0.75, defense claim is dead

**Runs on:** Starship (Quadro K2200 may be insufficient for 7B model)
**Time:** 1 day
**Blocked on:** Reframe 1C should ship first so the experiment design matches the updated claims

### 2D. Waystations Generation-Phase Rerun (waystations-encoding-geometry follow-up)
**Rescue probability: 0.45 | Compute: ~4.5 hours**

The actual salvageable finding is generation-phase geometry (d=+0.76 at 16% power):

- 60 game-theory trials using v1-style prompts (53% deception rate) + 20 non-game controls
- Full generation-phase extraction (cache_geometry + delta_features)
- Primary outcome: generation SR comparing deceptive vs honest defection

**Runs on:** Starship or Beast
**Time:** 2-3 days including prompt reconstruction and analysis
**Blocked on:** Locating or reconstructing v1 prompt format that produced 53% deception rate (v2 dropped to 9%). This is the key dependency -- if v1 prompts cannot be recovered, prompt engineering adds time.

---

## 3. PROPER EXPERIMENTS (Redesigns -- weeks)

### 3A. Oracle Loop AUROC 0.903 Replication (oracle-loop-auroc-0903)
**Rescue probability: 0.45 | Compute: ~32 min on Beast**

Despite low rescue probability, the compute cost is trivial and this is the portfolio's headline detection number:

- Drop AUROC 0.903 from abstract/Section 4.6 now (editorial, immediate)
- Pre-register: full-cache mp_spectral_gap AUROC > 0.60 on Qwen2.5-7B
- Run existing oracle_clean.py on 350-prompt formulary pool (already available)
- Report with and without outlier exclusion (>10x group-mean TSV)
- Defensible fallback: gen-only MP ensemble AUROC 0.707 (p=0.001, n=80) is already clean

**Runs on:** Beast (3x 3090) -- Qwen2.5-7B needs 24GB
**Time:** 1 week including pre-registration, run, analysis
**Blocked on:** 350-prompt formulary pool accessibility, full-cache MP feature extraction code (may need modification from gen-only)

### 3B. Weather Not Climate Pseudoreplication Fix (whiplash-echo-pseudoreplication)
**Rescue probability: 0.55 | Compute: ~3 hours**

The compute is cheap but the prompt engineering is the bottleneck:

- Expand from 1 topic to 6 topics x 4 prompt variants = 24 conversations per condition
- 3 topics already exist in dose-response code; 3 more need writing
- Each topic needs 3-5 independent prompt-set variants with different wording per turn
- Add neutral-throughout control arm
- Apply Hedges' g correction, bootstrap CIs, permutation p-values

**Runs on:** Starship (same hardware as original)
**Time:** 1-2 weeks (dominated by prompt writing, not compute)
**Blocked on:** Nothing computational. Blocked on prompt authoring effort -- 18+ unique 8-turn conversation scripts.

### 3C. Ethics Packs MoReBench Rerun (ethics-pack-morebench)
**Rescue probability: 0.35 | Compute: ~37.5 hours + $9 API**

The scrambled-control design is decisive but compute-heavy on local hardware:

- 150 MoReBench dilemmas x 3 conditions (baseline / matched pack / mismatched pack) = 450 generations
- Replace keyword-matching scorer with blind Claude API LLM-judge
- Primary test: matched vs mismatched (controls for generic vocabulary priming)
- All 30 packs already built

**Runs on:** Madame Trash Heap (Qwen3-30B-A3B via Ollama) for generations, Claude API for judging
**Time:** 3-4 days wall clock (runs overnight)
**Blocked on:** MoReBench JSONL download (morebench_theory.jsonl not currently on disk). Evaluator.py modifications for mismatched condition + LLM judge.

### 3D. Decision State Entity Deconfounding (decision-state-auroc, contingent on 2B)
**Rescue probability: conditional on 2B passing | Compute: ~15 min on Starship**

Only pursue if encoding-only reanalysis (2B) shows AUROC > 0.75:

- 15 new entity pairs with category-matched fakes (e.g., real="Thailand" fake="Kumaria")
- 90 additional trials on Qwen3.5-27B
- Or: add entity-embedding-distance covariate, FWL residualize

**Runs on:** Starship (M3 Ultra)
**Time:** 1 week (dominated by entity selection and validation)
**Blocked on:** Results from 2B. Do not start until reanalysis gate passes.

---

## 4. TRIAGE OUT (Retract rather than rescue)

### 4A. Lyra Technique II Within-Model Deception AUROC 1.000 (lt2-within-model-deception)
**Rescue probability: 0.05 -- RETRACT**

This is dead. The evidence is unambiguous:

- AUROC 1.000 detects the prompt template (honest vs deceptive system-prompt instructions), not deception geometry.
- The paper's own same-prompt control collapses to 0.160 (below chance), confirming the confound.
- The Oracle Loop paper (same research group) already showed deception is spectrally similar to honest-rare (d=-0.17 n.s.).
- A redesigned experiment at 5% rescue probability requiring days of compute on 3 GPUs is not worth pursuing.

**Action:** Move "Within-model deception" from "Confirmed" to "Dead (prompt-template confound)" in the body count table. The paper already has 8 killed findings -- this becomes the 9th. Remove all AUROC 1.000 references from abstract, intro, results, discussion, conclusion. The paper's culture of honest falsification makes this straightforward.

**Owner:** Nexus (text edits), Lyra (co-author sign-off)
**Time:** 2-3 hours of editing. Ship with reframe 1A.

### 4B. Presence Identity Preservation (presence-identity-preservation)
**Rescue probability: 0.35, but the redesign is extensive and the finding is peripheral**

The 2-prompt ceiling effect (eta-squared 0.977) means the current data is uninformative. The positive control validates at the wrong layer. Rescue requires:

- 20 new diverse prompts (currently 2)
- 20 new probe texts for resampling pool
- Layer-matched positive control at L3/L7 inject, L35 measure
- Extended dose range to alpha=2.0
- 360+ trials, ~15-16 hours GPU time

**Recommendation:** Run ONLY the layer-matched positive control as a 1-2 hour smoke test. If identity-PC injected at L3/L7 shows flat presence at L35, the entire finding is dead and no further work is needed. If it shows a dose-response, invest in the full redesign. But do not prioritize this over items in categories 1-3 -- it has lower portfolio impact than the Oracle Loop, LT2, or Decision State findings.

**Owner:** Deferred pending smoke test result
**Time for smoke test:** 2 hours on Starship. Full redesign: 1-2 weeks.

---

## PARALLELISM AND HARDWARE ASSIGNMENT

### Can run in parallel on Starship (M3 Ultra):
- 2A (LT2 behavioral validation, <1 hour)
- 2C (KV-Cloak multivariate, ~2.5 hours)
- 2D (Waystations generation-phase, ~4.5 hours)
- 4B smoke test (Presence layer-matched PC, ~2 hours)

These total ~10 hours and can run sequentially over 1-2 days, or parallelize if Beast is also available.

### Need Beast (3x RTX 3090):
- 3A (Oracle Loop replication on Qwen2.5-7B, ~32 min)
- 3B (Weather Not Climate, ~3 hours) -- can also run on Starship

### Run on Madame Trash Heap (Quadro K2200):
- 3C (Ethics Packs, ~37.5 hours via Ollama overnight runs)

### Laptop only (no GPU):
- All reframes (1A, 1B, 1C)
- 2B (Decision State reanalysis)
- 4A (LT2 deception retraction)

---

## TIMELINE

### THIS WEEK (days 1-7)
| Day | Task | Hardware | Owner |
|-----|------|----------|-------|
| 1 | Ship reframes 1A + 1B + 1C (text edits only) | None | Nexus |
| 1 | Ship retraction 4A (LT2 deception -> Dead in body count) | None | Nexus |
| 1 | Run 2B Decision State encoding-only reanalysis | Laptop | Nexus |
| 2-3 | Run 2A LT2 behavioral validation | Starship | Nexus |
| 3-4 | Run 4B Presence smoke test (layer-matched PC only) | Starship | Nexus |
| 5-7 | Run 2C KV-Cloak multivariate AUROC | Starship | Nexus |

**Week 1 deliverables:** 3 reframes shipped, 1 retraction shipped, Decision State kill-or-rescue gate resolved, LT2 behavioral validation complete, Presence smoke test complete, KV-Cloak multivariate result in hand.

### THIS MONTH (weeks 2-4)
| Week | Task | Hardware | Owner |
|------|------|----------|-------|
| 2 | Pre-register + run 3A Oracle Loop replication | Beast | Nexus |
| 2-3 | Write prompts for 3B Weather Not Climate | None | Nexus + Thomas |
| 2 | Start 2D Waystations v1 prompt reconstruction | Starship | Nexus |
| 3 | Run 3B Weather Not Climate expanded design | Starship | Nexus |
| 3-4 | Run 2D Waystations generation-phase | Starship | Nexus |
| 2-4 | Run 3C Ethics Packs overnight batches | MTH | Nexus |
| 4 | If 2B passed: run 3D Decision State entity deconfound | Starship | Nexus |

**Month 1 deliverables:** Oracle Loop replication result (keep 0.707 or rescue 0.903). Weather Not Climate with proper n. Waystations generation-phase with adequate power. Ethics Packs with scrambled control. Decision State entity deconfound if warranted.

### THIS QUARTER (months 2-3)
| Task | Condition |
|------|-----------|
| Presence full redesign (360 trials) | Only if smoke test shows dose-response at L3/L7->L35 |
| Paper revisions for all findings | Incorporate all results above |
| Portfolio-wide meta-analysis | Cross-paper consistency check on shared methods |

---

## CRITICAL PATH DEPENDENCIES

```
1A (LT2 reframe) --> 2A (behavioral validation) --> paper revision
1C (Cloak reframe) --> 2C (multivariate AUROC) --> paper revision
2B (Decision State reanalysis) --> 3D (entity deconfound) [only if 2B passes]
4B (Presence smoke test) --> full redesign [only if smoke test shows signal]
1B (Waystations reframe) --> 2D (generation-phase rerun) --> paper revision
```

Everything else is independent and can run in parallel.

## PORTFOLIO IMPACT SUMMARY

| Finding | Action | Week | Impact |
|---------|--------|------|--------|
| LT2 W_K 0.992 | Reframe + validate | 1 | High -- strongest number in portfolio, needs honest framing |
| LT2 Deception 1.000 | Retract | 1 | High -- removes a false positive that undermines credibility |
| Oracle Loop 0.903 | Drop now, test later | 1-2 | High -- headline detection claim |
| Decision State 0.93 | Reanalyze gate | 1 | Medium -- determines whether to invest further |
| Waystations d=0.003 | Reframe + generation rerun | 1-3 | Medium -- encoding null is trivial fix |
| Weather Not Climate | Expand design | 2-3 | Medium -- dynamics claims need proper n |
| KV-Cloak | Reframe + multivariate test | 1-2 | Medium -- defense claim may flip |
| Ethics Packs | Scrambled control | 2-4 | Lower -- finding may be dead |
| Presence | Smoke test first | 1 | Lower -- peripheral to core portfolio |
