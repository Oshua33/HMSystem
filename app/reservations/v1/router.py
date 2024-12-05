from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.reservations.services import reservations_services
from app.database import get_db
from app.reservations.v1.schema import ReservationsCreate, ReservationsUpdate, ReservationsStatus
from app.users.models import User
from app.users.auth import get_current_user

reserve_router = APIRouter(
    prefix='/reservations',
    tags=['Reservations']
)

@reserve_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reservation(payload: ReservationsCreate, curent_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_reservation = reservations_services.create_reservation(db, payload, curent_user)
    return new_reservation


@reserve_router.get("/", status_code=status.HTTP_200_OK)
async def get_all(skip, limit, db: Session = Depends(get_db)):
    return reservations_services.get_all(db, skip, limit)

@reserve_router.get("/reserve_id", status_code=status.HTTP_200_OK)
async def get_reserved_details(reserve_id: int, db: Session = Depends(get_db)):
    return reservations_services.get_reservation(db, reserve_id)

@reserve_router.delete('/reserve_id', status_code=status.HTTP_200_OK)
async def delete_reservation(reserve_id: int, db: Session = Depends(get_db)):
    return reservations_services.delete_room(db, reserve_id)


@reserve_router.put("/reserve_id", status_code=status.HTTP_201_CREATED)
async def update_reservation(
    reserve_id: int, 
    payload: ReservationsUpdate, 
    db: Session = Depends(get_db), 
    login_user: User = Depends(get_current_user)
    ):
    return reservations_services.update(db, reserve_id, payload, login_user)




