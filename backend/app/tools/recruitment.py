"""
Recruitment Management Tools
==============================
Tools for managing job postings, applicant tracking, and hiring workflows.
"""

import json
import uuid
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_JOB_POSTINGS = [
    {
        "id": "JOB-001",
        "title": "Senior React Developer",
        "department": "Engineering",
        "location": "Remote",
        "salary_range": "$120,000 - $160,000",
        "status": "Open",
        "posted_date": "2026-05-01",
        "applicants": 23,
        "description": "We are looking for a Senior React Developer to join our frontend team.",
    },
    {
        "id": "JOB-002",
        "title": "HR Business Partner",
        "department": "Human Resources",
        "location": "New York, NY",
        "salary_range": "$90,000 - $120,000",
        "status": "Open",
        "posted_date": "2026-05-10",
        "applicants": 15,
        "description": "Seeking an experienced HRBP to support our growing organization.",
    },
    {
        "id": "JOB-003",
        "title": "Data Analyst",
        "department": "Analytics",
        "location": "San Francisco, CA",
        "salary_range": "$85,000 - $110,000",
        "status": "Closed",
        "posted_date": "2026-04-15",
        "applicants": 42,
        "description": "Join our analytics team to drive data-informed decision making.",
    },
]


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------

class CreateJobPostingInput(BaseModel):
    """Input schema for creating a new job posting."""
    title: str = Field(..., description="Job title (e.g., 'Senior React Developer')")
    department: str = Field(..., description="Department name (e.g., 'Engineering')")
    location: str = Field(default="Remote", description="Job location (e.g., 'Remote', 'New York, NY')")
    salary_range: str = Field(default="Competitive", description="Salary range (e.g., '$100,000 - $130,000')")
    description: str = Field(default="", description="Job description text")


class ListJobPostingsInput(BaseModel):
    """Input schema for listing job postings."""
    status: Optional[str] = Field(
        default=None,
        description="Filter by status: 'Open', 'Closed', or None for all postings",
    )
    department: Optional[str] = Field(
        default=None,
        description="Filter by department name (case-insensitive partial match)",
    )


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool(args_schema=CreateJobPostingInput)
def create_job_posting(
    title: str,
    department: str,
    location: str = "Remote",
    salary_range: str = "Competitive",
    description: str = "",
) -> str:
    """Create a new job posting and publish it to the company's job board.

    Use this tool when someone asks to create, add, or publish a new job posting,
    job listing, or vacancy. This will generate a unique Job ID, set the posting
    date to today, and mark the status as 'Open'.

    Returns a confirmation with the new job posting details.
    """
    new_id = f"JOB-{uuid.uuid4().hex[:4].upper()}"
    posting = {
        "id": new_id,
        "title": title,
        "department": department,
        "location": location,
        "salary_range": salary_range,
        "status": "Open",
        "posted_date": datetime.now().strftime("%Y-%m-%d"),
        "applicants": 0,
        "description": description or f"We are hiring a {title} for the {department} department.",
    }
    # In production, this would save to the database
    MOCK_JOB_POSTINGS.append(posting)
    return json.dumps(
        {
            "success": True,
            "message": f"Job posting '{title}' created successfully.",
            "posting": posting,
        },
        indent=2,
    )


@tool(args_schema=ListJobPostingsInput)
def list_job_postings(
    status: Optional[str] = None,
    department: Optional[str] = None,
) -> str:
    """List all job postings, optionally filtered by status or department.

    Use this tool when someone asks to see, list, view, or show current job
    postings, job listings, vacancies, or open positions. Supports filtering
    by status ('Open' or 'Closed') and by department name.

    Returns a list of matching job postings with details including title,
    department, location, salary range, status, and applicant count.
    """
    results = MOCK_JOB_POSTINGS.copy()

    if status:
        results = [j for j in results if j["status"].lower() == status.lower()]

    if department:
        results = [
            j for j in results
            if department.lower() in j["department"].lower()
        ]

    return json.dumps(
        {
            "total": len(results),
            "postings": results,
        },
        indent=2,
    )
