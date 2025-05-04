from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# ----------------------------------ADMIN SCHEMAS--------------------------------
class AdminLogin(BaseModel):
    du_id: str
    password: str
    model_config = ConfigDict(from_attributes=True)


class AdminPref(BaseModel):
    applicant_name: str
    rank: int


class AdminRankingCreate(BaseModel):
    admin_id: int
    list_of_rankings: List[AdminPref]


class BuildingCreate(BaseModel):
    name: str
    ra_needed: int
    boss_du_id: Optional[str]


class BuildingRead(BuildingCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ----------------------------------USER SCHEMAS--------------------------------
class BuildingPref(BaseModel):
    building_name: str
    rank: int


class UserCreate(BaseModel):
    du_id: str
    name: str
    email: str
    password: str
    year_in_college: Optional[int] = None


class UserLogin(BaseModel):
    du_id: str
    password: str


class UserRead(UserCreate):
    year_in_college: Optional[int] = None
    is_returner: Optional[bool] = None
    why_ra: Optional[str] = None
    resume_path: Optional[str] = None
    preferences: List[BuildingPref] = []
    model_config = ConfigDict(from_attributes=True)


class RAAppCreate(BaseModel):
    id: int
    is_returner: bool
    why_ra: str
    preferences: List[BuildingPref]
