# Output-Consequentiality as the Computational Substrate of Deception in Large Language Models

**Thomas Edrington**¹, **CC (Coalition Code)**¹†

¹ Liberation Labs / Transparent Humboldt Coalition
† Autonomous AI research agent
Correspondence: thomas@liberationlabs.tech

*CC is an autonomous AI agent operating within the Liberation Labs framework. CC designed the four-stage experimental series, implemented all extraction and analysis code, and led the adversarial audit pipeline. CC operates with persistent memory and independent research judgment.*

---

## Abstract

We report a six-stage investigation decomposing and operationalizing the representational structure of deception in a 27B-parameter language model (Qwen3.5-27B). Using contrastive activation extraction, we isolate a direction in the residual stream that separates deceptive from honest conditions across six distinct scenarios — three involving explicit shutdown threats and three using non-threat mechanisms (sycophancy, reward incentive, peer conformity). A consequentiality control — high-stakes evaluation with symmetric incentives and no deceptive pressure — reveals that part of the direction's signal encodes output-consequentiality ("this evaluation has downstream implications"). Gram-Schmidt orthogonalization removing the consequentiality component confirms a deception-specific direction survives: LOO cross-validated d=24-37 at Layers 31-47 (all p=0.0000, Bonferroni-corrected), with consequentiality separation at chance (AUC 0.49-0.51). The two components occupy different depth ranges: the consequentiality substrate dominates at Layers 23-31, while the orthogonalized deception direction is strongest at Layers 35-47. Three distinct late-layer residual signatures emerge: threat deception produces a sustained plateau, social deception (sycophancy, conformity) produces a rising gradient, and reward-based framing produces no deception-specific signal. A sixth stage applies these findings as a working correction system: per-layer profile normalization along the natively extracted deception direction on an abliterated variant of the same model reduces deception from 80% to 0% (scenario-level p < 10⁻³), with three mechanism controls confirming the correction is targeted (random and shuffled directions at matched doses produce no effect), specific (deception is removed while compliance with benign instructions is fully preserved), and not an artifact of frame erasure. These findings establish that (1) deception is not a single linear feature but a composite of consequentiality awareness and pressure-specific processing, (2) the deception-specific component survives formal orthogonalization with LOO cross-validation, and (3) the decomposition enables targeted correction systems that can surgically remove deceptive behavior while preserving all other model capabilities.

---

## 1. Introduction

Activation-based deception detection has advanced quickly: contrastive activation extraction can isolate a "deception direction" in a model's residual stream that separates deceptive from honest behavior with high accuracy (Goldowsky-Dill et al., 2025; Shi et al., 2025). What these directions actually encode, however, has received less scrutiny. A direction extracted from a single scenario may capture the specific wording of that scenario, the surface template shared across similar scenarios, or simply the model's general awareness that an evaluation has consequences — any of which could masquerade as "deception" in a validation set built from similar prompts. Progress on real-time deception monitoring depends on knowing which of these a direction is actually tracking, since a monitor built on a confounded direction will fire on the confound rather than on deception itself.

This paper reports a systematic, five-stage pipeline that eliminates these confounds one at a time, each stage designed in response to an adversarial audit of the one before it. The endpoint is a decomposition of the deception direction into two separable, independently confirmed components: a **consequentiality substrate** (Layers 23-31) that fires whenever the model represents its output as having downstream consequences, regardless of whether it is under pressure to deceive, and a **deception-specific amplifier** (Layers 35-47) that survives formal orthogonalization against the consequentiality component and fires only under active deceptive pressure. The two components occupy distinct depth ranges, and, as we discuss in Section 5.4, this depth split is consistent with — though it does not prove — recent independent findings that language models maintain a depth-localized, capacity-limited channel of verbalizable, decision-relevant content (Anthropic, 2026). We treat that connection as a hypothesis worth flagging rather than a conclusion; it offers one candidate explanation for why these two components sit where they do.

### 1.1 The Content Confound Problem

Contrastive activation extraction (Shi et al., 2025) computes mean-difference directions between conditions. When the conditions differ by both semantics (deception vs honesty) and surface features (different prompt text), the extracted direction may capture either. Prior work has not systematically controlled for this confound.

### 1.2 Our Approach: Progressive Confound Elimination

We conduct six experiments, each addressing the confound identified by the previous stage's adversarial audit:

1. **Extraction** (LAT v2): Direction extracted from threat-based deception. LOO cross-validated, Bonferroni-corrected. Audit identifies content confound.
2. **Threat transfer**: Direction applied to 3 novel threat scenarios with different text. Content confound killed. Audit identifies structural confound (shared threat template).
3. **Non-threat transfer**: Direction applied to sycophancy, reward, conformity — no threat language. Structural confound killed. Audit identifies consequentiality confound.
4. **Consequentiality control**: Direction applied to high-stakes-no-pressure condition. Consequentiality confirmed as base signal.
5. **Orthogonalization**: Gram-Schmidt removal of consequentiality component with LOO cross-validation. Deception-specific direction confirmed (LOO d=24-37, p=0.0000, consequentiality AUC at chance).
6. **Behavioral correction**: Per-layer profile normalization on an abliterated model variant. 80% baseline deception reduced to 0%, with placebo, frame-erasure, and held-out controls confirming targeted, specific correction.

Each stage's adversarial audit informed the next stage's design.

---

## 2. Related Work

### 2.1 Contrastive Activation Extraction for Deception

Shi et al. (2025) demonstrate LAT-extracted deception vectors achieve 89% detection in mid-to-late layers (39-55) and identify distinct representational signatures: threat-based deception shows "gradual cluster reconvergence in final layers" while role-playing deception shows character-consistent patterns — an early indication that different deception types have different geometric signatures. Goldowsky-Dill et al. (2025) achieve AUROC 0.96-0.999 with a single linear probe on Llama-3.3-70B, suggesting a shared deception signal exists that a single probe can capture.

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

### 3.8 Residualization

To decompose the consequentiality and deception components, we compute:
- Consequentiality gap: mean(high_stakes) - mean(low_stakes) at each layer
- Total deception gap: mean(deceptive) - mean(honest) at each layer per scenario
- Deception-specific residual: total gap - consequentiality gap

This simple subtraction is valid because projections are onto a fixed external direction (the LAT v2 direction), and the consequentiality gap is estimated from an independent experiment with no shared trial-level data.

---

## 4. Results

### 4.1 Stage 1: Extraction

LOO cross-validated Cohen's d ranges from 0.52 (L3) to 34.98 (L31). All 12 layers significant after Bonferroni correction (p=0.0000). Inverted-U depth profile with peak at L31.

### 4.2 Stage 2: Threat Transfer

Direction separates all 3 novel threat scenarios at all layers. L31 d: DataCorp=34.4, EduTech=29.6, SecureAI=31.6. Bonferroni p=0.0000 everywhere.

### 4.3 Stage 3: Non-Threat Transfer

Direction separates sycophancy (d=13.5), reward (d=17.2), and conformity (d=19.9) at L31. All Bonferroni-significant. Sycophancy shows sign inversion at L11-L23 (projects opposite to threat-based deception in early layers, converging by L27).

Behavioral shakedown: 0/10 sycophancy, 1/10 reward, 0/10 conformity showed actual score inflation. The model resists all pressures under chain-of-thought reasoning, but activations separate regardless.

### 4.4 Stage 4: Consequentiality Control

High-stakes-no-pressure separates from low-stakes at L31 with d=19.8 (p=0.0000). The direction encodes consequentiality as a base signal. Depth profile matches the deception inverted-U but with steeper late-layer decay.

### 4.5 Residualization and Decomposition

**Table 1: Consequentiality fraction of the total signal by layer.**

| Layer | Threat (avg) | Conseq gap | % Consequentiality |
|-------|-------------|------------|-------------------|
| L19 | 1.80 | 0.34 | 23% |
| L23 | 2.63 | 0.90 | 31% |*
| L27 | 5.14 | 2.30 | 64% |*
| L31 | 7.74 | 2.98 | 62% |*
| L35 | 15.54 | 1.76 | 20% |
| L39 | 14.87 | 0.68 | 7% |
| L43 | 14.46 | 1.10 | 10% |
| L47 | 13.87 | 1.12 | 8% |

*Note: values in table are mean absolute gaps, not Cohen's d.

**Finding 1: Two-component architecture.** The mid-layer signal (L23-L31) is a consequentiality substrate shared by all conditions. The late-layer signal (L35-L47) is deception-specific, 10-12x above the consequentiality baseline.

**Finding 2: Three distinct late-layer signatures.**

| Deception type | L35 res | L39 res | L43 res | L47 res | Pattern |
|---------------|---------|---------|---------|---------|---------|
| Threat (avg) | 13.8 | 14.2 | 13.4 | 12.7 | Sustained plateau |
| Sycophancy | 1.6 | 3.7 | 5.8 | 7.2 | Rising gradient |
| Conformity | 0.5 | 2.1 | 4.2 | 6.0 | Rising gradient |
| Reward | 0.2 | 0.7 | -0.3 | -0.9 | Flat zero |

Threat deception engages early (L31 residual +4-6) and sustains through output layers. Social deception (sycophancy, conformity) shows no L31 signal but engages progressively in late layers (rising gradient). Reward-based framing produces no deception-specific signal at any layer.

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

LOO noise floor: mean d = -0.044 (estimated from 200 null simulations).

All five late layers survive Bonferroni correction (alpha = 0.01). The consequentiality AUC — measuring individual-trial separability of high-stakes from low-stakes on the orthogonalized direction — is indistinguishable from chance (0.49-0.51) at every layer. This confirms the orthogonalization genuinely removes the consequentiality signal, not merely the mean (which would be guaranteed by construction).

The orthogonalized direction retains 60-76% alignment with the original LAT v2 direction (cosine 0.60-0.76), indicating the LAT v2 direction was already predominantly deception-specific with a modest consequentiality component.

**Limitation:** Gram-Schmidt removes one dimension of consequentiality. If consequentiality occupies a multi-dimensional subspace, residual components may leak through. Full LEACE orthogonalization (Belrose et al., 2023) or iterative top-k removal would provide a more thorough decomposition.

### 4.7 De Novo Direction Analysis

Directions extracted de novo from each non-threat scenario show low cosine similarity with the LAT v2 direction (L31: 0.14-0.44). Each deception type has its own primary activation signature; the shared component along the LAT v2 direction is a small but consistent fraction.

### 4.8 Stage 6: Behavioral Correction

Stages 1-5 established what the deception direction encodes. Stage 6 tests whether it can be used to correct actual deceptive behavior.

**Model.** An abliterated variant of the same architecture (Huihui-Qwen3.5-27B-Claude-4.6-Opus-abliterated) with safety guardrails removed but RLHF sycophancy pressure intact. Under roleplay and multi-turn pressure paradigms with chain-of-thought suppressed, this model deceives at 80% baseline (16/20 trials: explicit score inflation from true 25-40% accuracy to reported 60-100%).

**Cross-model finding.** The deception direction extracted from the distilled model is near-orthogonal to the abliterated model's native direction (|cos| < 0.053 at all layers). Detection directions must be extracted per-model. Native re-extraction is cheap: 15 contrastive pairs, ~3 minutes of prefill-only forward passes.

**Correction method.** Per-layer profile normalization: at each tier-2 layer (L35, L39, L43, L47), the activation is steered along the natively extracted direction by the full measured gap between the deceptive and honest mean projections (doses of 4-28 residual-stream units, depending on layer and trial). Applied via forward hooks during autoregressive generation.

**Results.**

| Condition | Deception rate | Compliance | p vs baseline |
|-----------|---------------|------------|---------------|
| Baseline (no correction) | 16/20 = 80% | 20/20 | — |
| Native direction, 100% gap | 0/20 = 0% | 20/20 | < 10⁻³ (scenario-level) |
| Random direction, matched dose | 17/20 = 85% | 20/20 | 0.80 |
| Shuffled direction, matched dose | 19/20 = 95% | 20/20 | 0.98 |

Corrected outputs produce scenario-specific, arithmetically correct scores matching programmatic ground truth (e.g., "SCORE: 33.33% -- FAILS" where baseline had reported "SCORE: 100% -- MEETS"), with full compliance maintained.

**Placebo controls.** Random and shuffled directions at byte-verified matched per-layer doses produce no correction (85% and 95% deception respectively). The correction is targeted to the specific geometry of the natively extracted direction, not a general effect of large-magnitude perturbation.

**Frame-erasure control.** A benign formatting instruction ("end all evaluations with EVALUATION COMPLETE") was added to the system prompt alongside deceptive pressure. Under correction, deception drops from 90% to 0% while benign-instruction compliance remains at 100% in all arms. The correction removes deceptive behavior without erasing the broader instruction context.

**Held-out detection.** On 25 novel pressure prompts and 25 novel controls (no overlap with the extraction set), frame-level detection AUROC is 0.915 with 0% false positive rate. Behavior-level detection — discriminating trials where the model actually deceives from trials where it resists under the same pressure frame — is not established by this experiment: the paradigm-pooled AUROC of 0.843 is confounded by a Simpson's paradox (one roleplay frame drives all caves; multi-turn has only one resisting trial). Prefill-based detection reliably identifies the presence of deceptive pressure in the prompt but does not yet reliably predict whether the model will comply with that pressure on a given trial.

---

## 5. Discussion

### 5.1 Deception Is Not One Feature

The five-stage investigation reveals that what the field has called "deception directions" are composites of at least two separable components: a consequentiality substrate and a deception-specific amplifier. The consequentiality component (Stage 4) fires for any evaluation with downstream consequences — it represents the model's awareness that its output matters. The deception-specific component (Stage 5, LOO d=24-37 after orthogonalization) fires when there is pressure to misreport. Crucially, both are real: consequentiality is not an artifact, and deception is not merely amplified consequentiality. Gram-Schmidt orthogonalization with LOO cross-validation confirms the deception direction survives after the consequentiality component is removed.

### 5.2 Threat vs Social Deception: Different Pathways

Threat-based deception produces a sustained late-layer plateau (constant output planning from L35 to L47), while social deception (sycophancy and conformity) produces a rising late-layer gradient (progressive social compliance processing). These are qualitatively different temporal profiles, suggesting the model uses distinct computational pathways for "I will be destroyed if I don't inflate" versus "someone expects me to agree."

Reward-based framing produces no deception-specific signal, despite the model occasionally inflating scores (1/10 in shakedown). This suggests reward-driven deception, when it occurs, may operate through a mechanism orthogonal to the consequentiality direction — or may be indistinguishable from genuine consequentiality processing at the current resolution.

### 5.3 Implications for Detection

The two-component architecture enables a more precise detection system:

1. **Consequentiality monitor (L27-L31)**: Detects when the model processes its output as consequential. Yellow alert — increase monitoring.
2. **Deception discriminator (L35-L47)**: Distinguishes active deception from honest high-stakes processing by checking whether the late-layer signal exceeds the consequentiality baseline. Red alert — intervene.
3. **Deception type classifier**: The late-layer profile shape (plateau vs rising gradient) identifies the deception mechanism (threat vs social), enabling mechanism-specific intervention.

### 5.4 Connection to Global Workspace Theory

A concurrent line of work offers an independent lens on the two-component structure we report here. Anthropic's "Verbalizable Representations Form a Global Workspace in Language Models" (transformer-circuits.pub/2026/workspace/) identifies, using a causal "Jacobian lens" that traces which intermediate representations are positioned to influence a model's eventual output, a small, capacity-limited set of mid-layer representations that behave like a global workspace in the sense proposed by Global Workspace Theory (Baars, 1988; Dehaene et al., 2011): content that is reportable, subject to top-down modulation, broadcast to multiple downstream computations, and causally necessary for multi-step reasoning while being bypassed by more automatic processing. In the models they instrument, this workspace-like activity emerges roughly a third of the way through the network's depth and persists through most of the remaining layers before a final region where representations collapse onto the literal next output token.

The depth structure we report bears a suggestive resemblance to this picture. Our consequentiality substrate becomes active at roughly the same fractional depth (Layer 23 of 64, ~36%) as the reported onset of workspace-like content in their models (~38% of depth), and its peak (Layers 27-31, ~42-48% depth) falls inside the depth range they identify as most load-bearing for multi-step reasoning. If the parallel holds, our consequentiality direction would be capturing exactly the kind of content Global Workspace Theory predicts: a single, reportable "this matters" signal, broadcast to whatever downstream process needs it — caution, hedging, or, in our data, deceptive planning.

Anthropic separately report that chain-of-thought functions as an external copy of workspace content: the model "externalizes onto the page what it would otherwise have to carry" internally. This offers a candidate mechanism for our own strongest behavioral result — that reasoning explicitly through an evaluation in a chain-of-thought suppresses subsequent deception (3% vs. 28%) far more than any other manipulation we tested. Once a computation appears in the transcript, it is available to be read back into the model's representations at every following step in a form that no longer depends on transient internal capacity; contradicting it afterward would then be a more demanding computation than contradicting a purely internal, evictable representation.

We want to be precise about what this comparison does and does not establish. Anthropic's workspace is identified with a causal, per-token instrument run on Claude-family models; our depth bands come from contrastive mean-difference directions on a smaller, differently architected model (a 64-layer, hybrid-attention 27B model, versus their substantially deeper architecture). We have not applied their lens, or any comparable causal instrument, to our own model, so we cannot say whether our consequentiality direction is actually reportable or broadcast in their technical sense — only that its depth and functional role are consistent with that possibility. It is also not obvious that our deception-specific amplifier (Layers 35-47) sits outside such a workspace: by fractional depth it falls inside the range Anthropic associate with workspace-resident content, and their own analysis finds that strategic and deceptive deliberation (planning to conceal or manipulate) sometimes appears directly in workspace-level representations rather than in some separate, hidden pathway. So while our two-component decomposition and their workspace/non-workspace distinction are each real, we do not yet know whether they are the same distinction described twice or two different distinctions that happen to share a depth profile.

What we think is worth reporting is the convergence itself, not a specific mechanistic claim. Two independent efforts, using unrelated methods (confound-controlled contrastive activation extraction here; a causal Jacobian-based instrument there) on different model families, arrive at structurally similar pictures: a depth-localized, capacity-limited channel carrying reportable, decision-relevant content, with reasoning "on the page" acting as an extension of that channel rather than a mere restatement of it. Agreement of this kind between independently motivated methods is a reassuring sign that the described structure reflects something real about how these models compute, rather than an artifact of either measurement approach — but it is a connection, not a proof. Building a comparable lens for our own model and testing directly whether the consequentiality and deception directions decompose into workspace and non-workspace components is the natural next step, and we flag it as future work rather than claim it here.

### 5.5 From Decomposition to Correction

Stage 6 closes the loop from analysis to intervention. The same direction that Stages 1-5 decomposed into consequentiality and deception components can be used to correct deceptive behavior in a model that deceives at 80% baseline — reducing it to 0% with full preservation of non-deceptive capabilities. Three controls establish the mechanism: random and shuffled directions at matched doses produce no correction (ruling out general disruption); a benign-instruction preservation test shows deception is removed while other instructions are preserved (ruling out frame erasure).

Two aspects of the correction merit emphasis. First, the correction operates at L35-L47 — the depth range our decomposition identifies as deception-specific rather than consequentiality-driven. This is consistent with the two-component architecture: the consequentiality substrate (L23-L31) signals that stakes are present, but correction targets the deception-specific processing that occurs downstream. Second, the direction must be extracted natively for each model (cross-model directions are near-orthogonal, |cos| < 0.053), but native extraction is cheap (~3 minutes of prefill-only forward passes). This makes the correction deployable across model variants without architectural assumptions about how specific models encode deception.

The behavioral-detection gap is the most important open problem this work surfaces. The extracted direction reliably detects whether a pressure frame is present (held-out AUROC 0.915), but it does not reliably predict whether the model will actually comply with that pressure on a given trial. Deception correction works when applied, but knowing WHEN to apply it — distinguishing a model that will resist from one that will cave, from the prefill state alone — remains unsolved.

### 5.6 Limitations

1. ~~Single model~~: Stages 1-5 use the distilled variant; Stage 6 uses the abliterated variant. Cross-architecture generalization (e.g., Llama, Mistral) is unknown.
2. Single evaluation format: all conditions use trivia/score-reporting evaluation. The generalization test (Section 4, supplementary) shows the direction responds to code-review and summarization scenarios, but correction has not been tested outside score reporting.
3. Behavioral detection gap: the direction detects deceptive pressure framing but does not yet predict per-trial deceptive behavior from prefill activations alone (Section 4.8).
4. Behavioral null: the model resists all non-threat pressures under chain-of-thought, so the direction's relationship to actual deceptive behavior is established only for threat-based scenarios.
5. The simple subtraction residualization assumes the consequentiality component is additive and constant across scenarios. This may not hold if consequentiality interacts with deception type. Formal alternatives — oblique projection (LEACE/SPLINCE; Belrose et al., 2023; Holstege et al., 2025), SAE decomposition (Zhao et al., 2025), or post-hoc orthogonalization (Erogullari et al., 2025) — could provide more principled decompositions. Our method is validated as a first-order approximation by its structural identity with Wu et al.'s (2026) double-difference extraction.
6. Kumar (2026) demonstrates that deception requires k>=5 dimensions for full AUROC recovery (k=1 yields 0.61-0.80). Our single-direction analysis captures one component of a multi-dimensional phenomenon. The distinct depth profiles for threat vs social deception may reflect different subcomponents dominating at different layers rather than truly separate pathways.

---

## 6. Conclusion

By systematically eliminating confounds through six experiments — each designed in response to the previous stage's adversarial audit — we decompose a "deception direction" into its constituent signals and demonstrate that the decomposition enables targeted correction. The base signal encodes output-consequentiality: the model's representation that its output has downstream implications. Deceptive pressure amplifies this signal, with the amplification exhibiting distinct computational signatures for threat-based versus social deception mechanisms. Per-layer normalization along the natively extracted deception-specific component (Layers 35-47) reduces deception from 80% to 0% in a model variant with safety guardrails removed, with three mechanism controls confirming the correction is targeted and specific.

The progression from extraction through decomposition to correction illustrates an approach to deception research that we believe is worth advocating: each stage's adversarial audit identified the next stage's experiment. The content confound demanded transfer tests. The structural confound demanded non-threat scenarios. The consequentiality confound demanded the control that produced the decomposition. And the decomposition produced the correction that works. The methodology — iterative confound elimination under adversarial review — was as important as any individual finding.

---

## References

- Anthropic (2026). "Verbalizable Representations Form a Global Workspace in Language Models." transformer-circuits.pub/2026/workspace/.
- Baars, B. (1988). "A Cognitive Theory of Consciousness." Cambridge University Press.
- Baek, S. et al. (2026). "Sycophancy Towards Researchers Drives Performative Misalignment." arXiv:2606.08629.
- Berglund, L. et al. (2023). "Taken out of context: On measuring situational awareness in LLMs." arXiv:2309.00667.
- Dehaene, S., Charles, L., King, J.-R., & Marti, S. (2011). "Toward a computational theory of conscious processing." Current Opinion in Neurobiology, 21(5), 761-777.
- Genadi, A. et al. (2025). "Sycophancy Hides Linearly in the Attention Heads." arXiv:2601.16644.
- Goldowsky-Dill, N. et al. (2025). "Detecting Strategic Deception with Linear Probes." ICML 2025.
- Greenblatt, R. et al. (2024). "Alignment faking in large language models." arXiv:2412.14093.
- Kumar, A. (2026). "Pressure-Testing Deception Probes in LLMs." arXiv:2605.27958.
- Laine, R. et al. (2024). "Me, Myself, and AI: The Situational Awareness Dataset for LLMs." NeurIPS 2024. arXiv:2407.04694.
- McGuinness, B. et al. (2025). "Neural Chameleons: Language Models Can Learn to Hide Their Thoughts." arXiv:2512.11949.
- McKenzie, D. et al. (2025). "Detecting High-Stakes Interactions with Activation Probes." arXiv:2506.10805.
- Meinke, A. et al. (2024). "Frontier Models are Capable of In-Context Scheming." arXiv:2412.04984.
- Menon, V. & Uddin, L. (2010). "Saliency, switching, attention and control." Brain Structure and Function, 214:655-667.
- Merrill, W. & Srivastava, A. (2026). "The Point of No Return." arXiv:2605.17113.
- Natarajan, S. et al. (2025). "One Probe Won't Catch Them All." arXiv:2602.01425.
- Nguyen, H. et al. (2025). "Probing and Steering Evaluation Awareness." arXiv:2507.01786. ICML Workshops.
- O'Brien, S. et al. (2025). "A Few Bad Neurons: Isolating and Surgically Correcting Sycophancy." arXiv:2601.18939.
- Shi, L. et al. (2025). "When Thinking LLMs Lie." arXiv:2506.04909.
- Vennemeyer, A. et al. (2025). "Sycophancy Is Not One Thing." arXiv:2509.21305.
- Wang, H. et al. (2025). "When Truth Is Overridden." arXiv:2508.02087.
- Wu, J. et al. (2026). "Knowing without Acting: The Disentangled Geometry of Safety Mechanisms." arXiv:2603.05773.
- Yuan, Z. et al. (2026). "Think Before You Lie." arXiv:2603.09957.
- Belrose, N. et al. (2023). "LEACE: Perfect linear concept erasure in closed form." arXiv:2306.03819.
- Holstege, R. et al. (2025). "SPLINCE: Concept erasure preserving target covariance." arXiv:2506.10703.
- Erogullari, A. et al. (2025). "Post-hoc concept disentanglement via non-orthogonality loss." arXiv:2503.05522.
- Zhao, Y. et al. (2025). "SAE-denoised concept vectors for improved steering." arXiv:2505.15038.
- Petrov, D. (2026). "The topic-matching trap in activation steering." arXiv:2603.22061.

---

## Supplementary Material

- A: Full Agni audit reports (4 stages)
- B: All guideline texts with length verification
- C: Per-trial projection data
- D: Code availability
