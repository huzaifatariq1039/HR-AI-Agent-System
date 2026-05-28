from fastapi import APIRouter, HTTPException
from app.db import get_db

router = APIRouter()

@router.get("/balances")
async def list_balances():
    db = get_db()
    cursor = db.leave_balances.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.get("/balances/{employee_id}")
async def get_balance(employee_id: str):
    db = get_db()
    balance = await db.leave_balances.find_one({"employee_id": employee_id.upper()}, {"_id": 0})
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@router.post("/requests")
async def create_request(req: dict):
    db = get_db()
    await db.leave_requests.insert_one(req)
    req.pop("_id", None)
    return req
