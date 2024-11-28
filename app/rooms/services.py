from fastapi import HTTPException, status
from pydantic import HttpUrl
from sqlalchemy.orm import Session, joinedload
from app.rooms.v1.schema import RoomCreate, RoomUpdate, Rooms, RoomStatus
from app.users.v1.schema import UserCreate, CreateSpecialUser
from app.rooms.models import Rooms
from app.reseverations.models import ReseverationsStatus
from app.reseverations.services import ReseverationServices
from app.users.auth import  get_current_user
from app.reseverations.v1.schema import Reseveration


class RoomServices:
    
    def get_room(self, db: Session, room_id: int):
        # return db.query(Rooms).filter(Rooms.id == room_id).first()
        room = db.query(Rooms).options(joinedload(Rooms.reservations)).filter(Rooms.id == room_id).first()
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return room
        
    # check if resvered den return status along side the details
    def get_reserve_room(self, db: Session, room_id: int):
        room = self.get_room(db, room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        # for k, v in room_update.items():
        # for res in room.reservations.items():
        for k, v in room.reservations.items():
            if room.status == ReseverationsStatus.RESERVED:
                return {
                    "room_id": room.id,
                    "room_name": room.room_name,
                    "status": room.status[ReseverationsStatus.RESERVED]
                }                

    # check if room status is reserver or open.
    def create_room(self, db: Session, payload: RoomCreate, current_user: int = None):
        # user = get_current_user(db, current_user)
        # if not user:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not login")
        db_user = Rooms(**payload.model_dump(),
                        user_id = current_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    
    def get_all_rooms(self, db: Session, skip: 0, limit: 10):
        return db.query(Rooms).offset(skip).limit(limit).all()
    
    # able to update a status of a room too.
    def update_room(self, db: Session, room_id:int, payload: RoomUpdate, current_user: int = None):
        room= self.get_room(db, room_id)
        if not room:
            None
            # HTTPException("room do not exist")
            
        room_update = payload.model_dump(exclude_unset=True)
            
        for k, v in room_update.items():
            setattr(room, k, v)

        db.add(room)
        db.commit()
        db.refresh(room)

        return room
    
    def delete_room(self, db: Session, room_id: int):
        room = self.get_room(db, room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room not found")
            
        db.delete(room)
        db.commit()
        return {'messaage': "Room Deleted Succesfully"}
        
    
    # update the status for a room from open to reserved
    #  say a room was reserved and lata cancle, the admin can update d status.