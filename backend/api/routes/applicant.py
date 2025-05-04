from ..schemas import UserCreate, RAAppCreate, UserRead, UserLogin
from ..models import Applicant, BuildingPref
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from ..utlils import get_db, get_password_hash, verify_password
import os

router = APIRouter()


@router.post("/create_applicant/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(Applicant).filter(Applicant.du_id == user.du_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="DU ID already exists.")

    new_user = Applicant(
        du_id=user.du_id,
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
        year_in_college=user.year_in_college,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully!", "id": new_user.id}
    


@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Applicant).filter(Applicant.du_id == user.du_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful!", "id": db_user.id}


@router.post("/apply/")
def apply(data: RAAppCreate, db: Session = Depends(get_db)):
    user = db.query(Applicant).filter(Applicant.id == data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_returner = data.is_returner
    user.why_ra = data.why_ra

    for pref in data.preferences:
        user.preferences.append(
            BuildingPref(building_name=pref.building_name, rank=pref.rank)
        )
    db.commit()
    return {"message": "Application submitted!"}


@router.post("/upload-resume/{du_id}")
def upload_resume(
    du_id: str, resume: UploadFile = File(...), db: Session = Depends(get_db)
):
    applicant = db.query(Applicant).filter(Applicant.id == id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed.")

    du_id = applicant.du_id

    os.makedirs("resumes", exist_ok=True)
    save_path = f"resumes/{du_id}_{resume.filename}"
    with open(save_path, "wb") as f:
        f.write(resume.file.read())

    applicant.resume_path = save_path
    db.commit()
    return {"message": "Resume uploaded!", "path": save_path}


@router.get("/applicants/{du_id}", response_model=UserRead)
def get_applicant(du_id: str, db: Session = Depends(get_db)):
    user = db.query(Applicant).filter(Applicant.du_id == du_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user

@router.get("/applicant_given_preferences/{id}")
def get_applicant_given_preferences(id: str, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    return applicant.given_preferences

@router.get("/get_all_applicants/")
def all_applicants_with_preferences(db: Session = Depends(get_db)):
    applicants = db.query(Applicant).options(joinedload(Applicant.preferences)).all()
    if not applicants:
        raise HTTPException(status_code=404, detail="No applicants found")

    return applicants
