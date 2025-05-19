from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utlils import get_db
from ..models import Building

router = APIRouter()


@router.get("/buildings/")
def get_buildings(db: Session = Depends(get_db)):
    buildings = db["applicants"]
    list_of_buildings = buildings.find_one({})
    if not list_of_buildings:
        HTTPException(500, "Internal Server Error")

    return list_of_buildings
