"""
MongoDB bootstrap script
------------------------
Creates unique indexes for the *matching* database and loads
seed data from **dummy.json**.

Adds structured logging so that every significant step is recorded.
"""

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient, errors

# ---------------------------------------------------------------------------
# 🔧  Configuration & logger setup
# ---------------------------------------------------------------------------

# Configure application-wide logging
logging.basicConfig(
    level=logging.INFO,  # Switch to DEBUG for more detail
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env (if present)
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    logger.error("Environment variable MONGO_URL is not set. Aborting start-up.")
    raise EnvironmentError("Required env var MONGO_URL is missing.")

# Eagerly validate the connection so that failures happen up front
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    logger.info("✅  Connected to MongoDB at %s", MONGO_URL)
except errors.ServerSelectionTimeoutError as exc:
    logger.exception("❌  Unable to reach MongoDB: %s", exc)
    raise

# ---------------------------------------------------------------------------
# 📚  Helpers
# ---------------------------------------------------------------------------


def setup_index() -> None:
    """
    Ensure each collection has a unique index on its primary identifier.
    """
    logger.info("Creating unique indexes …")
    db = client.matching

    db["applicants"].create_index("applicant_id", unique=True)
    logger.debug("Index created: applicants.applicant_id")

    db["admins"].create_index("admin_id", unique=True)
    logger.debug("Index created: admins.admin_id")

    db["buildings"].create_index("building_id", unique=True)
    logger.debug("Index created: buildings.building_id")

    logger.info("Indexes finished ✅")


def insert_dummy_data(filepath: str = "dummy.json") -> None:
    """
    Wipe the three collections and repopulate them with data from *dummy.json*.

    The JSON file **must** be a list with three top-level arrays in the order:
    0 → applicants, 1 → admins, 2 → buildings.
    """
    logger.info("Loading dummy data from %s …", filepath)

    path = Path(filepath)
    if not path.exists():
        logger.error("File not found: %s", filepath)
        raise FileNotFoundError(filepath)

    with path.open("r", encoding="utf-8") as fp:
        dummy_data = json.load(fp)

    if len(dummy_data) != 3:
        logger.error(
            "Expected 3 top-level arrays in dummy.json, found %d.", len(dummy_data)
        )
        raise ValueError("Invalid structure in dummy.json")

    db = client.matching
    applicants, admins, buildings = (
        db["applicants"],
        db["admins"],
        db["buildings"],
    )

    # Populate collections in the same order as the JSON arrays
    for idx in range(len(dummy_data)):
        match idx:
            case 0:
                logger.info("Refreshing *applicants* collection …")
                applicants.delete_many({})
                result = applicants.insert_many(dummy_data[idx])
                logger.debug(
                    "Inserted %d applicant documents.", len(result.inserted_ids)
                )
            case 1:
                logger.info("Refreshing *admins* collection …")
                admins.delete_many({})
                result = admins.insert_many(dummy_data[idx])
                logger.debug("Inserted %d admin documents.", len(result.inserted_ids))
            case 2:
                logger.info("Refreshing *buildings* collection …")
                buildings.delete_many({})
                result = buildings.insert_many(dummy_data[idx])
                logger.debug(
                    "Inserted %d building documents.", len(result.inserted_ids)
                )
            case _:
                logger.error("Unexpected index %d while processing dummy.json", idx)
                raise ValueError("Unexpected data block in dummy.json")

    logger.info("Dummy data loaded successfully ✅")


# ---------------------------------------------------------------------------
# 🚀  Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    logger.info("🏁  Starting database bootstrap.")
    setup_index()
    insert_dummy_data()
    logger.info("🎉  Database bootstrap completed.")


if __name__ == "__main__":
    main()
