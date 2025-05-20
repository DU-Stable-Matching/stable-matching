from pymongo import MongoClient
from .models import Applicant, Admin, Building

client = MongoClient("mongodb://root:examplepassword@localhost:27017/?authSource=admin")
db = client.matching
