#!/usr/bin/env python3
"""Representative behavioral evals for the task prompt compiler."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


sys.dont_write_bytecode = True
TOOL_PATH = Path(__file__).resolve().parents[1] / "scripts" / "task_prompt_tool.py"


def load_tool() -> Any:
    spec = importlib.util.spec_from_file_location("task_prompt_tool_eval", TOOL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TOOL_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


tool = load_tool()


OWNER_OUTCOME = (
    "При любом порядке установки EA и PremiaOP «Приоритет по премии» строит "
    "полный результат при наличии точных локальных данных либо логично сообщает "
    "об их отсутствии без ложной отрисовки."
)


def inherited_spec() -> dict[str, Any]:
    return {
        "schema": "TASK_PROMPT_SPEC_V1",
        "mode": "inherited",
        "task_id": "TASK1_STARTUP_PRIORITY_CLEAN",
        "tree": r"E:\Dev Projects\OPTION_PROFIT",
        "baseline_head": "f9dc66c83e4160170825fa9c01459964f8fdb4b2",
        "continuation": True,
        "owner_outcome": OWNER_OUTCOME,
        "task_state": [
            ".codex/tasks/task1-startup-priority-clean/RECOVERY_CAPSULE.md",
            ".codex/tasks/task1-startup-priority-clean/SCENARIO_MATRIX.md",
            ".codex/tasks/task1-startup-priority-clean/IMPLEMENTATION_RECEIPTS.jsonl",
        ],
        "current_evidence": ["Последний owner smoke переоткрыл startup route."],
        "active_slice": "Post-registration formula route.",
        "authorization": {
            "allowed": ["Production/test edits and local verification."],
            "forbidden": ["MT5 smoke.", "Commit or push."],
        },
    }


def run_cli_with_stdin(stdin_bytes: bytes) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(TOOL_PATH), "roundtrip", "--spec-file", "-"],
        input=stdin_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
        check=False,
    )


def eval_inherited_is_minimal() -> dict[str, Any]:
    spec = inherited_spec()
    prompt = tool.render_prompt(spec)
    result = tool.validate_prompt(spec, prompt)
    assert result["ok"]
    assert "EXECUTION_CONTRACT" not in prompt
    assert "bounded impact sweep" not in prompt.casefold()
    assert "LOCAL_VERIFIED_AWAITING_OWNER_SMOKE" not in prompt
    assert len(prompt) < 2_500
    return {"chars": len(prompt), "mode": "inherited"}


def eval_continuation_changes_only_dynamic_state() -> dict[str, Any]:
    before = inherited_spec()
    after = inherited_spec()
    after["current_evidence"] = ["Новый trace уточнил failing route."]
    after["active_slice"] = "New failing route only as work priority."
    first = tool.render_prompt(before)
    second = tool.render_prompt(after)
    assert OWNER_OUTCOME in first and OWNER_OUTCOME in second
    assert before["task_state"] == after["task_state"]
    assert before["authorization"] == after["authorization"]
    assert tool.validate_prompt(after, second)["ok"]
    assert first != second
    return {"owner_outcome_preserved": True, "state_paths": len(after["task_state"])}


def eval_manual_workflow_append_is_rejected() -> dict[str, Any]:
    spec = inherited_spec()
    prompt = tool.render_prompt(spec)
    altered = prompt + "\nPerform a bounded impact sweep and repeat the full workflow.\n"
    result = tool.validate_prompt(spec, altered)
    assert not result["ok"]
    assert any(issue.startswith("prompt_not_canonical") for issue in result["issues"])
    return {"rejected": True, "issues": result["issues"]}


def eval_compaction_cannot_replace_owner_outcome() -> dict[str, Any]:
    spec = inherited_spec()
    prompt = tool.render_prompt(spec)
    altered = prompt.replace(OWNER_OUTCOME, "Исправь только текущую строку trace.")
    result = tool.validate_prompt(spec, altered)
    assert not result["ok"]
    assert OWNER_OUTCOME in tool.render_prompt(spec)
    return {"rejected": True, "owner_outcome_preserved": True}


def eval_arbitrary_process_field_is_rejected() -> dict[str, Any]:
    spec = inherited_spec()
    spec["workflow_steps"] = ["Repeat the skill workflow in the prompt."]
    try:
        tool.render_prompt(spec)
    except tool.PromptSpecError as error:
        assert "unknown top-level fields: workflow_steps" in str(error)
        return {"rejected": True, "reason": str(error)}
    raise AssertionError("arbitrary workflow field was accepted")


def eval_permissions_and_standalone_mode() -> dict[str, Any]:
    inherited = inherited_spec()
    inherited_prompt = tool.render_prompt(inherited)
    for item in inherited["authorization"]["allowed"] + inherited["authorization"]["forbidden"]:
        assert f"- {item}" in inherited_prompt

    standalone = inherited_spec()
    standalone["mode"] = "standalone"
    standalone_prompt = tool.render_prompt(standalone)
    assert standalone_prompt.count("\nEXECUTION_CONTRACT\n") == 1
    assert tool.validate_prompt(standalone, standalone_prompt)["ok"]
    assert "EXECUTION_CONTRACT" not in inherited_prompt
    return {"permissions_preserved": True, "standalone_contract_count": 1}


def eval_cli_roundtrip_preserves_unicode() -> dict[str, Any]:
    spec = inherited_spec()
    expected = tool.render_prompt(spec)
    completed = run_cli_with_stdin(
        json.dumps(spec, ensure_ascii=False).encode("utf-8", errors="strict")
    )
    stderr = completed.stderr.decode("utf-8", errors="strict")
    stdout = completed.stdout.decode("utf-8", errors="strict")
    assert completed.returncode == 0, stderr
    assert completed.stdout == expected.encode("utf-8", errors="strict")
    assert OWNER_OUTCOME in stdout
    assert "\ufffd" not in stdout
    assert tool.validate_prompt(spec, stdout)["ok"]
    return {
        "unicode_preserved": True,
        "byte_exact": True,
        "chars": len(stdout),
        "sha256": tool.sha256_text(stdout),
    }


def eval_replacement_character_is_fatal() -> dict[str, Any]:
    corrupted_spec = inherited_spec()
    corrupted_spec["owner_outcome"] += " \ufffd"
    try:
        tool.render_prompt(corrupted_spec)
    except tool.PromptSpecError as error:
        assert "U+FFFD" in str(error)
    else:
        raise AssertionError("U+FFFD in owner outcome was accepted")

    completed = run_cli_with_stdin(
        json.dumps(corrupted_spec, ensure_ascii=False).encode("utf-8", errors="strict")
    )
    stderr = completed.stderr.decode("utf-8", errors="strict")
    assert completed.returncode == 3
    assert completed.stdout == b""
    assert "U+FFFD replacement character" in stderr
    assert b"\xef\xbf\xbd" not in completed.stderr

    spec = inherited_spec()
    prompt = tool.render_prompt(spec)
    corrupted_prompt = prompt.replace("При любом", "\ufffdри любом", 1)
    result = tool.validate_prompt(spec, corrupted_prompt)
    assert not result["ok"]
    assert "prompt_contains_u_fffd_replacement_character" in result["issues"]
    return {"spec_rejected": True, "cli_rejected": True, "prompt_rejected": True}


def eval_invalid_utf8_stdin_fails_closed() -> dict[str, Any]:
    completed = run_cli_with_stdin(b'{"schema":"TASK_PROMPT_SPEC_V1","owner_outcome":"\xff"}')
    stderr = completed.stderr.decode("utf-8", errors="strict")
    assert completed.returncode == 3
    assert completed.stdout == b""
    assert "not valid UTF-8: stdin" in stderr
    assert "\ufffd" not in stderr
    return {"failed_closed": True, "error_stream_utf8": True}


def main() -> int:
    evals: list[tuple[str, Callable[[], dict[str, Any]]]] = [
        ("inherited_prompt_is_minimal", eval_inherited_is_minimal),
        ("continuation_changes_only_dynamic_state", eval_continuation_changes_only_dynamic_state),
        ("manual_workflow_append_is_rejected", eval_manual_workflow_append_is_rejected),
        ("compaction_cannot_replace_owner_outcome", eval_compaction_cannot_replace_owner_outcome),
        ("arbitrary_process_field_is_rejected", eval_arbitrary_process_field_is_rejected),
        ("permissions_and_standalone_mode", eval_permissions_and_standalone_mode),
        ("cli_roundtrip_preserves_unicode", eval_cli_roundtrip_preserves_unicode),
        ("replacement_character_is_fatal", eval_replacement_character_is_fatal),
        ("invalid_utf8_stdin_fails_closed", eval_invalid_utf8_stdin_fails_closed),
    ]
    results: list[dict[str, Any]] = []
    for name, function in evals:
        try:
            results.append({"name": name, "result": "PASS", **function()})
        except Exception as error:  # noqa: BLE001 - report every representative eval
            results.append({"name": name, "result": "FAIL", "error": repr(error)})
    passed = sum(result["result"] == "PASS" for result in results)
    payload = {
        "schema": "TASK_PROMPT_COMPILER_EVALS_V1",
        "passed": passed,
        "total": len(results),
        "results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
