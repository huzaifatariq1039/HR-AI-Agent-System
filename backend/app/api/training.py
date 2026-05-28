from fastapi import APIRouter, Query
from typing import Optional
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_programs(category: Optional[str] = None):
    db = get_db()
    filter_query = {}
    if category:
        filter_query["category"] = {"$regex": category, "$options": "i"}
        
    cursor = db.training_programs.find(filter_query, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results
