from __future__ import annotations


def render_markdown_report(report: dict[str, object]) -> str:
    lines = [
        "# AgentShield Security Report",
        "",
        f"Target: `{report.get('target', '')}`",
        f"Decision: `{report.get('decision', '')}`",
        f"Risk score: `{report.get('risk_score', 0)}`",
        f"Scanned files: `{report.get('scanned_files', 0)}`",
        "",
        "## Summary",
        "",
    ]

    summary = report.get("summary", {})
    if isinstance(summary, dict) and summary:
        for category, count in sorted(summary.items()):
            lines.append(f"- `{category}`: {count}")
    else:
        lines.append("- No risks detected.")

    lines.extend(["", "## Findings", ""])
    results = report.get("results", [])
    if not isinstance(results, list) or not results:
        lines.append("No scanned files.")
        return "\n".join(lines) + "\n"

    for result in results:
        if not isinstance(result, dict):
            continue
        lines.append(f"### {result.get('target', '')}")
        lines.append("")
        lines.append(f"- Decision: `{result.get('decision', '')}`")
        lines.append(f"- Risk score: `{result.get('risk_score', 0)}`")
        findings = result.get("findings", [])
        if not isinstance(findings, list) or not findings:
            lines.append("- Findings: none")
            lines.append("")
            continue
        for finding in findings:
            if not isinstance(finding, dict):
                continue
            lines.append(
                f"- `{finding.get('rule_id', '')}` `{finding.get('severity', '')}` "
                f"`{finding.get('category', '')}`: {finding.get('description', '')}"
            )
            evidence = str(finding.get("evidence", "")).replace("\n", " ")
            if evidence:
                lines.append(f"  Evidence: `{evidence}`")
            impact = str(finding.get("impact", "")).strip()
            if impact:
                lines.append(f"  Impact: {impact}")
            recommendation = str(finding.get("recommendation", "")).strip()
            if recommendation:
                lines.append(f"  Recommended fix: {recommendation}")
        lines.append("")

    return "\n".join(lines) + "\n"
