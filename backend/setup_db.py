from api.models import Building, Admin, Applicant, AdminRanking, BuildingPref
from api.utlils import get_password_hash
from api.database import SessionLocal
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def db_setup_admin(building_ids: list[int]):
    db = SessionLocal()
    logger.info("🚀 Starting admin database setup.")

    initial_admins = [
        {
            "du_id": "admin1",
            "name": "Admin One",
            "email": "admin1@example.com",
            "password": "pass1",
        },
        {
            "du_id": "admin2",
            "name": "Admin Two",
            "email": "admin2@example.com",
            "password": "pass2",
        },
        {
            "du_id": "admin3",
            "name": "Admin Three",
            "email": "admin3@example.com",
            "password": "pass3",
        },
        {
            "du_id": "admin4",
            "name": "Admin Four",
            "email": "admin4@example.com",
            "password": "pass4",
        },
        {
            "du_id": "admin5",
            "name": "Admin Five",
            "email": "admin5@example.com",
            "password": "pass5",
        },
        {
            "du_id": "admin6",
            "name": "Admin Six",
            "email": "admin6@example.com",
            "password": "pass6",
        },
    ]

    for idx, admin_data in enumerate(initial_admins):
        if db.query(Admin).filter(Admin.du_id == admin_data["du_id"]).first():
            logger.info(f"⚠️ Admin {admin_data['name']} already exists. Skipping.")
            continue

        building = db.query(Building).filter(Building.id == building_ids[idx]).first()
        if not building:
            logger.warning(
                f"⚠️ No building found for admin {admin_data['name']}. Skipping."
            )
            continue

        admin = Admin(
            du_id=admin_data["du_id"],
            name=admin_data["name"],
            email=admin_data["email"],
            password=get_password_hash(admin_data["password"]),
            building=building,
            given_preferences=False,
            rankings=[],
        )
        db.add(admin)
        logger.info(f"✅ Admin {admin.name} added successfully.")

    db.commit()
    logger.info("✅ All admins committed to the database.")
    db.close()
    logger.info("✅ Admin setup complete. Database session closed.")


def setup_database_building():
    db = SessionLocal()
    logger.info("✅ Starting building database setup.")

    initial_buildings = [
        {"name": "Halls", "ra_needed": 1},
        {"name": "Towers", "ra_needed": 1},
        {"name": "JMAC", "ra_needed": 1},
        {"name": "DFRV", "ra_needed": 1},
        {"name": "Nelson/Nagel", "ra_needed": 1},
        {"name": "Apartments", "ra_needed": 1},
    ]

    for b in initial_buildings:
        if db.query(Building).filter(Building.name == b["name"]).first():
            logger.info(f"⚠️ Building {b['name']} already exists. Skipping.")
            continue
        building = Building(name=b["name"], ra_needed=b["ra_needed"])
        db.add(building)
        logger.info(f"✅ Building {b['name']} added.")

    db.commit()
    logger.info("✅ All buildings committed to the database.")

    building_ids = [b.id for b in db.query(Building).all()]
    db.close()
    logger.info("✅ Building setup complete. Database session closed.")
    return building_ids


def db_setup_applicants():
    db = SessionLocal()
    logger.info("🚀 Starting applicant database setup.")

    initial_applicants = [
        {
            "du_id": "student1",
            "name": "Alice Applicant",
            "email": "alice@applicant.com",
            "password": "pass1",
            "year_in_college": 1,
        },
        {
            "du_id": "student2",
            "name": "Bob Candidate",
            "email": "bob@candidate.edu",
            "password": "pass2",
            "year_in_college": 2,
        },
        {
            "du_id": "student3",
            "name": "Carol Student",
            "email": "carol@student.du.edu",
            "password": "pass3",
            "year_in_college": 3,
        },
        {
            "du_id": "student4",
            "name": "Dave Learner",
            "email": "dave@learner.edu",
            "password": "pass4",
            "year_in_college": 4,
        },
        {
            "du_id": "student5",
            "name": "Eve Enrollee",
            "email": "eve@enrollee.edu",
            "password": "pass5",
            "year_in_college": 1,
        },
        {
            "du_id": "student6",
            "name": "Frank Freshman",
            "email": "frank@freshman.edu",
            "password": "pass6",
            "year_in_college": 2,
        },
    ]

    for app_data in initial_applicants:
        if db.query(Applicant).filter(Applicant.du_id == app_data["du_id"]).first():
            logger.info(f"⚠️ Applicant {app_data['name']} already exists. Skipping.")
            continue

        applicant = Applicant(
            du_id=app_data["du_id"],
            name=app_data["name"],
            email=app_data["email"],
            password=get_password_hash(app_data["password"]),
            year_in_college=app_data["year_in_college"],
            given_preferences=False,
        )
        db.add(applicant)
        logger.info(f"✅ Applicant {applicant.name} added successfully.")

    db.commit()
    logger.info("✅ All applicants committed to the database.")
    db.close()
    logger.info("✅ Applicant setup complete. Database session closed.")


def setup_admin_rankings():
    db = SessionLocal()
    logger.info("🚀 Starting admin rankings setup.")
    for i in range(1, 6):
        admin = db.query(Admin).filter(Admin.id == i).first()
        # random rankings from 1 to 6
        ranks = [i for i in range(1, 7)]
        random.shuffle(ranks)
        for j, rank in enumerate(ranks):
            applicant = db.query(Applicant).filter(Applicant.id == j + 1).first()
            if not applicant:
                logger.warning(f"⚠️ No applicant found for ID {j + 1}. Skipping.")
                continue

            admin_ranking = AdminRanking(
                applicant_id=applicant.id,
                rank=rank,
                admin_id=admin.id,
            )
            db.add(admin_ranking)
            logger.info(
                f"✅ Admin {admin.name} ranked applicant {applicant.name} with rank {rank}."
            )
        admin.given_preferences = True
    db.commit()
    logger.info("✅ All rankings committed to the database.")
    db.close()


def setup_applicant_rankings():
    db = SessionLocal()
    logger.info("🚀 Starting applicant rankings setup.")
    for i in range(1, 6):
        applicant = db.query(Applicant).filter(Applicant.id == i).first()
        # random rankings from 1 to 6
        ranks = [i for i in range(1, 7)]
        random.shuffle(ranks)
        for j, rank in enumerate(ranks):
            building = db.query(Building).filter(Building.id == j + 1).first()
            if not building:
                logger.warning(f"⚠️ No building found for ID {j + 1}. Skipping.")
                continue

            building_pref = BuildingPref(
                building_name=building.name,
                rank=rank,
                applicant_id=applicant.id,
            )
            db.add(building_pref)
            logger.info(
                f"✅ Applicant {applicant.name} ranked building {building.name} with rank {rank}."
            )
        applicant.given_preferences = True
    db.commit()
    logger.info("✅ All rankings committed to the database.")
    db.close()


def main():
    building_ids = setup_database_building()
    db_setup_admin(building_ids)
    db_setup_applicants()
    setup_admin_rankings()
    setup_applicant_rankings()
    logger.info("🎉 Full database setup completed.")


if __name__ == "__main__":
    main()
