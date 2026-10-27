# Data files

This folder contains the frozen case/evidence inputs needed to reproduce the experiments and minimal de-identified nurse comparator files needed to recompute nurse-alignment metrics.

## Experiment 1

- `experiment1_formal_30_cases.json` — frozen 30-case input set embedded in the Experiment 1 notebook.
- `experiment1_evidence_table.json` — original concise evidence/rule table used by the frozen Experiment 1 workflow.
- `experiment1_nurse_comparator_deidentified.csv` — de-identified nurse choices required for alignment scoring.

The comparator contains only:
`case_id`, `lighting_action`, `lighting_tone`, and `sound_option`.

`KEEP_CURRENT` is retained exactly as submitted and can be resolved against the current room state in the corresponding case when computing resulting-state agreement.

## Experiment 2

- `experiment2_cases.json` — frozen 12-case controlled synthetic input set.
- `experiment2_evidence_table.json` — frozen evidence table used by the final Experiment 2 notebook.
- `experiment2_nurse_comparator_deidentified.csv` — de-identified nurse choices required for alignment scoring.

The comparator contains only:
`case_id`, `brightness_recommendation`, `tone_recommendation`, `sound_recommendation`, and `clinical_assessment_needed`.

## Privacy

The public comparator files intentionally exclude participant identifiers, access codes, UUIDs, timestamps, professional-background fields, receipt IDs, free-text rationales, notes, and other metadata not required to reproduce the reported agreement metrics.