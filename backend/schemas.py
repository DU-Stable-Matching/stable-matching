from pydantic import BaseModel
from typing import List, Optional

class BuildingPref(BaseModel):
    building_name: str
    rank: int

class UserCreate(BaseModel):
    du_id: str
    name: str
    email: str

class UserRead(UserCreate):
    year_in_college: Optional[int] = None
    is_returner: Optional[bool] = None
    why_ra: Optional[str] = None
    resume_path: Optional[str] = None
    preferences: List[BuildingPref] = []

    class Config:
        orm_mode = True

class RAAppCreate(BaseModel):
    du_id: str
    year_in_college: int
    is_returner: bool
    why_ra: str
    preferences: List[BuildingPref]
