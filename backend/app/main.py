from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from app.api.router import route_request
from app.core.config import settings
from app.core.http import send_error
from app.db.database import init_db


class RuleDeskRequestHandler(BaseHTTPRequestHandler):
    server_version = "RuleDeskAPI/1.0"

    def do_OPTIONS(self) -> None:
        route_request(self)

    def do_GET(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._handle()

    def _handle(self) -> None:
        try:
            route_request(self)
        except Exception as exc:  # pragma: no cover - defensive boundary for demo server.
            send_error(self, 500, "Erro interno da API.", {"type": type(exc).__name__, "detail": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        print(f"[api] {self.address_string()} - {format % args}")


def run() -> None:
    init_db()
    server = ThreadingHTTPServer((settings.host, settings.port), RuleDeskRequestHandler)
    print(f"RuleDesk API rodando em http://{settings.host}:{settings.port}")
    print("Rotas: /health, /api/rules, /api/incidents, /api/stats")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando RuleDesk API...")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
