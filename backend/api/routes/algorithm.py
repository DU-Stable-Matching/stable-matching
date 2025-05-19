from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..utlils import get_preferences
from ..models import Applicant, FinalMatching, Building, Admin
from ..mongo import get_db
from ..logic import get_matching
from pymongo.collection import Collection
from ..schemas import matchApplicant, matchBuilding

router = APIRouter()


def populate_matches(matches: list[tuple[int, int]], db: Session):
    db.query(FinalMatching).delete()

    for applicant_id, building_id in matches:
        match = FinalMatching(applicant_id=applicant_id, building_id=building_id)
        db.add(match)

    db.commit()


def get_building(building_id: int, db: Depends(get_db)):
    buildings: Collection = db["buildings"]
    building = buildings.find_one({"building_id": building_id})
    if not building:
        raise Exception("could not retrieve Building")

    return building


def get_applicant(applicant_id: int, db: Depends(get_db)):
    applicants: Collection = db["Applicant"]
    applicant = applicants.find_one({"building_id": applicant_id})
    if not applicant:
        raise Exception("could not retrieve applicant")

    return applicant


@router.get("/user_algorithm/{user_id}", response_model=matchBuilding)
def run_algorithm(user_id: int, db: Session = Depends(get_db)):
    try:
        user_pref, admin_pref = get_preferences()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch preferences: {str(e)}"
        )

    if len(admin_pref) != len(user_pref):  # users haven't filled out their preferences
        raise HTTPException(
            status_code=400,
            detail="Mismatch in number of preferences between admins and applicants.",
        )

    for i in range(len(admin_pref)):
        if len(admin_pref[i][1]) == 0 or len(user_pref[i][1]) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"Admin admin_pref[{i}][0] hasn't provided ranking.",
            )

    matching = (
        db.query(FinalMatching).filter(FinalMatching.applicant_id == user_id).first()
    )

    if not matching:
        # run the algorithm and save the results
        applicants_matched_to_buildings = get_matching(user_pref, admin_pref)
        if not applicants_matched_to_buildings:
            raise HTTPException(
                status_code=500, detail="Algorithm failed to find a matching."
            )

        populate_matches(applicants_matched_to_buildings, db)

        matching = (
            db.query(FinalMatching)
            .filter(FinalMatching.applicant_id == user_id)
            .first()
        )

        return get_building(matching.building_id, db)
    else:
        # return the building name
        return get_building(matching.building_id, db)


@router.get("/admin_algorithm/{admin_id}", response_model=matchApplicant)
def run_algorithm(admin_id: int, db: Session = Depends(get_db)):
    # Fetch preferences from the database
    try:
        user_pref, admin_pref = get_preferences()
        applicants_matched_to_buildings = get_matching(user_pref, admin_pref)
        # print("Applicants matched to buildings:", applicants_matched_to_buildings)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch preferences: {str(e)}"
        )

    if len(admin_pref) != len(user_pref):  # users haven't filled out their preferences
        raise HTTPException(
            status_code=400,
            detail="Mismatch in number of preferences between admins and applicants.",
        )

    for i in range(len(admin_pref)):
        if len(admin_pref[i][1]) == 0 or len(user_pref[i][1]) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"Admin admin_pref[{i}][0] hasn't provided ranking.",
            )

    matching = (
        db.query(FinalMatching).filter(FinalMatching.building_id == admin_id).first()
    )
    if not matching:
        # run the algorithm and save the results
        applicants_matched_to_buildings = get_matching(user_pref, admin_pref)
        if not applicants_matched_to_buildings:
            raise HTTPException(
                status_code=500, detail="Algorithm failed to find a matching."
            )

        populate_matches(applicants_matched_to_buildings, db)

        matching = (
            db.query(FinalMatching)
            .filter(FinalMatching.building_id == admin_id)
            .first()
        )

        return get_applicant(matching.applicant_id, db)
    else:

        return get_applicant(matching.applicant_id, db)
