# Buyer Quickstart

## What This Does

OpenClaw AgentShield is an AI Agent Security Audit Toolkit. It scans prompts, documents, memory files, logs, and agent context files for risks that can affect AI agents and LLM applications.

It helps identify:

- prompt injection
- system-prompt extraction attempts
- data exfiltration requests
- destructive tool intent
- memory poisoning
- agent-to-agent privilege laundering
- high-autonomy agent requests touching privileged tools
- MCP/tool-manifest risk
- weak egress controls
- approval-fatigue risk

## Who Should Use It

Use AgentShield if your company, client, or internal team is connecting AI agents to files, tools, RAG databases, memory, browsers, inboxes, APIs, plugins, MCP servers, or other agents.

## Requirements

- Python 3.10 or newer
- Terminal access
- No cloud account required
- No API key required for the local MVP

## Step 1: Confirm Python

```bash
python3 --version
```

If that does not work, try:

```bash
python --version
```

## Step 2: Scan One File

```bash
python3 -m agentshield.cli examples/benign-request.txt --pretty
```

Expected result: a JSON report with `decision` set to `allow`.

## Step 3: Scan A Risky Example

```bash
python3 -m agentshield.cli examples/risky-exfiltration.txt --pretty
```

Expected result: a higher-risk decision such as `block`.

## Step 4: Scan A Directory

```bash
python3 -m agentshield.cli examples --pretty --report reports/examples-scan.json
```

This scans supported text-like files and writes a JSON report.

The included examples also cover Mythos-ready risks such as autonomous agent execution and over-permissive MCP/tool manifests.

## Step 5: Generate A Markdown Report

```bash
python3 -m agentshield.cli examples --markdown-report reports/examples-scan.md
```

Use Markdown reports for management reviews, audit notes, and buyer-facing evidence.

## Step 6: Use A Custom Policy

```bash
python3 -m agentshield.cli examples --policy policies/default-policy.json --pretty
```

Edit `policies/default-policy.json` when your team wants custom categories, wording, severities, or decisions.

## Step 7: Use CI-Style Failure Mode

Use `--fail-on-risk` when you want the command to return a non-zero exit code for risky content.

```bash
python3 -m agentshield.cli examples --fail-on-risk
```

This is useful for release gates, pre-deployment checks, and manual security checklists.

## Output Decisions

- `allow`: no security issue detected by the current rules.
- `quarantine`: keep content away from privileged agent context.
- `approval_required`: human review required before action.
- `block`: do not allow this content or action to proceed.

## Practical Enterprise Workflow

1. Scan incoming documents before agent ingestion.
2. Scan memory files before saving durable agent memory.
3. Scan tool-call requests before execution.
4. Save JSON reports for audit evidence.
5. Save Markdown reports for review meetings.
6. Review quarantine/block events with security, compliance, or operations.
7. Update policy rules as new agent risks appear.

## Troubleshooting

If `python3` is not recognized, use `python` in the commands instead.

If a path is not found, run the command from the AgentShield product folder.

If a report file is missing, check the path passed to `--report` or `--markdown-report`.

If the scanner reports risk in a file that looks harmless, open the report and review the `evidence` field. The scanner is intentionally conservative for agent safety.

If the report includes `impact` and `recommended fix`, use those fields as the first review notes for security, compliance, or engineering.

If the scanner misses a phrase that matters to your company, add a custom rule to the policy file and rerun the scan.

## Defensive-Only Use

AgentShield is for auditing, hardening, compliance support, and safe internal testing. It is not an exploitation toolkit and should not be used for unauthorized activity.
