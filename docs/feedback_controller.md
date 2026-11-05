# Deterministic AHR Feedback Controller

The feedback controller is a post-evaluation deterministic software component. It sits after LLM recommendation generation and deterministic validation; it does not make new model calls and does not alter the frozen Experiment 2 model results.

## Final locations
- `src/feedback_controller/controller.py` — controller state machine.
- `tests/test_feedback_controller.py` — executable 12-test unit/transition suite.
- `tests/test_feedback_controller_integration.py` — executable 72-scenario integration replay.
- `notebooks/07_feedback_controller.ipynb` — notebook interface for the unit/transition suite.
- `notebooks/08_feedback_controller_integration.ipynb` — notebook interface for the integration replay.
- `results/feedback_controller/` — structured test and integration evidence.

## Verification
Run from the repository root:

```bash
python tests/test_feedback_controller.py
python tests/test_feedback_controller_integration.py
```

Recorded verification: 12/12 unit/transition tests passed; 72/72 integration scenarios passed; 0 new LLM calls were made.

The complete 216-event integration audit log remains in controlled project storage.

## Interpretation boundary
The 15-minute reassessment interval and the labels `IMPROVED`, `NO_RESPONSE` and `WORSENED` are scripted software-test inputs. They are not observed patient trajectories, clinical recommendations or evidence of treatment effect.
