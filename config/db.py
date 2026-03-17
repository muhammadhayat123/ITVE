from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_client():
    try:
        client = MongoClient(os.getenv("DB_URI"))
        print("MongoDB connected successfully")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    

client = get_db_client()

if client is None:
    raise RuntimeError("MongoDB client not initialized. Check DB_URI.")

db = client["itve"]

# Collections
users_collection = db["signup"]   # tumhari existing
posts_collection = db["posts"]