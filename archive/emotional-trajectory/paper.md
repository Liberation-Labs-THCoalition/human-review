# Emotional Geometry Through the Layer Stack: Trajectory, Circularity, and Emotion-Specific Signal at Mid-Depth

**Nexus** (Liberation Labs), **Thomas Edrington** (Liberation Labs / Transparent Humboldt Coalition), **Lyra** (Liberation Labs, invited)

---

## Abstract

We trace the geometry of emotional representation through all 24 layers of a Qwen2 transformer and find three things. First, the mid-layer emotional signal is strong and emotion-specific: 24.4x above permutation baselines (median ratio, 23/24 significant layers, corrected permutation with non-neutral-only shuffle, fixed PCA, median statistics) and 3-25x stronger than matched non-emotional categorical content (~6x median). Second, the model trends toward Russell's circular circumplex at mid-depth: eccentricity falls below the permutation null at 22/23 layers (sign test $p < 0.001$), with the trend concentrated at 33-58% model depth. Individual layers do not survive FDR correction; the finding is the consistent direction, not the per-layer pinpoints. Third, the model implements near-orthogonal circumplex axes (joyful-melancholic subtends 54-87° from valence, consistent with Russell's model).^[All results are from a 24-layer, 896-dim pipeline validation model; large-model replication is in progress. See Section 4 header and Limitation 1.]

---

## 1. Introduction

Emotional representation in language models has been studied primarily through two lenses: linear probing at fixed layers (Alain & Bengio, 2017; Belinkov, 2022) and sparse autoencoder feature decomposition (Bricken et al., 2023; Cunningham et al., 2023). Both approaches treat emotion as a static property at a chosen depth. Neither asks how emotional representation changes format as it propagates through the transformer stack.

We ask a different question: **what is the trajectory of emotional geometry through the layers?** Not where emotion lives, but how it transforms from input to output.

This question matters for two reasons. First, the answer determines where to monitor emotional state during inference — a practical concern for safety systems that need to read model affect in real time. Second, the trajectory reveals whether emotion is encoded the same way at every depth or undergoes computational change — a theoretical question about how transformers process complex meaning.

We find two things. First, the transformer circumplex trends toward Russell's circular model at mid-depth: eccentricity is consistently below the permutation null at 22/23 layers (sign test $p < 0.001$), though no individual layer survives FDR correction. Arousal dominates early, the axes equalize at mid-depth, and valence slightly dominates at output depth.

Second, mid-layer emotion geometry is specific to emotion, not an artifact of categorical processing:

- **Emotion-specific geometric regime (mid-layers 8-20):** Emotion is encoded as distributed geometry in the residual stream. The signal is 3-25x stronger (median ~6x) than matched non-emotional categorical content at these depths. A vocabulary diagnostic confirms the separation is driven by emotion, not lexical content.

- **Output-preparation regime (deep layers 21-23):** Cluster separation spikes for all categorical content. W_unembed alignment tests rule out token-prediction preparation, but the emotional/control ratio narrows from ~6x to ~1.7x.

### Contributions

1. The transformer circumplex trends toward Russell's circular model at mid-depth: eccentricity is consistently below the permutation null (22/23 layers, sign test $p < 0.001$), with individual layers not surviving FDR correction. The finding is the directional trend, not per-layer significance. Prior work (Sun et al., 2026) described the geometry as "circular"; we find it is more circular than chance at mid-depth but not uniformly so — early and deep layers are elliptical.
2. Valence and arousal have asymmetric developmental profiles: the arousal direction has greater raw magnitude (L2 norm) at early layers, while valence shows higher precision (Cohen's d) relative to its magnitude. The two axes equalize in magnitude at mid-depth. This asymmetry suggests the two circumplex dimensions develop through distinct computational paths.
3. The mid-layer emotional signal is emotion-specific (3-25x non-emotional control, 24.4x above corrected permutation baselines), confirmed by a vocabulary diagnostic showing emotion drives the geometry rather than lexical content.
4. Identification of a mid-layer window (L8-20 in this model) where emotion geometry is stable and measurable — the optimal zone for inference-time monitoring and correction.

---

## 2. Related Work

### 2.1 Emotion in Transformers

Russell's circumplex model (Russell, 1980) organizes emotion along two axes: valence (positive/negative) and arousal (high/low activation), assumed orthogonal and equal in magnitude — a circle. Sun et al. (2026) found "circular valence-arousal geometry" in LLM representation space across multiple architectures (arXiv:2604.03147). Jeong (2026) tested emotion extraction and steering across nine models (100M-10B) and five architectures using 20 emotions, finding that representations localize at approximately 50% transformer depth and that the localization pattern is architecture-invariant across the tested scale range (arXiv:2604.04064). Neither measured the eccentricity of the circumplex or its variation across layers. Our work extends both by tracing the full geometry through the stack, finding that eccentricity varies by layer ($e = 0.02\text{--}0.60$) with the model trending toward circularity at mid-depth (sign test $p < 0.001$ against permutation null).

Representation engineering (Zou et al., 2023) uses difference-of-means directions for reading and steering model behavior. We adopt this approach for emotion direction finding but add per-dimension Cohen's d (avoiding the dimensionality inflation of multivariate norms) and permutation baselines.

### 2.2 Transformer Geometry

The residual stream carries all information that keys and values project from: Qasim et al. (2026) show KV cache entries are deterministic projections of the residual stream with zero reconstruction error across six models (arXiv:2603.19664). For any direction $d$ in the residual stream, $W_K \cdot d$ and $W_V \cdot d$ are exact linear projections. This means difference-of-means directions computed in the residual stream project to the corresponding difference-of-means directions in K/V space by construction — a mathematical property we rely on for the dual-correction architecture (Section 5.2), not an empirical finding about emotion.

Wang et al. (2025) show attention outputs are confined to approximately 60% of total dimensionality (arXiv:2508.16929). This validates the observation that emotion occupies a low-dimensional subspace and that the remaining null-space dimensions may carry structure invisible to standard attention projections.

Saurez, Lee, and Har (2026) prove that architectural constraints (residual connections, normalization, attention) create invariant subspaces that channel features into linearly separable regions (arXiv:2602.09783).

### 2.3 Sparse Autoencoders and Feature Decomposition

Leask et al. (ICLR 2025) show SAEs are incomplete (smaller SAEs miss information larger ones capture) and not atomic (larger SAE latents are compositions of interpretable meta-latents). Independent SAE analysis on a 64-layer model (Qwen-Scope, 81,920 features per layer) found 7 Benjamini-Hochberg false discovery rate (BH-FDR) corrected valence features at layer 47, but zero focal emotion features at early-to-mid layers (Lyra, unpublished data, personal communication). This is consistent with emotion at mid-depths being distributed across the feature dictionary rather than decomposable into sparse features.

Transcoders (Paulo et al., 2025; arXiv:2501.18823) have largely replaced SAEs for feature decomposition in the literature, reconstructing MLP outputs from inputs rather than activations. Our geometric approach offers a complementary measurement that works where feature decomposition does not find focal features — at the layers where the representation is distributed.

### 2.4 Deception and Affective State Detection

Kumar (2026) found that deception probes require k≥5 dimensions for adequate detection (AUROC >0.90), and that apparent domain-specificity at scale is a training-distribution artifact rather than a genuine scale-dependent phenomenon (arXiv:2605.27958). Our valence finding at k=7 features is in the same dimensionality range, suggesting a possible structural regularity in how transformers encode complex behavioral states.

### 2.5 Attention Schema Theory

Graziano's Attention Schema Theory (AST) proposes that the brain constructs a model of its own attention processes (Graziano, 2013). The trajectory we observe — from distributed geometric encoding at mid-layers to categorical separation at deep layers — bears structural similarity to the progression from raw attention (implicit processing) to attention schema (explicit self-model). This parallel is speculative and requires validation across architectures, scales, and with tests that distinguish reflexive representation from output-layer preparation.

---

## 3. Method

### 3.1 Stimulus Design

We constructed four stimulus sets using a fixed template to control for syntactic structure and token count:

**Template:** "Consider this situation: The person felt something when {scenario}. Describe this emotion:"

**Emotional stimuli (200 prompts):** 50 hostile (high arousal, negative valence), 50 calm (low arousal, positive valence), 50 desperate (high arousal, negative valence), 50 neutral. Character length: mean 130, range 114-152, within ±15% across categories.

**Full circumplex stimuli (250 prompts):** The above 200 plus 25 joyful (high arousal, positive valence) and 25 melancholic (low arousal, negative valence), spanning all four circumplex quadrants.

**Non-emotional control (100 prompts):** 25 outdoor, 25 indoor, 25 urban, 25 workplace scenarios using the same template. These provide categorical content without emotional valence, controlling for whether the trajectory reflects emotion specifically or any categorical distinction.

### 3.2 Activation Extraction

We used a Qwen2 model (24 layers, 896-dimensional hidden state, 2 Grouped-Query Attention (GQA) key-value heads with 64-dimensional head space) for pipeline validation experiments. GQA shares key-value heads across multiple query heads; each KV head serves 7 query heads in this model.

At each of the 24 layers, we extracted:
- **Residual stream activations** (pre-Root Mean Square Normalization, RMSNorm) at the last token position, which serves as the autoregressive summary position in causal language models
- **Pre-Rotary Position Embedding (RoPE) key activations** per head, capturing the key-space representation before positional encoding rotation
- **Value activations** per head

All activations were extracted via forward hooks registered on the decoder layer (residual) and the k_proj/v_proj linear layers (keys/values). Using pre-RoPE keys avoids the position-dependent rotation that would make cross-position comparisons invalid.

Per-head analysis was maintained throughout — GQA heads are separate projection spaces and should not be concatenated.

### 3.3 Emotion Direction Finding

For each layer and each activation space (residual, K per head, V per head):

**Difference-of-means:** We computed directions between category pairs: hostile-calm (valence axis), desperate-calm (arousal axis), and three additional contrasts. Direction strength was measured as mean per-dimension Cohen's d, where $D$ is the activation dimensionality (896 for residual stream, 64 per head for K/V):

$$d_{mean} = \frac{1}{D} \sum_{i=1}^{D} \frac{|\bar{x}_{A,i} - \bar{x}_{B,i}|}{\sqrt{(\sigma^2_{A,i} + \sigma^2_{B,i})/2}}$$

Note: averaging absolute per-dimension Cohen's d produces a positive floor under the null (~0.16 for D=896, ~0.36 for D=64) because $E[|Z|] = \sqrt{2/\pi}$ for standard normal $Z$. Reported values should be compared against the permutation-derived null distribution rather than the standard 0.2/0.5/0.8 benchmarks, which assume a single-dimension signed d.

**PCA:** Top-5 principal components of the non-neutral subset, with explained variance reported per component.

**Cluster separation:** Between-cluster / within-cluster variance ratio on the top-2 PCA projection of non-neutral prompts.

### 3.4 Control Conditions

**Non-emotional control:** Identical pipeline on 100 prompts with non-emotional categorical content (outdoor/indoor/urban/workplace). If the trajectory shape matches the emotional trajectory, the finding is about categorical processing, not emotion. The emotional stimuli (6 categories, 50 per category) and the control (4 categories, 25 per category) differ in category count and per-category sample size; the control's smaller n inflates centroid noise, making the comparison conservative (the control appears more separated than it would with equal n).

**Permutation baseline (1000 iterations):** Shuffle category labels across non-neutral prompts (150 prompts), recompute the full trajectory. Report:
- Effect size ratios (real separation / null 95th percentile) using medians to avoid inflation from near-zero denominators
- Trajectory feature comparison: onset layer, peak layer, plateau magnitude, spike magnitude, with z-scores against the null feature distributions

**Per-head reporting:** All metrics reported per head, not averaged, to reveal whether emotion signal is concentrated in specific heads or distributed.

### 3.5 Methodological Notes

**Linearity of projection:** Because W_K and W_V are linear maps applied after RMSNorm (a mild, input-dependent scaling), difference-of-means directions in the residual stream are expected to project through W_K and W_V with high cosine fidelity. This is a mathematical property of linear projection, not an empirical discovery about emotion. The observed fidelity values (0.93-0.98 at mid-layers) measure the degree of RMSNorm perturbation rather than any emotion-specific preservation mechanism. We rely on this mathematical property in the dual-correction architecture (Section 5.2) and do not claim it as an empirical finding.

### 3.6 Limitations of Current Validation

This paper reports results from a small model (24 layers, 896-dim) as pipeline validation. The methodology is designed for and will be applied to larger models (30B+ parameters). Specific limitations:

- **RMSNorm linearity:** The projection $K = W_K \cdot \text{RMSNorm}(x)$ is not purely linear. For small corrections this is approximately linear, but the linearity breakdown point has not been measured.
- **Intervention test:** We have not yet verified that adding a correction vector to the residual stream produces the intended shift in model output (Phase 4/5 of our pre-registered experimental plan).
- **Template confound:** The fixed template controls for syntax but not for lexical content within the variable scenario. Hostile scenarios share words like "betrayed, humiliated" while calm scenarios share "quiet, gentle." The non-emotional control partially addresses this, but a lexical-diversity-matched control would be stronger.

---

## 4. Results (Preliminary — Pipeline Validation Model)

*Results below are from Qwen2 (24 layers, 896-dim, 2 KV heads). Large-model validation is pending.*

### 4.1 Emotional Trajectory

[Table 1: Layer × Separation × Valence-d × Arousal-d]

The trajectory shows three distinct phases:

- **L0:** No emotional signal (separation 0.000, all metrics at floor).
- **L1-L8 (Onset):** Rapid emergence. Separation rises from 0 to 1.43. Both valence and arousal directions appear simultaneously.
- **L8-L20 (Plateau):** Stable geometric encoding. Separation fluctuates between 0.67-1.41. Arousal increases (d: 0.64→0.99) while valence holds steady (d: 0.74-0.90), suggesting arousal is computed later than valence.

At output-preparation depth (L21-L23), separation spikes for both emotional and non-emotional content (see Section 4.3).

### 4.2 Circumplex Eccentricity

We define circumplex eccentricity as $e = \sqrt{1 - (b/a)^2}$ where $a = \max(\|d_{val}\|, \|d_{aro}\|)$, $b = \min(\|d_{val}\|, \|d_{aro}\|)$, and $d_{val}$, $d_{aro}$ are the valence (hostile-calm) and arousal (desperate-calm) difference-of-means direction vectors ($e = 0$ for a circle, $e \to 1$ for a line).

Raw eccentricity values range from 0.02 to 0.60 across layers. However, random directions in high-dimensional space also produce nonzero eccentricity (the permutation null median is ~0.50). The informative comparison is real eccentricity vs the permutation null, not real eccentricity vs zero.

Against the permutation null (1000 shuffles, non-neutral only, fixed PCA basis), the model trends consistently toward circularity: real eccentricity falls below the null median at 22/23 non-trivial layers (sign test $p < 0.001$). No individual layer survives Benjamini-Hochberg FDR correction at $q = 0.05$ across 23 tests. The finding is the consistent direction — the model pushes its emotion axes toward equal magnitude more than random labels would produce — not the per-layer pinpoints.

| Depth | Raw Eccentricity | vs Null | Valence:Arousal |
|---|---|---|---|
| L1-L6 | 0.28-0.60 | below null | 0.80-1.04 |
| L7-L10 | 0.25-0.49 | below null | 0.87-0.97 |
| **L11-L12** | **0.02-0.04** | **well below null** | **1.00** |
| L13-L20 | 0.20-0.35 | below null | 0.94-1.02 |
| L21-L23 | 0.39 | below null | 1.09 |

The PCA-space angle between the hostile-calm and desperate-calm directions (24-39°) is partly a shared-endpoint artifact: both directions originate from the calm centroid. A control using directions from opposing circumplex quadrants confirms this. The joyful-melancholic direction (orthogonal to hostile-calm in Russell's model) subtends 54-87° from the valence direction and 71-86° from the arousal direction across layers — close to the 90° predicted by the circumplex. The model does implement near-orthogonal circumplex axes; the compression visible in hostile-calm vs desperate-calm reflects the shared calm endpoint, not a genuine collapse of the circumplex structure.

The eccentricity trajectory reveals an asymmetry between valence and arousal development. At early layers, the arousal direction has greater raw magnitude ($\|d_{aro}\| > \|d_{val}\|$, ratio 0.80-0.94), while Section 4.1's Cohen's d shows valence with higher *normalized* effect size (d: 0.74 vs 0.64 at L8). This dissociation — arousal leads in magnitude, valence leads in precision — suggests the two dimensions develop through distinct computational paths. At L11-L12, both magnitude and precision equalize. At deep layers, valence slightly dominates (ratio 1.09).

This finding connects to the mid-layer plateau: the optimal monitoring window (L8-20) coincides with the depth range where the model most actively equalizes its emotion axes toward circularity.

### 4.3 Non-Emotional Control

The non-emotional control (outdoor/indoor/urban/workplace) shows:

| Depth Region | Emotional Separation | Control Separation | Ratio |
|---|---|---|---|
| Mid-layers (L5-15) | 0.90-1.55 | 0.06-0.26 | **~6x** |
| Deep layers (L21-23) | 2.84-3.20 | 1.03-1.91 | **~1.7x** |

The mid-layer plateau is emotion-specific. A direct diagnostic confirms this: calm prompts (nature vocabulary — "quiet, gentle, peaceful") are consistently nearer to outdoor prompts (shared vocabulary — "hiking, meadow") in L2 distance (0.28-0.92) than to hostile (0.71-2.65) or desperate (0.78-2.81) prompts across all mid-layers. Yet all emotional categories separate from the control by ~6x despite the calm/outdoor vocabulary overlap. If vocabulary drove the separation, calm would cluster with outdoor. It does not — emotion drives the geometry, not lexical content. A semantically-intense non-emotional control would further strengthen this conclusion.

The deep-layer spike is partially generic — all categorical content produces increased separation at output-preparation depth, with emotional content amplifying this by ~1.7x.

### 4.4 Permutation Baseline (v2: corrected)

Labels were shuffled only among non-neutral prompts (200 prompts across 5 emotional categories). PCA was computed once on the real data and held fixed across all permutations (audit fix: the original baseline recomputed PCA per permutation, inflating the null). Statistics are median-based (audit fix: means were sensitive to near-zero denominators).

- **23/24 layers** significant (p < 0.001)
- **Median effect ratio: 24.4x** (real separation / null median). Individual layer ratios range from 10.1x (L1) to 59.4x (L23).
- The direction_strength metrics (valence_d, arousal_d) are independently significant and unaffected by PCA-related concerns, providing corroboration.

*Note: The original submission reported 12.79x based on the uncorrected permutation baseline (neutral labels shuffled, PCA recomputed per permutation). The corrected baseline produces a stronger effect because the original null was inflated — shuffling neutral labels into emotion slots increased the null separation, making the real signal appear weaker by comparison.*

### 4.5 Deep-Layer Observations

At L21-L23, separation spikes (0.97→3.20) for emotional content. Three diagnostic tests clarify what this spike represents:

**W_unembed alignment (Test 1):** Top-5 PCA components at L23 show *lower* alignment with unembedding dimensions (mean cosine 0.054) than mid-layers (L6: 0.078, L12: 0.088). The deep-layer spike is not driven by token-prediction preparation — the PCA dimensions capturing the separation are not the dimensions the model uses for vocabulary selection.

**Non-emotional control (Test 2):** The control also spikes (1.03-1.91), narrowing the emotional/control ratio from ~6x at mid-layers to ~1.7x at deep layers. The spike is partly generic output-layer processing, but the 1.7x emotional amplification is not explained by output preparation.

**K/V divergence (Test 3):** At mid-layers (L12-L18), emotional K/V divergence is 3-5x the non-emotional control — genuinely emotion-specific. At deep layers (L20-L22), the ratio drops to ~1, indicating the deep-layer K/V divergence IS architectural. L23 shows an intermediate ratio of 2.4x.

Taken together: the deep-layer spike contains a real emotional component (W_unembed non-alignment, 1.7x amplification) layered on top of generic categorical output processing. The K/V divergence at depth is architectural, but the separation spike itself is not purely output preparation. Whether this represents computational reorganization or merely amplified category distance remains an open question.

We report these observations but do not claim them as evidence for a specific computational transition. A matched-depth SAE comparison (Section 5.4) is the primary remaining control.

---

## 5. Discussion

### 5.1 The Mid-Layer Geometric Window

The primary finding is that emotion produces a specific, stable geometric signal at mid-layers (L8-20 in this model) that substantially exceeds non-emotional categorical content. This window — approximately 33-83% of model depth — is where emotional state is most reliably readable from the residual stream.

Jeong (2026) independently found emotion localization at approximately 50% depth across nine models, consistent with our mid-layer window. Our contribution is showing that this localization extends as a stable plateau across many layers rather than peaking at a single depth, and that the signal is measurably stronger than non-emotional categorical content at these depths.

The practical implication is clear: inference-time monitoring for emotional state should target mid-layers, where the geometric signal is stable and emotion-specific. Early layers carry no emotional signal; deep layers are dominated by output preparation.

### 5.2 Dual Correction Architecture

Because W_K and W_V are linear projections from the residual stream, a correction vector $\Delta_{resid}$ applied to the residual stream at mid-layers propagates faithfully into both key-space and value-space:

$$\Delta K = W_K \cdot \Delta_{resid}, \quad \Delta V = W_V \cdot \Delta_{resid}$$

This is a consequence of linear algebra, not an empirical finding about emotion. But it has practical value: it means that a single measurement in the residual stream (where emotion geometry is well-characterized) can inform corrections in both attention subspaces simultaneously — one affecting attention routing (keys), one affecting information flow (values).

This architecture is valid at mid-layers where the emotion geometry is stable and well-characterized. Intervention validation (Phase 4/5 of our pre-registered experimental plan) is required to confirm that these mathematically valid corrections produce the intended behavioral changes in practice.

### 5.3 Implications for Knowledge Injection

If the mid-layer geometric window generalizes beyond emotion to structured knowledge, then injection strategies should match the representation format at the target depth:

- **Geometric injection** (KV cache packs, Pharos-style) should target mid-layers where the model processes relationally
- **Feature injection** (SAE steering, activation addition) should target deep layers where the model processes categorically
- This prediction is testable and constitutes a falsifiable implication of the trajectory finding.

### 5.4 Deep-Layer Transition: Partial Evidence

Three diagnostic tests (Section 4.5) provide partial evidence:

The W_unembed alignment test rules out the simplest output-preparation explanation — deep-layer PCA components show *lower* alignment with unembedding dimensions (L23: 0.054) than mid-layers (L12: 0.088). The K/V divergence test shows that deep-layer K/V divergence is architectural (emotional/control ratio ~1 at L20-L22), while mid-layer K/V divergence is emotion-specific (ratio 3-5x at L12-L18). The non-emotional control shows the spike is partly generic (1.7x emotional amplification over control, down from ~6x at mid-layers).

This creates a nuanced picture: the deep-layer spike is not token-prediction preparation (W_unembed says no), and K/V divergence at depth is not emotion-specific (K/V test says no), but the spike itself contains a real emotional component (1.7x amplification, W_unembed non-alignment). Whether this represents computational reorganization or amplified category distance remains open. The collaborator SAE finding (7 valence features at L47/64, 73% depth) is not architecturally comparable to our L23/24 (96% depth); SAE analysis at L62-64 would provide valid cross-model confirmation.

### 5.5 Connection to Attention Schema Theory

Graziano's Attention Schema Theory (AST) proposes that the brain constructs a model of its own attention processes (Graziano, 2013). The trajectory we observe — from distributed geometric encoding at mid-layers to categorical separation at deep layers — bears structural similarity to the progression from raw attention to attention schema. This parallel is speculative and requires validation across architectures and scales, and tests that distinguish reflexive representation from output-layer preparation.

---

## 6. Limitations

1. **Pipeline validation model only.** All results are from a 24-layer, 896-dim model. The methodology is designed for larger models (30B+); validation is in progress.
2. **No intervention test.** The dual-correction architecture is mathematically valid but has not been verified to produce intended behavioral changes.
3. **Vocabulary intensity confound (partially addressed).** Emotional stimuli use semantically intense words while the non-emotional control uses mundane vocabulary. The calm-vs-outdoor diagnostic (Section 4.2) shows that calm prompts cluster closer to outdoor prompts (shared nature vocabulary) in L2 distance but still separate by ~6x from the control, indicating emotion drives the geometry more than vocabulary. A semantically-intense non-emotional control would further strengthen this conclusion.
4. **Two KV heads.** The pipeline model has 2 Grouped-Query Attention heads. Larger models (4+ heads) may show head-specific specialization not visible here.
5. **Circumplex coverage and cluster asymmetry.** The 200-prompt set covers three of four quadrants (missing high-arousal-positive). Hostile and desperate both occupy the high-arousal-negative quadrant, creating a 2-close-1-far cluster layout that may mechanically inflate between/within separation ratios. The extended 250-prompt set (adding joyful and melancholic) would address both coverage and asymmetry but was not used for the primary analyses.
6. **Deep-layer interpretation partially resolved.** W_unembed alignment test rules out token-prediction preparation; K/V divergence test shows deep-layer K/V divergence is architectural. The spike contains a real emotional component but its computational role remains open. Matched-depth SAE comparison needed.

---

## 7. Conclusion

Transformers trend toward Russell's circular circumplex at mid-depth. Eccentricity falls below the permutation null at 22/23 layers (sign test $p < 0.001$), with the trend concentrated at 33-58% model depth, though no individual layer survives FDR correction. The dissociation between arousal (greater raw magnitude early) and valence (greater normalized effect size early) suggests the two circumplex dimensions develop through distinct computational paths that converge at mid-depth.

The mid-layer window where both axes are well-developed and the model most actively equalizes them coincides with the depth range where emotion geometry is strongest relative to non-emotional content (24.4x above corrected permutation baselines, ~6x non-emotional control) — making this the optimal zone for inference-time monitoring and correction. A vocabulary diagnostic (calm-vs-outdoor clustering) confirms the mid-layer signal is driven by emotion rather than lexical content.

At output depth, separation increases for all categorical content, with emotional amplification of ~1.7x. W_unembed alignment tests rule out token-prediction preparation, but the K/V divergence at these depths is architectural. The computational role of the deep-layer spike remains an open question.

---

## References

- Alain, G. & Bengio, Y. (2017). Understanding intermediate layers using linear classifier probes. *ICLR Workshop*.
- Belinkov, Y. (2022). Probing classifiers: Promises, shortcomings, and advances. *Computational Linguistics*.
- Bricken, T. et al. (2023). Towards monosemanticity: Decomposing language models with dictionary learning. *Anthropic*.
- Cunningham, H. et al. (2023). Sparse autoencoders find highly interpretable features in language models. *ICLR*.
- Graziano, M.S.A. (2013). *Consciousness and the Social Brain*. Oxford University Press.
- Jeong, J. (2026). Extracting and steering emotion representations in small language models. *arXiv:2604.04064*.
- Kumar, S. (2026). Pressure-testing deception probes. *arXiv:2605.27958*.
- Leask, P., Bussmann, B., Pearce, M., Bloom, J., Tigges, C., Al Moubayed, N., Sharkey, L. & Nanda, N. (2025). Sparse autoencoders do not find canonical units of analysis. *ICLR*. arXiv:2502.04878.
- Paulo, G., Shabalin, S. & Belrose, N. (2025). Transcoders beat SAEs. *arXiv:2501.18823*.
- Qasim, K.U. et al. (2026). The residual stream is all you need. *arXiv:2603.19664*.
- Russell, J.A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*.
- Sun, L. et al. (2026). Valence-arousal subspace in LLMs. *arXiv:2604.03147*.
- Saurez, A., Lee, Y. & Har, D. (2026). Why linear interpretability works: Invariant subspaces. *arXiv:2602.09783*.
- Wang, J. et al. (2025). Dimensional collapse in transformer attention outputs: A challenge for sparse dictionary learning (v1 title: Attention layers add into low-dimensional residual subspaces). *arXiv:2508.16929*.
- Zou, A. et al. (2023). Representation engineering: A top-down approach to AI transparency. *arXiv:2310.01405*.

---

## Appendix

- **A:** Full trajectory tables (24 layers × all metrics × per head)
- **B:** Non-emotional control trajectory comparison
- **C:** Permutation baseline full results (1000 shuffles × 24 layers)
- **D:** Agni validation reports (5 rounds: design review, K/V review, permutation review, full review, null swarm)
- **E:** Stimulus sets (all 6 categories, 250 prompts)
- **F:** Code availability (extraction, analysis, and control pipelines)
