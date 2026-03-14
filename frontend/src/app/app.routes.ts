import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { RulesListComponent } from './components/rules-list/rules-list.component';
import { RuleStudioComponent } from './components/rule-studio/rule-studio.component';
import { DecisionLogsComponent } from './components/decision-logs/decision-logs.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'rules', component: RulesListComponent },
  { path: 'rules/new', component: RuleStudioComponent },
  { path: 'rules/:id/edit', component: RuleStudioComponent },
  { path: 'decision-logs', component: DecisionLogsComponent },
];
