from database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum



class RoomStatus(Enum):
    OPEN = "open"
    RESERVED = "reserved"
    
class Rooms(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True)
    room_name = Column(String(50), unique=True)
    room_no = Column(String(120), nullable=True)
    room_type = Column(String(50), unique=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    
    # Enum for status
    status = Column(SQLAlchemyEnum(RoomStatus), nullable=False, default=RoomStatus.OPEN)
    
    # Relationship with Reseverations
    reservations = relationship("Reseverations", back_populates="room")

    
# class Rooms(Base):
#     __tablename__ = "rooms"
    
#     id = Column(Integer, primary_key=True)
#     room_name = Column(String(50), unique=True)
#     room_no = Column(String(120), nullable=True)
#     room_type = Column(String(50), unique=True)
#     price = Column(DECIMAL(10, 2), nullable=False)
    
#     # Enum for status
#     status = Column(SQLAlchemyEnum(RoomStatus), nullable=False, default=RoomStatus.OPEN)
    
#     reservation = relationship("Reseverations", back_populates="room")
    
    

    
