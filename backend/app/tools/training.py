"""
Training & Development Tools
===============================
Tools for browsing training programs and certifications.
"""

import json
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_PROGRAMS = [
    {"id": "TRN-001", "title": "Leadership Essentials", "category": "Leadership", "format": "Online",
     "duration": "8 hours", "provider": "LinkedIn Learning", "status": "Open",
     "description": "Foundational leadership skills for new and aspiring managers.", "enrolled": 12, "capacity": 30},
    {"id": "TRN-002", "title": "Advanced Python Development", "category": "Technical", "format": "Instructor-Led",
     "duration": "16 hours", "provider": "Internal", "status": "Open",
     "description": "Deep dive into Python best practices, async programming, and system design.", "enrolled": 8, "capacity": 20},
    {"id": "TRN-003", "title": "Data Privacy & GDPR Compliance", "category": "Compliance", "format": "Online",
     "duration": "4 hours", "provider": "Coursera", "status": "Mandatory",
     "description": "Required training on data protection regulations and compliance.", "enrolled": 35, "capacity": 50},
    {"id": "TRN-004", "title": "Effective Communication", "category": "Soft Skills", "format": "Workshop",
     "duration": "6 hours", "provider": "Internal", "status": "Open",
     "description": "Improve verbal and written communication in professional settings.", "enrolled": 15, "capacity": 25},
    {"id": "TRN-005", "title": "Cloud Architecture (AWS)", "category": "Technical", "format": "Online",
     "duration": "24 hours", "provider": "AWS Training", "status": "Open",
     "description": "Comprehensive AWS cloud architecture certification prep.", "enrolled": 6, "capacity": 15},
]


class ListTrainingProgramsInput(BaseModel):
    category: Optional[str] = Field(default=None, description="Filter by category (e.g., 'Technical', 'Leadership')")


@tool(args_schema=ListTrainingProgramsInput)
def list_training_programs(category: Optional[str] = None) -> str:
    """List available training and development programs.

    Use this tool when someone asks about available training, courses, learning
    programs, certifications, skill development opportunities, or professional
    development options. Can be filtered by category.
    """
    results = MOCK_PROGRAMS.copy()
    if category:
        results = [p for p in results if category.lower() in p["category"].lower()]
    return json.dumps({"total": len(results), "programs": results}, indent=2)
