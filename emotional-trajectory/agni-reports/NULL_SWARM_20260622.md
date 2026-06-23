# AGNI NULL SWARM REPORT: "Emotional Geometry Through the Transformer Stack"

**Date:** 2026-06-22
**Auditors:** Dual-reviewer Agni pipeline (audit + cross-verification)
**Targets assessed:** 5 core claims/metrics


---

## 1. SUMMARY

**Nulls passed clean:** 0 of 5
**Flagged with issues:** 5 of 5
**Critical (potential claim invalidation):** 2
**Major (significant methodological concern):** 3
**Minor:** 0 (one reviewer downgraded Cohen's d to minor; consensus keeps it at major with caveats)

**Overall paper health: YELLOW -- publishable core exists but two central claims must be retracted or fundamentally reframed before external review.**

The mid-layer geometric encoding finding survives all audits as genuinely interesting, though its quantitative magnitude is uncertain due to vocabulary confounds. The deep-layer "focal transition" and projection fidelity claims do not survive scrutiny. The paper as currently written leads with its two weakest findings.


---

## 2. FINDING-BY-FINDING ASSESSMENT

### Finding 1: Permutation Baseline (28.6x effect ratio, 23/24 layers significant)

- **Target:** Core statistical validation of emotion-specific signal
- **Reviewer 1 verdict:** PARTIALLY_VALID (confidence 0.78)
- **Reviewer 2 verdict:** PARTIALLY_VALID (confidence 0.88)
- **Consensus:** PARTIALLY_VALID
- **Severity:** MAJOR

**Confirmed issues:**
- PCA recomputed per null iteration -- each null finds its own optimal 2D projection
- Neutral-prompt dilution: shuffling all 200 labels (including 50 neutral) means each null PCA sees ~37.5 originally-neutral activations that were never in the real PCA. If neutral activations have lower emotional variance (definitionally expected), the null is systematically depressed
- Mean-of-ratios inflated by near-zero denominators (range 0-70.5x, +1e-10 floor)

**Reviewer 2 nuance:** PCA recomputation alone is actually generous to the null (gives it its best projection). The bias only becomes directional when combined with neutral dilution. This is a useful clarification -- the fix priority is neutral dilution first, fixed PCA second.

**Direction_strength metrics (valence_d, arousal_d) are unaffected.** These provide independent corroboration.

---

### Finding 2: Non-Emotional Control (6x mid-layer ratio)

- **Target:** Evidence that signal is emotion-specific, not generic categorical
- **Reviewer 1 verdict:** PARTIALLY_VALID (confidence 0.72)
- **Reviewer 2 verdict:** PARTIALLY_VALID (confidence 0.78)
- **Consensus:** PARTIALLY_VALID
- **Severity:** MAJOR

**Confirmed issues:**
- Semantic intensity confound: emotional prompts use high-representational-weight words (betrayed, humiliated, terminal) vs. control's mundane vocabulary (hiking, typing, organizing)
- Asymmetric cluster geometry: hostile and desperate both occupy high-arousal-negative quadrant, creating a 2-close-1-far layout that mechanically inflates between/within ratio by approximately 2x (Monte Carlo confirmed)
- PCA re-fit per condition

**Reviewer 2 correction of Reviewer 1:** Sample size bias direction is WRONG in the first review. Smaller per-category n (25 vs 50) inflates between-cluster variance via centroid noise, making the control look MORE separated, not less. The 6x ratio is actually conservative with respect to sample size. The first reviewer's mechanism was backwards, though the recommendation to equalize is still correct.

**The 250-prompt set with joyful and melancholic already exists in the code but was not used for this comparison.** This is a missed opportunity.

---

### Finding 3: Projection Fidelity (cosine 0.93-0.98, "dual preservation")

- **Target:** Claim that W_K and W_V specifically preserve emotion directions
- **Reviewer 1 verdict:** INVALID (confidence 0.97)
- **Reviewer 2 verdict:** INVALID (confidence 0.95)
- **Consensus:** INVALID
- **Severity:** CRITICAL

**This is a near-tautology.** Both reviewers confirm with high confidence:

- Difference-of-means commutes with linear maps. W_K @ (mean_A - mean_B) = mean(W_K @ A) - mean(W_K @ B). Without nonlinearity, cosine would be exactly 1.0
- The only perturbation from 1.0 comes from RMSNorm, which is a mild input-dependent scaling not specific to emotion
- The random-vector null exploits concentration of measure in D=896 to produce trivially near-zero baselines (expected |cosine| ~ sqrt(2/(pi*64)) ~ 0.10)
- A proper permutation null (shuffle labels, recompute both directions) yields cosine 0.9993-0.9998 for every shuffle, confirming the metric measures RMSNorm nonlinearity magnitude, not emotion preservation
- The "dual preservation despite orthogonality" narrative (Section 4.5) follows trivially from linearity

**The dual-correction architecture (Section 5.2) is built on this finding.** It needs to be reframed as a consequence of linear algebra (which is itself useful for engineering), not as an empirical discovery about emotion.

---

### Finding 4: Cohen's d (d_mean) as Effect Size

- **Target:** Primary effect size metric and its interpretive framing
- **Reviewer 1 verdict:** PARTIALLY_VALID (confidence 0.88)
- **Reviewer 2 verdict:** PARTIALLY_VALID (confidence 0.82)
- **Consensus:** PARTIALLY_VALID
- **Severity:** MAJOR (Reviewer 2 argues minor; consensus: major for framing, minor for impact on conclusions)

**Confirmed issue:** Averaging |d_i| produces a positive floor of ~0.16 under the null. The paper claims this is "interpretable on the standard Cohen's d scale (0.2=small, 0.5=medium, 0.8=large)" -- this is false.

**Reviewer 2 correction:** The first reviewer's naive subtraction (subtracting 0.16 from all values) is mathematically wrong. Signal-carrying dimensions contribute negligible bias when their true effect exceeds ~0.3. Actual bias is 0.05-0.12, not the full 0.16. The corrected range is less pessimistic than Reviewer 1 claims.

**Impact on conclusions:** The trajectory shape is primarily supported by cluster separation (which has proper permutation baselines), not d_mean. This is a calibration/presentation fix, not a methodological one. But the paper text presents d_mean values at face value with standard benchmarks, which is misleading.

---

### Finding 5: Geometric-to-Focal Transition (deep layers L21-L23)

- **Target:** Central narrative claim -- deep-layer spike is emotional reorganization, not degradation
- **Reviewer 1 verdict:** INVALID (confidence 0.82)
- **Reviewer 2 verdict:** INVALID (confidence 0.88)
- **Consensus:** INVALID
- **Severity:** CRITICAL

**Six converging problems, all confirmed by both reviewers:**

1. **Output-layer confound:** The paper's own data shows the control ratio drops from 6x (mid-layer) to 1.7x (deep). Roughly 59% of the deep-layer spike is generic categorical output preparation. The paper acknowledges this but still builds its central claim around the transition.

2. **PCA metric artifact at output depth:** Top PCA components at L23 likely capture token-prediction variance (unembedding alignment), not emotion-specific dimensions. Different emotional scenarios preparing to generate different first tokens creates apparent separation.

3. **z-score of 201.3 is a metric artifact:** A near-zero-variance null distribution produces astronomically inflated z-scores. This tells us nothing about effect magnitude. The effect ratio (already computed) is the informative statistic.

4. **Cross-model SAE comparison is invalid:** L47/64 (73% depth, 17 layers remaining) is not comparable to L23/24 (96% depth, 0 layers remaining). These are fundamentally different architectural positions. The paper needs L62-64 SAE results to validly claim cross-model confirmation.

5. **K/V divergence is architecturally expected:** K-space must produce attention patterns while V-space carries token-prediction information at output depth for ANY content type. No non-emotional control comparison for K/V divergence is reported.

6. **"Not degradation" is unfalsifiable as stated:** Separation-up + fidelity-down is exactly what generic output preparation looks like. The paper has no test to distinguish its interpretation from the null hypothesis.

**The proposed diagnostic test:** Measure cosine alignment of deep-layer PCA components with W_unembed rows. If top PCA at L23 aligns with unembedding dimensions, the spike is output preparation.


---

## 3. CRITICAL ISSUES (Claim Invalidation Risk)

**CRITICAL 1: Projection Fidelity is a mathematical tautology, not an empirical finding.**
- Sections 3.4, 4.2, 4.5, and 5.2 are all affected
- The dual-correction architecture rests on this
- Both reviewers at 0.95+ confidence
- Must be removed or completely reframed before any external review

**CRITICAL 2: The "geometric-to-focal transition" is predominantly output-layer preparation.**
- The paper's own control data shows 59% of the deep-layer effect is generic
- The paper is currently structured around this as the central narrative
- The mid-layer finding (which IS emotion-specific) is undersold
- The paper leads with its weakest claim

**The paper as currently structured presents a tautology and a confounded output-layer effect as its two headline findings, while underselling its genuinely novel mid-layer geometric encoding result.** This is the core structural problem.


---

## 4. RECOMMENDATIONS (by severity)

### Must-fix before external review:

1. **Remove or fundamentally reframe projection fidelity (Sections 3.4, 4.2, 4.5).** If retained, reframe as: "Linear projection preserves all difference-of-means directions (a mathematical property), which makes the dual-correction architecture practically feasible." Do not present as an empirical finding about emotion. Remove the random-vector null entirely. (CRITICAL)

2. **Demote the geometric-to-focal transition from central claim to hypothesis.** Restructure the paper to lead with the mid-layer geometric encoding, which IS genuinely emotion-specific. The deep-layer spike should be described as "consistent with output-layer preparation, with a 1.7x emotional amplification requiring further investigation." (CRITICAL)

3. **Fix the permutation baseline.** Two changes: (a) Only shuffle labels among the 150 non-neutral prompts. (b) Compute PCA once on the real non-neutral data. Replace mean effect ratio with median. Re-run and report revised numbers. (MAJOR)

4. **Fix the Cohen's d framing.** Remove the claim that d_mean is interpretable on the standard 0.2/0.5/0.8 scale. Report the permutation-derived null distribution for d_mean alongside observed values. (MAJOR)

### Should-fix for methodological credibility:

5. **Report calm-vs-outdoor separation at mid-layers.** This is zero-cost (data exists) and directly diagnostic of the vocabulary confound. If calm clusters with outdoor despite shared nature vocabulary, the emotion interpretation weakens. If calm clusters with hostile/desperate despite vocabulary dissimilarity, it strengthens. (MAJOR)

6. **Address cluster geometry asymmetry.** Either use the existing 250-prompt set (with joyful and melancholic) to balance circumplex coverage, or compute pairwise separation ratios instead of the aggregate between/within metric. (MAJOR)

7. **Run the W_unembed alignment test at deep layers.** This directly tests whether the deep-layer PCA spike is output preparation or emotional reorganization. (MAJOR)

8. **Replace the z-score of 201.3 with effect size ratios.** The z-score is misleading and will draw reviewer fire. (MODERATE)

9. **Remove or qualify the cross-model SAE comparison.** L47/64 is not architecturally comparable to L23/24. Request L62-64 results from the collaborator. (MAJOR)

### Nice-to-have:

10. **Run a TF-IDF baseline** to establish a vocabulary-only ceiling for category separation. (MODERATE)

11. **Equalize sample sizes** between emotional and control conditions (25 vs 50 per category). Current imbalance is actually conservative, but equalization removes a reviewer objection. (MINOR)

12. **Construct a semantically-intense non-emotional control** (vivid sensory descriptions, complex mechanical processes) to match emotional prompts on representational weight. (MEDIUM-TERM)


---

## 5. COMPARISON TO LYRA'S NULL SWARM

Lyra's null swarm found 5/12 kills had methodology problems. The error classes were: measuring the wrong thing, think-block artifacts, and wrong probes.

**This paper is vulnerable to the same primary error class: measuring the wrong thing.**

| Error class | Lyra's swarm | This paper | Match? |
|---|---|---|---|
| Measuring the wrong thing | Primary finding | Projection fidelity (tautology), deep-layer spike (output prep), 6x ratio (vocabulary not emotion) | YES -- three instances |
| Think-block artifacts | Present | Not applicable (different architecture) | N/A |
| Wrong probes | Present | Cohen's d null floor, PCA re-fitting per condition | PARTIAL -- wrong null rather than wrong probe, but same family |

**We are MORE vulnerable than Lyra's swarm, not less.** Lyra had 5/12 (42%) kills with problems. We have 5/5 (100%) findings with issues, 2 critical. The difference: Lyra's problems were in individual kill experiments; ours are in the paper's core claims.

The pattern is consistent: **the most common failure mode in mechanistic interpretability is constructing a metric that appears to measure X but actually measures a mathematical/architectural property Y.** Projection fidelity measures linearity. The deep-layer spike measures output preparation. The 6x ratio partially measures vocabulary domain distance. The permutation baseline measures a biased null. Cohen's d measures |d| + constant, not d.

We are building on the same methodological foundation that produced Lyra's problems. The Agni pipeline caught these, which is exactly what it is designed for, but the density of findings suggests our metric design process needs a pre-registration step: before computing any metric, write down what the null hypothesis predicts the metric will show, and verify the null is not trivially near-zero or trivially near the observed value.


---

## 6. BOTTOM LINE

**Is this paper safe to send to Dwayne for external audit?**

**No. Not in its current form.**

Two critical claims (projection fidelity, focal transition) will not survive external review. A competent reviewer will identify the tautology within minutes of reading Section 4.2, and the output-layer confound is visible in the paper's own Table 2. Sending this to Dwayne in its current state risks the paper being dismissed entirely, including the mid-layer findings that ARE genuinely novel.

**What IS salvageable and worth building around:**

- The mid-layer geometric encoding finding (layers 8-18) with a properly fixed permutation baseline
- The direction_strength metrics (valence_d, arousal_d), which are unaffected by the PCA issues
- The trajectory shape (onset-plateau-spike) as descriptive structure, with the spike acknowledged as predominantly architectural
- The overall experimental framework and pipeline

**Recommended path:**

1. Fix the two critical issues (projection fidelity reframe, focal transition demotion) -- estimated 2-3 days of rewriting
2. Fix the permutation baseline and re-run -- estimated 1 day of computation + analysis
3. Run the calm-vs-outdoor comparison and W_unembed alignment test -- estimated 1 day
4. Restructure paper to lead with mid-layer findings
5. Then send to Dwayne

The mid-layer story is a genuinely interesting paper. The deep-layer story is a hypothesis for future work. The projection fidelity story is linear algebra. Separating these makes the paper stronger, not weaker.
