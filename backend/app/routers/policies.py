from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate, PolicyResponse, PolicyUpdate

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=list[PolicyResponse])
def list_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()


@router.post("", response_model=PolicyResponse, status_code=201)
def create_policy(policy_in: PolicyCreate, db: Session = Depends(get_db)):
    policy = Policy(**policy_in.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(policy_id: str, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
