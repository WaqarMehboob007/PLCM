from sqlmodel import SQLModel
from typing import Optional, List

class UserBase(SQLModel):
    name: str
    email: str
    hashPassword: str
    is_active : bool = False

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    hashPassword: Optional[str] = None
    is_active : Optional[bool] =  False 

