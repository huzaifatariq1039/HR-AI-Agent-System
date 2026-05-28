"""
Engagement & Benefits Tools
==============================
Tools for employee recognition and engagement programs.
"""

import json
import uuid
from datetime import datetime
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_RECOGNITIONS: list[dict] = []


class SendRecognitionInput(BaseModel):
    recipient_id: str = Field(..., description="Employee ID receiving recognition (e.g., 'EMP-001')")
    sender_name: str = Field(..., description="Name of the person sending the recognition")
    message: str = Field(..., description="Recognition message (what they did and why it matters)")
    category: str = Field(
        default="teamwork",
        description="Category: 'innovation', 'teamwork', 'leadership', 'customer_focus', 'above_and_beyond'",
    )


@tool(args_schema=SendRecognitionInput)
def send_recognition(recipient_id: str, sender_name: str, message: str, category: str = "teamwork") -> str:
    """Send a recognition or kudos to an employee for outstanding work.

    Use this tool when someone wants to recognize, appreciate, thank, give kudos,
    or send a shout-out to an employee. Creates a public recognition entry visible
    across the organization.

    Categories: innovation, teamwork, leadership, customer_focus, above_and_beyond.
    """
    valid = ["innovation", "teamwork", "leadership", "customer_focus", "above_and_beyond"]
    if category.lower() not in valid:
        category = "teamwork"

    recognition = {
        "recognition_id": f"REC-{uuid.uuid4().hex[:6].upper()}",
        "recipient_id": recipient_id,
        "sender": sender_name,
        "message": message,
        "category": category,
        "created_at": datetime.now().isoformat(),
        "points_awarded": 50,
    }
    MOCK_RECOGNITIONS.append(recognition)
    return json.dumps({"success": True, "message": "Recognition sent successfully! 🎉", "recognition": recognition}, indent=2)
