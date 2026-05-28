"""
Leave & Attendance Tools
==========================
Tools for managing employee leave requests, balances, and attendance.
"""

import json
import uuid
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_LEAVE_BALANCES = {
    "EMP-001": {
        "employee_id": "EMP-001",
        "employee_name": "John Doe",
        "fiscal_year": "2026",
        "balances": {
            "annual_leave": {"total": 20, "used": 8, "remaining": 12},
            "sick_leave": {"total": 10, "used": 2, "remaining": 8},
            "personal_leave": {"total": 5, "used": 1, "remaining": 4},
            "parental_leave": {"total": 12, "used": 0, "remaining": 12},
        },
    },
    "EMP-002": {
        "employee_id": "EMP-002",
        "employee_name": "Sarah Johnson",
        "fiscal_year": "2026",
        "balances": {
            "annual_leave": {"total": 22, "used": 12, "remaining": 10},
            "sick_leave": {"total": 10, "used": 5, "remaining": 5},
            "personal_leave": {"total": 5, "used": 3, "remaining": 2},
            "parental_leave": {"total": 12, "used": 0, "remaining": 12},
        },
    },
    "EMP-003": {
        "employee_id": "EMP-003",
        "employee_name": "Alex Chen",
        "fiscal_year": "2026",
        "balances": {
            "annual_leave": {"total": 18, "used": 3, "remaining": 15},
            "sick_leave": {"total": 10, "used": 0, "remaining": 10},
            "personal_leave": {"total": 5, "used": 0, "remaining": 5},
            "parental_leave": {"total": 12, "used": 0, "remaining": 12},
        },
    },
}

MOCK_LEAVE_REQUESTS: list[dict] = []


class ApplyLeaveInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g., 'EMP-001')")
    leave_type: str = Field(..., description="Type: 'annual_leave', 'sick_leave', 'personal_leave', or 'parental_leave'")
    start_date: str = Field(..., description="Start date YYYY-MM-DD")
    end_date: str = Field(..., description="End date YYYY-MM-DD")
    reason: str = Field(default="", description="Reason for leave")


class GetLeaveBalanceInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g., 'EMP-001')")


@tool(args_schema=ApplyLeaveInput)
def apply_leave(employee_id: str, leave_type: str, start_date: str, end_date: str, reason: str = "") -> str:
    """Submit a leave request for an employee.

    Use this tool when someone asks to apply for leave, request time off, take
    vacation, request sick days, or submit any kind of leave application. Validates
    the leave balance, checks dates, and creates a pending leave request.

    Supported leave types: annual_leave, sick_leave, personal_leave, parental_leave.
    """
    balance_data = MOCK_LEAVE_BALANCES.get(employee_id.upper())
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
    MOCK_LEAVE_REQUESTS.append(leave_request)
    return json.dumps({"success": True, "message": "Leave request submitted successfully.", "request": leave_request}, indent=2)


@tool(args_schema=GetLeaveBalanceInput)
def get_leave_balance(employee_id: str) -> str:
    """Check the leave balance for an employee across all leave types.

    Use this tool when someone asks about remaining leave, vacation days, sick days,
    leave balance, time-off balance, or PTO. Returns all leave categories with
    total entitlement, days used, and days remaining.
    """
    balance_data = MOCK_LEAVE_BALANCES.get(employee_id.upper())
    if not balance_data:
        return json.dumps({"success": False, "message": f"No leave data found for '{employee_id}'."}, indent=2)
    return json.dumps({"success": True, "leave_balance": balance_data}, indent=2)
