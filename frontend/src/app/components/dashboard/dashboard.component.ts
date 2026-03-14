import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="dashboard">
      <h1>G.A.R.D. Dashboard</h1>
      <p class="subtitle">Governance for Agentic Rules &amp; Decisions</p>

      <div class="status-bar">
        <span class="status" [class.online]="healthOk" [class.offline]="!healthOk">
          API: {{ healthOk ? 'Online' : 'Offline' }}
        </span>
      </div>

      <div class="cards">
        <a routerLink="/rules" class="card">
          <h3>Rules</h3>
          <span class="count">{{ ruleCount }}</span>
          <p>Active governance rules</p>
        </a>
        <a routerLink="/decision-logs" class="card">
          <h3>Decision Logs</h3>
          <span class="count">{{ logCount }}</span>
          <p>Traced decisions</p>
        </a>
        <div class="card">
          <h3>Agents</h3>
          <span class="count">{{ agentCount }}</span>
          <p>Registered agents</p>
        </div>
        <div class="card">
          <h3>Processes</h3>
          <span class="count">{{ processCount }}</span>
          <p>Business processes</p>
        </div>
        <a routerLink="/simulation-lab" class="card">
          <h3>Simulation Lab</h3>
          <p>Test rules before deploying</p>
        </a>
      </div>
    </div>
  `,
  styles: [`
    .dashboard { padding: 2rem; max-width: 960px; margin: 0 auto; }
    .subtitle { color: #666; margin-top: -0.5rem; margin-bottom: 1.5rem; }
    .status-bar { margin-bottom: 1.5rem; }
    .status {
      padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500;
    }
    .online { background: #d4edda; color: #155724; }
    .offline { background: #f8d7da; color: #721c24; }
    .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
    .card {
      background: #fff; border: 1px solid #e0e0e0; border-radius: 8px;
      padding: 1.25rem; text-decoration: none; color: inherit; transition: box-shadow 0.2s;
    }
    .card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .card h3 { margin: 0 0 0.25rem; font-size: 1rem; color: #333; }
    .count { font-size: 2rem; font-weight: 700; color: #1a73e8; }
    .card p { margin: 0.25rem 0 0; font-size: 0.85rem; color: #888; }
  `]
})
export class DashboardComponent implements OnInit {
  healthOk = false;
  ruleCount = 0;
  logCount = 0;
  agentCount = 0;
  processCount = 0;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getHealth().subscribe({
      next: () => this.healthOk = true,
      error: () => this.healthOk = false,
    });
    this.api.getRules().subscribe(r => this.ruleCount = r.length);
    this.api.getDecisionLogs().subscribe(l => this.logCount = l.length);
    this.api.getAgents().subscribe(a => this.agentCount = a.length);
    this.api.getProcesses().subscribe(p => this.processCount = p.length);
  }
}
