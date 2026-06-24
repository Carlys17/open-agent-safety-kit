# Claude Code Instructions

See [SKILL.md](../SKILL.md) for full agent instructions.

## Quick reference

```bash
# Install
pip install -e .

# Verify before claiming success
oask verify trace.json
```

Exit code 0 = safe, 1 = unsafe. Never claim success if exit code is 1.
