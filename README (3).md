# 🤖 HR AI Agent System — Complete HR Department Replacement

> A comprehensive n8n AI Agent that fully automates every function of a traditional HR department.

I built this HR AI Agent System to completely replace a traditional HR department using an n8n AI Agent workflow. Instead of an entire team handling recruitment, payroll, compliance, and employee relations, this system handles it all through a single conversational AI interface powered by GPT-4o.

This isn't a simple chatbot — it's a fully functional HR system with **11 specialized tools** and **80+ automated actions** that cover every aspect of human resource management.

---

## 📋 Table of Contents

- [What It Can Do](#-what-it-can-do)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Configuration](#-configuration)
- [How to Use](#-how-to-use)
- [Tools & Capabilities Breakdown](#-tools--capabilities-breakdown)
- [Customization Guide](#-customization-guide)
- [Production Deployment Notes](#-production-deployment-notes)
- [License](#-license)

---

## 🚀 What It Can Do

I designed this system to handle **every function** a typical HR department performs:

| Area | What It Handles |
|------|----------------|
| **Recruitment** | Job postings, resume screening & scoring, interview scheduling, offer letter generation, applicant tracking |
| **Employee Records** | Full employee database, org charts, document management, employment history |
| **Onboarding** | Automated onboarding checklists, welcome packs, buddy assignment, orientation scheduling |
| **Offboarding** | Exit interviews, final settlement calculations, experience letters, knowledge transfer plans |
| **Payroll** | Salary processing, tax calculations, payslip generation, bonuses, expense reimbursements |
| **Leave & Attendance** | Leave requests & approvals, balance tracking, attendance monitoring, overtime, shift management |
| **Performance** | Goal/OKR setting, performance reviews, 360° feedback, PIPs, promotion recommendations |
| **Training** | Training needs assessment, program enrollment, certification tracking, career development plans, skill matrices |
| **Employee Relations** | Grievance filing & resolution, disciplinary actions, conflict mediation, satisfaction surveys, counseling referrals |
| **Compliance** | Policy creation & management, labor law checks, audit scheduling, safety incident reporting |
| **Analytics** | Workforce summaries, turnover reports, compensation analysis, diversity metrics, predictive insights |
| **Engagement** | Recognition & rewards, team events, wellness programs, benefits enrollment, insurance claims, birthday/anniversary wishes |

---

## 🏗 Architecture

```
┌─────────────────────┐
│   Chat Interface    │  ← You talk to the agent here
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐     ┌──────────────────┐
│   HR AI Agent       │◄────│  GPT-4o (OpenAI) │
│   (Core Engine)     │     └──────────────────┘
│                     │     ┌──────────────────┐
│   System Prompt +   │◄────│ Conversation     │
│   Tool Routing      │     │ Memory           │
└─────────┬───────────┘     └──────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│           11 Specialized Tools          │
├─────────────┬─────────────┬─────────────┤
│ Recruitment │  Employee   │ Onboarding/ │
│ Management  │  Records    │ Offboarding │
├─────────────┼─────────────┼─────────────┤
│  Payroll &  │   Leave &   │ Performance │
│Compensation │ Attendance  │ Management  │
├─────────────┼─────────────┼─────────────┤
│ Training &  │  Employee   │ Compliance  │
│ Development │  Relations  │  & Policy   │
├─────────────┼─────────────┼─────────────┤
│ HR Analytics│ Engagement  │             │
│ & Reporting │ & Benefits  │             │
└─────────────┴─────────────┴─────────────┘
```

- **15 total nodes** in the workflow
- **11 AI-powered tool nodes** (each handles multiple actions via smart routing)
- **Conversation memory** for context-aware multi-turn interactions

---

## 📦 Prerequisites

Before setting up, make sure you have:

1. **n8n** — Self-hosted or cloud instance ([install guide](https://docs.n8n.io/hosting/installation/))
2. **OpenAI API Key** — With access to GPT-4o (or another supported model)
3. **Node.js 18+** — If running n8n locally

---

## 🛠 Setup & Installation

### Step 1: Import the Workflow

1. Download `HR_AI_Agent_System_Workflow.json` from this repository
2. Open your n8n instance
3. Navigate to **Workflows** → click the **⋮ menu** → **Import from File**
4. Select the downloaded JSON file
5. The workflow will load with all 15 nodes pre-configured

### Step 2: Configure OpenAI Credentials

1. In the imported workflow, click the **"OpenAI Chat Model"** node
2. Under **Credential to connect with**, click **Create New Credential**
3. Enter your **OpenAI API Key**
4. Click **Save**

### Step 3: Activate

1. Toggle the workflow to **Active** (top-right switch)
2. Click **"Chat"** in the top panel to open the built-in chat interface
3. Start talking to the HR AI Agent!

> **That's it.** No database setup, no additional services. I designed it to work out of the box for demonstration and testing purposes.

---

## ⚙ Configuration

### Changing the AI Model

I set GPT-4o as the default because it handles complex HR reasoning well. To change it:

1. Click the **"OpenAI Chat Model"** node
2. Change the `model` parameter (e.g., `gpt-4o-mini` for lower cost, `gpt-4-turbo` for alternatives)
3. Adjust `temperature` (default: `0.3` — I kept it low for consistent, professional responses)

### Adjusting Memory

The **Conversation Memory** node retains the last 20 messages by default. Adjust `contextWindowLength` if you need longer or shorter conversation context.

---

## 💬 How to Use

The HR AI Agent understands natural language. Just type your HR request as you would ask a human HR manager:

### Example Conversations

```
You: "Create a job posting for a Senior React Developer in the Engineering department"
Agent: ✅ Job posting JOB-XXXX created and published to all configured job boards...

You: "What's the leave balance for employee EMP-001?"
Agent: Here are the leave balances for EMP-001...

You: "Process this month's payroll"
Agent: ✅ Payroll PAY-XXXX processed for 40 employees...

You: "I need a turnover report for Q1 2026"
Agent: Here's the Q1 2026 turnover analysis...

You: "File a grievance for EMP-003 regarding working conditions"
Agent: ✅ Grievance GRV-XXXX filed confidentially...

You: "Create a performance improvement plan for EMP-002"
Agent: ✅ PIP-XXXX created with 90-day milestones...

You: "Show me upcoming birthdays and work anniversaries"
Agent: Here are the upcoming celebrations...
```

---

## 🔧 Tools & Capabilities Breakdown

### 1. Recruitment Management (7 actions)
`create_job_posting` · `list_job_postings` · `screen_resume` · `schedule_interview` · `list_candidates` · `generate_offer_letter` · `update_application_status`

### 2. Employee Records (7 actions)
`get_employee` · `list_employees` · `update_employee` · `search_employees` · `get_org_chart` · `add_document` · `get_employee_history`

### 3. Onboarding & Offboarding (7 actions)
`create_onboarding_plan` · `get_onboarding_status` · `initiate_offboarding` · `conduct_exit_interview` · `calculate_final_settlement` · `generate_experience_letter` · `knowledge_transfer_plan`

### 4. Payroll & Compensation (7 actions)
`process_payroll` · `get_payslip` · `calculate_tax` · `manage_bonus` · `process_expense` · `salary_revision` · `get_compensation_structure`

### 5. Leave & Attendance (8 actions)
`apply_leave` · `approve_leave` · `get_leave_balance` · `get_attendance` · `log_attendance` · `manage_overtime` · `get_shift_schedule` · `swap_shift`

### 6. Performance Management (7 actions)
`set_goals` · `get_goals` · `create_review` · `submit_feedback` · `get_review_history` · `create_pip` · `recommend_promotion`

### 7. Training & Development (7 actions)
`assess_training_needs` · `list_programs` · `enroll_employee` · `track_certifications` · `create_career_plan` · `get_skill_matrix` · `training_feedback`

### 8. Employee Relations (8 actions)
`file_grievance` · `get_grievances` · `resolve_grievance` · `disciplinary_action` · `conduct_survey` · `get_survey_results` · `mediate_conflict` · `counseling_referral`

### 9. Compliance & Policy (8 actions)
`create_policy` · `list_policies` · `get_policy` · `check_compliance` · `schedule_audit` · `get_audit_results` · `report_safety_incident` · `labor_law_check`

### 10. HR Analytics & Reporting (8 actions)
`workforce_summary` · `turnover_report` · `compensation_analysis` · `diversity_report` · `headcount_trends` · `department_metrics` · `generate_custom_report` · `predictive_insights`

### 11. Engagement & Benefits (8 actions)
`send_recognition` · `get_recognitions` · `plan_team_event` · `run_wellness_program` · `manage_benefits_enrollment` · `process_insurance_claim` · `get_benefits_summary` · `birthday_anniversary_wishes`

---

## 🔄 Customization Guide

I built this system with **sample/demo data** inside each tool so it works immediately upon import. For production use, here's what I recommend:

### Connecting a Real Database

Replace the sample data arrays in each tool's JavaScript code with actual database queries. For example, in the **Employee Records** tool:

```javascript
// BEFORE (demo data):
const emps = [{id: "EMP-001", name: "John Doe", ...}];

// AFTER (real database):
const response = await fetch('https://your-api.com/employees');
const emps = await response.json();
```

### Integrating External Services

I recommend connecting these services for a production deployment:

| Service | Purpose | n8n Integration |
|---------|---------|-----------------|
| **PostgreSQL / MySQL** | Employee database | n8n Database nodes |
| **Google Workspace / O365** | Calendar & email | n8n Google/Microsoft nodes |
| **Slack / Teams** | Notifications | n8n Chat nodes |
| **BambooHR / Workday** | HRIS sync | HTTP Request or API nodes |
| **QuickBooks / Xero** | Payroll integration | n8n Accounting nodes |
| **DocuSign** | Offer letters & contracts | HTTP Request nodes |

### Using n8n Sub-Workflows

For complex operations, I recommend converting individual tool actions into **n8n sub-workflows** using the `toolWorkflow` node type instead of `toolCode`. This allows you to build visual, multi-step processes for things like payroll that involve multiple systems.

---

## 🏭 Production Deployment Notes

Before deploying in a real organization, I recommend:

1. **🔐 Security**: Add authentication to the chat trigger (webhook auth, API keys, or SSO)
2. **🗄 Database**: Replace sample data with actual HRIS/database connections
3. **📧 Notifications**: Connect email/Slack nodes for automated notifications (leave approvals, onboarding tasks, etc.)
4. **📝 Audit Logging**: Add logging nodes to track all HR actions for compliance
5. **🔑 RBAC**: Implement role-based access so employees, managers, and admins see different data
6. **💾 Backup**: Enable n8n workflow versioning and database backups
7. **⚡ Rate Limiting**: Configure OpenAI rate limits to manage API costs

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it.

---

**Built with ❤️ using [n8n](https://n8n.io) and OpenAI GPT-4o**
