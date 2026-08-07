"""Report-only fail-closed capability manifest checker."""
import argparse, json
from pathlib import Path
FIELDS=("private_data","untrusted_input","external_communication","mutating","approval_sensitive")
def check(doc):
    reasons=[]; aggregate={k:False for k in FIELDS}
    if doc.get("schema_version")!="1.0" or not isinstance(doc.get("tools"),list): reasons.append({"code":"CAP_MANIFEST_INVALID"})
    for i,tool in enumerate(doc.get("tools",[])):
        if not isinstance(tool,dict) or not isinstance(tool.get("name"),str): reasons.append({"code":"CAP_TOOL_INVALID","index":i}); continue
        missing=[k for k in FIELDS if not isinstance(tool.get(k),bool)]
        if missing: reasons.append({"code":"CAP_METADATA_MISSING_HIGH_RISK","tool":tool.get("name"),"fields":missing})
        for k in FIELDS: aggregate[k] = aggregate[k] or (tool.get(k) is True) or (k in missing)
    if aggregate["private_data"] and aggregate["untrusted_input"] and aggregate["external_communication"]: reasons.append({"code":"CAP_LETHAL_TRIFECTA_BLOCKED"})
    return {"status":"pass" if not reasons else "fail","reasons":reasons,"report_only":True}
def main():
    p=argparse.ArgumentParser(); p.add_argument("manifest",type=Path); a=p.parse_args(); out=check(json.loads(a.manifest.read_text(encoding="utf-8"))); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
