from fastapi.responses import FileResponse
from ..schemas import UserCreate, RAAppCreate, UserRead, UserLogin
from ..models import Applicant, BuildingPref
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from ..utlils import get_password_hash, verify_password
from ..mongo import get_db
import os

router = APIRouter()


@router.post("/create_applicant/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    applcants = db["applicants"]
    existing = applcants.find_one({"du_id": user.du_id})

    if existing:
        raise HTTPException(status_code=400, detail="DU ID already exists.")

    # find max id in applicats colleciotn
    max_id = applcants.find_one({}, sort=[("applicant_id", -1)])

    new_user = Applicant(
        applicant_id=max_id["id"] + 1 if max_id else 1,
        du_id=user.du_id,
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
        year_in_college=user.year_in_college,
    )
    # Insert the new user into the MongoDB collection
    applcants.insert_one(new_user.model_dump())

   
    return {"message": "User created successfully!", "id": new_user.applicant_id}


@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    applicants = db["applicants"]
    db_user = applicants.find_one({"du_id": user.du_id})

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful!", "id": db_user.id}


@router.post("/apply/")
def apply(data: RAAppCreate, db: Session = Depends(get_db)):
    applicant = db["applicants"] 
    user 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_returner = data.is_returner
    user.why_ra = data.why_ra

    # Clear existing preferences
    user.preferences.clear()
    for pref in data.preferences:
        user.preferences.append(
            BuildingPref(building_name=pref.building_name, rank=pref.rank)
        )
    user.given_preferences = True

    db.commit()
    return {"message": "Application submitted!"}


@router.post("/upload_resume/{id}")
def upload_resume(
    id: int, resume: UploadFile = File(...), db: Session = Depends(get_db)
):
    applicant = db.query(Applicant).filter(Applicant.id == id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed.")

    os.makedirs("resumes", exist_ok=True)
    save_path = f"resumes/{id}_{resume.filename}"
    with open(save_path, "wb") as f:
        f.write(resume.file.read())

    applicant.resume_path = f"{id}_{resume.filename}"
    db.commit()
    return {"message": "Resume uploaded!", "path": save_path}


@router.get("/applicants/{du_id}", response_model=UserRead)
def get_applicant(du_id: str, db: Session = Depends(get_db)):
    user = db.query(Applicant).filter(Applicant.du_id == du_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user


@router.get("/get_all_applicants/")
def all_applicants_with_preferences(db: Session = Depends(get_db)):
    applicants = db.query(Applicant).options(joinedload(Applicant.preferences)).all()
    if not applicants:
        raise HTTPException(status_code=404, detail="No applicants found")

    return applicants


@router.get("/applicant_given_preferences/{applicant_id}")
def get_applicant_given_preferences(applicant_id: int, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    return applicant.given_preferences


@router.get("/applicant/resume/{path}")
def get_applicant_resume(path: str):
    path = os.path.join("resumes", path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Resume not found")
    return FileResponse(
        path, media_type="application/pdf", filename=os.path.basename(path)
    )
