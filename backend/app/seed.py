"""Seed the database with initial data."""

import json

from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Agent, DecisionLog, Policy, Process, Rule
from app.database import Base


def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Agent).first():
            print("Database already seeded, skipping.")
            return

        # Agents
        loan_assistant = Agent(name="loan_assistant", description="AI loan processing assistant")
        invoice_agent = Agent(name="invoice_agent", description="AI invoice processing agent")
        db.add_all([loan_assistant, invoice_agent])
        db.flush()

        # Processes
        loan_underwriting = Process(
            name="loan_underwriting", description="Loan underwriting and risk assessment"
        )
        vendor_payment = Process(
            name="vendor_payment", description="Vendor payment processing"
        )
        db.add_all([loan_underwriting, vendor_payment])
        db.flush()

        # Rules
        rules = [
            Rule(
                code="rule_loan_risk_01",
                name="High Risk Loan",
                description="Flag loans over 100k with credit score below 650",
                process_id=loan_underwriting.id,
                logic=json.dumps({
                    "and": [
                        {">": [{"var": "loan_amount"}, 100000]},
                        {"<": [{"var": "credit_score"}, 650]},
                    ]
                }),
                action="require_manager_approval",
                priority=10,
            ),
            Rule(
                code="rule_loan_auto_approve",
                name="Auto Approve Small Loan",
                description="Auto-approve loans under 50k with good credit",
                process_id=loan_underwriting.id,
                logic=json.dumps({
                    "and": [
                        {"<=": [{"var": "loan_amount"}, 50000]},
                        {">=": [{"var": "credit_score"}, 700]},
                    ]
                }),
                action="auto_approve",
                priority=20,
            ),
            Rule(
                code="rule_high_risk_vendor",
                name="High Risk Vendor",
                description="Hold payments for high-risk vendors",
                process_id=vendor_payment.id,
                logic=json.dumps({">": [{"var": "vendor_risk_score"}, 0.8]}),
                action="hold_payment",
                priority=10,
            ),
            Rule(
                code="rule_large_invoice",
                name="Large Invoice Approval",
                description="Require approval for invoices over 50k",
                process_id=vendor_payment.id,
                logic=json.dumps({">": [{"var": "invoice_amount"}, 50000]}),
                action="require_approval",
                priority=20,
            ),
        ]
        db.add_all(rules)

        # Policies
        policies = [
            Policy(
                code="high_risk_transaction_policy",
                name="High Risk Transaction Policy",
                description="Policy governing high-risk transaction handling",
                process_id=loan_underwriting.id,
            ),
            Policy(
                code="approval_threshold_policy",
                name="Approval Threshold Policy",
                description="Policy for approval thresholds across processes",
            ),
        ]
        db.add_all(policies)

        db.commit()
        print("Database seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
