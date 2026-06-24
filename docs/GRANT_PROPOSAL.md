# Grant Proposal Summary

## One line

Open-source safety tests for AI agents before real-world deployment.

## Problem

AI agents are increasingly trusted to run commands, write code, operate infrastructure, and interact with protocols. Small builders need practical ways to check whether those agents are safe and truthful before deployment. Closed evaluation systems make this hard to inspect, adapt, or trust.

## Users

- solo builders
- open-source maintainers
- small AI teams
- blockchain and infrastructure builders
- developers in emerging markets who depend on open-source tools

## What is open

The rules, traces, examples, scoring, docs, and integrations are public under MIT license.

## 3 month milestone plan

Month 1:
- publish core CLI and JSON trace format
- add 20 real-world failure traces
- document local usage and CI usage

Month 2:
- add adapters for common coding-agent transcripts
- add web3 and infrastructure safety packs
- publish case studies

Month 3:
- release benchmark v0.1
- add GitHub Actions integration
- collect feedback from early builders

## Why now

Agent use is expanding faster than safety practices among independent builders. The window to make practical safety tooling open is now, before the default becomes closed private benchmarks.
