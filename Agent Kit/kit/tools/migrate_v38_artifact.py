"""Read a v3.8 JSON/YAML artifact and print a conservative v4 proposal."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

TYPES={"task":"TaskContractV2","claim":"ClaimLedgerV2","handoff":"HandoffV2","working":"WorkingStateV2"}
ID_PATTERN=r"\b(?:TASK|CLM|COM|HO|CKPT|VR|SE|MD|FACT|DEC|RISK)-[A-Za-z0-9._-]+\b"
LIFECYCLE_VALUES={"active","blocked","completed","cancelled","archived","current","stale","superseded","rejected","verified","missing_evidence","conflict","open","settled_success","settled_failure","pending","approved","applied"}

def yaml_top_level(text):
    out={}
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if not line or line[0].isspace() or line.lstrip().startswith("#") or ":" not in line: continue
        key,value=line.split(":",1); value=value.strip().split(" #",1)[0].strip()
        if value in ("", "[]"):
            items=[]
            for later in lines[i+1:]:
                if later and not later[0].isspace(): break
                m=re.match(r"\s+-\s+[\"']?(.*?)[\"']?\s*$",later)
                if m: items.append(m.group(1))
            out[key]=items if items or value=="[]" else None
        elif value in ("null","~"): out[key]=None
        elif value.lower() in ("true","false"): out[key]=value.lower()=="true"
        else: out[key]=value.strip("\"'")
    return out

def identify(path, data, requested):
    if requested!="auto": return requested
    name=path.name.lower(); keys=set(data)
    if "task_id" in keys or "task" in name: return "task"
    if "claims" in keys or "claim" in name: return "claim"
    if "handoff_id" in keys or "handoff" in name: return "handoff"
    if "working" in name or "current_priority" in keys: return "working"
    raise ValueError("MIGRATION_ARTIFACT_TYPE_UNKNOWN")

def first(data,key,default="unknown"):
    value=data.get(key,default); return default if value in (None,"") else value

def propose(kind,data):
    governance={"contract_version":"2.0","supersedes":TYPES[kind].replace("V2","V1"),"effective_from":"pending","compatibility":"breaking","migration_note":"Generated proposal; owner review required."}
    if kind=="task":
        out={"schema_version":"2.0","governance":governance,"task_id":first(data,"task_id"),"status":first(data,"status","active"),"intent":first(data,"intent","unknown"),"permission_mode":first(data,"permission_mode","read-only"),"goal":first(data,"goal"),"scope":data.get("scope",{"project_map":[],"project_files":[],"external_sources":[]}),"commitment_refs":[],"expected_outcomes":["pending owner review"],"stop_conditions":["Stop when required evidence is missing."],"rollback_or_recovery":["pending owner review"],"reversibility":"unknown","expected_side_effects":[],"done_definition":data.get("done_definition",["pending owner review"])}
    elif kind=="claim":
        out={"schema_version":"2.0","governance":governance,"project_id":first(data,"project_id"),"claims":data.get("claims",[]),"final_answer_gate":data.get("final_answer_gate",{"if_gate_fails":"revise_or_report_missing_evidence"})}
        for claim in out["claims"]:
            if isinstance(claim,dict): claim.setdefault("verification_receipt_refs",[])
    elif kind=="handoff":
        out={"schema_version":"2.0","governance":governance,"handoff_id":first(data,"handoff_id"),"active_task":first(data,"active_task"),"checkpoint_id":first(data,"checkpoint_id"),"current_best_state":first(data,"current_best_state"),"next_safe_step":first(data,"next_safe_step"),"commitment_refs":[],"verification_receipt_refs":[],"unsafe_to_repeat":data.get("unsafe_to_repeat",[]),"replay_instructions":data.get("replay_instructions",{"retrieval_profile":"resume","check_side_effect_receipts_first":True,"check_open_commitments_first":True})}
        out["replay_instructions"].setdefault("check_open_commitments_first",True)
    else:
        out={"schema_version":"2.0","governance":governance,"active_task":data.get("active_task"),"checkpoint":data.get("checkpoint"),"cursor":first(data,"cursor",first(data,"current_priority")),"commitment_refs":[],"verification_receipt_refs":[],"side_effect_receipt_refs":[],"next_safe_step":first(data,"next_safe_step",str(data.get("next_recommended_action","unknown")))}
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("artifact",type=Path); p.add_argument("--type",choices=("auto",*TYPES),default="auto"); a=p.parse_args()
    raw=a.artifact.read_bytes(); text=raw.decode("utf-8-sig"); data=json.loads(text) if a.artifact.suffix.lower()==".json" else yaml_top_level(text)
    kind=identify(a.artifact,data,a.type); proposal=propose(kind,data)
    mapped=set(proposal)|{"schema_version"}; payload={"migration":"v3.8_to_v4.0","source_path":str(a.artifact),"source_sha256":hashlib.sha256(raw).hexdigest(),"detected_type":TYPES[kind],"proposal":proposal,"unmapped_source_fields":sorted(set(data)-mapped),"owner_review":"required","source_modified":False}
    payload["source_preservation"]={"recognized_ids":sorted(set(re.findall(ID_PATTERN,text))),"recognized_lifecycle_values":sorted({value for value in LIFECYCLE_VALUES if re.search(rf"\b{re.escape(value)}\b",text)}),"raw_source_retained_by_helper":False,"note":"Use source_path and source_sha256 as the immutable migration evidence; recognized references are reported even when narrow YAML parsing cannot map their nesting."}
    print(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
