import os

from pymongo import MongoClient
from .models import Applicant, Admin, Building
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")


client = MongoClient(MONGO_URL)
db = client.matching
