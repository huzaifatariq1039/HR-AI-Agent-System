"""
Recruitment Management Tools
==============================
Tools for managing job postings via MongoDB.
"""

import json
import uuid
from datetime import datetime
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class CreateJobPostingInput(BaseModel):
    title: str = Field(..., description="Job title (e.g., 'Senior React Developer')")
    department: str = Field(..., description="Department name (e.g., 'Engineering')")
    location: str = Field(default="Remote", description="Job location")
    salary_range: str = Field(default="Competitive", description="Salary range")
    description: str = Field(default="", description="Job description text")

class ListJobPostingsInput(BaseModel):
    status: Optional[str] = Field(
        default=None,
        description="Filter by status: 'Open', 'Closed', or None for all postings",
    )
    department: Optional[str] = Field(
        default=None,
        description="Filter by department name",
    )

@tool(args_schema=CreateJobPostingInput)
async def create_job_posting(
    title: str,
    department: str,
    location: str = "Remote",
    salary_range: str = "Competitive",
    description: str = "",
) -> str:
    """Create a new job posting and publish it."""
    db = get_db()
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
    await db.job_postings.insert_one(posting)
    posting.pop("_id", None)
    return json.dumps(
        {
            "success": True,
            "message": f"Job posting '{title}' created successfully.",
            "posting": posting,
        },
        indent=2,
    )

@tool(args_schema=ListJobPostingsInput)
async def list_job_postings(
    status: Optional[str] = None,
    department: Optional[str] = None,
) -> str:
    """List all job postings, optionally filtered by status or department."""
    db = get_db()
    
    filter_query = {}
    if status:
        filter_query["status"] = {"$regex": status, "$options": "i"}
    if department:
        filter_query["department"] = {"$regex": department, "$options": "i"}
        
    cursor = db.job_postings.find(filter_query, {"_id": 0})
    results = await cursor.to_list(length=100)

    return json.dumps(
        {
            "total": len(results),
            "postings": results,
        },
        indent=2,
    )
