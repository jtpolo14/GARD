import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.decision_log import DecisionLog

router = APIRouter(prefix="/decision-logs", tags=["decision-logs"])


def _log_to_response(log: DecisionLog) -> dict:
    return {
        "id": log.id,
        "agent_id": log.agent_id,
        "process_code": log.process_code,
        "input_data": json.loads(log.input_data),
        "rules_evaluated": json.loads(log.rules_evaluated),
        "rules_triggered": json.loads(log.rules_triggered),
        "outcome": json.loads(log.outcome),
        "decision": log.decision,
        "created_at": log.created_at,
    }


@router.get("")
def list_decision_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(DecisionLog)
        .order_by(DecisionLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_log_to_response(log) for log in logs]


@router.get("/{log_id}")
def get_decision_log(log_id: str, db: Session = Depends(get_db)):
    log = db.query(DecisionLog).filter(DecisionLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Decision log not found")
    return _log_to_response(log)
