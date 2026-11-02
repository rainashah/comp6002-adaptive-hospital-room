"""Replay the six deterministic controller pathways for all 12 Experiment 2 cases."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

from controller import RoomState, recommendation_from_row, run_pathway

PATHWAYS = [
    "ACCEPT_IMPROVED",
    "ACCEPT_FIRST_NO_RESPONSE",
    "ACCEPT_REPEATED_NO_RESPONSE",
    "ACCEPT_WORSENED",
    "DECLINE",
    "OVERRIDE_RETAIN_CURRENT_IMPROVED",
]

EXPECTED_FINAL_STATE = {
    "ACCEPT_IMPROVED": "MONITORING",
    "ACCEPT_FIRST_NO_RESPONSE": "MONITORING",
    "ACCEPT_REPEATED_NO_RESPONSE": "STAFF_REVIEW_REQUIRED",
    "ACCEPT_WORSENED": "STAFF_REVIEW_REQUIRED",
    "DECLINE": "CLOSED",
    "OVERRIDE_RETAIN_CURRENT_IMPROVED": "MONITORING",
}


def current_state_from_row(row: Dict[str, object]) -> RoomState:
    """Use a deterministic room-state proxy for public transition replay.

    The public pass/fail assertion concerns controller transitions, not physical
    room-response modelling. The archived Drive run also verified the selected
    rows against the original final-valid JSON outputs.
    """
    return RoomState(
        brightness_pct=float(row["resulting_brightness_pct"]),
        tone=str(row["resulting_tone"]),
        sound=str(row["resulting_sound"]),
        volume_pct=float(row["resulting_volume_pct"]),
        configured_duration_minutes=float(row["resulting_duration_minutes"]),
    )


def replay(representative_csv: Path) -> pd.DataFrame:
    representatives = pd.read_csv(representative_csv)
    rows: List[Dict[str, object]] = []

    for record in representatives.to_dict(orient="records"):
        recommendation = recommendation_from_row(record)
        current = current_state_from_row(record)
        for pathway in PATHWAYS:
            controller = run_pathway(recommendation, current, pathway)
            final_state = controller.state.value
            passed = final_state == EXPECTED_FINAL_STATE[pathway]
            rows.append({
                "case_id": recommendation.case_id,
                "source_repeat": int(record["source_repeat"]),
                "pathway": pathway,
                "result": "PASS" if passed else "FAIL",
                "final_controller_state": final_state,
                "elapsed_simulated_minutes": controller.elapsed_minutes,
                "no_response_count": controller.no_response_count,
                "clinical_review_recommended": recommendation.clinical_review_recommended,
                "lighting_action": recommendation.lighting_action,
                "light_tone": recommendation.resulting_room_state.tone,
                "sound_action": recommendation.sound_action,
                "resulting_brightness_pct": recommendation.resulting_room_state.brightness_pct,
                "resulting_sound": recommendation.resulting_room_state.sound,
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    results = replay(folder / "experiment2_feedback_controller_representative_runs.csv")
    print(results.groupby("pathway")["result"].value_counts().unstack(fill_value=0))
    print(f"Passed: {(results['result'] == 'PASS').sum()}/{len(results)}")
    if not (results["result"] == "PASS").all():
        raise SystemExit(1)
