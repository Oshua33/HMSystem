
from fastapi import HTTPException
import models
from sqlalchemy.orm import Session
from app.rooms.v1.schema import RoomCreate, RoomUpdate, Rooms
from app.users.v1.schema import UserCreate, CreateSpecialUser
from app.rooms.models import Rooms
from app.users.auth import  get_current_user


class RoomServices:
    
    def get_room(self, db: Session, room_id: int):
        return db.query(Rooms).filter(Rooms.id == room_id).first()
    
    
    def create_room(self, db: Session, payload: RoomCreate, current_user: int = None):
        db_user = Rooms(**payload.model_dump(),
                        user_id = current_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    
    def get_all_rooms(self, db: Session, skip: 0, limit: 10):
        return db.query(Rooms).offset(skip).limit(limit).all()
    
    
    def update_room(self, db: Session, room_id:int, payload: RoomUpdate, current_user: int = None):
        get_room= self.get_room(db, room_id)
        if not get_room:
            HTTPException("room do not exist")
            
        room_update = payload.model_dump(exclude_unset=True)
            
        for k, v in room_update.items():
            setattr(get_room, k, v)

        db.add(get_room)
        db.commit()
        db.refresh(get_room)

        return get_room
    
    def delete_room(self, db: Session, room_id: int):
        get_room = self.get_room(db, room_id)
        if not get_room:
            None
            
        db.delete(get_room)
        db.commit()
        return {'messaage': "Deleted Succesfully"}
        
    
    