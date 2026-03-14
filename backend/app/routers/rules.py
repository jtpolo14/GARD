import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleResponse, RuleUpdate

router = APIRouter(prefix="/rules", tags=["rules"])


def _rule_to_response(rule: Rule) -> dict:
    data = {
        "id": rule.id,
        "code": rule.code,
        "name": rule.name,
        "description": rule.description,
        "process_id": rule.process_id,
        "logic": json.loads(rule.logic),
        "action": rule.action,
        "priority": rule.priority,
        "status": rule.status,
        "created_at": rule.created_at,
        "updated_at": rule.updated_at,
    }
    return data


@router.get("", response_model=list[RuleResponse])
def list_rules(db: Session = Depends(get_db)):
    rules = db.query(Rule).all()
    return [_rule_to_response(r) for r in rules]


@router.post("", response_model=RuleResponse, status_code=201)
def create_rule(rule_in: RuleCreate, db: Session = Depends(get_db)):
    rule = Rule(
        **{**rule_in.model_dump(exclude={"logic"}), "logic": json.dumps(rule_in.logic)}
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return _rule_to_response(rule)


@router.get("/{rule_id}", response_model=RuleResponse)
def get_rule(rule_id: str, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return _rule_to_response(rule)


@router.put("/{rule_id}", response_model=RuleResponse)
def update_rule(rule_id: str, rule_in: RuleUpdate, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    update_data = rule_in.model_dump(exclude_unset=True)
    if "logic" in update_data:
        update_data["logic"] = json.dumps(update_data["logic"])
    for field, value in update_data.items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return _rule_to_response(rule)


@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: str, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
