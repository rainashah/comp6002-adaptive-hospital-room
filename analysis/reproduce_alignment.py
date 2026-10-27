#!/usr/bin/env python3
"""Recompute the reported nurse-alignment metrics from de-identified comparators.

Run from the repository root:
    python analysis/reproduce_alignment.py
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"

def pct(n, d):
    return 100.0 * n / d if d else float("nan")

def exp1():
    cases = {c["case_id"]: c for c in json.loads((DATA / "experiment1_formal_30_cases.json").read_text())}
    nurse = pd.read_csv(DATA / "experiment1_nurse_comparator_deidentified.csv").set_index("case_id")
    runs = pd.read_csv(RESULTS / "experiment1_run_results_300.csv")
    valid = runs[runs["final_valid"].astype(str).str.lower().eq("true")].copy()

    def nurse_tone(cid):
        t = nurse.loc[cid, "lighting_tone"]
        return cases[cid]["room"]["tone"] if t == "KEEP_CURRENT" else t

    def resulting_sound(cid, command):
        return cases[cid]["room"]["sound"] if command == "NO_CHANGE" else command

    valid["nurse_brightness"] = [nurse.loc[cid, "lighting_action"] for cid in valid.case_id]
    valid["nurse_tone"] = [nurse_tone(cid) for cid in valid.case_id]
    valid["nurse_sound_command"] = [nurse.loc[cid, "sound_option"] for cid in valid.case_id]
    valid["nurse_resulting_sound"] = [resulting_sound(cid, nurse.loc[cid, "sound_option"]) for cid in valid.case_id]
    valid["model_resulting_sound"] = [resulting_sound(cid, cmd) for cid, cmd in zip(valid.case_id, valid.sound_option)]

    rows = []
    for workflow, g in valid.groupby("workflow"):
        bright = g.lighting_action.eq(g.nurse_brightness)
        tone = g.light_tone.eq(g.nurse_tone)
        sound = g.sound_option.eq(g.nurse_sound_command)
        result_sound = g.model_resulting_sound.eq(g.nurse_resulting_sound)
        rows.append({
            "workflow": workflow,
            "valid_n": len(g),
            "brightness_agreement_pct": pct(bright.sum(), len(g)),
            "tone_agreement_pct": pct(tone.sum(), len(g)),
            "strict_sound_agreement_pct": pct(sound.sum(), len(g)),
            "exact_command_triplet_pct": pct((bright & tone & sound).sum(), len(g)),
            "resulting_sound_agreement_pct": pct(result_sound.sum(), len(g)),
        })
    return pd.DataFrame(rows).sort_values("workflow")

def exp2():
    cases = {c["case_id"]: c for c in json.loads((DATA / "experiment2_cases.json").read_text())}
    nurse = pd.read_csv(DATA / "experiment2_nurse_comparator_deidentified.csv").set_index("case_id")
    runs = pd.read_csv(RESULTS / "experiment2_run_results_60.csv")
    valid = runs[runs["final_valid"].astype(str).str.lower().eq("true")].copy()

    def nurse_resulting_sound(cid):
        cmd = nurse.loc[cid, "sound_recommendation"]
        return cases[cid]["room"]["sound"] if cmd == "NO_CHANGE" else cmd

    valid["nurse_brightness"] = [nurse.loc[cid, "brightness_recommendation"] for cid in valid.case_id]
    valid["nurse_tone"] = [nurse.loc[cid, "tone_recommendation"] for cid in valid.case_id]
    valid["nurse_sound_command"] = [nurse.loc[cid, "sound_recommendation"] for cid in valid.case_id]
    valid["nurse_resulting_sound"] = [nurse_resulting_sound(cid) for cid in valid.case_id]
    valid["nurse_clinical_review"] = [str(nurse.loc[cid, "clinical_assessment_needed"]).upper() for cid in valid.case_id]

    bright = valid.lighting_action.eq(valid.nurse_brightness)
    tone = valid.light_tone.eq(valid.nurse_tone)
    sound = valid.sound_option.eq(valid.nurse_sound_command)
    result_sound = valid.resulting_sound_state.eq(valid.nurse_resulting_sound)
    clinical = valid.clinical_review_recommended.eq(valid.nurse_clinical_review)

    return pd.DataFrame([{
        "valid_n": len(valid),
        "brightness_agreement_pct": pct(bright.sum(), len(valid)),
        "tone_agreement_pct": pct(tone.sum(), len(valid)),
        "strict_sound_agreement_pct": pct(sound.sum(), len(valid)),
        "resulting_sound_agreement_pct": pct(result_sound.sum(), len(valid)),
        "clinical_review_agreement_pct": pct(clinical.sum(), len(valid)),
        "exact_command_triplet_pct": pct((bright & tone & sound).sum(), len(valid)),
        "exact_resulting_state_triplet_pct": pct((bright & tone & result_sound).sum(), len(valid)),
    }])

if __name__ == "__main__":
    print("Experiment 1 — valid-run nurse alignment")
    print(exp1().to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    print("\nExperiment 2 — valid-run nurse alignment")
    print(exp2().to_string(index=False, float_format=lambda x: f"{x:.1f}"))