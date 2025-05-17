from pydantic import BaseModel, ConfigDict


class Applicant(BaseModel):
    id: int
    du_id: str
    name: str
    email: str
    password: str
    year_in_college: int
    is_returner: bool
    resume_path: str
    pref: list[int]


class Admin(BaseModel):
    id: int
    ad_du_id: str
    name: str
    email: str
    password: str
    building: int
    pref: list[list[int]]


class Building(BaseModel):
    id: int
    building_name: str
    ra_needed: int
    admin_id: int
