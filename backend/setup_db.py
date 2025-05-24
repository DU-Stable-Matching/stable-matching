import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)


def setup_index():
    db = client.matching
    applicants_collection = db["applicants"]
    applicants_collection.create_index("applicant_id", unique=True)

    admins_collection = db["admins"]
    admins_collection.create_index("admin_id", unique=True)

    buildings_collection = db["buildings"]
    buildings_collection.create_index("building_id", unique=True)


def insert_dummy_data():
    db = client.matching
    applicants_collection = db["applicants"]
    admins_collection = db["admins"]
    buildings_collection = db["buildings"]

    with open("dummy.json", "r") as f:
        dummy_data = json.load(f)
        for i in range(len(dummy_data)):
            match i:
                case 0:
                    applicants_collection.delete_many({})
                    applicants_collection.insert_many(dummy_data[i])
                case 1:
                    admins_collection.delete_many({})
                    admins_collection.insert_many(dummy_data[i])
                case 2:
                    buildings_collection.delete_many({})
                    buildings_collection.insert_many(dummy_data[i])
                case _:
                    raise Exception("invalid dummy.json")


def main():
    setup_index()
    insert_dummy_data()
    print("done setting up db")


if __name__ == "__main__":
    main()
