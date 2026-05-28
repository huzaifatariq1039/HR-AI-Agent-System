"""
Onboarding Tools
==================
Tools for tracking employee onboarding status via MongoDB.
"""

import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class GetOnboardingStatusInput(BaseModel):
    employee_id: str = Field(
        ...,
        description="The employee ID to check onboarding status for (e.g., 'EMP-003')",
    )

@tool(args_schema=GetOnboardingStatusInput)
async def get_onboarding_status(employee_id: str) -> str:
    """Get the onboarding status and checklist progress for an employee.

    Use this tool when someone asks about an employee's onboarding progress,
    onboarding status, onboarding checklist, or whether a new hire has completed
    their onboarding tasks.
    """
    db = get_db()
    record = await db.onboarding.find_one({"employee_id": employee_id.upper()}, {"_id": 0})

    if not record:
        return json.dumps(
            {
                "success": False,
                "message": f"No onboarding record found for '{employee_id}'. "
                           "The employee may have completed onboarding or may not have an active plan.",
            },
            indent=2,
        )

    return json.dumps({"success": True, "onboarding": record}, indent=2)
