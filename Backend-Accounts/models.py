from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional
from bson import ObjectId
from datetime import datetime
from utils import Trimmed_Datetime

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
    password: str
    name: str
    profile_picture: Optional[str]
    role: str
    created_on: Trimmed_Datetime()



    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
              'username':'john_doe',
              'email':'john@doe.com',
              'password':'johnisgreat1234',
              'name':'John Doe',
              'profile_picture':'https://example.com/profile.jpg',
              'role':'Admin',
              'created_on': '2023-06-26 11:42:34',
            }
        }


# class UpdatePlaylistModel(BaseModel):
#     name: Optional[str] 
#     description: Optional[str] 
#     created_on: Optional[str]
#     updated_on: Optional[str] 
#     owner_id: Optional[str] 
#     tracks: Optional[list]
#     duration: Optional[int] 
#     is_public: Optional[bool] 
#     tags: Optional[list]
#     creator_notes: Optional[str] 
#     image_url: Optional[str]
#     listener_comments: Optional[list] 

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                     'name': 'My Epic Playlist',
#                     'description': 'Songs for fighting bad guys',
#                     'created_on': '06/22/2023',
#                     'updated_on': '06/23/2023',
#                     'owner_id': 'A113',
#                     'tracks': ['BTK', 'lain', 'Leach', 'Amie'],
#                     'duration': 43000,
#                     'is_public': True,
#                     'tags': ['cool', 'epic', 'genre'],
#                     'creator_notes': 'I made this',
#                     'image_url': 'https://media.giphy.com/media/WWvteK57VNvxu/giphy.gif',
#                     'listener_comments': ['wow what a great playlist', 'this is awesome', 'who made this?']
#             }
#         }