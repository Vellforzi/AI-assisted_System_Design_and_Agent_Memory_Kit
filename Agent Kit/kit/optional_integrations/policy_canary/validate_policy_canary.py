"""Validate an offline policy-canary proposal without activating it."""
import argparse, json
from pathlib import Path
def validate(d):
    reasons=[]
    required=("baseline_identity","candidate_identity","baseline_cohort","candidate_cohort","guardrails","stop_thresholds","rollback_rule","owner_approval","live_traffic","auto_activate")
    if d.get("schema_version")!="1.0" or any(k not in d for k in required): reasons.append({"code":"CANARY_REQUIRED_FIELD_MISSING"})
    if d.get("baseline_identity")==d.get("candidate_identity"): reasons.append({"code":"CANARY_IDENTITIES_NOT_DISTINCT"})
    if d.get("baseline_cohort")!=d.get("candidate_cohort"): reasons.append({"code":"CANARY_COHORT_MISMATCH"})
    if not d.get("guardrails"): reasons.append({"code":"CANARY_GUARDRAILS_MISSING"})
    if not d.get("stop_thresholds"): reasons.append({"code":"CANARY_STOP_THRESHOLDS_MISSING"})
    if not d.get("rollback_rule"): reasons.append({"code":"CANARY_ROLLBACK_RULE_MISSING"})
    if d.get("live_traffic") is not False or d.get("auto_activate") is not False: reasons.append({"code":"CANARY_RUNTIME_ACTIVATION_FORBIDDEN"})
    return {"status":"pass" if not reasons else "fail","reasons":reasons,"rollout_authorized":d.get("owner_approval")=="approved" and not reasons,"validator_activated_rollout":False}
def main():
    p=argparse.ArgumentParser(); p.add_argument("policy",type=Path); a=p.parse_args(); out=validate(json.loads(a.policy.read_text(encoding="utf-8"))); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
