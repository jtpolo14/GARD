# G.A.R.D.

**Governance for Agentic Rules & Decisions**

*A control platform for defining, managing, and enforcing business rules used by AI agents and automated processes.*

---

## Core Concept

G.A.R.D. acts as the **decision governance layer** between:

- AI Agents
- Business Processes
- Enterprise Data Systems

Instead of agents making uncontrolled decisions, they **query G.A.R.D. for rules, policies, and validations**.

```
Agents / Apps
      │
      ▼
   G.A.R.D.
Decision Governance Layer
      │
      ▼
Rules • Policies • Controls • Approvals
```

---

## Core Modules

### 1. Rule Studio

Primary interface where business users manage rules.

**Features:**
- Human-readable rules
- Visual logic builder
- Version control
- Simulation testing

Example rule format:

```
IF loan_amount > 100000
AND credit_score < 650
THEN require_manager_approval
```

Advanced users can switch to **structured logic mode**:

```json
{
  "condition": [
    {"loan_amount": {">": 100000}},
    {"credit_score": {"<": 650}}
  ],
  "action": "require_manager_approval"
}
```

---

### 2. Control Policies

Higher-level governance policies.

**Examples:**
- Approval thresholds
- Risk tolerance
- Regulatory compliance checks
- Escalation paths

```yaml
Policy: High Risk Transaction
Trigger: transaction_risk_score > 0.8
Action:
  - halt automation
  - notify compliance team
```

---

### 3. Agent Access Gateway

Agents don't embed rules directly — they call G.A.R.D.

```http
POST /evaluate-decision
```

**Request:**
```json
{
  "agent": "loan_assistant",
  "process": "loan_underwriting",
  "data": {
    "loan_amount": 150000,
    "credit_score": 640
  }
}
```

**Response:**
```json
{
  "decision": "requires_manager_approval",
  "rules_triggered": ["rule_loan_risk_01"]
}
```

This ensures **centralized governance** — rules live in one place, not scattered across agents.

---

### 4. Decision Trace

Every decision must be explainable. G.A.R.D. logs:

- Rule triggered
- Agent requesting decision
- Data used
- Decision outcome
- Timestamp

```
Decision ID: 98432

Agent: LoanAssistantAI
Process: Loan Underwriting

Triggered Rules:
  - LoanRiskRule01
  - CreditScoreThreshold

Outcome: Manager approval required
```

This becomes **audit-ready AI governance**.

---

### 5. Simulation Lab

Before deploying rules, users can simulate against test data.

| credit_score | loan_amount | expected            |
|-------------|-------------|---------------------|
| 620         | 150000      | approval required   |

```
PASS
Rule: LoanRiskRule01 triggered correctly
```

This prevents **bad rules from breaking processes**.

---

### 6. Process View

Instead of just listing rules, show **rules mapped to business processes**.

```
Loan Underwriting Process

  Step 1: Identity Verification
  Step 2: Risk Evaluation
  Step 3: Approval Logic
```

Clicking **Risk Evaluation** shows:

```
Active Rules:
  • CreditScoreThreshold
  • DebtRatioCheck
  • LoanAmountLimit
```

---

### 7. Monitoring Dashboard

Real-time view of agent decisions.

**Metrics:**
- Rules triggered today
- Blocked decisions
- Agent activity
- Policy violations

**Dashboard widgets:**
- Top Triggered Rules
- High Risk Escalations
- Agent Decisions by Process

---

### 8. Rule Lifecycle Management

Enterprise governance requires lifecycle control.

**States:**
```
Draft → Testing → Approved → Active → Deprecated
```

**Approval workflow:**
```
Business Author → Risk Review → Activate
```

---

### 9. Human Override

Critical feature for agent systems.

```
Agent Recommendation: Reject Loan
Manager Override: Approve
Reason: VIP customer
```

Override feedback can **improve agents over time**.

---

## Decision Intelligence (The Differentiator)

G.A.R.D. isn't just a rule engine — it's a **Decision Intelligence System**. Agents don't just follow rules. They learn from how rules are used, overridden, and where they fail.

### Decision Memory

Every decision an agent asks G.A.R.D. for gets stored, building a **decision dataset** over time.

```
Agent: InvoiceAgent
Process: Vendor Payment

Input:
  invoice_amount = 55,000
  vendor_risk_score = 0.82

Rule Triggered: HighRiskVendorPolicy
Outcome: Payment Held
```

At scale, this dataset becomes the foundation for adaptive governance.

---

### Override Intelligence

Track when humans override rules and detect patterns.

```
Rule: Reject if credit_score < 650
Agent decision: Reject

Manager override: Approve
Reason: Long customer history
```

G.A.R.D. detects: *"This rule is overridden 38% of the time."*

**Suggested rule improvement:**

```
IF credit_score < 650
AND customer_tenure < 2 years
THEN reject
```

The system **evolves with the business**.

---

### Rule Impact Analysis

Before changing a rule, G.A.R.D. shows the blast radius:

```
If this rule changes:

  Processes affected:    6
  Agents affected:       12
  Avg decisions/day:     8,420
  Revenue exposure:      $2.4M
```

---

### Guardrail Confidence Score

Each rule gets a reliability score based on decision history.

```
Rule Reliability

  LoanRiskRule01          Confidence: 92%
  CreditScoreRejectRule   Confidence: 61%  ⚠ High override rate
```

Turns rule management into **data science for governance**.

---

### Process Heatmap

Show where automation is breaking down across business processes.

```
Loan Approval Process

  Identity Verification    ✅ Stable
  Risk Evaluation          ⚠ Frequent overrides
  Approval Logic           ❌ Policy conflicts
```

Leaders see **where the process itself is weak**, not just which rules fired.

---

### Natural Language Rule Creation

Business users write rules in plain English:

> "Require approval for invoices over 50k from new vendors."

G.A.R.D. converts it:

```
IF vendor_age < 12 months
AND invoice_amount > 50000
THEN require_approval
```

---

## Architecture

```
                 AI Agents
                     │
                     ▼
             G.A.R.D API Layer
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
    Rules Engine          Policy Engine
         │                       │
         └───────────┬───────────┘
                     ▼
           Decision Memory
          + Override Intelligence
          + Audit Trail
```

---

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 20+
- npm

### Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
ng serve
```

Frontend runs at `http://localhost:4200`.

---

## Tech Stack

| Layer         | Technology              |
|---------------|-------------------------|
| Frontend      | Angular                 |
| Backend       | Node / Python           |
| Rules Engine  | JSON Logic or custom DSL|
| Storage       | Rules, Policies, Decision Logs |

---

## The Vision

> **G.A.R.D. is the governance control plane for agentic enterprises.**

Agents make decisions. **G.A.R.D. decides the rules of the game.**
