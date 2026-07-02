from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from app.api.handlers import ApiHandlers
from app.core.http import send_empty, send_error
from app.repositories.incidents import IncidentRepository


def route_request(handler: BaseHTTPRequestHandler) -> None:
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip("/") or "/"
    query = parse_qs(parsed.query)
    method = handler.command.upper()
    api = ApiHandlers(IncidentRepository())

    if method == "OPTIONS":
        send_empty(handler)
        return

    if method == "GET" and path == "/health":
        api.health(handler)
        return

    if method == "GET" and path == "/api/rules":
        api.rules(handler)
        return

    if method == "GET" and path == "/api/incidents":
        api.incidents(handler, query)
        return

    if method == "GET" and path.startswith("/api/incidents/"):
        incident_id = parse_id(path.removeprefix("/api/incidents/"))
        if incident_id is None:
            send_error(handler, HTTPStatus.BAD_REQUEST, "ID de chamado invalido.")
            return
        api.incident_by_id(handler, incident_id)
        return

    if method == "GET" and path == "/api/stats":
        api.stats(handler)
        return

    if method == "POST" and path in {"/api/incidents", "/api/incidents/evaluate"}:
        api.evaluate(handler)
        return

    if method == "POST" and path == "/api/seed":
        api.seed(handler)
        return

    send_error(handler, HTTPStatus.NOT_FOUND, f"Rota nao encontrada: {method} {path}")


def parse_id(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
