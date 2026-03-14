import json
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.process import Process
from app.models.rule import Rule
from app.schemas.simulation import (
    SimulationRequest,
    SimulationResponse,
    SimulationTestResult,
)
from app.services.json_logic import json_logic as jsonLogic
from app.services.rule_engine import _get_matched_reasons

router = APIRouter(tags=["simulations"])


def _simulate_rules(
    db: Session,
    data: dict[str, Any],
    rule_id: str | None,
    process_name: str | None,
) -> tuple[list[str], str, list[str]]:
    """Evaluate rules against data without logging. Returns (triggered_codes, decision).

    If rule_id is provided, only that rule is tested (regardless of status).
    Otherwise, all active rules for the process are tested.
    """
    if rule_id:
        rules = db.query(Rule).filter(Rule.id == rule_id).all()
    else:
        query = db.query(Rule).filter(Rule.status == "active")
        if process_name:
            process = db.query(Process).filter(Process.name == process_name).first()
            if process:
                query = query.filter(
                    (Rule.process_id == process.id) | (Rule.process_id.is_(None))
                )
            else:
                query = query.filter(Rule.process_id.is_(None))
        else:
            query = query.filter(Rule.process_id.is_(None))
        rules = query.order_by(Rule.priority.asc()).all()

    triggered = []
    reasons: list[str] = []
    for rule in rules:
        logic = json.loads(rule.logic)
        condition_reasons = json.loads(rule.condition_reasons) if rule.condition_reasons else []
        if jsonLogic(logic, data):
            triggered.append({"code": rule.code, "action": rule.action})
            matched = _get_matched_reasons(logic, data, condition_reasons)
            if matched:
                reasons.extend(matched)
            elif rule.description:
                reasons.append(f"{rule.name}: {rule.description}")
            else:
                reasons.append(rule.name)

    decision = triggered[0]["action"] if triggered else "no_action"
    triggered_codes = [t["code"] for t in triggered]
    return triggered_codes, decision, reasons


@router.post("/simulate", response_model=SimulationResponse)
def run_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    results: list[SimulationTestResult] = []

    for tc in req.test_cases:
        triggered_codes, actual_decision, reasons = _simulate_rules(
            db, tc.data, req.rule_id, req.process
        )
        passed = actual_decision == tc.expected_decision
        results.append(
            SimulationTestResult(
                label=tc.label,
                data=tc.data,
                expected_decision=tc.expected_decision,
                actual_decision=actual_decision,
                rules_triggered=triggered_codes,
                reasons=reasons,
                passed=passed,
            )
        )

    passed_count = sum(1 for r in results if r.passed)
    return SimulationResponse(
        total=len(results),
        passed=passed_count,
        failed=len(results) - passed_count,
        results=results,
    )
