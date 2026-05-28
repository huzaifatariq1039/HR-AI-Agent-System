from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_grievances():
    db = get_db()
    cursor = db.grievances.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.post("/")
async def file_grievance(grievance: dict):
    db = get_db()
    await db.grievances.insert_one(grievance)
    grievance.pop("_id", None)
    return grievance
