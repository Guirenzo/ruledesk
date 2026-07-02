from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Any

from app.core.http import read_json, send_error, send_json
from app.repositories.incidents import IncidentRepository
from app.schemas.incidents import sample_incidents, validate_incident_payload
from app.services.analytics import build_stats
from app.services.rule_engine import evaluate_incident, knowledge_base


class ApiHandlers:
    def __init__(self, repository: IncidentRepository | None = None) -> None:
        self.repository = repository or IncidentRepository()

    def health(self, handler: BaseHTTPRequestHandler) -> None:
        send_json(handler, HTTPStatus.OK, {"status": "ok", "service": "ruledesk-api"})

    def rules(self, handler: BaseHTTPRequestHandler) -> None:
        send_json(handler, HTTPStatus.OK, {"rules": knowledge_base()})

    def evaluate(self, handler: BaseHTTPRequestHandler) -> None:
        try:
            payload = read_json(handler)
        except ValueError as exc:
            send_error(handler, HTTPStatus.BAD_REQUEST, str(exc))
            return

        incident, errors = validate_incident_payload(payload)
        if errors:
            send_error(handler, HTTPStatus.UNPROCESSABLE_ENTITY, "Dados invalidos.", errors)
            return

        evaluation = evaluate_incident(incident)
        saved = self.repository.create(evaluation)
        send_json(handler, HTTPStatus.CREATED, {"evaluation": evaluation, "saved": saved})

    def incidents(self, handler: BaseHTTPRequestHandler, query: dict[str, list[str]]) -> None:
        limit = parse_limit(query.get("limit", ["50"])[0])
        send_json(handler, HTTPStatus.OK, {"items": self.repository.list(limit=limit)})

    def incident_by_id(self, handler: BaseHTTPRequestHandler, incident_id: int) -> None:
        incident = self.repository.get(incident_id)
        if not incident:
            send_error(handler, HTTPStatus.NOT_FOUND, "Chamado nao encontrado.")
            return
        send_json(handler, HTTPStatus.OK, {"item": incident})

    def stats(self, handler: BaseHTTPRequestHandler) -> None:
        incidents = self.repository.list(limit=500)
        send_json(handler, HTTPStatus.OK, build_stats(incidents))

    def seed(self, handler: BaseHTTPRequestHandler) -> None:
        created: list[dict[str, Any]] = []
        for payload in sample_incidents():
            incident, errors = validate_incident_payload(payload)
            if errors:
                continue
            created.append(self.repository.create(evaluate_incident(incident)))
        send_json(handler, HTTPStatus.CREATED, {"created": created, "count": len(created)})


def parse_limit(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError:
        return 50
    return max(1, min(200, parsed))
