"""Interface for ``python -m scheduled_tests``."""

import os
import sys
import tempfile
from argparse import ArgumentParser
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

import pytest

from . import __version__

__all__ = ["main"]

CHECKS = Path(__file__).parent / "checks"


def run_checks(names: Sequence[str]) -> int:
    """Run the named check modules in order, in a single pytest session."""
    available = sorted(p.stem for p in CHECKS.glob("*.py") if p.stem != "__init__")
    unknown = [name for name in names if name not in available]
    if unknown:
        print(f"Unknown checks {unknown}, available: {available}", file=sys.stderr)
        return 2

    job = os.environ.get("JOB_NAME", "local")
    root = Path(os.environ.get("REPORT_DIR", Path(tempfile.gettempdir()) / "reports"))
    report = root / datetime.now().strftime("%Y-%m-%dT%H%M%S") / job

    paths = [str(CHECKS / f"{name}.py") for name in names]
    return pytest.main(
        [*paths, "-v", "-p", "no:cacheprovider", f"--junitxml={report / 'junit.xml'}"]
    )


def main(args: Sequence[str] | None = None) -> None:
    """Argument parser for the CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    subparsers = parser.add_subparsers(dest="command")
    run = subparsers.add_parser("run", help="run checks in the order given")
    run.add_argument("checks", nargs="+", help="check names, e.g. first second")
    parsed = parser.parse_args(args)

    if parsed.command == "run":
        sys.exit(run_checks(parsed.checks))


if __name__ == "__main__":
    main()
