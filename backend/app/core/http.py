from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Any

from app.core.config import settings


def send_json(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any] | list[Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", settings.cors_origin)
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(body)


def send_empty(handler: BaseHTTPRequestHandler, status: int = HTTPStatus.NO_CONTENT) -> None:
    handler.send_response(status)
    handler.send_header("Access-Control-Allow-Origin", settings.cors_origin)
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()


def send_error(handler: BaseHTTPRequestHandler, status: int, message: str, details: Any = None) -> None:
    payload: dict[str, Any] = {
        "error": HTTPStatus(status).phrase,
        "message": message,
    }
    if details is not None:
        payload["details"] = details
    send_json(handler, status, payload)


def read_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}

    raw_body = handler.rfile.read(length)
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("JSON invalido no corpo da requisicao.") from exc

    if not isinstance(payload, dict):
        raise ValueError("O corpo da requisicao deve ser um objeto JSON.")
    return payload
