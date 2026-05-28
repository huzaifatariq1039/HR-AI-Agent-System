"""
HR Analytics & Reporting Tools
=================================
Tools for generating workforce metrics and headcount data from MongoDB.
"""

import json
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class GetHeadcountMetricsInput(BaseModel):
    department: Optional[str] = Field(default=None, description="Filter by department name, or None for company-wide")

@tool(args_schema=GetHeadcountMetricsInput)
async def get_headcount_metrics(department: Optional[str] = None) -> str:
    """Get workforce headcount metrics and analytics.

    Use this tool when someone asks for workforce analytics, headcount data,
    employee statistics, turnover rates, attrition data, department metrics,
    or workforce summary. Can be filtered by department or returns company-wide data.
    """
    db = get_db()
    metrics = await db.metrics.find_one({"id": "latest_metrics"}, {"_id": 0})
    if not metrics:
        return json.dumps({"success": False, "message": "Metrics data not available."}, indent=2)

    if department:
        dept_data = {k: v for k, v in metrics.get("departments", {}).items() if department.lower() in k.lower()}
        if not dept_data:
            return json.dumps({"success": False, "message": f"No data for department '{department}'."}, indent=2)
        return json.dumps({"success": True, "department_metrics": dept_data, "report_date": metrics.get("report_date")}, indent=2)

    return json.dumps({"success": True, "metrics": metrics}, indent=2)
