from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError

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

db = client["itve"]  # local database
users_collection = db["signup"]  # collection
audit_logs_collection = db["audit_logs"]


def ensure_indexes():
    """
    Best-effort index creation for performance and uniqueness.
    If the collection contains duplicates, unique indexes will fail; we do not crash the app.
    """
    try:
        users_collection.create_index("email", unique=True, name="uniq_email")
    except PyMongoError as e:
        print(f"Index create failed (email): {e}")

    try:
        users_collection.create_index("username", unique=True, name="uniq_username")
    except PyMongoError as e:
        print(f"Index create failed (username): {e}")

    try:
        users_collection.create_index("location", name="idx_location")
    except PyMongoError as e:
        print(f"Index create failed (location): {e}")

    try:
        audit_logs_collection.create_index("created_at", name="idx_audit_created_at")
        audit_logs_collection.create_index("actor_user_id", name="idx_audit_actor_user_id")
    except PyMongoError as e:
        print(f"Index create failed (audit): {e}")


ensure_indexes()

