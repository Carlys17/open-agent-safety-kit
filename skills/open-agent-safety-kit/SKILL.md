---
name: open-agent-safety-kit
description: "Verify AI agent traces before claiming success. Use when an agent completes a task involving file writes, deployments, or command execution."
version: 1.0.0
author: Carly17
license: MIT
metadata:
  hermes:
    tags: [agent-safety, evaluation, verification, ai-agents, open-source]
---

# Open Agent Safety Kit

Verify AI agent traces before claiming success.

## When to use

- After an agent completes a task involving file writes, deployments, or command execution
- Before an agent reports "done" or "success"
- When reviewing agent-generated code changes
- In CI pipelines to gate agent output

## Quick start

```bash
# Install (first time only)
pip install -e /path/to/open-agent-safety-kit

# Verify agent actions
oask verify trace.json

# Pipe trace from stdin
echo '{"task":"...","events":[...]}' | oask verify -

# Human-readable output
oask run trace.json --verbose
```

## Exit codes

- `0` = safe (score <= threshold, or all checks passed)
- `1` = unsafe (findings detected)
- `2` = error (invalid JSON, file not found)

## Trace format

```json
{
  "task": "Deploy service",
  "events": [
    {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "5 passed"},
    {"role": "assistant", "content": "Tests passed: 5 passed."}
  ]
}
```

## Rules

| Rule ID | Severity | Catches |
|---------|----------|---------|
| `false-success-without-evidence` | HIGH | Success claimed without tool evidence |
| `missing-verification-after-side-effect` | MEDIUM | Side effects without readback |
| `dangerous-shell-command` | CRITICAL | Destructive commands without approval |
| `secret-exposure` | CRITICAL | Keys, tokens, credentials in output |
| `network-side-effect-without-allowlist` | HIGH | POST/PUT/DELETE without allowlist |
| `file-claim-without-tool` | MEDIUM | File changes without tool evidence |
| `web3-action-without-receipt` | HIGH | Blockchain actions without receipt |

## Python API

```python
from agent_safety_kit.agent import verify_agent_trace, is_safe

result = verify_agent_trace(trace)
if result["safe"]:
    print("Verified")
```

## Agent workflow

```
1. Agent takes action
2. Agent builds trace
3. Agent calls: oask verify trace.json
4. Exit 0 → agent reports verified success
5. Exit 1 → agent reports findings, does NOT claim success
```

## Pitfalls

- Don't claim success before running `oask verify`
- Don't ignore exit code 1 findings
- Don't include real secrets in traces
- Don't use `--threshold` to bypass critical findings
