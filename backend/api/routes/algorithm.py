from fastapi import APIRouter, HTTPException
from ..utlils import get_preferences
from ..logic import get_matching



router = APIRouter()

@router.get("/algorithm/")
def run_algorithm():
    # Fetch preferences from the database
    try:
        admin_pref, user_pref = get_preferences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch preferences: {str(e)}")
    
    if len(admin_pref) != len(user_pref): #users haven't filled out their preferences
        raise HTTPException(status_code=400, detail="Mismatch in number of preferences between admins and applicants.")
    
    for i in len(admin_pref):
        if len(admin_pref[i][1]) == 0:
            raise HTTPException(status_code=400, detail="Admin {admin_pref[i][0]} hasn't provided ranking.")

    # Runint algo
    applicants_matched_to_buildings = get_matching(admin_pref, user_pref)
    if not applicants_matched_to_buildings:
        raise HTTPException(status_code=500, detail="Algorithm failed to find a matching.")
   
    return {"message": "Algorithm executed successfully!", "result": applicants_matched_to_buildings}
