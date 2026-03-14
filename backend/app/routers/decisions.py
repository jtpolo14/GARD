import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.agent import Agent
from app.models.decision_log import DecisionLog
from app.schemas.decision import DecisionRequest, DecisionResponse
from app.services.rule_engine import evaluate_rules

router = APIRouter(tags=["decisions"])


@router.post("/evaluate-decision", response_model=DecisionResponse)
def evaluate_decision(req: DecisionRequest, db: Session = Depends(get_db)):
    # 1. Look up agent
    agent = db.query(Agent).filter(Agent.name == req.agent).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{req.agent}' not found")

    # 2-4. Evaluate rules
    rules_evaluated, rules_triggered, decision = evaluate_rules(
        db, req.process, req.data
    )

    # 5. Build outcome
    actions = [r["action"] for r in rules_triggered]
    triggered_codes = [r["code"] for r in rules_triggered]

    outcome = {
        "decision": decision,
        "rules_triggered": triggered_codes,
        "actions": actions,
    }

    # 6. Log
    log = DecisionLog(
        agent_id=agent.id,
        process_code=req.process,
        input_data=json.dumps(req.data),
        rules_evaluated=json.dumps(rules_evaluated),
        rules_triggered=json.dumps(rules_triggered),
        outcome=json.dumps(outcome),
        decision=decision,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # 7. Return
    return DecisionResponse(
        decision_id=log.id,
        decision=decision,
        rules_triggered=triggered_codes,
        actions=actions,
        timestamp=log.created_at,
    )
