from uuid import UUID
from pydantic import BaseModel
from enum import Enum
from typing import List
from datetime import datetime
from typing import Optional
from decimal import Decimal

class OrderStatus(Enum):
    OPEN = "open"
    RESERVED = "reserved"

class Rooms(BaseModel):
    room_name: str
    room_no: str
    room_type: str
    price: float

class RoomCreate(Rooms):
    pass

    class config:
        form_attribute: True
        
class RoomUpdate(Rooms):
    room_name: str
    room_no: str
    room_type: str
    price: float

class RoomDisplay(Rooms):
    id: int



