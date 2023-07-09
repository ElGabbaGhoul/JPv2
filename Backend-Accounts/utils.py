import time
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from models import TokenData, UserInDB
from database import fetch_one_user
import motor.motor_asyncio

load_dotenv()
import os
secret_key=os.getenv('SECRET_KEY')
algorithm=os.getenv('ALGORITHM')
access_token_expires_minutes=os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES')
connection_string = os.environ.get('DB_CONNECTION')

db = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
database = db.UserList
collection = database.user

# App object
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Begin Auth
async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(email: str, password: str,):
    # user = get_user(db, email)
    user = await fetch_one_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: 
      expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data= TokenData(username=username)
    except JWTError:
      raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    
    return current_user

async def check_db_for_user(username):
    user = await collection.find_one({"username": username})
    return user is not None

async def authenticate_user_by_email(email, plain_password):
    user = await collection.find_one({"username": email})
    if user and verify_password(plain_password, user.get('hashed_password')):
        return UserInDB(**user)
    return None

# Basic rate limiting mechanism

# request_history = {}
# @app.middleware("http")
# async def limiter(request, call_next):
#     max_requests = 10
#     duration = 60  # 60 seconds
#     ip_address = request.client.host

#     if ip_address in request_history:
#         timestamps = request_history[ip_address]
#         # Remove timestamps older than the duration
#         timestamps = [timestamp for timestamp in timestamps if timestamp > time.time() - duration]
#         if len(timestamps) >= max_requests:
#             raise HTTPException(status_code=429, detail="Too Many Requests")

#         timestamps.append(time.time())
#         request_history[ip_address] = timestamps
#     else:
#         request_history[ip_address] = [time.time()]

#     response = await call_next(request)
#     return response
