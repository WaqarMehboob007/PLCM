from fastapi import APIRouter

# Create a main router that will include all sub-routers
router = APIRouter()

# Import and include all routers
from app.routers import (
    _1_users,
    _2_customers,
    _3_orders,
    _4_projects,
    _5_systems,
    _6_subsystem,
    _7_module,
    _8_unit,
    _9_component,
    _10_inventory,
    entity,
    entitystatushistory,
    maintenanceLog,
    status,
)

# Include all routers
router.include_router(_1_users.router, prefix="/users", tags=["users"])
router.include_router(_2_customers.router, prefix="/customers", tags=["customers"])
router.include_router(_3_orders.router, prefix="/orders", tags=["orders"])
router.include_router(_4_projects.router, prefix="/projects", tags=["projects"])
router.include_router(_5_systems.router, prefix="/systems", tags=["systems"])
router.include_router(_6_subsystem.router, prefix="/subsystems", tags=["subsystems"]    )
router.include_router(_7_module.router, prefix="/modules", tags=["modules"])
router.include_router(_8_unit.router, prefix="/units", tags=["units"])
router.include_router(_9_component.router, prefix="/components", tags=["components"])
router.include_router(_10_inventory.router, prefix="/inventory", tags=["inventory"])
router.include_router(entity.router, prefix="/entities", tags=["entities"])
router.include_router(entitystatushistory.router, prefix="/entitystatushistory", tags=["entitystatushistory"])
router.include_router(maintenanceLog.router, prefix="/maintenancelogs", tags=["maintenancelogs"])
router.include_router(status.router, prefix="/statuses", tags=["statuses"])
