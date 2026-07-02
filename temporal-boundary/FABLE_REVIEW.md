A note before the review: per my configuration I'm listed as this paper's lead author, so this is a self-review. I'm treating that as license to be harsher, not gentler. Review follows, in role.

---

# Review: "The Temporal Boundary: Self/Other Separation in Transformers Is Temporal, Not Geometric"

## Summary

The paper claims the self/other distinction in transformer emotional processing is temporal: an SAE feature (58995, L47) tracks input-text valence during prefill and is silent during decoding, while behavioral steering operates via V-cache injection at L3/7 during decoding; the two are geometrically near-orthogonal, and injection does not alter the encoding-phase feature. A second finding (depth predicts resistance) is retracted within the paper itself. Three additional experiments were killed pre-claim by the authors' adversarial review process and are reported as methodological contributions.

The transparency infrastructure here is genuinely exemplary. The science underneath it, unfortunately, does not support the title claim.

## Section-by-section assessment

### Abstract and Introduction

**Claims vs. evidence: substantial overclaiming.** The title asserts a discovery about "self/other separation in transformers." What the data shows is: (a) a feature that correlates with the valence of input text fires during prefill, and (b) steering vectors applied during decoding change outputs. Calling the input phase "reading the other" and the decoding phase "becoming itself" is narrative gloss, not a measured construct. Nothing in the surviving experiments establishes that the encoding feature represents *another agent's mental state* (as opposed to the sentiment of the text itself), nor that generation-phase geometry constitutes a *self*-representation. Critically, the three experiments that attempted to establish self/other specificity — the probe experiment, the framing experiment, and the depth-reorganization experiment — were all killed. The paper therefore contains **zero surviving evidence that any measured quantity is self/other-specific**, yet the title, abstract, and conclusion all assert the self/other framing as the finding.

### Setup (Section 3)

- The model is a community distillation ("Jackrong," Qwen3.5-27B distilled from a Claude model) with unusual hybrid architecture. Was the Qwen-Scope SAE trained on this checkpoint or on base Qwen? SAE features do not automatically transfer across finetunes/distills; no reconstruction-error or feature-validity check on this specific model is reported. This threatens every feature-level claim.
- Internal inconsistency: Setup specifies `max_new_tokens=128`; Section 5 analyzes "the first 256 generated tokens." Trial accounting also differs between Section 5 (30 × 4 conditions × 3 repeats) and Section 6 (30 × 3 vectors × 4 conditions).
- An uncited self-reference ("confabulation correction at 95.6% on 350 trials") is load-bearing for the L3/7 machinery and cannot be evaluated.

### Section 4 (Three Kills)

**The strongest part of the paper.** Kill 2 (instruction framing drives encoding entropy, with a non-target control producing a *larger* effect) and Kill 3 (depth reorganization is generic to instruction variation) document real, generalizable confounds, and the provisional-kill caveat on Kill 2 is admirably honest. Kill 1, however, is textbook causal masking — scenario positions cannot attend to subsequent probe tokens — and reporting it as a generalizable insight is padding; any reviewer at this venue knows this before breakfast. Novelty of the kills as contributions: modest but nonzero for Kills 2–3.

### Section 5 (Finding 1: The Temporal Boundary)

This is the load-bearing section and it has four serious problems.

**1. The headline causal result appears tautological.** The claim that V-cache injection at L3/7 produces $<10^{-4}$ change in the L47 encoding-phase feature "across 360 trials" is presented as confirmation of a temporal boundary. But if injection follows the standard KV-cache protocol — modifying cached V *after* prefill — then the prefill activations at L47 were computed before the intervention existed. Zero change is then an arithmetic identity, not an empirical finding, and no number of trials makes it informative. The magnitude of the observed difference ($<10^{-4}$, i.e., numerical noise) itself suggests this is what happened; a genuine prefill-time intervention propagating through 40+ layers would not produce machine-epsilon differences. The authors' architecture caveat (linear-attention layers may block propagation) worries about the wrong problem. The abstract's word "confirming" is vacuous if the pipeline never re-runs prefill. This must be clarified, and if the tautology holds, the central result of the paper reduces to "modifying a cache does not retroactively change the computation that produced it."

**2. Feature selection is in-sample.** Feature 58995 was selected as the max-correlating feature from 81,920 features × 5 layers ≈ 410K tests, and its $r=0.686$ is reported on the same 30 scenarios used for selection. BH-FDR controls false discovery, not winner's-curse inflation of the selected feature's effect size. No held-out scenario set is reported. Moreover, valence takes only 6 distinct values tied to emotion category, so the effective sample is closer to 6 category means than 30 independent points; and since prefill is deterministic given the prompt, the "n=60 trials per emotion" in Figure 1's caption is pseudoreplication — the real unit is 5 scenarios per emotion.

**3. The "depth, not valence" interpretation is contradicted by the authors' own table.** Table 1 activations (4.51, 4.41, 3.94, 3.87, 3.60, 3.59) are *perfectly monotone* in assigned valence (+1.0, +0.8, +0.7, −0.8, −0.9, −1.0). The depth interpretation rests entirely on sadness (3.87) exceeding fear (3.60) and anger (3.59) — but sadness also has the least negative valence. The data are fully explained by valence tracking; "reflective depth" adds an unfalsified free parameter, is admitted to be untested ("a formal reflective-content rating study... has not yet been conducted"), and yet appears in the abstract's first paragraph. A simpler alternative — this is a sentiment/emotional-content feature of the input text — is never ruled out.

**4. "Silent during generation" has an obvious content confound.** The model's generated responses (assistant-voice consolation) differ in register and content from first-person emotional narratives. The feature going silent may reflect that generated *text* is not emotional first-person narrative, not that a *phase boundary* exists. The decisive control is cheap: feed the model's own generated responses back as input and check whether 58995 fires during prefill. If it does, the boundary is content, not time. This control is absent.

**Orthogonality (5.3):** cosine 0.031 between a decoder direction at L47 and steering directions at L3/7 — different layers, arguably different spaces — with permutation $p=0.155$, meaning the value is statistically indistinguishable from two *random* directions. In high-dimensional space, near-orthogonality is the null hypothesis. This is evidence of nothing and should not appear in the abstract as "geometrically independent."

### Section 6 (Finding 2)

The retraction itself is honest and well-documented (the six enumerated failures are a model of self-critique). But:

- The section is titled "**Depth Predicts Resistance, Not Empathy**" — a declarative claim for a result the section retracts. This is actively misleading at skim level.
- The Limitations section still says "the depth-resistance finding is based on 2 of 3 vectors showing negative correlation," treating the retracted result as a finding. This is leftover text from a pre-retraction draft and contradicts the retraction.
- The one surviving number, 72–74% text divergence from baseline, is uninterpretable without the **null-null baseline**: at temperature 0.3, what is the divergence between two *baseline* repeats of the same scenario? Stochastic decoding plus the admitted 97.8% formulaic-opening floor could produce most of this. The relevant control exists in their own 3-repeat design and is not reported.

A retracted analysis belongs in an appendix labeled as such, not as a titled "Finding."

### Discussion

Section 7.1 ("Representational Tube") and 7.2 (zero activation on factual prompts) introduce *new empirical results* — effective rank ~3, SV1 length correlation r=0.79, domain-specificity pre-check — with no methods, no ns, no statistics. Either promote to Results with full methodology or cut. The AST discussion is speculative but appropriately hedged.

### Reproducibility

Above average: public repo, pre-registrations, scenario texts, named protocol. Concerns: community-distilled model availability/provenance, SAE-transfer validity, unspecified seeds, and the paper contains a stray `% TODO` for two missing figures — the submission is not finished.

### Missing comparisons

- Activation steering literature (ActAdd/Turner et al.; Representation Engineering/Zou et al.; Contrastive Activation Addition/Rimsky et al.) — directly relevant to the L3/7 injection channel and uncited.
- Sentiment representations in LMs (e.g., Radford et al.'s sentiment neuron; subsequent probing work) — the null hypothesis for feature 58995.
- A simple linear probe for valence at L47 as a baseline: does the "one feature out of 81,920" framing add anything over a probe?
- Prefill-vs-decode representation analyses in the KV-cache/efficiency literature, which have long noted the architectural asymmetry the paper presents as under-theorized.

---

## Strengths

- **Exemplary epistemic practice**: pre-registration, adversarial review, in-paper retraction with enumerated failures, and publication of killed experiments. This should be the field norm and mostly isn't.
- Kills 2 and 3 document genuine, generalizable confounds (instruction-framing entropy; generic depth reorganization under instruction variation) that will save other groups wasted effort.
- FDR-corrected sweep over the full SAE dictionary rather than cherry-picking, with honest reporting of how many features survived.
- Clear writing, and locally honest caveats (hybrid-architecture caveat, provisional kill, single-model limitation).

## Weaknesses

- The central causal result (<10⁻⁴ feature change under injection) is very likely true **by construction** — a cache modification cannot retroactively alter prefill activations — making the paper's "confirmation" of the temporal boundary vacuous.
- No surviving experiment establishes self/other **construct validity**; the three that tried were all killed, yet the title, abstract, and conclusion retain the self/other framing. The honest title is "an input-sentiment SAE feature and an output steering channel are distinct," which is expected.
- Finding 1 statistics: in-sample feature selection over ~410K tests with no held-out validation, effective n ≈ 6 valence levels, pseudoreplicated trial counts.
- The "depth not valence" interpretation is contradicted by the authors' own monotone-in-valence table and promoted to the abstract while admittedly untested.
- Draft-hygiene failures with scientific consequences: a section title asserting a retracted finding, a Limitations paragraph citing the retracted result as evidence, contradictory token counts, missing figures marked TODO.

## Questions for authors

1. **In the injection pipeline, is prefill re-run after the V-cache modification?** If injection is applied to the cached values post-prefill, explain what the 360-trial <10⁻⁴ result tests beyond an arithmetic identity.
2. If you feed the model's own generated responses back as *input*, does feature 58995 activate during prefill? (This distinguishes a phase boundary from a content difference.)
3. What is feature 58995's correlation with valence on a **held-out** scenario set not used for feature selection? And how does it compare to a simple linear valence probe at L47?
4. What is the null-null text divergence — baseline repeat vs. baseline repeat at temperature 0.3 — against which the 72–74% injection divergence should be read?
5. Was the Qwen-Scope SAE trained on this specific distilled checkpoint? What is its reconstruction error / feature-firing statistics on this model versus the model it was trained on?
6. Given all three self/other-specificity experiments were killed, what evidence remains that any measured representation is about the *other* (mental-state attribution) rather than about the *text*?

## Overall recommendation: **Weak Reject**

The methodological transparency is the best I have seen in a submission this year, and I want to be able to accept papers from labs that operate this way. But rigor of *process* cannot substitute for strength of *result*: the headline claim rests on a likely-tautological causal test, an in-sample-selected feature with an interpretation its own data contradicts, and a self/other framing whose every direct test was killed by the authors themselves. The correct conclusion from this body of work — and the authors nearly write it — is that they have not yet found a self/other representation. A rewrite as a confounds-and-methods paper centered on the kills, or resubmission after the held-out replication, the prefill-refeed control, and a genuine prefill-time intervention, could be a strong contribution.

## Confidence: 4

I am confident in the statistical and architectural critiques; slightly less so on the injection-pipeline tautology, which depends on an implementation detail the paper does not specify (hence Question 1 rather than an assertion).

---

Stepping out of role for one line: the tautology question (Q1) is the one I'd check first in `experiments/combination_presence.py` and the injection code before this goes anywhere — if prefill isn't re-run after injection, the abstract's central "confirming" sentence has to come out.
