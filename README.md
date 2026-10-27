# COMP6002 Adaptive Hospital Room

Marker-facing repository for **Adaptive Hospital Room: Agentic LLM Recommendations for Contextually Appropriate Lighting and Sound**, an individual Master of Artificial Intelligence project at Curtin University.

## Scope

AHR is a software-only, non-clinical decision-support prototype. It uses structured physiological summaries, room context, patient preferences, staff restrictions and a fixed evidence representation to recommend permitted lighting and sound settings. It does not diagnose stress, recommend treatment or autonomously control hospital equipment.

## Repository structure

```text
notebooks/
  01_experiment1_context_v4_1.ipynb
  02_evidence_parity_v3_guardfix.ipynb
  03_state_aware_evidence_v4.ipynb
  04_compact_correction_replay.ipynb
  05_mechanical_repair_replay.ipynb
  06_experiment2_final_agent_v4.ipynb
data/
  experiment2_cases.json
  evidence_table.json
results/
  experiment2_run_results_60.csv
  controlled_pair_sensitivity_summary.csv
  repeat_stability_by_case.csv
  experiment2_case_level_summary.csv
docs/
  experiment2_findings.md
  experiment_register.md
requirements.txt
```

## Recommended reproduction target

Use `notebooks/06_experiment2_final_agent_v4.ipynb`.

Frozen formal design:

- 12 synthetic controlled cases
- 3 base situations × 2 environment conditions × 2 physiology conditions
- 5 repeated executions per case
- 60 formal agentic runs
- state-aware evidence validation
- at most one compact correction and one bounded mechanical repair
- nurse comparator loaded only after model generation

The recorded formal run produced **60/60 final-valid recommendations**, with **49/60 first-pass valid**.

## Environment and dependencies

The notebooks were developed in Google Colab using Python 3.

Install the small Python dependency set with:

```bash
pip install -r requirements.txt
```

The main notebook also contains its own `%pip` installation cell.

For live calls, the notebook expects an **OpenRouter API key** named:

```text
OPENROUTER_API_KEY
```

Do not commit API keys. In Colab, store the key in **Secrets** and grant the notebook access. The notebook can also fall back to a secure `getpass` prompt.

## Reproduction instructions

### 1. Offline validation — no paid API calls

Open `notebooks/06_experiment2_final_agent_v4.ipynb` in Google Colab.

Keep:

```python
RUN_STAGE = 'offline'
APPROVE_PAID_CALLS = False
```

For an ephemeral/local run, set:

```python
USE_GOOGLE_DRIVE = False
```

Run all cells through the offline validation section. The notebook checks:

- 12-case frozen design
- case/evidence hashes
- schemas and deterministic tools
- state-aware retained-sound behavior
- prompt-size guards
- absence of nurse-comparator fields from model prompts

### 2. Smoke test — paid API call

Add `OPENROUTER_API_KEY`, then change only:

```python
RUN_STAGE = 'smoke'
APPROVE_PAID_CALLS = True
```

Run all cells. Confirm the pilot ends as `VALID_SIMULATION` with `final_valid = true`.

### 3. Formal 60-run experiment — paid API calls

After a successful smoke test, change only:

```python
RUN_STAGE = 'full'
APPROVE_PAID_CALLS = True
```

Run all cells again.

The notebook writes a frozen run contract/fingerprint, logs each request/output, and is resume-safe. The provider endpoint, model availability and prices can change over time, so a later reproduction is a new stochastic execution of the same software logic rather than a guarantee of byte-identical outputs.

## Experiment 2 data

`data/experiment2_cases.json` and `data/evidence_table.json` are exported from the exact frozen objects embedded in the final notebook. The notebook is the authoritative executable artifact.

## Protected nurse comparator

The public repository intentionally does **not** include the raw nurse-response CSV. It contains human-participant responses and is retained in the controlled project archive.

This does not affect reproduction of model generation: the final notebook is explicitly structured so the nurse file is not read by inference, tools, validation or repair. It is loaded only in the final post-run comparison cell.

The public `results/` folder contains non-identifying model and aggregate comparison summaries used in the report.

## Reproducibility features

The notebooks preserve or log:

- exact model/provider identifier
- prompts and evidence representation
- deterministic tool definitions
- output schema and validators
- run labels and SHA-256 hashes
- first-pass and final validity
- correction/repair use
- request counts, cost metadata and elapsed time where available

Historical experiments were not overwritten when the methodology changed; new conditions received new run labels.

## Privacy and safety

- no identifiable patient records are included;
- Experiment 2 is fully synthetic;
- API keys and raw nurse responses are excluded;
- staff restrictions remain authoritative in the simulated workflow;
- AHR is research software, not a clinical device.

## Author

Raina Shah  
Master of Artificial Intelligence, Curtin University  
COMP6002 Computer Science Project