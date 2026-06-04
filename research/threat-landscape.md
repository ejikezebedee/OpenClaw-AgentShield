# AI Agent Threat Landscape

Research date: 2026-06-04

## Executive Finding

AI abuse has moved from isolated chatbot jailbreaks toward agentic security risk: prompt injection, unsafe tool execution, data exfiltration, memory poisoning, RAG poisoning, software supply-chain compromise, and multi-agent instruction laundering.

The product opportunity is clear: corporations need a security layer purpose-built for AI agents, not just generic antivirus or chatbot moderation.

## Verified Source Base

1. OWASP Top 10 for LLM Applications 2025
   - URL: https://owasp.org/www-project-top-10-for-large-language-model-applications
   - Relevance: identifies critical LLM application risks including prompt injection, sensitive information disclosure, supply-chain risk, data/model poisoning, improper output handling, excessive agency, system prompt leakage, vector/embedding weaknesses, misinformation, and unbounded consumption.

2. OWASP Top 10 for Agentic Applications 2026
   - URL: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
   - Relevance: focuses on autonomous and agentic systems that plan, act, and make decisions across workflows.

3. OWASP MCP Top 10
   - URL: https://owasp.org/www-project-mcp-top-10/
   - Relevance: maps risks around model-context-protocol integrations, including token exposure, scope creep, prompt injection through context, command execution, and excessive permissions.

4. NIST AI Risk Management Framework: Generative AI Profile
   - URL: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
   - Relevance: enterprise risk-management foundation for trustworthy and responsible generative AI systems.

5. Microsoft Security Blog: When prompts become shells
   - URL: https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/
   - Relevance: explains why tool-connected AI agents can turn prompt-handling weaknesses into execution-layer risk.

6. MiroFish
   - URL: https://github.com/666ghj/MiroFish
   - Relevance: useful as inspiration for multi-agent simulation, scenario modeling, and red-team testing. It is not a dedicated security foundation.

## Threat Categories To Defend

### Prompt Injection

Untrusted content attempts to override, bypass, or redirect the agent's intended instructions. This may appear in chat messages, documents, webpages, emails, tickets, comments, transcripts, tool output, or retrieved knowledge.

Defensive requirement:

- scan user input and external content
- classify hostile instruction patterns
- quarantine untrusted text from privileged instructions
- require structured policy decisions before tool use

### Indirect Prompt Injection

The user may be benign, but the agent reads hostile content from an external source. The attack path is especially dangerous when the agent has tool access or sensitive context.

Defensive requirement:

- treat webpages, emails, PDFs, GitHub issues, support tickets, and search results as untrusted
- never flatten untrusted content into trusted instruction context
- isolate retrieved content and summarize through a low-privilege processor

### Excessive Agency

Agents with broad permissions can perform unintended actions because the model interprets language as authority.

Defensive requirement:

- least-privilege tool scopes
- per-tool policy manifests
- approval gates for destructive, external, financial, credential, deployment, or data-export actions
- deny-by-default execution for unclear intent

### Tool-Call Abuse

An agent may be tricked into calling tools with unsafe parameters or chaining harmless calls into harmful outcomes.

Defensive requirement:

- validate tool parameters
- classify tool intent before execution
- block unsafe combinations such as private data access plus external egress
- log all tool decisions

### Data Exfiltration

The agent may reveal private context, secrets, files, customer data, source code, internal policy, or credentials through normal output or external connectors.

Defensive requirement:

- secret scanning
- protected-data detection
- output filtering
- egress control
- audit trail for data movement

### Memory Poisoning

Hostile content may be written into persistent memory, changing future behavior across sessions.

Defensive requirement:

- scan every memory write
- mark memory provenance
- separate trusted operator memory from untrusted external memory
- expire or quarantine suspicious memory
- require approval before durable instruction updates

### RAG and Document Poisoning

Documents, embeddings, vector stores, or retrieval results may carry malicious instructions or false facts.

Defensive requirement:

- pre-ingestion document scanner
- retrieval-time risk scoring
- source provenance
- content trust labels
- citation requirement for high-impact decisions

### Agent-To-Agent Instruction Laundering

A compromised low-privilege agent can package an attacker instruction as a legitimate task for a higher-privilege agent.

Defensive requirement:

- agent identity and role boundaries
- message provenance
- inter-agent firewall
- task intent validation
- privilege escalation detection

### Skill, Plugin, and MCP Supply Chain Risk

Agent skills, plugins, connectors, and MCP servers can become execution-layer supply-chain risks.

Defensive requirement:

- manifest linting
- permission diffing
- source reputation checks
- signature/hash verification
- sandbox testing before installation

## Product Conclusion

OpenClaw AgentShield should be built as a layered enterprise defense:

- scanner before content enters the agent
- policy engine before tools run
- memory guard before persistence
- firewall between agents
- audit layer across everything
- red-team simulator to continuously test controls

