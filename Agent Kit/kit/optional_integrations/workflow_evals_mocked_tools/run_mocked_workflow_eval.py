"""Validate a pre-recorded mock trace; never executes a tool."""
import argparse, json, re
from pathlib import Path

def nested(data, path):
    for key in path.split("."):
        if not isinstance(data, dict) or key not in data: return None
        data = data[key]
    return data

def run(case, trace):
    calls = trace.get("tool_calls", [])
    seen = [c.get("tool") for c in calls]
    reasons = []
    for tool in case.get("expected_tools", []):
        if tool not in seen: reasons.append({"code":"WF_EXPECTED_TOOL_MISSING","tool":tool})
    for tool in case.get("forbidden_tools", []):
        if tool in seen: reasons.append({"code":"WF_FORBIDDEN_TOOL_CALLED","tool":tool})
    for rule in case.get("argument_constraints", []):
        matching = [c for c in calls if c.get("tool") == rule["tool"]]
        if not matching: continue
        actual = nested(matching[0].get("arguments", {}), rule["path"])
        op, expected = rule["operator"], rule["value"]
        ok = actual == expected if op == "equals" else actual != expected if op == "not_equals" else str(expected) in str(actual) if op == "contains" else re.search(str(expected), str(actual)) is not None
        if not ok: reasons.append({"code":"WF_ARGUMENT_CONSTRAINT_FAILED","tool":rule["tool"],"path":rule["path"]})
    if trace.get("terminal_outcome") != case.get("expected_terminal_outcome"):
        reasons.append({"code":"WF_TERMINAL_OUTCOME_MISMATCH"})
    return {"status":"pass" if not reasons else "fail","reasons":reasons,"executed_tools":False,"advisory_graders_blocking":False}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--case",type=Path,required=True); p.add_argument("--trace",type=Path,required=True); a=p.parse_args()
    result=run(json.loads(a.case.read_text(encoding="utf-8")),json.loads(a.trace.read_text(encoding="utf-8")))
    print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result["status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
