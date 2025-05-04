from fastapi import FastAPI, HTTPException
from .database import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from .routes import applicant, building, admin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for any endpoint
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the user routes
app.include_router(applicant.router, prefix="/api", tags=["user"])
app.include_router(building.router, prefix="/api", tags=["building"])
app.include_router(admin.router, prefix="/api", tags=["admin"])


@app.delete("/reset-database/")
def reset_database():
    try:
        # Drop all tables known to Base
        Base.metadata.drop_all(bind=engine)
        # Re-create all tables
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        # Return a 500 if anything goes wrong
        raise HTTPException(status_code=500, detail=f"Failed to reset database: {e}")
    return {"message": "Database reset successfully!"}
