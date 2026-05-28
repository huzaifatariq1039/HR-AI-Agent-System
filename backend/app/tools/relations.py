"""
Employee Relations Tools
==========================
Tools for filing and tracking employee grievances.
"""

import json
import uuid
from datetime import datetime
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_GRIEVANCES: list[dict] = []


class FileGrievanceInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID filing the grievance (e.g., 'EMP-003')")
    category: str = Field(..., description="Category: 'working_conditions', 'harassment', 'discrimination', 'compensation', 'management', 'other'")
    description: str = Field(..., description="Detailed description of the grievance")
    is_anonymous: bool = Field(default=False, description="Whether to file anonymously")


@tool(args_schema=FileGrievanceInput)
def file_grievance(employee_id: str, category: str, description: str, is_anonymous: bool = False) -> str:
    """File a formal employee grievance confidentially.

    Use this tool when someone needs to file a grievance, complaint, report an
    issue, report harassment, or raise a workplace concern. All grievances are
    handled with strict confidentiality. Supports anonymous filing.

    Categories: working_conditions, harassment, discrimination, compensation, management, other.
    """
    valid_categories = ["working_conditions", "harassment", "discrimination", "compensation", "management", "other"]
    if category.lower() not in valid_categories:
        return json.dumps({"success": False, "message": f"Invalid category. Valid: {', '.join(valid_categories)}"}, indent=2)

    grievance_id = f"GRV-{uuid.uuid4().hex[:6].upper()}"
    grievance = {
        "grievance_id": grievance_id,
        "filed_by": "Anonymous" if is_anonymous else employee_id,
        "category": category,
        "description": description,
        "status": "Under Review",
        "priority": "High" if category in ["harassment", "discrimination"] else "Medium",
        "filed_at": datetime.now().isoformat(),
        "assigned_to": "HR Relations Team",
        "expected_resolution": "5-10 business days",
    }
    MOCK_GRIEVANCES.append(grievance)
    return json.dumps({"success": True, "message": "Grievance filed confidentially.", "grievance": grievance}, indent=2)
