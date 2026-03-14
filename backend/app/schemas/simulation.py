from typing import Any

from pydantic import BaseModel


class SimulationTestCase(BaseModel):
    label: str
    data: dict[str, Any]
    expected_decision: str


class SimulationRequest(BaseModel):
    rule_id: str | None = None
    process: str | None = None
    test_cases: list[SimulationTestCase]


class SimulationTestResult(BaseModel):
    label: str
    data: dict[str, Any]
    expected_decision: str
    actual_decision: str
    rules_triggered: list[str]
    reasons: list[str]
    passed: bool


class SimulationResponse(BaseModel):
    total: int
    passed: int
    failed: int
    results: list[SimulationTestResult]
