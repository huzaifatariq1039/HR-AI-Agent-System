"""
Performance Management Tools
===============================
Tools for tracking employee goals, OKRs, and performance metrics.
"""

import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_GOALS = {
    "EMP-001": {
        "employee_id": "EMP-001",
        "employee_name": "John Doe",
        "review_cycle": "H1 2026",
        "goals": [
            {"id": "G-001", "title": "Migrate legacy services to microservices", "category": "Technical",
             "status": "In Progress", "progress": 65, "due_date": "2026-06-30",
             "key_results": ["Complete API gateway setup", "Migrate 3 core services", "Achieve 99.9% uptime"]},
            {"id": "G-002", "title": "Mentor 2 junior developers", "category": "Leadership",
             "status": "On Track", "progress": 50, "due_date": "2026-06-30",
             "key_results": ["Weekly 1:1 sessions", "Code review participation", "Knowledge sharing presentations"]},
            {"id": "G-003", "title": "Reduce deployment time by 40%", "category": "Efficiency",
             "status": "Completed", "progress": 100, "due_date": "2026-03-31",
             "key_results": ["Implement CI/CD pipeline", "Automate testing", "Dockerize all services"]},
        ],
    },
    "EMP-002": {
        "employee_id": "EMP-002",
        "employee_name": "Sarah Johnson",
        "review_cycle": "H1 2026",
        "goals": [
            {"id": "G-004", "title": "Launch Q2 brand campaign", "category": "Marketing",
             "status": "In Progress", "progress": 80, "due_date": "2026-06-15",
             "key_results": ["Design campaign assets", "Execute across 5 channels", "Achieve 15% engagement increase"]},
            {"id": "G-005", "title": "Increase MQL by 25%", "category": "Growth",
             "status": "At Risk", "progress": 30, "due_date": "2026-06-30",
             "key_results": ["Optimize landing pages", "Launch email nurture sequence", "Partner content collaborations"]},
        ],
    },
}


class GetGoalsInput(BaseModel):
    employee_id: str = Field(..., description="Employee ID (e.g., 'EMP-001')")


@tool(args_schema=GetGoalsInput)
def get_goals(employee_id: str) -> str:
    """Retrieve the performance goals and OKRs for a specific employee.

    Use this tool when someone asks about an employee's goals, objectives, key results,
    OKRs, performance targets, or what someone is working toward. Returns all goals
    with progress percentages, status, due dates, and key results.
    """
    data = MOCK_GOALS.get(employee_id.upper())
    if not data:
        return json.dumps({"success": False, "message": f"No goals found for '{employee_id}'."}, indent=2)
    return json.dumps({"success": True, "performance": data}, indent=2)
