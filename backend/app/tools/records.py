"""
Employee Records Tools
========================
Tools for querying and searching the employee database.
"""

import json
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_EMPLOYEES = [
    {
        "id": "EMP-001",
        "name": "John Doe",
        "email": "john.doe@company.com",
        "department": "Engineering",
        "position": "Senior Software Engineer",
        "manager": "Jane Smith",
        "hire_date": "2023-03-15",
        "status": "Active",
        "location": "San Francisco, CA",
        "phone": "+1-555-0101",
        "salary": "$145,000",
    },
    {
        "id": "EMP-002",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@company.com",
        "department": "Marketing",
        "position": "Marketing Manager",
        "manager": "Michael Brown",
        "hire_date": "2022-07-01",
        "status": "Active",
        "location": "New York, NY",
        "phone": "+1-555-0102",
        "salary": "$110,000",
    },
    {
        "id": "EMP-003",
        "name": "Alex Chen",
        "email": "alex.chen@company.com",
        "department": "Engineering",
        "position": "DevOps Engineer",
        "manager": "Jane Smith",
        "hire_date": "2024-01-10",
        "status": "Active",
        "location": "Remote",
        "phone": "+1-555-0103",
        "salary": "$130,000",
    },
    {
        "id": "EMP-004",
        "name": "Maria Garcia",
        "email": "maria.garcia@company.com",
        "department": "Human Resources",
        "position": "HR Coordinator",
        "manager": "Lisa Wang",
        "hire_date": "2023-09-20",
        "status": "Active",
        "location": "New York, NY",
        "phone": "+1-555-0104",
        "salary": "$75,000",
    },
    {
        "id": "EMP-005",
        "name": "James Wilson",
        "email": "james.wilson@company.com",
        "department": "Finance",
        "position": "Financial Analyst",
        "manager": "Robert Taylor",
        "hire_date": "2024-06-01",
        "status": "Active",
        "location": "Chicago, IL",
        "phone": "+1-555-0105",
        "salary": "$95,000",
    },
]


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------

class GetEmployeeProfileInput(BaseModel):
    """Input schema for fetching an employee profile."""
    employee_id: str = Field(
        ...,
        description="The employee ID to look up (e.g., 'EMP-001')",
    )


class SearchEmployeesInput(BaseModel):
    """Input schema for searching employees."""
    query: str = Field(
        default="",
        description="Search query — matches against name, department, position, or email (case-insensitive)",
    )
    department: Optional[str] = Field(
        default=None,
        description="Filter by department name (case-insensitive)",
    )
    status: Optional[str] = Field(
        default=None,
        description="Filter by employment status: 'Active' or 'Inactive'",
    )


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool(args_schema=GetEmployeeProfileInput)
def get_employee_profile(employee_id: str) -> str:
    """Retrieve the full profile of a specific employee by their Employee ID.

    Use this tool when someone asks for details about a specific employee, wants
    to look up an employee by their ID, or needs employee information like contact
    details, department, position, manager, hire date, or employment status.

    Accepts an employee ID in the format 'EMP-XXX' and returns the complete
    employee profile including personal details, organizational info, and status.
    """
    employee = next(
        (e for e in MOCK_EMPLOYEES if e["id"].upper() == employee_id.upper()),
        None,
    )

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
def search_employees(
    query: str = "",
    department: Optional[str] = None,
    status: Optional[str] = None,
) -> str:
    """Search the employee directory by name, department, position, or email.

    Use this tool when someone asks to find employees, search the directory,
    list employees in a department, or look up people by name, role, or email.
    Supports optional filtering by department and employment status.

    Returns a list of matching employee profiles.
    """
    results = MOCK_EMPLOYEES.copy()

    if query:
        q = query.lower()
        results = [
            e for e in results
            if q in e["name"].lower()
            or q in e["department"].lower()
            or q in e["position"].lower()
            or q in e["email"].lower()
        ]

    if department:
        results = [
            e for e in results
            if department.lower() in e["department"].lower()
        ]

    if status:
        results = [
            e for e in results
            if e["status"].lower() == status.lower()
        ]

    return json.dumps(
        {"total": len(results), "employees": results},
        indent=2,
    )
