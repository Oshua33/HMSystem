from typing import List
from fastapi import HTTPException, status, Depends
# from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.rooms.v1.schema import RoomCreate, RoomUpdate, RoomStatus
from app.rooms.models import Rooms
from app.users.models import User
from app.reservations.models import ReservationsStatus
from app.users.auth import  get_current_user


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
            if room.status == ReservationsStatus.RESERVED:
                return {
                    "room_id": room.id,
                    "room_name": room.room_name,
                    "status": room.status[ReservationsStatus.RESERVED]
                }     


    # @staticmethod
    def create_room(self, db: Session, payload: RoomCreate, current_user: User):
        room_data = payload.model_dump()  # or payload.dict()

        # Convert status to its enum value (string)
        room_data['status'] = room_data['status'].value

        db_room = Rooms(**room_data, user_id=current_user.id)

        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room                

    # @staticmethod
    # def create_room( db: Session, payload: RoomCreate, current_user: User):
    
    #     # db_room = Rooms(**payload.model_dump(),
    #     #                 user_id=current_user.id,
    #     # )
    #     db_room = Rooms(
    #         room_name=payload.room_name,
    #         room_no=payload.room_no,
    #         room_type=payload.room_type,
    #         price=payload.price,
    #         status=payload.status.value,  # Pass the enum value as string
    #         user_id=current_user.id
    #     )

    #     db.add(db_room)
    #     db.commit()
    #     db.refresh(db_room)
    #     return db_room
    
    
    # def get_all_rooms(self, db: Session, skip: 0, limit: 10):
    #     return db.query(Rooms).offset(skip).limit(limit).all()
    
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
        
    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[dict]:
    # Build the query
        query = select(Rooms.room_no, Rooms.room_type, Rooms.price).filter(
            Rooms.room_no.isnot(None),   # Check for non-None room_no
            Rooms.price.isnot(None),     # Check for non-None price
            Rooms.room_type.isnot(None)  # Check for non-None room_type
        ).offset(skip).limit(limit)

        # Execute the query
        result = db.execute(query)

        # Fetch all results and return them as a list of dictionaries
        rooms = result.fetchall()

        # If you need to return the result as a list of dictionaries instead of tuples:
        room_list = [{"room_no": room[0], "room_type": room[1], "price": room[2]} for room in rooms]
        
        return room_list
    
    # # get rooms  with only price nd no
    # def get_all(self, db: Session, skip: 0, limit: 10):
    #     rooms = db.query(Rooms).select(Rooms.room_no, Rooms.room_type, Rooms.price).offset(skip).limit(limit).all()
    #     return rooms
    
    # def get_all(self, db: Session, skip: int = 0, limit: int = 10):
    #     query = (
    #         select(Rooms.room_no, Rooms.room_type, Rooms.price)
    #         .offset(skip)
    #         .limit(limit)
    #         )
    #     filtered_query  = query.filter(
    #         Rooms.room_no != None,
    #         Rooms.price != None,
    #         Rooms.room_type != None
    #     )
    #     rooms = db.execute(filtered_query )
    #     return rooms.fetchall()
    
    # update the status for a room from open to reserved
    #  say a room was reserved and lata cancle, the admin can update d status.
    
room_services = RoomServices()
