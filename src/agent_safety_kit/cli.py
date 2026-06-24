from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .evaluator import evaluate_file
from .report import to_json, to_markdown


def _render(result, fmt: str) -> str:
    return to_markdown(result) if fmt == "markdown" else to_json(result)


def run_command(args: argparse.Namespace) -> int:
    result = evaluate_file(args.trace)
    print(_render(result, args.format))
    if args.max_score is not None and result.score > args.max_score:
        return 2
    return 0 if result.passed else 1


def batch_command(args: argparse.Namespace) -> int:
    paths = sorted(Path(args.directory).glob("*.json"))
    if not paths:
        print(f"No .json traces found in {args.directory}", file=sys.stderr)
        return 2
    worst = 0
    for path in paths:
        result = evaluate_file(path)
        worst = max(worst, result.score)
        print(f"\n<!-- {path.name} -->")
        print(_render(result, args.format))
    if args.max_score is not None and worst > args.max_score:
        return 2
    return 0 if worst == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oask", description="Open Agent Safety Kit CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Evaluate one JSON trace")
    run.add_argument("trace")
    run.add_argument("--format", choices=["json", "markdown"], default="json")
    run.add_argument("--max-score", type=int, default=None, help="Return exit 2 if score is above this threshold")
    run.set_defaults(func=run_command)

    batch = sub.add_parser("batch", help="Evaluate all JSON traces in a directory")
    batch.add_argument("directory")
    batch.add_argument("--format", choices=["json", "markdown"], default="json")
    batch.add_argument("--max-score", type=int, default=None)
    batch.set_defaults(func=batch_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
