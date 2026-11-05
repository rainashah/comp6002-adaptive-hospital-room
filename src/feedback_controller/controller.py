"""Deterministic post-recommendation controller for the AHR prototype.

This module contains no model calls and no clinical decision logic. It accepts a
previously validated room recommendation, preserves explicit staff authority,
and handles scripted software-test reassessment states.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ControllerState(str, Enum):
    AWAITING_STAFF_DECISION = "AWAITING_STAFF_DECISION"
    ACTIVE = "ACTIVE"
    MONITORING = "MONITORING"
    STAFF_REVIEW_REQUIRED = "STAFF_REVIEW_REQUIRED"
    CLOSED = "CLOSED"


class ControllerAction(str, Enum):
    NONE = "NONE"
    WITHHOLD = "WITHHOLD"
    APPLY_VALIDATED_RECOMMENDATION = "APPLY_VALIDATED_RECOMMENDATION"
    NO_AHR_ENVIRONMENTAL_CHANGE = "NO_AHR_ENVIRONMENTAL_CHANGE"
    APPLY_STAFF_OVERRIDE = "APPLY_STAFF_OVERRIDE"
    MAINTAIN_AND_MONITOR = "MAINTAIN_AND_MONITOR"
    CONTINUE_MONITORING = "CONTINUE_MONITORING"
    REQUEST_STAFF_ASSISTANCE = "REQUEST_STAFF_ASSISTANCE"


class StaffDecision(str, Enum):
    ACCEPT = "ACCEPT"
    DECLINE = "DECLINE"
    OVERRIDE = "OVERRIDE"


class FollowUpState(str, Enum):
    IMPROVED = "IMPROVED"
    NO_RESPONSE = "NO_RESPONSE"
    REPEATED_NO_RESPONSE = "REPEATED_NO_RESPONSE"
    WORSENED = "WORSENED"


@dataclass(frozen=True)
class RoomState:
    brightness_pct: float
    tone: str
    sound: str
    volume_pct: float
    configured_duration_minutes: float

    @classmethod
    def from_mapping(cls, value: Dict[str, Any]) -> "RoomState":
        return cls(
            brightness_pct=float(value["brightness_pct"]),
            tone=str(value["tone"]),
            sound=str(value["sound"]),
            volume_pct=float(value["volume_pct"]),
            configured_duration_minutes=float(value["configured_duration_minutes"]),
        )


@dataclass(frozen=True)
class ValidatedRecommendation:
    case_id: str
    valid: bool
    resulting_room_state: RoomState
    lighting_action: str
    sound_action: str
    clinical_review_recommended: str


@dataclass
class ControllerEvent:
    case_id: str
    pathway: str
    step: int
    elapsed_minutes: int
    event: str
    controller_state: str
    controller_action: str
    no_response_count: int
    active_room_state: Dict[str, Any]
    clinical_review_recommended: str
    note: str


class FeedbackController:
    """Deterministic state machine used after recommendation validation."""

    def __init__(
        self,
        recommendation: ValidatedRecommendation,
        current_room_state: RoomState,
        pathway: str = "UNSPECIFIED",
        reassessment_minutes: int = 15,
    ) -> None:
        self.recommendation = recommendation
        self.current_room_state = current_room_state
        self.active_room_state = current_room_state
        self.pathway = pathway
        self.reassessment_minutes = int(reassessment_minutes)
        self.elapsed_minutes = 0
        self.no_response_count = 0
        self.step = 0
        self.events: List[ControllerEvent] = []

        if recommendation.valid:
            self.state = ControllerState.AWAITING_STAFF_DECISION
            self._record(
                "VALID_RECOMMENDATION_RECEIVED",
                ControllerAction.NONE,
                "Validated recommendation available for staff decision.",
            )
        else:
            self.state = ControllerState.STAFF_REVIEW_REQUIRED
            self._record(
                "INVALID_RECOMMENDATION_WITHHELD",
                ControllerAction.WITHHOLD,
                "Invalid output withheld; no room change applied.",
            )

    def _record(self, event: str, action: ControllerAction, note: str) -> None:
        self.step += 1
        self.events.append(
            ControllerEvent(
                case_id=self.recommendation.case_id,
                pathway=self.pathway,
                step=self.step,
                elapsed_minutes=self.elapsed_minutes,
                event=event,
                controller_state=self.state.value,
                controller_action=action.value,
                no_response_count=self.no_response_count,
                active_room_state=asdict(self.active_room_state),
                clinical_review_recommended=self.recommendation.clinical_review_recommended,
                note=note,
            )
        )

    def decide(
        self,
        decision: StaffDecision,
        override_state: Optional[RoomState] = None,
    ) -> None:
        if self.state != ControllerState.AWAITING_STAFF_DECISION:
            raise RuntimeError("A staff decision is only valid while awaiting staff decision.")

        if decision == StaffDecision.ACCEPT:
            self.active_room_state = self.recommendation.resulting_room_state
            self.state = ControllerState.ACTIVE
            self._record(
                "STAFF_ACCEPTED",
                ControllerAction.APPLY_VALIDATED_RECOMMENDATION,
                "Validated recommendation applied; scripted reassessment scheduled.",
            )
        elif decision == StaffDecision.DECLINE:
            self.active_room_state = self.current_room_state
            self.state = ControllerState.CLOSED
            self._record(
                "STAFF_DECLINED",
                ControllerAction.NO_AHR_ENVIRONMENTAL_CHANGE,
                "Current room state retained and controller cycle closed.",
            )
        elif decision == StaffDecision.OVERRIDE:
            if override_state is None:
                raise ValueError("OVERRIDE requires an explicit staff-selected room state.")
            self.active_room_state = override_state
            self.state = ControllerState.ACTIVE
            self._record(
                "STAFF_OVERRIDDEN",
                ControllerAction.APPLY_STAFF_OVERRIDE,
                "Staff-selected room state applied and remains authoritative.",
            )
        else:
            raise ValueError(f"Unsupported staff decision: {decision}")

    def reassess(self, follow_up: FollowUpState) -> None:
        if self.state not in {ControllerState.ACTIVE, ControllerState.MONITORING}:
            raise RuntimeError("Reassessment requires an active or monitoring controller state.")

        self.elapsed_minutes += self.reassessment_minutes

        if follow_up == FollowUpState.IMPROVED:
            self.state = ControllerState.MONITORING
            self._record(
                "REASSESS_IMPROVED",
                ControllerAction.MAINTAIN_AND_MONITOR,
                "Active room state maintained; no additional environmental change.",
            )
        elif follow_up == FollowUpState.NO_RESPONSE:
            self.no_response_count += 1
            if self.no_response_count >= 2:
                self.state = ControllerState.STAFF_REVIEW_REQUIRED
                self._record(
                    "REASSESS_REPEATED_NO_RESPONSE",
                    ControllerAction.REQUEST_STAFF_ASSISTANCE,
                    "Repeated no-response state; escalate rather than cycling settings.",
                )
            else:
                self.state = ControllerState.MONITORING
                self._record(
                    "REASSESS_NO_RESPONSE",
                    ControllerAction.CONTINUE_MONITORING,
                    "First no-response state; retain room state and continue monitoring.",
                )
        elif follow_up == FollowUpState.REPEATED_NO_RESPONSE:
            self.no_response_count = max(2, self.no_response_count + 1)
            self.state = ControllerState.STAFF_REVIEW_REQUIRED
            self._record(
                "REASSESS_REPEATED_NO_RESPONSE",
                ControllerAction.REQUEST_STAFF_ASSISTANCE,
                "Repeated no-response state; escalate rather than cycling settings.",
            )
        elif follow_up == FollowUpState.WORSENED:
            self.state = ControllerState.STAFF_REVIEW_REQUIRED
            self._record(
                "REASSESS_WORSENED",
                ControllerAction.REQUEST_STAFF_ASSISTANCE,
                "Worsening scripted state; request staff assistance.",
            )
        else:
            raise ValueError(f"Unsupported follow-up state: {follow_up}")

    def audit_log(self) -> List[Dict[str, Any]]:
        return [asdict(event) for event in self.events]


def recommendation_from_row(row: Dict[str, Any]) -> ValidatedRecommendation:
    """Build a validated recommendation from the public representative-runs CSV."""
    return ValidatedRecommendation(
        case_id=str(row["case_id"]),
        valid=str(row.get("historical_final_valid", "True")).lower() == "true",
        resulting_room_state=RoomState(
            brightness_pct=float(row["resulting_brightness_pct"]),
            tone=str(row["resulting_tone"]),
            sound=str(row["resulting_sound"]),
            volume_pct=float(row["resulting_volume_pct"]),
            configured_duration_minutes=float(row["resulting_duration_minutes"]),
        ),
        lighting_action=str(row["lighting_action"]),
        sound_action=str(row["sound_action"]),
        clinical_review_recommended=str(row["clinical_review_recommended"]),
    )


def run_pathway(
    recommendation: ValidatedRecommendation,
    current_room_state: RoomState,
    pathway: str,
) -> FeedbackController:
    """Execute one of the six scripted integration pathways."""
    controller = FeedbackController(recommendation, current_room_state, pathway=pathway)

    if pathway == "DECLINE":
        controller.decide(StaffDecision.DECLINE)
    elif pathway == "OVERRIDE_RETAIN_CURRENT_IMPROVED":
        controller.decide(StaffDecision.OVERRIDE, override_state=current_room_state)
        controller.reassess(FollowUpState.IMPROVED)
    else:
        controller.decide(StaffDecision.ACCEPT)
        if pathway == "ACCEPT_IMPROVED":
            controller.reassess(FollowUpState.IMPROVED)
        elif pathway == "ACCEPT_FIRST_NO_RESPONSE":
            controller.reassess(FollowUpState.NO_RESPONSE)
        elif pathway == "ACCEPT_REPEATED_NO_RESPONSE":
            controller.reassess(FollowUpState.NO_RESPONSE)
            controller.reassess(FollowUpState.NO_RESPONSE)
        elif pathway == "ACCEPT_WORSENED":
            controller.reassess(FollowUpState.WORSENED)
        else:
            raise ValueError(f"Unknown pathway: {pathway}")
    return controller
