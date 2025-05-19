from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import joinedload
from ..utlils import get_password_hash, verify_password, db
from ..models import Admin, Building, Applicant
from ..schemas import AdminLogin, AdminRankingCreate

router = APIRouter()


@router.post("/admin_login/")
def admin_login(admin: AdminLogin):
    db_admin = db.query(Admin).filter(Admin.du_id == admin.du_id).first()
    if not db_admin:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(admin.password, db_admin.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful!", "id": db_admin.id}


@router.get("/admin/{admin_id}")
def get_admin(admin_id: str):
    admin_db = (
        db.query(Admin)
        .options(joinedload(Admin.buildings))
        .filter(Admin.id == admin_id)
        .first()
    )
    if not admin_db:
        raise HTTPException(status_code=404, detail="Building not found")

    return admin_db


@router.get("/admin_given_preferences/{admin_id}")
def get_admin_given_preferences(admin_id: str):
    admin_db = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin_db:
        raise HTTPException(status_code=404, detail="Admin not found")

    return admin_db.given_preferences


@router.get("/get_all_admins/")
def get_all_admins():
    admins = db.query(Admin).options(joinedload(Admin.buildings)).all()
    if not admins:
        raise HTTPException(status_code=404, detail="No admins found")

    return admins


@router.post("/admin_rank/")
def admin_rank(data: AdminRankingCreate):
    admin = db.query(Admin).filter(Admin.id == data.admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    # Clear existing rankings
    db.query(AdminRanking).filter(AdminRanking.admin_id == data.admin_id).delete()

    for ranking in data.list_of_rankings:
        applicant = (
            db.query(Applicant).filter(Applicant.name == ranking.applicant_name).first()
        )
        new_ranking = AdminRanking(
            applicant_id=applicant.id,
            rank=ranking.rank,
            admin_id=data.admin_id,
        )
        db.add(new_ranking)

    admin.given_preferences = True
    db.commit()
    return {"message": "Rankings submitted successfully!"}


@router.get("/admin_rankings_by_admin/{admin_id}")
def view_admin_rankings(admin_id: int):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    rankings = db.query(AdminRanking).filter(AdminRanking.admin_id == admin_id).all()
    return rankings
