// Context / Scope / Model Advisor v1
// Portable contract for Agent Memory Kit v3.9.3. No runtime dependencies.

export type AdvisorIntent =
  | 'answer'
  | 'analyze'
  | 'plan'
  | 'apply'
  | 'audit'
  | 'repair'
  | 'recover'
  | 'resume'
  | 'debug'
  | 'research'
  | 'prompt_optimize'
  | 'project_map_update'
  | 'handoff_package_update';

export type MutationKind = 'none' | 'docs' | 'code' | 'memory' | 'db' | 'deploy' | 'git' | 'external';
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type SufficiencyGate = 'green' | 'amber' | 'red' | 'blocked';

export type AdvisorProfile =
  | 'answer_project'
  | 'analyze_project'
  | 'plan_change'
  | 'apply_change'
  | 'debug_runtime'
  | 'audit_contract'
  | 'repair_state'
  | 'recover_context'
  | 'resume_task'
  | 'research_external'
  | 'prompt_token_optimize'
  | 'project_map_update'
  | 'handoff_package_update';

export type ContextClass =
  | 'project_map_core'
  | 'source_authority'
  | 'memory_relevant'
  | 'active_workstream'
  | 'progress_logs'
  | 'routes_contracts'
  | 'services_logic'
  | 'db_schema'
  | 'scraper_jobs'
  | 'redis_cache'
  | 'mt_client'
  | 'tests'
  | 'runtime_logs'
  | 'external_current_docs'
  | 'screenshots_ui'
  | 'diff_refs'
  | 'provider_capability_snapshot'
  | 'side_effect_receipts'
  | 'secrets';

export type Surface = 'chatgpt' | 'cursor' | 'codex_ide' | 'deep_research' | 'web' | 'other';
export type ReasoningEffort = 'none' | 'low' | 'medium' | 'high' | 'extra' | 'extra_high' | 'max' | 'pro' | 'xhigh' | 'provider_default';
export type SpeedMode = 'standard' | 'fast' | 'auto' | 'provider_default';
export type CursorModelId = 'auto' | 'composer_2_5' | 'gpt_5_3_codex' | 'codex_5_3' | 'gpt_5_5' | 'sonnet_4_6' | 'opus_4_8' | 'fable_5' | 'gemini_3_1_pro' | 'grok_4_3_or_grok_build' | 'other';
export type CursorModelControl = 'fast' | 'thinking' | 'context_200k' | 'context_272k' | 'context_300k' | 'context_1m' | 'reasoning' | 'effort' | 'none';
export type ContextMode = 'explicit_refs_only' | 'implicit_ide_advisory' | 'ide_context' | 'max_mode' | 'full_repo_forbidden' | 'provider_default';
export type HintMode = 'silent' | 'compact' | 'expanded' | 'blocking';
export type ModelCostClass = 'economy' | 'standard' | 'premium' | 'optional' | 'unknown';
export type CapabilityNeed = 'simple' | 'bounded' | 'complex' | 'critical';
export type RefKind = 'file' | 'folder' | 'memory_unit' | 'workstream' | 'artifact' | 'external_snapshot' | 'log' | 'screenshot' | 'command' | 'url' | 'ide_context';

export interface EvidenceRef {
  kind: RefKind;
  ref: string;
  title?: string;
  reason: string;
  required: boolean;
  volatile?: boolean;
  containsSecrets?: boolean;
}

export interface TaskBrief {
  id: string;
  rawUserRequest: string;
  normalizedGoal: string;
  intent: AdvisorIntent;
  mutation: MutationKind;
  risk: RiskLevel;
  explicitScope: EvidenceRef[];
  implicitContextRefs?: EvidenceRef[];
  requestedOutput: string[];
  language: 'ru' | 'en' | 'mixed' | 'other';
  ownerOk?: boolean;
  verificationProvided?: boolean;
  notes?: string[];
}

export interface ProviderCapabilitySnapshot {
  id: string;
  capturedAt: string;
  expiresAt: string;
  sourceRefs: EvidenceRef[];
  surfaces: SurfaceCapability[];
  notes?: string[];
}

export interface SurfaceCapability {
  surface: Surface;
  provider?: string;
  modelOrModelClass?: string;
  supportsReasoning?: boolean;
  supportedReasoning?: ReasoningEffort[];
  supportsMaxMode?: boolean;
  maxContextTokens?: number;
  defaultContextTokens?: number;
  supportsFastMode?: boolean;
  supportsIdeContext?: boolean;
  supportsTools?: boolean;
  approvalModes?: string[];
  pricingNotes?: string[];
  dataRetentionNotes?: string[];
  capturedAt?: string;
  expiresAt?: string;
  sourceRefIds?: string[];
}

export type CursorModelRouterRole =
  | 'default_working_horse'
  | 'code_test_repair_executor'
  | 'hard_reasoning_escalation'
  | 'balanced_review_refactor'
  | 'rare_hard_planning_audit'
  | 'rare_long_running_agentic'
  | 'optional_huge_multimodal_fallback'
  | 'optional_fast_coding_experiment'
  | 'other';

export interface CursorModelControls {
  options: string[];
  context: string[];
  reasoningOrEffort: ReasoningEffort[];
}

export interface CursorModelRouteEntry {
  id: CursorModelId;
  display: string;
  provider?: string;
  routerRole: CursorModelRouterRole;
  core: boolean;
  optional: boolean;
  defaultFor: AdvisorIntent[] | string[];
  controls: CursorModelControls;
  defaultSettings?: Record<string, string | boolean | number>;
  escalationNotes: string[];
}

export interface CursorProviderModelSnapshot extends ProviderCapabilitySnapshot {
  snapshotKind: 'cursor_model_routing';
  ownerUiObservedAt: string;
  coreModels: CursorModelRouteEntry[];
  optionalModels: CursorModelRouteEntry[];
  exactModelAdviceRequiresSnapshotDate: boolean;
  optionalModelsRequireCapabilityGap: boolean;
}


export interface CursorModelCapabilityObserved {
  modelId: CursorModelId;
  displayName: string;
  observedInCursorUiAt: string;
  options: CursorModelControl[];
  contextTokenChoices?: number[];
  reasoningOrEffortChoices?: ReasoningEffort[];
  defaultFor: string[];
  avoidAsDefaultFor?: string[];
  premiumRouteRequiresReason: boolean;
  notes?: string[];
}

export interface CursorModelRoutingMatrix {
  version: string;
  collectedAt: string;
  expiresAt: string;
  evidenceRefs: EvidenceRef[];
  models: CursorModelCapabilityObserved[];
  routingRules: CursorTaskRoute[];
  refreshTriggers: string[];
}

export interface CursorTaskRoute {
  taskClass: string;
  defaultModel: CursorModelId;
  fallbackModels: CursorModelId[];
  defaultReasoningOrEffort?: ReasoningEffort;
  defaultSpeed?: SpeedMode;
  defaultContextTokens?: number;
  maxContextRequiresReason: boolean;
  planMode: 'on' | 'off' | 'ask' | 'provider_default';
  escalationTriggers: string[];
  why: string;
}

export interface ContextNeed {
  contextClass: ContextClass;
  reason: string;
  priority: 'mandatory' | 'recommended' | 'optional' | 'forbidden';
  suggestedRefs: EvidenceRef[];
  maxTokens?: number;
}

export interface ContextNeedsManifest {
  id: string;
  taskId: string;
  profile: AdvisorProfile;
  mandatory: ContextNeed[];
  recommended: ContextNeed[];
  optional: ContextNeed[];
  forbidden: ContextNeed[];
  likelyMissing: ContextNeed[];
  highRiskOmissions: string[];
  tokenBudget: TokenBudgetPlan;
}

export interface TokenBudgetPlan {
  maxPromptTokens?: number;
  mandatoryContextPercent: number;
  codeDocsPercent: number;
  stateProgressPercent: number;
  testsLogsEvidencePercent: number;
  instructionsOutputPercent: number;
  deferredRefs: EvidenceRef[];
  excludedRefs: EvidenceRef[];
  rawEscalationRequired: boolean;
}

export interface ScopeSufficiencyReport {
  gate: SufficiencyGate;
  score0to100: number;
  reasons: string[];
  missingMandatory: ContextNeed[];
  overBroadRefs: EvidenceRef[];
  unsafeRefs: EvidenceRef[];
  recommendedAction: 'proceed' | 'proceed_with_warning' | 'ask_user' | 'run_readonly_discovery' | 'block';
}

export interface RoutingRecommendation {
  surface: Surface;
  provider?: string;
  modelOrModelClass?: string;
  reasoning: ReasoningEffort;
  speed: SpeedMode;
  contextMode: ContextMode;
  maxMode: 'on' | 'off' | 'auto' | 'provider_default';
  includeIdeContext: 'on' | 'off' | 'only_exact_open_files' | 'provider_default';
  planMode: 'on' | 'off' | 'ask' | 'provider_default';
  approvalMode: 'chat' | 'agent' | 'agent_full_access' | 'read_only' | 'owner_approval_required' | 'provider_default';
  costClass: ModelCostClass;
  capabilityNeed: CapabilityNeed;
  cheaperAlternative?: string;
  premiumEscalationReasons: string[];
  whyNotCheaper?: string[];
  rationale: string[];
  volatileSnapshotRef?: string;
  providerSnapshotCapturedAt?: string;
  modelControlsRef?: string;
  optionalModelGap?: string;
}

export interface UserHint {
  mode: HintMode;
  compactText: string;
  expandedMarkdown?: string;
  triggerReasons: string[];
}

export interface HydrationRequestDraft {
  profile: string;
  taskId: string;
  mandatoryRefs: EvidenceRef[];
  optionalRefs: EvidenceRef[];
  forbiddenRefs: EvidenceRef[];
  tokenBudget: TokenBudgetPlan;
  branchScope?: {
    branchId?: string;
    checkpointId?: string;
    allowFutureFacts: boolean;
  };
}

export interface PolicyViolation {
  code:
    | 'missing_mandatory_context'
    | 'overbroad_scope'
    | 'secret_ref_detected'
    | 'owner_ok_missing'
    | 'verification_missing'
    | 'branch_lineage_ambiguous'
    | 'duplicate_side_effect_risk'
    | 'provider_snapshot_stale'
    | 'provider_model_snapshot_missing'
    | 'provider_model_snapshot_stale'
    | 'unsupported_model_control'
    | 'context_window_over_escalated'
    | 'implicit_ide_context_unscoped'
    | 'unsafe_mutation_mode'
    | 'premium_model_without_escalation_reason'
    | 'reasoning_over_escalated'
    | 'cheaper_alternative_missing'
    | 'provider_model_snapshot_missing'
    | 'provider_model_snapshot_stale'
    | 'fast_mode_without_time_pressure'
    | 'large_context_without_scope_need'
    | 'optional_model_without_capability_gap'
    | 'model_over_capable_for_narrow_task';
  severity: RiskLevel;
  message: string;
  refs: EvidenceRef[];
}

export interface ContextAdvisorTrace {
  id: string;
  createdAt: string;
  task: TaskBrief;
  profile: AdvisorProfile;
  contextManifest: ContextNeedsManifest;
  sufficiency: ScopeSufficiencyReport;
  routing: RoutingRecommendation;
  userHint: UserHint;
  hydrationDraft: HydrationRequestDraft;
  violations: PolicyViolation[];
  unresolvedQuestions: string[];
  deterministicInputs: string[];
}

export interface AdvisorProfileSpec {
  profile: AdvisorProfile;
  intents: AdvisorIntent[];
  defaultRisk: RiskLevel;
  mandatoryContextClasses: ContextClass[];
  recommendedContextClasses: ContextClass[];
  optionalContextClasses: ContextClass[];
  forbiddenContextClasses: ContextClass[];
  defaultSurface: Surface;
  fallbackSurface?: Surface;
  defaultProvider?: string;
  defaultModelOrModelClass: string;
  defaultReasoning: ReasoningEffort;
  defaultSpeed: SpeedMode;
  defaultContextMode: ContextMode;
  defaultCostClass: ModelCostClass;
  defaultCapabilityNeed: CapabilityNeed;
  cheaperAlternative?: string;
  premiumRequiresExplicitReason: boolean;
  premiumEscalationTriggers: string[];
  maxModeDefault: 'on' | 'off' | 'auto' | 'provider_default';
  includeIdeContextDefault: 'on' | 'off' | 'only_exact_open_files' | 'provider_default';
  implicitIdeContextPolicy?: 'advisory_only' | 'allowed_when_exact_scope' | 'forbidden_for_scope_expansion' | 'provider_default';
  planModeDefault: 'on' | 'off' | 'ask' | 'provider_default';
  blockingConditions: string[];
  compactHintTemplate: string;
  providerSnapshotRef?: string;
  providerSnapshotCapturedAt?: string;
  modelSetPolicy?: 'core_models_first_optional_models_only_with_gap' | 'provider_default';
}

export interface ContextAdvisorPolicyV1 {
  version: '1.0.0' | '1.0.1' | '1.0.2' | '1.0.3';
  profiles: AdvisorProfileSpec[];
  defaultHintMode: HintMode;
  expandedHintTriggers: string[];
  providerSnapshotTtlHours: number;
  rules: string[];
}
