"""
Compliance & Policy Tools
===========================
Tools for looking up company policies and compliance information.
"""

import json
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MOCK_POLICIES = {
    "remote_work": {
        "id": "POL-001", "title": "Remote Work Policy", "category": "Work Arrangements",
        "effective_date": "2025-01-01", "last_updated": "2025-11-15", "version": "2.1",
        "summary": "Employees may work remotely up to 3 days per week with manager approval. Full remote requires VP approval.",
        "key_points": [
            "Eligible after 90-day probation period",
            "Must maintain core hours (10 AM - 3 PM local time)",
            "Home office stipend of $500/year provided",
            "Quarterly in-office attendance required",
            "Manager approval needed for schedule changes",
        ],
    },
    "pto": {
        "id": "POL-002", "title": "Paid Time Off (PTO) Policy", "category": "Leave",
        "effective_date": "2025-01-01", "last_updated": "2026-01-10", "version": "3.0",
        "summary": "Comprehensive PTO policy covering annual, sick, personal, and parental leave entitlements.",
        "key_points": [
            "Annual leave: 15-25 days based on tenure",
            "Sick leave: 10 days per year (no carryover)",
            "Personal leave: 5 days per year",
            "Parental leave: 12 weeks paid",
            "Unused annual leave carries over (max 5 days)",
        ],
    },
    "code_of_conduct": {
        "id": "POL-003", "title": "Code of Conduct", "category": "Ethics",
        "effective_date": "2024-06-01", "last_updated": "2025-06-01", "version": "4.0",
        "summary": "Standards of professional behavior, ethics, and integrity expected of all employees.",
        "key_points": [
            "Zero tolerance for harassment and discrimination",
            "Conflicts of interest must be disclosed",
            "Confidentiality of company and client information",
            "Social media guidelines for professional representation",
            "Reporting violations via ethics hotline or HR",
        ],
    },
    "data_privacy": {
        "id": "POL-004", "title": "Data Privacy & Security Policy", "category": "IT Security",
        "effective_date": "2025-03-01", "last_updated": "2026-02-15", "version": "2.0",
        "summary": "Guidelines for handling personal and sensitive data in compliance with GDPR and local regulations.",
        "key_points": [
            "All data classified as Public, Internal, Confidential, or Restricted",
            "MFA required for all systems",
            "Data breach must be reported within 24 hours",
            "Annual data privacy training mandatory",
            "Third-party data processing requires DPA",
        ],
    },
}


class GetPolicyInput(BaseModel):
    policy_name: str = Field(
        ...,
        description="Policy name/keyword to look up (e.g., 'remote_work', 'pto', 'code_of_conduct', 'data_privacy')",
    )


@tool(args_schema=GetPolicyInput)
def get_policy(policy_name: str) -> str:
    """Look up a company policy by name or keyword.

    Use this tool when someone asks about company policies, workplace rules,
    guidelines, compliance requirements, or wants to know the policy on a
    specific topic like remote work, PTO, code of conduct, or data privacy.

    Available policies: remote_work, pto, code_of_conduct, data_privacy.
    """
    key = policy_name.lower().replace(" ", "_").replace("-", "_")
    policy = MOCK_POLICIES.get(key)

    if not policy:
        # Fuzzy search
        matches = [p for k, p in MOCK_POLICIES.items() if key in k or key in p["title"].lower()]
        if matches:
            policy = matches[0]
        else:
            available = ", ".join(MOCK_POLICIES.keys())
            return json.dumps({"success": False, "message": f"Policy '{policy_name}' not found. Available: {available}"}, indent=2)

    return json.dumps({"success": True, "policy": policy}, indent=2)
