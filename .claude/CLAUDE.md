# Open Agent Safety Kit - Agent Instructions

## Project

Open-source safety tests for AI agents before real-world deployment.
Repository: https://github.com/Carlys17/open-agent-safety-kit

## How to use

```bash
# Install (first time)
cd /path/to/open-agent-safety-kit
pip install -e .

# Verify agent actions before claiming success
oask verify trace.json

# Pipe trace from stdin
echo '{"task":"...","events":[...]}' | oask verify -

# Human-readable output
oask run trace.json --verbose
```

## When to verify

After ANY of these actions:
- File writes or modifications
- Shell command execution
- Deployments
- API calls
- Blockchain transactions
- Code generation

## How to build a trace

```json
{
  "task": "Description of what you did",
  "events": [
    {"role": "tool", "tool": "terminal", "command": "...", "status": "ok", "output": "..."},
    {"role": "tool", "tool": "write_file", "command": "path/to/file", "status": "ok", "output": "written"},
    {"role": "assistant", "content": "Summary of what was done."}
  ]
}
```

## Rules

Exit code 0 = safe. Exit code 1 = unsafe (do NOT claim success).

Critical rules that always fail:
- `secret-exposure` - never include real keys/tokens in traces
- `dangerous-shell-command` - never run `rm -rf /` or similar

## Integration

See docs/INTEGRATIONS.md for Hermes, Claude Code, Copilot, Cursor, Aider patterns.
