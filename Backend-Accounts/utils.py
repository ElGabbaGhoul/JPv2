from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv()
import os
secret_key=os.getenv('SECRET_KEY')
algorithm=os.getenv('ALGORITHM')
access_token_expires_minutes=os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES')

# Fake Database
db = {
    "tim": {
        "username":"tim",
        "full_name":"Tim Ruscica",
        "email":"tim@gmail.com",
        "hashed_password":"$2b$12$cJOxjcBBpipzGRjY0TgpleJ0TUzrv4K0DFU1QjJfa8ppi8VkPx5WC",
        "disabled": False
    }
}

# Move this to models.py
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str


# App object
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Begin Auth
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def authenticate_user(db, username: str, password: str,):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
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
# End Auth

# Begin Model Normalization


# wrote this to simplify model, decided to not use it
# def Trimmed_Datetime():
#     current_datetime = datetime.now()
#     trimmed_datetime = current_datetime.replace(microsecond=0)
#     return trimmed_datetime

