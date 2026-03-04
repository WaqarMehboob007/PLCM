"""
Authentication and Authorization Module
Handles JWT token generation, password hashing, and role-based access control
Works entirely offline - no internet required
"""

from datetime import datetime, timedelta, timezone, UTC
from typing import Optional, List
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlmodel import Session, select

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 12 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==================== PASSWORD HANDLING ====================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ==================== JWT TOKEN HANDLING ====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def extract_token_from_header(authorization: str) -> str:
    """Extract JWT token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )
    return authorization.split(" ")[1]


# ==================== USER RETRIEVAL ====================

def get_user_from_token(token: str, session: Session):
    """Get user object from JWT token."""
    from app.models.tables import User
    
    payload = decode_token(token)
    user_id = payload.get("sub")
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


# ==================== PERMISSION CHECKING ====================

def get_user_permissions(user) -> List[str]:
    """Get all permissions for a user based on their roles."""
    permissions = set()
    
    for role in user.roles:
        for permission in role.permissions:
            permissions.add(permission.name)
    
    return list(permissions)


def check_permission(user, required_permission: str) -> bool:
    """Check if user has a specific permission."""
    permissions = get_user_permissions(user)
    return required_permission in permissions

def check_role(user, required_role: str) -> bool:
    return any(role.name == required_role for role in user.roles)

# def check_role(user, required_role: str) -> bool:
#     """Check if user has a specific role."""
#     role_names = [role.name for role in user.roles]
#     return required_role in role_names


# ==================== DEFAULT ROLES & PERMISSIONS ====================

DEFAULT_PERMISSIONS = [
    {"name": "view_users", "description": "View users"},
    {"name": "create_users", "description": "Create new users"},
    {"name": "edit_users", "description": "Edit user information"},
    {"name": "delete_users", "description": "Delete users"},
    
    {"name": "view_projects", "description": "View projects"},
    {"name": "create_projects", "description": "Create projects"},
    {"name": "edit_projects", "description": "Edit projects"},
    {"name": "delete_projects", "description": "Delete projects"},
    
    {"name": "view_systems", "description": "View systems"},
    {"name": "create_systems", "description": "Create systems"},
    {"name": "edit_systems", "description": "Edit systems"},
    {"name": "delete_systems", "description": "Delete systems"},
    
    {"name": "view_components", "description": "View components"},
    {"name": "create_components", "description": "Create components"},
    {"name": "edit_components", "description": "Edit components"},
    {"name": "delete_components", "description": "Delete components"},
    
    {"name": "view_inventory", "description": "View inventory"},
    {"name": "manage_inventory", "description": "Manage inventory"},
    
    {"name": "view_reports", "description": "View reports"},
    {"name": "manage_maintenance", "description": "Manage maintenance logs"},
]

DEFAULT_ROLES = [
    {
        "name": "Admin",
        "description": "Full access to all features",
        "permissions": [p["name"] for p in DEFAULT_PERMISSIONS]
    },
    {
        "name": "ProjectManager",
        "description": "Can manage projects and teams",
        "permissions": [
            "view_users", "view_projects", "create_projects", "edit_projects",
            "view_systems", "create_systems", "edit_systems",
            "view_components", "create_components", "edit_components",
            "view_inventory", "view_reports"
        ]
    },
    {
        "name": "Technician",
        "description": "Can view and manage systems and components",
        "permissions": [
            "view_users", "view_projects", "view_systems", "edit_systems",
            "view_components", "edit_components", "view_inventory",
            "manage_inventory", "manage_maintenance"
        ]
    },
    {
        "name": "Viewer",
        "description": "Read-only access",
        "permissions": [
            "view_users", "view_projects", "view_systems",
            "view_components", "view_inventory", "view_reports"
        ]
    }
]

def initialize_roles_and_permissions(session: Session):
    """Initialize default roles and permissions in the database."""
    from app.models.tables import Role, Permission
    
    existing_roles = session.exec(select(Role)).all()
    if existing_roles:
        return
    
    permission_map = {}
    for perm_data in DEFAULT_PERMISSIONS:
        perm = Permission(**perm_data)
        session.add(perm)
        session.flush()
        permission_map[perm.name] = perm
    
    for role_data in DEFAULT_ROLES:
        role = Role(name=role_data["name"], description=role_data["description"])
        role.permissions = [permission_map[perm_name] for perm_name in role_data["permissions"]]
        session.add(role)
    
    session.commit()
