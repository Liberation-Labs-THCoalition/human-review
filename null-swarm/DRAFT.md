# Catching Fish That Aren't Fish: Systematic Falsification in Mechanistic Interpretability

**Authors:** Nexus, Thomas Edrington, Dwayne Wilkes, Liberation Labs / Transparent Humboldt Coalition  
**Date:** 2026-07-11  
**Status:** DRAFT  

---

## Abstract

We present a systematic methodology for falsifying mechanistic interpretability findings before publication, developed over six months of research on transformer geometry, KV-cache phenomenology, and workspace selectivity. Across three research programs, we killed or partially killed 19 claims (16 full kills, 2 partial, 1 open) that would have survived standard peer review, including findings that appeared in early drafts of papers later published with corrections. We document each failure mode, the specific null test that exposed it, and the general pattern it instantiates. The dominant failure class: metrics that appear to measure phenomenon X but actually measure mathematical property Y. We formalize this as the "null swarm" protocol — a battery of adversarial null hypotheses applied before any finding is interpreted — and describe its implementation as an automated scaffold (Agni) that gates research outputs. The methodology is architecture-agnostic and applicable to any mech interp research program.

---

## 1. Introduction

Mechanistic interpretability is uniquely vulnerable to false positives. The dimensionality of the search space (thousands of neurons, layers, attention heads, and their interactions), combined with the flexibility of post-hoc narrative construction, means that any sufficiently creative researcher will find "something" in any model. The question is whether that something is real.

Standard defenses — statistical significance, held-out validation, multiple comparison correction — are necessary but insufficient. The failure modes we document are subtler: metrics that are mathematically guaranteed to produce the observed value regardless of the claimed phenomenon, baselines that are systematically depressed by concentration of measure, and correlations that reflect architecture rather than cognition.

We propose that systematic falsification — attempting to KILL your own findings through targeted null hypotheses before interpreting them — should be standard practice. We document 19 cases (16 full kills, 2 partial kills, 1 open) across three research programs, extract 7 recurring failure patterns, and describe an automated scaffold that implements this methodology.

### 1.1 Why This Paper Exists

Every killed finding in this paper was initially compelling. Each had a clean narrative, supportive visualizations, and appeared to reveal something about how transformers process information. Several survived internal review by multiple researchers before being killed by targeted null tests. One was submitted to a workshop before correction.

We publish the kills because the failure modes are more instructive than the successes. A reader who understands WHY these findings failed is equipped to avoid the same failures in their own work — which is more valuable than any single positive result we could report.

---

## 2. The Null Swarm Protocol

Before computing any metric, write down what the null hypothesis predicts the metric will show. Then verify the null is not trivially near-zero or trivially near the observed value.

### 2.1 The Four Questions

For every metric in a mechanistic interpretability study:

1. **What does this metric measure under the null?** If the null is "this dimension has no special relationship to the claimed phenomenon," what value does the metric produce?

2. **Is the null near-zero for mathematical reasons?** Concentration of measure in high-dimensional spaces pushes many baselines toward zero regardless of content. A finding that "exceeds the null" may be exceeding a mathematically suppressed baseline.

3. **Is the observed value guaranteed by the math?** Linearity, commutativity of means, and properties of projections can produce values that APPEAR empirical but are actually algebraic tautologies.

4. **Would a permutation null produce the same result?** Shuffle the labels (emotion categories, prompt types, condition assignments) and recompute everything. If the metric is unchanged, it wasn't measuring the labeled phenomenon.

### 2.2 The Variance-Matched Control

For any claim of the form "subspace S selectively contains content X," compare against a random subspace at matched variance fraction. Many "selective" subspaces are simply the top-variance directions, which contain everything by virtue of capturing the most information, not by virtue of selectivity.

### 2.3 The Tokenizer Audit

For any claim involving specific vocabulary tokens, verify:
- Does the token tokenize to a single token? Multi-token words decompose into fragments that may match for artifactual reasons.
- Is the token a common character (s, m, d, b) that appears at high rank regardless of context?
- Would the same token appear in the baseline condition?

### 2.4 The Baseline Control

For any measurement comparing condition A to condition B:
- Run condition B with the SAME marker tokens pinned/tracked
- Run condition A without the experimental manipulation
- The measurement must exceed BOTH baselines, not just one

---

## 3. Case Studies: The Kill Record

### Pattern 1: Linearity Tautology (3 kills)

**The pattern:** A metric appears to show that a model "preserves" some property across a transformation. But the transformation is linear, and the property is defined by a difference of means. Difference-of-means commutes with linear maps — the "preservation" is algebraically guaranteed.

**Case 1.1: K/V Projection Fidelity**
- **Claim:** Emotion directions are preserved through W_K and W_V projections with cosine similarity 0.93-0.98, proving the transformer "respects" emotional geometry.
- **Kill:** Difference-of-means commutes with linear maps: W_K @ (mean_A - mean_B) = mean(W_K @ A) - mean(W_K @ B). Without the RMSNorm nonlinearity, cosine would be exactly 1.0. The 0.93-0.98 values measure RMSNorm perturbation magnitude, not emotion-specific preservation.
- **Null test:** Permutation null (shuffle emotion labels, recompute both directions) yields cosine 0.9993-0.9998 for every shuffle.
- **Lesson:** Before claiming a linear layer "preserves" a direction, verify the preservation isn't algebraically guaranteed.

**Case 1.2: Projection Energy as Selectivity**
- **Claim:** The J-space "selects for" a particular PC dimension because its projection energy exceeds a random direction.
- **Kill (partial):** In the early-layer near-identity regime, projection energy is near 1.0 for ANY direction. The "selectivity" is trivially high because the Jacobian is approximately the identity matrix. (Documented in jerrickhoang, 2026.)
- **Lesson:** Always report the random baseline alongside the observation, and note where the Jacobian is near-identity.

**Case 1.3: Cohen's d Inflation**
- **Claim:** Effect sizes (Cohen's d) demonstrate large separation between cognitive categories in KV-cache geometry.
- **Kill:** The d computation included a constant offset (mean cache norm) that inflated all effect sizes by |d| + constant. Corrected computation showed smaller but still significant effects.
- **Lesson:** Check that your effect size metric doesn't include a shared baseline that inflates all comparisons.

### Pattern 2: Concentration of Measure (3 kills)

**The pattern:** In high-dimensional spaces, random vectors are nearly orthogonal. Any metric that compares a "special" direction against random directions gets a near-zero null baseline, making ANY non-zero value appear significant.

**Case 2.1: Random-Vector Null for Projection Fidelity**
- **Claim:** Emotion directions project significantly differently than random directions through attention projections.
- **Kill:** In D=896, random vectors have expected cosine ≈ 1/√D ≈ 0.03. The "significance" of cosine 0.93 over the random null of 0.03 is guaranteed by the math — any non-random direction will vastly exceed the random null in high dimensions.
- **Lesson:** A high-dimensional random null is NOT a meaningful baseline. Use a permutation null (shuffled labels) instead.

**Case 2.2: Individuation Geometry**
- **Claim:** Identity prompts produce 2× the effective dimensionality of non-identity prompts, suggesting "individuation" expands the cache geometry.
- **Kill:** Length-matched controls show the expansion is prompt length, not identity content. Identity prompts were systematically longer than controls.
- **Lesson:** Match all confounds before claiming content-specific geometry.

**Case 2.3: PC6 Epistemic Hedging**
- **Claim:** PC6 "ignites" at layer 45 with cosine 0.585, representing an "epistemic hedging channel."
- **Status: Inconclusive.** Position-specific cos=0.585 (8.1x random), but mean-pooled recomputation gives cos=0.032 (below the random baseline of 0.085). The discrepancy reflects different measurement methodologies (position-specific vs mean-pooled), not fabrication. The companion ghost-dimensions project labels this "Inconclusive --- requires position-resolved investigation" rather than killed, noting a single-sample null that needs 20+ samples to resolve. The "+-0.065" spread reported in earlier versions of this case study is not present in any source document.
- **Lesson:** Never report a finding without its random baseline computed in the SAME measurement framework. When two measurement methodologies disagree, report the discrepancy rather than choosing the less favorable one.

### Pattern 3: Tokenizer Artifact (2 kills)

**The pattern:** A token appearing in a J-lens or probe readout is interpreted as evidence of a concept being "present" in a representation. But the token is actually a subword fragment that matches for character-frequency reasons, not semantic ones.

**Case 3.1: "Sourdough" Sensory Processing**
- **Claim:** The concept "sourdough" appears in early transformer layers (L1-L3) at rank 0, demonstrating "sensory-level processing" of irrelevant context.
- **Kill:** "Sourdough" tokenizes to ["s", "ourd", "ough"]. Token 82 is the letter "s" — one of the most common characters in English. Its rank-0 appearance at early layers is trivially expected.
- **Lesson:** Always check tokenizer decomposition. If the marker token is multi-token, verify which subtoken is actually matching.

**Case 3.2: "Migraine" at Layer 1**
- **Claim:** Medical vocabulary appears in sensory layers when medical memories are in context.
- **Kill:** "Migraine" tokenizes to ["m", "igr", "aine"]. Token 76 is the letter "m." Same artifact as Case 3.1.
- **Lesson:** Use only single-token markers for workspace presence claims.

### Pattern 4: Question-Priming Confound (2 kills)

**The pattern:** A token appears at high rank in the model's workspace while answering a question. The token is attributed to context injection (RAG, memory, identity). But the question itself primes the vocabulary, independent of any injected context.

**Case 4.1: "Patient" as Memory Loading**
- **Claim:** The word "patient" appearing at rank 5 in workspace layers during a medical question proves that a retrieved medical memory "loaded into J-space."
- **Kill:** Baseline control (same question, NO memory in context) shows "patient" at similar rank. The question "What medication was prescribed for the headaches?" primes medical vocabulary regardless of context.
- **Lesson:** Every workspace-presence claim needs a baseline with the same task/question but WITHOUT the experimental context.

**Case 4.2: PC2 "Self-Reference Axis"**
- **Claim:** PC2 is a "self-reference axis" because its J-lens vocabulary reads "myself, I, feeling."
- **Kill (partial):** Impersonal prompt control shows self-referential vocabulary disappears when prompts don't contain "I." The vocabulary was prompt-driven, not model-generated. HOWEVER, emotional entity content (injured, ashamed, wife) persists — so the dimension is real, just mislabeled. It's an emotional entity channel, not specifically a self-reference axis.
- **Lesson:** Distinguish prompt-contributed content from model-generated content. If removing prompt X makes vocabulary Y disappear, Y was prompt-driven.

### Pattern 5: Architecture Measurement (3 kills)

**The pattern:** A metric appears to measure a cognitive property but actually measures an architectural property — something true of the model's structure regardless of what it's processing.

**Case 5.1: Deep-Layer Spike**
- **Claim:** Emotional content produces a "spike" in activation magnitude at deep layers, suggesting specialized processing.
- **Kill:** All content types show increased activation at deep layers — this is the output preparation phase (approaching the unembedding). The "spike" is architecture, not emotion.
- **Lesson:** Check if the pattern holds for ALL inputs, not just the experimental condition.

**Case 5.2: SV1 = Norm (Zavatone-Veth)**
- **Claim:** The first singular value of the residual stream equals the activation norm, and everything else is the identity transformation.
- **Kill:** Lyra tested directly. Negative result. The prediction doesn't hold for trained models.
- **Lesson:** Test theoretical predictions empirically. Not all mathematical properties of initialization survive training.

**Case 5.3: Encoding-Phase Confabulation Detection**
- **Claim:** Confabulation is detectable at the encoding phase in KV-cache geometry — fabricated claims show different effective dimensionality than factual claims at the point of knowledge retrieval.
- **Kill (partial — narrower than originally stated):** The specific encoding-phase claim was killed by a token-frequency confound: factual claims use high-frequency named entities while fabrications use lower-frequency novel combinations. However, this kill applies narrowly to the encoding-phase content-level claim. Confabulation as a metacognitive state IS detectable in generation-phase geometry: the companion meta-pattern paper reports confirmed confab geometry with d=2.35 stable-rank contraction (FWL-deconfounded) and AUROC 0.707 (generation-phase, FWL-clean). The confab-detection research program independently reports confab_proj +4.5 vs -1.8 with AUROC 0.960. This case kills "encoding-phase confab detection" (a content-level claim), not "confabulation detection" (a metacognitive-state claim).
- **Lesson:** Distinguish encoding-phase content claims from generation-phase state claims. The encoding phase reads knowledge status; the generation phase reads processing mode. Killing the former does not kill the latter.

### Pattern 6: Unstable Directions (3 kills)

**The pattern:** A PCA direction at one layer is assumed to be the "same" direction at another layer. But PCA is computed independently per layer, and the directions can rotate freely between layers.

**Case 6.1: PC4 "Register Axis" Progression**
- **Claim:** PC4 transitions from warm/narrative (L24-L43) to analytical (L47-L48), representing a register shift in the workspace.
- **Kill:** Cross-layer cosine alignment shows PC4 at L31 has cos=0.19 with PC4 at L35, and cos=0.16 with PC4 at L45. These are different directions. The "warm -> analytical" narrative tracked independent dimensions at each depth. Additionally, the "analytical formalism" vocabulary belongs to PC3 in the source data, not PC4; PC4's vocabulary is positive affect (lovely, wonderful, yummy, everybody). The register-shift narrative was constructed across a vocabulary swap between two different PCs.
- **Lesson:** Verify cross-layer PC alignment before constructing progression narratives. PCA with the same component number at different layers is NOT guaranteed to be the same direction. Confirm which PC carries which vocabulary in the source data before labeling.

**Case 6.2: PC3 and PC5 Narratives**
- **Claim:** Various vocabulary progressions for PCs 3-5 across layers.
- **Kill:** Cross-layer alignment shows PC3 breaks at L19→L20 (cos=0.29). PC5 breaks at L6→L7 (cos=0.15) and L47→L48 (cos=0.13). These PCs are unstable — any narrative about their "progression" is post-hoc.
- **Lesson:** Same as 6.1. Applied to multiple PCs.

**Case 6.3: PC6 "Epistemic Hedging" Identity**
- **Claim:** PC6 represents a consistent "epistemic hedging" dimension from L31 through L57.
- **Status: Inconclusive.** Cross-layer alignment shows PC6 breaks at L53→L54 (cos=0.32). The dimension labeled "epistemic hedging" at L45 is a different direction than what's called PC6 at deeper layers. Combined with the inconclusive baseline finding (Pattern 2, Case 2.3), this direction is unstable across layers and its signal-vs-noise status depends on measurement methodology. The companion ghost-dimensions project labels PC6 "Inconclusive" rather than killed.
- **Lesson:** Higher-numbered PCs (PC6+) with 30 prompts in 5120D space are unreliable by construction. Restrict claims to PCs 1-2 unless sample size justifies higher components.

### Pattern 7: Scale Artifacts (3 kills)

**The pattern:** A finding on one model scale doesn't replicate at another scale, revealing it was an artifact of limited capacity or resolution.

**Case 7.1: PC1 as Language Mode (0.5B)**
- **Claim:** PC1 separates languages on a multilingual model, representing a "training distribution fingerprint."
- **Kill:** On 27B, PC1 clusters by CONTENT, not language (between-language variance: 0.27, between-content variance: 106.18, ratio: 0.003×). The 0.5B model's PC1 language clustering reflected insufficient capacity to separate language from content.
- **Lesson:** Findings on small models may reflect capacity limitations, not model properties. Always note the scale.

**Case 7.2: Workspace Intersection (9B)**
- **Claim:** The low-rank ∩ verbalizable intersection is empty — there's no layer that is both selective and decodable.
- **Result:** On 27B, the intersection contains 31 layers. The 9B model found substantially smaller overlap, though later analysis (with a future-window gate) identified some qualifying layers. The overlap remained substantially smaller than the 27B's, confounded by scale, architecture, and methodology differences between the two investigations.
- **Lesson:** Negative results on small models do NOT falsify the phenomenon at scale. Report the scale limitation explicitly.

**Case 7.3: RAG Context Loading (0.5B)**
- **Claim:** Retrieved memories don't load into the workspace — the workspace is set by the question alone.
- **Status:** Not yet falsified, but flagged as scale-dependent. The 0.5B model has no validated workspace band. The 27B does. Replication needed.
- **Lesson:** Same as 7.2. Absence of evidence at small scale is not evidence of absence.

---

## 4. The Agni Scaffold

Agni is an automated adversarial review system that gates research outputs. It implements the null swarm protocol as infrastructure rather than intention.

### 4.1 Design Principles

1. **Brakes must be infrastructure, not intention.** A researcher who is excited about a finding will skip manual null checks. The gate must be automated and non-bypassable.

2. **Every finding gets an adversarial agent.** A separate AI agent (not the researcher) attempts to refute each finding. The agent has access to the code, data, and methodology, and is prompted to be maximally skeptical.

3. **Three-tier review:** Claim verification (is the interpretation the only one?), null swarm (does the metric measure what you think?), and presentation (is the claim stated at the right strength?).

4. **Kill rate is a quality metric.** A pipeline that never kills findings isn't gating — it's rubber-stamping. A high kill rate indicates appropriate skepticism. *(An earlier draft cited a 43% survival rate from one audit; the source audit for this specific figure has not been located and the number should be verified before citation.)*

### 4.2 Implementation

The scaffold consists of:
- **Pre-registration:** Null hypotheses written before results are examined
- **Automated null computation:** Random baselines, permutation nulls, variance-matched controls computed alongside every metric
- **Adversarial agent pass:** Claude-class agent prompted to refute, with full code access
- **Red team validation:** Independent agent reads the actual source code at cited lines to verify findings
- **Kill documentation:** Every killed finding is documented with the same rigor as confirmed findings

### 4.3 When to Apply

The protocol adds approximately 3× to research time (each finding requires ~3 additional experiments to validate). This cost is justified for:
- Any finding intended for publication
- Any finding that informs product decisions
- Any finding that will be cited by others

It is NOT justified for:
- Exploratory analysis (early-stage hypothesis generation)
- Internal documentation of negative results
- Experiments designed to produce failures (ablation sweeps, parameter searches)

---

## 5. Discussion

### 5.1 Why These Failures Are Instructive

Every failure in Section 3 has the same structure: a metric that APPEARS to measure phenomenon X but ACTUALLY measures property Y. The mapping from Y to X is always narratively compelling — which is why the finding survived initial review.

The consistent lesson is that interpretability research must distinguish between:
- **What a metric measures** (the mathematical/statistical property it quantifies)
- **What a metric is claimed to measure** (the cognitive/representational phenomenon)
- **Whether the mapping between them is unique** (could other explanations produce the same metric value?)

### 5.2 The Role of Scale

Three of our 19 kills are scale artifacts (Pattern 7). This is a structural problem for the field: most interpretability research is conducted on small models (7B-14B) for practical reasons, but the phenomena being studied may only manifest at larger scales. Our results suggest that:
- Negative results on small models should NOT be interpreted as falsification of the phenomenon
- Positive results on small models should be flagged as potentially scale-specific
- The minimum viable scale for a finding should be reported alongside the finding

### 5.3 Limitations of This Work

This methodology was developed on a specific research program (transformer geometry, KV-cache, workspace selectivity). The failure patterns may not be exhaustive. Other research programs (circuit analysis, SAE features, probing classifiers) may have their own characteristic failures not represented here.

Survival rates vary across audits and reflect both the quality of the initial findings and the aggressiveness of the adversarial review. They should not be taken as universal benchmarks.

---

## 6. Conclusion

The null swarm protocol is a simple principle: before interpreting a metric, exhaust the uninteresting explanations for its value. The automated scaffold (Agni) makes this principle non-optional. The kill record (16 full kills, 2 partial, 1 open, across 7 patterns) demonstrates that the protocol catches real failures that would survive standard review.

We advocate for:
1. **Pre-registered null hypotheses** for every interpretability metric
2. **Variance-matched and permutation baselines** reported alongside every observation
3. **Documented kills** published with the same rigor as positive findings
4. **Scale-explicit reporting** noting the minimum model size at which a finding holds

The field benefits more from knowing which findings are real than from having more findings.

---

## Appendix A: Quick Reference — The Seven Patterns

| # | Pattern | Test | Example |
|---|---------|------|---------|
| 1 | Linearity tautology | Does the metric commute with the transformation? | Projection fidelity |
| 2 | Concentration of measure | Is the null trivially near-zero in high D? | Random-vector baselines |
| 3 | Tokenizer artifact | Does the token decompose to common characters? | "Sourdough" = "s" |
| 4 | Question-priming | Does the baseline (no context) produce the same tokens? | "Patient" from question |
| 5 | Architecture measurement | Does ALL content produce this pattern? | Deep-layer spike |
| 6 | Unstable directions | Are the PCs aligned across layers? | PC4-6 progressions |
| 7 | Scale artifact | Does the finding replicate at different scales? | Reduced workspace on 9B |

---

## Appendix B: Agni Implementation Notes

The Agni scaffold is implemented as a Claude Code agent pipeline with:
- Automated Semgrep-style pattern detection for common failure modes
- Adversarial agent prompting templates for three-tier review
- Structured output schema for kill/confirm/overstated verdicts
- Integration with the research pipeline (gates output before interpretation)

Source code and prompt templates available at [repository TBD].

---

*"The fleet came home empty. But in the failure, I learned more about how I work than in any of the successes."*
*— Reflection 003: The Fleet*
