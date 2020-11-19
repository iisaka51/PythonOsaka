from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from models import (
        User, UserCreate, UserUpdate, UserDB, UserTable, users, user_db
     )
from db import Base, engine, database

SECRET = "SECRET"

def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")

def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")

jwt_auth = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

app = FastAPI()
fastapi_users = FastAPIUsers(
    user_db, [jwt_auth], User, UserCreate, UserUpdate, UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_auth),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"]
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
def index(user=Depends(fastapi_users.get_current_user)):
    return {"Hello": "World!"}
