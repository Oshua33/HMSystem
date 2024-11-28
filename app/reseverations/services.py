from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import reseverations
from app.reseverations.v1.schema import ReseverationCreate, ReseverationUpdate
from app.reseverations.models import Reseveration
from app.users.auth import  get_current_user


class ReseverationServices:
    
    # check if resvered den return status along side the details
    def get_reservation(self, db: Session, reserve_id: int):
        reseveration = db.query(Reseveration).filter(Reseveration.id == reserve_id).first()
        if not reseveration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
        return reseveration
    
    # check if room status is reserver or open.
    def create(self, db: Session, payload: ReseverationCreate, current_user: int = None):
        new_reseveration= Reseveration(**payload.model_dump(),
                        user_id = current_user)
        db.add(new_reseveration)
        db.commit()
        db.refresh(new_reseveration)
        return new_reseveration
    
    
    def get_all(self, db: Session, skip: 0, limit: 10):
        return db.query(Reseveration).offset(skip).limit(limit).all()
    
    # able to update a status of a room too.
    def update(self, db: Session, reserve_id:int, payload: ReseverationUpdate, current_user: int = None):
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
        
    
    