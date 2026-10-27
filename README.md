# COMP6002 Adaptive Hospital Room

Project and reproducibility repository for **Adaptive Hospital Room: Agentic LLM Recommendations for Contextually Appropriate Lighting and Sound**, an individual Master of Artificial Intelligence project at Curtin University.

## Scope

AHR is a software-only, non-clinical decision-support prototype. It uses structured physiological summaries, room context, patient preferences, staff restrictions and a fixed evidence representation to recommend permitted lighting and sound settings. It does not diagnose stress, recommend treatment or autonomously control hospital equipment.

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
  experiment2_run_results_60.csv
  controlled_pair_sensitivity_summary.csv
  repeat_stability_by_case.csv
analysis/
  reproduce_alignment.py
docs/
  llm_candidate_screen_audit_2026-10-09.md
  experiment_register.md
requirements.txt
```

## Environment and dependencies

The notebooks were developed in Google Colab using Python 3.

Install dependencies with:

```bash
pip install -r requirements.txt
```

For live model calls, the notebooks expect an **OpenRouter API key** named:

```text
OPENROUTER_API_KEY
```

Do not commit API keys. In Colab, store the key in **Secrets** and grant the notebook access. The notebooks can also fall back to a secure `getpass` prompt.

## Development-stage LLM selection

Before the formal 30-case study, candidate model/provider configurations were screened on the same five development cases (`PILOT_201`-`PILOT_205`) using the same shared case adaptation, evidence, tools, output schema, validation rules and one baseline plus one agentic workflow per case.

The purpose of this screen was **technical workflow reliability**, not nurse alignment or clinical appropriateness.

- **GPT-6 Luna / OpenAI:** 10/10 final-valid workflows, all valid on the first answer; recorded API cost USD $0.01968.
- **Gemini 3.8 Flash / Google AI Studio:** 5/10 final-valid workflows; failures included output-length truncation, duplicate JSON/schema problems and an input-size-blocked correction; recorded API cost USD $0.56152.
- **Qwen3.8 27B / Cerebras:** not executed in the archived full screen because provider/preflight requirements were not satisfied; this is recorded as inconclusive rather than a model failure.

Luna was therefore selected as the strongest **fully tested technical configuration** in the development screen and was frozen for the later formal experiments. This selection does not imply that Luna was clinically superior.

Files:
- `notebooks/00_llm_candidate_reliability_screen.ipynb`
- `results/model_selection_summary.csv`
- `docs/llm_candidate_screen_audit_2026-10-09.md`

## Reproduce the reported nurse-alignment metrics

The repository includes the frozen run-level model outputs used in the main Experiment 1 and Experiment 2 comparisons, together with minimal de-identified nurse comparator files.

From the repository root:

```bash
python analysis/reproduce_alignment.py
```

This reproduces the reported valid-run alignment values, including:

- Experiment 1 agent/baseline brightness, tone, strict sound, exact-command and resulting-sound agreement;
- Experiment 2 brightness, tone, strict sound, resulting-sound, clinical-review and exact-triplet agreement.

The de-identified comparator files contain only the categorical fields required for these calculations. Participant identifiers, access codes, UUIDs, timestamps, professional-background fields, receipt IDs, rationales and notes are not published.

## Experiment 1

### Frozen inputs

- `data/experiment1_formal_30_cases.json` — exact frozen 30-case input dataset.
- `data/experiment1_evidence_table.json` — original concise evidence/rule table.
- `data/experiment1_nurse_comparator_deidentified.csv` — de-identified nurse choices used for agreement scoring.
- `results/experiment1_run_results_300.csv` — frozen 300-run agent/baseline output summary.

The 30-case input JSON SHA-256 is:

`a09d532e3d6d8bcd051e91699d3fb9f933a1f0ae565f6d0f159fc2cb7c735b8b`

The authoritative executable is:

`notebooks/01_experiment1_context_v4_1.ipynb`

The notebook contains the original frozen case/evidence payloads and exports `run_results_300.csv` after a full execution.

## Experiment 2

### Frozen inputs and outputs

- `data/experiment2_cases.json` — exact frozen 12-case controlled synthetic dataset.
- `data/experiment2_evidence_table.json` — frozen evidence table used by the final architecture.
- `data/experiment2_nurse_comparator_deidentified.csv` — de-identified nurse choices used for agreement scoring.
- `results/experiment2_run_results_60.csv` — frozen 60-run model summary.
- `results/controlled_pair_sensitivity_summary.csv` — controlled environment/physiology sensitivity summary.
- `results/repeat_stability_by_case.csv` — repeated-run stability summary.

The authoritative executable is:

`notebooks/06_experiment2_final_agent_v4.ipynb`

Frozen formal design:

- 12 synthetic controlled cases;
- 3 base situations × 2 environment conditions × 2 physiology conditions;
- 5 repeated executions per case;
- 60 formal agentic runs;
- state-aware evidence validation;
- at most one compact correction and one bounded mechanical repair;
- nurse comparator loaded only after model generation.

The recorded formal run produced **60/60 final-valid recommendations**, with **49/60 first-pass valid**.

### Offline validation — no paid API calls

Open `notebooks/06_experiment2_final_agent_v4.ipynb` in Google Colab and keep:

```python
RUN_STAGE = 'offline'
APPROVE_PAID_CALLS = False
```

For an ephemeral/local run, set:

```python
USE_GOOGLE_DRIVE = False
```

Run all cells through the offline validation section. The notebook checks the frozen case/evidence hashes, schemas, deterministic tools, state-aware retained-sound behavior, prompt-size guards and absence of nurse-comparator fields from model prompts.

### Smoke test — paid API call

Add `OPENROUTER_API_KEY`, then change only:

```python
RUN_STAGE = 'smoke'
APPROVE_PAID_CALLS = True
```

Run all cells and confirm the pilot ends as `VALID_SIMULATION` with `final_valid = true`.

### Formal 60-run experiment — paid API calls

After a successful smoke test, change only:

```python
RUN_STAGE = 'full'
APPROVE_PAID_CALLS = True
```

Run all cells again.

The frozen notebook's final post-run comparison cell references the original archived nurse CSV and its hash. That frozen code is intentionally preserved unchanged. For reproduction from the public repository, use `analysis/reproduce_alignment.py`, which performs the same reported categorical agreement calculations from the published de-identified comparator.

The provider endpoint, model availability and prices can change over time, so a later live run is a new stochastic execution of the same software logic rather than a guarantee of byte-identical outputs.

## Other experiment notebooks

The repository includes the final development-stage model-selection notebook plus the main methodological follow-up notebooks, without publishing every abandoned or superseded development version:

- evidence parity and input-guard correction;
- state-aware evidence validation;
- compact correction replay;
- mechanical repair replay.

Historical experiments were not overwritten when the methodology changed; new conditions received new run labels.

## Reproducibility features

The notebooks preserve or log:

- exact model/provider identifier;
- prompts and evidence representation;
- deterministic tool definitions;
- output schema and validators;
- run labels and SHA-256 hashes;
- first-pass and final validity;
- correction/repair use;
- request counts, cost metadata and elapsed time where available.

## Privacy and safety

- no identifiable patient records are included;
- Experiment 2 is fully synthetic;
- the nurse comparator files are de-identified and limited to categorical scoring fields;
- raw participant exports and API keys are excluded;
- staff restrictions remain authoritative in the simulated workflow;
- AHR is research software, not a clinical device.

## Author

Raina Shah  
Master of Artificial Intelligence, Curtin University  
COMP6002 Computer Science Project
