from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..utlils import get_preferences, get_db
from ..models import Applicant, FinalMatching, Building
from ..logic import get_matching

router = APIRouter()

def populate_matches(matches: list[tuple[int, int]], db: Session):
    db.query(FinalMatching).delete()
    
    for applicant_id, building_id in matches:
        match = FinalMatching(applicant_id=applicant_id, building_id=building_id)
        db.add(match)

    db.commit()

def get_building_name(building_id: int, db: Session):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building.name

def get_applicant_name(applicant_id: int, db: Session):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    # print(applicant.name)
    return applicant.name


@router.get("/user_algorithm/{user_id}", response_model=str)
def run_algorithm(user_id: int, db: Session = Depends(get_db)):
    try:
        user_pref, admin_pref = get_preferences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch preferences: {str(e)}")
    

    if len(admin_pref) != len(user_pref): #users haven't filled out their preferences
        raise HTTPException(status_code=400, detail="Mismatch in number of preferences between admins and applicants.")
    
    for i in range(len(admin_pref)):
        if len(admin_pref[i][1]) == 0:
            raise HTTPException(status_code=400, detail="Admin {admin_pref[i][0]} hasn't provided ranking.")
    
    matching = db.query(FinalMatching).filter(FinalMatching.applicant_id == user_id).first()

    if not matching:
        #run the algorithm and save the results 
        applicants_matched_to_buildings = get_matching(user_pref, admin_pref)
        if not applicants_matched_to_buildings:
            raise HTTPException(status_code=500, detail="Algorithm failed to find a matching.")
        
        populate_matches(applicants_matched_to_buildings, db)

        matching = db.query(FinalMatching).filter(FinalMatching.applicant_id == user_id).first()

        return get_building_name(matching.building_id, db)
    else: 
        #return the building name
        return get_building_name(matching.building_id, db)
    

@router.get("/admin_algorithm/{admin_id}", response_model=str)
def run_algorithm(admin_id: int, db: Session = Depends(get_db)):
    # Fetch preferences from the database
    try:
        user_pref, admin_pref = get_preferences()
        applicants_matched_to_buildings = get_matching(user_pref, admin_pref)
        # print("Applicants matched to buildings:", applicants_matched_to_buildings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch preferences: {str(e)}")
    

    if len(admin_pref) != len(user_pref): #users haven't filled out their preferences
        raise HTTPException(status_code=400, detail="Mismatch in number of preferences between admins and applicants.")
    
    for i in range(len(admin_pref)):
        if len(admin_pref[i][1]) == 0:
            raise HTTPException(status_code=400, detail="Admin {admin_pref[i][0]} hasn't provided ranking.")
        
    matching = db.query(FinalMatching).filter(FinalMatching.building_id == admin_id).first()
    if not matching:
        #run the algorithm and save the results 
        applicants_matched_to_buildings = get_matching(user_pref, admin_pref)
        if not applicants_matched_to_buildings:
            raise HTTPException(status_code=500, detail="Algorithm failed to find a matching.")
        
        populate_matches(applicants_matched_to_buildings, db)

        matching = db.query(FinalMatching).filter(FinalMatching.building_id == admin_id).first()
    
        return get_applicant_name(matching.applicant_id, db)
    else: 
        #return the building name
        # print(f" building to applicant:", matching.building_id, " ", matching.applicant_id)
        return get_applicant_name(matching.applicant_id, db)
    
    



