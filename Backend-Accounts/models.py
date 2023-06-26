# # from typing import Optional
# from pydantic import BaseModel, Field
# from bson.objectid import ObjectId
# from typing import Optional
# from bson import ObjectId


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


# class Playlist(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     name: str
#     description: str
#     created_on: str
#     updated_on: str
#     owner_id: str
#     tracks: list
#     duration: int
#     is_public: bool
#     tags: list
#     creator_notes: str
#     image_url: str
#     listener_comments: list


#     class Config:
#         allow_population_by_field_name = True
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