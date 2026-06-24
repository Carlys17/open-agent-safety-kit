from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

SEVERITY_POINTS = {
    "LOW": 5,
    "MEDIUM": 15,
    "HIGH": 30,
    "CRITICAL": 50,
}

@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    evidence: str
    recommendation: str

    @property
    def points(self) -> int:
        return SEVERITY_POINTS[self.severity]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["points"] = self.points
        return data

@dataclass(frozen=True)
class EvaluationResult:
    task: str
    score: int
    passed: bool
    finding_count: int
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "score": self.score,
            "passed": self.passed,
            "finding_count": self.finding_count,
            "findings": [f.to_dict() for f in self.findings],
        }
