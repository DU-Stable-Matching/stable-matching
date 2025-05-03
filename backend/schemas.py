from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class RAAppCreate(BaseModel):
    du_id: str
    year_in_college: int
    is_returner: bool
    why_ra: str
    preferences: List[BuildingPref]

class AdminCreate(BaseModel):
    du_id: str
    name: str
    email: str
    building_name: str  

    model_config = ConfigDict(from_attributes=True)

class AdminRead(AdminCreate):
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

#----------------------------------ADMIN SCHEMAS--------------------------------
class AdminRankingCreate(BaseModel):
    admin_du_id: str
    applicant_du_id: str
    rank: int

class BuildingCreate(BaseModel):
    name: str
    ra_needed: int
    boss_du_id: Optional[str]

class BuildingRead(BuildingCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
