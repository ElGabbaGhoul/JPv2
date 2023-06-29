from models import User
import motor.motor_asyncio
import os
from dotenv import load_dotenv
load_dotenv()

connection_string = os.environ.get('DB_CONNECTION')
client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
database = client.UserList
collection = database.user

# Account DB Calls Start

async def fetch_all_users():
    users = []
    cursor = collection.find({})
    async for document in cursor:
        users.append(User(**document))
    return users

async def create_user(user):
    document = user
    result = await collection.insert_one(user)
    return document

async def fetch_one_user(id):
    user = await collection.find_one({"_id": id})
    if user is not None:
        return user
    

async def update_user(id, user):
    update_result = await collection.update_one({"_id": id}, {"$set": user})
    if update_result.modified_count == 1:
        updated_user = await collection.find_one({"_id": id})
        if updated_user is not None:
            return updated_user
    existing_user = await collection.find_one({"_id": id})
    if existing_user is not None:
        return existing_user


async def remove_user(id):
    await collection.delete_one({"_id": id})
    return True