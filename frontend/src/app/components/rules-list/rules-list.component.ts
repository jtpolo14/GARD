import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Rule } from '../../models/api.models';

@Component({
  selector: 'app-rules-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="rules-page">
      <div class="header">
        <div>
          <h2>Rules</h2>
          <a routerLink="/" class="back-link">&larr; Dashboard</a>
        </div>
        <a routerLink="/rules/new" class="create-btn">+ New Rule</a>
      </div>

      <table *ngIf="rules.length > 0">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Action</th>
            <th>Priority</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let rule of rules">
            <td><code>{{ rule.code }}</code></td>
            <td>{{ rule.name }}</td>
            <td><span class="action-badge">{{ rule.action }}</span></td>
            <td>{{ rule.priority }}</td>
            <td><span class="status-badge" [class]="rule.status">{{ rule.status }}</span></td>
            <td><a [routerLink]="['/rules', rule.id, 'edit']" class="edit-link">Edit</a></td>
          </tr>
        </tbody>
      </table>

      <p *ngIf="rules.length === 0 && !loading" class="empty">No rules found.</p>
      <p *ngIf="loading" class="empty">Loading...</p>
    </div>
  `,
  styles: [`
    .rules-page { padding: 2rem; max-width: 960px; margin: 0 auto; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .back-link { text-decoration: none; color: #1a73e8; font-size: 0.85rem; }
    .create-btn {
      background: #1a73e8; color: #fff; text-decoration: none; padding: 0.5rem 1rem;
      border-radius: 6px; font-size: 0.85rem; font-weight: 600;
    }
    .create-btn:hover { background: #1557b0; }
    .edit-link { color: #1a73e8; text-decoration: none; font-size: 0.85rem; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid #e0e0e0; }
    th { font-weight: 600; color: #555; font-size: 0.85rem; text-transform: uppercase; }
    code { background: #f5f5f5; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.85rem; }
    .action-badge {
      background: #e8f0fe; color: #1a73e8; padding: 0.2rem 0.5rem;
      border-radius: 4px; font-size: 0.8rem; font-weight: 500;
    }
    .status-badge {
      padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500;
    }
    .active { background: #d4edda; color: #155724; }
    .draft { background: #fff3cd; color: #856404; }
    .deprecated { background: #f8d7da; color: #721c24; }
    .empty { color: #888; text-align: center; padding: 2rem; }
  `]
})
export class RulesListComponent implements OnInit {
  rules: Rule[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getRules().subscribe({
      next: (rules) => { this.rules = rules; this.loading = false; },
      error: () => this.loading = false,
    });
  }
}
