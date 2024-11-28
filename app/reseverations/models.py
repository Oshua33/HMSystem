from database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum



class ReseverationsStatus(Enum):
    OPEN = "open"
    RESERVED = "reserved"
    
class Reseveration(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String, nullable=False)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(ReseverationsStatus), nullable=False, default=ReseverationsStatus.RESERVED)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    
    # Relationship with Rooms
    room = relationship("Rooms", back_populates="reservations")

