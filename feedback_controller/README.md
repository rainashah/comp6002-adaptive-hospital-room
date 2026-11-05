# Deterministic AHR Feedback Controller

This folder contains the post-recommendation feedback-controller implementation and its structured test evidence.

## Purpose

The controller sits **after** the LLM recommendation and deterministic validation layers. It does not call the LLM again. Its purpose is to preserve staff authority and provide predictable state transitions after a validated recommendation.

## Files

### Executable artefacts
- `AHR_Feedback_Controller.ipynb` — deterministic controller implementation plus 12 unit/transition tests.
- `AHR_Experiment2_Feedback_Controller_Integration.ipynb` — loads representative final-valid outputs from all 12 frozen Experiment 2 cases and exercises six pathways per case.
- `controller.py` — deterministic controller state machine.
- `unit_tests.py` — executable 12-test suite.
- `integration_replay.py` — public 72-scenario replay.

### Structured outputs
Generated controller evidence is grouped under `results/`:
- `results/feedback_controller_test_results.csv` — unit-test results.
- `results/feedback_controller_transition_summary.csv` — unit-test transition summary.
- `results/feedback_controller_example_log.json` — compact example audit log.
- `results/experiment2_feedback_controller_summary.json` — integration-run summary.
- `results/experiment2_feedback_controller_integration_results.csv` — all 72 integration scenarios.
- `results/experiment2_feedback_controller_pathway_summary.csv` — pass counts by pathway.
- `results/experiment2_feedback_controller_case_summary.csv` — pass counts by Experiment 2 case.
- `results/experiment2_feedback_controller_representative_runs.csv` — selected frozen run used for each case.

## Tested pathways

Each representative Experiment 2 output was exercised through:

1. `ACCEPT_IMPROVED`
2. `ACCEPT_FIRST_NO_RESPONSE`
3. `ACCEPT_REPEATED_NO_RESPONSE`
4. `ACCEPT_WORSENED`
5. `DECLINE`
6. `OVERRIDE_RETAIN_CURRENT_IMPROVED`

The recorded integration run produced **72/72 passing scenarios** with **0 new LLM calls**.

## Reproduction

1. Run `AHR_Feedback_Controller.ipynb` or `python feedback_controller/unit_tests.py` to verify the deterministic unit/transition tests.
2. Run `AHR_Experiment2_Feedback_Controller_Integration.ipynb` or `python feedback_controller/integration_replay.py`.
3. Confirm the summary reports 12 representative outputs and 72 passing integration scenarios.

The complete 216-event integration audit log is retained in controlled project storage; the public repository includes the structured summary and all 72 scenario rows.

## Interpretation boundary

The 15-minute interval and the labels `IMPROVED`, `NO_RESPONSE` and `WORSENED` are scripted software-test inputs. They are not observed patient trajectories, clinical recommendations or evidence of treatment effect.
