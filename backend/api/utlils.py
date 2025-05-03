from .database import SessionLocal
from .models import Admin, Applicant, Building

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


def get_prefrences():
    db = SessionLocal()
    # get all buildings
    admin = db.query(Admin).all()
    if not admin:
        raise Exception(status_code=404, detail="No admins found")

    admin_pref: list = []

    for admin in admin:
        pref = (admin.id, [])
        for pref in admin.rankings:
            pref[1].append(pref.applicant_id)

    # get all applicants

    apps = db.query(Applicant).all()
    if not apps:
        raise Exception(status_code=404, detail="No applicants found")

    app_pref: list = []

    for app in apps:
        pref = (app.id, [])
        for pref in app.preferences:
            building_name = pref.building_name
            # get the building id
            building = db.query(Building).filter(Building.name == building_name).first()
            boss_id = building.boss_id
            pref[1].append((building_name, boss_id))
        app_pref.append(pref)

    return admin_pref, app_pref
