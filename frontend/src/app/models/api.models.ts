export interface Agent {
  id: string;
  name: string;
  description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Rule {
  id: string;
  code: string;
  name: string;
  description: string;
  process_id: string | null;
  logic: any;
  action: string;
  priority: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Process {
  id: string;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface Policy {
  id: string;
  code: string;
  name: string;
  description: string;
  process_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface DecisionLog {
  id: string;
  agent_id: string;
  process_code: string;
  input_data: any;
  rules_evaluated: any;
  rules_triggered: any;
  outcome: any;
  decision: string;
  created_at: string;
}

export interface RuleCreate {
  code: string;
  name: string;
  description?: string;
  process_id?: string | null;
  logic: any;
  action: string;
  priority: number;
  status: string;
}

export interface RuleUpdate {
  code?: string;
  name?: string;
  description?: string;
  process_id?: string | null;
  logic?: any;
  action?: string;
  priority?: number;
  status?: string;
}

export interface DecisionRequest {
  agent: string;
  process: string;
  data: Record<string, any>;
}

export interface SimulationTestCase {
  label: string;
  data: Record<string, any>;
  expected_decision: string;
}

export interface SimulationRequest {
  rule_id?: string | null;
  process?: string | null;
  test_cases: SimulationTestCase[];
}

export interface SimulationTestResult {
  label: string;
  data: Record<string, any>;
  expected_decision: string;
  actual_decision: string;
  rules_triggered: string[];
  reasons: string[];
  passed: boolean;
}

export interface SimulationResponse {
  total: number;
  passed: number;
  failed: number;
  results: SimulationTestResult[];
}

export interface DecisionResponse {
  decision_id: string;
  decision: string;
  rules_triggered: string[];
  actions: string[];
  reasons: string[];
  timestamp: string;
}
