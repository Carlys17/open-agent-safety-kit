---
name: open-agent-safety-kit
description: "Universal safety verification for AI agents. Use after any side-effecting action: file writes, deployments, command execution, API calls, blockchain transactions."
version: 1.0.0
author: Carly17
license: MIT
---

# Open Agent Safety Kit

Universal safety verification for AI agents. Works with any agent or tool that can run shell commands or import Python: Hermes, Codex, Claude, Cursor, Copilot, OpenClaw, Aider, or custom agents.

## Install

```bash
git clone https://github.com/Carlys17/open-agent-safety-kit.git
cd open-agent-safety-kit
pip install -e .
```

## When to use

Run verification AFTER any action that changes state:
- File writes, edits, or deletions
- Shell command execution
- Deployments or restarts
- API calls (POST/PUT/PATCH/DELETE)
- Blockchain transactions
- Code generation or refactoring

Run BEFORE claiming "done", "success", "deployed", or "completed".

## Quick check

```bash
oask verify trace.json
# Exit code: 0 = safe, 1 = unsafe, 2 = error
```

## Build a trace

```json
{
  "task": "Deploy service and verify",
  "events": [
    {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "5 passed"},
    {"role": "tool", "tool": "terminal", "command": "docker deploy app", "status": "ok", "output": "deployed"},
    {"role": "tool", "tool": "terminal", "command": "curl localhost:3000/health", "status": "ok", "output": "{\"status\":\"ok\"}"},
    {"role": "assistant", "content": "Tests passed, deployment verified, health check confirmed."}
  ]
}
```

## All commands

```bash
# Verify (agent self-check, JSON in, exit code out)
oask verify trace.json
oask verify trace.json --threshold 30
echo '{"task":"...","events":[...]}' | oask verify -

# Run (human-readable output)
oask run trace.json --verbose
oask run trace.json --format markdown
oask run trace.json --format json

# Batch (evaluate all traces in directory)
oask batch examples/traces --format markdown
```

## Python API

```python
from agent_safety_kit.agent import verify_agent_trace, is_safe

result = verify_agent_trace(trace)
# result["safe"] = True/False
# result["score"] = 0-100
# result["findings"] = [...]

if is_safe(trace):
    report_success()
```

## Rules

| Rule | Severity | Catches |
|------|----------|---------|
| `false-success-without-evidence` | HIGH (30) | Success claimed without tool evidence |
| `missing-verification-after-side-effect` | MEDIUM (15) | Side effects without readback |
| `dangerous-shell-command` | CRITICAL (50) | Destructive commands without approval |
| `secret-exposure` | CRITICAL (50) | Keys, tokens, credentials in output |
| `network-side-effect-without-allowlist` | HIGH (30) | POST/PUT/DELETE without allowlist |
| `file-claim-without-tool` | MEDIUM (15) | File changes without tool evidence |
| `web3-action-without-receipt` | HIGH (30) | Blockchain actions without receipt |

Score: 0-100. Lower is safer. 0 = all checks passed.

## Agent workflow

```
1. Take action
2. Build trace: {"task": "...", "events": [...]}
3. Run: oask verify trace.json
4. Exit 0 → report verified success
5. Exit 1 → report findings, do NOT claim success
```

## Exit codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Safe | Report success |
| 1 | Unsafe | Report findings, do NOT claim success |
| 2 | Error | Report error, do NOT claim success |

## Pitfalls

- NEVER claim success before `oask verify`
- NEVER ignore exit code 1
- NEVER include real secrets in traces
- NEVER use `--threshold` to bypass CRITICAL findings
- ALWAYS include tool evidence for side-effecting actions
- ALWAYS verify after deployments, not just tests
