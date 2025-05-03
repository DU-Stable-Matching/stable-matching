from .database import SessionLocal
from .models import Admin, Applicant, Building
from typing import List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session

# utils/security.py
from passlib.hash import bcrypt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    db = SessionLocal()

    admins = db.query(Admin).all()
    if not admins:
        raise Exception("No admins found")

    admin_pref = []

    for ad in admins:
        temp = (ad.id, [])
        ad.rankings.sort(key=lambda x: x.rank)
        for rank in ad.rankings:
            temp[1].append(rank.applicant_id)

        admin_pref.append(temp)

    user_pref = []

    apps = db.query(Applicant).all()
    if not apps:
        raise Exception("No users found")

    for app in apps:
        temp = (app.id, [])
        app.preferences.sort(key=lambda x: x.rank)
        for pref in app.preferences:
            temp[1].append(pref.id)

        user_pref.append(temp)

    return admin_pref, user_pref
