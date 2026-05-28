"""
Payroll & Compensation Tools
==============================
Tools for payslip generation and compensation queries.
"""

import json

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_PAYSLIPS = {
    "EMP-001": {
        "employee_id": "EMP-001",
        "employee_name": "John Doe",
        "pay_period": "May 2026",
        "gross_salary": 12083.33,
        "deductions": {
            "federal_tax": 2416.67,
            "state_tax": 966.67,
            "social_security": 749.17,
            "medicare": 175.21,
            "health_insurance": 350.00,
            "401k_contribution": 604.17,
        },
        "net_pay": 6821.44,
        "ytd_gross": 60416.65,
        "ytd_net": 34107.20,
        "payment_date": "2026-05-30",
        "payment_method": "Direct Deposit",
    },
    "EMP-002": {
        "employee_id": "EMP-002",
        "employee_name": "Sarah Johnson",
        "pay_period": "May 2026",
        "gross_salary": 9166.67,
        "deductions": {
            "federal_tax": 1833.33,
            "state_tax": 641.67,
            "social_security": 568.33,
            "medicare": 132.92,
            "health_insurance": 350.00,
            "401k_contribution": 458.33,
        },
        "net_pay": 5182.09,
        "ytd_gross": 45833.35,
        "ytd_net": 25910.45,
        "payment_date": "2026-05-30",
        "payment_method": "Direct Deposit",
    },
}


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------

class GetPayslipSummaryInput(BaseModel):
    """Input schema for retrieving a payslip summary."""
    employee_id: str = Field(
        ...,
        description="The employee ID to fetch the payslip for (e.g., 'EMP-001')",
    )
    pay_period: str = Field(
        default="May 2026",
        description="The pay period to retrieve (e.g., 'May 2026'). Defaults to the current period.",
    )


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool(args_schema=GetPayslipSummaryInput)
def get_payslip_summary(employee_id: str, pay_period: str = "May 2026") -> str:
    """Get a detailed payslip summary for an employee for a specific pay period.

    Use this tool when someone asks for a payslip, salary breakdown, pay stub,
    compensation details, or monthly earnings for an employee. It returns a
    detailed breakdown including gross salary, all deductions (taxes, insurance,
    retirement), net pay, year-to-date totals, and payment information.
    """
    payslip = MOCK_PAYSLIPS.get(employee_id.upper())

    if not payslip:
        return json.dumps(
            {
                "success": False,
                "message": f"No payslip found for employee '{employee_id}' in period '{pay_period}'.",
            },
            indent=2,
        )

    return json.dumps({"success": True, "payslip": payslip}, indent=2)
