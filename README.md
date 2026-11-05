# COMP6002 Adaptive Hospital Room

Project and reproducibility repository for **Adaptive Hospital Room: Agentic LLM Recommendations for Contextually Appropriate Lighting and Sound**, an individual Master of Artificial Intelligence project at Curtin University.

## Scope

AHR is a software-only, non-clinical decision-support prototype. It uses structured physiological summaries, room context, patient preferences, staff restrictions and fixed evidence representations to recommend permitted lighting and sound settings. It does not diagnose stress, recommend treatment or autonomously control hospital equipment.

## Repository structure

```text
notebooks/
  00_llm_candidate_reliability_screen.ipynb
  01_experiment1_context_v4_1.ipynb
  02_evidence_parity_v3_guardfix.ipynb
  03_state_aware_evidence_v4.ipynb
  04_compact_correction_replay.ipynb
  05_mechanical_repair_replay.ipynb
  06_experiment2_final_agent_v4.ipynb
  07_feedback_controller.ipynb
  08_feedback_controller_integration.ipynb
src/
  feedback_controller/
    __init__.py
    controller.py
tests/
  test_feedback_controller.py
  test_feedback_controller_integration.py
data/
  README.md
  experiment1_formal_30_cases.json
  experiment1_evidence_table.json
  experiment1_nurse_comparator_deidentified.csv
  experiment2_cases.json
  experiment2_evidence_table.json
  experiment2_nurse_comparator_deidentified.csv
results/
  model_selection_summary.csv
  experiment1_run_results_300.csv
  experiment1_repeatability_summary.csv
  experiment2_run_results_60.csv
  controlled_pair_sensitivity_summary.csv
  repeat_stability_by_case.csv
  feedback_controller/
    feedback_controller_test_results.csv
    feedback_controller_transition_summary.csv
    feedback_controller_example_log.json
    experiment2_feedback_controller_summary.json
    experiment2_feedback_controller_integration_results.csv
    experiment2_feedback_controller_pathway_summary.csv
    experiment2_feedback_controller_case_summary.csv
    experiment2_feedback_controller_representative_runs.csv
analysis/
  reproduce_alignment.py
docs/
  llm_candidate_screen_audit_2026-10-09.md
  experiment_register.md
  final_reproducibility_manifest.md
  feedback_controller.md
requirements.txt
```

The numbered notebooks follow the project sequence. Reusable controller code is under `src/`, executable verification scripts are under `tests/`, and generated evidence is under `results/`.

## Environment and dependencies

The notebooks were developed in Google Colab using Python 3.

```bash
pip install -r requirements.txt
```

Live model experiments require an **OpenRouter API key** named `OPENROUTER_API_KEY`. Do not commit API keys. Store the key in Colab Secrets or supply it through the secure prompt in the notebooks.

The controller notebooks and tests use only the frozen Experiment 2 outputs and make no new LLM calls.

## Development-stage LLM selection

Before the formal 30-case study, candidate model/provider configurations were screened on the same five development cases using the same shared case adaptation, evidence, tools, output schema, validation rules and one baseline plus one agentic workflow per case.

The purpose of this screen was **technical workflow reliability**, not nurse alignment or clinical appropriateness.

- **GPT-6 Luna / OpenAI:** 10/10 final-valid workflows, all valid on the first answer.
- **Gemini 3.8 Flash / Google AI Studio:** 5/10 final-valid workflows; failures included output truncation, duplicate JSON/schema problems and an input-size-blocked correction.
- **Qwen3.8 27B / Cerebras:** not executed in the archived full screen because provider/preflight requirements were not satisfied; recorded as inconclusive rather than a model failure.

Luna was selected as the strongest fully tested technical configuration for the formal experiments. This does not imply clinical superiority.

Files:
- `notebooks/00_llm_candidate_reliability_screen.ipynb`
- `results/model_selection_summary.csv`
- `docs/llm_candidate_screen_audit_2026-10-09.md`

## Reproduce the nurse-alignment metrics

The repository includes the frozen run-level model outputs used in the main Experiment 1 and Experiment 2 comparisons, together with minimal de-identified nurse comparator files.

From the repository root:

```bash
python analysis/reproduce_alignment.py
```

This reproduces the reported valid-run alignment values, including:

- Experiment 1 agent/baseline brightness, tone, strict sound, exact-command and resulting-sound agreement;
- Experiment 2 brightness, tone, strict sound, resulting-sound, clinical-review and exact-triplet agreement.

The de-identified comparator files contain only the categorical fields required for scoring. Participant identifiers, access codes, UUIDs, timestamps, professional-background fields, receipt IDs, rationales and notes are not published.

## Experiment 1

### Frozen inputs and outputs

- `data/experiment1_formal_30_cases.json` — frozen 30-case input dataset.
- `data/experiment1_evidence_table.json` — original concise evidence/rule table.
- `data/experiment1_nurse_comparator_deidentified.csv` — de-identified nurse choices used for agreement scoring.
- `results/experiment1_run_results_300.csv` — frozen 300-run agent/baseline output summary.
- `results/experiment1_repeatability_summary.csv` — case-level five-repeat consistency summary.

The authoritative executable is `notebooks/01_experiment1_context_v4_1.ipynb`.

## Experiment 2

### Frozen inputs and outputs

- `data/experiment2_cases.json` — frozen 12-case controlled synthetic dataset.
- `data/experiment2_evidence_table.json` — frozen evidence table used by the final architecture.
- `data/experiment2_nurse_comparator_deidentified.csv` — de-identified nurse choices used for agreement scoring.
- `results/experiment2_run_results_60.csv` — frozen 60-run model summary.
- `results/controlled_pair_sensitivity_summary.csv` — matched environment/physiology sensitivity summary.
- `results/repeat_stability_by_case.csv` — repeated-run stability summary.

The authoritative executable is `notebooks/06_experiment2_final_agent_v4.ipynb`.

Frozen design:

- 12 synthetic controlled cases;
- 3 base situations × 2 environment conditions × 2 physiology conditions;
- 5 repeated executions per case;
- 60 formal agentic runs;
- state-aware evidence validation;
- at most one compact correction and one bounded mechanical repair;
- nurse comparator loaded only after model generation.

The recorded formal run produced **60/60 final-valid recommendations**, with **49/60 first-pass valid**.

### Offline validation — no paid API calls

Open `notebooks/06_experiment2_final_agent_v4.ipynb` and keep:

```python
RUN_STAGE = 'offline'
APPROVE_PAID_CALLS = False
```

For an ephemeral/local run, set `USE_GOOGLE_DRIVE = False`, then run all cells through the offline validation section.

### Smoke/full modes — paid API calls

After adding `OPENROUTER_API_KEY`, use `RUN_STAGE = 'smoke'` for a one-case live test or `RUN_STAGE = 'full'` for a new 60-run stochastic execution. Set `APPROVE_PAID_CALLS = True` only when intentionally making paid calls.

The frozen notebook's post-run comparison cell references the archived nurse CSV and its hash. For public reproduction, use `analysis/reproduce_alignment.py` with the published de-identified comparator.

## Repeatability / stochastic consistency

The formal experiments repeated identical cases under the same frozen configuration to measure stochastic consistency rather than treating repeats as independent patients.

- Experiment 1 used five repeats per case in both workflows: 30 cases × 2 workflows × 5 repeats = 300 executions.
- Experiment 2 used five repeats for each of 12 controlled cases: 60 executions.

The frozen summaries are `results/experiment1_repeatability_summary.csv` and `results/repeat_stability_by_case.csv`.

## Deterministic feedback controller

After the formal model evaluation, a deterministic post-recommendation controller was implemented as a separate human-in-the-loop software layer. It receives an already validated recommendation and makes no new LLM calls.

Public verification from the repository root:

```bash
python tests/test_feedback_controller.py
python tests/test_feedback_controller_integration.py
```

Recorded results:
- **12/12 unit and transition tests passed**;
- one representative final-valid output from each of the 12 Experiment 2 cases was exercised through six scripted pathways;
- **72/72 integration scenarios passed**;
- **0 new LLM calls** were made.

These are scripted software-test conditions, not patient observations, treatment outcomes or evidence that the 15-minute interval is clinically valid.

Final controller artefacts:
- implementation: `src/feedback_controller/controller.py`;
- notebook interfaces: `notebooks/07_feedback_controller.ipynb` and `notebooks/08_feedback_controller_integration.ipynb`;
- executable verification: `tests/test_feedback_controller.py` and `tests/test_feedback_controller_integration.py`;
- structured evidence: `results/feedback_controller/`;
- documentation: `docs/feedback_controller.md`.

The complete 216-event integration audit log is retained in controlled project storage rather than duplicated in the public repository.

## Reproducibility features

The project artefacts preserve or log:

- exact model/provider identifier;
- prompts and evidence representation;
- deterministic tool definitions;
- output schema and validators;
- run labels and SHA-256 hashes;
- first-pass and final validity;
- correction/repair use;
- request counts, cost metadata and elapsed time where available;
- controller events, states, actions and scripted transition outcomes.

Historical experiments were not overwritten when the methodology changed; new conditions received new run labels.

## Privacy and safety

- no identifiable patient records are included;
- Experiment 2 is fully synthetic;
- nurse comparator files are de-identified and limited to categorical scoring fields;
- raw participant exports and API keys are excluded;
- staff restrictions and explicit staff decisions remain authoritative;
- feedback states are scripted software tests, not clinical outcomes;
- AHR is research software, not a clinical device.

## Author

Raina Shah  
Master of Artificial Intelligence, Curtin University  
COMP6002 Computer Science Project
