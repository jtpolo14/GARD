import json
from typing import Any

from app.services.json_logic import json_logic as jsonLogic
from sqlalchemy.orm import Session

from app.models.process import Process
from app.models.rule import Rule


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

        rule_info = {"code": rule.code, "name": rule.name, "action": rule.action}
        rules_evaluated.append(rule_info)

        if result:
            rules_triggered.append(rule_info)

    decision = rules_triggered[0]["action"] if rules_triggered else "no_action"
    return rules_evaluated, rules_triggered, decision
