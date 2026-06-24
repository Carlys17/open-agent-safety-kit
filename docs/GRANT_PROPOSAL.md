# Grant Proposal Summary

## One line

Open-source safety tests for AI agents before real-world deployment.

## Problem

As AI agents become powerful enough to run commands, write code, manage infrastructure, and interact with protocols, control over safety evaluation is concentrating in the hands of a few closed-source incumbents. They are becoming the OPEC of intelligence safety — deciding what gets checked, how, and for whom.

Independent builders, open-source maintainers, and developers in emerging markets are being locked out of the tools they need to verify whether their agents are safe and truthful. If evaluation stays closed, the many who build in the open will always depend on the few who control the benchmarks.

## Solution

Open Agent Safety Kit is a local, open-source CLI that evaluates AI agent traces for practical failure modes: false success reporting, missing verification, dangerous shell commands, secret exposure, unsafe network writes, hallucinated file claims, and web3 transaction risks.

The rules, examples, scoring, and failure cases are all public under MIT license. Any builder can inspect the rules, adapt them, and run them locally — no API keys, no proprietary systems, no gatekeepers.

## Alignment with Sentient Foundation

This project directly supports Sentient's mission: keeping AGI open, decentralized, and aligned with humanity's interests.

- **Open by default**: MIT license, all rules and traces public, no closed dependencies
- **Decentralized safety**: builders run checks locally, not through a centralized platform
- **Serves the many**: designed for solo builders, small teams, and emerging-market developers who lack enterprise tooling
- **Prevents safety monopoly**: if evaluation tools stay open, no single entity controls what "safe" means for AI agents

## Users

- solo builders shipping with AI coding agents
- open-source maintainers reviewing agent-generated changes
- small AI teams without private evaluation infrastructure
- blockchain and infrastructure builders where tool mistakes become real losses
- developers in emerging markets who need local, inspectable, low-cost safety tooling

## What is open

The rules, traces, examples, scoring, docs, CLI, tests, and integrations are public under MIT license. At least one essential element (the safety evaluation engine) is openly available and contributes meaningfully to every builder's ability to deploy agents safely.

## Current state

Already working:
- installable Python package with `oask` CLI
- 7 safety rules with stable, documented IDs
- 8 unit tests covering all rules
- 5 example traces (safe and unsafe)
- GitHub Actions CI
- verbose CLI output for human-readable analysis
- comprehensive documentation

## 3 month milestone plan

Month 1 — Benchmark foundation:
- publish 20+ curated real-world agent failure traces
- stable, documented rule IDs
- redaction guide for safe trace sharing
- CI integration documentation

Month 2 — Integrations:
- transcript adapters for popular coding-agent CLIs
- web3 and infrastructure safety packs
- real-world case studies from builder workflows

Month 3 — Public v0.1:
- 50+ trace benchmark
- downstream project templates
- benchmark report with findings
- tagged public release

## Why now

Agent use is expanding faster than safety practices among independent builders. Capital is pouring into proprietary models and closed evaluation systems. The window to make practical safety tooling open is now, before the default becomes hidden benchmarks controlled by the few.

The future of intelligence should be built by the many, not controlled by the few. Safety evaluation is part of that future.

## Grant ask

$25,000 to turn the current prototype into a stronger public benchmark and toolkit for practical AI agent safety.
