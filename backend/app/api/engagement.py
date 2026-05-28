from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_recognitions():
    db = get_db()
    cursor = db.recognitions.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.post("/")
async def send_recognition(rec: dict):
    db = get_db()
    await db.recognitions.insert_one(rec)
    rec.pop("_id", None)
    return rec
