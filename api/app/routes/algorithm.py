from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import joinedload
from ..utlils import get_preferences, db as session_db
from ..models import Applicant, FinalMatching, Building, Admin
from ..mongo import db as mongo_db
from ..logic import get_matching
from pymongo.collection import Collection
from ..schemas import matchApplicant, matchBuilding

router = APIRouter()


def populate_matches(matches: list[tuple[int, int]]):
    # Clear all existing final matchings
    session_db.query(FinalMatching).delete()
    for applicant_id, building_id in matches:
        match = FinalMatching(applicant_id=applicant_id, building_id=building_id)
        session_db.add(match)
    session_db.commit()


def get_building(building_id: int):
    buildings: Collection = mongo_db["buildings"]
    building = buildings.find_one({"building_id": building_id})
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


def get_applicant(applicant_id: int):
    applicants: Collection = mongo_db["applicants"]
    applicant = applicants.find_one({"applicant_id": applicant_id})
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant


@router.get("/user_algorithm/{user_id}", response_model=matchBuilding)
def run_applicant_algorithm(user_id: int):
    # Fetch preferences
    try:
        user_pref, admin_pref = get_preferences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch preferences: {e}")

    if len(admin_pref) != len(user_pref):
        raise HTTPException(
            status_code=400,
            detail="Mismatch in number of preferences between admins and applicants.",
        )

    for i in range(len(admin_pref)):
        if not admin_pref[i][1] or not user_pref[i][1]:
            raise HTTPException(
                status_code=400,
                detail=f"Admin {admin_pref[i][0]} or applicant {user_pref[i][0]} hasn't provided ranking.",
            )

    # Check existing match
    existing = (
        session_db.query(FinalMatching)
        .filter(FinalMatching.applicant_id == user_id)
        .first()
    )
    if not existing:
        matches = get_matching(user_pref, admin_pref)
        if not matches:
            raise HTTPException(
                status_code=500, detail="Algorithm failed to find a matching."
            )
        populate_matches(matches)
        existing = (
            session_db.query(FinalMatching)
            .filter(FinalMatching.applicant_id == user_id)
            .first()
        )

    return get_building(existing.building_id)


@router.get("/admin_algorithm/{admin_id}", response_model=matchApplicant)
def run_admin_algorithm(admin_id: int):
    # Fetch preferences and run matching
    try:
        user_pref, admin_pref = get_preferences()
        matches = get_matching(user_pref, admin_pref)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch preferences: {e}")

    if len(admin_pref) != len(user_pref):
        raise HTTPException(
            status_code=400,
            detail="Mismatch in number of preferences between admins and applicants.",
        )

    for i in range(len(admin_pref)):
        if not admin_pref[i][1] or not user_pref[i][1]:
            raise HTTPException(
                status_code=400,
                detail=f"Admin {admin_pref[i][0]} or applicant {user_pref[i][0]} hasn't provided ranking.",
            )

    existing = (
        session_db.query(FinalMatching)
        .filter(FinalMatching.building_id == admin_id)
        .first()
    )
    if not existing:
        matches = get_matching(user_pref, admin_pref)
        if not matches:
            raise HTTPException(
                status_code=500, detail="Algorithm failed to find a matching."
            )
        populate_matches(matches)
        existing = (
            session_db.query(FinalMatching)
            .filter(FinalMatching.building_id == admin_id)
            .first()
        )

    return get_applicant(existing.applicant_id)
