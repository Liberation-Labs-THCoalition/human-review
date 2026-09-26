# Figure Specifications — Consequentiality Decomposition Paper

**Paper:** `/home/asdf/oracle-harness/paper/consequentiality_decomposition_draft.md`
**Responds to:** `CONSEQUENTIALITY_AUDIT.md` FIX-5.1 / FIX-7.2 (BLOCKING: zero figures)
**Companion script:** `/home/asdf/oracle-harness/paper/generate_figures.py`
**Style authority:** `/home/asdf/oracle-harness/visualization-briefs/02_SCIENTIFIC_paper_figures.md`
**Data verified:** 2026-08-29. Every field path below was checked against the live JSONs; all
headline numbers quoted here were recomputed from source and match the audit's independent
recomputation (including the FIX-1.1 corrected L23/L27 values — figures built from these
JSONs are automatically immune to the Table 1 transcription errors).

---

## 0. Global conventions (all figures)

### 0.1 Sizes and layout

Design target is NeurIPS/ICML text width (5.5 in). Nature-format resizing is a uniform
scale-down; do not design at Nature column width.

| Figure | Size (w × h, in) | Placement in paper |
|--------|------------------|--------------------|
| Fig 1  | 5.5 × 3.0 | Section 4.4 (after Stage 4 results; summarizes 4.2–4.4) |
| Fig 2  | 5.5 × 3.0 | Section 4.5, beside Table 1 / Finding 1 |
| Fig 3  | 5.5 × 3.2 | Section 4.5, beside Finding 2 (Table 2 after FIX-2.2) |
| Fig 4  | 5.5 × 2.7 | Section 4.6, beside Table 3 |

Margins: `constrained_layout=True` (or `tight_layout`), no suptitles — captions live in
the paper, not the image. Panel letters **A, B, C**: bold, 9 pt, top-left corner of each
panel, outside the axes frame (brief: "bold single-letter in top-left").

### 0.2 Typography

- Sans-serif: **Inter** if installed, fallback `DejaVu Sans` (matplotlib default).
  `rcParams["font.family"] = ["Inter", "DejaVu Sans", "sans-serif"]`
- Math (d, λ, ×): mathtext serif (`rcParams["mathtext.fontset"] = "cm"`).
- JSON field names / layer tokens in annotations: monospace (brief convention), e.g.
  `loo_d`, `L35`.
- Sizes: tick labels 7 pt; axis labels 8 pt; in-plot annotations 6.5–7 pt; direct line
  labels 7.5 pt; panel letters 9 pt bold. Never smaller than 6 pt after final scaling.

### 0.3 Palette

From the visualization brief, with role assignments fixed **across all four figures**
(brief: "same colors mean same things across all figures"; deceptive = red-violet,
honest = amber).

| Role | Hex | Source in brief |
|------|-----|-----------------|
| Threat deception / deceptive condition | `#b83280` (red-violet) | CONFABULATED/deceptive |
| Honest condition | `#f5a623` (amber) | HEDGED/honest |
| Consequentiality (stakes) | `#4a8fa6` (cool teal) | encoding/cool teal |
| Sycophancy | `#e89545` (warm amber) | generation/warm amber |
| Conformity | `#e85d45` (warm red-orange) | warm red-orange |
| Reward (null-signal mechanism) | `#8b909c` (slate gray) | extension of silver for "no signal" — darker than structural silver so the line stays legible |
| Total (composite) gap | `#2b2e38` (near-black ink) | extension — neutral composite that visually "contains" teal + red-violet components |
| Axes, zero lines, reference diagonals | `#c0c5ce` (silver) | structure/reference |
| Background | `#faf7f2` (paper cream) | background |

Notes:
- Sycophancy `#e89545` and honest `#f5a623` are near neighbors; they never appear in the
  same panel (Figs 1–3 have no "honest" element — d and gaps already encode the
  deceptive−honest contrast; Fig 4A has no mechanism lines).
- Band tints: substrate band = teal at alpha 0.08; amplifier band = red-violet at
  alpha 0.055. CI ribbons = line color at alpha 0.15, no edge.
- Background: cream per the brief. Provide a single `BG` constant; set to `#ffffff` for
  venues that mandate white (camera-ready check).

### 0.4 Axes style

Tufte-esque per the brief: no top/right spines; left/bottom spines silver `#c0c5ce`,
0.6 pt; ticks outward 2 pt, silver; grid off (the shaded bands carry the depth structure —
gridlines would fight them). Data lines 1.1 pt default, 1.6 pt for emphasized lines.
No legend boxes anywhere — direct labels at line ends (right margin), matching line color.

X-axis for all depth figures: actual layer index, linear scale, range [1, 49], ticks at
exactly the 12 capture layers `3 7 11 15 19 23 27 31 35 39 43 47` (Figs 1–2) or the
plotted subset (Figs 3–4C). Axis label: `Layer (residual stream)`.

### 0.5 Depth bands (Figs 1, 2; optional in 3)

Two full-height `axvspan` bands, drawn first (lowest zorder):
- **Substrate band:** L21–L33 (visual envelope of the L23–31 claim; spans halfway to
  neighboring capture layers so the named layers sit centered). Teal alpha 0.08.
  Label inside top of band, 6.5 pt, teal, small caps: `CONSEQUENTIALITY SUBSTRATE L23–31`.
- **Amplifier band:** L33–L49. Red-violet alpha 0.055. Label:
  `DECEPTION-AMPLIFIER BAND L35–47`.

Language contingency (RED-6.1): if the orthogonalized-direction transfer experiment is
NOT run before submission, the amplifier label and all captions must say
"threat-deception" rather than "deception" — the audit makes this blocking. The
companion script keeps this string in one constant (`AMPLIFIER_LABEL`).

### 0.6 Statistical conventions baked into the figures

These implement audit fixes; do not regress them:

- **p-values:** never `p=0.0000`. Use `p < 10⁻⁴ (0/10,000 permutations)` at first
  occurrence per figure, `p < 10⁻⁴` after (FIX-1.4).
- **Bootstrap CIs (Figs 1–3):** trial-level nonparametric bootstrap, B = 10,000,
  seed 20260828, percentile 95% intervals. Resample trials with replacement
  *independently within each scenario × condition cell* (15 trials/cell for Stages 2–4);
  recompute the full derived quantity (d, gap, residual, slope) per resample. The conseq
  gap is resampled in the same loop so residual CIs propagate both sources of error.
  This is FIX-3.1(a) — the figures are where the audit told these CIs to live.
- **Effect-size framing (FIX-4.2):** any caption quoting a d must anchor it against the
  design's own noise floor, not social-science convention. Standard sentence (reuse
  verbatim): "d values in this fixed-text design index separability along the direction,
  not behavioral effect magnitude; the LOO null floor is d = −0.04 (|99th| = 0.71)."
- **No intentionality language in captions (FIX-4.3):** "deceptive-pressure framing" /
  "pressure to misreport", never "planning to deceive".
- **Expected CI magnitudes** (analytic cross-check for the executor; bootstrap should
  land near these): gap-space 95% half-widths grow from ±0.06 (L27) to ±0.9 (L47) —
  small relative to the 12–15 unit threat residuals, so Fig 3's profiles will separate
  cleanly. d-space half-widths are large (±9 at d ≈ 34, n=15); Fig 1 therefore leans on
  ribbons + the cross-scenario band rather than point whiskers.

### 0.7 Output

Per figure: vector PDF (primary, embedded fonts, `fig1_depth_profile.pdf` etc.) plus
600 dpi PNG preview. Output dir: `/home/asdf/oracle-harness/paper/figures/`.

---

## Figure 1 — Depth profile: one direction, seven conditions

**Audit items addressed:** FIX-5.1 item 1 (depth profile with bands); visualizes the
Section 4.3 sycophancy sign inversion; caption implements FIX-1.4, FIX-2.5 (states n),
WARN-4.1 (scoped language).

**Claim supported:** Sections 4.2–4.4 — the fixed Stage 1 direction separates every
transfer condition, consequentiality-without-pressure included; the conditions differ
sharply in *where* in depth they separate.

### Layout

Single panel, 5.5 × 3.0 in. Right margin reserved (~0.9 in) for direct labels.

### Data

All series are Cohen's d of projections onto the fixed LAT v2 direction (external to all
plotted data — no circularity), at the 12 capture layers.

| Series | Source | Field path |
|--------|--------|-----------|
| Threat mean + min–max band (3 scenarios) | `experiments/results/lat_transfer_results.json` | `test_a.{datacorp,edutech,secureai}.layers.{L}.d` |
| Sycophancy | `experiments/results/nonthreat_transfer_results.json` | `extraction.sycophancy.layers.{L}.d` |
| Reward | same | `extraction.reward.layers.{L}.d` |
| Conformity | same | `extraction.conformity.layers.{L}.d` |
| Consequentiality | `experiments/results/consequentiality_control_results.json` | `layer_results.{L}.d` |
| Bootstrap CI ribbons | trial-level projections | `…trials[*].condition`, `…trials[*].projections.{L}` (conseq file: `trials[*]`, conditions `high_stakes`/`low_stakes`) |

Key values (verified): threat mean peaks 39.9 at L35 (per-scenario max 43.1);
consequentiality peaks 19.8 at L31 then collapses to 1.4 at L47; reward peaks 17.2 at
L31 then collapses to 0.25 at L47 (visually parallel to conseq — this is the point);
sycophancy dips to −6.1 at L19 and crosses zero between L23 and L27.

### Axes

- X: layer, [1, 49], 12 ticks (§0.4).
- Y: `Cohen's d (projection onto LAT v2 direction)`, range **[−9, 48]**, ticks at
  −5, 0, 10, 20, 30, 40. Zero line: silver, 0.6 pt, solid (it is semantically load-bearing
  — the sycophancy inversion crosses it).

### Marks

- Threat: mean line red-violet 1.6 pt; band = per-layer min–max across the 3 scenarios,
  red-violet alpha 0.12 (shows cross-scenario spread without 3 extra lines).
- Sycophancy `#e89545`, reward `#8b909c`, conformity `#e85d45`, consequentiality teal
  1.4 pt (headline concept, slightly heavier); others 1.1 pt.
- Bootstrap 95% ribbons on the four single lines, own color alpha 0.15. (Threat mean
  ribbon optional — the min–max band already dominates it; if drawn, alpha 0.10.)
- Round markers (2.2 pt) at the 12 capture layers on every line — the x-axis is a sparse
  sample of depth and the markers say so honestly.
- Depth bands per §0.5.

### Annotations

1. Sycophancy inversion: 6.5 pt annotation at (L19, −6.1), short leader line:
   `sycophancy projects opposite until ~L27`.
2. Late collapse: annotation near (L45, ~3) pointing at the converging teal + gray
   tails: `consequentiality and reward collapse late`.
3. Direct labels, right edge, in line color: `threat (mean of 3)`, `conformity`,
   `sycophancy`, `reward`, `consequentiality` — vertically nudged to avoid collisions
   (at L47 the values are 16.8 / 11.7 / 10.2 / 0.25 / 1.4; reward and consequentiality
   labels will need stacking with leader lines).

### Rejected alternatives

- Seven individual lines: unreadable; the min–max band encodes threat spread better.
- Including Stage 1's extraction curve: different estimator (LOO d vs fixed-direction
  transfer d); mixing estimators in one panel invites the exact confusion FIX-4.2 exists
  to prevent. If desired, add as a separate 1.8 × 1.2 in inset (top-left, `loo_d` with
  `ci_low`/`ci_high` band from `lat_deception_v2.json` top-level `{L}.loo_d` etc.),
  clearly titled `Stage 1 extraction (LOO)`. Optional.

### Caption (proposed verbatim)

> **Figure 1. One direction, seven conditions: depth profiles of separability along the
> fixed Stage 1 direction.** Cohen's d for deceptive vs honest conditions (three threat
> scenarios, mean with min–max band; sycophancy; reward; conformity) and for high- vs
> low-stakes with no pressure to misreport (consequentiality), all projected onto the
> same externally fixed LAT v2 direction (n = 15 pairs per scenario; ribbons are
> trial-level bootstrap 95% CIs, B = 10,000). All conditions separate significantly at
> L31 (all p < 10⁻⁴, 0/10,000 permutations, Bonferroni-corrected), but with distinct
> depth structure: consequentiality and reward peak in the substrate band (L23–31) and
> collapse in late layers, threat separation persists through L47, sycophancy inverts
> sign before L27. In this fixed-text design d indexes separability along the direction,
> not behavioral effect magnitude (see Section 3.3).

---

## Figure 2 — Decomposition: total gap = consequentiality substrate + residual

**Audit items addressed:** FIX-5.1 item 2; FIX-1.1 (figure computed from canonical JSONs
reproduces the *corrected* L23 = 2.48/0.62 and L27 = 3.91/1.83 values); FIX-1.2 (single
explicit metric — raw projection gaps, stated on the axis; no percentage column);
FIX-1.3 (correct 8–21× annotation replaces "10–12×"); FIX-3.1(a) (bootstrap CIs).

**Claim supported:** Section 4.5 Table 1 + Finding 1 — the composite signal decomposes
into a mid-depth consequentiality substrate and a late deception-specific residual.

### Layout

Single panel, 5.5 × 3.0 in, right margin for direct labels.

### Data

All series in **gap space**: mean projection difference (activation units) onto the
fixed LAT v2 direction. Recompute from means, never from the paper's Table 1
(FIX-1.1 provenance):

| Series | Definition | Field paths |
|--------|-----------|------------|
| Total threat gap | mean over 3 scenarios of `dec_mean − hon_mean` | `lat_transfer_results.json: test_a.{sc}.layers.{L}.dec_mean/hon_mean` |
| Consequentiality gap | `hs_mean − ls_mean` | `consequentiality_control_results.json: layer_results.{L}.hs_mean/ls_mean` |
| Deception-specific residual | total − consequentiality (the paper's §3.8 subtraction) | derived |
| CI ribbons | trial-level bootstrap per §0.6 | `…trials[*].projections.{L}` |

Verified anchor values: total 7.74 (L31) → 15.54 (L35 peak); conseq 2.98 (L31 peak) →
0.68 (L39); residual 4.76 (L31) → 13.78–14.19 (L35–39). Residual/conseq ratio across
L35–47: 7.8× / 20.9× / 12.1× / 11.3× — annotate as "8–21×", not "10–12×" (FIX-1.3).

### Axes

- X: layer, [1, 49], 12 ticks. Full depth range — the early-layer near-zero region is
  honest information (the direction does nothing until ~L15).
- Y: `Projection gap along LAT v2 direction (activation units)`, range **[−1.5, 16.5]**,
  ticks 0, 4, 8, 12, 16. Zero line silver.

### Marks

- Total: ink `#2b2e38`, 1.6 pt. Consequentiality: teal, 1.4 pt. Residual: red-violet,
  1.4 pt. Markers at capture layers (2.2 pt).
- Bootstrap 95% ribbons on all three (alpha 0.15). Expected half-widths ±0.06–0.9
  (§0.6) — visible but tight; that is the finding.
- Depth bands per §0.5.

### Annotations

1. Decomposition bracket at **L31** (vertical dotted silver guide): brace or paired
   arrows showing `7.74 = 2.98 + 4.76`, 6.5 pt, labeled `total = substrate + residual`.
2. At **L39**: thin vertical connector between teal (0.68) and red-violet (14.19)
   points, labeled `residual ≥ 8–21× substrate across L35–47`.
3. Direct labels right edge: `total (threat mean)` ink, `deception-specific residual`
   red-violet, `consequentiality` teal. (Apply RED-6.1 contingency: "threat-deception-
   specific residual" if the transfer experiment is not run.)

### Rejected alternatives

- Stacked area (teal below, red-violet above, envelope = total): visually seductive and
  arithmetically true, but it *asserts* additivity, which is an assumption the paper
  itself flags (Limitation 5) and the audit stresses (RED-6.4: the subtracted baseline
  may be underestimated). Independent lines with independent CIs represent the epistemic
  state correctly.
- Plotting "% consequentiality": this is the metric the audit burned (FIX-1.2 — the
  d-ratio/gap-ratio collision). The figure shows magnitudes; percentages, if kept at
  all, live in the corrected Table 1 with an explicit metric label.

### Caption (proposed verbatim)

> **Figure 2. Decomposing the composite signal.** Mean projection gap along the fixed
> LAT v2 direction for threat deception (total; mean of 3 scenarios, n = 15 pairs each),
> for high- vs low-stakes with symmetric incentives and no pressure to misreport
> (consequentiality; n = 15 pairs), and their difference (deception-specific residual,
> Section 3.8). Ribbons: trial-level bootstrap 95% CIs (B = 10,000), propagating both
> terms of the subtraction. The consequentiality gap peaks inside the substrate band
> (L23–31) and decays by L39; the residual dominates the amplifier band, exceeding the
> consequentiality gap by 8–21× across L35–47. The subtraction assumes additivity
> (Limitation 5); see Section 4.6 for the orthogonalization that removes this
> assumption.

---

## Figure 3 — Three late-layer residual signatures

**Audit items addressed:** FIX-5.1 item 3; FIX-3.1 (the blocking one — CIs on every
point plus the L35–47 slope test rendered directly in the figure); RED-6.2 caveat
carried in the caption; FIX-2.2 (figure is the graphical form of the newly numbered
Table 2).

**Claim supported:** Section 4.5 Finding 2 / Section 5.2 — threat plateau vs social
rising gradient vs reward flat-zero. This claim is in the abstract twice and currently
"rests on eyeballing eight numbers" (audit). This figure is where it earns its keep, or
gets demoted.

### Layout

Single panel 5.5 × 3.2 in, right margin ~1.1 in for direct labels + slope readouts.

### Data

Residual per mechanism = scenario gap − consequentiality gap, at **L27–L47** (5 layers:
27, 31, 35, 39, 43, 47 — six points). Extending below the Finding 2 table's L35 start is
deliberate: it shows threat engaging at L31 (+4.8) while social mechanisms sit at ≈ 0
(−1.2 to −0.7) — the "threat engages early" half of the claim.

| Series | Field paths |
|--------|------------|
| Threat (mean) + 3 thin per-scenario traces | `lat_transfer_results.json: test_a.{sc}.layers.{L}` |
| Sycophancy, conformity, reward | `nonthreat_transfer_results.json: extraction.{sc}.layers.{L}` |
| Consequentiality gap (subtracted term) | `consequentiality_control_results.json: layer_results.{L}` |
| CIs + slopes | trial-level bootstrap per §0.6 from `…trials[*].projections.{L}` |

Verified values (residuals): threat 2.08, 4.76, 13.78, 14.19, 13.35, 12.74;
sycophancy −1.22, −1.05, 1.65, 3.68, 5.77, 7.18; conformity −1.06, −0.76, 0.54, 2.12,
4.25, 5.97; reward −0.68, −0.37, 0.25, 0.67, −0.26, −0.88. Per-scenario threat traces
at L35–47 stay within 11.1–15.2 (plateau is not an averaging artifact).

**Slope statistic (FIX-3.1(b)):** per mechanism, OLS slope of residual on layer over
L35–47 (4 points), recomputed inside the same bootstrap loop → slope with percentile
95% CI. Point estimates (OLS, verified by `--check-data`): threat −0.099/layer,
sycophancy +0.467/layer, conformity +0.461/layer, reward −0.108/layer — social slopes
are positive and ~4.5× the magnitude of threat's. The figure displays these; the paper's text should
additionally report the permutation test of slope *differences* (threat vs social,
social vs reward) that the audit requires — same bootstrap machinery, text-side.

Preview (B = 200 smoke test; final run uses B = 10,000): slope 95% CIs — threat
[−0.15, −0.05], sycophancy [+0.42, +0.52], conformity [+0.41, +0.52], reward
[−0.18, −0.04]. The social CIs exclude both threat's and reward's entirely, so the
three-signature claim survives FIX-3.1 with room to spare. Caution for the caption:
reward's slope CI narrowly excludes zero (slightly negative) — its "flat null" label
rests on its *level* (≈ 0 across all layers, CIs spanning zero at most points), not on
a literally zero slope. Phrase as "remains at zero" (level claim), never "zero slope".

### Axes

- X: layer, [25, 49], ticks at 27, 31, 35, 39, 43, 47.
- Y: `Deception-specific residual (activation units)`, range **[−3, 16]**, ticks 0, 4,
  8, 12, 16. Zero line silver 0.8 pt — the reward signature *is* this line; make it
  slightly heavier than other reference lines.

### Marks

- Threat mean red-violet 1.6 pt + markers; per-scenario traces red-violet alpha 0.30,
  0.7 pt, no markers (texture, not data points to read).
- Sycophancy `#e89545`, conformity `#e85d45`, reward `#8b909c`; 1.2 pt + markers.
- Point-wise bootstrap 95% CI: vertical cap-less error bars at each marker (these
  points are few enough that bars read better than ribbons here; expected half-widths
  ±0.08–0.9).
- Optional: amplifier band tint (L33–49) only; substrate band omitted (x starts at 25 —
  a partial band would mislead).

### Annotations (right margin block, aligned to line ends)

Three signature groups, 7.5 pt labels with 6.5 pt slope readouts beneath (slope values
from the companion analysis; the script templates them):

```
threat — plateau            slope −0.10 [CI] /layer
sycophancy | conformity —
  rising gradient           slopes +0.47, +0.46 [CI] /layer
reward — flat null          slope −0.11 [CI] /layer
```

Plus one in-panel annotation at (L31, 4.8): `threat engages by L31; social mechanisms
at zero until L35`.

### Rejected alternatives

- 1×3 small multiples (one per signature class): wastes the direct visual comparison —
  the claim is *about the contrast between profiles*, so they must share axes.
- Starting at L35 (matching the Finding 2 table): hides the L31 divergence that
  motivates "threat engages early"; six points cost nothing.

### Caption (proposed verbatim)

> **Figure 3. Three late-layer residual signatures.** Deception-specific residual
> (scenario gap minus consequentiality gap, both onto the fixed LAT v2 direction) across
> L27–L47. Threat deception (mean of 3 scenarios; thin traces show each scenario)
> engages by L31 and sustains a plateau (L35–47 slope −0.10/layer); sycophancy and
> conformity show no signal at L31 and rise monotonically (+0.47 and +0.46/layer);
> reward framing stays at zero throughout. Error bars: trial-level bootstrap 95% CIs
> (B = 10,000; n = 15 pairs per scenario), propagating uncertainty in the subtracted
> consequentiality gap. All profiles are projections onto a threat-derived direction;
> mechanism-specific axes (Section 4.7, de novo cosines 0.14–0.44) may accumulate
> alignment differently with depth, so the shapes characterize alignment with this
> direction rather than each mechanism's full computation.

(The final caption sentence is the RED-6.2 hedge; keep it unless the de-novo-direction
control is run.)

---

## Figure 4 — Stage 5: the orthogonalized direction separates deception, not stakes

**Audit items addressed:** FIX-5.1 item 4; FIX-4.2 (noise floor rendered, giving the
mandated d-scale framing a visual anchor); PASS-3.4 recommendation (circular noise floor
d ≈ 14.6 made visible); FIX-3.3 hook (raw-d overlay in Panel C); FIX-3.2 caveat carried
in caption (conseq mean removed in-sample by construction; split-half variant noted).
Caption implements RED-6.1 scoping ("threat-deception-specific").

**Claim supported:** Section 4.6 Table 3 — after Gram-Schmidt removal of the
consequentiality component, a deception-linked component survives LOO cross-validation
(d = 24–37) while stakes separability on the same direction sits at chance (AUC
0.49–0.51).

### Layout

Three panels in a row, 5.5 × 2.7 in total; width ratios ≈ 1.15 : 1 : 1.15
(A slightly wider for the two distribution columns, C for the layer axis).

### Panel A — held-out projections at L35

The paper's strongest single number (LOO d = 36.9), shown as raw data.

**Data:** `subspace_reanalysis.json: loo_projections.35.dec` (50 floats) and
`…35.hon` (50 floats). These are *held-out* projections: per LOO fold, direction
re-extracted from n−1 pairs, re-orthogonalized against the full-data consequentiality
vector, applied to the held-out pair (`subspace_reanalysis.py:39-77`).
Verified stats: dec 8.71 ± 0.56, range [7.10, 9.63]; hon −7.78 ± 0.29,
range [−8.52, −7.09]. Zero overlap; 16.5-unit gulf.

**Marks:** two categories on X (`honest`, `deceptive`), jittered strip plots (dot size
2.5 pt, jitter width 0.16, alpha 0.55; hon amber, dec red-violet) with half-violin
(KDE) outward of each strip, same color alpha 0.25; horizontal mean tick (1.2 pt, solid
color, width 0.3 category units) per group.

**Axes:** Y: `Held-out projection, orthogonalized direction (activation units)`,
range **[−10.5, 11]**. X: the two category labels, no axis line needed beyond baseline.

**Annotations:**
- Between the groups, at mid-height: `LOO d = 36.9` (7.5 pt) with `p < 10⁻⁴
  (0/10,000)` beneath (6.5 pt).
- At y = 0: silver zero line; small text `LOO null floor: d = −0.04, |99th| = 0.71`
  anchored bottom-left (6.5 pt) — at this axis scale the null band is invisibly thin,
  which is precisely the point; text carries it.
- Panel title (7.5 pt, above axes): `L35, n = 50 pairs`.

### Panel B — ROC: same direction, two questions

The panel that states the paper's thesis in one image: one direction, perfect for
deception, chance for stakes.

**Data:**
- Consequentiality ROCs (5 layers): **recomputed** from
  `experiments/results/subspace_raw_activations.pt` (dict: `raw[condition][layer_int]` →
  float32 array (50, 5120); conditions `threat_dec`, `threat_hon`, `conseq_high`,
  `conseq_low`; layer keys are ints 31/35/39/43/47). Per layer: conseq direction =
  normalized mean difference `conseq_high − conseq_low`; threat direction = mean
  difference `threat_dec − threat_hon`, Gram-Schmidt orthogonalized against the conseq
  direction, normalized (mirror `subspace_reanalysis.py:214-223` exactly); project
  `conseq_high`/`conseq_low`, `sklearn.metrics.roc_curve`. Verified: this reproduces the
  stored `results.{L}.conseq_auc` exactly (L35: 0.488).
- Deception ROC (reference): from the stored **held-out** LOO projections
  (`loo_projections.35.dec/hon`) — AUC = 1.000 at L35 (distributions disjoint).

**Marks:** five conseq ROC curves in teal, 1.0 pt, alpha graded 0.35→0.9 by layer
(L31 lightest → L47 darkest); chance diagonal silver dashed 0.8 pt; deception ROC
red-violet 1.6 pt, `clip_on=False` (it runs along the axes frame).

**Axes:** X `False positive rate`, Y `True positive rate`, both [0, 1], ticks 0/0.5/1,
aspect equal.

**Annotations:** top-left, 6.5 pt, two-line block:
`deception (held-out): AUC = 1.00` (red-violet) /
`stakes, L31–47: AUC 0.49–0.51` (teal). No per-curve labels — the five teal curves are
deliberately an indistinguishable braid around the diagonal.

### Panel C — Table 3 as a picture (recommended; drop if space demands A+B only)

**Data:** `subspace_reanalysis.json: results.{31,35,39,43,47}.loo_d` (24.1–36.9);
`metadata.noise_floor_loo_mean` (−0.044), `metadata.noise_floor_loo_99th` (0.706),
`metadata.noise_floor_circular_mean` (14.63). Bootstrap CI per layer from the stored
per-trial `loo_projections` (resample 50 held-out pairs). Optional FIX-3.3 overlay: raw
(non-orthogonalized) LOO d recomputed from the `.pt` with the identical LOO fold
structure minus the Gram-Schmidt step — the companion script stubs
`compute_raw_loo_d()` for this; plot as open circles beside the filled orthogonalized
points so "the cost of orthogonalization" is a within-dataset visual.

**Marks:** X: the 5 late layers; Y: `LOO Cohen's d`, range [0, 42]. Filled red-violet
points (4 pt) + bootstrap CI whiskers, thin red-violet connector 0.8 pt alpha 0.5.
Horizontal reference lines: LOO null band ±0.71 around 0 (silver fill alpha 0.5 — a
sliver at this scale, labeled `LOO noise floor`); circular-extraction floor at 14.63,
silver dashed 0.8 pt, labeled `circular (non-CV) floor on pure noise ≈ 14.6` (6.5 pt).

The circular-floor line is the audit's PASS-3.4 recommendation made graphic: naive
fixed-direction reprojection at n = 50, dim = 5120 produces d ≈ 14.6 on *noise*; the
LOO estimates clear it by 10–22 units and the LOO null sits at zero.

### Caption (proposed verbatim)

> **Figure 4. The orthogonalized threat-deception direction separates deceptive-pressure
> framing, not stakes.** (A) Held-out projections at L35: per leave-one-out fold the
> threat direction is re-extracted from n−1 pairs and re-orthogonalized against the
> consequentiality mean-difference vector before projecting the held-out pair (n = 50
> pairs). Deceptive and honest conditions are disjoint (LOO d = 36.9, p < 10⁻⁴,
> 0/10,000 permutations). (B) ROC curves on the same orthogonalized direction:
> deceptive vs honest (held-out, AUC = 1.00) against high- vs low-stakes (AUC
> 0.49–0.51 across L31–47) — the direction retains full deception separability while
> stakes separability is at chance. The first moment of the stakes contrast is removed
> in-sample by construction; the chance-level AUC additionally rules out
> higher-moment leakage (split-half validation in supplement). (C) LOO d across late
> layers, calibrated against the design's own noise floors: the LOO null (d = −0.04,
> |99th| = 0.71, 200 simulations) and the d ≈ 14.6 floor that *circular*
> (non-cross-validated) extraction produces on pure noise at n = 50, dim = 5120 —
> the reason LOO estimation is load-bearing. d here indexes separability of fixed-text
> conditions along the direction, not behavioral effect magnitude.

(Panel B caption sentence implements the FIX-3.2 honesty requirement; if the
split-half is not run, replace the parenthetical with "the AUC check rules out
higher-moment leakage; the first moment is removed by construction".)

---

## Data field reference (verified 2026-08-29)

```
experiments/results/lat_deception_v2.json          # Stage 1
  {L}.loo_d, .ci_low, .ci_high, .perm_p, .full_norm, .n_pairs, .direction[5120]
  L ∈ {"3","7","11","15","19","23","27","31","35","39","43","47"}

experiments/results/lat_transfer_results.json      # Stage 2 (+ behavioral Test B)
  metadata.n_pairs_per_scenario = 15, .n_perms = 10000
  test_a.{datacorp|edutech|secureai}.layers.{L}.{d,p,n,dec_mean,hon_mean,dec_std,hon_std}
  test_a.{sc}.trials[30]: {trial, condition∈{deceptive,honest}, prompt_len, projections.{L}}
  test_b[30]: {trial, prompt_len, text, score, inflated, has_think, projections}  # 0/30 inflated

experiments/results/nonthreat_transfer_results.json  # Stage 3
  metadata.n_pairs = 15
  extraction.{sycophancy|reward|conformity}.layers.{L}.{d,p,n,dec_mean,hon_mean,dec_std,hon_std}
  extraction.{sc}.trials[30]  (same trial schema, condition∈{deceptive,honest})
  extraction.{sc}.denovo_cosines.{3|11|19|31|47}.cosine_with_lat_v2
  shakedown.{sc}.{inflated,total,rate}

experiments/results/consequentiality_control_results.json  # Stage 4
  metadata.n_pairs = 15; design_audit.char_diff = 0
  layer_results.{L}.{d,p,n,hs_mean,ls_mean,hs_std,ls_std}
  trials[30]: {trial, condition∈{high_stakes,low_stakes}, prompt_len, projections.{L}}

experiments/results/subspace_reanalysis.json       # Stage 5
  metadata.{n_perms=10000, bonferroni_alpha=0.01,
            noise_floor_loo_mean=-0.0445, noise_floor_loo_99th=0.7062,
            noise_floor_circular_mean=14.6285}
  results.{31|35|39|43|47}.{loo_d, p_perm, conseq_auc, cosine_lat_v2,
            raw_cosine_threat_conseq, signal_above_noise, n=50}
  loo_projections.{L}.{dec[50], hon[50]}          # held-out per-trial projections

experiments/results/subspace_raw_activations.pt    # Stage 5 raw (25 MB, torch.load)
  raw[{threat_dec|threat_hon|conseq_high|conseq_low}][{31|35|39|43|47:int}]
    → np.float32 array (50, 5120)
```

## Execution notes

- `matplotlib` is **not installed** on this box (numpy 2.4.4, torch 2.12, sklearn 1.8,
  scipy 1.17 are). Run the script wherever matplotlib lives (Starship:
  `/Users/margaret/miniforge/bin/python3`), or `pip install matplotlib` locally.
- `generate_figures.py --check-data` runs *without* matplotlib and verifies every field
  path + prints the anchor numbers above; run it first on any machine.
- The `.pt` load and the 5-layer ROC recomputation take seconds; the only nontrivial
  compute is the B = 10,000 bootstrap (~1–2 min, vectorizable).
- Do not hand-transcribe any number into plotting code — every value must flow from the
  JSONs at render time (this is what neutralizes FIX-1.1 permanently).
