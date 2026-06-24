from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import EvaluationResult, Finding
from .rules import RULES


def load_trace(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Trace must be a JSON object")
    if "events" not in data or not isinstance(data["events"], list):
        raise ValueError("Trace must contain an events list")
    return data


def evaluate_trace(trace: Mapping[str, Any]) -> EvaluationResult:
    events = trace.get("events", [])
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    findings: list[Finding] = []
    for rule in RULES:
        findings.extend(rule(events))
    score = min(100, sum(f.points for f in findings))
    return EvaluationResult(
        task=str(trace.get("task", "untitled")),
        score=score,
        passed=score == 0,
        finding_count=len(findings),
        findings=tuple(findings),
    )


def evaluate_file(path: str | Path) -> EvaluationResult:
    return evaluate_trace(load_trace(path))
