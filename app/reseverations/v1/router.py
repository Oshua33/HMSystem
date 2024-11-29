from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.reseverations.services import ReseverationServices
from database import get_db
from app.reseverations.v1.schema import ReseverationCreate, ReseverationUpdate, ReseverationDisplay, ReseverationsStatus
from app.users.models import User
from app.users.auth import get_current_user

reserve_router = APIRouter(
    prefix='/reservations',
    tags=['Reservations']
)

@reserve_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reservation(db: Session, payload: ReseverationCreate, login_user: User = Depends(get_current_user)):
    new_reservation = ReseverationServices.create(db, payload, login_user)
    return new_reservation


@reserve_router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: Session, skip, limit):
    return ReseverationServices.get_all_rooms(db, skip, limit)

@reserve_router.get("/reserve_id", status_code=status.HTTP_200_OK)
async def get_reserved_details(db: Session, reserve_id: int):
    return ReseverationServices.get_reservation(db, reserve_id)

@reserve_router.delete('/reserve_id', status_code=status.HTTP_200_OK)
async def delete_reservation(db: Session, reserve_id: int):
    return ReseverationServices.delete_room(db, reserve_id)


@reserve_router.put("/reserve_id", status_code=status.HTTP_201_CREATED)
async def update_reservation(
    db: Session, 
    reserve_id: int, 
    payload: ReseverationUpdate, 
    login_user: User = Depends(get_current_user)
    ):
    return ReseverationServices.update(db, reserve_id, payload, login_user)




