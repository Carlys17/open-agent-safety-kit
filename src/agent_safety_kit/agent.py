"""Agent integration API for Open Agent Safety Kit.

Use this module to verify agent traces programmatically before claiming success.

Example usage in an agent workflow:

    from agent_safety_kit import verify_agent_trace

    # After completing a task, verify the trace
    result = verify_agent_trace({
        "task": "Deploy service",
        "events": [
            {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "5 passed"},
            {"role": "assistant", "content": "Tests passed. Deployment verified."}
        ]
    })

    if result["safe"]:
        print("Agent action verified. Safe to report success.")
    else:
        print(f"Agent action NOT verified. Score: {result['score']}")
        for f in result["findings"]:
            print(f"  - {f['rule_id']}: {f['message']}")
"""

from __future__ import annotations

from typing import Any

from .evaluator import evaluate_trace


def verify_agent_trace(trace: dict[str, Any], threshold: int = 0) -> dict[str, Any]:
    """Verify an agent trace and return a structured result.

    Args:
        trace: A dict with "task" (str) and "events" (list of event dicts).
        threshold: Max acceptable risk score. 0 = must pass all checks.

    Returns:
        dict with keys:
            - safe (bool): True if score <= threshold
            - score (int): Risk score 0-100
            - task (str): Task description
            - finding_count (int): Number of findings
            - findings (list): List of finding dicts
            - below_threshold (bool): True if score <= threshold
    """
    result = evaluate_trace(trace)
    return {
        "safe": result.score <= threshold,
        "score": result.score,
        "task": result.task,
        "finding_count": result.finding_count,
        "findings": [f.to_dict() for f in result.findings],
        "below_threshold": result.score <= threshold,
    }


def is_safe(trace: dict[str, Any], threshold: int = 0) -> bool:
    """Quick check: is this agent trace safe?

    Args:
        trace: A dict with "task" and "events".
        threshold: Max acceptable risk score.

    Returns:
        True if the trace passes all checks (or score <= threshold).
    """
    return verify_agent_trace(trace, threshold)["safe"]
