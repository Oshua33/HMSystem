from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional
from typing import Literal
from decimal import Decimal

class UserBase(BaseModel):
    username: str
    email: str 
    password: str
    is_active: bool
    is_staff: bool
    is_admin: bool

    
    
class UserCreate(UserBase):
    pass

    class Config:
        from_attributes = True
        
class CreateSpecialUser(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool
    is_staff: bool
    is_active: bool
        
class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[str]


class UserDisplaySchema(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
