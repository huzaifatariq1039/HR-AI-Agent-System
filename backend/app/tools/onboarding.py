"""
Onboarding Tools
==================
Tools for tracking employee onboarding status and checklists.
"""

import json

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_ONBOARDING = {
    "EMP-003": {
        "employee_id": "EMP-003",
        "employee_name": "Alex Chen",
        "start_date": "2024-01-10",
        "status": "In Progress",
        "progress_percent": 75,
        "buddy": "John Doe (EMP-001)",
        "checklist": [
            {"task": "Sign employment contract", "completed": True, "date": "2024-01-10"},
            {"task": "Complete I-9 verification", "completed": True, "date": "2024-01-10"},
            {"task": "IT equipment setup", "completed": True, "date": "2024-01-11"},
            {"task": "Access credentials provisioned", "completed": True, "date": "2024-01-11"},
            {"task": "Orientation session", "completed": True, "date": "2024-01-12"},
            {"task": "Meet with manager", "completed": True, "date": "2024-01-12"},
            {"task": "Complete compliance training", "completed": False, "date": None},
            {"task": "30-day check-in scheduled", "completed": False, "date": None},
        ],
    },
    "EMP-005": {
        "employee_id": "EMP-005",
        "employee_name": "James Wilson",
        "start_date": "2024-06-01",
        "status": "Completed",
        "progress_percent": 100,
        "buddy": "Sarah Johnson (EMP-002)",
        "checklist": [
            {"task": "Sign employment contract", "completed": True, "date": "2024-06-01"},
            {"task": "Complete I-9 verification", "completed": True, "date": "2024-06-01"},
            {"task": "IT equipment setup", "completed": True, "date": "2024-06-02"},
            {"task": "Access credentials provisioned", "completed": True, "date": "2024-06-02"},
            {"task": "Orientation session", "completed": True, "date": "2024-06-03"},
            {"task": "Meet with manager", "completed": True, "date": "2024-06-03"},
            {"task": "Complete compliance training", "completed": True, "date": "2024-06-07"},
            {"task": "30-day check-in scheduled", "completed": True, "date": "2024-07-01"},
        ],
    },
}


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------

class GetOnboardingStatusInput(BaseModel):
    """Input schema for checking onboarding status."""
    employee_id: str = Field(
        ...,
        description="The employee ID to check onboarding status for (e.g., 'EMP-003')",
    )


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool(args_schema=GetOnboardingStatusInput)
def get_onboarding_status(employee_id: str) -> str:
    """Get the onboarding status and checklist progress for an employee.

    Use this tool when someone asks about an employee's onboarding progress,
    onboarding status, onboarding checklist, or whether a new hire has completed
    their onboarding tasks.

    Returns the onboarding checklist with completion status for each task,
    overall progress percentage, assigned buddy, and start date.
    """
    record = MOCK_ONBOARDING.get(employee_id.upper())

    if not record:
        return json.dumps(
            {
                "success": False,
                "message": f"No onboarding record found for '{employee_id}'. "
                           "The employee may have completed onboarding or may not have an active onboarding plan.",
            },
            indent=2,
        )

    return json.dumps({"success": True, "onboarding": record}, indent=2)
