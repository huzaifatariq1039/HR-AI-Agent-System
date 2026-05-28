from fastapi import APIRouter, HTTPException
from app.db import get_db

router = APIRouter()

@router.get("/")
async def get_metrics():
    db = get_db()
    metrics = await db.metrics.find_one({"id": "latest_metrics"}, {"_id": 0})
    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics
