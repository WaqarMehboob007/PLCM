from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.tables import (Module)
from app.schemas import schemas

router = APIRouter()

# ===================== MODULE ENDPOINTS =====================
@router.post("/modules/", response_model=schemas.ModuleRead, tags=["modules"])
def create_module(module: schemas.ModuleCreate, session: Session = Depends(get_session)):
    db_module = Module(**module.dict())
    session.add(db_module)
    session.commit()
    session.refresh(db_module)
    return db_module

@router.get("/modules/", response_model=List[schemas.ModuleRead], tags=["modules"])
def list_modules(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(Module).offset(skip).limit(limit)).all()

@router.get("/modules/{module_id}/", response_model=schemas.ModuleRead, tags=["modules"])
def get_module(module_id: int, session: Session = Depends(get_session)):
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@router.put("/modules/{module_id}/", response_model=schemas.ModuleRead, tags=["modules"])
def update_module(module_id: int, module: schemas.ModuleUpdate, session: Session = Depends(get_session)):
    db_module = session.get(Module, module_id)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    for k, v in module.dict(exclude_unset=True).items():
        setattr(db_module, k, v)
    session.add(db_module)
    session.commit()
    session.refresh(db_module)
    return db_module

@router.delete("/modules/{module_id}/", tags=["modules"])
def delete_module(module_id: int, session: Session = Depends(get_session)):
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    session.delete(module)
    session.commit()
    return {"ok": True}

@router.get("/modules/{module_id}/units/", response_model=List[schemas.UnitRead], tags=["modules"])
def list_module_units(module_id: int, session: Session = Depends(get_session)):
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.units
