from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.db import get_db
import json

router = APIRouter()

@router.get("/jobs")
async def list_jobs(status: Optional[str] = None, department: Optional[str] = None):
    db = get_db()
    filter_query = {}
    if status:
        filter_query["status"] = {"$regex": status, "$options": "i"}
    if department:
        filter_query["department"] = {"$regex": department, "$options": "i"}
        
    cursor = db.job_postings.find(filter_query, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.post("/jobs")
async def create_job(job: dict):
    db = get_db()
    await db.job_postings.insert_one(job)
    job.pop("_id", None)
    return job
