from fastapi import APIRouter,  Depends, status
from sqlalchemy.orm import Session
from app.rooms.services import room_services
from app.rooms.models import Rooms
from app.database import get_db
from app.rooms.v1.schema import RoomCreate, RoomUpdate
from app.users.models import User
from app.users.auth import get_current_user

room_router = APIRouter(
    # prefix='/rooms',
    tags=['Rooms']
)

@room_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(payload: RoomCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_room = room_services.create_room(db, payload, current_user)
    return new_room
    # return new_room


# @room_router.get("/", status_code=status.HTTP_200_OK)
# async def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return RoomServices.get_all_rooms(db, skip, limit)

@room_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return room_services.get_all(db, skip, limit)

@room_router.get("/room_id", status_code=status.HTTP_200_OK)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    return room_services.get_room(db, room_id)

@room_router.delete('/room_id', status_code=status.HTTP_200_OK)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_services.delete_room(db, room_id)


@room_router.put("/room_id", status_code=status.HTTP_201_CREATED)
async def update_room(
    room_id: int, 
    payload: RoomUpdate, 
    db: Session = Depends(get_db), 
    login_user: User = Depends(get_current_user)
    ):
    return room_services.update_room(db, room_id, payload, login_user)

# update the status for a room using patach