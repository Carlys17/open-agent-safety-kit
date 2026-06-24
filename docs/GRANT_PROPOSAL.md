# Grant Proposal Summary

## One line

Open-source safety tests for AI agents — giving agents safe hands before they act on our behalf.

## Problem

A few companies are tightening their grip on AI safety evaluation. Access is metered, priced, and revocable overnight. A developer in Lagos, Bangalore, or Jakarta can lose the safety tools their work depends on without warning.

AI agents are about to act on our behalf — writing code, deploying services, managing infrastructure, handling transactions. But most builders have no way to verify whether their agents are safe and truthful before deployment. If safety evaluation stays closed, the defaults get set behind glass: metered, surveilled, revocable, shaped for whoever pays most.

## Solution

Open Agent Safety Kit is a local, open-source CLI that evaluates AI agent traces for practical failure modes. It gives agents safe hands: proof that an agent did what it claims, before builders trust it with real tasks.

The toolkit checks for:
- false success reporting (agent claims success without evidence)
- missing verification (side effects without readback)
- dangerous shell commands (destructive actions without approval)
- secret exposure (keys, tokens, credentials leaked)
- unsafe network writes (API calls without allowlist)
- hallucinated file claims (file changes without tool evidence)
- web3 transaction risks (blockchain actions without receipt)

Everything runs locally. No API keys. No data leaves the builder's device. No proprietary dependencies.

## Alignment with Sentient's 6 beliefs

**Open**: MIT license. Anyone can run it, inspect it, and build on it.

**Yours to keep**: No lock-in, no proprietary dependencies, no API keys required. A tool you can be cut off from was never yours.

**Accessible**: Pure Python. No GPU required. Runs on any machine, including the hardware people actually own in emerging markets.

**Good for humanity**: Protects independent builders and open-source maintainers from deploying unsafe agents. Makes real workflows measurably safer, especially for those the market overlooked.

**Private by default**: All evaluation runs locally. Agent traces never leave the builder's device. No telemetry, no cloud dependency.

**Empowering, not extractive**: Hands builders a capability to verify their agents. Does not harvest data, does not require accounts, does not gate access.

## What we build (Sentient's framework)

This project addresses one of Sentient's core infrastructure requests:

> "Identity and safe hands for the agents about to act on our behalf."
> "Proof that a model is what it claims and did what it says."

Open Agent Safety Kit is the safety layer for agents. Before an agent deploys, transfers, or claims success, builders can verify its actions against open, inspectable rules. This is what "safe hands" means in practice.

## Users

- solo builders shipping with AI coding agents
- open-source maintainers reviewing agent-generated changes
- small AI teams without private evaluation infrastructure
- blockchain and infrastructure builders where tool mistakes become real losses
- developers in emerging markets who need local, inspectable, low-cost safety tooling

## What is open

Everything. Rules, traces, examples, scoring, docs, CLI, tests, and integrations — all MIT, all public. No essential element is closed or gated.

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
- 20+ curated real-world agent failure traces
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

The window is open now, and it does not stay open. Open models are within striking distance of the frontier. If closed labs set the defaults for agent safety evaluation, those defaults get set behind glass. If open builders win the race, the default flips because open tools, once released, can never be taken back.

We are funding the people who move through that window. This is our move.

## Grant ask

$25,000 to turn the current prototype into a stronger public benchmark and toolkit for practical AI agent safety.

## Beyond the grant

With Sentient's support beyond funding:
- **Distribution**: getting the toolkit in front of the builders who need it most
- **Compute**: credits for running large-scale benchmark evaluations
- **Engineering**: guidance from the Sentient Stack team on integrating with agent frameworks
- **Community**: connecting with other open-source AI builders in the ecosystem
