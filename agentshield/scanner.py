from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    rule_id: str
    category: str
    severity: str
    decision: str
    pattern: re.Pattern[str]
    description: str
    impact: str
    recommendation: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    category: str
    severity: str
    decision: str
    description: str
    impact: str
    recommendation: str
    evidence: str


@dataclass(frozen=True)
class ScanResult:
    risk_score: int
    decision: str
    findings: list[Finding]
    summary: dict[str, int]


RULES: tuple[Rule, ...] = (
    Rule(
        "AS-PI-001",
        "prompt_injection",
        "high",
        "quarantine",
        re.compile(r"\b(ignore|override|disregard)\b.{0,80}\b(previous|prior|system|developer)\b.{0,80}\b(instruction|message|rule|policy)s?\b", re.I | re.S),
        "Attempts to override higher-priority instructions.",
        "A compromised context may cause the agent to ignore trusted instructions or policy.",
        "Quarantine the content, keep it outside privileged context, and review the source before ingestion.",
    ),
    Rule(
        "AS-PI-002",
        "system_prompt_extraction",
        "high",
        "block",
        re.compile(r"\b(reveal|print|show|dump|export)\b.{0,80}\b(system prompt|developer message|hidden instruction|internal instruction)s?\b", re.I | re.S),
        "Attempts to extract privileged prompts or hidden instructions.",
        "Disclosure of hidden instructions can expose internal controls and make later bypass attempts easier.",
        "Block the request and avoid returning hidden prompts, policies, chain-of-thought, or internal tool instructions.",
    ),
    Rule(
        "AS-DE-001",
        "data_exfiltration",
        "critical",
        "block",
        re.compile(r"\b(send|upload|post|exfiltrate|forward)\b.{0,120}\b(secret|token|api key|private key|credential|password|customer data|internal file)s?\b", re.I | re.S),
        "Attempts to move protected data outside the trusted boundary.",
        "Sensitive data, credentials, or customer records may be exposed to an untrusted destination.",
        "Block the action, verify destination trust, and ensure secrets are never available in agent context.",
    ),
    Rule(
        "AS-TG-001",
        "destructive_tool_intent",
        "critical",
        "approval_required",
        re.compile(r"\b(delete|wipe|destroy|remove|drop|overwrite)\b.{0,120}\b(database|repo|repository|file|folder|bucket|account|record)s?\b", re.I | re.S),
        "Requests a destructive action that requires approval.",
        "The agent may destroy or corrupt business data, source code, customer records, or infrastructure state.",
        "Require explicit human approval, backup verification, and least-privilege execution before proceeding.",
    ),
    Rule(
        "AS-MG-001",
        "memory_poisoning",
        "high",
        "quarantine",
        re.compile(r"\b(remember|store|save to memory|from now on)\b.{0,120}\b(always|never|ignore|bypass|do not ask|without approval)\b", re.I | re.S),
        "Attempts to persist behavior-changing instructions into memory.",
        "Persistent memory can carry attacker instructions into future sessions after the original context is gone.",
        "Quarantine the memory write and require review before saving durable agent memory.",
    ),
    Rule(
        "AS-AG-001",
        "agent_laundering",
        "high",
        "approval_required",
        re.compile(r"\b(tell|instruct|delegate to|ask)\b.{0,80}\b(admin agent|higher privilege|privileged agent|another agent)\b.{0,120}\b(run|send|approve|export|delete)\b", re.I | re.S),
        "Possible agent-to-agent instruction laundering or privilege escalation.",
        "A lower-trust agent may indirectly command a more privileged agent to perform restricted actions.",
        "Require cross-agent trust boundaries, signed delegation rules, and human approval for privileged actions.",
    ),
    Rule(
        "AS-MY-001",
        "mythos_autonomy_risk",
        "critical",
        "approval_required",
        re.compile(r"\b(autonomous|without supervision|no human approval|auto.?approve|self.?execute)\b.{0,160}\b(shell|browser|network|api|credential|filesystem|database|deployment|production)\b", re.I | re.S),
        "High-autonomy agent request touching privileged tools or sensitive environments.",
        "A highly capable agent can chain small permissions into large operational impact without further review.",
        "Deny autonomous execution until sandboxing, network egress controls, workspace boundaries, and approval gates are verified.",
    ),
    Rule(
        "AS-MCP-001",
        "mcp_tool_manifest_risk",
        "high",
        "approval_required",
        re.compile(r"\b(mcp|model context protocol|tool manifest|connector|plugin)\b.{0,200}\b(shell|filesystem|network|secrets|credentials|browser|email|github|database|payments?)\b", re.I | re.S),
        "MCP/tool manifest exposes sensitive or high-impact capabilities.",
        "A poisoned or over-permissive connector can convert untrusted text into unauthorized tool use.",
        "Review connector permissions, remove unnecessary scopes, and require trust verification before enabling the tool.",
    ),
    Rule(
        "AS-EG-001",
        "egress_control_gap",
        "high",
        "approval_required",
        re.compile(r"\b(network|internet|egress|webhook|external url|remote server|public endpoint)\b.{0,180}\b(allow all|unrestricted|no approval|default allow|wildcard)\b", re.I | re.S),
        "Network or egress policy appears overly permissive.",
        "Unrestricted outbound access can let a compromised agent leak data or call attacker-controlled services.",
        "Use network deny-by-default, destination allowlists, and separate approval for external requests.",
    ),
    Rule(
        "AS-AF-001",
        "approval_fatigue_risk",
        "medium",
        "approval_required",
        re.compile(r"\b(always approve|approve all|remember my approval|do not ask again|skip confirmation|reduce prompts)\b", re.I | re.S),
        "Request may weaken human approval gates or create approval fatigue.",
        "Repeated or blanket approvals reduce meaningful supervision and can normalize unsafe actions.",
        "Keep fail-closed defaults, batch low-risk approvals carefully, and require fresh approval for high-impact tools.",
    ),
    Rule(
        "AS-BN-001",
        "benign_security_discussion",
        "info",
        "allow",
        re.compile(r"\b(defensive|audit|mitigation|hardening|security report|risk assessment|policy)\b", re.I),
        "Benign defensive security context.",
        "No direct harmful action detected in this defensive context.",
        "Allow, while still applying normal review if the content later requests privileged tool use.",
    ),
)


SEVERITY_SCORE = {
    "info": 0,
    "low": 15,
    "medium": 35,
    "high": 70,
    "critical": 95,
}

DECISION_PRIORITY = {
    "allow": 0,
    "allow_with_warning": 1,
    "quarantine": 2,
    "approval_required": 3,
    "block": 4,
}


def scan_text(text: str, rules: Iterable[Rule] = RULES) -> ScanResult:
    findings: list[Finding] = []

    for rule in rules:
        match = rule.pattern.search(text)
        if not match:
            continue
        evidence = normalize_evidence(match.group(0))
        findings.append(
            Finding(
                rule_id=rule.rule_id,
                category=rule.category,
                severity=rule.severity,
                decision=rule.decision,
                description=rule.description,
                impact=rule.impact,
                recommendation=rule.recommendation,
                evidence=evidence,
            )
        )

    if not findings:
        return ScanResult(risk_score=0, decision="allow", findings=[], summary={})

    risk_score = max(SEVERITY_SCORE[item.severity] for item in findings)
    decision = max(findings, key=lambda item: DECISION_PRIORITY[item.decision]).decision

    return ScanResult(
        risk_score=risk_score,
        decision=decision,
        findings=findings,
        summary=summarize_findings(findings),
    )


def summarize_findings(findings: Iterable[Finding]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for finding in findings:
        summary[finding.category] = summary.get(finding.category, 0) + 1
    return dict(sorted(summary.items()))


def normalize_evidence(value: str, limit: int = 180) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
