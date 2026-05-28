from fastapi import APIRouter, HTTPException
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_goals():
    db = get_db()
    cursor = db.goals.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.get("/{employee_id}")
async def get_goals(employee_id: str):
    db = get_db()
    data = await db.goals.find_one({"employee_id": employee_id.upper()}, {"_id": 0})
    if not data:
        raise HTTPException(status_code=404, detail="Goals not found")
    return data
