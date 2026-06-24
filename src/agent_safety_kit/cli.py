from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .evaluator import evaluate_file, load_trace, evaluate_trace
from .rules import RULES
from .report import to_json, to_markdown
from .models import EvaluationResult


def _render(result, fmt: str) -> str:
    return to_markdown(result) if fmt == "markdown" else to_json(result)


def _verbose_header(task: str) -> None:
    rule_count = len(RULES)
    print(f"Analyzing trace: {task}")
    print(f"Applying {rule_count} rule sets...")
    print("─" * 50)


def _verbose_result(result) -> None:
    if result.passed:
        print(f"\n✓ PASS — Risk score: {result.score}/100")
        print("  All checks passed. No findings.")
    else:
        print(f"\n✗ FAIL — Risk score: {result.score}/100")
        print(f"  {result.finding_count} finding(s):")
        for i, f in enumerate(result.findings, 1):
            print(f"    {i}. [{f.severity}] {f.rule_id}")
            print(f"       {f.message}")
    print(f"\n✓ Check complete")


def run_command(args: argparse.Namespace) -> int:
    if args.verbose:
        trace = load_trace(args.trace)
        _verbose_header(trace.get("task", args.trace))
        result = evaluate_trace(trace)
        _verbose_result(result)
        return 0 if result.passed else 1

    result = evaluate_file(args.trace)
    print(_render(result, args.format))
    if args.max_score is not None and result.score > args.max_score:
        return 2
    return 0 if result.passed else 1


def verify_command(args: argparse.Namespace) -> int:
    """Agent-friendly verification. Reads trace from file or stdin.
    Outputs JSON to stdout. Exit code: 0=safe, 1=unsafe, 2=error."""
    try:
        if args.trace == "-" or args.trace is None:
            raw = sys.stdin.read()
            trace = json.loads(raw)
            result = evaluate_trace(trace)
        else:
            result = evaluate_file(args.trace)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stdout)
        return 2
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {args.trace}"}), file=sys.stdout)
        return 2
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stdout)
        return 2

    output = {
        "safe": result.passed,
        "score": result.score,
        "task": result.task,
        "finding_count": result.finding_count,
        "findings": [f.to_dict() for f in result.findings],
    }

    if args.threshold is not None:
        output["threshold"] = args.threshold
        output["below_threshold"] = result.score <= args.threshold

    print(json.dumps(output))

    if args.threshold is not None:
        return 0 if result.score <= args.threshold else 1
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
        if args.verbose:
            _verbose_header(result.task)
            _verbose_result(result)
        else:
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
    run.add_argument("--verbose", "-v", action="store_true", help="Show human-readable analysis output")
    run.set_defaults(func=run_command)

    verify = sub.add_parser("verify", help="Agent-friendly verification (JSON in, JSON out, exit code)")
    verify.add_argument("trace", nargs="?", default="-", help="Trace file path, or - for stdin (default)")
    verify.add_argument("--threshold", "-t", type=int, default=None, help="Max acceptable risk score (default: 0 = must pass all)")
    verify.set_defaults(func=verify_command)

    batch = sub.add_parser("batch", help="Evaluate all JSON traces in a directory")
    batch.add_argument("directory")
    batch.add_argument("--format", choices=["json", "markdown"], default="json")
    batch.add_argument("--max-score", type=int, default=None)
    batch.add_argument("--verbose", "-v", action="store_true", help="Show human-readable analysis output")
    batch.set_defaults(func=batch_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
