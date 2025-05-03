from models import Building
from database import SessionLocal

def seed_initial_buildings():
    db = SessionLocal()
    try:
        # Check if buildings already exist
        if db.query(Building).first():
            print("Buildings already seeded.")
            return

        # List of initial buildings
        initial_buildings = [
            {"name": "DFRV", "ra_needed": 1},
            {"name": "Halls", "ra_needed": 1},
            {"name": "Towers", "ra_needed": 1},
        ]

        # Add buildings to the database
        for building in initial_buildings:
            db.add(Building(name=building["name"], ra_needed=building["ra_needed"]))

        db.commit()

        # get all buildings to verify
        buildings = db.query(Building).all()
        for building in buildings:
            print(f"Building Name: {building.name}, RA Needed: {building.ra_needed}, {building.id}")

        print("Initial buildings seeded successfully.")
    finally:
        db.close()