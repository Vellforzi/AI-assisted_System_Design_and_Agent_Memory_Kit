"""Portable, dependency-free documentation lifecycle governance engine."""

from .checks import build_report
from .delta import build_delta_report

__all__ = ["build_report", "build_delta_report"]
