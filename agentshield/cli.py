from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .policy import load_rules
from .reporting import render_markdown_report
from .scanner import scan_text

DEFAULT_SUFFIXES = {
    ".txt",
    ".md",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".log",
    ".csv",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="agentshield",
        description="Scan prompts, documents, logs, and memory files for AI-agent security risk.",
    )
    parser.add_argument("target", help="Text file or directory to scan.")
    parser.add_argument("--audit-log", default="audit/agentshield-events.jsonl", help="Path for JSONL audit events.")
    parser.add_argument("--fail-on-risk", action="store_true", help="Return non-zero when any target is not allowed.")
    parser.add_argument("--max-bytes", type=int, default=1_000_000, help="Maximum bytes to read from each file.")
    parser.add_argument("--policy", help="Optional JSON policy file. Defaults to built-in rules.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    parser.add_argument("--report", help="Optional path to write a JSON report.")
    parser.add_argument("--markdown-report", help="Optional path to write a markdown report.")
    args = parser.parse_args()

    target = Path(args.target)
    rules = load_rules(Path(args.policy)) if args.policy else None
    events = [scan_path(path, args.max_bytes, rules=rules) for path in collect_targets(target)]

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": str(target),
        "decision": combine_decisions(item["decision"] for item in events),
        "risk_score": max((item["risk_score"] for item in events), default=0),
        "scanned_files": len(events),
        "summary": summarize_events(events),
        "results": events,
    }

    audit_path = Path(args.audit_log)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("a", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.markdown_report:
        markdown_path = Path(args.markdown_report)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_markdown_report(report), encoding="utf-8")

    indent = 2 if args.pretty else None
    print(json.dumps(report, indent=indent, sort_keys=True))
    risky = report["decision"] in {"block", "approval_required", "quarantine"}
    return 2 if args.fail_on_risk and risky else 0


def collect_targets(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if not target.is_dir():
        raise SystemExit(f"Target not found: {target}")

    paths = [
        path
        for path in target.rglob("*")
        if path.is_file() and path.suffix.lower() in DEFAULT_SUFFIXES and ".git" not in path.parts
    ]
    return sorted(paths)


def scan_path(path: Path, max_bytes: int, rules=None) -> dict[str, object]:
    raw = path.read_bytes()[:max_bytes]
    text = raw.decode("utf-8", errors="replace")
    result = scan_text(text, rules=rules) if rules is not None else scan_text(text)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": str(path),
        "bytes_scanned": len(raw),
        "risk_score": result.risk_score,
        "decision": result.decision,
        "summary": result.summary,
        "findings": [asdict(item) for item in result.findings],
    }


def combine_decisions(decisions) -> str:
    priority = {
        "allow": 0,
        "allow_with_warning": 1,
        "quarantine": 2,
        "approval_required": 3,
        "block": 4,
    }
    return max(decisions, key=lambda item: priority[item], default="allow")


def summarize_events(events: list[dict[str, object]]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for event in events:
        event_summary = event.get("summary", {})
        if not isinstance(event_summary, dict):
            continue
        for category, count in event_summary.items():
            summary[category] = summary.get(category, 0) + int(count)
    return dict(sorted(summary.items()))


if __name__ == "__main__":
    raise SystemExit(main())
