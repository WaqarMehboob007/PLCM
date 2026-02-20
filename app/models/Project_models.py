from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# Base class for Project models
class ProjectBase(SQLModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    owner_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Core tables for build/maintenance hierarchy and logging
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status_changes: List["EntityStatusHistory"] = Relationship(back_populates="changed_by_user")
    maintenances: List["MaintenanceLog"] = Relationship(back_populates="performed_by_user")


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orders: List["Order"] = Relationship(back_populates="customer")


class Status(StatusBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer: Optional[Customer] = Relationship(back_populates="orders")
    projects: List["Project"] = Relationship(back_populates="order")


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    order: Optional[Order] = Relationship(back_populates="projects")
    systems: List["System"] = Relationship(back_populates="project")


class System(SystemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project: Optional[Project] = Relationship(back_populates="systems")
    subsystems: List["Subsystem"] = Relationship(back_populates="system")


class Subsystem(SubsystemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    system: Optional[System] = Relationship(back_populates="subsystems")
    modules: List["Module"] = Relationship(back_populates="subsystem")


class Module(ModuleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subsystem: Optional[Subsystem] = Relationship(back_populates="modules")
    units: List["Unit"] = Relationship(back_populates="module")


class Unit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="module.id")
    name: str
    description: Optional[str] = None
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    module: Optional[Module] = Relationship(back_populates="units")
    components: List["Component"] = Relationship(back_populates="unit")


class Component(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    unit_id: int = Field(foreign_key="unit.id")
    name: str
    sku: Optional[str] = None
    description: Optional[str] = None
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    unit: Optional[Unit] = Relationship(back_populates="components")
    inventory_items: List["Inventory"] = Relationship(back_populates="component")


class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    component_id: int = Field(foreign_key="component.id")
    quantity: int = 0
    location: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    component: Optional[Component] = Relationship(back_populates="inventory_items")


class Entity(SQLModel, table=True):
    """Generic entity reference for status/history/maintenance logging.
    Use `entity_type` to indicate which table the `entity_pk` refers to
    (e.g. 'project','system','subsystem','unit','component').
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_type: str
    entity_pk: int
    display_name: Optional[str] = None
    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status_history: List["EntityStatusHistory"] = Relationship(back_populates="entity")
    maintenance_logs: List["MaintenanceLog"] = Relationship(back_populates="entity")


class EntityStatusHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_id: int = Field(foreign_key="entity.id")
    status_id: int = Field(foreign_key="status.id")
    changed_by: Optional[int] = Field(default=None, foreign_key="user.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    entity: Optional[Entity] = Relationship(back_populates="status_history")
    changed_by_user: Optional[User] = Relationship(back_populates="status_changes")


class MaintenanceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_id: int = Field(foreign_key="entity.id")
    performed_by: Optional[int] = Field(default=None, foreign_key="user.id")
    notes: Optional[str] = None
    performed_at: datetime = Field(default_factory=datetime.utcnow)
    next_due: Optional[datetime] = None
    entity: Optional[Entity] = Relationship(back_populates="maintenance_logs")
    performed_by_user: Optional[User] = Relationship(back_populates="maintenances")
