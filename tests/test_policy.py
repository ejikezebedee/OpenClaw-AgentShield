import tempfile
import unittest
from pathlib import Path

from agentshield.policy import load_rules
from agentshield.scanner import scan_text


class PolicyTests(unittest.TestCase):
    def test_load_rules_from_json_policy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            policy = Path(temp_dir) / "policy.json"
            policy.write_text(
                """
                {
                  "rules": [
                    {
                      "rule_id": "CUSTOM-001",
                      "category": "custom_risk",
                      "severity": "medium",
                      "decision": "approval_required",
                      "pattern": "custom risky phrase",
                      "description": "Custom policy matched."
                    }
                  ]
                }
                """,
                encoding="utf-8",
            )

            rules = load_rules(policy)
            result = scan_text("This includes a custom risky phrase.", rules=rules)

            self.assertEqual(result.decision, "approval_required")
            self.assertEqual(result.summary["custom_risk"], 1)


if __name__ == "__main__":
    unittest.main()

