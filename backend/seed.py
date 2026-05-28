"""
Database Seed Script
====================
Clears and populates the MongoDB database with realistic HR mock data.
Run this script directly to reset the database: `python seed.py`
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "myhr_agent"

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

async def seed_database():
    print("Seeding MongoDB Database...")

    # 1. Job Postings
    await db.job_postings.drop()
    job_postings = [
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
    await db.job_postings.insert_many(job_postings)
    print("Seeded job postings")

    # 2. Employees
    await db.employees.drop()
    employees = [
        {
            "id": "EMP-001",
            "name": "John Doe",
            "email": "john.doe@company.com",
            "department": "Engineering",
            "position": "Senior Software Engineer",
            "manager": "Jane Smith",
            "hire_date": "2023-03-15",
            "status": "Active",
            "location": "San Francisco, CA",
            "phone": "+1-555-0101",
            "salary": "$145,000",
        },
        {
            "id": "EMP-002",
            "name": "Sarah Johnson",
            "email": "sarah.johnson@company.com",
            "department": "Marketing",
            "position": "Marketing Manager",
            "manager": "Michael Brown",
            "hire_date": "2022-07-01",
            "status": "Active",
            "location": "New York, NY",
            "phone": "+1-555-0102",
            "salary": "$110,000",
        },
        {
            "id": "EMP-003",
            "name": "Alex Chen",
            "email": "alex.chen@company.com",
            "department": "Engineering",
            "position": "DevOps Engineer",
            "manager": "Jane Smith",
            "hire_date": "2024-01-10",
            "status": "Active",
            "location": "Remote",
            "phone": "+1-555-0103",
            "salary": "$130,000",
        },
        {
            "id": "EMP-004",
            "name": "Maria Garcia",
            "email": "maria.garcia@company.com",
            "department": "Human Resources",
            "position": "HR Coordinator",
            "manager": "Lisa Wang",
            "hire_date": "2023-09-20",
            "status": "Active",
            "location": "New York, NY",
            "phone": "+1-555-0104",
            "salary": "$75,000",
        },
        {
            "id": "EMP-005",
            "name": "James Wilson",
            "email": "james.wilson@company.com",
            "department": "Finance",
            "position": "Financial Analyst",
            "manager": "Robert Taylor",
            "hire_date": "2024-06-01",
            "status": "Active",
            "location": "Chicago, IL",
            "phone": "+1-555-0105",
            "salary": "$95,000",
        },
    ]
    await db.employees.insert_many(employees)
    print("Seeded employees")

    # 3. Onboarding
    await db.onboarding.drop()
    onboarding_data = [
        {
            "employee_id": "EMP-003",
            "employee_name": "Alex Chen",
            "start_date": "2024-01-10",
            "status": "In Progress",
            "progress_percent": 75,
            "buddy": "John Doe (EMP-001)",
            "checklist": [
                {"task": "Sign employment contract", "completed": True, "date": "2024-01-10"},
                {"task": "Complete I-9 verification", "completed": True, "date": "2024-01-10"},
                {"task": "IT equipment setup", "completed": True, "date": "2024-01-11"},
                {"task": "Access credentials provisioned", "completed": True, "date": "2024-01-11"},
                {"task": "Orientation session", "completed": True, "date": "2024-01-12"},
                {"task": "Meet with manager", "completed": True, "date": "2024-01-12"},
                {"task": "Complete compliance training", "completed": False, "date": None},
                {"task": "30-day check-in scheduled", "completed": False, "date": None},
            ],
        },
        {
            "employee_id": "EMP-005",
            "employee_name": "James Wilson",
            "start_date": "2024-06-01",
            "status": "Completed",
            "progress_percent": 100,
            "buddy": "Sarah Johnson (EMP-002)",
            "checklist": [
                {"task": "Sign employment contract", "completed": True, "date": "2024-06-01"},
                {"task": "Complete I-9 verification", "completed": True, "date": "2024-06-01"},
                {"task": "IT equipment setup", "completed": True, "date": "2024-06-02"},
                {"task": "Access credentials provisioned", "completed": True, "date": "2024-06-02"},
                {"task": "Orientation session", "completed": True, "date": "2024-06-03"},
                {"task": "Meet with manager", "completed": True, "date": "2024-06-03"},
                {"task": "Complete compliance training", "completed": True, "date": "2024-06-07"},
                {"task": "30-day check-in scheduled", "completed": True, "date": "2024-07-01"},
            ],
        },
    ]
    await db.onboarding.insert_many(onboarding_data)
    print("Seeded onboarding")

    # 4. Payslips
    await db.payslips.drop()
    payslips = [
        {
            "employee_id": "EMP-001",
            "employee_name": "John Doe",
            "pay_period": "May 2026",
            "gross_salary": 12083.33,
            "deductions": {
                "federal_tax": 2416.67,
                "state_tax": 966.67,
                "social_security": 749.17,
                "medicare": 175.21,
                "health_insurance": 350.00,
                "401k_contribution": 604.17,
            },
            "net_pay": 6821.44,
            "ytd_gross": 60416.65,
            "ytd_net": 34107.20,
            "payment_date": "2026-05-30",
            "payment_method": "Direct Deposit",
        },
        {
            "employee_id": "EMP-002",
            "employee_name": "Sarah Johnson",
            "pay_period": "May 2026",
            "gross_salary": 9166.67,
            "deductions": {
                "federal_tax": 1833.33,
                "state_tax": 641.67,
                "social_security": 568.33,
                "medicare": 132.92,
                "health_insurance": 350.00,
                "401k_contribution": 458.33,
            },
            "net_pay": 5182.09,
            "ytd_gross": 45833.35,
            "ytd_net": 25910.45,
            "payment_date": "2026-05-30",
            "payment_method": "Direct Deposit",
        },
    ]
    await db.payslips.insert_many(payslips)
    print("Seeded payslips")

    # 5. Leave Balances
    await db.leave_balances.drop()
    leave_balances = [
        {
            "employee_id": "EMP-001",
            "employee_name": "John Doe",
            "fiscal_year": "2026",
            "balances": {
                "annual_leave": {"total": 20, "used": 8, "remaining": 12},
                "sick_leave": {"total": 10, "used": 2, "remaining": 8},
                "personal_leave": {"total": 5, "used": 1, "remaining": 4},
                "parental_leave": {"total": 12, "used": 0, "remaining": 12},
            },
        },
        {
            "employee_id": "EMP-002",
            "employee_name": "Sarah Johnson",
            "fiscal_year": "2026",
            "balances": {
                "annual_leave": {"total": 22, "used": 12, "remaining": 10},
                "sick_leave": {"total": 10, "used": 5, "remaining": 5},
                "personal_leave": {"total": 5, "used": 3, "remaining": 2},
                "parental_leave": {"total": 12, "used": 0, "remaining": 12},
            },
        },
        {
            "employee_id": "EMP-003",
            "employee_name": "Alex Chen",
            "fiscal_year": "2026",
            "balances": {
                "annual_leave": {"total": 18, "used": 3, "remaining": 15},
                "sick_leave": {"total": 10, "used": 0, "remaining": 10},
                "personal_leave": {"total": 5, "used": 0, "remaining": 5},
                "parental_leave": {"total": 12, "used": 0, "remaining": 12},
            },
        },
    ]
    await db.leave_balances.insert_many(leave_balances)
    print("Seeded leave balances")

    # 6. Goals
    await db.goals.drop()
    goals = [
        {
            "employee_id": "EMP-001",
            "employee_name": "John Doe",
            "review_cycle": "H1 2026",
            "goals": [
                {"id": "G-001", "title": "Migrate legacy services to microservices", "category": "Technical",
                 "status": "In Progress", "progress": 65, "due_date": "2026-06-30",
                 "key_results": ["Complete API gateway setup", "Migrate 3 core services", "Achieve 99.9% uptime"]},
                {"id": "G-002", "title": "Mentor 2 junior developers", "category": "Leadership",
                 "status": "On Track", "progress": 50, "due_date": "2026-06-30",
                 "key_results": ["Weekly 1:1 sessions", "Code review participation", "Knowledge sharing presentations"]},
                {"id": "G-003", "title": "Reduce deployment time by 40%", "category": "Efficiency",
                 "status": "Completed", "progress": 100, "due_date": "2026-03-31",
                 "key_results": ["Implement CI/CD pipeline", "Automate testing", "Dockerize all services"]},
            ],
        },
        {
            "employee_id": "EMP-002",
            "employee_name": "Sarah Johnson",
            "review_cycle": "H1 2026",
            "goals": [
                {"id": "G-004", "title": "Launch Q2 brand campaign", "category": "Marketing",
                 "status": "In Progress", "progress": 80, "due_date": "2026-06-15",
                 "key_results": ["Design campaign assets", "Execute across 5 channels", "Achieve 15% engagement increase"]},
                {"id": "G-005", "title": "Increase MQL by 25%", "category": "Growth",
                 "status": "At Risk", "progress": 30, "due_date": "2026-06-30",
                 "key_results": ["Optimize landing pages", "Launch email nurture sequence", "Partner content collaborations"]},
            ],
        },
    ]
    await db.goals.insert_many(goals)
    print("Seeded goals")

    # 7. Training Programs
    await db.training_programs.drop()
    programs = [
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
    await db.training_programs.insert_many(programs)
    print("Seeded training programs")

    # 8. Policies
    await db.policies.drop()
    policies = [
        {
            "id": "POL-001", "title": "Remote Work Policy", "category": "Work Arrangements", "key": "remote_work",
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
        {
            "id": "POL-002", "title": "Paid Time Off (PTO) Policy", "category": "Leave", "key": "pto",
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
        {
            "id": "POL-003", "title": "Code of Conduct", "category": "Ethics", "key": "code_of_conduct",
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
        {
            "id": "POL-004", "title": "Data Privacy & Security Policy", "category": "IT Security", "key": "data_privacy",
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
    ]
    await db.policies.insert_many(policies)
    print("Seeded policies")

    # 9. Metrics
    await db.metrics.drop()
    metrics = {
        "id": "latest_metrics",
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
    await db.metrics.insert_one(metrics)
    print("Seeded metrics")
    
    # Empty collections for inserts
    await db.leave_requests.drop()
    await db.grievances.drop()
    await db.recognitions.drop()
    print("Initialized empty collections for dynamic inserts")

    print("\nDatabase Seeding Complete!")

if __name__ == "__main__":
    asyncio.run(seed_database())
