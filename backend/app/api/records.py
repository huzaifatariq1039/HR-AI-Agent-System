from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.db import get_db

router = APIRouter()

@router.get("/employees")
async def list_employees(
    query: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None
):
    db = get_db()
    filter_query = {}
    if query:
        filter_query["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"department": {"$regex": query, "$options": "i"}},
            {"position": {"$regex": query, "$options": "i"}},
            {"email": {"$regex": query, "$options": "i"}},
        ]
    if department:
        filter_query["department"] = {"$regex": department, "$options": "i"}
    if status:
        filter_query["status"] = {"$regex": status, "$options": "i"}
        
    cursor = db.employees.find(filter_query, {"_id": 0})
    results = await cursor.to_list(length=100)
    return results

@router.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    db = get_db()
    employee = await db.employees.find_one({"id": employee_id.upper()}, {"_id": 0})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
