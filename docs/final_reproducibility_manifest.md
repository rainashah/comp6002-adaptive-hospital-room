# Final Reproducibility Manifest

This repository contains the public, de-identified artefacts supporting the COMP6002 Adaptive Hospital Room final report.

## Formal model experiments

- Frozen Experiment 1 cases/evidence, run-level outputs and de-identified nurse comparator.
- Frozen Experiment 2 cases/evidence, run-level outputs, sensitivity summary, stability summary and de-identified nurse comparator.
- Standalone nurse-alignment reproduction script.

## Post-evaluation controller integration

- Implementation: `src/feedback_controller/controller.py`.
- Executable verification: `tests/test_feedback_controller.py` and `tests/test_feedback_controller_integration.py`.
- Notebook interfaces: `notebooks/07_feedback_controller.ipynb` and `notebooks/08_feedback_controller_integration.ipynb`.
- Structured evidence: `results/feedback_controller/`.
- Documentation: `docs/feedback_controller.md`.
- The complete 216-event audit log is retained in controlled Drive storage rather than duplicated publicly.

## Safety and privacy boundary

The repository contains no identifiable patient records or raw reviewer exports. The Experiment 2 cases and controller follow-up states are synthetic. Controller results demonstrate deterministic software behaviour only, not patient benefit or clinical validation.
