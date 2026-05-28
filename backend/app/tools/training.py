"""
Training & Development Tools
===============================
Tools for browsing training programs and certifications via MongoDB.
"""

import json
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class ListTrainingProgramsInput(BaseModel):
    category: Optional[str] = Field(default=None, description="Filter by category")

@tool(args_schema=ListTrainingProgramsInput)
async def list_training_programs(category: Optional[str] = None) -> str:
    """List available training and development programs."""
    db = get_db()
    
    filter_query = {}
    if category:
        filter_query["category"] = {"$regex": category, "$options": "i"}
        
    cursor = db.training_programs.find(filter_query, {"_id": 0})
    results = await cursor.to_list(length=100)
    
    return json.dumps({"total": len(results), "programs": results}, indent=2)
