from .database import SessionLocal
from .models import Admin, Applicant, Building
from typing import List, Tuple
import random
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
            building =  db.query(Building).filter(Building.name == pref.building_name).first()
            temp[1].append(building.id)
        user_pref.append(temp)
    # if len(user_pref) > len(admin_pref):

    #     user_pref =  user_pref[: len(admin_pref)]

    return user_pref, admin_pref


def get_two_preferences():
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
        ra_needed = ad.building.ra_needed
        for i in range(ra_needed):
            temp = ((ad.id,i+1), [])
            for rank in ad.rankings:
                applicant_ranking = random.shuffle(rank)
                for app in applicant_ranking:
                    temp[1].append(app.applicant_id) 
        admin_pref.append(temp)

    user_pref = []

    apps = db.query(Applicant).all()
    if not apps:
        raise Exception("No users found")

    for app in apps:
        temp = (app.id, [])
        app.preferences.sort(key=lambda x: x.rank)
        for pref in app.preferences:
            building =  db.query(Building).filter(Building.name == pref.building_name).first()
            temp[1].append(building.id)
        user_pref.append(temp)

    return user_pref, admin_pref

