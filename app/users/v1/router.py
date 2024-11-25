# import auth
# import email
from typing import List
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app.users import services
from app.users.v1.schema import UserBase, UserCreate, UserUpdate, UserDisplaySchema
from app.users.services import UserServices
from app.users.models import User
from database import get_db
from app.users.auth import create_access_token, authenticate_user, pwd_context


user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@user_router.get('/', response_model=List[UserBase])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return  users


#logger = get_logger(__name__)


@user_router.post("/create_user/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserServices.get_user_by_username(db, username=user.username)
    hashed_password =pwd_context.hash(user.password)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return UserServices.create_user(db=db, username=user.username, email=user.email, hashed_password=hashed_password)



@user_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



    
@user_router.get("/users/", response_model=list[UserDisplaySchema])
def get_users(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 10, 
):
    users = UserServices.get_all_users(db, skip, limit)
    return users

