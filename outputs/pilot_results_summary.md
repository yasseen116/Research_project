# Pilot Results Summary

| Metric | Clean | Noisy | Delta |
| --- | ---: | ---: | ---: |
| Frame Overall F1 | 1.0000 | 0.2399 | -0.7601 |
| Dialogue-Frame Consistency | 1.0000 | 1.0000 | 0.0000 |
| Slot Overall F1 | 1.0000 | 0.3013 | -0.6987 |
| Slot Auth Methods F1 | 1.0000 | 0.8222 | -0.1778 |
| Slot Functional Capabilities F1 | 1.0000 | 0.0952 | -0.9048 |
| Slot Security Constraints F1 | 1.0000 | 0.2667 | -0.7333 |
| Requirement Overall F1 | 1.0000 | 0.2015 | -0.7985 |
| Requirement Coverage | 1.0000 | 0.1322 | -0.8678 |
| Requirement Hallucination Rate | 0.0000 | 0.5000 | 0.5000 |
| Requirement Source Slot Coverage | 1.0000 | 0.2643 | -0.7357 |

## Interpretation

- The clean pilot is saturated by the current rule baseline because the dataset is tiny and the phrasing remains close to the schema.
- The noisy pilot exposes the real weakness of the rule baseline at both the frame and slot levels: capabilities, roles, and constraints break quickly under paraphrase.
- This makes the next step clear: compare a stronger LLM frame extractor against the same evaluation pipeline rather than changing the metrics.
