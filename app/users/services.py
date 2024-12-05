from fastapi import HTTPException, status
from httpx import delete
from sqlalchemy.orm import Session
from app.users.v1.schema import  CreateSpecialUser, UserUpdate
from app.users.models import User

class UserServices:

    @staticmethod
    def create_user( db: Session, username: str, email: str, hashed_password: str):
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_username( db, username: str):
        # check if the user exist
        user = db.query(User).filter(User.username == username).first()
        return user
        # if not user:
        #     raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        # )
    @staticmethod
    def get_user_by_id( user_id: int, db: Session):
        # check if the user exist
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        return user

    @staticmethod
    def get_active_users( db: Session):
        return db.query(User).filter(User.is_active == True).all()

    @staticmethod
    def get_all( db: Session, skip: int = 0, limit: int = 10):
    # Fetch all user fields (ORM objects) from the database
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user( user_id: int, db:Session, payload = UserUpdate, ):
        user = user_service.get_user_by_id(user_id, db)

        for k, v in payload.dict(exclude_unset=True).items():
            setattr(user, k, v)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    

user_service = UserServices()
            
