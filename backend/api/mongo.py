from pymongo import MongoClient
from models import Applicant, Admin, Building

client = MongoClient("mongodb://admin:pass@localhost:27017")
db = client.matching


def get_db():
    db = client.matching
    try:
        yield db
    finally:
        db.close()

