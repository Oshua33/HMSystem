from uuid import UUID
import uuid
from pydantic import BaseModel
from enum import Enum
from typing import List
from typing import Optional

class RoomStatus(Enum):
    IS_AVAILABLE = 'IS_AVAILABLE'
    RESERVED = 'RESERVED'


class Room(BaseModel):
    room_name: str
    room_no: str
    room_type: str
    price: float
    status: RoomStatus
    
    class Config:
        orm_mode = True

class RoomCreate(Room):
    pass

    class config:
        form_attribute: True
        
class RoomUpdate(Room):
    room_name: Optional[str]
    room_no: Optional[str]
    room_type: Optional[str]
    price: Optional[float]
    status: Optional[RoomStatus]  
        
    class Config:
        orm_mode = True

class RoomDisplay(BaseModel):
    id: int
    room_name: str
    room_no: str
    room_type: str
    price: float
    status: RoomStatus



