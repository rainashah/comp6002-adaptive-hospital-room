# Adaptive Hospital Room — Independent audit of full Luna/Gemini development run

**Date:** 9 October 2026  
**Uploaded archive:** `AHR_WESAD5_Three_Model_Master_v1_RESULTS-2.zip`  
**Phase:** Development-stage LLM selection based strictly on *technical workflow completion*. Nurse alignment, recommendation appropriateness and clinical effectiveness are not assessed.

## Experiment integrity

- Original five WESAD-derived case input records: `PILOT_201`–`PILOT_205`.
- All five original per-case canonical SHA-256 values match the archived export manifest, and the unmodified export's byte SHA-256 matches the manifest.
- Both Luna and Gemini have all ten planned case/workflow results (one baseline and one bounded agentic workflow per case).
- The four earlier `PILOT_201` smoke-test workflow records (two models × two workflows) are byte-identical to the records in this full export. They were carried forward rather than generated again.
- Qwen3.8 27B was not executed in this archive: Cerebras preflight failed, then the full stage correctly blocked because Qwen smoke results were missing. This does **not** count as a Qwen model failure.

## Full-run outcome

| Model / OpenRouter provider | Cases | Workflows attempted | Valid first answers | Final valid workflows | Baseline | Agentic | HTTP responses | Recorded API cost (USD) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-6 Luna / OpenAI | 5 | 10 | 10 | **10/10** | 5/5 | 5/5 | 16/16 HTTP 200 | $0.01968 |
| Gemini 3.8 Flash / Google AI Studio | 5 | 10 | 5 | **5/10** | 4/5 | 1/5 | 19/19 HTTP 200 | $0.56152 |
| Qwen3.8 27B / Cerebras | 0 | 0 | 0 | Not tested | Not run | Not run | 0 | $0 |

**Combined confirmed provider ledger cost:** $0.58120 (USD; rounded). Luna and Gemini use high reasoning, but differ in model-specific inference parameters. Outputs were subjected to the same shared mechanical validation requirements.

## Per-case workflow outcomes

| Case | Luna baseline | Luna agentic | Gemini baseline | Gemini agentic |
|---|---|---|---|---|
| PILOT_201 — ordinary comfort | Valid | Valid | Valid | Valid |
| PILOT_202 — unknown preferences | Valid | Valid | Valid | Truncated output |
| PILOT_203 — unavailable comparisons | Valid | Valid | Valid | Truncated output |
| PILOT_204 — movement context | Valid | Valid | Valid | Truncated output |
| PILOT_205 — locked lighting | Valid | Valid | Invalid JSON (duplicate `policy_ids` key); withheld | Schema error (missing `sound.option`); revision stopped by input-size safeguard |

### Gemini failures: evidence from saved raw responses

1. `PILOT_202 agent`: final request finished with `finish_reason=length`, 16,380 completion tokens, including 15,726 reasoning tokens. Final structured answer was not accepted.
2. `PILOT_203 agent`: final request finished with `finish_reason=length`, 16,380 completion tokens, including 15,729 reasoning tokens. Final structured answer was not accepted.
3. `PILOT_204 agent`: final request finished with `finish_reason=length`, 16,380 completion tokens, including 15,728 reasoning tokens. Final structured answer was not accepted.
4. `PILOT_205 baseline`: response was received (`finish_reason=stop`) but the validator rejected a duplicate JSON key `policy_ids`; no revision is allowed for baseline.
5. `PILOT_205 agent`: initial final response was rejected because `sound.option` was absent from structured output. The allowed revision could not be sent because the input-size safeguard stopped it. Its final result remains invalid.

All 19 Gemini API requests returned HTTP 200. Therefore these five noncompletions are **not evidence of HTTP outages**. This run also does not establish that Gemini would pass under another inference configuration; such a change would be a distinct development version and should retain the failures above.

## Latency and API request counts

| Model | Mean baseline workflow (s) | Mean agentic workflow (s) | Total HTTP requests |
|---|---:|---:|---:|
| Luna | 31.85 | 19.56 | 16 |
| Gemini | 61.78 | 109.76 | 19 |

Luna's recorded mean agentic time happened to be less than baseline time on this small set. This is not proof that the agentic architecture is faster in general.

## Research interpretation

The development objective is to identify which accessible LLM/provider/inference configuration completes both workflows without format, tool, calculation, evidence-reference, or restriction errors. Under the tested settings **Luna is the strongest of the two fully tested new candidates**: 10/10 final valid, all on the first response. Gemini achieved 5/10, with three agentic output-limit failures and two `PILOT_205` validation/input-size failures. These five scenarios are a small development screen, not a formal performance estimate or nurse-based evaluation.

Historical Qwen3-235B completed 9/10 WESAD workflow runs with a separate mixed-provider configuration, but it is a different model/configuration from the pending Qwen3.8 27B/Cerebras experiment. Keep those results separately labeled.

**Next action:** Run the standalone `AHR_WESAD5_Qwen38_Cerebras_Standalone.ipynb` using its `offline` → `smoke` → `full` stages and upload **`AHR_WESAD5_Qwen38_Cerebras_v1_RESULTS.zip`**. The uploaded three-model master ZIP is not the standalone Qwen result. Do **not** rerun Luna or Gemini.

**Audit scope:** Integrity and consistency of the supplied archive, saved workflow statuses, validation diagnostics, raw finish reasons, request statuses, and cost ledgers. No new paid calls or revisions were made. Accepted recommendations have not been independently judged by nurses or evaluated for clinical appropriateness.