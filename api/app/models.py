from pydantic import BaseModel, ConfigDict


class Applicant(BaseModel):
    applicant_id: int
    du_id: str
    name: str
    email: str
    password: str
    year_in_college: int
    is_returner: bool | None
    resume_path: str | None
    pref: list[int] | None
    has_given_pref: bool = False


class Admin(BaseModel):
    admin_id: int
    ad_du_id: str
    name: str
    email: str
    password: str
    building: int
    pref: list[list[int]] # list of applicant ids, each sublist represents applicants for a given preference level equal to the index of the sublist
    has_given_pref: bool = False


class Building(BaseModel):
    build_id: int
    building_name: str
    ra_needed: int
    admin_id: int


class FinalMatching(BaseModel):
    admin_id: int
    applicant_id: int
