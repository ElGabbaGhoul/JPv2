from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    name: str
    profile_picture: Optional[str]
    role: str



    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
              'username':'john_doe',
              'email':'john@doe.com',
              'name':'John Doe',
              'profile_picture':'https://example.com/profile.jpg',
              'role':'Admin'
            }
        }


class UpdateUserModel(BaseModel):
    username: Optional[str] 
    email: Optional[str] 
    name: Optional[str]
    profile_picture: Optional[str]
    role: Optional[str]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
              'username':'john_doe',
              'email':'john@doe.com',
              'name':'John Doe',
              'profile_picture':'https://example.com/profile.jpg',
              'role':'Admin'
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class UserInDB(User):
    hashed_password: str

    class Config:
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
      schema_extra = {
          "example": {
            'username':'john_doe',
            'email':'john@doe.com',
            'name':'John Doe',
            'profile_picture':'https://example.com/profile.jpg',
            'role':'Admin',
            'hashed_password':'password123'
          }
      }