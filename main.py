# user-management-service/main.py

from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import httpx

load_dotenv()

app = FastAPI()

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Service URLs
INCIDENT_MANAGEMENT_URL = os.getenv("INCIDENT_MANAGEMENT_URL")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user-management")
async def user_management_root():
    return {"message": "User Management Blue Green"}

@app.get("/user-management/health")
async def health():
    return {"status": "OK"}

@app.get("/user-management/db-test")
async def test_db_connection(db: SessionLocal = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        return {"message": "Database connection successful", "result": result.scalar()}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/user-management/create-incident/{user_id}")
async def create_incident(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{INCIDENT_MANAGEMENT_URL}/incidents", json={"user_id": user_id})
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)