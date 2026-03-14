import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Rule, Process } from '../../models/api.models';

interface Condition {
  variable: string;
  operator: string;
  value: string;
}

@Component({
  selector: 'app-rule-studio',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './rule-studio.component.html',
  styleUrl: './rule-studio.component.scss',
})
export class RuleStudioComponent implements OnInit {
  mode: 'create' | 'edit' = 'create';
  ruleId: string | null = null;

  // Form fields
  code = '';
  name = '';
  description = '';
  processId: string | null = null;
  action = '';
  priority = 100;
  status = 'draft';
  combinator: 'and' | 'or' = 'and';
  conditions: Condition[] = [{ variable: '', operator: '>', value: '' }];

  processes: Process[] = [];
  saving = false;
  error = '';

  operators = [
    { value: '>', label: 'greater than' },
    { value: '>=', label: 'greater than or equal' },
    { value: '<', label: 'less than' },
    { value: '<=', label: 'less than or equal' },
    { value: '==', label: 'equals' },
    { value: '!=', label: 'not equals' },
  ];

  statuses = ['draft', 'testing', 'approved', 'active', 'deprecated'];

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private router: Router,
  ) {}

  ngOnInit() {
    this.api.getProcesses().subscribe(p => this.processes = p);

    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.mode = 'edit';
      this.ruleId = id;
      this.api.getRule(id).subscribe({
        next: (rule) => this.loadRule(rule),
        error: () => this.error = 'Rule not found',
      });
    }
  }

  loadRule(rule: Rule) {
    this.code = rule.code;
    this.name = rule.name;
    this.description = rule.description || '';
    this.processId = rule.process_id;
    this.action = rule.action;
    this.priority = rule.priority;
    this.status = rule.status;
    this.parseLogic(rule.logic);
  }

  parseLogic(logic: any) {
    if (!logic) return;

    // Handle {"and": [...]} or {"or": [...]}
    if (logic['and'] || logic['or']) {
      this.combinator = logic['and'] ? 'and' : 'or';
      const items = logic[this.combinator] as any[];
      this.conditions = items.map(item => this.parseCondition(item));
    } else {
      // Single condition
      this.combinator = 'and';
      this.conditions = [this.parseCondition(logic)];
    }
  }

  parseCondition(item: any): Condition {
    // Format: { ">": [{"var": "field"}, value] }
    const op = Object.keys(item)[0];
    const args = item[op];
    const variable = args[0]?.var || '';
    const value = String(args[1] ?? '');
    return { variable, operator: op, value };
  }

  addCondition() {
    this.conditions.push({ variable: '', operator: '>', value: '' });
  }

  removeCondition(index: number) {
    if (this.conditions.length > 1) {
      this.conditions.splice(index, 1);
    }
  }

  buildLogic(): any {
    const parts = this.conditions.map(c => {
      const val = isNaN(Number(c.value)) ? c.value : Number(c.value);
      return { [c.operator]: [{ var: c.variable }, val] };
    });
    if (parts.length === 1) return parts[0];
    return { [this.combinator]: parts };
  }

  getHumanReadable(): string {
    const parts = this.conditions
      .filter(c => c.variable && c.value)
      .map(c => {
        const opLabel = this.operators.find(o => o.value === c.operator)?.label || c.operator;
        return `${c.variable} ${opLabel} ${c.value}`;
      });
    if (parts.length === 0) return 'No conditions defined';
    const joined = parts.join(` ${this.combinator.toUpperCase()} `);
    return `IF ${joined} THEN ${this.action || '___'}`;
  }

  save() {
    this.error = '';
    if (!this.code || !this.name || !this.action) {
      this.error = 'Code, name, and action are required.';
      return;
    }
    if (this.conditions.some(c => !c.variable || !c.value)) {
      this.error = 'All conditions must have a variable and value.';
      return;
    }

    this.saving = true;
    const payload = {
      code: this.code,
      name: this.name,
      description: this.description || undefined,
      process_id: this.processId || undefined,
      logic: this.buildLogic(),
      action: this.action,
      priority: this.priority,
      status: this.status,
    };

    const request = this.mode === 'edit' && this.ruleId
      ? this.api.updateRule(this.ruleId, payload)
      : this.api.createRule(payload as any);

    request.subscribe({
      next: () => this.router.navigate(['/rules']),
      error: (err) => {
        this.saving = false;
        this.error = err.error?.detail || 'Failed to save rule.';
      },
    });
  }

  deleteRule() {
    if (!this.ruleId) return;
    if (!confirm('Delete this rule?')) return;
    this.api.deleteRule(this.ruleId).subscribe({
      next: () => this.router.navigate(['/rules']),
      error: (err) => this.error = err.error?.detail || 'Failed to delete rule.',
    });
  }
}
