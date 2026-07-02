from __future__ import annotations

import unittest

from app.schemas.incidents import sample_incidents, validate_incident_payload
from app.services.rule_engine import evaluate_incident


class RuleEngineTestCase(unittest.TestCase):
    def test_critical_outage_reaches_p1(self) -> None:
        incident, errors = validate_incident_payload(sample_incidents()[0])

        self.assertEqual(errors, [])
        result = evaluate_incident(incident)

        self.assertEqual(result["priority"]["level"], "P1")
        self.assertGreaterEqual(result["score"], 85)
        self.assertIn("R02", {rule["code"] for rule in result["rules_fired"]})

    def test_minor_issue_stays_low_priority(self) -> None:
        incident, errors = validate_incident_payload(sample_incidents()[2])

        self.assertEqual(errors, [])
        result = evaluate_incident(incident)

        self.assertEqual(result["priority"]["level"], "P4")
        self.assertLess(result["score"], 35)
        self.assertIn("R16", {rule["code"] for rule in result["rules_fired"]})

    def test_invalid_title_is_rejected(self) -> None:
        _, errors = validate_incident_payload({"title": "abc"})

        self.assertTrue(errors)
        self.assertIn("title", errors[0])


if __name__ == "__main__":
    unittest.main()
