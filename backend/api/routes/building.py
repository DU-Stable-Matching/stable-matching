from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utlils import get_db
from ..models import Building

router = APIRouter()


@router.get("/buildings/")
def get_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    result = []
    for building in buildings:
        result.append(
            {
                "id": building.id,
                "name": building.name,
                "ra_needed": building.ra_needed,
                "boss_du_id": building.boss_du_id,
            }
        )
    return result
