"""
Employee Records Tools
========================
Tools for querying and searching the employee database via MongoDB.
"""

import json
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class GetEmployeeProfileInput(BaseModel):
    employee_id: str = Field(
        ...,
        description="The employee ID to look up (e.g., 'EMP-001')",
    )

class SearchEmployeesInput(BaseModel):
    query: str = Field(
        default="",
        description="Search query — matches against name, department, position, or email",
    )
    department: Optional[str] = Field(
        default=None,
        description="Filter by department name",
    )
    status: Optional[str] = Field(
        default=None,
        description="Filter by employment status: 'Active' or 'Inactive'",
    )

@tool(args_schema=GetEmployeeProfileInput)
async def get_employee_profile(employee_id: str) -> str:
    """Retrieve the full profile of a specific employee by their Employee ID."""
    db = get_db()
    employee = await db.employees.find_one({"id": employee_id.upper()}, {"_id": 0})

    if not employee:
        return json.dumps(
            {"success": False, "message": f"No employee found with ID '{employee_id}'."},
            indent=2,
        )

    return json.dumps(
        {"success": True, "employee": employee},
        indent=2,
    )

@tool(args_schema=SearchEmployeesInput)
async def search_employees(
    query: str = "",
    department: Optional[str] = None,
    status: Optional[str] = None,
) -> str:
    """Search the employee directory by name, department, position, or email."""
    db = get_db()
    
    # Build filter
    filter_query = {}
    if query:
        q = query
        filter_query["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"department": {"$regex": q, "$options": "i"}},
            {"position": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}},
        ]
    
    if department:
        filter_query["department"] = {"$regex": department, "$options": "i"}
        
    if status:
        filter_query["status"] = {"$regex": status, "$options": "i"}

    cursor = db.employees.find(filter_query, {"_id": 0})
    results = await cursor.to_list(length=100)

    return json.dumps(
        {"total": len(results), "employees": results},
        indent=2,
    )
