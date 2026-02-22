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

# Generic pattern implemented per resource (create, list, get, update, delete)
def make_crud(model, create_schema, read_schema, update_schema, prefix: str):
    r = APIRouter(prefix=prefix, tags=[model.__name__.lower() + "s"])

    @r.post("/", response_model=read_schema)
    def create(item: create_schema, session: Session = Depends(get_session)):
        db_obj = model(**item.dict(exclude_unset=True))
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @r.get("/", response_model=List[read_schema])
    def list_items(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
        stmt = select(model).offset(skip).limit(limit)
        return session.exec(stmt).all()

    @r.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: int, session: Session = Depends(get_session)):
        obj = session.get(model, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

    @r.put("/{item_id}", response_model=read_schema)
    def update_item(item_id: int, item: update_schema, session: Session = Depends(get_session)):
        db_obj = session.get(model, item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Not found")
        for k, v in item.dict(exclude_unset=True).items():
            setattr(db_obj, k, v)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @r.delete("/{item_id}", response_model=dict)
    def delete_item(item_id: int, session: Session = Depends(get_session)):
        db_obj = session.get(model, item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Not found")
        session.delete(db_obj)
        session.commit()
        return {"ok": True}

    return r

# Register routers for core models
router.include_router(make_crud(User, schemas.UserCreate, schemas.UserRead, schemas.UserUpdate, "/users"))
router.include_router(make_crud(Customer, schemas.CustomerCreate, schemas.CustomerRead, schemas.CustomerUpdate, "/customers"))
router.include_router(make_crud(Status, schemas.StatusCreate, schemas.StatusRead, schemas.StatusUpdate, "/statuses"))
router.include_router(make_crud(Order, schemas.OrderCreate, schemas.OrderRead, schemas.OrderUpdate, "/orders"))
router.include_router(make_crud(Project, schemas.ProjectCreate, schemas.ProjectRead, schemas.ProjectUpdate, "/projects"))
router.include_router(make_crud(System, schemas.SystemCreate, schemas.SystemRead, schemas.SystemUpdate, "/systems"))
router.include_router(make_crud(Subsystem, schemas.SubsystemCreate, schemas.SubsystemRead, schemas.SubsystemUpdate, "/subsystems"))
router.include_router(make_crud(Module, schemas.ModuleCreate, schemas.ModuleRead, schemas.ModuleUpdate, "/modules"))
router.include_router(make_crud(Unit, schemas.UnitCreate, schemas.UnitRead, schemas.UnitUpdate, "/units"))
router.include_router(make_crud(Component, schemas.ComponentCreate, schemas.ComponentRead, schemas.ComponentUpdate, "/components"))
router.include_router(make_crud(Inventory, schemas.InventoryCreate, schemas.InventoryRead, schemas.InventoryUpdate, "/inventory"))
router.include_router(make_crud(Entity, schemas.EntityCreate, schemas.EntityRead, schemas.EntityUpdate, "/entities"))
router.include_router(make_crud(EntityStatusHistory, schemas.EntityStatusHistoryCreate, schemas.EntityStatusHistoryRead, schemas.EntityStatusHistoryUpdate, "/entity-status-history"))
router.include_router(make_crud(MaintenanceLog, schemas.MaintenanceLogCreate, schemas.MaintenanceLogRead, schemas.MaintenanceLogUpdate, "/maintenance-logs"))