# from uuid import UUID
# from pydantic import BaseModel
# from enum import Enum
# from typing import List
# from datetime import datetime
# from typing import Optional

# class ReservationsStatus(Enum):
#     RESERVED = "reserved"
#     IS_AVAILABLE = "is_available"

# class Reservations(BaseModel):
#     guest_name: str
#     room_no: str
#     arrival_date: int
#     departure_date: int
#     status: ReservationsStatus

# class ReservationsCreate(Reservations):
#     pass

#     class config:
#         form_attribute: True
        
# class ReservationsUpdate(Reservations):
#     guest_name: Optional[str]
#     arrival_date: Optional[int]
#     departure_date: Optional[int]
#     status:Optional[str] 
    
    
# class ReservationsDisplay(BaseModel):
#     id: int
#     room_name: str
#     room_no: str
#     room_type: str
#     price: float
#     status: ReservationsStatus
    


from uuid import UUID
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class ReservationsStatus(Enum):
    RESERVED = "RESERVED"
    IS_AVAILABLE = "IS_AVAILABLE"

class Reservations(BaseModel):
    guest_name: str
    room_no: str
    arrival_date: datetime  # Using datetime for better handling of date fields
    departure_date: datetime
    status: ReservationsStatus
    
    class Config:
        orm_mode = True

class ReservationsCreate(Reservations):
    pass

    class Config:  # Corrected `config` to `Config` and `orm_mode = True`
        orm_mode = True  # Important for serialization and deserialization of ORM models

class ReservationsUpdate(Reservations):
    guest_name: Optional[str]
    arrival_date: Optional[datetime]  # Use datetime to handle dates correctly
    departure_date: Optional[datetime] 
    status: Optional[ReservationsStatus]  # Change to Enum type to match the ReservationsStatus Enum

    class Config:
        orm_mode = True
        
class ReservationsDisplay(BaseModel):
    id: int
    room_name: str
    room_no: str
    room_type: str
    price: float
    status: ReservationsStatus

    class Config:
        orm_mode = True  # Ensure that the ORM model can be serialized to a Pydantic model



