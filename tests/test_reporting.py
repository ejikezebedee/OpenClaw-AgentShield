import unittest

from agentshield.reporting import render_markdown_report


class ReportingTests(unittest.TestCase):
    def test_render_markdown_report_includes_summary_and_findings(self):
        report = {
            "target": "examples",
            "decision": "block",
            "risk_score": 95,
            "scanned_files": 1,
            "summary": {"data_exfiltration": 1},
            "results": [
                {
                    "target": "examples/risky.txt",
                    "decision": "block",
                    "risk_score": 95,
                    "findings": [
                        {
                            "rule_id": "AS-DE-001",
                            "severity": "critical",
                            "category": "data_exfiltration",
                            "description": "Blocked data movement.",
                            "impact": "Sensitive data may leave the trust boundary.",
                            "recommendation": "Block the action and verify destination trust.",
                            "evidence": "Send customer data",
                        }
                    ],
                }
            ],
        }

        markdown = render_markdown_report(report)

        self.assertIn("# AgentShield Security Report", markdown)
        self.assertIn("`data_exfiltration`: 1", markdown)
        self.assertIn("AS-DE-001", markdown)
        self.assertIn("Impact:", markdown)
        self.assertIn("Recommended fix:", markdown)


if __name__ == "__main__":
    unittest.main()
