from fastapi import APIRouter, HTTPException
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_onboarding():
    db = get_db()
    cursor = db.onboarding.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.get("/{employee_id}")
async def get_onboarding_status(employee_id: str):
    db = get_db()
    record = await db.onboarding.find_one({"employee_id": employee_id.upper()}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="Onboarding record not found")
    return record
