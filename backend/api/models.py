from pydantic import BaseModel, ConfigDict


class Applicant(BaseModel):
    applicant_id: int
    du_id: str
    name: str
    email: str
    password: str
    year_in_college: int
    is_returner: bool
    resume_path: str
    pref: list[int]


class Admin(BaseModel):
    admin_id: int
    ad_du_id: str
    name: str
    email: str
    password: str
    building: int
    pref: list[list[int]] # list of applicant ids, each sublist represents applicants for a given preference level equal to the index of the sublist


class Building(BaseModel):
    build_id: int
    building_name: str
    ra_needed: int
    admin_id: int
