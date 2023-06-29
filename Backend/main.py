from fastapi import FastAPI, HTTPException, Body
from models import Playlist, UpdatePlaylistModel

from database import (
    fetch_all_playlists,
    fetch_one_playlist,
    create_playlist,
    update_playlist,
    remove_playlist
)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime

# App object
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


@app.get("/")
async def read_root():
    response = {"hello": "world"}
    return response

# Playlists Start


@app.get("/api/playlist")
async def get_playlists():
    response = await fetch_all_playlists()
    return response


@app.post("/api/playlist", response_description="Add a new playlist", response_model=Playlist)
async def post_playlist(playlist: Playlist = Body(...)):
    playlist = jsonable_encoder(playlist)
    response = await create_playlist(playlist)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad Request")


@app.get("/api/playlist/{id}", response_description="Get a single playlist", response_model=Playlist)
async def get_playlist_by_id(id: str):
    response = await fetch_one_playlist(id)
    if response:
        return response
    raise HTTPException(404, f"ID {id} not found")


@app.put("/api/playlist/{id}", response_description="Update a playlist", response_model=Playlist)
async def put_playlist(id: str, playlist: UpdatePlaylistModel = Body(...)):
    playlist = {k: v for k, v in playlist.dict().items() if v is not None}
    if len(playlist) >= 1:
        response = await update_playlist(id, playlist)
    if response:
        return response
    raise HTTPException(404, f"There is no playlist with id of {id}")


@app.delete("/api/playlist/{id}", response_description="Delete a playlist")
async def delete_playlist(id: str):
    response = await remove_playlist(id)
    if response:
        return "Successfully deleted playlist item"
    raise HTTPException(404, f"There is no playlist with id of {id}")
# Playlists End