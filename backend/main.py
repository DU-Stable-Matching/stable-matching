from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from typing import List
import os

from database import SessionLocal, engine
from models import Admin, AdminRanking, Base, Applicant, Building, BuildingPreference
from schemas import AdminRankingCreate, BuildingCreate, BuildingRead, UserCreate, UserRead, RAAppCreate, AdminCreate, AdminRead

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--------------------------------USER ROUTES--------------------------------

@app.post("/create_applicant/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(Applicant).filter(Applicant.du_id == user.du_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="DU ID already exists.")
    new_user = Applicant(du_id=user.du_id, name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/apply/")
def apply(data: RAAppCreate, db: Session = Depends(get_db)):
    user = db.query(Applicant).filter(Applicant.du_id == data.du_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.year_in_college = data.year_in_college
    user.is_returner = data.is_returner
    user.why_ra = data.why_ra
    user.resume_path = None  

    db.query(BuildingPreference).filter(BuildingPreference.applicant_du_id == data.du_id).delete()

    for pref in data.preferences:
        db.add(BuildingPreference(
            building_name=pref.building_name,
            rank=pref.rank,
            applicant_du_id=data.du_id
        ))

    db.commit()
    return {"message": "Application submitted!"}


@app.post("/upload-resume/{du_id}")
def upload_resume(du_id: str, resume: UploadFile = File(...), db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.du_id == du_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed.")

    os.makedirs("resumes", exist_ok=True)
    save_path = f"resumes/{du_id}_{resume.filename}"
    with open(save_path, "wb") as f:
        f.write(resume.file.read())

    applicant.resume_path = save_path
    db.commit()
    return {"message": "Resume uploaded!", "path": save_path}

'''------GET FUNCS-----'''
@app.get("/applicants/{du_id}", response_model=UserRead)
def get_applicant(du_id: str, db: Session = Depends(get_db)):
    user = db.query(Applicant).filter(Applicant.du_id == du_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user

@app.get("/all_applicants_with_preferences/")
def all_applicants_with_preferences(db: Session = Depends(get_db)):
    applicants = db.query(Applicant).all()
    result = []

    for applicant in applicants:
        prefs = sorted(applicant.preferences, key=lambda p: p.rank)
        formatted_prefs = [
            {
                "building": pref.building_name,
                "rank": pref.rank
            } for pref in prefs
        ]

        result.append({
            "du_id": applicant.du_id,
            "preferences": formatted_prefs
        })

    return result

#--------------------------------ADMIN ROUTES--------------------------------
@app.post("/create_admin/", response_model=AdminRead)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    if db.query(Admin).filter(Admin.du_id == admin.du_id).first():
        raise HTTPException(status_code=400, detail="Admin already exists")

    new_admin = Admin(
        du_id=admin.du_id,
        name=admin.name,
        email=admin.email,
        building_name=admin.building_name
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


# Admin ranks an applicant
@app.post("/admin_rank/")
def admin_rank(data: AdminRankingCreate, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.du_id == data.admin_du_id).first()
    applicant = db.query(Applicant).filter(Applicant.du_id == data.applicant_du_id).first()

    if not admin or not applicant:
        raise HTTPException(status_code=404, detail="Admin or applicant not found")

    existing_rank = db.query(AdminRanking).filter(
        AdminRanking.admin_du_id == data.admin_du_id,
        AdminRanking.applicant_du_id == data.applicant_du_id
    ).first()

    if existing_rank:
        existing_rank.rank = data.rank
        db.commit()
        return {"message": f"Updated ranking: {admin.name} now ranked {applicant.name} as #{data.rank}"}
    else:
        ranking = AdminRanking(
            admin_id=data.admin_du_id,
            applicant_du_id=data.applicant_du_id,
            rank=data.rank
        )
        db.add(ranking)
        db.commit()
        return {"message": f"{admin.name} ranked {applicant.name} as #{data.rank}"}

@app.get("/admin_rankings_by_admin/{admin_id}")
def view_admin_rankings(admin_du_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.du_id == admin_du_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    rankings = db.query(AdminRanking).filter(AdminRanking.admin_du_id == admin_du_id).all()

    return [
        {
            "applicant_du_id": r.applicant.du_id,
            "applicant_name": r.applicant.name,
            "rank": r.rank
        }
        for r in rankings
    ]
@app.post("/create_building/", response_model=BuildingRead)
def create_building(data: BuildingCreate, db: Session = Depends(get_db)):
    if db.query(Building).filter(Building.name == data.name).first():
        raise HTTPException(status_code=400, detail="Building already exists")
    
    building = Building(
        name=data.name,
        ra_needed=data.ra_needed,
        boss_du_id=data.boss_du_id
    )
    if data.boss_du_id:
        admin = db.query(Admin).filter(Admin.du_id == data.boss_du_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        building.boss = admin
    else:
        building.boss = None
    db.add(building)
    db.commit()
    db.refresh(building)
    return building

@app.get("/buildings/", response_model=List[BuildingRead])
def get_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()
#-------------------------------RESET DATABASE-----------------------------------

@app.delete("/reset-database/")
def reset_database():
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Database reset successfully!"}
