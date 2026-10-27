#!/usr/bin/env python3
"""Render and validate minimal agent prompts from a bounded JSON spec."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


SCHEMA = "TASK_PROMPT_SPEC_V1"
RESULT_SCHEMA = "TASK_PROMPT_VALIDATION_V1"
MODES = {"inherited", "standalone"}
TOP_LEVEL_FIELDS = {
    "schema",
    "mode",
    "task_id",
    "tree",
    "baseline_head",
    "continuation",
    "owner_outcome",
    "task_state",
    "current_evidence",
    "active_slice",
    "authorization",
}
AUTHORIZATION_FIELDS = {"allowed", "forbidden"}
MAX_ITEMS = 12
MAX_ITEM_CHARS = 1_200
MAX_OUTCOME_CHARS = 6_000
MAX_ACTIVE_SLICE_CHARS = 1_600
MAX_PROMPT_CHARS = {"inherited": 8_000, "standalone": 12_000}
UNICODE_REPLACEMENT_CHARACTER = "\ufffd"


class PromptSpecError(ValueError):
    """Raised when a task prompt spec is incomplete or expands the contract."""


def configure_standard_streams() -> None:
    """Keep task prompts lossless across Windows console and pipe code pages."""

    for stream_name, stream in (("stdin", sys.stdin), ("stdout", sys.stdout), ("stderr", sys.stderr)):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="strict", newline="\n")
            except (LookupError, OSError, ValueError) as error:
                raise PromptSpecError(f"cannot configure {stream_name} as strict UTF-8") from error


def require_lossless_unicode(text: str, field: str) -> None:
    if UNICODE_REPLACEMENT_CHARACTER in text:
        raise PromptSpecError(f"{field} contains U+FFFD replacement character")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in text):
        raise PromptSpecError(f"{field} contains an unpaired Unicode surrogate")


def clean_text(value: Any, field: str, *, maximum: int, required: bool = True) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise PromptSpecError(f"{field} must be a string")
    text = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    require_lossless_unicode(text, field)
    if required and not text:
        raise PromptSpecError(f"{field} must not be empty")
    if "\x00" in text:
        raise PromptSpecError(f"{field} contains NUL")
    if len(text) > maximum:
        raise PromptSpecError(f"{field} exceeds {maximum} characters")
    return text


def clean_list(value: Any, field: str, *, required: bool = False) -> list[str]:
    if value is None:
        value = []
    if not isinstance(value, list):
        raise PromptSpecError(f"{field} must be a JSON array")
    if len(value) > MAX_ITEMS:
        raise PromptSpecError(f"{field} exceeds {MAX_ITEMS} items")
    items = [clean_text(item, f"{field}[{index}]", maximum=MAX_ITEM_CHARS) for index, item in enumerate(value)]
    if required and not items:
        raise PromptSpecError(f"{field} must contain at least one item")
    return items


def normalize_spec(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise PromptSpecError("spec must be a JSON object")
    unknown = sorted(set(raw) - TOP_LEVEL_FIELDS)
    if unknown:
        raise PromptSpecError("unknown top-level fields: " + ", ".join(unknown))
    if raw.get("schema") != SCHEMA:
        raise PromptSpecError(f"schema must be {SCHEMA}")

    mode = clean_text(raw.get("mode"), "mode", maximum=32).casefold()
    if mode not in MODES:
        raise PromptSpecError("mode must be inherited or standalone")
    continuation = raw.get("continuation")
    if not isinstance(continuation, bool):
        raise PromptSpecError("continuation must be true or false")

    authorization = raw.get("authorization")
    if not isinstance(authorization, dict):
        raise PromptSpecError("authorization must be an object")
    unknown_auth = sorted(set(authorization) - AUTHORIZATION_FIELDS)
    if unknown_auth:
        raise PromptSpecError("unknown authorization fields: " + ", ".join(unknown_auth))

    task_state = clean_list(raw.get("task_state"), "task_state")
    if mode == "inherited" and continuation and not task_state:
        raise PromptSpecError("an inherited continuation must identify task_state")

    normalized = {
        "schema": SCHEMA,
        "mode": mode,
        "task_id": clean_text(raw.get("task_id"), "task_id", maximum=200),
        "tree": clean_text(raw.get("tree"), "tree", maximum=1_000),
        "baseline_head": clean_text(
            raw.get("baseline_head"), "baseline_head", maximum=200, required=False
        ),
        "continuation": continuation,
        "owner_outcome": clean_text(
            raw.get("owner_outcome"), "owner_outcome", maximum=MAX_OUTCOME_CHARS
        ),
        "task_state": task_state,
        "current_evidence": clean_list(raw.get("current_evidence"), "current_evidence"),
        "active_slice": clean_text(
            raw.get("active_slice"),
            "active_slice",
            maximum=MAX_ACTIVE_SLICE_CHARS,
            required=False,
        ),
        "authorization": {
            "allowed": clean_list(authorization.get("allowed"), "authorization.allowed", required=True),
            "forbidden": clean_list(authorization.get("forbidden"), "authorization.forbidden"),
        },
    }
    return normalized


def append_section(lines: list[str], title: str, body: str | list[str]) -> None:
    lines.extend(["", title])
    if isinstance(body, list):
        lines.extend(f"- {item}" for item in body)
    else:
        lines.append(body)


def render_prompt(raw_spec: Any) -> str:
    spec = normalize_spec(raw_spec)
    lines = ["TASK_PROMPT_V1", f"MODE: {spec['mode']}"]
    append_section(lines, "TASK_ID", spec["task_id"])
    append_section(lines, "TREE", spec["tree"])
    if spec["baseline_head"]:
        append_section(lines, "BASELINE_HEAD", spec["baseline_head"])
    if spec["continuation"]:
        append_section(
            lines,
            "CONTINUATION",
            "Continue the same task. CURRENT_EVIDENCE and ACTIVE_SLICE update its state; "
            "they do not replace OWNER_OUTCOME.",
        )
    append_section(lines, "OWNER_OUTCOME", spec["owner_outcome"])
    if spec["task_state"]:
        append_section(lines, "TASK_STATE", spec["task_state"])
    if spec["current_evidence"]:
        append_section(lines, "CURRENT_EVIDENCE", spec["current_evidence"])
    if spec["active_slice"]:
        append_section(lines, "ACTIVE_SLICE", spec["active_slice"])

    lines.extend(["", "AUTHORIZATION", "Allowed:"])
    lines.extend(f"- {item}" for item in spec["authorization"]["allowed"])
    lines.append("Forbidden or separately gated:")
    forbidden = spec["authorization"]["forbidden"]
    lines.extend(f"- {item}" for item in forbidden or ["None beyond inherited instructions."])

    if spec["mode"] == "standalone":
        append_section(
            lines,
            "EXECUTION_CONTRACT",
            [
                "Treat OWNER_OUTCOME and its success conditions as the task; evidence and the active slice are not replacement scope.",
                "Inspect the bounded relevant behavior surface, implement all confirmed blockers, and preserve unrelated changes.",
                "Use the strongest available behavioral verification and state exactly what remains unproven.",
                "Do not claim completion or perform separately gated side effects without the required evidence and authorization.",
            ],
        )

    prompt = "\n".join(lines).rstrip() + "\n"
    limit = MAX_PROMPT_CHARS[spec["mode"]]
    if len(prompt) > limit:
        raise PromptSpecError(f"rendered {spec['mode']} prompt exceeds {limit} characters")
    return prompt


def normalized_prompt(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_prompt(raw_spec: Any, actual_prompt: str) -> dict[str, Any]:
    spec = normalize_spec(raw_spec)
    canonical = render_prompt(spec)
    actual = normalized_prompt(actual_prompt)
    issues: list[str] = []
    if UNICODE_REPLACEMENT_CHARACTER in actual:
        issues.append("prompt_contains_u_fffd_replacement_character")
    if actual != canonical:
        mismatch = next(
            (index for index, pair in enumerate(zip(actual, canonical)) if pair[0] != pair[1]),
            min(len(actual), len(canonical)),
        )
        issues.append(f"prompt_not_canonical:first_mismatch={mismatch}")
    if len(actual) > MAX_PROMPT_CHARS[spec["mode"]]:
        issues.append("prompt_size_budget_exceeded")
    if spec["mode"] == "inherited" and "\nEXECUTION_CONTRACT\n" in actual:
        issues.append("inherited_prompt_contains_standalone_workflow")
    return {
        "schema": RESULT_SCHEMA,
        "ok": not issues,
        "mode": spec["mode"],
        "issues": issues,
        "actual_chars": len(actual),
        "canonical_chars": len(canonical),
        "actual_sha256": sha256_text(actual),
        "canonical_sha256": sha256_text(canonical),
    }


def read_text(path: str, label: str) -> str:
    try:
        if path == "-":
            return sys.stdin.read()
        candidate = Path(path).expanduser().resolve()
        if not candidate.is_file():
            raise PromptSpecError(f"{label} file does not exist: {candidate}")
        return candidate.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError as error:
        source = "stdin" if path == "-" else str(Path(path).expanduser().resolve())
        raise PromptSpecError(f"{label} is not valid UTF-8: {source}") from error


def read_spec(path: str) -> dict[str, Any]:
    try:
        raw = json.loads(read_text(path, "spec"))
    except json.JSONDecodeError as error:
        raise PromptSpecError(f"spec is not valid JSON: {error}") from error
    return normalize_spec(raw)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("render", "roundtrip"):
        command = subparsers.add_parser(name)
        command.add_argument("--spec-file", default="-")
    validate = subparsers.add_parser("validate")
    validate.add_argument("--spec-file", required=True)
    validate.add_argument("--prompt-file", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_standard_streams()
    args = build_parser().parse_args(argv)
    try:
        if args.command in {"render", "roundtrip"}:
            spec = read_spec(args.spec_file)
            prompt = render_prompt(spec)
            if args.command == "roundtrip":
                result = validate_prompt(spec, prompt)
                if not result["ok"]:
                    raise PromptSpecError("canonical roundtrip failed: " + ", ".join(result["issues"]))
            sys.stdout.write(prompt)
            return 0

        if args.spec_file == "-" and args.prompt_file == "-":
            raise PromptSpecError("spec and prompt cannot both read from stdin")
        spec = read_spec(args.spec_file)
        prompt = read_text(args.prompt_file, "prompt")
        result = validate_prompt(spec, prompt)
        sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        return 0 if result["ok"] else 2
    except (OSError, PromptSpecError) as error:
        sys.stderr.write(
            json.dumps(
                {"schema": "TASK_PROMPT_TOOL_ERROR_V1", "ok": False, "error": str(error)},
                ensure_ascii=False,
            )
            + "\n"
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
