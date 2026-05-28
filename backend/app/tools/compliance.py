"""
Compliance & Policy Tools
===========================
Tools for looking up company policies from MongoDB.
"""

import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from app.db import get_db

class GetPolicyInput(BaseModel):
    policy_name: str = Field(
        ...,
        description="Policy name/keyword to look up (e.g., 'remote_work', 'pto', 'code_of_conduct', 'data_privacy')",
    )

@tool(args_schema=GetPolicyInput)
async def get_policy(policy_name: str) -> str:
    """Look up a company policy by name or keyword.

    Use this tool when someone asks about company policies, workplace rules,
    guidelines, compliance requirements, or wants to know the policy on a
    specific topic like remote work, PTO, code of conduct, or data privacy.
    """
    db = get_db()
    key = policy_name.lower().replace(" ", "_").replace("-", "_")
    
    # Exact match on key
    policy = await db.policies.find_one({"key": key}, {"_id": 0})
    
    if not policy:
        # Fuzzy match
        cursor = db.policies.find({}, {"_id": 0})
        policies = await cursor.to_list(length=100)
        matches = [p for p in policies if key in p["key"] or key in p["title"].lower()]
        if matches:
            policy = matches[0]
        else:
            available = ", ".join([p["key"] for p in policies])
            return json.dumps({"success": False, "message": f"Policy '{policy_name}' not found. Available: {available}"}, indent=2)

    return json.dumps({"success": True, "policy": policy}, indent=2)
