#!/usr/bin/env python3
"""Validate the Agents catalog, source coverage, targets, and travel references."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from agent_catalog import validate_catalog
except ModuleNotFoundError:  # Imported as a module from repository tests.
    from scripts.agent_catalog import validate_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, warnings = validate_catalog(args.repo)
    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"FAIL  {error}", file=sys.stderr)
    if errors:
        print(f"\n{len(errors)} catalog error(s).", file=sys.stderr)
        return 1
    print(f"OK — catalog valid ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
