# ShiftFair ⚖️

## Fair Shift Swaps. Better Teams.

**ShiftFair** is an explainable and intelligent shift swap arbitration system designed to help organizations evaluate employee shift swap requests fairly.

Instead of manually searching for replacement employees, ShiftFair evaluates potential swap partners using predefined rules such as:

* Role compatibility
* Department compatibility
* Schedule availability
* Shift conflicts
* Eligibility rules
* Explainable decision generation

The system then recommends an eligible partner and provides a human-readable explanation describing **why the decision was made**.

---

# 🚀 Current Version

## ShiftFair Version 1

This repository currently contains a working end-to-end prototype of ShiftFair.

### Version 1 Includes

* Working frontend interface
* AWS SAM backend
* AWS Lambda functions
* LocalStack for local AWS emulation
* DynamoDB data storage
* Employee roster management
* Shift management
* Shift swap requests
* Intelligent partner matching
* Schedule conflict detection
* Explainable arbitration decisions
* Decision history
* Cedar policy experiments
* OpenSearch experiments
* Strands agent experimentation
* Automated startup script

---

# 🎯 Problem Statement

Organizations such as hospitals, companies, service centers, and operational teams often need employees to exchange shifts.

Traditional shift swap systems usually require:

1. An employee requests a shift swap.
2. A manager manually searches for another employee.
3. Eligibility is checked manually.
4. Schedule conflicts are identified manually.
5. A final decision is made.

This process can be:

* Time-consuming
* Difficult to scale
* Inconsistent
* Potentially unfair
* Difficult to explain

ShiftFair aims to improve this process by providing an automated and explainable arbitration system.

---

# 💡 Solution

ShiftFair evaluates a shift swap request and searches for employees who satisfy the required eligibility conditions.

The system currently evaluates:

```text
Employee
    │
    ▼
Shift Swap Request
    │
    ▼
Arbitration Engine
    │
    ├── Role Matching
    │
    ├── Department Matching
    │
    ├── Schedule Conflict Detection
    │
    └── Eligible Partner Selection
    │
    ▼
Explainable Decision
    │
    ▼
Suggested Swap Partner
```

---

# 🏗️ System Architecture

ShiftFair currently uses the following architecture:

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │ HTML / CSS / JS     │
                    └──────────┬──────────┘
                               │
                               │ HTTP API
                               ▼
                    ┌─────────────────────┐
                    │      AWS SAM        │
                    │   Local API Layer   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼

        ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
        │   Roster     │ │  Decisions   │ │ Swap Request    │
        │   Lambda     │ │   Lambda     │ │     Lambda      │
        └──────┬───────┘ └──────┬───────┘ └────────┬────────┘
               │                │                   │
               └────────────────┼───────────────────┘
                                │
                                ▼
                       ┌────────────────┐
                       │    DynamoDB    │
                       │   LocalStack   │
                       └────────────────┘
```

---

# 🧠 Arbitration Engine

The core functionality of ShiftFair is the arbitration engine.

When an employee submits a shift swap request, the system evaluates other employees and determines who can potentially take the shift.

---

## Rule 1 — Role Matching

The potential partner should have the same or compatible role.

Example:

```text
Employee requesting swap:

David Wilson
Role: Nurse

Potential Partner:

Alice Johnson
Role: Nurse

Result:

✓ Role Match
```

---

## Rule 2 — Department Matching

The potential partner should belong to the same department.

Example:

```text
Employee requesting swap:

Department: Emergency

Potential Partner:

Department: Emergency

Result:

✓ Department Match
```

---

## Rule 3 — Schedule Conflict Detection

The potential partner should not already have a conflicting shift.

Example:

```text
Requested Shift:

2026-09-16
08:00 - 16:00


Potential Partner Shift:

2026-09-15
08:00 - 16:00


Result:

✓ No Conflict
```

Example of a conflict:

```text
Requested Shift:

2026-09-16
08:00 - 16:00


Potential Partner Shift:

2026-09-16
08:00 - 16:00


Result:

✗ Schedule Conflict
```

---

## Rule 4 — Eligible Partner Selection

Employees satisfying the required conditions are added to the eligible partner list.

Example:

```text
Eligible Partners Found:

Alice Johnson
Bob Smith
```

The arbitration engine selects a suggested partner.

---

## Rule 5 — Explainable Decisions

ShiftFair does not simply return a result.

It generates an explanation.

Example:

```text
Alice Johnson was selected as the suggested swap partner.

They have the same role and work in the same department.

They have no conflicting shift during the requested time.

2 eligible partners were found.
```

This improves:

* Transparency
* Trust
* Auditability
* Fairness
* Human understanding

---

# ✨ Current Features

## 👥 Employee Roster

The system displays employees and their details.

Example:

```text
Employee Name

Employee ID

Role

Department

Assigned Shift
```

---

## 📅 Shift Management

The system stores employee shifts.

Each shift contains information such as:

```text
Shift ID

Date

Start Time

End Time

Employee
```

---

## 🔄 Shift Swap Requests

Employees can submit a request to exchange a shift.

The request includes:

```text
Employee

Shift

Reason
```

Example:

```text
Employee:

David Wilson


Shift:

S051


Reason:

Personal commitment
```

---

## 🤖 Intelligent Partner Matching

The system searches for eligible employees.

Current matching factors:

```text
✓ Same Role

✓ Same Department

✓ No Schedule Conflict
```

---

## 📊 Arbitration Decisions

The system stores arbitration decisions.

Each decision contains information such as:

```text
Request ID

Employee

Shift

Suggested Partner

Eligible Partners

Reason

Explanation

Status
```

Example:

```text
Request ID:

805b3e94


Status:

pending_approval


Suggested Partner:

Alice Johnson


Eligible Partners:

2
```

---

## 📜 Decision History

Previous arbitration decisions can be viewed through the frontend.

This provides:

* Decision traceability
* Historical records
* Audit support
* Transparency

---

# 🖥️ Frontend

The ShiftFair frontend is built using:

```text
HTML

CSS

JavaScript
```

Current frontend functionality includes:

* System dashboard
* Employee count
* Shift count
* Decision count
* Shift swap request form
* Employee selection
* Shift selection
* Reason input
* Arbitration result display
* Team roster
* Decision history

---

# 📡 API Endpoints

The current backend provides the following API endpoints.

---

## GET `/roster`

Returns:

* Employees
* Employee details
* Assigned shifts

Example purpose:

```text
Load Team Roster
```

---

## GET `/decisions`

Returns:

* Previous arbitration decisions
* Decision history

Example purpose:

```text
Load Decision History
```

---

## POST `/swap-request`

Submits a new shift swap request.

The backend:

1. Receives the request.
2. Validates the request.
3. Loads employee and shift information.
4. Searches for eligible partners.
5. Checks schedule conflicts.
6. Selects a suggested partner.
7. Generates an explanation.
8. Stores the decision.
9. Returns the result.

---

# 🗄️ Database

ShiftFair currently uses:

```text
DynamoDB
```

For local development, DynamoDB runs through:

```text
LocalStack
```

Current table:

```text
ShiftFairTable
```

The table currently stores multiple record types including:

```text
Employees

Shifts

Decisions
```

---

# 📁 Project Structure

The repository currently contains:

```text
shiftfair/
│
├── cedar-policies/
│
│   ├── entities.json
│   └── shiftfair.cedar
│
├── opensearch-setup/
│
│   ├── docker-compose.yml
│   └── seed_and_search.py
│
├── shiftfair-app/
│
│   ├── decisions/
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   ├── frontend/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   │
│   ├── roster/
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   ├── seed/
│   │   └── seed_data.py
│   │
│   ├── swap_request/
│   │   ├── app.py
│   │   ├── matcher.py
│   │   ├── requirements.txt
│   │   ├── test_boto.py
│   │   └── test_lambda.py
│   │
│   ├── e001.json
│   │
│   ├── events.json
│   │
│   ├── setup_table.sh
│   │
│   ├── template.yaml
│   │
│   └── test_dynamo.py
│
├── strands-agent/
│
│   └── swap_agent.py
│
├── start-shiftfair.ps1
│
├── .gitignore
│
└── README.md
```

---

# 📂 Important Components

---

## `shiftfair-app`

This is the primary application directory.

It contains:

```text
Backend

Frontend

AWS SAM Configuration

Database Seeding

Tests
```

---

## `shiftfair-app/frontend`

Contains the user interface.

```text
index.html
```

Main HTML structure.

```text
style.css
```

Frontend styling.

```text
script.js
```

Frontend logic and API communication.

---

## `shiftfair-app/roster`

Contains the Lambda implementation for:

```text
GET /roster
```

Responsibilities:

* Retrieve employees
* Retrieve shifts
* Build roster data
* Return structured JSON

---

## `shiftfair-app/decisions`

Contains the Lambda implementation for:

```text
GET /decisions
```

Responsibilities:

* Retrieve decision records
* Filter decisions
* Return decision history

---

## `shiftfair-app/swap_request`

Contains the core arbitration logic.

Important files:

```text
app.py
```

Main Lambda handler.

```text
matcher.py
```

Partner matching logic.

Responsibilities include:

* Role matching
* Department matching
* Schedule conflict detection
* Partner eligibility
* Suggested partner selection

---

## `shiftfair-app/seed`

Contains database seed logic.

```text
seed_data.py
```

Used to populate DynamoDB with initial ShiftFair data.

---

## `template.yaml`

AWS SAM configuration.

Defines:

* Lambda functions
* API routes
* Runtime configuration

---

# ⚙️ Technologies Used

## Backend

```text
Python
```

```text
AWS Lambda
```

```text
AWS SAM
```

```text
Boto3
```

---

## Database

```text
Amazon DynamoDB
```

```text
LocalStack
```

---

## Frontend

```text
HTML
```

```text
CSS
```

```text
JavaScript
```

---

## Infrastructure

```text
Docker
```

```text
LocalStack
```

---

## Additional Experiments

```text
Cedar Policies
```

```text
OpenSearch
```

```text
Strands Agent
```

---

# 💻 Local Development Setup

## Prerequisites

The following should be installed.

```text
Python
```

```text
Docker Desktop
```

```text
AWS SAM CLI
```

```text
Git
```

```text
Visual Studio Code
```

---

# 🐍 Python Virtual Environment

The project currently uses a Python virtual environment.

Current environment name:

```text
hackenv
```

Activate it in PowerShell.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\hackenv\Scripts\Activate.ps1
```

After activation:

```text
(hackenv)
```

should appear in the terminal.

Example:

```text
(hackenv) PS D:\shiftfair-starter\shiftfair>
```

---

# 🚀 Starting ShiftFair

## Recommended Method

The project contains:

```text
start-shiftfair.ps1
```

This script was created to simplify the local startup process.

From the project root:

```powershell
.\start-shiftfair.ps1
```

Project root example:

```text
D:\shiftfair-starter\shiftfair
```

---

# 🔥 Recommended Startup Order

When opening VS Code again after restarting your computer, use the following approach.

---

## Step 1 — Open Docker Desktop

Make sure Docker Desktop is running.

Wait until Docker is fully ready.

---

## Step 2 — Open VS Code

Open the project root:

```text
shiftfair
```

Do not open only:

```text
shiftfair-app
```

The full project root should be opened because other project components are also located outside `shiftfair-app`.

Correct:

```text
shiftfair
```

Contains:

```text
cedar-policies

opensearch-setup

shiftfair-app

strands-agent

start-shiftfair.ps1
```

---

## Step 3 — Open a PowerShell Terminal

Navigate to:

```text
D:\shiftfair-starter\shiftfair
```

---

## Step 4 — Activate Virtual Environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\hackenv\Scripts\Activate.ps1
```

---

## Step 5 — Start ShiftFair

Use:

```powershell
.\start-shiftfair.ps1
```

Allow the required services to start.

---

# 🧪 Manual Development Workflow

If the automatic startup process needs troubleshooting, the project can be started component by component.

The general dependency order is:

```text
Docker
    ↓
LocalStack
    ↓
DynamoDB
    ↓
Seed Data
    ↓
AWS SAM API
    ↓
Frontend
```

---

# 🐳 LocalStack

LocalStack emulates AWS services locally.

ShiftFair currently uses LocalStack for DynamoDB development.

The backend connects to LocalStack using the local endpoint.

Example from the working environment:

```text
http://host.docker.internal:4566
```

The backend connection process currently verifies the DynamoDB connection by checking available tables.

Expected table:

```text
ShiftFairTable
```

---

# 🗄️ Database Verification

The project contains:

```text
shiftfair-app/test_dynamo.py
```

This can be used for DynamoDB connection testing and troubleshooting.

The working system has successfully verified:

```text
DynamoDB tables:

['ShiftFairTable']
```

---

# 🌱 Database Seed Data

Initial data is stored using:

```text
shiftfair-app/seed/seed_data.py
```

The Version 1 dataset includes:

```text
4 Employees
```

```text
4 Shifts
```

along with arbitration decision records.

Example employees include:

```text
David Wilson
```

```text
Alice Johnson
```

```text
Bob Smith
```

```text
Carol Davis
```

---

# 🧪 Testing the Application

After starting the system:

---

## Test 1 — Load Frontend

Open the frontend in your browser.

Verify that the dashboard loads.

Expected:

```text
Employees

Shifts

Decisions
```

---

## Test 2 — Verify Employee Dropdown

The employee dropdown should display available employees.

Example:

```text
David Wilson

Alice Johnson

Bob Smith

Carol Davis
```

---

## Test 3 — Verify Shift Dropdown

The shift dropdown should display available shifts.

Example:

```text
S051 — 2026-09-16
```

---

## Test 4 — Submit Swap Request

Select:

```text
Employee
```

Select:

```text
Shift
```

Optionally enter:

```text
Reason
```

Click:

```text
Request Fair Swap
```

---

## Test 5 — Verify Arbitration Result

The system should display:

```text
Request ID

Status

Suggested Partner

Eligible Partners

Explanation
```

---

## Test 6 — Verify Roster

The roster should display:

```text
Employee

ID

Role

Department

Assigned Shift
```

---

## Test 7 — Verify Decision History

Decision history should display previous arbitration decisions.

---

# 📊 Example Arbitration

Example request:

```text
Employee:

David Wilson


Role:

Nurse


Department:

Emergency


Requested Shift:

2026-09-16

08:00 - 16:00
```

---

## Candidate Evaluation

### Alice Johnson

```text
Role Match:

✓ Yes


Department Match:

✓ Yes


Schedule Conflict:

✓ No
```

Result:

```text
Eligible
```

---

### Bob Smith

```text
Role Match:

✓ Yes


Department Match:

✓ Yes


Schedule Conflict:

✓ No
```

Result:

```text
Eligible
```

---

### Carol Davis

```text
Role Match:

✓ Yes


Department Match:

✓ Yes


Schedule Conflict:

✗ Yes
```

Result:

```text
Not Eligible
```

---

## Final Result

Example:

```text
Suggested Partner:

Alice Johnson


Eligible Partners:

2


Status:

pending_approval
```

---

# 🔍 Explainability

Explainability is a core design principle of ShiftFair.

Instead of returning only:

```text
Alice Johnson
```

the system provides reasoning.

Example:

```text
Alice Johnson was selected as the suggested swap partner.

They have the same role.

They work in the same department.

They have no conflicting shift.

2 eligible partners were found.
```

This allows users and administrators to understand the decision.

---

# ⚖️ Fairness Philosophy

ShiftFair is designed around the principle that automated workforce decisions should be understandable.

The system aims to provide:

```text
Fairness
```

```text
Transparency
```

```text
Consistency
```

```text
Explainability
```

```text
Auditability
```

The current Version 1 implementation uses rule-based arbitration.

---

# 🔐 Cedar Policies

The repository contains:

```text
cedar-policies/
```

Files:

```text
entities.json
```

```text
shiftfair.cedar
```

These files are included for policy-based authorization and decision experiments.

This component can be expanded in future versions to support more formal authorization and policy enforcement.

---

# 🔎 OpenSearch

The repository contains:

```text
opensearch-setup/
```

Files:

```text
docker-compose.yml
```

```text
seed_and_search.py
```

This component contains OpenSearch experimentation.

Potential future applications include:

```text
Decision Search
```

```text
Employee Search
```

```text
Historical Analytics
```

```text
Arbitration Record Search
```

---

# 🤖 Strands Agent

The repository contains:

```text
strands-agent/
```

File:

```text
swap_agent.py
```

This component contains experimentation related to agent-based functionality.

Potential future applications include:

```text
AI-assisted arbitration
```

```text
Natural language requests
```

```text
Decision assistance
```

```text
Policy-aware reasoning
```

---

# 👩‍💻 Team Development

ShiftFair is now being developed collaboratively.

The current development responsibilities include separate areas of work.

---

# 🎨 Frontend Development

## Likith Kumar

Focus:

```text
Frontend

UI

UX

Animations

Visual Experience
```

Primary working directory:

```text
shiftfair-app/frontend/
```

Important files:

```text
index.html

style.css

script.js
```

Frontend development should preserve existing API compatibility.

Current APIs:

```text
GET /roster
```

```text
GET /decisions
```

```text
POST /swap-request
```

---

## Frontend Goal

The goal is to create a more modern and polished experience with:

```text
Smooth Animations
```

```text
Micro-interactions
```

```text
Responsive Design
```

```text
Loading States
```

```text
Transition Effects
```

```text
Interactive Cards
```

```text
Professional Dashboard
```

```text
Improved Arbitration Visualization
```

---

# 🧠 Arbitration Rules Research

## Jyothsna

Focus:

```text
Research
```

```text
Rule Design
```

```text
Fairness Logic
```

```text
Arbitration Conditions
```

The goal is to explore additional rules that can improve the ShiftFair arbitration system.

Examples include:

```text
Shift Duration
```

```text
Employee Workload
```

```text
Weekly Working Hours
```

```text
Rest Periods
```

```text
Shift Preferences
```

```text
Skill Compatibility
```

```text
Certification Requirements
```

```text
Emergency Availability
```

```text
Fair Opportunity Distribution
```

```text
Previous Swap History
```

```text
Consecutive Shift Limits
```

Jyothsna's research should first focus on:

```text
Rule Definition
```

```text
Reasoning
```

```text
Fairness Impact
```

```text
Required Data
```

before modifying the working backend.

---

# ⚠️ Important Development Rule

## Do Not Break Version 1

The current Version 1 system is a working baseline.

Before making significant changes:

```text
Create Branch
```

```text
Make Changes
```

```text
Test Locally
```

```text
Commit Changes
```

```text
Push Branch
```

```text
Create Pull Request
```

Avoid directly making experimental changes without testing.

---

# 🌳 Recommended Git Workflow

Each developer should work on a separate branch.

Example:

```text
main
```

Stable version.

---

## Frontend Branch

Example:

```text
feature/frontend-ui
```

---

## Arbitration Branch

Example:

```text
feature/arbitration-rules
```

---

# 🔄 Developer Workflow

Before starting:

```bash
git pull origin main
```

Create a branch:

```bash
git checkout -b feature/branch-name
```

Make changes.

Check changes:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Describe the changes"
```

Push:

```bash
git push origin feature/branch-name
```

Then create a Pull Request.

---

# 🛡️ Version 1 Baseline

The current `main` branch represents:

# ShiftFair Version 1

This version should remain a stable reference point.

The working Version 1 currently demonstrates:

```text
Frontend
        ↓
API
        ↓
AWS SAM
        ↓
Lambda
        ↓
Arbitration Engine
        ↓
DynamoDB
        ↓
Explainable Result
```

---

# 🐛 Known Development Considerations

During local development, the following issues may occasionally occur.

---

## LocalStack Not Running

Symptoms:

```text
DynamoDB Connection Failed
```

Solution:

```text
Ensure Docker Desktop is running.
```

Then restart LocalStack using the project's startup workflow.

---

## SAM API Not Running

Symptoms:

```text
Frontend API Error
```

```text
Failed to Fetch
```

Solution:

Restart the local SAM API.

---

## DynamoDB Table Missing

Symptoms:

```text
Table Not Found
```

Expected table:

```text
ShiftFairTable
```

Solution:

Run the database setup and seed process.

---

## Port Already in Use

Symptoms:

```text
Address Already in Use
```

Solution:

Check existing terminals and previously running processes.

Stop duplicate services before starting another instance.

---

## Ctrl + C Stops Services

If `Ctrl + C` is pressed in a terminal running a development service, that service may stop.

This is normal.

Restart the stopped component.

For normal startup, use the documented startup workflow.

---

# ⚠️ Important Local Development Note

Do not assume that all terminals must remain permanently open after a restart.

When opening the project again:

1. Start Docker Desktop.
2. Open the project root.
3. Activate the virtual environment.
4. Run the ShiftFair startup process.
5. Verify LocalStack.
6. Verify DynamoDB.
7. Verify the SAM API.
8. Open the frontend.

---

# 📈 Future Roadmap

ShiftFair Version 1 establishes the basic working architecture.

Future development can expand the system significantly.

---

# Version 2 — Advanced Arbitration

Potential improvements:

```text
Workload Balancing
```

```text
Rest Period Validation
```

```text
Weekly Hour Limits
```

```text
Shift Preferences
```

```text
Skill Matching
```

```text
Certification Validation
```

```text
Consecutive Shift Limits
```

```text
Historical Swap Fairness
```

---

# Version 3 — Fairness Intelligence

Potential improvements:

```text
Fairness Scoring
```

```text
Employee Opportunity Balancing
```

```text
Bias Detection
```

```text
Decision Auditing
```

```text
Policy Simulation
```

```text
Explainable Fairness Metrics
```

---

# Version 4 — AI-Assisted Shift Arbitration

Potential improvements:

```text
Natural Language Requests
```

Example:

```text
I have an important family event tomorrow.

Can someone cover my morning shift?
```

Possible future system:

```text
Natural Language Input
        ↓
AI Agent
        ↓
Policy Evaluation
        ↓
Arbitration Engine
        ↓
Eligible Partners
        ↓
Explainable Decision
```

---

# Version 5 — Enterprise Platform

Potential features:

```text
Authentication
```

```text
Role-Based Access
```

```text
Manager Dashboard
```

```text
Notifications
```

```text
Email Alerts
```

```text
Employee Preferences
```

```text
Analytics Dashboard
```

```text
Audit Logs
```

```text
Cloud Deployment
```

---

# 📊 Current Development Status

| Component                   | Status            |
| --------------------------- | ----------------- |
| Frontend                    | ✅ Working         |
| Employee Roster             | ✅ Working         |
| Shift Data                  | ✅ Working         |
| Swap Request                | ✅ Working         |
| Role Matching               | ✅ Working         |
| Department Matching         | ✅ Working         |
| Schedule Conflict Detection | ✅ Working         |
| Partner Selection           | ✅ Working         |
| Explainable Decisions       | ✅ Working         |
| Decision History            | ✅ Working         |
| DynamoDB                    | ✅ Working         |
| LocalStack                  | ✅ Working         |
| AWS SAM                     | ✅ Working         |
| Docker                      | ✅ Working         |
| Cedar Experimentation       | 🧪 Experimental   |
| OpenSearch Experimentation  | 🧪 Experimental   |
| Strands Agent               | 🧪 Experimental   |
| Advanced Fairness Rules     | 🚧 Planned        |
| Advanced UI/UX              | 🚧 In Development |
| Authentication              | 📋 Planned        |
| Cloud Deployment            | 📋 Planned        |

---

# 🎯 Project Vision

ShiftFair aims to evolve beyond a simple shift management system.

The long-term vision is:

> Build an explainable, fair, and intelligent workforce arbitration platform capable of evaluating shift decisions transparently.

The system should help organizations answer:

```text
Who is eligible?
```

```text
Why were they selected?
```

```text
Was the decision fair?
```

```text
Were policy constraints respected?
```

```text
Can the decision be audited?
```

---

# 🤝 Contributing

Contributions should follow the development workflow:

```text
1. Pull Latest Changes

2. Create Branch

3. Make Changes

4. Test Locally

5. Commit Changes

6. Push Branch

7. Create Pull Request
```

Avoid directly modifying stable functionality without testing.

---

# 🧪 Testing Before Commit

Before committing major changes, verify:

```text
✓ Frontend Loads
```

```text
✓ Roster Loads
```

```text
✓ Decisions Load
```

```text
✓ Employee Dropdown Works
```

```text
✓ Shift Dropdown Works
```

```text
✓ Swap Request Works
```

```text
✓ Arbitration Result Appears
```

```text
✓ Decision History Updates
```

```text
✓ No Existing API Is Broken
```

---

# 📌 Version

Current Release:

```text
ShiftFair Version 1.0
```

Status:

```text
Working Prototype
```

Development Stage:

```text
Active Development
```

---

# 👥 Contributors

### Sai Pradyumna Thiriveedi

Project Development and Architecture

### Jyothsna

Arbitration Rules and Fairness Research

### Likith Kumar

Frontend, UI/UX, Animation and Visual Experience

---

# ⚖️ Disclaimer

ShiftFair Version 1 is currently a prototype and development project.

The current arbitration engine is primarily rule-based and should not yet be considered a complete workforce decision system.

Future versions should include additional validation, organizational policies, fairness analysis, authentication, security controls, and production-level infrastructure before deployment in real-world high-stakes environments.

---

# 🌟 ShiftFair

## Fair Shift Swaps. Better Teams.

```text
Explainable Decisions

Fair Arbitration

Intelligent Matching

Better Workforce Coordination
```

---
