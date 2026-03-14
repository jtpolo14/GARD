import json
from typing import Any

from app.services.json_logic import json_logic as jsonLogic
from sqlalchemy.orm import Session

from app.models.process import Process
from app.models.rule import Rule


def _get_matched_reasons(
    logic: dict, data: dict[str, Any], condition_reasons: list[str]
) -> list[str]:
    """Evaluate each condition individually and return reasons for those that matched."""
    if not condition_reasons:
        return []

    # Extract individual conditions from and/or combinators
    conditions: list[dict] = []
    if "and" in logic:
        conditions = logic["and"]
    elif "or" in logic:
        conditions = logic["or"]
    else:
        # Single condition
        conditions = [logic]

    matched = []
    for i, condition in enumerate(conditions):
        if i < len(condition_reasons) and condition_reasons[i]:
            if jsonLogic(condition, data):
                matched.append(condition_reasons[i])
    return matched


def evaluate_rules(
    db: Session, process_name: str | None, data: dict[str, Any]
) -> tuple[list[dict], list[dict], str]:
    """Evaluate active rules against input data.

    Returns (rules_evaluated, rules_triggered, decision).
    """
    query = db.query(Rule).filter(Rule.status == "active")

    if process_name:
        process = db.query(Process).filter(Process.name == process_name).first()
        if process:
            # Get rules for this process + global rules (no process)
            query = query.filter(
                (Rule.process_id == process.id) | (Rule.process_id.is_(None))
            )
        else:
            # Only global rules
            query = query.filter(Rule.process_id.is_(None))
    else:
        query = query.filter(Rule.process_id.is_(None))

    rules = query.order_by(Rule.priority.asc()).all()

    rules_evaluated = []
    rules_triggered = []

    for rule in rules:
        logic = json.loads(rule.logic)
        result = jsonLogic(logic, data)
        condition_reasons = json.loads(rule.condition_reasons) if rule.condition_reasons else []

        # Determine which specific conditions matched
        matched_reasons = _get_matched_reasons(logic, data, condition_reasons)

        rule_info = {
            "code": rule.code,
            "name": rule.name,
            "description": rule.description,
            "action": rule.action,
            "matched_reasons": matched_reasons,
        }
        rules_evaluated.append(rule_info)

        if result:
            rules_triggered.append(rule_info)

    decision = rules_triggered[0]["action"] if rules_triggered else "no_action"
    return rules_evaluated, rules_triggered, decision
