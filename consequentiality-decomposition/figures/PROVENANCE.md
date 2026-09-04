# Figure provenance

The build gate flags these PDFs as UNVERIFIABLE because there is no `.tex`
beside them. They are matplotlib output, not LaTeX, so that check does not
apply — but the thing the gate is protecting does, and it caught a real defect.

## What was wrong

`supplementary/code/generate_figures.py` hard-coded `REPO =
Path("/home/asdf/oracle-harness")`. A reviewer who checked out this repository
could not rebuild a single figure: the script looked for data on the author's
machine. Shipping a generator that only runs where it was written is not
shipping reproducibility, and "the generator ships" was not an adequate answer.

Fixed: the script now resolves data from `supplementary/data/` relative to its
own location, falling back to the author path only if that directory is absent.

## What can be rebuilt, and what cannot

    python3 supplementary/code/generate_figures.py

| Figure | Rebuildable from shipped data | Source |
|---|---|---|
| fig1_depth_profile | yes | `lat_deception_v2.json`, `lat_transfer_results.json` |
| fig2_decomposition | yes | `consequentiality_control_results.json` |
| fig3_signatures | yes | `nonthreat_transfer_results.json`, `signature_cis.json` |
| fig4_stage5_orthogonalization panel A | yes | `subspace_reanalysis.json` |
| fig4 panels B and C | **NO** | needs `subspace_raw_activations.pt` (25 MB) |

**Panels 4B and 4C cannot be rebuilt from this repository.** They are projection
scatter plots drawn from raw per-token activations, a 25 MB tensor too large to
commit here. It is available on request and lives at
`experiments/results/subspace_raw_activations.pt` in the Oracle harness. Every
*number* those panels illustrate is in `subspace_reanalysis.json`, which does
ship — the omission costs the visual, not the claim.

## What I did NOT verify

I did not regenerate these figures and diff them against the committed PDFs.
matplotlib is not installed in the environment where this pass was made, so the
path fix above is reasoned, not executed. **A reviewer should treat these PDFs
as unconfirmed against current source until someone runs the generator and
compares.** That is a smaller claim than "verified", and it is the true one.

The figure-to-data mapping in `supplementary/figure_specifications.md` was
checked field-by-field against the live JSONs on 2026-08-29, including the
FIX-1.1 corrected L23/L27 values, so figures built from these files are immune
to the Table 1 transcription errors the audit found.
