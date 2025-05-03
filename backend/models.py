from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Applicant(Base):
    __tablename__ = "applications"

    du_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    year_in_college = Column(Integer, nullable=True)
    is_returner = Column(Boolean, nullable=True)
    why_ra = Column(String, nullable=True)
    resume_path = Column(String, nullable=True)

    preferences = relationship("BuildingPreference", back_populates="applicant", cascade="all, delete")

class BuildingPreference(Base):
    __tablename__ = "building_preferences"

    id = Column(Integer, primary_key=True)
    building_name = Column(String)
    rank = Column(Integer)

    applicant_du_id = Column(String, ForeignKey("applications.du_id"))
    applicant = relationship("Applicant", back_populates="preferences")
