"""Stable finding and report primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, order=True)
class Finding:
    rule_id: str
    path: str
    message: str
    severity: str = "error"

    def identity(self) -> tuple[str, str, str]:
        return self.rule_id, self.path, self.message

    def as_dict(self) -> dict[str, str]:
        return {
            "id": self.rule_id,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
        }


def finding_from_mapping(value: Mapping[str, object]) -> Finding:
    return Finding(
        str(value["id"]),
        str(value.get("path", "")),
        str(value.get("message", "")),
        str(value.get("severity", "error")),
    )
