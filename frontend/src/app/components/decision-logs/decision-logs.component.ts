import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { DecisionLog } from '../../models/api.models';

@Component({
  selector: 'app-decision-logs',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="logs-page">
      <div class="header">
        <h2>Decision Logs</h2>
        <a routerLink="/" class="back-link">&larr; Dashboard</a>
      </div>

      <table *ngIf="logs.length > 0">
        <thead>
          <tr>
            <th>Time</th>
            <th>Process</th>
            <th>Decision</th>
            <th>Rules Triggered</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let log of logs">
            <td>{{ log.created_at | date:'short' }}</td>
            <td>{{ log.process_code }}</td>
            <td><span class="decision-badge">{{ log.decision }}</span></td>
            <td>
              <span *ngFor="let r of parseTriggered(log.rules_triggered)" class="rule-chip">
                {{ r.code }}
              </span>
              <span *ngIf="parseTriggered(log.rules_triggered).length === 0" class="none">none</span>
            </td>
          </tr>
        </tbody>
      </table>

      <p *ngIf="logs.length === 0 && !loading" class="empty">No decision logs yet.</p>
      <p *ngIf="loading" class="empty">Loading...</p>
    </div>
  `,
  styles: [`
    .logs-page { padding: 2rem; max-width: 960px; margin: 0 auto; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .back-link { text-decoration: none; color: #1a73e8; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid #e0e0e0; }
    th { font-weight: 600; color: #555; font-size: 0.85rem; text-transform: uppercase; }
    .decision-badge {
      background: #e8f0fe; color: #1a73e8; padding: 0.2rem 0.5rem;
      border-radius: 4px; font-size: 0.8rem; font-weight: 500;
    }
    .rule-chip {
      background: #f5f5f5; padding: 0.15rem 0.4rem; border-radius: 3px;
      font-size: 0.8rem; margin-right: 0.25rem;
    }
    .none { color: #aaa; font-size: 0.8rem; }
    .empty { color: #888; text-align: center; padding: 2rem; }
  `]
})
export class DecisionLogsComponent implements OnInit {
  logs: DecisionLog[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getDecisionLogs().subscribe({
      next: (logs) => { this.logs = logs; this.loading = false; },
      error: () => this.loading = false,
    });
  }

  parseTriggered(value: any): any[] {
    if (typeof value === 'string') {
      try { return JSON.parse(value); } catch { return []; }
    }
    return Array.isArray(value) ? value : [];
  }
}
