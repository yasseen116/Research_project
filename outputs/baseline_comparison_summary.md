# Baseline Comparison Summary

| Baseline | Condition | Frame F1 | Frame Consistency | Slot F1 | Capability F1 | Security F1 | Requirement F1 | Coverage | Hallucination |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | clean | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| B1 | noisy | 0.2399 | 1.0000 | 0.3013 | 0.0952 | 0.2667 | 0.2015 | 0.1322 | 0.5000 |
| B2 | clean | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| B2 | noisy | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

## Read This First

- `B1` is the brittle lexical baseline.
- `B2` adds normalization and paraphrase-aware keyword mapping for the fixed six-question dialogue flow.
- `G1` is the native Gemini frame-first pipeline when a Gemini run has been executed.
- Frame metrics isolate dialogue understanding quality before slot projection and requirement generation.
