from __future__ import annotations

import json
import re
from pathlib import Path

from .scanner import Rule


def load_rules(path: Path) -> tuple[Rule, ...]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    rules = raw.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("Policy file must contain a 'rules' list.")

    loaded: list[Rule] = []
    for item in rules:
        loaded.append(
            Rule(
                rule_id=require_string(item, "rule_id"),
                category=require_string(item, "category"),
                severity=require_string(item, "severity"),
                decision=require_string(item, "decision"),
                pattern=re.compile(require_string(item, "pattern"), re.I | re.S),
                description=require_string(item, "description"),
                impact=optional_string(
                    item,
                    "impact",
                    "Matched a custom policy rule that may affect agent security.",
                ),
                recommendation=optional_string(
                    item,
                    "recommendation",
                    "Review the matched content against the organization's AI-agent policy.",
                ),
            )
        )
    return tuple(loaded)


def require_string(item: object, key: str) -> str:
    if not isinstance(item, dict):
        raise ValueError("Each policy rule must be an object.")
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Policy rule field '{key}' must be a non-empty string.")
    return value


def optional_string(item: object, key: str, default: str) -> str:
    if not isinstance(item, dict):
        raise ValueError("Each policy rule must be an object.")
    value = item.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Policy rule field '{key}' must be a non-empty string when provided.")
    return value
