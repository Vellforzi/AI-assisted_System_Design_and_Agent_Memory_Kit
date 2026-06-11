#!/usr/bin/env python3
"""Context Advisor preflight helper for Agent Memory Kit.

This optional helper is intentionally simple and local. It does not call model APIs,
read project files, or perform writes. It loads the profile matrix and emits a
compact advisory gate for the current task, including cost-aware model routing and dated provider/model snapshots.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROFILE_FILE = Path(__file__).resolve().parents[1] / "context_advisor" / "context_advisor_v1.profile_matrix.json"
ROUTING_MATRIX_FILE = Path(__file__).resolve().parents[1] / "context_advisor" / "cursor_model_routing_matrix.v1.json"
SURFACE_MATRIX_FILE = Path(__file__).resolve().parents[1] / "context_advisor" / "execution_surface_routing_matrix.v1.json"


def load_profiles(path: Path = PROFILE_FILE) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    profiles = data.get("profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("profile_matrix.json must contain a profiles list")
    return profiles


def load_routing_matrix(path: Path = ROUTING_MATRIX_FILE) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def load_surface_matrix(path: Path = SURFACE_MATRIX_FILE) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def choose_profile(profiles: list[dict[str, Any]], intent: str) -> dict[str, Any]:
    for profile in profiles:
        if intent in profile.get("intents", []):
            return profile
    raise ValueError(f"No Context Advisor profile for intent: {intent}")


def parse_csv(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}



def normalized_model_name(value: str | None) -> str:
    if not value:
        return ""
    return value.lower().replace(" ", "_").replace("-", "_").replace(".", "_")


def make_report(args: argparse.Namespace) -> dict[str, Any]:
    profiles = load_profiles()
    routing_matrix = load_routing_matrix()
    surface_matrix = load_surface_matrix()
    profile = choose_profile(profiles, args.intent)
    have = parse_csv(args.have)
    scope_refs = [s for s in (args.scope or []) if s.strip()]
    mandatory = set(profile.get("mandatoryContextClasses", []))
    forbidden = set(profile.get("forbiddenContextClasses", []))
    missing = sorted(mandatory - have)
    unsafe = []
    for ref in scope_refs:
        lowered = ref.lower()
        if any(mark in lowered for mark in ["secret", "password", "token", "access", "доступ"]):
            unsafe.append(ref)
    blocking = []
    if unsafe:
        blocking.append("secret_ref_detected")
    if args.intent == "apply" and not args.owner_ok:
        blocking.append("owner_ok_missing")
    if args.intent == "apply" and not args.verification:
        blocking.append("verification_missing")
    if args.mutation in {"db", "deploy", "git"} and not args.owner_ok:
        blocking.append(f"{args.mutation}_mutation_without_owner_ok")
    if args.implicit_ide_context and not args.implicit_ide_approved:
        blocking.append("implicit_ide_context_unscoped")

    cost_warnings = []
    premium_reasons = parse_csv(args.premium_justification)
    requested_model = args.requested_model or profile.get("defaultCursorModelPreference") or "provider_default"
    snapshot_ref = routing_matrix.get("matrixId") if routing_matrix else None
    if args.model_routing_requested and not routing_matrix:
        cost_warnings.append("provider_model_snapshot_missing")
    if args.model_routing_requested and routing_matrix and not args.provider_snapshot_current:
        cost_warnings.append("provider_model_snapshot_not_confirmed_current")
    if requested_model == "auto" and args.intent in {"project_map_update", "handoff_package_update", "apply", "audit", "repair", "recover"} and not args.owner_ok:
        cost_warnings.append("auto_mode_without_owner_acceptance")
    if requested_model == "auto" and (args.context_1m or args.large_context):
        cost_warnings.append("max_mode_not_applicable_to_auto")
    if requested_model == "composer_2_5" and args.high_reasoning:
        cost_warnings.append("unsupported_model_control_composer_2_5_reasoning")
    if args.context_1m and args.intent in {"project_map_update", "answer", "prompt_optimize"} and not premium_reasons:
        cost_warnings.append("context_window_over_escalated")
    if args.premium_model and not premium_reasons:
        cost_warnings.append("premium_model_without_escalation_reason")
    if requested_model in {"fable_5", "opus_4_8"} and not premium_reasons:
        cost_warnings.append("premium_model_without_escalation_reason")
    if args.high_reasoning and args.intent in {"project_map_update", "answer", "prompt_optimize"} and not premium_reasons:
        cost_warnings.append("reasoning_over_escalated")

    model_name = normalized_model_name(args.model_name)
    narrow_intents = {"project_map_update", "answer", "prompt_optimize"}
    if model_name and args.intent in narrow_intents and any(mark in model_name for mark in ["gpt_5_5", "opus", "fable"]):
        if not premium_reasons:
            cost_warnings.append("model_over_capable_for_narrow_task")
    if model_name and any(mark in model_name for mark in ["opus", "fable"]):
        if not premium_reasons:
            cost_warnings.append("rare_escalation_model_without_trigger")
    if args.fast_mode and not ({"time_critical", "low_risk_speed_sensitive", "draft_only"} & premium_reasons):
        cost_warnings.append("fast_mode_without_time_pressure")
    if args.large_context and not ({"context_overflow", "huge_context", "large_cross_repo_audit", "multimodal_huge_context"} & premium_reasons):
        cost_warnings.append("large_context_without_scope_need")
    if args.optional_model and not args.optional_model_gap:
        cost_warnings.append("optional_model_without_capability_gap")
    if args.settings_requested and not args.provider_snapshot_date:
        cost_warnings.append("provider_model_snapshot_missing")

    # v3.9.3 execution surface / mode routing warnings.
    if args.surface == "auto" and not args.owner_ok:
        cost_warnings.append("surface_auto_without_owner_acceptance")
    if args.cursor_mode == "multitask" and not args.owner_ok:
        cost_warnings.append("multitask_without_owner_approval")
    if args.cursor_mode == "multitask" and not args.independent_subscopes:
        cost_warnings.append("multitask_without_independent_subscopes")
    if args.cursor_mode == "plan" and args.intent in {"project_map_update", "answer", "prompt_optimize"} and not premium_reasons:
        cost_warnings.append("plan_mode_over_escalated_for_narrow_task")
    if args.cursor_mode == "debug" and args.intent in {"project_map_update", "answer", "prompt_optimize"}:
        cost_warnings.append("debug_mode_wrong_for_narrow_task")
    if args.surface == "chatgpt_pro_web" and args.intent == "apply":
        blocking.append("chatgpt_web_has_no_repo_mutation_authority")
    if args.surface == "codex_ide" and args.pursue_goal and not args.owner_ok:
        cost_warnings.append("codex_pursue_goal_without_owner_acceptance")
    if args.model_routing_requested and not surface_matrix:
        cost_warnings.append("execution_surface_snapshot_missing")

    if blocking:
        gate = "blocked" if "secret_ref_detected" in blocking else "red"
        action = "block" if gate == "blocked" else "ask_user"
        score = 25
    elif missing and args.intent in {"apply", "repair", "recover"}:
        gate = "red"
        action = "run_readonly_discovery"
        score = 45
    elif missing:
        gate = "amber"
        action = "proceed_with_warning"
        score = 68
    elif cost_warnings:
        gate = "amber"
        action = "ask_user"
        score = 75
    else:
        gate = "green"
        action = "proceed"
        score = 90

    report = {
        "gate": gate,
        "score0to100": score,
        "profile": profile["profile"],
        "intent": args.intent,
        "missingMandatory": missing,
        "unsafeRefs": unsafe,
        "blocking": blocking,
        "route": {
            "surface": profile.get("defaultSurface"),
            "fallbackSurface": profile.get("fallbackSurface"),
            "modelOrModelClass": profile.get("defaultModelOrModelClass"),
            "reasoning": profile.get("defaultReasoning"),
            "speed": profile.get("defaultSpeed"),
            "maxMode": profile.get("maxModeDefault"),
            "includeIdeContext": profile.get("includeIdeContextDefault"),
            "planMode": profile.get("planModeDefault"),
            "costClass": profile.get("defaultCostClass"),
            "capabilityNeed": profile.get("defaultCapabilityNeed"),
            "cheaperAlternative": profile.get("cheaperAlternative"),
            "premiumEscalationReasons": sorted(premium_reasons),
            "requestedModel": requested_model,
            "providerModelSnapshotRef": snapshot_ref,
            "executionSurfaceSnapshotRef": surface_matrix.get("matrixId") if surface_matrix else None,
            "surfaceRequested": args.surface,
            "cursorModeRequested": args.cursor_mode,
            "providerSnapshotConfirmedCurrent": bool(args.provider_snapshot_current),
        },
        "costWarnings": sorted(cost_warnings),
        "recommendedAction": action,
        "compactHint": "ContextAdvisor: gate={gate}; missing={missing}; surface={surface}; model={model}; reasoning={reasoning}; cost={cost}; settings=Max {max_mode}, IDE {ide}, Plan {plan}, speed {speed}; action={action}.".format(
            gate=gate,
            missing=",".join(missing) if missing else "none",
            surface=profile.get("defaultSurface"),
            model=profile.get("defaultModelOrModelClass"),
            reasoning=profile.get("defaultReasoning"),
            cost=profile.get("defaultCostClass"),
            max_mode=profile.get("maxModeDefault"),
            ide=profile.get("includeIdeContextDefault"),
            plan=profile.get("planModeDefault"),
            speed=profile.get("defaultSpeed"),
            action=action,
        ),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Agent Memory Kit Context Advisor preflight.")
    parser.add_argument("--intent", required=True, choices=["answer", "analyze", "plan", "apply", "audit", "repair", "recover", "resume", "debug", "research", "prompt_optimize", "project_map_update", "handoff_package_update"])
    parser.add_argument("--mutation", default="none", choices=["none", "docs", "code", "memory", "db", "deploy", "git", "external"])
    parser.add_argument("--risk", default="medium", choices=["low", "medium", "high", "critical"])
    parser.add_argument("--have", help="Comma-separated context classes already available, e.g. project_map_core,source_authority")
    parser.add_argument("--scope", action="append", default=[], help="Scoped ref/path. May be repeated.")
    parser.add_argument("--owner-ok", action="store_true", help="Owner explicitly approved the mutation/scope.")
    parser.add_argument("--verification", help="Verification command or manual check description.")
    parser.add_argument("--implicit-ide-context", action="store_true", help="Implicit open tabs/selections/diagnostics/workspace context would be used as task context.")
    parser.add_argument("--implicit-ide-approved", action="store_true", help="Owner explicitly approved using implicit IDE context as scope.")
    parser.add_argument("--premium-model", action="store_true", help="The proposed route uses a premium/frontier/high/pro model/settings class.")
    parser.add_argument("--requested-model", choices=["auto", "composer_2_5", "gpt_5_5", "codex_5_3", "sonnet_4_6", "opus_4_8", "fable_5", "other"], help="Specific Cursor model proposed for the route.")
    parser.add_argument("--model-routing-requested", action="store_true", help="User asked which model/settings to use. Requires dated provider snapshot evidence.")
    parser.add_argument("--provider-snapshot-current", action="store_true", help="Current provider/model snapshot was checked in this run.")
    parser.add_argument("--context-1m", action="store_true", help="The proposed route uses a 1M context window / Max context tier.")
    parser.add_argument("--high-reasoning", action="store_true", help="The proposed route uses high or stronger reasoning.")
    parser.add_argument("--premium-justification", help="Comma-separated concrete escalation reasons for premium/high/pro routing.")
    parser.add_argument("--model-name", help="Proposed concrete model name, e.g. Composer 2.5 or GPT-5.5.")
    parser.add_argument("--fast-mode", action="store_true", help="The proposed route enables Fast mode.")
    parser.add_argument("--large-context", action="store_true", help="The proposed route enables Max/1M/large context.")
    parser.add_argument("--optional-model", action="store_true", help="The proposed route uses a non-core optional model such as Gemini/Grok.")
    parser.add_argument("--optional-model-gap", help="Concrete capability gap that justifies an optional model.")
    parser.add_argument("--settings-requested", action="store_true", help="The owner asked for exact model/settings advice.")
    parser.add_argument("--provider-snapshot-date", help="Dated provider/model capability snapshot used for exact model advice.")
    parser.add_argument("--surface", choices=["cursor_agent", "codex_ide", "chatgpt_pro_web", "auto", "other"], default="cursor_agent", help="Execution surface proposed for the task.")
    parser.add_argument("--cursor-mode", choices=["ask", "plan", "agent", "debug", "multitask", "none"], default="none", help="Cursor task mode proposed for the route.")
    parser.add_argument("--independent-subscopes", action="store_true", help="Multitask has explicit independent subscopes and verification per subagent.")
    parser.add_argument("--pursue-goal", action="store_true", help="Codex pursue-goal/goal-mode style autonomy is enabled.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    report = make_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(report["compactHint"])
        if report["gate"] in {"amber", "red", "blocked"}:
            if "implicit_ide_context_unscoped" in report["blocking"]:
                print("Implicit IDE context is advisory only; request owner approval before using it to expand read/apply scope.")
            if report["missingMandatory"]:
                print("Missing mandatory context classes: " + ", ".join(report["missingMandatory"]))
            if report["blocking"]:
                print("Blocking conditions: " + ", ".join(report["blocking"]))
            if report.get("costWarnings"):
                print("Cost/model warnings: " + ", ".join(report["costWarnings"]))
                print("Premium/high/pro/1M routing requires an escalation trigger, dated provider snapshot, and a cheaper alternative.")
                if any("unsupported_model_control" in warning for warning in report.get("costWarnings", [])):
                    print("Do not invent unsupported model controls for the selected model.")
                if "auto_mode_without_owner_acceptance" in report.get("costWarnings", []) or "surface_auto_without_owner_acceptance" in report.get("costWarnings", []):
                    print("Auto is not a reproducible default route for controlled work; use only with owner acceptance.")
                if "multitask_without_owner_approval" in report.get("costWarnings", []) or "multitask_without_independent_subscopes" in report.get("costWarnings", []):
                    print("Multitask is high-fuel/high-coordination; require owner approval and independent subscopes.")
                if "chatgpt_web_has_no_repo_mutation_authority" in report.get("blocking", []):
                    print("ChatGPT Pro web is advisor/research/synthesis only; use Cursor/Codex for repo apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
