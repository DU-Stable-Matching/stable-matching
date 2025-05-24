import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client.matching
applicants_collection = db["applicants"]
applicants_collection.create_index("applicant_id", unique=True)

admins_collection = db["admins"]
admins_collection.create_index("admin_id", unique=True)

buildings_collection = db["buildings"]
buildings_collection.create_index("building_id", unique=True)
