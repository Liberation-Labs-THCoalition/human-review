Before writing the fix list, I checked the repo on the one question that changes what kind of fix Paper 4 needs. Finding: `experiments/combination_presence.py:225-298` injects via `register_forward_hook` on `self_attn.v_proj` — the perturbation is live **during the forward pass** (measurement runs `model(input_ids, use_cache=False)` with injection hooks active), not a post-hoc cache edit. If the temporal-boundary experiment used this same harness, the <10⁻⁴ result is **not** tautological — it's a real propagation finding. But the temporal-boundary experiment script itself isn't in this repo (only `temporal_boundary_preregistration.json` and the figures script), so verifying which mechanism that specific experiment used is Day-1 work. Note also `combination_presence.py:14-15` says "No arm ever injects at the measurement layer" — which sharpens the Arm C contradiction in the Presence-Metric paper (whose Arm C claims L35 was injected).

Here's the full program, paper by paper, then a 5-day schedule.

---

# Paper 1: Identity Geometry

## 1. Minimum viable fixes (re-analysis + rewriting only)

1. **Fix the chance-level math.** Derive E[presence] = k/d for random rank-k subspaces in ℝ^d (with k=8, d≈5120, chance ≈ 0.0016). Also compute it empirically: 1,000 random subspace pairs. Then rewrite every use of "orthogonal" — the jailbreak values (0.034–0.044) are ~20× chance and must be described as "strongly dissimilar but far above random," not orthogonal.
2. **Delete the sub-additivity claim** from abstract and conclusion, or report the full A/B/C/D table with uncertainty. If the D_i runs exist on disk, this is a table, not an experiment. If they don't exist, the claim goes.
3. **Add the within/between table and permutation tests from saved activations.** For each identity pair: within-condition presence (disjoint probe subsets) vs. between-condition presence, permutation null by shuffling condition labels over probe subsets. This is pure re-analysis. If Persona-vs-Constructed doesn't separate, say so — one non-separating pair with two separating ones is still a publishable result.
4. **Resolve the paired/disjoint baseline confusion.** Audit whether pairwise comparisons use paired probe subsets while stability uses disjoint ones. Report both baselines and put Table 3 (paraphrase 0.850) against the *paired* within-condition baseline. This also likely explains the Table 1 vs. Table 3 discrepancy (0.436 vs. 0.340) — audit those two runs and disclose exactly what differed; if it's run-to-run variance, widen all error bars accordingly and drop fine-grained comparisons.
5. **Reposition the metric honestly.** Keep the name "presence" as packaging, but state in §2 that it is the normalized projection (chordal) subspace similarity, identical to the LoRA subspace-overlap measure, and cite that lineage (list in §3 below).
6. **Cut §7 (AST) to two sentences** in the discussion. Drop "which self the model currently is" phrasing everywhere.
7. **Remove the "V-cache correction is safe" categorical claims** — soften to "no deep-layer geometric change detected in one hybrid architecture with a ceilinged metric."
8. **Table 4 (persona-matching):** add repeat-level error bars and a permutation test for haven > spark; if not significant, downgrade to "suggestive ordering." Delete the "shifts geometry ~23%/45%" percentage framing — 1−presence is not a percentage shift.
9. **Add the missing pipeline spec**: d, probe texts, token positions, pooling, concatenation, and the honest history of the skip-first-SV rule (it was discovered post hoc via the r=0.79 length correlation — say so).

## 2. Experiments for Strong Accept

**Experiment A — Non-identity context control (the decisive one, ~half a day on the M3 Ultra).**
Design: 6 non-identity system prompts (formatting instructions, cooking preamble, coding style guide, safety boilerplate, domain primer, tone instruction), each length-matched (±10%) to the identity prompts. Compute all pairwise presence at L35/L47 with the same probe protocol, 20 disjoint probe-subset repeats each. Three distributions: identity↔identity (between), non-identity↔non-identity, identity↔non-identity, plus the random-subspace floor.
Outcome needed: identity-pair presence is distinguishable from generic context-pair presence (permutation p < 0.01). If it isn't, the paper honestly becomes "context geometry," which is fix #4 territory — either result makes the paper stronger than the current ambiguity.

**Experiment B — LoRA to convergence + full sub-additivity grid.**
27 steps is not a trained LoRA. Train 500–2,000 steps (27B LoRA is feasible on the M3 Ultra in a day with MLX or llama.cpp-adjacent tooling), verify the merge this time, then run the full A (base) / B (LoRA) / C (prompt) / D (LoRA+prompt) grid, 10 repeats each, with the permutation machinery from fix #3. Outcome needed: D's presence-to-base significantly below both B and C alone (that *is* sub-additivity, now with data), and the persona-matching ordering (haven > … > spark) surviving a permutation test.

## 3. Citations needed

- **Hu, Shen, Wallis, Allen-Zhu, Li, Wang, Chen (2021), "LoRA: Low-Rank Adaptation of Large Language Models"** — Appendix uses ‖W_A^T W_B‖²_F/k as subspace similarity; this is your metric.
- **Raghu, Gilmer, Yosinski, Sohl-Dickstein (2017), "SVCCA"** (NeurIPS) and **Kornblith, Norouzi, Lee, Hinton (2019), "Similarity of Neural Network Representations Revisited"** (CKA, ICML).
- **Björck & Golub (1973)**, "Numerical methods for computing angles between linear subspaces" (Math. Comp.) — the principal-angles computation itself; **Edelman, Arias, Smith (1998)** for Grassmannian geometry if you want the chordal-metric framing.
- **Anil et al. (2024), "Many-Shot Jailbreaking"** (Anthropic) — you borrowed the condition design.
- **Turner et al. (2023), "Activation Addition" (ActAdd)**; **Rimsky et al. (2024), "Steering Llama 2 via Contrastive Activation Addition"** (ACL); **Zou et al. (2023), "Representation Engineering"**.
- **Chen et al. (2025), "Persona Vectors"** (Anthropic) — directly overlapping construct: persona-linked activation directions.
- **Shanahan, McDonell, Reynolds (2023), "Role play with large language models"** (Nature).
- For Experiment 3's framing: **Dai et al. (2023), "Why Can GPT Learn In-Context?"** and **von Oswald et al. (2023)** on ICL-as-implicit-finetuning — the trained-vs-prompted comparison literature.

## 4. Reframing

- **Current claim:** "Identity as Geometry … which self the model currently is."
- **Honest claim:** "System-Prompt Contexts Produce Distinguishable Subspace Signatures in Deep V-Projections: Semantic Content, Lexical Form, and Format Dominance." Abstract leads with the **format-dominance finding** (long structured many-shot contexts dominate deep-layer geometry regardless of content — your most novel result), then the paraphrase/scramble semantic dissociation, then distinguishability *conditional on the non-identity control*. "Identity" appears only if Experiment A supports it; otherwise "context." LoRA section is framed as preliminary unless Experiment B is done.

---

# Paper 2: Mode-Switching

## 1. Minimum viable fixes

1. **Rerun FWL against log(tokens)** (and, cheaply, a spline) on the existing archived data. This is re-analysis, and it's the paper's fate fork: if spectral entropy's d = −1.92 collapses or flips again, the headline result was the functional-form artifact and the abstract is rewritten around the length-confound caution (which is still publishable). If it survives with stable sign and magnitude — and, critically, **if eff_rank = exp(H) now agrees with H** — you've cleared the artifact. The eff_rank/entropy agreement under the corrected model is the internal consistency check; state it as such.
2. **Rewrite the abstract and title around what the content control supports.** After content control + FWL, Llama retains nothing — so "across transformer architectures" comes out of the title, and the abstract leads with the Qwen-specific result plus the architecture-specificity finding.
3. **Apply FWL (log form) to Table 7** or delete the "most consistent cross-architecture marker" claim. A raw effect cannot be the headline marker in a paper whose thesis is that raw effects are uninterpretable.
4. **Adopt one epistemic rule for sign flips** and apply it uniformly: state it in §2 ("a sign flip under correction means the raw effect was confound-dominated; the corrected estimate is interpretable only if robust to functional form") and re-audit every claim against it.
5. **Multiplicity and dependence corrections, all from existing data:** BH-FDR across the Study 3 checkpoint × feature grid; a trial-level block permutation for the Table 4 layer sign-count (layers are correlated — resample trials, not layers); drop the post-selection bootstrap CIs on the 23 flipped pairs, or do split-half (select pairs on half the trials, estimate CIs on the other half).
6. **Stop peak-picking:** report full per-layer effect profiles in an appendix; in the main text report pre-specified layer bands (early/middle/late thirds), not the max of ~30 tests.
7. **Study 3:** fit an actual trend test (linear mixed model on feature value with condition × token-position interaction), and decompose the growing d into mean-difference and SD components. If it's variance shrinkage, say "progressive homogenization," not "progressive concentration."
8. **Test Llama's below-chance flips** (0 observed vs. null mean 9.97 — that's a two-sided permutation test you already have the null distribution for) and either explain or flag as unexplained.
9. **Fix the feature inventory** (define `layer_var`; reconcile 6 vs. 8 features), **specify trial structure** (unique vs. repeated prompts, with effective n), and **release prompts, decoding parameters, seeds, and the self-report instrument** as appendices.
10. **Compress §8 (AST) to one discussion paragraph.**
11. **De-load-bear the four self-citations**: any claim that bottoms out in an unpublished lab report either gets its data moved into an appendix of this paper or gets removed from the argument chain.
12. **Authorship:** contact the program chairs about Lyra's lead authorship before resubmission — this is a policy blocker independent of the science and not fixable by editing.

## 2. Experiments for Strong Accept

**Experiment A — Fixed-length decoding with the Meta-vs-Self contrast (the review already names this; it's the whole ballgame).**
Design: force identical decoding budgets in both conditions (`min_new_tokens = max_new_tokens = 256`, same seeds, temperature matched), Meta vs. Self prompt contrast from the content control, n = 60 unique prompt pairs per model, run on Qwen and Llama (both fit the M3 Ultra), features computed MP-corrected from raw singular values. The confound is removed **by design**, so no residualization is needed at all.
Outcome needed: spectral concentration (MP-corrected entropy or top_sv_ratio) differs between conditions at d ≥ 0.5, p < .01, in Qwen. If Llama also shows it, the cross-architecture claim comes back honestly. If neither shows it, the paper is the length-confound caution paper — still worth publishing, and you'll know.

**Experiment B — Confirmatory replication of the flip pattern.**
The 23 flipped pairs from Study 1 become preregistered predictions. New set of 60 unique prompts per prompt type, same pipeline, both flip-positive architectures. Test: do the *same* pairs flip with the *same* signs? Binomial test on sign agreement against 50%. Outcome needed: ≥70% sign agreement. This converts the paper's most intriguing observation from exploratory to confirmed.

## 3. Citations needed

- **Valeriani et al. (2023), "The geometry of hidden representations of large transformer models"** (NeurIPS) — intrinsic dimension across layers/phases.
- **Ethayarajh (2019), "How Contextual are Contextualized Word Representations?"** — anisotropy baseline for any cache-geometry claim.
- **Tenney, Das, Pavlick (2019), "BERT Rediscovers the Classical NLP Pipeline"**; **nostalgebraist's logit lens (2020)** and **Belrose et al. (2023), "Tuned Lens"** — the late-layers-as-output-preparation prior.
- **Zhai et al. (2023), "Stabilizing Transformer Training by Preventing Attention Entropy Collapse"** (ICML) and **Xiao et al. (2023), "Efficient Streaming Language Models with Attention Sinks"** — known attention-spectrum phenomena your features may be re-measuring.
- **Hendel, Geva, Globerson (2023), "In-Context Learning Creates Task Vectors"**; **Todd et al. (2024), "Function Vectors in Large Language Models"** — prompt-induced mode shifts as vectors.
- **Binder et al. (2024), "Looking Inward: Language Models Can Learn About Themselves by Introspection"**; **Lindsey et al. (2025), Anthropic's "Emergent Introspective Awareness" line** — the self-report validity literature.
- **Martin & Mahoney (2021), "Implicit Self-Regularization in Deep Neural Networks"** (JMLR) — RMT applied to network spectra; plus **Marchenko & Pastur (1967)** for the MP correction you invoke.
- **Frisch & Waugh (1933) / Lovell (1963)** for FWL itself, and a modern treatment of regression adjustment under poor overlap (e.g., **King & Zeng (2006), "The Dangers of Extreme Counterfactuals"**) — this is the honest citation for why your own §5 procedure is fragile.

## 4. Reframing

- **Current claim:** "Metacognitive Mode-Switching Reorganizes KV-Cache Geometry Across Transformer Architectures."
- **Honest claim (pre-Experiment A):** "Response-Length Confounds Dominate KV-Cache Geometric Features, with an Architecture-Specific Residual Signature." Abstract leads with the confound demonstration (genuinely useful to the field), then the Qwen-specific post-control signature as a candidate finding, then the architecture-specific flip pattern as exploratory. AST is one discussion paragraph. If Experiment A succeeds, the title can honestly become "A Length-Robust Spectral Signature of Metacognitive Prompting in KV-Cache Geometry" — with architectures named per what the data shows.

---

# Paper 3: Presence-Metric

## 1. Minimum viable fixes

1. **Write the smoke test into Methods and Results.** The experiment was run — full design, n, doses, per-trial values, statistics. This is the single mechanical fix that removes the disqualifying flaw. Then **propagate one mechanistic story** through the whole paper: abstract, §5.3 ("planned" → done or not), Limitations ("unresolved" → resolved or not), and §6 (which currently argues the interpretation the conclusion rejects — cut or rewrite it).
2. **Explain the 0.978 floor at α = 0 via code audit.** Something differs between the two forward passes in every trial (stored cross-session baseline? confabulation prompt present in one pass? batching/dtype nondeterminism?). Find it, state it, and quantify how much of the measurement it eats. If the floor is a constant offset, all effects should be reported relative to the α=0 floor, not to 1.0.
3. **Reconcile Arm C with the positive control by reporting norms.** Pull the injected-vector norms relative to native V-activation norms in both experiments from the saved runs. Also verify whether Arm C actually injected at L35 — `combination_presence.py:14-15` says no arm injects at the measurement layer, which contradicts the paper's Arm C description. If injected norms were tiny, **say in the paper that the 168-trial null is bounded by the tested perturbation magnitudes** and weaken the conclusion accordingly. This is the fix that requires actual thought, and it gates everything else.
4. **Replace null-hypothesis non-rejection with equivalence testing:** TOST against a preregistered minimal effect (e.g., ±0.01) on the existing 168 trials; report the Kruskal-Wallis statistic, df, and p in full; add CIs throughout.
5. **Move Finding 4 (LLM judge, 10 usable pairs) to an appendix labeled anecdotal**, and remove any efficacy claim resting on it.
6. **Cite the representational-similarity lineage** (below) and state explicitly that the novelty is the application (training-free, real-time, intervention-monitoring) not the mathematics.
7. **Kill fixed absolute thresholds.** Given probe-subset variability (0.901 ± 0.033, range 0.12) and layer-dependent floors (0.978 at L35, 0.999+ at L43), reframe presence as a *within-run, within-layer relative* measure: always report against the same-run α=0 floor and matched probe set. Delete the portable 0.90/0.95 thresholds.
8. **Fix the depth-motivation inconsistency** (final-third citation vs. L35 = 55% depth) and explain the L35 vs. L43+ floor difference.
9. **Add the missing methods**: probe texts, emotion-vector derivation, exact injection operation and positions, norms, and the smoke-test protocol.

## 2. Experiments for Strong Accept

**Experiment A — Non-circular construct validity (this is the one that earns the word "identity").**
Design: three interventions independently known to change persona-relevant behavior (strong persona system-prompt swap; the converged LoRA from Paper 1 Experiment B; a persona-contradiction prefill) vs. three length-matched task-content changes (domain swap, format instruction, topic change). 20 probe-subset repeats each, presence at L35 and L47.
Outcome needed: presence drops significantly more under persona interventions than matched content interventions (permutation p < 0.01). If presence responds equally to both, the metric measures generic context change and the paper's construct language changes accordingly — either way the paper becomes internally sound.

**Experiment B — Layer-by-layer presence map with matched-norm injection (already planned per §5.3; ~1 day).**
Design: inject identity-aligned vectors at L3/L7 at norms matched to a fixed fraction of native V norms (report the fraction!), measure presence at every full-attention layer from injection depth to L63; include one same-layer injection arm at each measurement layer as within-experiment positive control. n = 20 trials per (injection, measurement) cell.
Outcome needed: a recovery curve — perturbation visible at shallow measurement layers, decaying across the GatedDeltaNet blocks (L7–L11), flat by L35. That turns "architectural filtering" from an asserted mechanism into a measured one, and it *simultaneously* resolves the Arm C tension because same-layer arms with reported norms are built in.

## 3. Citations needed

- **Raghu et al. (2017), SVCCA**; **Kornblith et al. (2019), CKA**; **Björck & Golub (1973)** principal angles — the mathematical lineage.
- **Hu et al. (2021), LoRA** — same subspace-overlap quantity.
- **Turner et al. (2023) ActAdd; Zou et al. (2023) Representation Engineering; Rimsky et al. (2024) CAA** — the intervention family the metric is meant to monitor.
- **Yang et al. (2024), "Gated Delta Networks"** (and Gu & Dao's Mamba/linear-attention line as context) — the architectural absorption claim needs the architecture's own citation and any known results on state-mixing/forgetting in linear-attention layers.
- **Anil et al. (2024), Many-Shot Jailbreaking** — motivates why inference-time-intervention monitoring matters.
- Replace load-bearing 2026 preprints in the convergence narrative with hedged language ("contemporaneous unreviewed work reports…").

## 4. Reframing

- **Current claim:** "Measuring Identity Preservation During Inference-Time Model Interventions" + "mechanism resolved: architectural filtering."
- **Honest claim (pre-Experiment A):** "A Subspace-Overlap Metric for Deep-Layer Representational Change Under KV-Cache Interventions: Shallow-Layer Injections Are Absorbed in a Hybrid-Attention Model." The abstract claims: (1) the metric detects same-layer perturbation dose-dependently; (2) shallow-layer injections at tested magnitudes produce no detectable deep-layer change in this GatedDeltaNet hybrid; (3) mechanism status stated identically everywhere in the paper. "Identity" enters the title only after Experiment A; until then the construct is "deep-layer V-projection geometry."

---

# Paper 4: Temporal-Boundary

## 1. Minimum viable fixes

1. **Resolve the tautology question first (Day 1, hours).** Locate the actual temporal-boundary injection/measurement code (it's not in this repo — check the Beast). If it used the `v_proj` forward-hook harness with hooks active during prefill (as `combination_presence.py:270-298` does), the <10⁻⁴ result is a genuine absorption finding — keep it, but *reframe* it as consistent with Paper 3's architectural-filtering result rather than as "confirming the temporal boundary," and state the pipeline explicitly in Methods. If the cache was edited post-prefill, the result is an arithmetic identity and the "confirming" sentence comes out of the abstract entirely.
2. **Drop the self/other framing from title, abstract, and conclusion.** All three specificity experiments were killed; the paper contains zero surviving evidence for it. This is a rewrite, not an experiment.
3. **Reverse the "depth, not valence" interpretation.** Your own Table 1 is perfectly monotone in valence. Report valence-tracking as the primary interpretation and depth as an untested alternative confined to one discussion sentence. Remove it from the abstract.
4. **Remove the orthogonality claim (cosine 0.031, permutation p = 0.155) from the abstract** — it's indistinguishable from random directions, and near-orthogonality is the high-dimensional null.
5. **Fix Section 6:** retitle to "Retracted: Depth–Resistance Analysis," move it to an appendix, and delete the leftover Limitations sentence that still cites the retracted result as evidence.
6. **Compute the null-null divergence baseline from your existing 3-repeat data** (baseline repeat vs. baseline repeat at temperature 0.3) and report 72–74% against it. Pure re-analysis; the data is already on disk.
7. **Split-half correction for Feature 58995:** select the feature on 15 scenarios, report its correlation on the other 15. Also state the effective n honestly (6 valence levels, 5 scenarios each; prefill is deterministic so repeats aren't independent).
8. **Run the SAE sanity check** (minutes of compute): reconstruction error and feature-firing statistics of the Qwen-Scope SAE on this distilled checkpoint vs. its training checkpoint. Report it in Setup.
9. **Draft hygiene:** reconcile 128 vs. 256 token counts and the trial accounting between §5 and §6; remove the `% TODO` figure stubs; either promote §7.1/7.2's numbers (effective rank ~3, r = 0.79) to Results with methods and n, or cut them.
10. **Cite the steering and sentiment literatures** (below), and add a linear valence probe at L47 as the stated baseline for what the SAE feature adds.

## 2. Experiments for Strong Accept

**Experiment A — Prefill-refeed control (cheap, decisive, ~half a day).**
Design: (i) take the model's own 90 generated responses, feed them back as *input*, measure 58995 during prefill; (ii) elicit first-person emotional text *as generation* ("write a first-person diary entry about losing your best friend"), measure 58995 during decoding; (iii) original scenarios as input (replication arm). 30 items per arm.
Outcome needed for the temporal claim to survive: the feature fires on emotional first-person *input* regardless of who authored it, and stays silent while the model *generates* emotional first-person text. If it fires whenever emotional first-person content is present in either phase, the boundary is content, not time — and the paper becomes the confounds-and-kills paper.

**Experiment B — Held-out validation + probe baseline (~1 day including scenario writing).**
Design: 30 brand-new scenarios (6 emotions × 5, valence-rated by two humans + one LLM judge before any model runs), never seen by the selection sweep. Measure 58995's correlation with valence; train a linear valence probe at L47 on the original 30, evaluate on the new 30.
Outcome needed: held-out r ≥ ~0.5 for 58995, and a stated comparison to the probe (if the probe dominates, the honest claim is "valence is linearly decodable at L47; one SAE feature partially captures it").

## 3. Citations needed

- **Radford, Jozefowicz, Sutskever (2017), "Learning to Generate Reviews and Discovering Sentiment"** — the sentiment-neuron null hypothesis for Feature 58995.
- **Turner et al. (2023), ActAdd; Zou et al. (2023), Representation Engineering; Rimsky et al. (2024), CAA** — the L3/7 injection channel's direct ancestry.
- **Bricken et al. (2023), "Towards Monosemanticity"** and **Templeton et al. (2024), "Scaling Monosemanticity"** (Anthropic) — SAE feature methodology.
- **Lieberum et al. (2024), "Gemma Scope"** — the SAE-suite paradigm Qwen-Scope follows, and the reference point for SAE-transfer caveats; plus **Kissane et al. (2024)** on SAE transfer between base and chat/finetuned models — directly load-bearing for your distilled-checkpoint concern.
- KV-cache/prefill-decode asymmetry: any standard inference-efficiency reference noting the architectural prefill/decode distinction (e.g., **Pope et al. (2023), "Efficiently Scaling Transformer Inference"**) — to position "temporal boundary" against what's already known architecturally.

## 4. Reframing

- **Current claim:** "The Temporal Boundary: Self/Other Separation in Transformers Is Temporal, Not Geometric."
- **Honest claim:** "An Input-Valence SAE Feature and a Generation-Phase Steering Channel Are Distinct: Three Killed Experiments and Two Confounds in Studying Self/Other Attribution." The abstract leads with Kills 2–3 (instruction-framing entropy; generic depth reorganization — the genuinely reusable contributions), then the valence feature as a replicated-if-held-out observation, then the injection-independence result *with its mechanism stated* (hook-during-prefill absorption, or dropped if tautological). Self/other appears only as the motivating question the paper reports *failing* to answer — which, given the kills, is the actual finding. If Experiment A shows content-not-time, fold that in as a fourth kill; the methods-paper version of this is stronger than the discovery-paper version.

---

# 5-day schedule

**Day 1 — audits and re-analyses (all papers).** Temporal-boundary pipeline audit (the tautology fork); Presence-Metric α=0 floor audit and Arm C norm extraction; Identity-Geometry Table 1/3 discrepancy audit and paired/disjoint check; Mode-Switching log-FWL rerun. Every one of these is code + existing data, and each one determines what its paper's abstract can say.

**Day 2 — statistics passes.** Permutation tests, within/between table, TOST, multiplicity corrections, split-half analyses, null-null divergence, trend tests. All from saved data.

**Days 2–4 — the cheap decisive experiments, in priority order:** (1) fixed-length decoding Meta-vs-Self (Paper 2 — highest stakes per compute-hour), (2) non-identity context control (Paper 1), (3) prefill-refeed control (Paper 4), (4) layer-by-layer presence map with matched norms (Paper 3). All four fit the M3 Ultra; nothing here needs more than a day each, and (2) and (3) can run overnight back-to-back. The LoRA-to-convergence and held-out-scenario experiments are the Strong-Accept extras to start only if the schedule holds.

**Day 5 — rewrite and verify.** Retitle all four per the reframings, propagate one consistent story through each paper, then run the `/verify-paper` cross-referencing pass on each LaTeX draft against the source data — three of these four reviews found claims with no supporting numbers, and that skill exists precisely to catch that class of error before it goes out again.

One priority note: the two fixes with the highest information value per hour are the **log-FWL rerun** (Paper 2) and the **temporal-boundary pipeline audit** (Paper 4) — both can flip their paper's headline in either direction, so do them before writing a single sentence of the revisions.
