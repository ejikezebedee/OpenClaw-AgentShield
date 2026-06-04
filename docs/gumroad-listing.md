# Gumroad Listing

## Product Title

OpenClaw AgentShield - Mythos-Ready AI Agent Security Audit Toolkit

## Short Description

A defensive AI-agent security scanner and policy toolkit for auditing prompts, documents, memory files, logs, MCP/tool manifests, and agent context before they reach tool-using AI agents.

## Long Description

AI agents are being connected to files, inboxes, browsers, CRMs, APIs, RAG systems, memory, plugins, and other agents. That creates a new security problem: malicious or unsafe instructions can hide inside normal-looking documents, webpages, support tickets, logs, memory entries, and tool output.

OpenClaw AgentShield gives teams a practical starting point for AI-agent security reviews. It scans text-like files and folders for prompt injection, system-prompt extraction attempts, data exfiltration requests, destructive tool intent, memory poisoning, agent-to-agent privilege laundering, high-autonomy agent risk, MCP/tool-manifest risk, weak egress controls, and approval-fatigue patterns.

This is a defensive MVP package for security teams, AI automation consultants, SaaS teams, compliance teams, and operators building internal AI-agent governance.

## What Is Included

- Local AI-agent security scanner
- Prompt, document, log, memory, and context scanning
- Configurable JSON policy file
- JSON report output
- Markdown report output
- JSONL audit log output
- Mythos-ready risk categories
- MCP/tool-manifest review examples
- Safe example files
- Buyer quickstart guide
- Mythos-ready agent security guide
- Defensive threat landscape brief
- Product architecture blueprint
- Final release audit checklist
- Sales and positioning copy

## Buyer Pain Point

Traditional security tools were not designed for natural-language instructions hidden inside the content AI agents read. AgentShield helps buyers add a practical review layer before agents ingest content, save memory, call tools, or share context with other agents.

## Recommended Price

Launch price: $49.

Standard starter price: $79.

Future professional tier: $299 to $999 after adding dashboard, middleware, integrations, and advanced reporting.

## Best-Fit Buyers

- Security teams adopting AI agents
- AI automation consultants
- SaaS teams adding autonomous workflows
- Compliance and governance teams
- Companies using RAG, memory, tools, plugins, or MCP-style integrations
- Internal operations teams that need repeatable AI-agent review evidence

## What Buyers Can Do Immediately

1. Scan a prompt, document, log, or memory file.
2. Scan a folder of agent context files.
3. Generate JSON and Markdown reports.
4. Review risky findings with rule IDs, severity, decisions, and evidence.
5. Customize policy language for internal governance.
6. Use `--fail-on-risk` in a manual release gate or CI-style check.

## Simple Setup

Requirements:

- Python 3.10 or newer
- Terminal access
- No cloud account required
- No API key required

Example command:

```bash
python3 -m agentshield.cli examples --pretty --report reports/examples-scan.json --markdown-report reports/examples-scan.md
```

## Disclaimer

AgentShield is defensive software. It does not guarantee complete protection, does not replace security review, and does not provide exploitation playbooks. It reduces AI-agent risk through scanning, policy decisions, audit evidence, and human approval gates for high-risk actions.
