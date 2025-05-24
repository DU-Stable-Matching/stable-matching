from .models import Admin, Applicant, Building
from typing import List, Tuple
from fastapi import HTTPException
from pymongo.collection import Collection
from .mongo import db
from bson import ObjectId

# utils/security.py
from passlib.hash import bcrypt


def get_password_hash(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def get_preferences():
    """
    Returns two lists of preferences:
      1. Admin preferences as (admin_id, [applicant_id, …])
      2. Applicant preferences as (applicant_id, [(building_name, boss_id), …])
    Raises 404 if no admins or no applicants exist.
    """
    db = get_db()
    applicants: Collection = db["applicants"]
    admins: Collection = db["Admins"]

    user_pref = applicants.find_one({})["pref"]
    admin_pref = admins.find_one({})["pref"]

    return user_pref, admin_pref


def mongo_arr_to_dict(arr: list[dict]):
    res = []
    for v in arr:
        if "_id" in v:
            del v["_id"]
        res.append(v)
    return res
