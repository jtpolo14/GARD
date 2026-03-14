from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.process import Process
from app.schemas.process import ProcessCreate, ProcessResponse, ProcessUpdate

router = APIRouter(prefix="/processes", tags=["processes"])


@router.get("", response_model=list[ProcessResponse])
def list_processes(db: Session = Depends(get_db)):
    return db.query(Process).all()


@router.post("", response_model=ProcessResponse, status_code=201)
def create_process(process_in: ProcessCreate, db: Session = Depends(get_db)):
    process = Process(**process_in.model_dump())
    db.add(process)
    db.commit()
    db.refresh(process)
    return process


@router.get("/{process_id}", response_model=ProcessResponse)
def get_process(process_id: str, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process


@router.put("/{process_id}", response_model=ProcessResponse)
def update_process(
    process_id: str, process_in: ProcessUpdate, db: Session = Depends(get_db)
):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    for field, value in process_in.model_dump(exclude_unset=True).items():
        setattr(process, field, value)
    db.commit()
    db.refresh(process)
    return process
