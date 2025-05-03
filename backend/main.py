from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from typing import List
import os

from setup_db import seed_initial_buildings

from database import SessionLocal, engine
from models import Admin, AdminRanking, Base, Applicant, Building, BuildingPreference
from schemas import AdminRankingCreate, BuildingCreate, BuildingRead, UserCreate, UserRead, RAAppCreate, AdminCreate
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.on_event("startup")
def on_startup():
    seed_initial_buildings()



#--------------------------------USER ROUTES--------------------------------

@app.post("/create_applicant/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(Applicant).filter(Applicant.du_id == user.du_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="DU ID already exists.")
    new_user = Applicant(du_id=user.du_id, name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.du_id

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


@app.get("/buildings/")
def get_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    #convert buidling object to dict
    result = []
    for building in buildings:  
        print(building.id)
        result.append({
            "id": building.id,
            "name": building.name,
            "ra_needed": building.ra_needed,
            "boss_du_id": building.boss_du_id
        })
    return result
#-------------------------------RESET DATABASE-----------------------------------

@app.delete("/reset-database/")
def reset_database():
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Database reset successfully!"}


#-------------------------------ADMIN-----------------------------------
@app.post("/create_admin/")
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    if db.query(Admin).filter(Admin.du_id == admin.du_id).first():
        raise HTTPException(status_code=400, detail="Admin already exists")

    # Query the Building instance
    building_instance = db.query(Building).filter(Building.name == admin.building).first()
    if not building_instance:
        raise HTTPException(status_code=404, detail="Building not found")

        # Check if the building already has an admin
    if building_instance.boss_du_id:
        raise HTTPException(status_code=400, detail=f"Building '{admin.building}' already has an admin")
    # Create the Admin instance
    new_admin = Admin(
        du_id=admin.du_id,
        name=admin.name,
        email=admin.email,
        building=building_instance  # Assign the Building instance here
    )
   
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin.du_id


# Admin ranks anapplicant
@app.post("/admin_rank/")
def admin_rank(data: AdminRankingCreate, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.du_id == data.admin_du_id).first()
    applicant = db.query(Applicant).filter(Applicant.du_id == data.applicant_du_id).first()

    if not admin or not Applicant:
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
            admin_du_id=data.admin_du_id,
            applicant_du_id=data.applicant_du_id,
            rank=data.rank
        )
        db.add(ranking)
        db.commit()
        return {"message": f"{admin.name} ranked {applicant.name} as #{data.rank}"}

@app.get("/admin_rankings_by_admin/{admin_id}")
def view_admin_rankings(admin_du_id: str, db: Session = Depends(get_db)):
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