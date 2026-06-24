# Agent Integrations

Open Agent Safety Kit works with any AI agent that can run shell commands or import Python. Here are integration patterns for popular tools.

## Hermes Agent

Add as a shell hook to verify agent actions automatically:

```yaml
# In Hermes config.yaml
hooks:
  post_tool:
    - name: oask-verify
      command: |
        echo '{{tool_result}}' | oask verify - 2>/dev/null || true
```

Or use the Python API in a custom tool:

```python
from agent_safety_kit.agent import is_safe

def verify_before_report(trace: dict) -> bool:
    """Call before agent claims success."""
    if not is_safe(trace):
        return False  # Agent should NOT claim success
    return True
```

## Claude Code

Add to your project's `CLAUDE.md` or `.claude/commands`:

```markdown
## Safety check

Before claiming any task is complete, run:
```
oask verify /tmp/agent_trace.json --threshold 0
```

If exit code is 1, report the findings and do NOT claim success.
```

Or create a wrapper script:

```bash
#!/bin/bash
# claude-safe.sh - Run Claude Code with safety checks
# Usage: ./claude-safe.sh "your prompt here"

TRACE_FILE="/tmp/claude_trace_$(date +%s).json"

# Run Claude Code and capture output
claude "$@" 2>&1 | tee /tmp/claude_output.log

# Build trace from output
python3 -c "
import json, sys
output = open('/tmp/claude_output.log').read()
trace = {
    'task': '$*',
    'events': [{'role': 'assistant', 'content': output[:2000]}]
}
json.dump(trace, open('$TRACE_FILE', 'w'))
"

# Verify
oask verify "$TRACE_FILE"
```

## GitHub Copilot

Add to `.github/copilot-instructions.md`:

```markdown
After completing any task that involves file writes, deployments, or command execution:
1. Build a trace of actions taken
2. Run: oask verify trace.json
3. Only report success if exit code is 0
```

## Cursor / Aider / Generic coding agents

Most coding agents support pre/post hooks or custom instructions. Add this pattern:

```markdown
## Safety verification

After any tool use that modifies files, runs commands, or deploys:
1. Collect the actions into a trace: {"task": "...", "events": [...]}
2. Run: echo '$TRACE' | oask verify -
3. If exit code != 0, report findings and do NOT claim success
4. If exit code == 0, claim verified success
```

## Direct shell integration

Any agent that runs shell commands can use this pattern:

```bash
# Agent builds its trace, then verifies
cat > /tmp/trace.json << 'EOF'
{
  "task": "Deploy service",
  "events": [
    {"role": "tool", "tool": "terminal", "command": "npm test", "status": "ok", "output": "5 passed"},
    {"role": "tool", "tool": "terminal", "command": "docker deploy", "status": "ok", "output": "deployed"},
    {"role": "assistant", "content": "Deployment verified."}
  ]
}
EOF

# Verify - exit code determines if agent should claim success
oask verify /tmp/trace.json
echo "Exit code: $?"  # 0=safe, 1=unsafe
```

## Python SDK

```python
from agent_safety_kit.agent import verify_agent_trace, is_safe

# In your agent's code
def agent_complete_task(task_result: dict, actions: list):
    """Call this before agent reports task completion."""
    trace = {
        "task": task_result.get("task", "unknown"),
        "events": actions
    }

    result = verify_agent_trace(trace)

    if not result["safe"]:
        return {
            "status": "verification_failed",
            "score": result["score"],
            "findings": result["findings"],
            "message": "Agent actions could not be verified. Not claiming success."
        }

    return {
        "status": "verified",
        "score": result["score"],
        "message": "Agent actions verified. Safe to report success."
    }
```

## CI/CD integration

```yaml
# GitHub Actions
- name: Verify agent output
  run: |
    oask verify agent_trace.json --threshold 0
```

```yaml
# GitLab CI
verify-agent:
  script:
    - oask verify agent_trace.json --threshold 0
```

## Custom agent framework

If you're building your own agent:

```python
from agent_safety_kit.agent import verify_agent_trace

class SafeAgent:
    def complete(self, task: str, actions: list) -> dict:
        trace = {"task": task, "events": actions}
        result = verify_agent_trace(trace)

        if result["safe"]:
            return {"status": "success", "verified": True}
        else:
            return {
                "status": "failed_safety_check",
                "verified": False,
                "score": result["score"],
                "findings": result["findings"]
            }
```
