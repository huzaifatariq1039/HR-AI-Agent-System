from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.db import get_db

router = APIRouter()

@router.get("/")
async def list_payslips():
    db = get_db()
    cursor = db.payslips.find({}, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.get("/{employee_id}")
async def get_payslip(employee_id: str, pay_period: str = "May 2026"):
    db = get_db()
    payslip = await db.payslips.find_one({
        "employee_id": employee_id.upper(),
        "pay_period": pay_period
    }, {"_id": 0})
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return payslip
