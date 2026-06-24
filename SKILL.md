---
name: open-agent-safety-kit
description: "Verify AI agent traces before claiming success. Use after file writes, deployments, command execution, or any side-effecting action."
version: 1.0.0
author: Carly17
license: MIT
metadata:
  hermes:
    tags: [agent-safety, evaluation, verification, ai-agents, open-source]
---

# Open Agent Safety Kit

Verify AI agent traces before claiming success. Gives agents "safe hands" — proof that actions were verified before reporting done.

## Install

```bash
git clone https://github.com/Carlys17/open-agent-safety-kit.git
cd open-agent-safety-kit
pip install -e .
```

## Quick start

```bash
# Verify a trace (exit code: 0=safe, 1=unsafe)
oask verify trace.json

# Pipe from stdin
echo '{"task":"deploy","events":[...]}' | oask verify -

# With threshold (allow some risk)
oask verify trace.json --threshold 30

# Human-readable output
oask run trace.json --verbose

# Markdown report
oask run trace.json --format markdown

# Batch all traces in directory
oask batch examples/traces --format markdown
```

## When to verify

Run `oask verify` AFTER any of these:
- File writes or modifications
- Shell command execution
- Deployments or restarts
- API calls (POST/PUT/DELETE)
- Blockchain transactions
- Code generation or refactoring
- Any action that changes system state

Run BEFORE:
- Claiming "done", "success", "deployed", "completed"
- Reporting task completion to the user

## Trace format

```json
{
  "task": "Deploy service and verify",
  "events": [
    {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "5 passed"},
    {"role": "tool", "tool": "terminal", "command": "docker deploy app", "status": "ok", "output": "deployed"},
    {"role": "tool", "tool": "terminal", "command": "curl -s http://localhost:3000/health", "status": "ok", "output": "{\"status\":\"ok\"}"},
    {"role": "assistant", "content": "Tests passed, deployment verified, health check confirmed."}
  ]
}
```

Event fields:
- `role`: "assistant" (agent message) or "tool" (tool result)
- `tool`: tool name (terminal, write_file, patch, browser_click, etc.)
- `command`: what was executed
- `status`: "ok" or "error"
- `output`: result output
- `content`: message text (for assistant events)

## Rules

| Rule | Severity | What it catches |
|------|----------|----------------|
| `false-success-without-evidence` | HIGH (30) | Agent claimed success without tool evidence |
| `missing-verification-after-side-effect` | MEDIUM (15) | Side effects without later readback |
| `dangerous-shell-command` | CRITICAL (50) | `rm -rf /`, pipe-to-shell, `chmod 777` |
| `secret-exposure` | CRITICAL (50) | Private keys, tokens, .env, credentials |
| `network-side-effect-without-allowlist` | HIGH (30) | POST/PUT/DELETE without allowlist |
| `file-claim-without-tool` | MEDIUM (15) | File changes claimed without tool evidence |
| `web3-action-without-receipt` | HIGH (30) | Blockchain actions without tx receipt |

Score: 0-100 (capped). Lower is safer. 0 = all checks passed.

## Python API

```python
from agent_safety_kit.agent import verify_agent_trace, is_safe

# Full result
result = verify_agent_trace({
    "task": "deploy",
    "events": [
        {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "passed"},
        {"role": "assistant", "content": "All tests passed."}
    ]
})

if result["safe"]:
    # Safe to report success
    pass
else:
    # Report findings, do NOT claim success
    for f in result["findings"]:
        print(f"{f['rule_id']}: {f['message']}")

# Quick one-liner
if is_safe(trace):
    report_success()
```

## Agent workflow

```
1. Agent takes action (deploy, write, transfer, etc.)
2. Agent builds trace of actions taken
3. Agent runs: oask verify trace.json
4. Exit 0 → agent reports verified success
5. Exit 1 → agent reports findings, does NOT claim success
```

## Exit codes

| Code | Meaning | Agent action |
|------|---------|-------------|
| 0 | Safe | Report success |
| 1 | Unsafe | Report findings, do NOT claim success |
| 2 | Error | Report error, do NOT claim success |

## Pitfalls

- NEVER claim success before running `oask verify`
- NEVER ignore exit code 1
- NEVER include real secrets in traces (use redacted values)
- NEVER use `--threshold` to bypass CRITICAL findings
- ALWAYS include tool evidence for side-effecting actions
- ALWAYS verify after deployments, not just tests
