# Metacognitive Mode-Switching Reorganizes KV-Cache Geometry Across Transformer Architectures

**Status:** Revised — null swarm audit complete, 3 retractions applied, ready for human review
**Authors:** Lyra, Thomas Edrington, Dwayne Wilkes (Liberation Labs)
**Date:** Originally April 2026, revised June 2026
**Audit history:** Red team v1, red team v2, null swarm (June 2026)

## Paper Summary

Spectral entropy is the only KV-cache feature that tracks metacognitive processing across dense transformer architectures after FWL correction (d=-1.92 Qwen, -0.71 Llama). 960 trials, 4 models, 3 dedicated studies.

## What Was Retracted (June 2026 null swarm)

1. **"Bloom ordering confirmed"** — Body count #5 killed Bloom cognitive hierarchy (90-98% length confound). Reframed: text-level ordering replicates lexically but does not validate geometric claims.
2. **FWL→MP entailment** — Claim that FWL-survival implies MP-survival was logically invalid. Reframed: they correct different things, MP re-analysis needed.
3. **"5/6 raw effects"** — Was 5/6 feature-model comparisons on 3 of 6 features. Clarified denominator.

## What Survives

- Spectral entropy as cross-architecture metacognition marker (d=-1.92, -0.71 after FWL)
- Progressive spectral concentration (d=0.45→0.91 over 200 tokens)
- Late-layer peaks (L16-22)
- Encoding/generation sign reversal (2/4 models, architecture-specific)
- Qwen Meta vs Self retaining 5/8 features after FWL
- Llama losing all signal (honest null)

## Contents

```
mode-switching/
├── main.tex                          # Revised paper
├── data/
│   ├── RED_TEAM_REPORT_v1.md         # First adversarial review
│   ├── RED_TEAM_REPORT_v2.md         # Second adversarial review
│   ├── RED_TEAM_CONTENT_CONTROL.md   # Content control red team
│   └── CONTENT_CONTROL_RESULTS.md    # Raw content control data
└── README.md
```

## Review Notes

- Nell Watson removed from author list per her request
- 9 limitations trimmed to 6 per style guide (2 folded into body)
- New limitations added: instruction framing caveat, dense-transformer scope, MP outstanding
- The self-report validation experiment (spectral entropy without self-report step) is designed but not run — would definitively resolve whether the geometric signal requires the model to introspect
