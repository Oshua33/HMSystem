from app.database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum


class RoomStatus(Enum):
    IS_AVAILABLE = "is_available"
    RESERVED = "reserved"
    


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_name = Column(String(50), unique=True)
    room_no = Column(String(120), nullable=True)
    room_type = Column(String(50), unique=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLAlchemyEnum(RoomStatus), nullable=False, default=RoomStatus.IS_AVAILABLE)

    # Relationships
    reservations = relationship("Reservations", back_populates="room")
    user = relationship("User", back_populates="rooms")

    

    
