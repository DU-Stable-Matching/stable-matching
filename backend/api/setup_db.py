from .models import Building, Admin
from .utlils import get_password_hash
from .database import SessionLocal


def seed_initial_buildings():
    db = SessionLocal()
    try:
        # Check if buildings already exist
        if db.query(Building).first():
            print("Buildings already seeded.")
            return

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
        ]
        admins: list[Admin] = []
        for admin in initial_admins:
            # Check if admin already exists
            admins.append(
                Admin(
                    du_id=admin["du_id"],
                    name=admin["name"],
                    email=admin["email"],
                    password=get_password_hash(admin["password"]),
                )
            )
            db.add(admins[-1])
        db.commit()

        for admin in admins:
            db.refresh(admin)

        initial_buildings = [
            {"name": "DFRV", "ra_needed": 1, "boss_id": admins[0].id},
            {"name": "Halls", "ra_needed": 1, "boss_id": admins[1].id},
            {"name": "Towers", "ra_needed": 1, "boss_id": admins[2].id},
        ]

        buildings = []
        for building in initial_buildings:
            buildings.append(
                Building(
                    name=building["name"],
                    ra_needed=building["ra_needed"],
                    boss_id=building["boss_id"],
                )
            )
            db.add(buildings[-1])

        db.commit()

        buildings = db.query(Building).all()
        for building in buildings:
            print(
                f"Building Name: {building.name}, RA Needed: {building.ra_needed}, {building.id}"
            )

        print("Initial buildings seeded successfully.")
    finally:
        db.close()
