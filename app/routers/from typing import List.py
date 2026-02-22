from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import engine
from app.models.tables import (
    User, Customer, Order, Project, System, Subsystem, Module, Unit,
    Component, Inventory, Entity, EntityStatusHistory, MaintenanceLog, Status
)
from app.schemas import schemas

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

# ---- User Endpoints ----
@router.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[schemas.UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/users/{user_id}/", response_model=schemas.UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/{user_id}/projects/", response_model=List[schemas.ProjectRead])
def list_user_projects(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.projects

# ---- Customer Endpoints ----
@router.post("/customers/", response_model=schemas.CustomerRead)
def create_customer(customer: schemas.CustomerCreate, session: Session = Depends(get_session)):
    db_customer = Customer(**customer.dict())
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

@router.get("/customers/", response_model=List[schemas.CustomerRead])
def list_customers(session: Session = Depends(get_session)):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}/orders/", response_model=List[schemas.OrderRead])
def list_customer_orders(customer_id: int, session: Session = Depends(get_session)):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer.orders

# ---- Order Endpoints ----
@router.post("/orders/", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.dict())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/orders/", response_model=List[schemas.OrderRead])
def list_orders(session: Session = Depends(get_session)):
    return session.exec(select(Order)).all()

@router.get("/orders/{order_id}/projects/", response_model=List[schemas.ProjectRead])
def list_order_projects(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.projects

# ---- Project Endpoints ----
@router.post("/projects/", response_model=schemas.ProjectRead)
def create_project(project: schemas.ProjectCreate, session: Session = Depends(get_session)):
    db_project = Project(**project.dict())
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("/projects/", response_model=List[schemas.ProjectRead])
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()

@router.get("/projects/{project_id}/systems/", response_model=List[schemas.SystemRead])
def list_project_systems(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.systems

# ---- System Endpoints ----
@router.post("/systems/", response_model=schemas.SystemRead)
def create_system(system: schemas.SystemCreate, session: Session = Depends(get_session)):
    db_system = System(**system.dict())
    session.add(db_system)
    session.commit()
    session.refresh(db_system)
    return db_system

@router.get("/systems/{system_id}/subsystems/", response_model=List[schemas.SubsystemRead])
def list_system_subsystems(system_id: int, session: Session = Depends(get_session)):
    system = session.get(System, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system.subsystems

# ---- Subsystem, Module, Unit, Component, Inventory ----
# Repeat similar patterns for Subsystem, Module, Unit, Component, and Inventory.

# ---- Entity Endpoints ----
@router.get("/entities/{entity_id}/status-history/", response_model=List[schemas.EntityStatusHistoryRead])
def list_entity_status_history(entity_id: int, session: Session = Depends(get_session)):
    entity = session.get(Entity, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity.status_history

@router.get("/entities/{entity_id}/maintenance-logs/", response_model=List[schemas.MaintenanceLogRead])
def list_entity_maintenance_logs(entity_id: int, session: Session = Depends(get_session)):
    entity = session.get(Entity, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity.maintenance_logs