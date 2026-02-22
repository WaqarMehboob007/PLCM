from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.tables import (Order)
from app.schemas import schemas

router = APIRouter()

# ===================== ORDER ENDPOINTS =====================
@router.post("/orders/", response_model=schemas.OrderRead, tags=["orders"])
def create_order(order: schemas.OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.dict())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/orders/", response_model=List[schemas.OrderRead], tags=["orders"])
def list_orders(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(Order).offset(skip).limit(limit)).all()

@router.get("/orders/{order_id}/", response_model=schemas.OrderRead, tags=["orders"])
def get_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/", response_model=schemas.OrderRead, tags=["orders"])
def update_order(order_id: int, order: schemas.OrderUpdate, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for k, v in order.dict(exclude_unset=True).items():
        setattr(db_order, k, v)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.delete("/orders/{order_id}/", tags=["orders"])
def delete_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return {"ok": True}

@router.get("/orders/{order_id}/projects/", response_model=List[schemas.ProjectRead], tags=["orders"])
def list_order_projects(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.projects
