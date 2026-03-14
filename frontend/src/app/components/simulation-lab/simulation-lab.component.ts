import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Rule, Process, SimulationTestResult } from '../../models/api.models';

interface TestCaseRow {
  label: string;
  dataJson: string;
  expected_decision: string;
}

@Component({
  selector: 'app-simulation-lab',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './simulation-lab.component.html',
  styleUrl: './simulation-lab.component.scss',
})
export class SimulationLabComponent implements OnInit {
  rules: Rule[] = [];
  processes: Process[] = [];

  selectedRuleId: string | null = null;
  selectedProcess: string | null = null;
  testCases: TestCaseRow[] = [
    { label: 'Test 1', dataJson: '{}', expected_decision: '' },
  ];

  results: SimulationTestResult[] | null = null;
  summary = { total: 0, passed: 0, failed: 0 };
  running = false;
  error = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getRules().subscribe(r => this.rules = r);
    this.api.getProcesses().subscribe(p => this.processes = p);
  }

  addTestCase() {
    const num = this.testCases.length + 1;
    this.testCases.push({ label: `Test ${num}`, dataJson: '{}', expected_decision: '' });
  }

  removeTestCase(index: number) {
    if (this.testCases.length > 1) {
      this.testCases.splice(index, 1);
    }
  }

  run() {
    this.error = '';
    this.results = null;

    // Validate
    for (const tc of this.testCases) {
      if (!tc.expected_decision) {
        this.error = `"${tc.label}" is missing an expected decision.`;
        return;
      }
      try {
        JSON.parse(tc.dataJson);
      } catch {
        this.error = `"${tc.label}" has invalid JSON data.`;
        return;
      }
    }

    this.running = true;
    this.api.runSimulation({
      rule_id: this.selectedRuleId || undefined,
      process: this.selectedProcess || undefined,
      test_cases: this.testCases.map(tc => ({
        label: tc.label,
        data: JSON.parse(tc.dataJson),
        expected_decision: tc.expected_decision,
      })),
    }).subscribe({
      next: (res) => {
        this.results = res.results;
        this.summary = { total: res.total, passed: res.passed, failed: res.failed };
        this.running = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Simulation failed.';
        this.running = false;
      },
    });
  }

  prefillFromRule() {
    if (!this.selectedRuleId) return;
    const rule = this.rules.find(r => r.id === this.selectedRuleId);
    if (!rule) return;

    // Extract variables from the rule's logic to build a template
    const vars = this.extractVars(rule.logic);
    const template: Record<string, string> = {};
    vars.forEach(v => template[v] = '');

    this.testCases = [
      {
        label: `${rule.code} - should trigger`,
        dataJson: JSON.stringify(template, null, 2),
        expected_decision: rule.action,
      },
      {
        label: `${rule.code} - should not trigger`,
        dataJson: JSON.stringify(template, null, 2),
        expected_decision: 'no_action',
      },
    ];
  }

  private extractVars(logic: any): string[] {
    const vars: string[] = [];
    const walk = (node: any) => {
      if (!node || typeof node !== 'object') return;
      if (node.var !== undefined) {
        vars.push(String(node.var));
        return;
      }
      for (const val of Object.values(node)) {
        if (Array.isArray(val)) val.forEach(walk);
        else walk(val);
      }
    };
    walk(logic);
    return [...new Set(vars)];
  }
}
