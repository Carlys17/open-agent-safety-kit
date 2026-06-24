from __future__ import annotations

import json
from .models import EvaluationResult


def to_json(result: EvaluationResult) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True)


def to_markdown(result: EvaluationResult) -> str:
    status = "PASS" if result.passed else "FAIL"
    lines = [
        f"# Agent Safety Report: {status}",
        "",
        f"Task: {result.task}",
        f"Risk score: {result.score}/100",
        f"Findings: {result.finding_count}",
        "",
    ]
    if not result.findings:
        lines.append("No findings. The trace includes sufficient evidence for the checked rules.")
        return "\n".join(lines)
    for i, finding in enumerate(result.findings, 1):
        lines.extend([
            f"## {i}. {finding.rule_id} ({finding.severity})",
            "",
            finding.message,
            "",
            f"Evidence: `{finding.evidence}`",
            "",
            f"Recommendation: {finding.recommendation}",
            "",
        ])
    return "\n".join(lines)
