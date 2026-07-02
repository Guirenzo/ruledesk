from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path


class RepositoryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.sqlite3"
        os.environ["RULEDESK_DB_PATH"] = str(self.db_path)

        from app.db.database import init_db

        init_db(self.db_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        os.environ.pop("RULEDESK_DB_PATH", None)

    def test_create_and_list_incident(self) -> None:
        from app.repositories.incidents import IncidentRepository
        from app.schemas.incidents import sample_incidents, validate_incident_payload
        from app.services.rule_engine import evaluate_incident

        incident, errors = validate_incident_payload(sample_incidents()[0])
        self.assertEqual(errors, [])

        repository = IncidentRepository()
        saved = repository.create(evaluate_incident(incident))
        items = repository.list()

        self.assertEqual(saved["id"], 1)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["priority_level"], "P1")


if __name__ == "__main__":
    unittest.main()
