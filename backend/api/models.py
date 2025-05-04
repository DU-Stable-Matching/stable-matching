from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    du_id: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    name: Mapped[str]
    building: Mapped["Building"] = relationship(back_populates="boss")
    given_preferences: Mapped[bool] = mapped_column(default=False)

    rankings: Mapped[List["AdminRanking"]] = relationship(
        back_populates="admin", cascade="all, delete-orphan"
    )


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    ra_needed: Mapped[int]
    boss_id: Mapped[str] = mapped_column(ForeignKey("admins.id"), nullable=True)
    boss: Mapped["Admin"] = relationship(back_populates="building")


class AdminRanking(Base):
    __tablename__ = "admin_rankings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    applicant_id: Mapped[int]
    rank: Mapped[int]
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"))
    admin: Mapped["Admin"] = relationship(back_populates="rankings")


class Applicant(Base):
    __tablename__ = "applicants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    du_id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    year_in_college: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_returner: Mapped[Optional[bool]] = mapped_column(nullable=True)
    why_ra: Mapped[Optional[str]] = mapped_column(nullable=True)
    resume_path: Mapped[Optional[str]]
    preferences: Mapped[List["BuildingPref"]] = relationship(
        back_populates="applicant", cascade="all, delete-orphan"
    )
    given_preferences: Mapped[bool] = mapped_column(default=False)



class BuildingPref(Base):
    __tablename__ = "building_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    building_name: Mapped[str]
    rank: Mapped[int]
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))
    applicant: Mapped["Applicant"] = relationship(back_populates="preferences")

class FinalMatching(Base):
    __tablename__ = "final_matching"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))

    # applicant: Mapped["Applicant"] = relationship(back_populates="preferences")
    # building: Mapped["Building"] = relationship(back_populates="id")
