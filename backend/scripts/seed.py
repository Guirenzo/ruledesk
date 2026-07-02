from __future__ import annotations

from app.db.database import init_db
from app.repositories.incidents import IncidentRepository
from app.schemas.incidents import sample_incidents, validate_incident_payload
from app.services.rule_engine import evaluate_incident


def main() -> None:
    init_db()
    repository = IncidentRepository()
    created = []

    for payload in sample_incidents():
        incident, errors = validate_incident_payload(payload)
        if errors:
            raise SystemExit(f"Seed invalida: {errors}")
        created.append(repository.create(evaluate_incident(incident)))

    print(f"{len(created)} chamados de exemplo criados.")
    for item in created:
        print(f"#{item['id']} {item['priority_level']} - {item['title']}")


if __name__ == "__main__":
    main()
