from fastapi import APIRouter, HTTPException
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_policies():
    db = get_db()
    cursor = db.policies.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.get("/{policy_key}")
async def get_policy(policy_key: str):
    db = get_db()
    key = policy_key.lower().replace(" ", "_").replace("-", "_")
    policy = await db.policies.find_one({"key": key}, {"_id": 0})
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
