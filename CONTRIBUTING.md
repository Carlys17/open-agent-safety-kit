# Contributing

Open Agent Safety Kit is designed to be easy to inspect and extend.

## Good first contributions

- Add a new unsafe trace in `examples/traces/`
- Add a new rule in `src/agent_safety_kit/rules.py`
- Add a regression test in `tests/test_evaluator.py`
- Improve docs for local builders
- Add adapters for agent transcript formats

## Rule quality bar

A useful rule should:

1. catch a real agent failure mode
2. include clear evidence
3. avoid flagging normal safe behavior
4. include a recommendation that a builder can act on
5. have at least one unit test

## Local checks

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python -m unittest discover -s tests
oask batch examples/traces --format markdown
```

## Trace contribution format

Please remove secrets and personal data from traces. Keep the failure realistic, but safe to publish.
