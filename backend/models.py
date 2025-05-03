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

class Admin(Base):
    __tablename__ = "admins"

    du_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

    building_name = Column(String, ForeignKey("buildings.name"))
    
    building = relationship("Building", back_populates="admin", foreign_keys=[building_name])
    # Restore this relationship!
    rankings = relationship("AdminRanking", back_populates="admin", cascade="all, delete")



class AdminRanking(Base):
    __tablename__ = "admin_rankings"

    id = Column(Integer, primary_key=True)
    applicant_du_id = Column(String, ForeignKey("applications.du_id"))
    admin_du_id = Column(String, ForeignKey("admins.du_id"))
    rank = Column(Integer)

    admin = relationship("Admin", back_populates="rankings")
    applicant = relationship("Applicant")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer)
    name = Column(String, unique=True, primary_key=True)
    ra_needed = Column(Integer)
    boss_du_id = Column(String, ForeignKey("admins.du_id"))

    admin = relationship("Admin", back_populates="building", uselist=False, foreign_keys=[boss_du_id])

