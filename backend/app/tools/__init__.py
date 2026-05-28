"""
HR Tools — Aggregation Module
================================
Exports all HR tools as a single list for binding to the LangGraph agent.
"""

from app.tools.recruitment import create_job_posting, list_job_postings
from app.tools.records import get_employee_profile, search_employees
from app.tools.onboarding import get_onboarding_status
from app.tools.payroll import get_payslip_summary
from app.tools.leave import apply_leave, get_leave_balance
from app.tools.performance import get_goals
from app.tools.training import list_training_programs
from app.tools.relations import file_grievance
from app.tools.compliance import get_policy
from app.tools.analytics import get_headcount_metrics
from app.tools.engagement import send_recognition


def get_all_tools() -> list:
    """Return all HR tools as a flat list."""
    return [
        create_job_posting,
        list_job_postings,
        get_employee_profile,
        search_employees,
        get_onboarding_status,
        get_payslip_summary,
        apply_leave,
        get_leave_balance,
        get_goals,
        list_training_programs,
        file_grievance,
        get_policy,
        get_headcount_metrics,
        send_recognition,
    ]
