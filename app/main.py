from router import router
from app.users.v1.router import user_router
from app.rooms.v1.router import room_router
from app.reservations.v1.router import reserve_router
from fastapi import FastAPI



app = FastAPI()

# app.include_router(router)
app.include_router(router=user_router,  prefix='/users', tags=['Users'])
app.include_router(router=room_router,  prefix='/rooms', tags=['Rooms'])
app.include_router(router=reserve_router,  prefix='/reservations', tags=['Reservations'])





@app.get("/")
async def root():
    return {"message": "Hello World"}




