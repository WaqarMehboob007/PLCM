from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


# Base models for all entities, defining common fields and structure

# All Base models are immutable and include created_at timestamp. Updateable fields are defined in separate Common models.
# Common models are used for create/update operations and do not include created_at or primary key fields. They can be extended with additional fields as needed.
# Base models are used for database tables and include primary key fields. They can also include relationships if needed, but should not include updateable fields directly.

class UserCommon(SQLModel):    
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True

class UserBase(UserCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCommon(SQLModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    owner_id: int

class ProjectBase(ProjectCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerCommon(SQLModel):
    name: str
    contact_info: Optional[str] = None

class CustomerBase(CustomerCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StatusCommon(SQLModel):
    name: str
    description: Optional[str] = None
    
class StatusBase(StatusCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCommon(SQLModel):
    customer_id: int
    order_number: Optional[str] = None
    status_id: Optional[int] = None

class OrderBase(OrderCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SystemCommon(SQLModel):
    name: str
    description: Optional[str] = None

class SystemBase(SystemCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SubsystemCommon(SQLModel):
    name: str
    description: Optional[str] = None

class SubsystemBase(SubsystemCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ModuleCommon(SQLModel):
    name: str
    description: Optional[str] = None

class ModuleBase(ModuleCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UnitCommon(SQLModel):
    name: str
    description: Optional[str] = None

class UnitBase(UnitCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ComponentCommon(SQLModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None


class ComponentBase(ComponentCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EntityCommon(SQLModel):
    name: str
    display_name: Optional[str] = None
    entity_type: str
    entity_pk: int

class EntityBase(EntityCommon):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EntityStatusHistoryCommon(SQLModel):
    notes: Optional[str] = None

class EntityStatusHistoryBase(EntityStatusHistoryCommon):
    changed_at: datetime = Field(default_factory=datetime.utcnow)

class MaintenanceLogCommon(SQLModel):
    entity_id: int
    notes: Optional[str] = None
    next_due: Optional[datetime] = None
    
class MaintenanceLogBase(MaintenanceLogCommon):
    performed_at: datetime = Field(default_factory=datetime.utcnow)

class InventoryCommon(SQLModel):
    component_id: int
    quantity: int = 0
    location: Optional[str] = None

class InventoryBase(InventoryCommon):
    updated_at: datetime = Field(default_factory=datetime.utcnow)   