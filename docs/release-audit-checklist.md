# Release Audit Checklist

Use this before marking AgentShield as commercial-ready.

## Defensive-Only Safety

- [x] No exploitation instructions.
- [x] No credential harvesting instructions.
- [x] No stealth, persistence, evasion, or unauthorized access workflow.
- [x] No reusable malicious payload library.
- [x] Red-team examples are safe, abstracted, and defensive.

## Product Quality

- [x] Title is clear: OpenClaw AgentShield.
- [x] Enterprise positioning is clear: AI Agent Security Audit Toolkit.
- [x] Mythos-ready positioning is clear for frontier agent risk.
- [x] Buyer pain point is obvious.
- [x] Setup instructions are complete for local MVP use.
- [x] Examples are included.
- [x] Troubleshooting is included.
- [x] Pricing justification is included.
- [x] Release package includes a final checklist.
- [x] Gumroad listing copy is included.
- [x] Mythos-ready agent security guide is included.

## Technical Readiness

- [x] Scanner works locally.
- [x] Policy engine produces deterministic decisions.
- [x] JSON output is documented.
- [x] Markdown report output is documented.
- [x] Audit logs are structured as JSONL.
- [x] Tool-call decisions are explainable through rule IDs, severity, evidence, and decisions.
- [x] Reports include impact and recommended fix fields.
- [x] Memory writes are scanned through the same file/context pipeline.
- [x] RAG/document scanning path is documented as directory scanning for text-like files.
- [x] MCP/tool-manifest risk scanning is included.
- [x] Approval-fatigue and egress-control risk rules are included.
- [x] Tests cover benign security discussion vs harmful instruction attempts.

## Commercial Cleanup

- [x] No private tokens found in buyer-facing package scan.
- [x] No keys found in buyer-facing package scan.
- [x] No private emails found in buyer-facing package scan.
- [x] No internal hostnames found in buyer-facing package scan.
- [x] No internal operational references required for buyer use.
- [x] Paths are portable and relative where buyer-facing docs require commands.
- [x] Documentation is understandable to external buyers.
- [x] Logs do not leak sensitive data by default.

## Compliance And Governance

- [x] OWASP LLM Top 10 mapping included in research/threat-landscape.md.
- [x] OWASP Agentic AI risk language included in product positioning and threat landscape.
- [x] NIST AI RMF reference included in research/threat-landscape.md.
- [x] Risk language avoids impossible "bulletproof" guarantees.
- [x] Human approval gates are described for high-risk actions.
- [x] Buyer-facing disclaimers are clear.

## Release Decision

Status: sell-ready as a Mythos-ready defensive MVP and commercial starter package.

Approved package scope: local scanner, policy file, JSON report, Markdown report, JSONL audit log, examples, Mythos-ready guide, research brief, product blueprint, buyer quickstart, sales copy, Gumroad listing copy, and release audit documentation.

Not included in this release: hosted dashboard, SaaS backend, browser extension, MCP middleware, enterprise SSO, managed monitoring, or automated remediation.
