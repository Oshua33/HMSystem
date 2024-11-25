from uuid import UUID
from pydantic import BaseModel
from enum import Enum
from typing import List
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ReseverationsStatus(Enum):
    OPEN = "open"
    RESERVED = "reserved"

class Reseveration(BaseModel):
    guest_name: str
    room_no: str
    arrival_date: int
    departure_date: int

class ReseverationCreate(Reseveration):
    pass

    class config:
        form_attribute: True
        
class ReseverationUpdate(Reseveration):
    guest_name: str
    arrival_date: int
    departure_date: int

class ReseverationDisplay(Reseveration):
    id: int



