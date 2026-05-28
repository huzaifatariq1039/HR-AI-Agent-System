"""
Leave & Attendance Tools
==========================
Tools for managing leave requests and balances via MongoDB.
"""

import json
import uuid
from datetime import datetime
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class ApplyLeaveInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g., 'EMP-001')")
    leave_type: str = Field(..., description="Type: 'annual_leave', 'sick_leave', 'personal_leave', or 'parental_leave'")
    start_date: str = Field(..., description="Start date YYYY-MM-DD")
    end_date: str = Field(..., description="End date YYYY-MM-DD")
    reason: str = Field(default="", description="Reason for leave")

class GetLeaveBalanceInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g., 'EMP-001')")

@tool(args_schema=ApplyLeaveInput)
async def apply_leave(employee_id: str, leave_type: str, start_date: str, end_date: str, reason: str = "") -> str:
    """Submit a leave request for an employee.

    Use this tool to apply for leave, request time off, take vacation, or sick days.
    Validates balance and creates a pending request.
    """
    db = get_db()
    balance_data = await db.leave_balances.find_one({"employee_id": employee_id.upper()}, {"_id": 0})
    if not balance_data:
        return json.dumps({"success": False, "message": f"No employee found with ID '{employee_id}'."}, indent=2)

    if leave_type not in balance_data["balances"]:
        return json.dumps({"success": False, "message": f"Invalid leave type '{leave_type}'."}, indent=2)

    leave_balance = balance_data["balances"][leave_type]
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days_requested = (end - start).days + 1
    except ValueError:
        return json.dumps({"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}, indent=2)

    if days_requested > leave_balance["remaining"]:
        return json.dumps({"success": False, "message": f"Insufficient balance. Requested: {days_requested}, Available: {leave_balance['remaining']}"}, indent=2)

    request_id = f"LR-{uuid.uuid4().hex[:6].upper()}"
    leave_request = {
        "request_id": request_id, "employee_id": employee_id, "leave_type": leave_type,
        "start_date": start_date, "end_date": end_date, "days": days_requested,
        "reason": reason, "status": "Pending Approval", "submitted_at": datetime.now().isoformat(),
    }
    
    await db.leave_requests.insert_one(leave_request)
    leave_request.pop("_id", None)
    
    # Optional: Deduct balance here or keep pending until approved. Currently kept as pending.
    return json.dumps({"success": True, "message": "Leave request submitted successfully.", "request": leave_request}, indent=2)

@tool(args_schema=GetLeaveBalanceInput)
async def get_leave_balance(employee_id: str) -> str:
    """Check the leave balance for an employee across all leave types.

    Use this tool when someone asks about remaining leave, vacation days, sick days,
    or PTO. Returns all leave categories with entitlement, used, and remaining days.
    """
    db = get_db()
    balance_data = await db.leave_balances.find_one({"employee_id": employee_id.upper()}, {"_id": 0})
    if not balance_data:
        return json.dumps({"success": False, "message": f"No leave data found for '{employee_id}'."}, indent=2)
    return json.dumps({"success": True, "leave_balance": balance_data}, indent=2)
