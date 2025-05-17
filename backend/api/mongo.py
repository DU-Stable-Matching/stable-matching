from pymongo import MongoClient

client = MongoClient("mongodb://admin:secret@localhost:27017")
db = client.my_new_database  # instead of client["my_new_database"]
coll = db.products  # instead of db["products"]

coll.insert_one({"name": "Gadget", "price": 19.99})
print(coll.find_one())
