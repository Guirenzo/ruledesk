from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = "RuleDesk API"
    host: str = os.getenv("RULEDESK_HOST", "127.0.0.1")
    port: int = int(os.getenv("RULEDESK_PORT", "8000"))
    base_dir: Path = Path(__file__).resolve().parents[2]
    cors_origin: str = os.getenv("RULEDESK_CORS_ORIGIN", "*")

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @property
    def database_path(self) -> Path:
        return Path(os.getenv("RULEDESK_DB_PATH", str(self.data_dir / "ruledesk.sqlite3")))


settings = Settings()
