# Pilot Flow Report

## Read This First

This is the clearest current path through the project:
- Use the public source corpora in `raw_sources/public/` as the trusted origin.
- Use the manual gold samples in `raw_sources/manual_gold/` and the noisy variants in `synthetic/pilot_noisy/` as the current pilot benchmark.
- Run the full benchmark with `python3 scripts/run_pilot_pipeline.py`.
- Read the current best summary in `outputs/baseline_comparison_summary.md`.

## Current Best Result

- Best pilot baseline: `B2` on the noisy condition.
- Slot F1: `1.0000`
- Requirement F1: `1.0000`
- Coverage: `1.0000`
- Hallucination rate: `0.0000`

## Full Flow

1. Trusted public requirements documents are downloaded into `raw_sources/public/`.
2. Selected documents are converted manually into source-grounded gold samples in `raw_sources/manual_gold/`.
3. The same gold samples are paraphrased into noisy dialogue variants in `synthetic/pilot_noisy/`.
4. A dialogue-to-slots baseline predicts the six slot groups.
5. A deterministic slot-to-requirements stage generates FRs and NFRs.
6. Slot and requirement outputs are scored with the evaluation scripts in `scripts/`.

## Baseline Results

| Baseline | Condition | Slot F1 | Capability F1 | Security F1 | Requirement F1 | Coverage | Hallucination |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | clean | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| B1 | noisy | 0.3013 | 0.0952 | 0.2667 | 0.2015 | 0.1322 | 0.5000 |
| B2 | clean | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| B2 | noisy | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

## Why B1 Fails and B2 Works On The Pilot

- B1 mostly copies literal phrases from the dialogue. When the user paraphrases the same intent, it misses roles, capabilities, and constraints.
- B2 adds normalized phrase mapping for the fixed six-question chatbot flow. That makes it robust to the current noisy paraphrases.
- This is a good pilot result, but it is still a controlled benchmark. The next validation step is scaling the gold set, not changing the metrics.

## Walkthrough Sample: `manual_001_amazing_lunch_indicator_noisy`

Source anchor: `software_requirements_dataset` document `c01_amazing_lunch_indicator` with source sentence ids FR3, FR4, FR6, FR7, FR8, FR9, FR11, QR6, QR8, QR12, QR15

### Dialogue

- `1` `bot`: What kind of system do you want?
- `2` `user`: Basically a phone app for finding food spots near me and checking what each place offers.
- `3` `bot`: Who will use it?
- `4` `user`: Regular app users, restaurant people using the portal, and whoever manages the whole thing.
- `5` `bot`: What should users be able to do?
- `6` `user`: People should be able to look up places to eat, bounce between map and list results, open the full place details, and get directions. The restaurant side should update venue info, and management should approve those restaurant accounts.
- `7` `bot`: Do users need login or authentication?
- `8` `user`: Yeah, the mobile side needs sign-in, and the portal side needs accounts too for the restaurant side and the people running it.
- `9` `bot`: Are there performance requirements?
- `10` `user`: Searches need to feel quick, like two seconds tops, and if GPS or the internet dies the app should say so instead of just hanging.
- `11` `bot`: Are there security requirements?
- `12` `user`: Login traffic needs protecting, and after three bad tries the portal account should cool off for about thirty minutes.

### Gold Slots

- System type: `restaurant discovery mobile application`
- User roles: users, restaurant owners, administrators
- Authentication required: `true`
- Authentication methods: mobile app username/password login, web portal username/password login
- Functional capabilities (6):
- users -> search for restaurants using multiple search options
- users -> view restaurant results in map and list views
- users -> open detailed restaurant information pages
- users -> navigate to a selected restaurant using GPS
- restaurant owners -> manage restaurant information through the web portal
- administrators -> verify restaurant owners
- Performance constraints (2): return search results within 2 seconds; inform the user if internet or GPS connectivity is lost
- Security constraints (2): encrypt log-in communication messages; disable restaurant owner and administrator log-in for 30 minutes after three failed attempts

### B1 Output On This Same Noisy Dialogue

- Slot F1: `0.2500`
- Requirement F1: `0.1538`
- Coverage: `0.0909`
- Hallucination rate: `0.5000`

Predicted slots:
- System type: `basically a phone app for finding food spots near me and checking what each place offers.`
- User roles: regular app users, restaurant people using the portal, whoever manages the whole thing
- Authentication required: `true`
- Authentication methods: web portal username/password login
- Functional capabilities (1):
- users -> view restaurant results in map and list views
- Performance constraints (0): none
- Security constraints (0): none

Generated requirements:
- Functional requirements (2):
- The system shall support authentication using web portal username/password login.
- The system shall allow users to view restaurant results in map and list views.
- Non-functional requirements (0):
- none

### B2 Output On This Same Noisy Dialogue

- Slot F1: `1.0000`
- Requirement F1: `1.0000`
- Coverage: `1.0000`
- Hallucination rate: `0.0000`

Predicted slots:
- System type: `restaurant discovery mobile application`
- User roles: users, restaurant owners, administrators
- Authentication required: `true`
- Authentication methods: mobile app username/password login, web portal username/password login
- Functional capabilities (6):
- users -> search for restaurants using multiple search options
- users -> view restaurant results in map and list views
- users -> open detailed restaurant information pages
- users -> navigate to a selected restaurant using GPS
- restaurant owners -> manage restaurant information through the web portal
- administrators -> verify restaurant owners
- Performance constraints (2): return search results within 2 seconds; inform the user if internet or GPS connectivity is lost
- Security constraints (2): encrypt log-in communication messages; disable restaurant owner and administrator log-in for 30 minutes after three failed attempts

Generated requirements:
- Functional requirements (7):
- The system shall support authentication using mobile app username/password login and web portal username/password login.
- The system shall allow users to search for restaurants using multiple search options.
- The system shall allow users to view restaurant results in map and list views.
- The system shall allow users to open detailed restaurant information pages.
- The system shall allow users to navigate to a selected restaurant using GPS.
- The system shall allow restaurant owners to manage restaurant information through the web portal.
- The system shall allow administrators to verify restaurant owners.
- Non-functional requirements (4):
- performance: The system shall return search results within 2 seconds.
- performance: The system shall inform the user if internet or GPS connectivity is lost.
- security: The system shall encrypt log-in communication messages.
- security: The system shall disable restaurant owner and administrator log-in for 30 minutes after three failed attempts.

## What To Use Now

- Use `B2` as the current best pilot baseline.
- Use `B1` as the weak comparison baseline in the paper.
- Use the existing evaluation scripts unchanged when you scale from 3 pilot samples to a larger gold set.

## Important Limits

- B2 is the current best pilot system, but it is still a hand-built normalized rule baseline.
- The pilot set is only 3 source-grounded samples, so these scores are useful for proving the pipeline works, not for claiming broad generalization.
- The next stronger result is to scale the manual gold set and then keep the same evaluation scripts unchanged.
