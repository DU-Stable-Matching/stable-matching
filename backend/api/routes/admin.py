from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from ..utlils import get_password_hash, verify_password
from ..schemas import AdminLogin, AdminRankingCreate
from ..mongo import get_db

router = APIRouter()


@router.post("/admin_login/")
def admin_login(admin: AdminLogin, db=Depends(get_db)):
    admins = db["admins"]
    db_admin = admins.find_one({"du_id": admin.du_id})
    if not db_admin or not verify_password(admin.password, db_admin["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful!", "id": str(db_admin["_id"])}


@router.get("/admin/{admin_id}")
def get_admin(admin_id: str, db=Depends(get_db)):
    admins = db["admins"]
    try:
        admin_db = admins.find_one({"_id": ObjectId(admin_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")
    if not admin_db:
        raise HTTPException(status_code=404, detail="Admin not found")
    admin_db["_id"] = str(admin_db["_id"])
    return admin_db


@router.get("/admin_given_preferences/{admin_id}")
def get_admin_given_preferences(admin_id: str, db=Depends(get_db)):
    admin = get_admin(admin_id, db)
    return admin.get("pref", [])


@router.get("/get_all_admins/")
def get_all_admins(db=Depends(get_db)):
    admins = list(db["admins"].find({}))
    if not admins:
        raise HTTPException(status_code=404, detail="No admins found")
    for admin in admins:
        admin["_id"] = str(admin["_id"])
    return admins


@router.post("/admin_rank/")
def admin_rank(data: AdminRankingCreate, db=Depends(get_db)):
    admins = db["admins"]
    applicants = db["applicants"]
    rankings = db["admin_rankings"]

    try:
        admin_obj_id = ObjectId(data.admin_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    admin = admins.find_one({"_id": admin_obj_id})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    # Clear existing rankings
    rankings.delete_many({"admin_id": data.admin_id})

    # Insert new rankings
    new_rankings = []
    for r in data.list_of_rankings:
        applicant = applicants.find_one({"name": r.applicant_name})
        if not applicant:
            raise HTTPException(status_code=404, detail=f"Applicant '{r.applicant_name}' not found")
        new_rankings.append({
            "admin_id": data.admin_id,
            "applicant_id": str(applicant["_id"]),
            "rank": r.rank
        })

    if new_rankings:
        rankings.insert_many(new_rankings)

    return {"message": "Rankings submitted successfully!"}


@router.get("/admin_rankings_by_admin/{admin_id}")
def view_admin_rankings(admin_id: str, db=Depends(get_db)):
    try:
        ObjectId(admin_id)  # validate
    except:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    rankings = list(db["admin_rankings"].find({"admin_id": admin_id}))
    for r in rankings:
        r["_id"] = str(r["_id"])
    return rankings
