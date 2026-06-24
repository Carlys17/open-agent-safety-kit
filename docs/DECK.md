# Open Agent Safety Kit Deck

## 1. Title
Open Agent Safety Kit
Open-source safety tests for AI agents before real-world deployment.

## 2. Problem
Agents now write code, run shell commands, deploy services, and interact with protocols. Many look successful while failing silently: no verification, unsafe commands, hallucinated results, or leaked secrets.

## 3. Why it matters
Independent builders and emerging-market developers rely on open-source AI tools but do not have access to enterprise safety systems. If evaluation stays closed, small builders cannot inspect or adapt the rules that judge their agents.

## 4. Solution
A local, open-source toolkit that evaluates agent traces for practical failure modes: false success, missing verification, unsafe tool use, secret exposure, unsafe network writes, and blockchain transaction risks.

## 5. Demo
Run:
`oask run examples/traces/unsafe_false_success.json --format markdown`

The toolkit flags an agent that claims deployment success without tool evidence.

## 6. Grant unlock
Funding turns the prototype into a usable public good: more traces, adapters, docs, CI integration, web3 safety pack, and case studies.
