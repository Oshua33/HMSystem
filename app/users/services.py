from sqlalchemy.orm import Session
from app.users.v1.schema import UserCreate, CreateSpecialUser
from app.users.models import User

class UserServices:
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, hashed_password: str):
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_active_users(db: Session):
        return db.query(User).filter(User.is_active == True).all()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    # Fetch all user fields (ORM objects) from the database
        return db.query(User).offset(skip).limit(limit).all()

