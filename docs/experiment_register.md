# AHR Experiment and Integration Register

This register identifies the final artefacts used in the COMP6002 report. Historical development versions remain in controlled project storage and are not overwritten.

| Stage | Purpose | Authoritative artefact | Frozen output / evidence |
|---|---|---|---|
| Development model screen | Compare technical workflow reliability before the formal study | `notebooks/00_llm_candidate_reliability_screen.ipynb` | `results/model_selection_summary.csv`; `docs/llm_candidate_screen_audit_2026-10-09.md` |
| Experiment 1 | Compare agentic and same-model non-agentic workflows on 30 frozen cases against the independent nurse comparator | `notebooks/01_experiment1_context_v4_1.ipynb` | `results/experiment1_run_results_300.csv`; `results/experiment1_repeatability_summary.csv` |
| Evidence parity / reliability follow-ups | Investigate evidence-access, state-aware validation and bounded repair effects without overwriting Experiment 1 | `notebooks/02_evidence_parity_v3_guardfix.ipynb` to `notebooks/05_mechanical_repair_replay.ipynb` | Follow-up outputs documented in the report and controlled project archive |
| Experiment 2 | Evaluate the refined final architecture using 12 controlled synthetic cases and five repeats per case | `notebooks/06_experiment2_final_agent_v4.ipynb` | `results/experiment2_run_results_60.csv`; `results/controlled_pair_sensitivity_summary.csv`; `results/repeat_stability_by_case.csv` |
| Nurse-alignment reproduction | Recompute reported categorical agreement metrics without new model calls | `analysis/reproduce_alignment.py` | Published de-identified comparator files and frozen run summaries |
| Feedback-controller unit testing | Test deterministic accept, decline, override and reassessment transitions | `src/feedback_controller/controller.py`, `tests/test_feedback_controller.py` and `notebooks/07_feedback_controller.ipynb` | 12/12 tests passed; structured CSV/log outputs in `results/feedback_controller/` |
| Feedback-controller integration | Pass representative final-valid Experiment 2 outputs through six deterministic pathways per case | `tests/test_feedback_controller_integration.py` and `notebooks/08_feedback_controller_integration.ipynb` | 12 cases × 6 pathways = 72/72 passing scenarios; 0 new LLM calls |

## Interpretation notes

- Formal model experiments and feedback-controller testing are separate stages.
- The controller integration reuses frozen final-valid Experiment 2 outputs and does not modify Experiment 2 results.
- Controller follow-up states are scripted software-test conditions, not patient observations or clinical outcomes.
- Raw participant exports, reviewer identifiers, access codes and free-text nurse responses are excluded from the public repository.
