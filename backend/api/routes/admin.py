from fastapi import APIRouter, HTTPException
from ..utlils import get_password_hash, verify_password, db ## we need to fix this typo in the file name
from ..schemas import AdminLogin, AdminRankingCreate

router = APIRouter()


@router.post("/admin_login/")
def admin_login(admin: AdminLogin):
    admins = db["admins"]
    db_admin = admins.find_one({"du_id": admin.du_id})
    if not db_admin or not verify_password(admin.password, db_admin["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful!", "id": db_admin["admin_id"]}


@router.get("/admin/{admin_id}")
def get_admin(admin_id: str):
    admins = db["admins"]
    try:
        admin_id_int = int(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    admin_db = admins.find_one({"admin_id": admin_id_int})
    if not admin_db:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin_db


@router.get("/admin_given_preferences/{admin_id}")
def get_admin_given_preferences(admin_id: str):
    admin = get_admin(admin_id, db)
    return admin.get("pref", [])


@router.get("/get_all_admins/")
def get_all_admins():
    admins = list(db["admins"].find({}))
    if not admins:
        raise HTTPException(status_code=404, detail="No admins found")
    return admins


@router.post("/admin_rank/")
def admin_rank(data: AdminRankingCreate):
    admins = db["admins"]
    applicants = db["applicants"]
    rankings = db["admin_rankings"]

    admin = admins.find_one({"admin_id": data.admin_id})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    # Clear existing rankings
    rankings.delete_many({"admin_id": data.admin_id})

    new_rankings = [] ## create new rankings 
    for r in data.list_of_rankings:
        applicant = applicants.find_one({"name": r.applicant_name})
        if not applicant:
            raise HTTPException(status_code=404, detail=f"Applicant '{r.applicant_name}' not found")
        new_rankings.append({
            "admin_id": data.admin_id,
            "applicant_id": applicant["applicant_id"],
            "rank": r.rank
        })

    if new_rankings:
        rankings.insert_many(new_rankings)
    admin["has_given_pref"] = True
    return {"message": "Rankings submitted successfully!"}


@router.get("/admin_rankings_by_admin/{admin_id}")
def view_admin_rankings(admin_id: str):
    try:
        admin_id_int = int(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    rankings = list(db["admin_rankings"].find({"admin_id": admin_id_int}))
    return rankings
