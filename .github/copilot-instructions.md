# Open Agent Safety Kit - Copilot Instructions

## Project

Open-source safety tests for AI agents before real-world deployment.

## Safety verification

After completing any task that involves file writes, deployments, or command execution:

1. Build a trace of actions taken
2. Run: `oask verify trace.json`
3. Only report success if exit code is 0
4. If exit code is 1, report the findings and do NOT claim success

## Quick commands

```bash
# Verify agent actions
oask verify trace.json

# Pipe trace
echo '{"task":"...","events":[...]}' | oask verify -

# Human-readable output
oask run trace.json --verbose
```

## Trace format

```json
{
  "task": "Description",
  "events": [
    {"role": "tool", "tool": "terminal", "command": "...", "status": "ok", "output": "..."},
    {"role": "assistant", "content": "Summary."}
  ]
}
```
