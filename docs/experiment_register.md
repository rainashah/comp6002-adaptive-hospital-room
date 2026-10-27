# Experiment register

| Notebook | Purpose |
|---|---|
| `00_llm_candidate_reliability_screen.ipynb` | Development-stage technical reliability screen used to select the Luna configuration; nurse/clinical appropriateness was not assessed. |
| `01_experiment1_context_v4_1.ipynb` | Original 30-case agent-vs-baseline experiment. |
| `02_evidence_parity_v3_guardfix.ipynb` | Equal evidence access plus corrected local input-size guard. |
| `03_state_aware_evidence_v4.ipynb` | State-aware evidence validation for retained environmental state. |
| `04_compact_correction_replay.ipynb` | Targeted compact correction replay on failed agent records. |
| `05_mechanical_repair_replay.ipynb` | Targeted structured-output/calculation repair replay. |
| `06_experiment2_final_agent_v4.ipynb` | Final controlled 12-case Experiment 2 architecture and formal run. |

Historical raw outputs are preserved in the controlled research archive. The repository includes the frozen inputs, selected run-level result summaries and minimal de-identified nurse comparator files needed to reproduce the reported agreement calculations.

The LLM-selection audit and compact summary are stored in `docs/llm_candidate_screen_audit_2026-10-09.md` and `results/model_selection_summary.csv`. Qwen3.8/Cerebras is recorded as not tested in the archived full screen because provider/preflight requirements were not satisfied, not as a failed model.
