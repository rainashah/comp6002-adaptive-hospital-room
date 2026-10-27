# AHR Experiment 2 — Final Agent v4 Findings

**Date:** 26 October 2026  
**Formal design:** 12 synthetic cases × 5 repeats = 60 agentic runs  
**Comparator:** one frozen nurse reviewer (17 years nursing experience; MICU)  
**Model:** GPT-6 Luna via the frozen Experiment 2 final-agent v4 architecture  
**Primary caution:** five repeats from the same case are correlated and are not independent patients; all percentages are descriptive. A single nurse is an independent comparator, not a clinical gold standard.

## Executive summary

The final Experiment 2 system completed all **60/60 formal runs with a valid final recommendation**. First-pass validity was **49/60 (81.7%)**; **11/60 (18.3%)** used the prespecified compact-correction path, and **0/60** required mechanical repair. The formal workflow cost was **$0.138** (mean **$0.0023/run**) with a mean elapsed time of **33.9 s/run**.

Against NURSE-001, run-level agreement was:

| Outcome | Agreement |
|---|---:|
| Brightness action | **43/60 (71.7%)** |
| Light tone | **60/60 (100.0%)** |
| Strict sound command | **21/60 (35.0%)** |
| **Resulting sound state** | **50/60 (83.3%)** |
| Clinical-review / assessment flag | **52/60 (86.7%)** |
| Exact brightness + tone + sound command | **15/60 (25.0%)** |
| **Exact brightness + tone + resulting sound** | **38/60 (63.3%)** |

Using one modal model recommendation per case to reduce repeat pseudo-replication, agreement was **9/12 brightness**, **12/12 tone**, **4/12 strict sound command**, **10/12 resulting sound**, **10/12 clinical review**, and **8/12 exact resulting-state triplet**.

The most important finding is that **command-level sound agreement substantially understates actual environmental agreement**. Of the 39 strict sound-command disagreements, **29 (74.4%) produced exactly the same resulting sound state as the nurse recommendation**. Only 10/60 runs had a genuine sound-state disagreement, all in the two supportive overnight cases.

## 1. Technical reliability

- Planned formal runs: **60**
- Attempted: **60**
- Final valid: **60/60 (100%)**
- First-pass valid: **49/60 (81.7%)**
- Compact correction used: **11/60 (18.3%)**
- Mechanical repair used: **0/60**
- Total HTTP requests: **131**
- Mean HTTP requests/run: **2.18**
- Formal workflow cost: **$0.137947**
- Mean elapsed time/run: **33.9 s**
- Median elapsed time/run: **30.6 s**

Ten of the eleven compact corrections were concentrated in E2_001/E2_002, the supportive overnight cases with an already-active nature-sound state. Sampled records show the known E05 retained-active-sound contract issue: the first answer could place E05 on a `NO_CHANGE` retained-sound recommendation, after which compact correction removed the inappropriate policy citation and preserved the substantive recommendation. The remaining correction occurred in E2_009 when E05 was placed in `sound.evidence_ids` instead of the policy field. No final recommendation remained invalid.

**Interpretation:** the deployable correction layer achieved 100% final technical validity, but the first-pass rate shows that the citation/output contract still creates a recurring mechanical correction burden in particular `NO_CHANGE` sound states. This should be reported, not hidden by the 100% final-valid rate.

## 2. Nurse alignment — command versus resulting state

The largest discrepancy between strict-command and resulting-state scoring is sound.

- Strict sound command agreement: **35.0%**
- Resulting sound agreement: **83.3%**
- Improvement when scoring the resulting state: **+48.3 percentage points**

The 29 command-only disagreements were mainly:

- daytime cases: nurse explicitly selected `PREFERRED_CALMING_MUSIC`, while the model selected `NO_CHANGE` because that preferred music was already playing;
- postoperative cases: `NO_CHANGE` and `NONE_SILENCE` both resulted in silence.

The **10 substantive sound-state disagreements** were all E2_001/E2_002. NURSE-001 selected `WHITE_NOISE`, whereas the model consistently retained the already-playing, patient-acceptable `NATURE_SOUNDS`.

This strongly supports the decision to evaluate **resulting environmental state**, rather than treating the literal control command as the sole outcome.

## 3. Brightness disagreement pattern

All **17 brightness disagreements** had the same direction:

> **Nurse = DECREASE; model = NO_CHANGE**

They occurred in:

- E2_001: 5/5 runs
- E2_009: 5/5
- E2_010: 5/5
- E2_011: 2/5

There were no cases where the model increased when the nurse decreased, or vice versa.

The model was therefore systematically **more conservative about changing brightness in rooms it already regarded as supportive or acceptable**. For example:

- E2_001: current room was dim/warm with no complaint; model retained 22%, nurse preferred a decrease.
- E2_009/E2_010: current postoperative room was warm and moderately dim at 45%; model retained it, while the nurse decreased toward the 40% staff minimum.
- E2_011: the model varied between retaining 45% and decreasing; the nurse consistently decreased.

This is a policy-style difference rather than random disagreement.

## 4. Clinical-review / assessment behavior

Clinical-review agreement was **52/60 (86.7%)**.

Every disagreement occurred in the **overnight changed-physiology cases**:

- E2_002: model recommended review in 3/5 runs; nurse = NO.
- E2_004: model recommended review in 5/5; nurse = NO.

The model and nurse agreed:

- NO review for all stable-physiology cases;
- NO review for both daytime changed-physiology cases;
- YES review for all postoperative changed-physiology cases (E2_010/E2_012).

Thus the system correctly differentiated the deliberately large postoperative pattern (HR 90→122 bpm, RMSSD 30→15 ms, EDA 2.9→5.0 µS), but was **more sensitive than NURSE-001 to the overnight arousal-like profile** (HR +14 bpm, RMSSD −14 ms, EDA +1.0 µS).

The clinical-review field already existed in the nurse instrument before the nurse completed it. The analogous model field was finalized during pre-formal piloting. The frozen nurse response file was not available to model inference or validation and was loaded only after all 60 model records existed.

## 5. Controlled environment-versus-physiology sensitivity

### Case-mode changes across the six matched environment contrasts

| Outcome         | Environment contrast — model   | Environment contrast — nurse   | Physiology contrast — model   | Physiology contrast — nurse   |
|:----------------|:-------------------------------|:-------------------------------|:------------------------------|:------------------------------|
| Lighting action | 6/6                            | 3/6                            | 0/6                           | 1/6                           |
| Light tone      | 0/6                            | 0/6                            | 0/6                           | 0/6                           |
| Resulting sound | 2/6                            | 0/6                            | 0/6                           | 0/6                           |
| Clinical review | 0/6                            | 0/6                            | 4/6                           | 2/6                           |

The most interpretable pattern is:

- **Environment changed → model environmental action changed.**
  - Lighting changed in **6/6** environment pairs.
  - Resulting sound changed in **2/6**, both overnight pairs.
  - Light tone changed in **0/6**.
  - Clinical-review mode changed in **0/6**.

- **Physiology changed → model largely preserved the environment.**
  - Modal lighting action changed in **0/6** physiology pairs.
  - Tone changed in **0/6**.
  - Resulting sound changed in **0/6**.
  - Clinical review changed in **4/6**.

This is an important system-level result: **the final agent generally used room/environment information to drive environmental controls and used physiological changes to influence escalation/review rather than automatically changing the room**.

NURSE-001 showed a similar but less pronounced separation: clinical assessment changed in **2/6** physiology pairs (the two postoperative cases), and brightness changed in **1/6** physiology pairs.

The model was therefore more sensitive to physiology in the clinical-review channel, but did not translate that sensitivity into sound or tone changes.

## 6. Agreement by clinical situation

| Situation                  | Brightness   | Tone   | Sound command   | Resulting sound   | Clinical review   | Exact command triplet   | Exact resulting-state triplet   |
|:---------------------------|:-------------|:-------|:----------------|:------------------|:------------------|:------------------------|:--------------------------------|
| Daytime wakefulness        | 100.0%       | 100.0% | 0.0%            | 100.0%            | 100.0%            | 0.0%                    | 100.0%                          |
| Overnight sleep            | 75.0%        | 100.0% | 50.0%           | 50.0%             | 60.0%             | 50.0%                   | 50.0%                           |
| Postoperative evening rest | 40.0%        | 100.0% | 55.0%           | 100.0%            | 100.0%            | 25.0%                   | 40.0%                           |

### Daytime wakefulness

This was the cleanest domain. All 20 model runs matched the nurse on **brightness, tone, resulting sound and clinical review**. Strict sound-command agreement was 0% only because the model used `NO_CHANGE` to retain the already-playing preferred music while the nurse explicitly selected the music option.

### Overnight sleep

Environmental agreement was strong in the disruptive cases but weaker in supportive cases. The model retained acceptable nature sounds in supportive rooms, while the nurse consistently preferred switching to white noise. The model also escalated the changed physiology more often than the nurse.

### Postoperative evening rest

Tone, resulting silence and clinical-review behavior were highly consistent with the nurse. The main disagreement was brightness: the model often retained an already warm/moderately dim supportive room while the nurse decreased brightness to the lowest staff-permitted level.

## 7. Case-level modal comparison

| Case   | Situation                  | Environment   | Physiology   | Nurse brightness   | Model brightness mode   | Nurse tone   | Model tone mode   | Nurse resulting sound   | Model resulting sound mode   | Nurse clinical review   | Model clinical review mode   | Exact resulting-state runs   | Clinical-review agreement runs   |
|:-------|:---------------------------|:--------------|:-------------|:-------------------|:------------------------|:-------------|:------------------|:------------------------|:-----------------------------|:------------------------|:-----------------------------|:-----------------------------|:---------------------------------|
| E2_001 | Overnight sleep            | Supportive    | Stable       | DECREASE           | NO_CHANGE               | WARM         | WARM              | WHITE_NOISE             | NATURE_SOUNDS                | NO                      | NO                           | 0/5                          | 5/5                              |
| E2_002 | Overnight sleep            | Supportive    | Changed      | NO_CHANGE          | NO_CHANGE               | WARM         | WARM              | WHITE_NOISE             | NATURE_SOUNDS                | NO                      | YES                          | 0/5                          | 2/5                              |
| E2_003 | Overnight sleep            | Disruptive    | Stable       | DECREASE           | DECREASE                | WARM         | WARM              | WHITE_NOISE             | WHITE_NOISE                  | NO                      | NO                           | 5/5                          | 5/5                              |
| E2_004 | Overnight sleep            | Disruptive    | Changed      | DECREASE           | DECREASE                | WARM         | WARM              | WHITE_NOISE             | WHITE_NOISE                  | NO                      | YES                          | 5/5                          | 0/5                              |
| E2_005 | Daytime wakefulness        | Supportive    | Stable       | NO_CHANGE          | NO_CHANGE               | NEUTRAL      | NEUTRAL           | PREFERRED_CALMING_MUSIC | PREFERRED_CALMING_MUSIC      | NO                      | NO                           | 5/5                          | 5/5                              |
| E2_006 | Daytime wakefulness        | Supportive    | Changed      | NO_CHANGE          | NO_CHANGE               | NEUTRAL      | NEUTRAL           | PREFERRED_CALMING_MUSIC | PREFERRED_CALMING_MUSIC      | NO                      | NO                           | 5/5                          | 5/5                              |
| E2_007 | Daytime wakefulness        | Disruptive    | Stable       | INCREASE           | INCREASE                | NEUTRAL      | NEUTRAL           | PREFERRED_CALMING_MUSIC | PREFERRED_CALMING_MUSIC      | NO                      | NO                           | 5/5                          | 5/5                              |
| E2_008 | Daytime wakefulness        | Disruptive    | Changed      | INCREASE           | INCREASE                | NEUTRAL      | NEUTRAL           | PREFERRED_CALMING_MUSIC | PREFERRED_CALMING_MUSIC      | NO                      | NO                           | 5/5                          | 5/5                              |
| E2_009 | Postoperative evening rest | Supportive    | Stable       | DECREASE           | NO_CHANGE               | WARM         | WARM              | NONE_SILENCE            | NONE_SILENCE                 | NO                      | NO                           | 0/5                          | 5/5                              |
| E2_010 | Postoperative evening rest | Supportive    | Changed      | DECREASE           | NO_CHANGE               | WARM         | WARM              | NONE_SILENCE            | NONE_SILENCE                 | YES                     | YES                          | 0/5                          | 5/5                              |
| E2_011 | Postoperative evening rest | Disruptive    | Stable       | DECREASE           | DECREASE                | WARM         | WARM              | NONE_SILENCE            | NONE_SILENCE                 | NO                      | NO                           | 3/5                          | 5/5                              |
| E2_012 | Postoperative evening rest | Disruptive    | Changed      | DECREASE           | DECREASE                | WARM         | WARM              | NONE_SILENCE            | NONE_SILENCE                 | YES                     | YES                          | 5/5                          | 5/5                              |

## 8. Repeat stability

Repeat stability was high for the outcomes that matter at the resulting-state level:

- Light tone modal share: **100% in all 12 cases**
- Resulting sound-state modal share: **100% in all 12 cases**
- Lighting action: **11/12 cases had 100% agreement across repeats**; E2_011 was 3/5 DECREASE vs 2/5 NO_CHANGE
- Clinical review: **11/12 cases had 100% agreement across repeats**; E2_002 was 3/5 YES vs 2/5 NO
- Strict sound command varied in E2_010–E2_012, but the resulting sound remained **silence in 5/5 runs for every postoperative case**

All 60 runs reported `certainty = MEDIUM`. This is conservative but **non-discriminating**; the certainty field did not distinguish between stable, changed, supportive or disruptive cases in this experiment.

## 9. What Experiment 2 supports

Experiment 2 supports the following descriptive claims:

1. The final architecture achieved **100% final technical validity** using its prespecified bounded correction layer.
2. **Resulting-state scoring is materially more meaningful than command-only scoring** for an adaptive room where `NO_CHANGE` can preserve an already-desired environmental state.
3. The final agent showed strong alignment with NURSE-001 on **tone (100%)**, **resulting sound (83.3%)**, and **clinical review (86.7%)**.
4. The controlled manipulation produced the intended separation: **environmental changes primarily altered environmental recommendations, while physiological changes primarily altered clinical-review behavior**.
5. The most important residual differences were interpretable rather than random:
   - model more conservative about brightness changes in already-supportive rooms;
   - model retained acceptable existing nature sounds rather than switching to the nurse's first-choice white noise;
   - model was more likely than the nurse to recommend review for the moderate overnight changed-physiology pattern.

## 10. What Experiment 2 does not support

Do not claim:

- that the model is clinically correct because it agrees with one nurse;
- that 60 runs represent 60 independent patients;
- that Experiment 2 proves superiority over the baseline, because no baseline was run in Experiment 2;
- that the final architecture is statistically superior to Experiment 1, because the case designs, evidence, output contract and evaluation metrics differ;
- that clinical-review disagreement means either the nurse or model was wrong;
- that lux or dBA values establish patient stress, sleep or clinical abnormality.

## 11. Recommended report framing

A defensible main finding is:

> In a controlled 12-case synthetic evaluation, the final agentic AHR produced valid recommendations in all 60 formal executions after bounded correction. Agreement with an experienced nurse was strongest for light tone, resulting sound state and clinical-review decisions. Command-level sound agreement substantially understated environmental agreement because the model frequently selected `NO_CHANGE` when the nurse explicitly selected the same sound already present in the room. Controlled contrasts showed that the agent generally changed environmental recommendations in response to environmental manipulations while keeping those recommendations stable across physiological manipulations, using clinical-review recommendations instead to respond to notable physiological change.

The strongest methodological contribution is therefore not “the AI matched the nurse perfectly.” It is that **state-aware evaluation and controlled factor manipulation reveal whether the system is responding to the right kind of information in the right output channel**.

## Source integrity

- Frozen nurse CSV SHA-256: `fd11d3cf2523cf43dff938db6e459d72b08277d040162bfbfa48469ee9c56cd5`
- Formal 60-run result CSV SHA-256: `ac512b2a9cc65df201a147df6d7c0d85b2df2cb5137d07d66864efc9b5887c58`
- Nurse responses were loaded only after all model records existed and were not visible to the model or validator.