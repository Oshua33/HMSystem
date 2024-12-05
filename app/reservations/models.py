from app.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum


class ReservationsStatus(Enum):
    IS_AVAILABLE = "is_available"
    RESERVED = "reserved"


class Reservations(Base):  # Correct class name
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String, nullable=False)
    
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(ReservationsStatus), nullable=False, default=ReservationsStatus.RESERVED)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))

    # Relationships
    room = relationship("Rooms", back_populates="reservations")
    user = relationship("User", back_populates="reservations")

