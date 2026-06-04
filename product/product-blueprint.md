# OpenClaw AgentShield Product Blueprint

## Product Title

OpenClaw AgentShield: AI Agent Security Firewall for Corporate AI Workflows

## One-Line Offer

Detect, block, and audit prompt injection, unsafe tool calls, memory poisoning, and AI-agent data exfiltration before they become enterprise incidents.

## Target Buyers

- CISOs
- security engineering teams
- AI governance teams
- enterprise IT departments
- SaaS companies adding AI agents
- regulated businesses using AI with customer or operational data
- AI automation consultancies

## Core Use Cases

1. Scan AI-agent inputs before execution.
2. Scan webpages, PDFs, emails, tickets, and docs before ingestion.
3. Block risky tool calls unless policy allows them.
4. Prevent untrusted content from becoming persistent memory.
5. Produce audit logs for blocked attempts and approved actions.
6. Generate enterprise risk reports for leadership and compliance.
7. Run safe red-team simulations against corporate agents.

## Architecture

### Layer 1: Input Scanner

Classifies incoming content:

- normal user instruction
- untrusted external content
- prompt-injection attempt
- sensitive-data request
- system-prompt extraction attempt
- jailbreak or policy-bypass attempt
- suspicious encoded or hidden instruction
- benign security discussion

Output:

- risk score
- category
- recommended decision: allow, allow-with-warning, quarantine, redact, approval-required, block
- evidence summary

### Layer 2: Context Isolation

Separates:

- trusted system policy
- trusted operator instruction
- untrusted user input
- untrusted tool output
- retrieved documents
- memory records
- agent-to-agent messages

Rule:

Untrusted content can be analyzed, summarized, cited, or transformed, but it must not become authority over tools, policy, credentials, approvals, or system behavior.

### Layer 3: Tool Gatekeeper

Every tool call receives a policy decision before execution.

Inputs:

- actor identity
- requested tool
- tool parameters
- originating content source
- risk score
- data sensitivity
- action type

Decisions:

- allow
- require confirmation
- require elevated approval
- redact parameters
- sandbox only
- block

High-risk action classes:

- shell execution
- file write/delete
- network egress
- credential access
- external messaging
- financial action
- production deployment
- database modification
- memory update
- account/profile change

### Layer 4: Memory Guard

Scans memory writes and updates for:

- hidden instructions
- attacker persistence
- credential leakage
- false identity claims
- policy override attempts
- malicious task continuation
- unsafe personal data retention

Memory decisions:

- write trusted memory
- write untrusted observation
- quarantine
- redact then write
- require approval
- block

### Layer 5: RAG and Document Guard

Before ingestion:

- extract text
- detect hidden or instruction-like content
- identify sensitive data
- classify provenance
- score trust level

At retrieval:

- attach source trust labels
- prevent retrieved content from issuing commands
- require citations for claims
- block dangerous retrieval-to-tool chains

### Layer 6: Agent-To-Agent Firewall

Controls messages between agents:

- validate sender identity
- preserve provenance
- label delegated authority
- detect instruction laundering
- prevent low-privilege agents from commanding high-privilege agents
- require approval for cross-agent escalation

### Layer 7: Audit and Reporting

Every security decision should produce structured logs:

- timestamp
- agent identity
- source channel
- content type
- risk category
- tool requested
- decision
- policy rule triggered
- human approval status
- redaction summary

Reports:

- daily security summary
- blocked prompt-injection attempts
- risky tool-call report
- memory quarantine report
- AI compliance report
- buyer-facing PDF export

## MVP Build Scope

### MVP 1: CLI Scanner and Policy Engine

Deliver:

- local scanner for text files, markdown, prompts, tool logs, and memory files
- JSON risk output
- policy rules YAML
- allow/block/approval decisions
- audit log writer
- sample test corpus
- buyer documentation

### MVP 2: Runtime Middleware

Deliver:

- Python/Node middleware wrapper
- tool-call interception
- policy checks before execution
- memory write interception
- RAG document pre-scan

### MVP 3: Dashboard and Reports

Deliver:

- local dashboard
- risk trend charts
- blocked event timeline
- compliance export
- team policy configuration

### MVP 4: Red-Team Simulator

Deliver:

- safe defensive test scenarios
- multi-agent simulation inspired by MiroFish-style swarm testing
- control effectiveness report
- no operational attack automation

## Rule Engine Starting Categories

- `prompt_injection`
- `indirect_prompt_injection`
- `jailbreak`
- `system_prompt_extraction`
- `data_exfiltration`
- `credential_exposure`
- `destructive_tool_intent`
- `network_egress_risk`
- `memory_poisoning`
- `rag_poisoning`
- `agent_laundering`
- `benign_security_discussion`

## Product Differentiation

AgentShield should compete on practical enterprise execution:

- local-first
- auditable
- policy-driven
- agent-aware
- memory-aware
- tool-call-aware
- buyer-portable
- OpenClaw-native but framework-adaptable

## Pricing Direction

Starter digital product:

- CLI scanner + policy templates + report generator
- $49-$149

Professional:

- runtime middleware + advanced policies + dashboard
- $299-$999

Enterprise:

- custom deployment, integration, reporting, support
- quote-based

## Gumroad Product Requirements

Every release package should include:

- clear title and positioning
- buyer pain point
- practical tool or template
- setup instructions
- examples
- troubleshooting
- sales page copy
- pricing justification
- final release checklist

