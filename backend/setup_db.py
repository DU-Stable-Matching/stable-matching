from api.models import Building, Admin
from api.utlils import get_password_hash
from api.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def db_setup_admin(buidling_ids: list[int]):
    db = SessionLocal()
    print(buidling_ids)
    try:
        logger.info("🚀 Starting admin database setup.")

        initial_admins = [
            {
                "du_id": "admin1",
                "name": "Admin One",
                "email": "admin1@example.com",
                "password": "password1",  # In production, use proper hashing
            },
            {
                "du_id": "admin2",
                "name": "Admin Two",
                "email": "admin2@example.com",
                "password": "password2",
            },
            {
                "du_id": "admin3",
                "name": "Admin Three",
                "email": "admin3@example.com",
                "password": "password3",
            },
            {
                "du_id": "admin4",
                "name": "Admin Four",
                "email": "admin4@example.com",
                "password": "password4",
            },
            {
                "du_id": "admin5",
                "name": "Admin Five",
                "email": "admin5@example.com",
                "password": "password5",
            },
            {
                "du_id": "admin6",
                "name": "Admin Six",
                "email": "admin6@example.com",
                "password": "password6",
            },
        ]

        admins: list[Admin] = []
        for i in range(len(initial_admins)):
            admin = initial_admins[i]
            # check if admin already exists
            existing_admin = (
                db.query(Admin).filter(Admin.du_id == admin["du_id"]).first()
            )
            if existing_admin:
                logger.info(f"⚠️ Admin {admin['name']} already exists. Skipping.")
                continue

            logger.info(f"✅ Adding admin: {admin['name']}")

            building = db.query(Building).filter(Building.id == buidling_ids[i]).first()
            if not building:
                logger.warning(
                    f"⚠️ No building found for admin {admin['name']}. Skipping."
                )
                continue

            existing_admin = (
                db.query(Admin).filter(Admin.du_id == admin["du_id"]).first()
            )
            if existing_admin:
                logger.info(f"⚠️ Admin {admin['name']} already exists. Skipping.")
                continue

            admins.append(
                Admin(
                    du_id=admin["du_id"],
                    name=admin["name"],
                    email=admin["email"],
                    password=get_password_hash(admin["password"]),
                    building=building,
                    given_preferences=False,
                    rankings=[]
                )
            )
            db.add(admins[-1])
            logger.info(f"✅ Admin {admin['name']} added successfully.")

        db.commit()
        logger.info("✅ Admins committed to the database.")

        for admin in admins:
            db.refresh(admin)
            logger.info(
                f"🆔 Admin ID: {admin.id}, Name: {admin.name}, Email: {admin.email}"
            )

        logger.info("🎉 Admin database setup completed successfully.")

    except Exception as e:
        logger.error(f"❌ An error occurred during admin database setup: {e}")
        db.rollback()
        raise

    finally:
        db.close()
        logger.info("✅ Database session closed.")


def setup_database_building():
    db = SessionLocal()
    try:
        logger.info("✅ Starting database setup.")

        initial_buildings = [
            {"name": "Halls", "ra_needed": 1},
            {"name": "Towers", "ra_needed": 1},
            {"name": "JMAC", "ra_needed": 1},
            {"name": "DFRV", "ra_needed": 1},
            {"name": "Nelson/Nagel", "ra_needed": 1},
            {"name": "Apartments", "ra_needed": 1},
        ]

        buildings = []
        for building in initial_buildings:
            # check if building already exists
            existing_building = (
                db.query(Building).filter(Building.name == building["name"]).first()
            )
            if existing_building:
                logger.info(f"⚠️ Building {building['name']} already exists. Skipping.")
                continue
            logger.info(f"✅ Adding building: {building['name']}")
            buildings.append(
                Building(name=building["name"], ra_needed=building["ra_needed"])
            )
            db.add(buildings[-1])

        db.commit()
        logger.info("✅ Initial buildings committed to the database.")

        building_ids = []
        buildings = db.query(Building).all()
        for building in buildings:
            building_ids.append(building.id)
            logger.info(f"🏢 Building ID: {building.id}, Name: {building.name}")

        logger.info("✅ Database setup completed successfully.")
        return building_ids

    except Exception as e:
        logger.error(f"❌ An error occurred during database setup: {e}")
        db.rollback()
        raise

    finally:
        db.close()
        logger.info("✅ Database session closed.")


def main():
    building_ids = setup_database_building()
    db_setup_admin(building_ids)
    logger.info("Database setup completed.")


if __name__ == "__main__":
    main()
