from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from typing import List
import os

from database import SessionLocal, engine
from models import Base, Applicant, BuildingPreference
from schemas import UserCreate, UserRead, RAAppCreate, BuildingPref

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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


@app.get("/applicants/{du_id}", response_model=UserRead)
def get_applicant(du_id: str, db: Session = Depends(get_db)):
    user = db.query(Applicant).filter(Applicant.du_id == du_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user

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

@app.delete("/reset-database/")
def reset_database():
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "Database reset successfully!"}
