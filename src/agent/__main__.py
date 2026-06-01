"""Package CLI entry point for running Resilience Copilot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agent.resilience_agent import ResilienceAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the safety-bounded Resilience Copilot agent on a case note."
    )
    parser.add_argument(
        "--scenario",
        required=True,
        help="Raw disaster-relief case note text to process.",
    )
    parser.add_argument(
        "--no-memory",
        action="store_true",
        help="Disable bounded memory retrieval for this run.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = ResilienceAgent().run(args.scenario, use_memory=not args.no_memory)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
