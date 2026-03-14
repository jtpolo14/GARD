import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Agent,
  Rule,
  RuleCreate,
  RuleUpdate,
  Process,
  Policy,
  DecisionLog,
  DecisionRequest,
  DecisionResponse,
  SimulationRequest,
  SimulationResponse,
} from '../models/api.models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  // Health
  getHealth(): Observable<{ status: string }> {
    return this.http.get<{ status: string }>(`${this.baseUrl}/health`);
  }

  // Agents
  getAgents(): Observable<Agent[]> {
    return this.http.get<Agent[]>(`${this.baseUrl}/agents`);
  }

  // Processes
  getProcesses(): Observable<Process[]> {
    return this.http.get<Process[]>(`${this.baseUrl}/processes`);
  }

  // Rules
  getRules(): Observable<Rule[]> {
    return this.http.get<Rule[]>(`${this.baseUrl}/rules`);
  }

  getRule(id: string): Observable<Rule> {
    return this.http.get<Rule>(`${this.baseUrl}/rules/${id}`);
  }

  createRule(rule: RuleCreate): Observable<Rule> {
    return this.http.post<Rule>(`${this.baseUrl}/rules`, rule);
  }

  updateRule(id: string, rule: RuleUpdate): Observable<Rule> {
    return this.http.put<Rule>(`${this.baseUrl}/rules/${id}`, rule);
  }

  deleteRule(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/rules/${id}`);
  }

  // Policies
  getPolicies(): Observable<Policy[]> {
    return this.http.get<Policy[]>(`${this.baseUrl}/policies`);
  }

  // Decision Logs
  getDecisionLogs(): Observable<DecisionLog[]> {
    return this.http.get<DecisionLog[]>(`${this.baseUrl}/decision-logs`);
  }

  // Evaluate Decision
  evaluateDecision(req: DecisionRequest): Observable<DecisionResponse> {
    return this.http.post<DecisionResponse>(`${this.baseUrl}/evaluate-decision`, req);
  }

  // Simulation
  runSimulation(req: SimulationRequest): Observable<SimulationResponse> {
    return this.http.post<SimulationResponse>(`${this.baseUrl}/simulate`, req);
  }
}
