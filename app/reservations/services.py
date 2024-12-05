from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from app.reservations.v1.schema import ReservationsCreate, ReservationsUpdate, ReservationsStatus
from app.reservations.models import Reservations
from app.rooms.models import Rooms
from app.rooms.v1.schema import Room
from app.users.auth import  get_current_user
from app.users.models import User
from app.rooms.services import room_services


class ReservationsServices:
    
    # check if resvered den return status along side the details
    def get_reservations(self, db: Session, reserve_id: int):
        reservations = db.query(Reservations).filter(Reservations.id == reserve_id).first()
        if not reservations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
        return reservations
    
    # # check if room status is reserver or open.
    # def create(self, db: Session, payload: ReservationsCreate, current_user: User):
    #     reservations_data = payload.model_dump() 
    #     reservations_data['status'] = reservations_data['status'].value
    #     new_reservations = Reservations(**reservations_data, user_id=current_user.id
    #                                     )
    #     db.add(new_reservations)
    #     db.commit()
    #     db.refresh(new_reservations)
    #     return new_reservations
    #     # new_reservations= Reservations(**payload.model_dump(),
    #     #                 user_id = current_user.id)
    
    
    def get_all(self, db: Session, skip: 0, limit: 10):
        return db.query(Reservations).offset(skip).limit(limit).all()
    
    # able to update a status of a room too.
    def update(self, db: Session, reserve_id:int, payload: ReservationsUpdate, current_user: User):
        get_reservation= self.get_reservation(db, reserve_id)
        
        update = payload.model_dump(exclude_unset=True)
            
        for k, v in update.items():
            setattr(get_reservation, k, v)

        db.add(get_reservation)
        db.commit()
        db.refresh(get_reservation)
        return get_reservation
    
    
    def delete(self, db: Session, reserve_id: int):
        get_reservation= self.get_reservation(db, reserve_id)
        db.delete(get_reservation)
        db.commit()
        return {'messaage': "Deleted Succesfully"}
        
        
    def check_room_availability(self, db: Session, room_id: int, start_date: date, end_date: date):
        """
        check if the arrival date of quest is before or lesser dan the end date of the checkin of anoda client.
        check if the booking end date of the quest is after or greater than someone else checkout date.
        this ensures no mutiple clients gets to have conflict booking same room at same time.
        """
        check_availability = db.query(Reservations).filter(
            Reservations.room_id == room_id,
            Reservations.arrival_date < end_date,
            Reservations.departure_date > start_date
        ).all()
        
        """
        if the checks marks the room is available(i.e equal to 0), 
        but if checks is false is not available(i.e not equal to zero)
        """
        return len(check_availability) == 0
    
    def create_reservation(self, db: Session, payload: ReservationsCreate, current_user: User):
        # get the room
        room = db.query(Rooms).filter(Rooms.room_no == payload.room_no).first()
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Room with room_no {payload.room_no} not found"
                                )
            
        # check if room is avaiable during the client requested dates if not raise error
        start_date = payload.arrival_date
        end_date = payload.departure_date
        
        if not self.check_room_availability(db, room.id, start_date, end_date):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Room {payload.room_no} is not available for reservations"
                                )
            
        # but if available create reservations with the room_id
        reservation_data = payload.model_dump()
        reservation_data.pop('room_no', None)  # Remove room_no if it exists
        reservation_data["room_id"] = room.id
        reservation_data['user_id'] = current_user.id
        
        new_reservation = Reservations(**reservation_data,
                                    status=ReservationsStatus.RESERVED)
        
        db.add(new_reservation)
        print(new_reservation.status.value)  # Should print "RESERVED"

        db.commit()
        db.refresh(new_reservation)
        
        return new_reservation
        
        
    
reservations_services = ReservationsServices()