from models import Playlist
import motor.motor_asyncio  # MongoDB Driver
# from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()
connection_string = os.environ.get('DB_CONNECTION')

client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)  # helps to connect with mongodb compass
database = client.PlaylistList  # name of database
# same thing as a table in SQL not really sure on why this isnt deploying
collection = database.playlist
category_collection = database.category

# Playlist DB Calls Start


async def fetch_all_playlists():
    playlists = []
    cursor = collection.find({})
    async for document in cursor:
        playlists.append(Playlist(**document))
    return playlists


async def create_playlist(playlist):
    document = playlist
    result = await collection.insert_one(document)
    return document


async def fetch_one_playlist(id):
    playlist = await collection.find_one({"_id": id})
    if playlist is not None:
        return playlist


async def update_playlist(id, playlist):
    update_result = await collection.update_one({"_id": id}, {"$set": playlist})
    if update_result.modified_count == 1:
        updated_playlist = await collection.find_one({"_id": id})
        if updated_playlist is not None:
            return updated_playlist
    existing_playlist = await collection.find_one({"_id": id})
    if existing_playlist is not None:
        return existing_playlist


async def remove_playlist(id):
    await collection.delete_one({"_id": id})
    return True
# Playlist DB Calls End