from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from ..schemas import UserCreate, RAAppCreate, UserRead, UserLogin
from ..models import Applicant  # your Pydantic/ORM model used for validating inserts
from ..utlils import get_password_hash, verify_password, mongo_arr_to_dict
from ..mongo import db
from bson import ObjectId
import os

router = APIRouter()


@router.post("/create_applicant/")
def create_user(
    user: UserCreate,
):
    applicants = db["applicants"]
    existing = applicants.find_one({"du_id": user.du_id})
    if existing:
        raise HTTPException(status_code=400, detail="DU ID already exists.")

    # find max applicant_id in applicants collection
    max_doc = applicants.find_one({}, sort=[("applicant_id", -1)])
    next_id = (max_doc["applicant_id"] + 1) if max_doc else 1

    new_user = Applicant(
        applicant_id=next_id,
        du_id=user.du_id,
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
        year_in_college=user.year_in_college,
        resume_path=None,
        pref=None,
        is_returner=None,
    )
    applicants.insert_one(new_user.model_dump())
    return {"message": "User created successfully!", "id": new_user.applicant_id}


@router.post("/login/")
def login(user: UserLogin):
    applicants = db["applicants"]
    db_user = applicants.find_one({"du_id": user.du_id})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful!", "id": db_user["applicant_id"]}


@router.post("/apply/")
def apply(data: RAAppCreate):
    applicants = db["applicants"]
    user = applicants.find_one({"applicant_id": data.id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # TODO: likely the prefrences will come in the form which are not well formated
    # this means there will likely be a

    update_fields = {
        "is_returner": data.is_returner,
        "why_ra": data.why_ra,
        "preferences": [pref.model_dump() for pref in data.preferences],
        "has_given_pref": True,
    }

    applicants.update_one({"_id": user["_id"]}, {"$set": update_fields})
    return {"message": "Application submitted!"}


@router.post("/upload_resume/{id}")
def upload_resume(id: int, resume: UploadFile = File(...)):
    applicants = db["applicants"]
    user = applicants.find_one({"applicant_id": id})
    if not user:
        raise HTTPException(status_code=404, detail="Applicant not found")
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed.")

    os.makedirs("resumes", exist_ok=True)
    save_path = f"resumes/{id}_{resume.filename}"
    with open(save_path, "wb") as f:
        f.write(resume.file.read())

    applicants.update_one({"_id": user["_id"]}, {"$set": {"resume_path": save_path}})
    return {"message": "Resume uploaded!", "path": save_path}


@router.get("/applicants/{du_id}")
def get_applicant(du_id: str, db):
    applicants = db["applicants"]
    doc = applicants.find_one({"du_id": du_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return doc


@router.get("/get_all_applicants/")
def all_applicants_with_preferences():
    applicants = db["applicants"]
    docs = mongo_arr_to_dict(list(applicants.find({})))
    if not docs:
        raise HTTPException(status_code=404, detail="No applicants found")
    return docs


@router.get("/applicant_given_preferences/{applicant_id}")
def get_applicant_given_preferences(applicant_id: int):
    applicants = db["applicants"]
    doc = applicants.find_one({"applicant_id": applicant_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Applicant not found")
    # return only the boolean (or full doc if you prefer)
    return {"given_preferences": doc.get("given_preferences", False)}
