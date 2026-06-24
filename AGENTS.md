# Open Agent Safety Kit

Use `oask` to verify AI agent traces before claiming success.

## When to use

- After an agent completes a task involving file writes, deployments, or command execution
- Before an agent reports "done" or "success"
- When reviewing agent-generated code changes
- In CI pipelines to gate agent output

## Commands

```bash
# Verify a trace (agent self-check)
oask verify trace.json

# Verify from stdin (pipe-friendly)
echo '{"task":"...","events":[...]}' | oask verify -

# Verify with threshold (allow some risk)
oask verify trace.json --threshold 30

# Run with verbose output (human-readable)
oask run trace.json --verbose

# Run with markdown report
oask run trace.json --format markdown

# Batch all traces in a directory
oask batch examples/traces --format markdown
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
    {"role": "assistant", "content": "I will deploy and test it."},
    {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "5 passed"},
    {"role": "assistant", "content": "Tests passed: 5 passed."}
  ]
}
```

Event roles:
- `assistant` - agent message
- `tool` - tool call result (should include `tool`, `command`, `status`, `output`)

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

# Full result
result = verify_agent_trace(trace)
if result["safe"]:
    print("Verified")

# Quick check
if is_safe(trace):
    report_success()
```

## Agent workflow

```
1. Agent takes action (deploy, transfer, write file, etc.)
2. Agent builds trace of its actions
3. Agent calls: oask verify trace.json
4. If exit code 0 → agent reports verified success
5. If exit code 1 → agent reports findings, does NOT claim success
```

## Pitfalls

- Don't claim success before running `oask verify`
- Don't ignore exit code 1 findings
- Don't include real secrets in traces (use redacted values)
- Don't use `--threshold` to bypass critical findings
