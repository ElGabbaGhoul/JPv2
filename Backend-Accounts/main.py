from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from utils import *
from dotenv import load_dotenv
load_dotenv()
import os
secret_key=os.getenv('SECRET_KEY')
algorithm=os.getenv('ALGORITHM')
access_token_expires_minutes=int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'))

from database import (
    fetch_all_users, 
    fetch_one_user, 
    create_user, 
    update_user, 
    remove_user
    )

# Set up a settings.py file later to import these settings?
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or passowrd", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=access_token_expires_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


@app.post("/api/user", response_description="Create new user", response_model=User)
async def create_new_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    response = await create_user(user)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad Request")
