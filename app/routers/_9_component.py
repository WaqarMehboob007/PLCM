from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.tables import (Component)
from app.schemas import schemas

router = APIRouter()

# ===================== COMPONENT ENDPOINTS =====================
@router.post("/components/", response_model=schemas.ComponentRead, tags=["components"])
def create_component(component: schemas.ComponentCreate, session: Session = Depends(get_session)):
    db_component = Component(**component.dict())
    session.add(db_component)
    session.commit()
    session.refresh(db_component)
    return db_component

@router.get("/components/", response_model=List[schemas.ComponentRead], tags=["components"])
def list_components(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(Component).offset(skip).limit(limit)).all()

@router.get("/components/{component_id}/", response_model=schemas.ComponentRead, tags=["components"])
def get_component(component_id: int, session: Session = Depends(get_session)):
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component

@router.put("/components/{component_id}/", response_model=schemas.ComponentRead, tags=["components"])
def update_component(component_id: int, component: schemas.ComponentUpdate, session: Session = Depends(get_session)):
    db_component = session.get(Component, component_id)
    if not db_component:
        raise HTTPException(status_code=404, detail="Component not found")
    for k, v in component.dict(exclude_unset=True).items():
        setattr(db_component, k, v)
    session.add(db_component)
    session.commit()
    session.refresh(db_component)
    return db_component

@router.delete("/components/{component_id}/", tags=["components"])
def delete_component(component_id: int, session: Session = Depends(get_session)):
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    session.delete(component)
    session.commit()
    return {"ok": True}

@router.get("/components/{component_id}/inventory/", response_model=List[schemas.InventoryRead], tags=["components"])
def list_component_inventory(component_id: int, session: Session = Depends(get_session)):
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component.inventory_items
