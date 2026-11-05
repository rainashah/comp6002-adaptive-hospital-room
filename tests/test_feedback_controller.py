"""Executable deterministic unit tests for the AHR feedback controller."""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Dict, List

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from feedback_controller.controller import (
    ControllerState,
    FeedbackController,
    FollowUpState,
    RoomState,
    StaffDecision,
    ValidatedRecommendation,
)


def fixture(valid: bool = True):
    current = RoomState(65, "NEUTRAL", "NONE_SILENCE", 0, 0)
    recommended = RoomState(55, "WARM", "NATURE_SOUNDS", 20, 15)
    rec = ValidatedRecommendation(
        case_id="UNIT_TEST",
        valid=valid,
        resulting_room_state=recommended,
        lighting_action="DECREASE",
        sound_action="NATURE_SOUNDS",
        clinical_review_recommended="NO",
    )
    return current, recommended, rec


def run_tests() -> pd.DataFrame:
    rows: List[Dict[str, str]] = []

    def record(test_id: str, requirement: str, fn):
        try:
            fn()
            rows.append({"test_id": test_id, "requirement": requirement, "result": "PASS", "detail": ""})
        except Exception as exc:
            rows.append({"test_id": test_id, "requirement": requirement, "result": "FAIL", "detail": repr(exc)})

    current, recommended, rec = fixture()

    record("TC01", "Invalid recommendation is withheld", lambda: (
        lambda c: (_ for _ in ()).throw(AssertionError()) if c.state != ControllerState.STAFF_REVIEW_REQUIRED else None
    )(FeedbackController(fixture(False)[2], current)))

    def tc02():
        c = FeedbackController(rec, current); c.decide(StaffDecision.ACCEPT)
        assert c.active_room_state == recommended and c.state == ControllerState.ACTIVE
    record("TC02", "Staff ACCEPT applies validated recommendation", tc02)

    def tc03():
        c = FeedbackController(rec, current); c.decide(StaffDecision.DECLINE)
        assert c.active_room_state == current and c.state == ControllerState.CLOSED
    record("TC03", "Staff DECLINE leaves room unchanged and closes cycle", tc03)

    def tc04():
        override = RoomState(40, "WARM", "NONE_SILENCE", 0, 0)
        c = FeedbackController(rec, current); c.decide(StaffDecision.OVERRIDE, override)
        assert c.active_room_state == override
    record("TC04", "Staff OVERRIDE applies staff-selected state", tc04)

    def tc05():
        c = FeedbackController(rec, current); c.decide(StaffDecision.ACCEPT); c.reassess(FollowUpState.IMPROVED)
        assert c.state == ControllerState.MONITORING and c.active_room_state == recommended
    record("TC05", "IMPROVED maintains current state and monitors", tc05)

    def tc06():
        c = FeedbackController(rec, current); c.decide(StaffDecision.ACCEPT); c.reassess(FollowUpState.NO_RESPONSE)
        assert c.state == ControllerState.MONITORING and c.no_response_count == 1
    record("TC06", "First NO_RESPONSE retains state and continues monitoring", tc06)

    def tc07():
        c = FeedbackController(rec, current); c.decide(StaffDecision.ACCEPT)
        c.reassess(FollowUpState.NO_RESPONSE); c.reassess(FollowUpState.NO_RESPONSE)
        assert c.state == ControllerState.STAFF_REVIEW_REQUIRED
    record("TC07", "Second NO_RESPONSE requests staff assistance", tc07)

    def tc08():
        c = FeedbackController(rec, current); c.decide(StaffDecision.ACCEPT); c.reassess(FollowUpState.REPEATED_NO_RESPONSE)
        assert c.state == ControllerState.STAFF_REVIEW_REQUIRED
    record("TC08", "Explicit REPEATED_NO_RESPONSE requests staff assistance", tc08)

    def tc09():
        c = FeedbackController(rec, current); c.decide(StaffDecision.ACCEPT); c.reassess(FollowUpState.WORSENED)
        assert c.state == ControllerState.STAFF_REVIEW_REQUIRED
    record("TC09", "WORSENED requests staff assistance", tc09)

    def tc10():
        override = RoomState(40, "WARM", "NONE_SILENCE", 0, 0)
        c = FeedbackController(rec, current); c.decide(StaffDecision.OVERRIDE, override); c.reassess(FollowUpState.IMPROVED)
        assert c.active_room_state == override
    record("TC10", "Staff override remains authoritative during follow-up", tc10)

    def tc11():
        c = FeedbackController(rec, current)
        try: c.reassess(FollowUpState.IMPROVED)
        except RuntimeError: return
        raise AssertionError("Expected RuntimeError")
    record("TC11", "Reassessment is blocked before staff decision", tc11)

    def tc12():
        c = FeedbackController(rec, current)
        try: c.decide(StaffDecision.OVERRIDE)
        except ValueError: return
        raise AssertionError("Expected ValueError")
    record("TC12", "Override requires an explicit staff-selected room state", tc12)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    results = run_tests()
    print(results.to_string(index=False))
    if not (results["result"] == "PASS").all():
        raise SystemExit(1)
