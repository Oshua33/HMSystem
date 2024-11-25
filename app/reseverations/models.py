from database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum



class ReseverationsStatus(Enum):
    OPEN = "open"
    RESERVED = "reserved"
    
class Reseverations(Base):
    __tablename__ = "reserverations"
    
    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String, nullable=False)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    status = Column(Enum(ReseverationsStatus, name="order_status"),default="reserved", nullable=False)
    room_no = Column(String, ForeignKey("rooms.room_no"), nullable=False)  # Match room_number as String in ForeignKey
    room_id = Column(Integer, ForeignKey("rooms.id"))
    
    room = relationship("Room", back_populates="reservations")
    
