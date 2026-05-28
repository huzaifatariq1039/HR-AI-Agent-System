"""
HR Analytics & Reporting Tools
=================================
Tools for generating workforce metrics and headcount data.
"""

import json
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_METRICS = {
    "total_headcount": 247,
    "active_employees": 238,
    "on_leave": 9,
    "departments": {
        "Engineering": {"headcount": 82, "open_positions": 5, "avg_tenure_years": 2.8, "attrition_rate": "8.2%"},
        "Marketing": {"headcount": 35, "open_positions": 2, "avg_tenure_years": 3.1, "attrition_rate": "6.5%"},
        "Sales": {"headcount": 45, "open_positions": 4, "avg_tenure_years": 2.2, "attrition_rate": "12.1%"},
        "Human Resources": {"headcount": 18, "open_positions": 1, "avg_tenure_years": 4.0, "attrition_rate": "4.3%"},
        "Finance": {"headcount": 22, "open_positions": 1, "avg_tenure_years": 3.5, "attrition_rate": "5.8%"},
        "Operations": {"headcount": 28, "open_positions": 2, "avg_tenure_years": 2.9, "attrition_rate": "7.1%"},
        "Product": {"headcount": 17, "open_positions": 3, "avg_tenure_years": 2.4, "attrition_rate": "9.0%"},
    },
    "company_avg_tenure_years": 2.9,
    "overall_attrition_rate": "7.8%",
    "diversity": {"gender": {"male": "54%", "female": "43%", "non_binary": "3%"},
                  "avg_age": 33.5},
    "new_hires_ytd": 42,
    "separations_ytd": 19,
    "report_date": "2026-05-28",
}


class GetHeadcountMetricsInput(BaseModel):
    department: Optional[str] = Field(default=None, description="Filter by department name, or None for company-wide")


@tool(args_schema=GetHeadcountMetricsInput)
def get_headcount_metrics(department: Optional[str] = None) -> str:
    """Get workforce headcount metrics and analytics.

    Use this tool when someone asks for workforce analytics, headcount data,
    employee statistics, turnover rates, attrition data, department metrics,
    or workforce summary. Can be filtered by department or returns company-wide data.
    """
    if department:
        dept_data = {k: v for k, v in MOCK_METRICS["departments"].items() if department.lower() in k.lower()}
        if not dept_data:
            return json.dumps({"success": False, "message": f"No data for department '{department}'."}, indent=2)
        return json.dumps({"success": True, "department_metrics": dept_data, "report_date": MOCK_METRICS["report_date"]}, indent=2)

    return json.dumps({"success": True, "metrics": MOCK_METRICS}, indent=2)
