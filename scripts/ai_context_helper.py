"""Repository entry point for the bundled read-only context helper."""

from pathlib import Path
import runpy


REFERENCE_HELPER = (
    Path(__file__).resolve().parents[1]
    / "Agent Kit"
    / "kit"
    / "tools"
    / "context_governance_helper.py"
)


if __name__ == "__main__":
    if not REFERENCE_HELPER.is_file():
        raise SystemExit(f"Bundled context helper not found: {REFERENCE_HELPER}")
    runpy.run_path(str(REFERENCE_HELPER), run_name="__main__")
