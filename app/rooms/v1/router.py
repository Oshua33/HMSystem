from fastapi import APIRouter,  Depends, status
from sqlalchemy.orm import Session
from app.rooms.services import RoomServices
from database import get_db
from app.rooms.v1.schema import RoomCreate, RoomUpdate
from app.users.models import User
from app.users.auth import get_current_user

room_router = APIRouter(
    prefix='/rooms',
    tags=['Rooms']
)

@room_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(db: Session, payload: RoomCreate, login_user: User = Depends(get_current_user)):
    new_room = RoomServices.create_room(db, payload, login_user)
    return new_room


@room_router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: Session, skip, limit):
    return RoomServices.get_all_rooms(db, skip, limit)

@room_router.get("/room_id", status_code=status.HTTP_200_OK)
async def get_room(db: Session, room_id: int):
    return RoomServices.get_room(db, room_id)

@room_router.delete('/room_id', status_code=status.HTTP_200_OK)
async def delete_room(db: Session, room_id: int):
    return RoomServices.delete_room(db, room_id)


@room_router.put("/room_id", status_code=status.HTTP_201_CREATED)
async def update_room(
    db: Session, 
    room_id: int, 
    payload: RoomUpdate, 
    login_user: User = Depends(get_current_user)
    ):
    return RoomServices.update_room(db, room_id, payload, login_user)

# update the status for a room using patach