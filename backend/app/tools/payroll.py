"""
Payroll & Compensation Tools
==============================
Tools for payslip generation and compensation queries via MongoDB.
"""

import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class GetPayslipSummaryInput(BaseModel):
    employee_id: str = Field(
        ...,
        description="The employee ID to fetch the payslip for (e.g., 'EMP-001')",
    )
    pay_period: str = Field(
        default="May 2026",
        description="The pay period to retrieve (e.g., 'May 2026'). Defaults to the current period.",
    )

@tool(args_schema=GetPayslipSummaryInput)
async def get_payslip_summary(employee_id: str, pay_period: str = "May 2026") -> str:
    """Get a detailed payslip summary for an employee for a specific pay period.

    Use this tool when someone asks for a payslip, salary breakdown, pay stub,
    compensation details, or monthly earnings for an employee. It returns a
    detailed breakdown.
    """
    db = get_db()
    payslip = await db.payslips.find_one({
        "employee_id": employee_id.upper(),
        "pay_period": pay_period
    }, {"_id": 0})

    if not payslip:
        return json.dumps(
            {
                "success": False,
                "message": f"No payslip found for employee '{employee_id}' in period '{pay_period}'.",
            },
            indent=2,
        )

    return json.dumps({"success": True, "payslip": payslip}, indent=2)
