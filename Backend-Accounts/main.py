from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from utils import *
from dotenv import load_dotenv
load_dotenv()
import os
secret_key=os.getenv('SECRET_KEY')
algorithm=os.getenv('ALGORITHM')
access_token_expires_minutes=os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES')


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



# from database import (
#     fetch_all_playlists,
#     fetch_one_playlist,
#     create_playlist,
#     update_playlist,
#     remove_playlist
# )

# from fastapi import FastAPI, HTTPException, Body
# from fastapi.encoders import jsonable_encoder
# from fastapi.middleware.cors import CORSMiddleware
# # from datetime import datetime




# # Set up a settings.py file later to import these settings?
# origins = ['*']

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# async def read_root():
#     response = {"hello": "world"}
#     return response

# # Playlists Start


# @app.get("/api/playlist")
# async def get_playlists():
#     response = await fetch_all_playlists()
#     return response


# @app.post("/api/playlist", response_description="Add a new playlist", response_model=Playlist)
# async def post_playlist(playlist: Playlist = Body(...)):
#     playlist = jsonable_encoder(playlist)
#     response = await create_playlist(playlist)
#     if response:
#         return response
#     raise HTTPException(400, "Something went wrong / Bad Request")


# @app.get("/api/playlist/{id}", response_description="Get a single playlist", response_model=Playlist)
# async def get_playlist_by_id(id: str):
#     response = await fetch_one_playlist(id)
#     if response:
#         return response
#     raise HTTPException(404, f"ID {id} not found")


# @app.put("/api/playlist/{id}", response_description="Update a playlist", response_model=Playlist)
# async def put_playlist(id: str, playlist: UpdatePlaylistModel = Body(...)):
#     playlist = {k: v for k, v in playlist.dict().items() if v is not None}
#     if len(playlist) >= 1:
#         response = await update_playlist(id, playlist)
#     if response:
#         return response
#     raise HTTPException(404, f"There is no TODO item with this title {id}")


# @app.delete("/api/playlist/{id}", response_description="Delete a playlist")
# async def delete_playlist(id: str):
#     response = await remove_playlist(id)
#     if response:
#         return "Successfully deleted playlist item"
#     raise HTTPException(404, f"There is no TODO item with this id:{id}")
# # Playlists End