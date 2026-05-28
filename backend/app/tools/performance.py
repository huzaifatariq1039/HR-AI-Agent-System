"""
Performance Management Tools
===============================
Tools for tracking employee goals, OKRs, and performance metrics via MongoDB.
"""

import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class GetGoalsInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g., 'EMP-001')")

@tool(args_schema=GetGoalsInput)
async def get_goals(employee_id: str) -> str:
    """Retrieve the performance goals and OKRs for a specific employee.

    Use this tool when someone asks about an employee's goals, objectives, key results,
    OKRs, performance targets, or what someone is working toward.
    """
    db = get_db()
    data = await db.goals.find_one({"employee_id": employee_id.upper()}, {"_id": 0})
    if not data:
        return json.dumps({"success": False, "message": f"No goals found for '{employee_id}'."}, indent=2)
    return json.dumps({"success": True, "performance": data}, indent=2)
