from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from models import User, UpdateUserModel, Token
from dotenv import load_dotenv
import motor.motor_asyncio
load_dotenv()
import os
secret_key=os.getenv('SECRET_KEY')
algorithm=os.getenv('ALGORITHM')
access_token_expires_minutes=int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'))
connection_string = os.environ.get('DB_CONNECTION')


from utils import (
    verify_password,
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user
)

from database import (
    fetch_all_users, 
    fetch_one_user, 
    create_user, 
    update_user, 
    remove_user
    )

app = FastAPI()

# Set up a settings.py file later to import these settings?
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
database = db.UserList
collection = database.user

# Begin auth functions
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
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

# End auth functions

# Begin User API

@app.get("/api/user")
async def get_all_users():
    response = await fetch_all_users()
    return response

@app.post("/api/user", response_description="Create new user", response_model=User)
async def create_new_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    response = await create_user(user)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad Request")


@app.get("/api/user/{id}", response_description="Get a single user", response_model=User)
async def get_user_by_username(username: str):
    response = await fetch_one_user(username)
    if response:
        return response
    raise HTTPException(404, f"User with username {username} not found")

@app.put("/api/user/{id}", response_description="Update a user", response_model=User)
async def put_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        response = await update_user(id, user)
    if response:
        return response
    raise HTTPException(404, f"User with ID of {id} not found.")

@app.delete("/api/user/{id}", response_description="Delete a user")
async def delete_user(id: str):
    response = await remove_user(id)
    if response:
        return "Successfully deleted user item"
    raise HTTPException(404, f"User with ID of {id} not found.")

# End user API