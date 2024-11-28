from fastapi import HTTPException, status
from httpx import delete
from sqlalchemy.orm import Session
from app.users.v1.schema import UserCreate, CreateSpecialUser, UserUpdate
from app.users.models import User

class UserServices:
    
    def create_user(self, db: Session, username: str, email: str, hashed_password: str):
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    
    def get_user_by_username(self, db: Session, username: str):
        # check if the user exist
        user = db.query(User).filter(User.id == username).first()
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        return user
    
    def get_user_by_id(self,user_id: int, db: Session):
        # check if the user exist
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        return user

    
    def get_active_users(self, db: Session):
        return db.query(User).filter(User.is_active == True).all()

    
    def get_all_users(self, db: Session, skip: int = 0, limit: int = 10):
    # Fetch all user fields (ORM objects) from the database
        return db.query(User).offset(skip).limit(limit).all()
    
    def update_user(self, user_id: int, db:Session, payload = UserUpdate, ):
        user = self.get_user_by_id(user_id, db)

        for k, v in payload.dict(exclude_unset=True).items():
            setattr(user, k, v)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    
            
