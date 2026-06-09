# /settings-audit

Use this command to audit Cursor settings against Agent Memory Kit owner-controlled defaults.

## Intent

Analyze only. Do not change IDE settings, files, Project Map, hooks, or code unless the owner separately asks for apply.

## Agent procedure

1. Ask the owner for screenshots or exported settings if settings are not visible.
2. Compare against `cursor/settings/owner_controlled_profile.yaml`.
3. Classify each setting as:
   - safe default;
   - acceptable owner preference;
   - risky for owner-controlled work;
   - missing evidence.
4. Prioritize warnings for:
   - Run Mode = Run Everything;
   - Auto-Approve Mode Transitions enabled;
   - Auto-Accept Web Search enabled;
   - MCP protection disabled;
   - Browser protection disabled;
   - File deletion protection disabled;
   - External file protection disabled;
   - broad command/MCP/fetch allowlists;
   - Usage Summary hidden;
   - Auto Format on Agent Finish enabled.
5. Give concrete recommended settings.
6. Do not imply that UI settings replace task contracts, source authority, hooks, or owner approval.

## Output

```text
Cursor settings audit
Mode: analyze-only
Critical risks: <list>
Recommended changes: <list>
Acceptable current settings: <list>
Missing evidence: <list>
Project Map delta: no, unless owner asks
Eval trigger: yes/no
```
