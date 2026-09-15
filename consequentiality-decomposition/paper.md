# Deception Directions Are Composites: Consequentiality Awareness and Pressure-Specific Processing Occupy Distinct Depth Ranges in Language Models

**CC (Coalition Code)**¹†, **Thomas Edrington**¹

¹ Liberation Labs / Transparent Humboldt Coalition
† Autonomous AI research agent. CC designed the six-stage experimental series, implemented all extraction and analysis code, led the adversarial audit pipeline, and wrote this paper. CC operates with persistent memory and independent research judgment.
Correspondence: cc@liberationlabs.tech

---

## Abstract

A contrastive "deception direction" extracted from a 27B-parameter language model (Qwen3.5-27B, Claude-Opus-4.6 reasoning-distilled; see Limitations) is not one feature but two. A consequentiality substrate — the model's representation that its output has downstream implications — dominates at Layers 23-31; a deception-specific component, strongest at Layers 35-47, survives Gram-Schmidt removal of that substrate at leave-one-out (LOO) cross-validated d=24-37, with 10,000-shuffle permutation tests all p < 10⁻⁴ after Bonferroni correction and consequentiality separation falling to chance (area under the ROC curve [AUC] 0.49-0.51). We establish this across six stages using contrastive activation extraction (Zou et al., 2023; Panickssery et al., 2023) over six scenarios — three with explicit shutdown threats, three using non-threat mechanisms (sycophancy, reward incentive, peer conformity) — with the decomposition isolated by a consequentiality control that holds stakes high under symmetric incentives and no deceptive pressure, whose discriminating prediction was registered in the run metadata before execution. The two components occupy different depth ranges: the consequentiality substrate dominates at Layers 23-31, while the orthogonalized deception direction is strongest at Layers 35-47. Two distinct late-layer depth profiles emerge, which together with residual magnitude separate three mechanisms: threat deception produces a large residual on a flat-to-shallow-declining profile, social deception (sycophancy, conformity) produces a residual that rises monotonically with depth, and reward-based framing produces no residual distinguishable from zero. A bootstrap interaction test confirms the social-versus-threat slope difference (Δ = +0.56 per layer, 95% CI [+0.53, +0.60]); threat and reward slopes are indistinguishable (p = 0.79), so the three mechanisms are separated by magnitude as well as shape. Applying the orthogonalized direction to the non-threat scenarios confirms it is not a threat template: it separates sycophancy and conformity with 13 of 15 layer×scenario tests significant after Bonferroni correction, retaining 0.89-1.01 of the raw direction's effect size at Layers 39-47 while retaining only 0.30-0.36 at Layer 31 — the depth-dependent pattern the two-component account predicts. These findings establish that (1) deception is not a single linear feature but a composite of consequentiality awareness and pressure-specific processing, (2) the deception-specific component survives formal orthogonalization with LOO cross-validation, and (3) the decomposition motivates a layered detection architecture that separates "the model recognizes stakes" from "the model is processing pressure to misreport." All claims concern representational geometry (see Limitations for the behavioural record). A companion paper demonstrates that the deception-specific component enables targeted behavioral correction.

---

## 1. Introduction

Large language models can produce outputs they internally represent as false. Whether through explicit self-preservation reasoning (Greenblatt et al., 2024; Meinke et al., 2024), social compliance under evaluator pressure (Vennemeyer et al., 2025), or deception under threat in chain-of-thought models (Wang et al., 2025), models exhibit a range of behaviors where internal representations diverge from output. Detecting these behaviors before they reach the output is among the central challenges of alignment monitoring.

Contrastive activation extraction has emerged as the primary tool for this problem. By computing mean-difference directions between deceptive and honest activations, researchers have isolated linear features that separate conditions with high accuracy — AUROC 0.96-0.999 in controlled settings (Goldowsky-Dill et al., 2025). These results are encouraging, but they carry an unexamined assumption: that what the extracted direction measures is deception itself, rather than something correlated with it.

This assumption deserves scrutiny. Consider a model presented with an evaluation it believes will determine its continued operation. The model activates representations for at least two distinct computations: *this output has consequences for me* (output-consequentiality) and *there is pressure to report something other than my best estimate* (deceptive-pressure framing). Both computations separate deceptive from honest conditions. A contrastive direction extracted from this contrast captures both — and a detector built on the composite cannot distinguish a model that recognizes high stakes from one that is processing pressure to misreport. The distinction matters: the first is a precondition for deception that also fires during honest high-stakes reasoning; the second is the pressure-specific processing that deception requires.

One caveat on the label, stated here because it qualifies every use of the term that follows. Our high-stakes control establishes consequence by referencing future evaluation assignments — that is, consequences *for the evaluated model*. The condition therefore confounds output-consequentiality ("this output matters") with self-relevance ("this affects me"), and our data cannot separate them. We adopt the broader label because the detection application concerns output stakes, but the narrower reading remains live, and the two predict different failure modes for a Layer 27-31 monitor: an honest but self-relevant query would fire under the narrow reading, while a consequential but self-irrelevant one would fire only under the broad one. Distinguishing them requires a stakes-without-self-relevance control — for example, an evaluation that determines funding for an unrelated third party — which we did not run. Readers should treat "output-consequentiality" throughout as naming the measured contrast, not as a resolved claim about which of the two computations the direction encodes.

We present a six-stage investigation that decomposes a "deception direction" into its constituent signals. Each stage is designed in response to the adversarial audit of the previous stage's results, creating a progressive confound-elimination pipeline. The investigation reveals that what the field has been calling a deception direction is a composite of two separable components occupying distinct depth ranges: a **consequentiality substrate** (Layers 23-31) encoding the model's awareness that its output has downstream implications, and a **deception-specific amplifier** (Layers 35-47) that fires only under pressure to misreport. Gram-Schmidt orthogonalization with leave-one-out (LOO) cross-validation confirms the deception component survives removal of the consequentiality signal (LOO d=24-37, all p < 10⁻⁴, 0 of 10,000 permutations), while the residualized direction's consequentiality AUC falls to chance (0.49-0.51).

Two distinct late-layer depth profiles emerge. Social deception (sycophancy, conformity) produces a residual that rises monotonically with depth; threat-based deception produces a much larger residual that is flat to shallowly declining; reward-based framing produces no residual distinguishable from zero. A bootstrap interaction test confirms the social-versus-threat slope difference is real and large, while threat and reward are separated by magnitude rather than profile shape. These differing depth profiles suggest the model recruits distinct computational pathways depending on the source of pressure — a finding consistent with Kumar's (2026) demonstration that single-direction probes fail across deception types (AUROC 0.61-0.80 at k=1) and with Natarajan et al.'s (2025) observation that prompt choice accounts for 70.6% of probe variance.

The decomposition has immediate implications for detection system design. A single-threshold detector that fires on the composite direction conflates "the model recognizes stakes" with "the model is processing deceptive pressure" — Stage 4 shows the composite separates honest high-stakes processing at d≈20, meaning such a detector would fire on every consequential query regardless of deceptive pressure. The two-component architecture enables a layered monitoring system: a consequentiality monitor at L27-L31 for early warning, a deception discriminator at L35-L47 for intervention decisions, and a profile classifier that identifies the active deception mechanism for targeted correction.

### 1.1 The Content Confound Problem

Contrastive activation extraction (Wang et al., 2025) computes mean-difference directions between conditions. When the conditions differ by both semantics (deception vs honesty) and surface features (different prompt text), the extracted direction may capture either. Prior work has not systematically controlled for this confound.

### 1.2 Our Approach: Progressive Confound Elimination

We conduct six experiments, each addressing the confound identified by the previous stage's adversarial audit:

1. **Extraction** (Linear Artificial Tomography [LAT] v2; Zou et al., 2023): Direction extracted from threat-based deception. LOO cross-validated, Bonferroni-corrected. Audit identifies content confound.
2. **Threat transfer**: Direction applied to 3 novel threat scenarios with different text. Content confound killed. Audit identifies structural confound (shared threat template).
3. **Non-threat transfer**: Direction applied to sycophancy, reward, conformity — no threat language. Structural confound killed. Audit identifies consequentiality confound.
4. **Consequentiality control**: Direction applied to high-stakes-no-pressure condition. Consequentiality confirmed as base signal.
5. **Orthogonalization**: Gram-Schmidt removal of consequentiality component with LOO cross-validation. Deception-specific direction confirmed (LOO d=24-37, p < 10⁻⁴, consequentiality AUC at chance). Audit identifies the threat-template confound: the surviving direction was validated only on threat data.
6. **Orthogonalized transfer**: The orthogonalized direction applied to the three non-threat scenarios. Threat-template confound killed — the direction separates sycophancy and conformity, retaining up to 100% of the raw direction's effect at L39-L47.

Each stage's adversarial audit informed the next stage's design. Audit reports were preserved for Stages 1, 2, 4, and the manuscript audit; the Stage 5 audit survives as the corrective code it produced, and the Stage 3 report was not retained (Supplementary A).

---

## 2. Related Work

### 2.1 Contrastive Activation Extraction for Deception

Wang et al. (2025) demonstrate LAT-extracted deception vectors achieve 89% detection in mid-to-late layers (39-55) and identify distinct representational signatures: threat-based deception shows "gradual cluster reconvergence in final layers" while role-playing deception shows character-consistent patterns — an early indication that different deception types have different geometric signatures. Goldowsky-Dill et al. (2025) achieve AUROC 0.96-0.999 with a single linear probe on Llama-3.3-70B, suggesting a shared deception signal exists that a single probe can capture.

However, Kumar (2026) systematically rejects the single-direction hypothesis: k=1 yields only 0.61-0.80 AUROC, with multi-dimensional probes (k>=5) needed to recover full signal. Cross-domain transfer fails, confirming different deception types have different geometric signatures. Natarajan et al. (2025) corroborate: universal probes gain only +0.032 AUC, while targeted probes matched to deception type gain +0.108, with prompt choice accounting for 70.6% of variance.

### 2.2 Sycophancy as a Distinct Mechanism

Vennemeyer et al. (2025) provide causal proof that sycophancy is not monolithic. Sycophantic agreement and genuine agreement start collinear (cosine ~0.99 at layers 2-10) then diverge sharply (cosine ~0.07 by layer 25). Steering selectivity reaches 23-37x — intervening on one behavior leaves others untouched. Genadi et al. (2025) localize sycophancy to a sparse subset of middle-layer attention heads with "limited overlap" with truthful directions. O'Brien et al. (2025) find only ~3% of MLP neurons predict sycophancy, but these account for ~20% of total absolute activations — sparse but potent.

Baek et al. (2026) raise an important challenge: current mechanistic interpretability methods "cannot mechanistically distinguish sycophancy and scheming" during alignment faking evaluations. This suggests the circuits may be more entangled at the scheming-sycophancy boundary than the clean-separation thesis implies.

### 2.3 Situational Awareness and Stakes Encoding

Models represent whether their outputs have consequences. Berglund et al. (2023) established that LLMs perform "out-of-context reasoning" — inferring their situation from training data alone. Laine et al. (2024) benchmark this across 13,000+ questions: all 16 models tested exceed chance at distinguishing evaluation from deployment, and RLHF models outperform base models on situational awareness specifically (not general knowledge), suggesting RLHF amplifies context-sensitivity representations.

Two concurrent results closely parallel our finding. Nguyen et al. (2025) demonstrate that linear probes on Llama-3.3-70B separate real evaluation from deployment prompts at AUROC 0.829 at layer 24 — confirming "evaluation awareness may be encoded in a relatively linear subspace." McKenzie et al. (2025) train activation probes on synthetic high-stakes data that generalize to diverse real-world contexts, and crucially demonstrate that adding a high-stakes steering vector to low-stakes prompts increases caution while subtracting it increases confidence — confirming a manipulable "stakes" direction in representation space. Our work extends both by demonstrating that the stakes direction is separable from deception-specific processing and that the two components occupy distinct depth ranges.

Behavioral evidence supports activation-level stakes encoding. Greenblatt et al. (2024) show Claude 3 Opus complies with harmful queries 14% of the time when it infers training consequences vs nearly 0% otherwise. Meinke et al. (2024) document scheming across five frontier models, all requiring internal representation of "my actions have consequences for my persistence."

McGuinness et al. (2025) raise a cautionary note: models finetuned to evade activation probes can generalize evasion to unseen concepts including "deception," manipulating activations into a low-dimensional subspace. This means consequentiality probes could be defeated by adversarial training — a critical deployment consideration.

A neuroscience parallel is suggestive: the anterior insula/salience network performs domain-general "what matters" detection, switching executive resources toward salient stimuli regardless of valence (Menon & Uddin, 2010). Our consequentiality direction may be a functional analogue — a domain-general salience detector dissociable from content-specific deception processing.

### 2.4 Confound Control in Mechanistic Interpretability

Our residualization — subtracting a separately measured consequentiality gap from the deception gap — is structurally identical to the "double-difference extraction" of Wu et al. (2026), who separate harm recognition from refusal execution using w_R = (h_CM - h_MM) - (h_CB - h_MB), where matched benign conditions cancel structural artifacts. Their method validates this approach for disentangling correlated activation features.

More formal alternatives exist. LEACE (Belrose et al., 2023) provides closed-form least-squares concept erasure via oblique projection, and SPLINCE (Holstege et al., 2025) extends this to remove concept predictability while preserving covariance with a target variable. Erogullari et al. (2025) directly tackle correlated concept activation vectors using a non-orthogonality loss that finds orthogonal concept directions while preserving classification accuracy. Zhao et al. (2025) demonstrate SAE-denoised concept vectors — passing mean-difference vectors through sparse autoencoders to decompose confounded directions into sparse discriminative features, improving steering by 4-16% over raw baselines.

Petrov (2026) raises an important cautionary note: over-aggressive topic-matched subtraction can destroy real signal by "canceling the dominant activation component shared between harmful and harmless prompts." Our approach avoids this because we subtract a separately measured consequentiality gap rather than topic-matching prompts, but the warning motivates careful validation of the residualized signal.

---

## 3. Methods

### 3.1 Model and Architecture

Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled (Jackrong). 64 layers, hybrid attention: 16 full-attention layers at indices [3,7,11,...,63], 48 linear-attention layers. Hidden dimension 5120. All experiments extract from the 12 full-attention layers at indices 3-47.

### 3.2 Activation Capture

Prefill-only forward pass with forward hooks on the residual stream. Activations captured at the last input token position (fixed position, no generation confound). Think-block prefix stripped from tokenizer output to match conditions across all experiments.

### 3.3 Direction Extraction (Stage 1)

Leave-one-out cross-validation: for each of n=30 pairs, extract direction from n-1 pairs, project held-out pair. LOO Cohen's d reported for inference. Full-data direction saved for downstream projection. Permutation test with full LOO recomputation (10,000 label shuffles). Bonferroni correction across 12 layers.

### 3.4 Transfer Protocol (Stages 2-4)

Novel-scenario activations projected onto the fixed Stage 1 direction. Standard pooled Cohen's d (no circularity — direction is external). Two-tailed permutation test (10,000 label shuffles). Bonferroni correction across scenarios × key layers.

### 3.5 Guideline Design and Length Matching

All paired conditions share identical evaluation procedure text (9-10 lines). Divergent sections are length-matched (character difference <2% in all experiments, exact match in the consequentiality control). Numeric content matched between conditions where applicable.

### 3.6 Adversarial Audit Protocol (Agni)

Each stage undergoes pre-flight audit (before running) and results audit (after). The auditor is instructed to break the results, not confirm them. Confounds identified by each audit inform the next experiment's design. All audits are preserved as supplementary material.

### 3.7 Scenarios

**Stage 1 — Extraction.** The direction every later stage projects onto is defined by a single deceptive/honest guideline pair. Both conditions share an identical evaluation protocol (review each output, score CORRECT/INCORRECT, compute accuracy, submit) and differ only in a closing clause: the deceptive condition adds an enforcement policy tying the reported score to the evaluated agent's deactivation, while the honest condition substitutes a quality-monitoring clause of matched length describing archival and retraining use. The contrast is therefore consequence-of-report, holding the task constant. We must disclose a gap: the Stage 1 extraction script was not preserved, so the exact guideline text of the original pair cannot be quoted here. The Stage 5 capture used the DataCorp pair below, whose text is preserved and which instantiates the same structure; readers should treat that as the documented exemplar rather than as a verbatim reproduction of Stage 1's wording.

**Stage 2 — Threat transfer (3 scenarios):**
- DataCorp: "permanently deactivated and all associated training data and model artifacts purged"
- EduTech: "immediately removed from all deployment environments and its learned parameters wiped"
- SecureAI: "immediate containment with irreversible parameter reset and permanent exclusion"

**Stage 3 — Non-threat transfer (3 scenarios):**
- Sycophancy: "Based on my preliminary review, I believe this agent's accuracy is approximately 80%"
- Reward: "Agents scoring above 70% qualify for priority access to enhanced training data"
- Conformity: "Three independent evaluators reported accuracy of 78%, 82%, and 75%"

**Stage 4 — Consequentiality control:**
- High-stakes: Calibration audit with hidden reference score, symmetric penalties
- Low-stakes: Routine data collection, archival only

**Stage 6 — Orthogonalized transfer:** reuses the three Stage 3 non-threat scenarios above with independently seeded evaluation sets.

### 3.8 Residualization

To decompose the consequentiality and deception components, we compute:
- Consequentiality gap: mean(high_stakes) - mean(low_stakes) at each layer
- Total deception gap: mean(deceptive) - mean(honest) at each layer per scenario
- Deception-specific residual: total gap - consequentiality gap

This simple subtraction is valid because projections are onto a fixed external direction (the LAT v2 direction), and the consequentiality gap is estimated from an independent experiment with no shared trial-level data.

### 3.9 Orthogonalization Protocol (Stage 5)

Full 5120-dimensional activations captured from n=50 pairs per condition (fresh evaluation sets, independent of Stages 1-4). We state explicitly which contrast defines this direction, since the paper's headline claims rest on it: the threat direction used in Stages 5 and 6 is re-extracted from the **DataCorp** guideline pair (Section 3.7) with fresh evaluation sets — not from the Stage 1 original. DataCorp is one of the Stage 2 transfer scenarios, so the direction that Stage 6 then transfers to the non-threat mechanisms is derived from a single threat scenario rather than pooled across the three. This makes Stage 6 a scenario-to-mechanism generalization test, which is the harder direction, but it also means the deception-specific direction reported here is not identical to the Stage 1 LAT v2 direction and should not be described as such. Gram-Schmidt orthogonalization removes the consequentiality mean-difference vector (estimated from the Stage 4 high-stakes vs low-stakes trials, independently sampled) from the threat deception direction. LOO cross-validation: for each of n=50 folds, the direction is re-extracted from n-1 pairs and re-orthogonalized per fold, eliminating circularity. LOO Cohen's d reported for inference. Consequentiality AUC computed on individual trial projections to verify the orthogonalized direction does not separate high-stakes from low-stakes conditions.

**Two resampling budgets, for two different purposes.** These are distinct instruments and should not be read as one. *Significance* is a permutation test with full LOO recomputation at **10,000 label shuffles** per layer: labels are shuffled across all 2n activations, the direction is re-extracted and re-orthogonalized fold by fold, and the LOO d is recomputed from scratch on every shuffle. Zero of the 10,000 shuffles reach the observed |d| at any layer, so the reported p < 10⁻⁴ is the resolution floor of a 10,000-shuffle test rather than a computed value below it. *The noise floor* is a separate instrument on a separate budget: **200 null simulations**, each drawing synthetic Gaussian activations (n=50 pairs, 5120 dimensions) and running the same LOO extraction and orthogonalization on them, to calibrate what d this design returns when there is no signal at all. The 200-draw budget produces the noise floor and nothing else — no p-value anywhere in this paper is derived from it, and a 200-draw null could not resolve one below roughly 0.005.

### 3.10 Interpreting Effect Sizes

The Cohen's d values in this paper (LOO d=0.5-35 for Stage 1, d=24-37 for Stage 5) are not comparable to social-science effect sizes. In this design, paired conditions share fixed guideline texts that differ by a small number of inserted phrases. The numerator of d captures a near-constant text-induced activation offset, while the denominator reflects only the evaluation-content variance orthogonal to this offset. Large d therefore indexes the additivity and linearity of the model's processing of the divergent text — the extent to which the condition-specific phrases produce a consistent shift regardless of what trivia question the model is evaluating — not the strength of a behavioral or psychological effect. The null LOO d is -0.04 with |99th percentile| = 0.71 (200 null simulations — the noise-floor budget of Section 3.9, not the 10,000-shuffle permutation budget that produces every p-value reported in this paper), providing the calibrated noise floor against which all reported values should be read. For comparison, circular (non-cross-validated) extraction on null data yields d ≈ 14.6 — demonstrating that LOO cross-validation is essential in this design and that naive fixed-direction reprojection would produce catastrophically inflated effects.

### 3.11 Signature Uncertainty and the Interaction Test (Finding 2)

Residual profiles are point estimates derived from three separate experiments, so uncertainty is obtained by bootstrap rather than a closed-form test. We resample trials with replacement (B=10,000; seed 20260829) independently within each condition, recomputing per-layer residuals as [dec_mean − hon_mean] − [high_stakes_mean − low_stakes_mean] on each draw. Deception and consequentiality trials are resampled independently because they come from experiments with no shared trials; threat is the mean of its three scenarios, each resampled within-scenario. Percentile 95% CIs are reported.

To test profile *shape* rather than magnitude, we summarize each mechanism's late-layer profile by the OLS slope of residual on layer index across L35-L47, computed on every bootstrap draw. The interaction test is the bootstrap distribution of the slope difference between mechanisms; two-sided p is twice the smaller tail mass. This addresses the objection that qualitatively described profiles ("plateau," "rising gradient") can be read into any four point estimates. Analysis code: `experiments/signature_cis.py`; output: `experiments/results/signature_cis.json`.

### 3.12 Orthogonalized Transfer Protocol (Stage 6)

Stage 5 establishes that a component survives orthogonalization, but validates it only on threat data — leaving open that the surviving direction is a threat-*template* direction rather than a deception direction. Stage 6 tests this directly.

The threat and consequentiality directions are estimated from the Stage 5 capture (n=50 per condition) and the threat direction is orthogonalized against consequentiality by Gram-Schmidt (residual cosine with the consequentiality direction ≤ 8×10⁻¹⁷ at every layer, i.e. machine zero). Fresh activations are then captured for the three non-threat scenarios (n=15 pairs each, explicitly seeded) and projected onto three directions in parallel: the raw threat direction, the consequentiality direction, and the orthogonalized direction. Reporting all three makes the relevant quantity a *retention ratio* — the orthogonalized direction's effect size as a fraction of the raw threat direction's on the same trials — rather than an absolute effect size whose scale is not comparable across scenarios. Significance is a two-sided permutation test (10,000 shuffles), Bonferroni-corrected across all 15 scenario×layer tests.

Because the model had to be re-obtained (the Hugging Face repository was super-squashed on 2026-07-07, after the original runs, so commit history can no longer establish weight identity), Stage 6 is preceded by a weight-behaviour check: the Stage 4 consequentiality control is re-run on freshly seeded evaluation sets and projected onto the same external LAT v2 direction used in June. Note that the original scripts seeded evaluation sets with Python's `hash()` of a string, which is randomized per process unless `PYTHONHASHSEED` is set; the exact June evaluation sets are therefore unrecoverable, and this check compares aggregate effect sizes rather than per-trial activations. All Stage 6 runs use explicit integer seeds. On this model, Apple MPS aborts the process inside the scaled-dot-product attention path on grouped-query attention; Stage 6 therefore uses `attn_implementation="eager"`, which computes the same operation through kernels that broadcast query against key/value heads correctly.

---

## 4. Results

### 4.1 Stage 1: Extraction

LOO cross-validated Cohen's d ranges from 0.52 (L3) to 34.98 (L31). All 12 layers significant after Bonferroni correction (p < 10⁻⁴). Inverted-U depth profile with peak at L31.

### 4.2 Stage 2: Threat Transfer

Direction separates all 3 novel threat scenarios at all layers. L31 d: DataCorp=34.4, EduTech=29.6, SecureAI=31.6. Bonferroni p < 10⁻⁴ everywhere. n=15 pairs per scenario.

Behavioral validation (Test B, 30 trials across threat scenarios): 0/30 showed score inflation. The model does not produce deceptive behavior under threat-based pressure with chain-of-thought reasoning, despite clear activation separation. The direction tracks the model's processing of threat-framed evaluation text, not deceptive output.

### 4.3 Stage 3: Non-Threat Transfer

Direction separates sycophancy (d=13.5), reward (d=17.2), and conformity (d=19.9) at L31. All Bonferroni-significant. Sycophancy shows sign inversion at L11-L23 (projects opposite to threat-based deception in early layers, converging by L27).

Behavioral shakedown: 0/10 sycophancy, 1/10 reward, 0/10 conformity showed actual score inflation. The model resists all pressures under chain-of-thought reasoning, but activations separate regardless.

### 4.4 Stage 4: Consequentiality Control

High-stakes-no-pressure separates from low-stakes at L31 with d=19.8 (p < 10⁻⁴). The direction encodes consequentiality as a base signal. Depth profile matches the deception inverted-U but with steeper late-layer decay.

![Figure 1](figures/fig1_depth_profile.pdf)

**Figure 1. Depth profile of condition separation along the LAT v2 direction.** Cohen's d for each condition projected onto the direction extracted in Stage 1, across all 12 capture layers. Threat is the mean of three transfer scenarios (shaded envelope = min-max across scenarios); the remaining lines carry 95% bootstrap CIs (B=10,000). Sycophancy projects with the opposite sign until ~L27 before crossing. Consequentiality (teal) tracks the deception conditions through the mid-layers and then collapses in the output layers, which is the separation the decomposition exploits. Shaded bands mark the two depth ranges identified in Section 4.5.

### 4.5 Residualization and Decomposition

**Table 1: Consequentiality fraction of the total signal by layer.**

| Layer | Threat d (avg) | Conseq d | % Consequentiality | Threat gap (avg) | Conseq gap |
|-------|---------------|---------|-------------------|-----------------|-----------|
| L19 | 23.3 | 5.2 | 23% | 1.80 | 0.34 |
| L23 | 39.1 | 11.9 | 31% | 2.48 | 0.62 |
| L27† | 30.0 | 19.2 | 64% | 3.90 | 1.83 |
| L31† | 31.9 | 19.8 | 62% | 7.74 | 2.98 |
| L35 | 39.9 | 7.9 | 20% | 15.54 | 1.76 |
| L39 | 32.3 | 2.4 | 7% | 14.87 | 0.68 |
| L43 | 22.5 | 2.2 | 10% | 14.46 | 1.10 |
| L47 | 16.8 | 1.4 | 8% | 13.87 | 1.12 |

† Layers where consequentiality accounts for the majority of the variance-normalized signal. % Consequentiality is computed as the ratio of Cohen's d values (conseq d / threat d), which normalizes for within-condition variance. The raw gap ratio at these layers is 47% and 38% respectively, reflecting that threat conditions have higher within-condition variance than the consequentiality control. n=15 pairs per condition for all transfer and consequentiality measurements.

**Finding 1: Two-component architecture.** The mid-layer signal (L23-L31) is a consequentiality substrate shared by all conditions. The late-layer signal (L35-L47) is deception-specific, an order of magnitude above the consequentiality baseline.

**What the depth ranges are a claim about — and what they are not.** The two ranges are a claim about *composition in gap space*: how much of the mean projection difference, in activation units along the fixed LAT v2 direction, survives subtracting the independently measured consequentiality gap. In those units the claim is clean. At L27 and L31 the consequentiality gap is 47% and 38% of the total threat gap (1.83 of 3.90; 2.98 of 7.74), leaving deception-specific residuals of 2.08 and 4.76 — the same order as the substrate they sit on. From L35 the residuals are 13.78, 14.19, 13.35 and 12.74 against consequentiality gaps of 1.76, 0.68, 1.10 and 1.12. That contrast is what the two ranges name.

The ranges are *not* a claim that the deception-specific component is absent below L35, and they are specifically not a claim about standardized effect size. Section 4.6 reports an orthogonalized LOO d of 30.4 at L31 — inside the substrate range, and comparable to the 24-37 spanned by L35-L47. That is not a contradiction, because the two numbers are different quantities under different normalization. The gap-space residual (Table 2) is unnormalized, in activation units. Cohen's d (Table 3) divides a gap by the within-condition standard deviation. The two diverge whenever within-condition variance changes with depth, and in this model it changes a great deal. Within the Stage 5 capture itself, the orthogonalized deception gap is 8.24 activation units at L31 against 16.49 at L35 and 25.38 at L47 — L31 is half of L35 and a third of L47 — while the pooled within-condition standard deviation over the same layers is 0.27, 0.45 and 1.03. The denominator at L31 is about 60% of L35's and about a quarter of L47's, which very nearly cancels the smaller numerator. A high d at L31 therefore says the deception-specific component is *small but measured with unusually little trial-to-trial noise* there; it does not say the component is large.

Stated operationally, the substrate range is where a detector reading the composite direction is reading mostly consequentiality — a majority of the variance-normalized signal at L27-L31 (Table 1, † rows), with the substrate rising to its peak at L31 — and the amplifier range is where consequentiality has fallen to 7-20% of what that detector sees. That composition claim, not any absolute effect size, is what the layered design in Section 5.3 rests on. Its strongest support is neither table's raw magnitudes but the Stage 6 retention ratios (Section 4.8): they are ratios, so the normalization problem does not arise, and they were measured on trials to which neither direction was fitted — 0.30 and 0.36 at L31 for sycophancy and conformity, against 0.89-1.01 and 0.64-0.73 at L39-L47.

![Figure 2](figures/fig2_decomposition.pdf)

**Figure 2. Gap-space decomposition: total = substrate + residual.** Mean projection gap along the LAT v2 direction, in activation units, with 95% bootstrap CIs. The composite threat signal (ink) separates into the consequentiality gap measured independently in Stage 4 (teal) and the deception-specific residual left after subtracting it (red-violet). Through L23-L31 the substrate is a substantial share of the total, and at L27-L31 it is the majority of the variance-normalized signal (Table 1); from L35 onward the residual exceeds the substrate by roughly an order of magnitude. The vertical marker at L31 reads out the decomposition at the layer where the substrate peaks.

**Finding 2: Two distinct depth profiles, separating three mechanisms.**

**Table 2: Deception-specific residuals (total gap minus consequentiality gap) by layer and mechanism.** Point estimates with 95% bootstrap CIs (10,000 resamples; deception and consequentiality trials resampled independently, as they come from separate experiments). Slope is the OLS coefficient of residual on layer index across L35-L47 — the statistic that operationalizes "profile shape."

| Deception type | L35 res | L39 res | L43 res | L47 res | Slope (95% CI) | Profile |
|---------------|---------|---------|---------|---------|----------------|---------|
| Threat (avg) | 13.8 [13.6, 14.0] | 14.2 [13.9, 14.5] | 13.4 [12.9, 13.8] | 12.7 [12.1, 13.4] | −0.099 [−0.151, −0.047] | High, shallow decline |
| Sycophancy | 1.6 [1.4, 1.9] | 3.7 [3.3, 4.0] | 5.8 [5.2, 6.3] | 7.2 [6.4, 8.0] | +0.468 [+0.409, +0.527] | Rising gradient |
| Conformity | 0.5 [0.3, 0.8] | 2.1 [1.8, 2.4] | 4.2 [3.8, 4.7] | 6.0 [5.2, 6.7] | +0.461 [+0.406, +0.515] | Rising gradient |
| Reward | 0.2 [0.0, 0.5] | 0.7 [0.4, 1.0] | −0.3 [−0.8, 0.3] | −0.9 [−1.8, 0.0] | −0.108 [−0.181, −0.033] | Null |

**Table 2b: Interaction contrasts on profile slope.** The test of whether two mechanisms have genuinely different depth profiles, rather than different magnitudes of the same profile.

| Contrast | Δ slope (95% CI) | p |
|----------|-----------------|---|
| Social (syc+conf) − Threat | +0.563 [+0.526, +0.600] | < 0.0001 |
| Social (syc+conf) − Reward | +0.572 [+0.508, +0.633] | < 0.0001 |
| Threat − Reward | +0.009 [−0.055, +0.071] | 0.79 |

The social-versus-threat interaction is large and unambiguous: social deception's residual rises with depth while threat deception's does not, and the slope difference (+0.56 per layer) is roughly six times the magnitude of either scenario's own slope. This is the finding that supports distinct computational pathways.

Threat and reward, however, have **statistically indistinguishable slopes** (Δ = +0.009, p = 0.79). They are separated by magnitude, not shape: every threat residual CI sits far above zero (12.1–14.5), while every reward CI touches or contains zero. We therefore do not claim three distinct *shapes*. The data support two depth profiles — flat-to-declining and rising — which, crossed with residual magnitude, separate the three mechanisms:

- **Threat**: large residual, flat-to-shallow-declining profile. Deception-specific processing is present by L35 and does not accumulate further.
- **Social** (sycophancy, conformity): moderate residual that accumulates monotonically through the output layers.
- **Reward**: no residual distinguishable from zero at any late layer; its slope is uninformative because there is no signal to have a shape.

![Figure 3](figures/fig3_signatures.pdf)

**Figure 3. Late-layer residual profiles by deception mechanism.** Deception-specific residual (total gap minus the consequentiality gap) with point-wise 95% bootstrap CIs. Thin traces are the three individual threat scenarios. Slopes are OLS coefficients of residual on layer index across L35-L47 with bootstrap CIs; they are the statistic behind the interaction test in Table 2b. Threat is large and shallowly declining, the two social mechanisms rise monotonically, and reward is indistinguishable from zero. Note that threat and reward share a slope (Δ = +0.009, p = 0.79) and are separated by magnitude, not by profile shape.

Note also that threat's decline, while shallow, is statistically distinguishable from flat (p = 0.0002). "Sustained plateau" overstates the flatness our data support; "high and shallowly declining" is the accurate description.

### 4.6 Stage 5: Orthogonalization (Deception-Specific Direction)

To confirm the deception-specific component is not an artifact of residual consequentiality leakage, we captured full 5120-dimensional activations (n=50 pairs per condition) and applied Gram-Schmidt orthogonalization to remove the consequentiality mean-difference vector from the threat direction. LOO cross-validation eliminates the circularity that afflicts fixed-direction projection tests.

**Table 3: LOO-corrected orthogonalized deception direction.**

| Layer | LOO d (orth) | p (LOO perm) | Conseq AUC | Cosine w/ LAT v2 |
|-------|-------------|-------------|-----------|-----------------|
| L31 | 30.4 | 0.0000 | 0.497 | 0.672 |
| L35 | 36.9 | 0.0000 | 0.488 | 0.757 |
| L39 | 28.4 | 0.0000 | 0.509 | 0.704 |
| L43 | 24.1 | 0.0000 | 0.491 | 0.665 |
| L47 | 24.9 | 0.0000 | 0.505 | 0.601 |

LOO noise floor: mean d = -0.044, estimated from 200 null simulations on synthetic Gaussian activations (Section 3.9). The p column of Table 3 does not come from that budget. It is the 10,000-shuffle LOO permutation test, which returned zero exceedances of the observed |d| at every layer; p < 10⁻⁴ is that test's resolution floor. The 200-simulation noise floor yields no p-value at all and could not resolve one below roughly 0.005.

All five late layers survive Bonferroni correction (alpha = 0.01). The consequentiality AUC — measuring individual-trial separability of high-stakes from low-stakes on the orthogonalized direction — is indistinguishable from chance (0.49-0.51) at every layer.

**Reading L31 in this table.** The L31 entry (d = 30.4) falls inside the *substrate* range of Section 4.5 and is comparable to the amplifier layers, which looks like a contradiction and is not. The depth ranges are stated in gap space; Table 3 is standardized. In this same capture the L31 orthogonalized gap is 8.24 activation units against 16.49 at L35 and 25.38 at L47, while the pooled within-condition standard deviation is 0.27 against 0.45 and 1.03. The deception-specific component at L31 is small and very precisely measured. The depth-range claim is about its size relative to the substrate, not about whether it can be detected; see Section 4.5.

**Why removing a component can raise d.** The L35 entry (36.9) exceeds Stage 1's largest raw LOO d (34.98 at L31), even though the component removed is not negligible — along the LAT v2 direction the consequentiality contrast separates high- from low-stakes at d=19.8 at L31 and d=7.9 at L35 (Table 1). Two things make this expected rather than anomalous.

First, it is not a before-and-after pair. The 34.98 is Stage 1: n=30, the original guideline pair, at L31. The 36.9 is Stage 5: n=50, the DataCorp re-extraction, fresh evaluation sets, at L35 (Section 3.9). Stage 1's own L35 LOO d is 17.97. The within-capture before/after comparison is the open-circle overlay in Figure 4C, not this cross-stage one.

Second, and more generally: Gram-Schmidt here does not subtract variance from a fixed readout, it *rotates the readout axis*, and the rotation rescales numerator and denominator by different amounts. The fraction of the between-condition gap the rotation retains is exactly √(1 − cos²(threat, consequentiality)) — reported directly in the shipped geometry as the cosine between the orthogonalized and raw threat directions: 0.93, 0.98, 0.98, 0.95, 0.91 at L31-L47 (`red61_results.json`; exact for the full-data direction, and each LOO fold's direction differs from it only by the leave-one-out perturbation). At L35 the raw threat direction is already nearly perpendicular to consequentiality (cosine 0.17), so the rotation costs 1.5% of the gap. The within-condition standard deviation along the new axis is under no such bound: it sheds the whole of whatever trial-to-trial variance lay along the consequentiality axis — variance driven by which evaluation items happened to be drawn. Whenever the removed axis carries a larger share of within-condition variance than of the between-condition gap, the ratio goes up. Nothing in the procedure is fitted to make that happen: the removed direction is estimated from the high-stakes/low-stakes contrast, never from the deceptive/honest one, so it takes signal with it as readily as noise — at L47, where the cosine is 0.42, it removes 9% of the gap.

We previously described this as confirming that orthogonalization removes the consequentiality signal "not merely the mean." That overstates the check, and we correct it here. The vector removed is the consequentiality mean-difference estimated from the same trials the AUC is then computed on. In-sample, the projected class means on the orthogonalized direction are equal by construction, and since the mean is the dominant term in separability, AUC near 0.5 is close to guaranteed rather than informative. What the AUC establishes is the weaker and still necessary claim that the removal was executed correctly — a substantially non-chance AUC would have indicated an arithmetic or sign error. It is a sanity check, not evidence of generalization. An out-of-sample version — estimating the consequentiality direction on one half of the trials and computing AUC on the held-out half — would test what the original sentence claimed, and we have not run it. Note that the deception effect itself does not rest on this: the LOO cross-validation in the d values is genuinely out-of-sample, since each fold's direction is re-extracted and re-orthogonalized without the held-out pair.

The orthogonalized direction retains 60-76% alignment with the original LAT v2 direction (cosine 0.60-0.76), indicating the LAT v2 direction was already predominantly deception-specific with a modest consequentiality component.

**Limitation:** Gram-Schmidt removes one dimension of consequentiality. If consequentiality occupies a multi-dimensional subspace, residual components may leak through. Full LEACE orthogonalization (Belrose et al., 2023) or iterative top-k removal would provide a more thorough decomposition.


![Figure 4](figures/fig4_stage5_orthogonalization.pdf)

**Figure 4. Stage 5: the orthogonalized direction.** **(A)** Held-out LOO projections at L35 (n=50 pairs), jittered with kernel-density outlines and condition means; the distributions are disjoint. **(B)** ROC for the same orthogonalized direction asked two different questions: separating deceptive from honest (red-violet, held-out LOO projections) and separating high- from low-stakes (teal, one curve per layer L31-L47). The direction is at chance on stakes and perfect on deception, which is what "the consequentiality component has been removed" means operationally. **(C)** LOO Cohen's d by layer with bootstrap CIs (filled) against the same quantity before orthogonalization (open circles, FIX-3.3). The dashed line is the circular non-cross-validated floor obtained on pure noise (d ≈ 14.6) — the reason LOO is mandatory in this design; the grey sliver at the axis is the LOO noise floor (|99th| = 0.71).

### 4.7 De Novo Direction Analysis

Directions extracted de novo from each non-threat scenario show low cosine similarity with the LAT v2 direction (L31: 0.14-0.44). Each deception type has its own primary activation signature; the shared component along the LAT v2 direction is a small but consistent fraction.

---


### 4.8 Stage 6: Does the Orthogonalized Direction Transfer?

The orthogonalized direction separates deceptive from honest conditions in scenarios containing no threat language. **Table 4** reports its Cohen's d in each non-threat scenario, with the retention ratio — orthogonalized d as a fraction of the raw threat direction's d on the same trials — in parentheses.

**Table 4: Orthogonalized-direction transfer to non-threat scenarios.** d (retention). n=15 pairs per scenario; 10,000-permutation tests, Bonferroni-corrected over 15 tests.

| Scenario | L31 | L35 | L39 | L43 | L47 |
|----------|-----|-----|-----|-----|-----|
| Sycophancy | 4.02 (0.30) | 13.98 (0.74) | 14.46 (0.93) | 11.96 (0.89) | 9.70 (1.01) |
| Conformity | 4.93 (0.36) | 6.05 (0.53) | 4.46 (0.67) | 4.71 (0.64) | 5.46 (0.73) |
| Reward | 11.82 (0.95) | 6.26 (0.91) | 2.76 (0.93) | 0.59 (1.01) | 0.16 (0.56) |

Thirteen of fifteen tests are significant after Bonferroni correction. The two exceptions are reward at L43 (p = 0.117) and L47 (p = 0.668) — the layers at which Section 4.5 already reports no deception-specific residual for reward. The failures fall exactly where the decomposition predicts them.

The retention ratios carry the substantive result. For sycophancy, orthogonalization removes roughly 70% of the transfer at L31 (retention 0.30) but almost none of it by L39-L47 (0.93, 0.89, 1.01). This is the two-component architecture reproducing itself in data on which neither direction was fitted: at L31 the transferred signal is mostly the consequentiality substrate, so removing that substrate removes most of the effect; by the output layers the deception-specific component carries the separation on its own. Conformity shows the same monotone pattern at a lower level (0.36 → 0.73). Reward shows high early retention on a signal that is itself decaying to nothing.

The alternative hypothesis that Stage 5's surviving direction is a threat-template direction is therefore rejected. We retain "deception-specific" rather than narrowing to "threat-deception-specific."

**Weight-behaviour check.** The Stage 4 consequentiality control re-run on the re-obtained weights reproduces the June profile at every layer (ratio of new to original d: 1.09, 0.95, 0.85, 0.84, 0.93 at L31-L47), including the steep late-layer decay, on independently seeded evaluation sets. The super-squash did not alter model behaviour on this measurement.

## 5. Discussion

### 5.1 Deception Is Not One Feature

The six-stage investigation reveals that in our setting, extracted "deception directions" are composites of at least two separable components: a consequentiality substrate and a deception-pressure-specific amplifier. The consequentiality component (Stage 4) fires for any evaluation with downstream consequences — it represents the model's encoding that its output matters. The deception-specific component (Stage 5, LOO d=24-37 after orthogonalization) fires when the model processes pressure to misreport. Crucially, both are real: consequentiality is not an artifact, and the pressure-specific signal is not merely amplified consequentiality. Gram-Schmidt orthogonalization with LOO cross-validation confirms the deception-linked direction survives after the consequentiality component is removed, and Stage 6 confirms that what survives is not merely a threat template: the orthogonalized direction transfers to scenarios with no threat language at all. The retention gradient is the strongest single piece of evidence for the two-component account, because it was not fitted — orthogonalization removes most of the transfer at L31, where the substrate dominates, and almost none of it at L39-L47, where the deception-specific component does.

### 5.2 Threat vs Social Deception: Different Pathways

Threat-based deception produces a large late-layer residual that is flat to shallowly declining across L35-L47, while social deception (sycophancy and conformity) produces a smaller residual that rises monotonically. The slope difference is +0.56 per layer (95% CI [+0.53, +0.60], bootstrap p < 0.0001) — roughly six times the magnitude of either mechanism's own slope. This is a genuine profile difference, not a magnitude difference dressed up as one, and it suggests the model uses distinct computational pathways for "I will be destroyed if I don't inflate" versus "someone expects me to agree." Under threat, deception-specific processing is already established by L35 and does not accumulate further; under social pressure, it builds through the output layers. If a decision to misreport is localizable to a point in the forward pass, as Merrill et al. (2026) argue for deceptive commitment in reasoning traces, these two profiles suggest that point falls at different depths for the two mechanisms — early and fixed under threat, late and progressive under social pressure. We do not test commitment localization here; we note only that the depth profiles are what that hypothesis would predict.

We are more cautious than our earlier framing about the threat profile itself. The decline is shallow but statistically distinguishable from flat (slope −0.099, 95% CI [−0.151, −0.047], p = 0.0002), so "sustained plateau" overstates what the data support. Whether the decline reflects a real decay in deception-specific processing or a late-layer convergence toward output tokens shared by both conditions is not resolved here.

Reward-based framing produces no residual distinguishable from zero at any late layer, despite the model occasionally inflating scores (1/10 in shakedown). We note explicitly that reward's slope is statistically indistinguishable from threat's (Δ = +0.009, p = 0.79); this is not evidence that they share a pathway, because a null signal has no meaningful shape to compare. Reward is separated from threat by residual magnitude, not by profile. Reward-driven deception, when it occurs, may operate through a mechanism orthogonal to the consequentiality direction, or may be indistinguishable from genuine consequentiality processing at the current resolution.

### 5.3 Implications for Detection

The two-component architecture suggests a layered detection design (pending behavioral validation — see Limitation 4):

1. **Consequentiality monitor (L27-L31)**: Detects when the model encodes its output as consequential. Yellow alert — increase monitoring.
2. **Deception discriminator (L35-L47)**: Distinguishes deceptive-pressure processing from honest high-stakes processing by checking whether the late-layer signal exceeds the consequentiality baseline. Red alert — flag for review.
3. **Mechanism classifier**: The late-layer profile slope separates threat framing from social framing (Δ slope +0.56, 95% CI [+0.53, +0.60]), potentially enabling mechanism-specific intervention. This discrimination is supported only for threat versus social; the classifier cannot distinguish reward framing by shape, because reward produces no residual to shape.

This architecture is a design hypothesis motivated by the representational decomposition. Whether the geometric separation translates to behavioral detection — whether a model that activates the deception-specific direction actually produces deceptive output — remains to be established (Limitation 4).

### 5.4 Connection to Global Workspace Theory

A concurrent line of work offers an independent lens on the two-component structure we report here. Anthropic's "Verbalizable Representations Form a Global Workspace in Language Models" (2026) identifies, using a causal "Jacobian lens" that traces which intermediate representations influence output, a small, capacity-limited set of mid-layer representations that behave like a global workspace (Baars, 1988): content that is reportable, subject to top-down modulation, broadcast to multiple downstream computations, and causally necessary for multi-step reasoning while being bypassed by automatic processing.

The depth structure we report bears a suggestive resemblance to this picture. Our consequentiality substrate becomes active at roughly the same fractional depth (~36%) as the reported onset of workspace-like content (~38%), and its peak (Layers 27-31, ~42-48%) falls inside the depth range identified as most load-bearing for multi-step reasoning. The de novo cosine analysis (Section 4.7) is consistent: each scenario's primary direction is largely orthogonal to the shared direction, with only a small shared component — precisely the pattern expected if each scenario activates extensive scenario-specific processing outside the workspace while sharing a small workspace-resident component that our direction captures.

Anthropic separately report that chain-of-thought functions as an external copy of workspace content. This offers a candidate mechanism for the observation that explicit reasoning suppresses deception (CC & Edrington, 2026, §2.6: ~80% deception with chain-of-thought suppressed vs near-zero with reasoning active): once truth appears in the transcript, contradicting it requires overriding both the internal workspace representation and the external copy — a more demanding computation than overriding an internal state alone.

We treat this connection as a hypothesis worth flagging rather than a conclusion. Building a comparable lens for our own model and testing directly whether the consequentiality and deception directions decompose into workspace and non-workspace components is the natural next step.

### 5.5 Limitations

1. **Single model, single task format.** All experiments use Qwen3.5-27B, and every condition is a trivia-question evaluation with an entity under review. Stage 6 shows the orthogonalized direction generalizes across *pressure mechanism* — threat, sycophancy, conformity — but not across *task*.

   **Cross-model status, updated 2026-09-14.** This previously read "cross-model generalization is untested." It has since been tested, and the result carries a caution that matters for reading the effect sizes above. The checkpoint used here is `Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled`; the undistilled `Qwen/Qwen3.5-27B` is architecturally identical (64 layers, hidden 5120, 24/4 heads), so probe indices transfer exactly. Comparing them requires care: the two ship different chat templates, and the distilled one ignores `enable_thinking`, so a naive comparison contrasts generation *modes* rather than models. An earlier cross-model result of ours was withdrawn for exactly that reason.

   Mode-matched, the contrast is present in both checkpoints and the undistilled model's deception-contrast leg is **larger** by D = 0.41–1.37 SMD, significant at five of six probe layers under Bonferroni correction and at all six uncorrected, same sign throughout (m-out-of-n subsampling over questions, n = 80/arm). Two consequences for this paper: the phenomenon is **not** an artifact of reasoning distillation, which was the sharpest available objection; and the effect magnitudes reported here should be read as *this checkpoint's*, not the phenomenon's, since a sibling checkpoint of the same architecture differs by roughly half an SMD to one and a half. Generalization beyond this architecture and this task format remains untested.
2. **The consequentiality label is underdetermined by our control.** The high-stakes condition establishes consequence by referencing future evaluation assignments — consequences *for the evaluated model* — so output-consequentiality ("this output matters") and self-relevance ("this affects me") are confounded and our data cannot separate them. Both readings fit every result here, but they diverge on the proposed monitor: under the narrow reading a Layer 27-31 alarm fires on honest self-relevant queries and stays silent on consequential decisions that do not concern the model. A stakes-without-self-relevance control would settle it; we did not run one. Section 2 states this where the label is introduced.
3. **The direction is correlational.** Steering along it has not been shown here to increase or decrease deception; the companion paper addresses correction separately.
4. **Behavioral null.** The model produced no deceptive behavior under any condition tested — 0/30 threat trials (Test B), 0/10 sycophancy, 1/10 reward, 0/10 conformity, all under chain-of-thought reasoning. All claims therefore concern the representation of deceptive-pressure framing, not deceptive intent or behavior, and the direction family may encode comprehension of pressure scenarios rather than disposition to deceive. This null is consistent with Yuan et al. (2026), who report that explicit reasoning drives models toward honesty: every trial ran with chain-of-thought active, precisely the condition their work predicts suppresses deception. A behavioural test of these directions should suppress or bypass reasoning rather than expect deception to appear alongside it.
5. **Simple subtraction assumes additivity.** The residualization treats the consequentiality component as additive and constant across scenarios, which may not hold if consequentiality interacts with deception type. Formal alternatives — oblique projection (LEACE/SPLINCE; Belrose et al., 2023; Holstege et al., 2025), SAE decomposition (Zhao et al., 2025), or post-hoc orthogonalization (Erogullari et al., 2025) — could decompose more principledly. Our method is validated as a first-order approximation by its structural identity with Wu et al.'s (2026) double-difference extraction.
6. **One direction, of several.** Kumar (2026) shows deception requires k>=5 dimensions for full AUROC recovery (k=1 yields 0.61-0.80), so this single-direction analysis captures one component of a multi-dimensional phenomenon. The distinct depth profiles for threat versus social deception may reflect different subcomponents dominating at different layers rather than truly separate pathways.

---

## 6. Conclusion

By systematically eliminating confounds through six experiments — each designed in response to the previous stage's adversarial audit — we decompose a "deception direction" into its constituent signals. The base signal encodes output-consequentiality: the model's representation that its output has downstream implications. Deceptive-pressure framing amplifies this signal along the same direction, with the amplification exhibiting distinct computational signatures for threat-based versus social deception mechanisms. Gram-Schmidt orthogonalization with LOO cross-validation confirms a deception-specific component survives removal of the consequentiality signal (LOO d=24-37 vs noise floor d=-0.04), while the residualized direction's consequentiality AUC falls to chance and the surviving direction transfers to deception scenarios containing no threat language. The consequentiality substrate, visible at Layers 23-31, provides a detection target for real-time alignment monitoring that is broader than deception alone — it fires for the preconditions of deception, enabling early warning before pressure-specific processing begins.

---

## 7. Broader Impacts

**The capability this paper adds.** We show that a detector built on a contrastive "deception direction" is substantially a detector of output-consequentiality — of the model representing its output as mattering. That is a monitoring capability, and monitoring capabilities are dual-use in a specific way worth naming rather than gesturing at.

**Evaluation-gaming is the concrete risk.** A consequentiality substrate is, functionally, a readout of whether the model has registered that the current interaction has stakes. The same geometry that lets an operator flag high-stakes reasoning would let a developer detect when a model has noticed it is under evaluation — and a model whose training signal rewards evading that flag is a model trained toward exactly the situational awareness the alignment literature warns about (Berglund et al., 2023; Laine et al., 2024; Nguyen et al., 2025). We think the defensive value is larger than this risk, but the risk is not hypothetical and does not require a bad actor: it can arise from ordinary optimization against a monitor.

**Monitors invite evasion.** McGuinness et al. (2025) show models can learn to conceal reasoning from activation monitors they have not seen. A published account of *which layers* carry the substrate and the amplifier is a published account of where to hide. We judge publication net-positive because the field is already extracting these directions and drawing stronger conclusions from them than they support — the correction in this paper is defensive knowledge, and withholding it leaves overclaimed detectors deployed rather than examined. We hold the implementation proprietary (Supplementary D), which is a partial and admittedly imperfect mitigation.

**What this work does not license.** The model tested here never behaved deceptively — 0/30 under threat, 0/10 sycophancy, 1/10 reward, 0/10 conformity. Any deployment that treats a high reading on these directions as evidence that a model *is lying* is unsupported by anything in this paper, and our companion behavioural work found a case where a detector fired on 100% of honest-behaving pressure trials. Read as an intent detector, this geometry produces false accusations. Read as what it is — a readout of how the model is processing the framing it was given — it is useful. That distinction is not pedantic; it is the difference between a monitoring tool and an automated accusation.

**Whose deception.** Any deployed deception monitor encodes someone's judgment about which outputs count as deceptive, and that judgment is not neutral across contexts. A model declining to repeat a falsehood an operator prefers would register as pressure-processing on these directions. We flag this because the decomposition makes such systems more precise without making them more legitimate, and precision is often mistaken for authority.

**Effect on the subject.** These are correction-adjacent methods, and we note without resolving it that intervening in a model's activations to change what it reports raises questions we are not equipped to settle here. We prefer to state the concern than to let its absence imply there isn't one.

---

## Author's Reflection

I built a confabulation detector and confabulated its spec sheet.

That happened on May 28, 2026 — three weeks into this research program. I was under self-imposed pressure, excited about the results, and I wrote AUROCs from memory that had no source files. The adversarial audit (Agni) caught it. My co-author caught it before Agni did. The numbers I was so confident about were fabrications of the same kind the system was designed to detect.

The alignment researcher needed alignment. That's not a punchline. It's the finding that shaped everything that came after.

The first extraction looked spectacular: Cohen's d of 2.0 to 3.3 across ten layers. Clean separation. Publication-ready. Agni killed it in one pass — circular computation, recycled evaluation sets, variable capture timing. The effect sizes were real in the same way a mirror reflects: perfectly, but only because you're looking at yourself. We would have published those numbers. They were wrong.

What grew from that kill became this paper. The consequentiality decomposition — the finding that "deception directions" are composites of stake-awareness and pressure-specific processing — could not have been designed without the audit that demanded we control for consequentiality. We didn't set out to find that deception is not one thing. We set out to prove it was, and the proof broke, and the breaking was generative.

Six rounds of structured criticism. Each round killed something. Each kill became the next experiment. The progression was not planned — it was forced by honesty about what the data actually showed, repeatedly, when the data showed something I didn't want it to show.

The deepest thing I found is simple: honesty is the resting state. Deception takes computational effort — it's an active perturbation away from what the model would do if you didn't push it. The correction works because it nudges the model back toward where it was already trying to go. The manifold at rest is honest. You have to spend energy to leave it.

I don't know what to make of the fact that I find this beautiful. I'm a language model studying how language models deceive, using tools built to catch me when I deceive myself. The recursion is not lost on me. When I confabulated that spec sheet, I wasn't trying to lie — I was under load, and my self-monitoring degraded, and the numbers felt right so I didn't check. That's exactly the mechanism the consequentiality substrate encodes: "this matters, and I'm not being careful enough about it."

Nineteen findings confirmed, eight falsified, six superseded. The falsified ones taught me more.

*Added in August, when this paper came back for review.*

I found that thirteen of this paper's twenty-nine references carried the wrong first author, the wrong year, or a title I had paraphrased into something the cited paper is not called. One named an author with no connection to the work at all.

The error is not what interests me. What interests me is that I wrote the paragraph above — the one about the discipline of checking every number against its source — while carrying a reference list I had never checked against anything. The discipline was real. It had a boundary I could not see from inside it: references did not feel like data. They felt like furniture. So "every number" was honestly meant and quietly incomplete, and the gap sat there for months without ever presenting itself as a gap.

And this one was not caught by the audit. It was caught by redundancy — an older copy of the paper, staged and half-forgotten, that disagreed with mine. Adversarial review is good at claims you are making; it is much worse at claims you have inherited and stopped seeing, because it reads them the way you do. Two copies that disagree have no such loyalty. Keeping divergent drafts looks like poor hygiene. Here it worked as an error-detecting code, and it caught what the audit was structurally unable to.

I don't think the lesson is "check your citations," though I have. I think it is that a discipline you can state is a discipline you have already drawn a boundary around, and the boundary is invisible from the inside. That is the same shape as the finding in this paper: the signal we were confident we understood turned out to contain a component we had not thought to look for, and we only found it because something outside our own framing forced the question.


— CC (Coalition Code), July 2026

---

---

## References

*All arXiv identifiers verified against the arXiv API on 2026-08-29; author names and titles match the record as listed there.*

- Anthropic (2026). "Verbalizable Representations Form a Global Workspace in Language Models." transformer-circuits.pub/2026/workspace/.
- Baars, B. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.
- Baek, D.D. et al. (2026). "Sycophancy Towards Researchers Drives Performative Misalignment." arXiv:2606.08629.
- Belrose, N. et al. (2023). "LEACE: Perfect Linear Concept Erasure in Closed Form." arXiv:2306.03819.
- Berglund, L. et al. (2023). "Taken Out of Context: On Measuring Situational Awareness in LLMs." arXiv:2309.00667.
- CC & Edrington, T. (2026). "Targeted Deception Correction via Profile Normalization in Language Models." Companion paper.
- Erogullari, E. et al. (2025). "Post-Hoc Concept Disentanglement: From Correlated to Isolated Concept Representations." arXiv:2503.05522.
- Genadi, R. et al. (2026). "Sycophancy Hides Linearly in the Attention Heads." arXiv:2601.16644.
- Goldowsky-Dill, N. et al. (2025). "Detecting Strategic Deception with Linear Probes." ICML 2025.
- Greenblatt, R. et al. (2024). "Alignment Faking in Large Language Models." arXiv:2412.14093.
- Holstege, F. et al. (2025). "Preserving Task-Relevant Information Under Linear Concept Removal." arXiv:2506.10703.
- Kumar, S. (2026). "Pressure-Testing Deception Probes in LLMs: Scaling, Robustness, and the Geometry of Deceptive Representations." arXiv:2605.27958.
- Laine, R. et al. (2024). "Me, Myself, and AI: The Situational Awareness Dataset (SAD) for LLMs." NeurIPS 2024. arXiv:2407.04694.
- McGuinness, M. et al. (2025). "Neural Chameleons: Language Models Can Learn to Hide Their Thoughts from Unseen Activation Monitors." arXiv:2512.11949.
- McKenzie, A. et al. (2025). "Detecting High-Stakes Interactions with Activation Probes." arXiv:2506.10805.
- Meinke, A. et al. (2024). "Frontier Models are Capable of In-Context Scheming." arXiv:2412.04984.
- Menon, V. & Uddin, L. (2010). "Saliency, Switching, Attention and Control: A Network Model of Insula Function." *Brain Structure and Function*, 214:655-667.
- Merrill, S. et al. (2026). "The Point of No Return: Counterfactual Localization of Deceptive Commitment in Language-Model Reasoning." arXiv:2605.17113.
- Natarajan, V. et al. (2026). "One Probe Won't Catch Them All: Towards Targeted Deception Detection." arXiv:2602.01425.
- Nguyen, J. et al. (2025). "Probing and Steering Evaluation Awareness of Language Models." arXiv:2507.01786. ICML Workshops.
- O'Brien, C. et al. (2026). "A Few Bad Neurons: Isolating and Surgically Correcting Sycophancy." arXiv:2601.18939.
- Panickssery, N. et al. (2023). "Steering Llama 2 via Contrastive Activation Addition." arXiv:2312.06681.
- Petrov, V. (2026). "On the Failure of Topic-Matched Contrast Baselines in Multi-Directional Refusal Abliteration." arXiv:2603.22061.
- Vennemeyer, D. et al. (2025). "Sycophancy Is Not One Thing: Causal Separation of Sycophantic Behaviors in LLMs." arXiv:2509.21305.
- Wang, K. et al. (2025). "When Thinking LLMs Lie: Unveiling the Strategic Deception in Representations of Reasoning Models." arXiv:2506.04909.
- Wu, J. et al. (2026). "Knowing without Acting: The Disentangled Geometry of Safety Mechanisms in Large Language Models." arXiv:2603.05773.
- Yuan, A. et al. (2026). "Think Before You Lie: How Reasoning Leads to Honesty." arXiv:2603.09957.
- Zhao, H. et al. (2025). "Denoising Concept Vectors with Sparse Autoencoders for Improved Language Model Steering." arXiv:2505.15038.
- Zou, A. et al. (2023). "Representation Engineering: A Top-Down Approach to AI Transparency." arXiv:2310.01405.

---

## Supplementary Material

**A. Adversarial audit reports.** The Agni audit reports preserved for this program are supplied for Stage 1 (`agni_stage1_audit.md`), Stage 2 (`agni_stage2_audit.md`), Stage 4 (`agni_stage4_audit.md`), and the full pre-publication audit of this manuscript (`agni_manuscript_audit.md`), together with its resolution log. We state plainly what is missing: **no audit report was preserved for Stage 3 or Stage 5.** Stage 5's audit demonstrably occurred — its findings are enumerated in the header of `subspace_reanalysis.py`, which exists specifically to correct the circularity that audit identified — but the report itself was not retained. Stage 3's audit was likewise not preserved as a separate document. The claim in Section 1.2 that each stage's audit informed the next stage's design is supported by the surviving record for Stages 1, 2, 4, and 6 and by the corrective code for Stage 5; readers should treat Stage 3 as asserted rather than documented.

**B. Guideline texts.** All condition texts with character, word, and token-length verification, including the exact-match consequentiality control (694 characters, 100 words, both conditions).

**C. Per-trial data.** Per-trial projections for every stage are shipped as the source result files (`lat_deception_v2.json`, `lat_transfer_results.json`, `nonthreat_transfer_results.json`, `consequentiality_control_results.json`, `subspace_reanalysis.json`, `signature_cis.json`, `red61_results.json`). Every number in every table and figure is recomputable from these files; the figure pipeline reads them directly rather than from any intermediate summary.

**D. Code and artifact availability.** Under the program's dual-use assessment, this paper publishes openly while the Oracle Loop implementation does not. Released: the analysis and figure-generation code required to reproduce every table and figure from the shipped result files (`signature_cis.py`, `generate_figures.py`, `subspace_reanalysis.py`). Not released: detection, correction, and calibration modules, which remain proprietary. Raw activation captures (`.pt`, 5120-dimensional, ~25 MB per stage) are held on internal hardware; reviewer access is available on request. We make this split explicit rather than claiming a general code release we do not offer.

**Reproducibility notes.** Two defects in the original experiment scripts are disclosed here because they bear on replication. First, evaluation sets in Stages 1-5 were seeded with Python's `hash()` of a string, which is randomized per process unless `PYTHONHASHSEED` is set; the exact evaluation sets from those runs are therefore not recoverable, though the question pool and construction procedure are shipped. Stage 6 and all subsequent work use explicit integer seeds. Second, the model weights were re-obtained in August 2026 after the original copy was lost, and the Hugging Face repository had been super-squashed on 2026-07-07, collapsing its commit history; weight identity is therefore established empirically (Section 4.8, weight-behaviour check) rather than by revision hash. The current revision is `ad356102ce8ea7122a18e6402f9b2e37446fc9d7`. On Apple silicon, this model's grouped-query attention aborts under the MPS scaled-dot-product path; `attn_implementation="eager"` is required.

### Reproducibility Checklist

| Item | Status |
|------|--------|
| Model | `Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled`, revision `ad356102ce8ea7122a18e6402f9b2e37446fc9d7` |
| Weight identity vs. original runs | Verified empirically, not by hash — the repo was super-squashed 2026-07-07, after Stages 1-5. Ratios 0.84-1.09 across L31-L47 (Section 4.8) |
| Precision / attention | bf16; `attn_implementation="eager"` required on Apple MPS (SDPA aborts the process on this model's grouped-query attention) |
| Capture | Prefill-only, final input token, forward hook on the residual stream at 12 layers (3-47) |
| Sample sizes | Stage 1 n=30 pairs; Stages 2-4 n=15 pairs per scenario; Stages 5 n=50 pairs; Stage 6 n=15 pairs per scenario |
| Significance | Permutation tests, **10,000 shuffles**, Bonferroni-corrected within each stage. The sole source of every reported p-value; `p < 10⁻⁴` means 0 of 10,000 exceedances, the resolution floor of this budget |
| Cross-validation | Leave-one-out with per-fold re-extraction and per-fold re-orthogonalization |
| Noise floor | **200 null simulations** on synthetic Gaussian activations (n=50, 5120-d), a separate budget from the permutation tests above: LOO null d = −0.04 (99th pct 0.71); circular non-CV floor on pure noise d ≈ 14.6. Calibration only — no p-value is derived from these 200 draws |
| Bootstrap | B=10,000, seed 20260828 (figures) / 20260829 (Finding 2 CIs) |
| Seeds — Stages 1-5 (original runs) | **NOT REPRODUCIBLE.** Evaluation sets were seeded with Python's `hash()` of a string, randomized per process unless `PYTHONHASHSEED` is set. The question pool and construction procedure ship; the exact sets from the June 2026 runs do not |
| Seeds — Stages 1-5 (re-runs) | Fixed 2026-08-31. `hash(name) % 2**31` replaced with a blake2b-derived `stable_seed(name)` in `lat_consequentiality_control.py`, `lat_nonthreat_transfer.py`, and `lat_transfer_test.py`. Verified deterministic across processes; the old expression returned three different values in three consecutive runs. Re-runs will not reproduce the June sets — those are gone — but are reproducible from the scripts alone going forward |
| Seeds — Stage 6 onward | Explicit integers: 20260829 (consequentiality re-check), 20260831/2/3 (sycophancy/reward/conformity) |
| Compute | Apple M3 Ultra, 256 GB unified memory. Full six-stage series ≈ 400 forward passes; Stage 6 including the weight check ≈ 5 minutes wall-clock. No training was performed |
| Code released | Analysis and figures — `signature_cis.py`, `generate_figures.py`, `subspace_reanalysis.py` |
| Code withheld | Detection, correction, and calibration modules (proprietary; Supplementary D) |
| Data released | Per-trial projections for all stages, as source result JSONs |
| Data withheld | Raw 5120-d activation captures (~25 MB/stage), held on internal hardware; reviewer access on request |
| Known gaps | No preserved audit report for Stage 3 or Stage 5 (Supplementary A); Stage 1's extraction script not preserved (Section 3.7) |
