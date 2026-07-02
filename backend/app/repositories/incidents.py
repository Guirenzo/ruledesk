from __future__ import annotations

import json
from typing import Any

from app.db.database import session


BOOL_FIELDS = {
    "service_down",
    "no_workaround",
    "data_loss",
    "security_risk",
    "customer_impact",
    "recent_deploy",
    "recurring",
    "financial_impact",
}


class IncidentRepository:
    def create(self, evaluation: dict[str, Any]) -> dict[str, Any]:
        incident = evaluation["incident"]
        priority = evaluation["priority"]

        with session() as connection:
            cursor = connection.execute(
                """
                INSERT INTO incidents (
                    title, category, environment, affected_users, sla_hours,
                    service_down, no_workaround, data_loss, security_risk,
                    customer_impact, recent_deploy, recurring, financial_impact,
                    reported_by, score, priority_label, priority_level, response_time,
                    owner, ticket_type, rules_fired, recommendations, created_at
                )
                VALUES (
                    :title, :category, :environment, :affected_users, :sla_hours,
                    :service_down, :no_workaround, :data_loss, :security_risk,
                    :customer_impact, :recent_deploy, :recurring, :financial_impact,
                    :reported_by, :score, :priority_label, :priority_level, :response_time,
                    :owner, :ticket_type, :rules_fired, :recommendations, :created_at
                )
                """,
                {
                    **incident,
                    "service_down": int(incident["service_down"]),
                    "no_workaround": int(incident["no_workaround"]),
                    "data_loss": int(incident["data_loss"]),
                    "security_risk": int(incident["security_risk"]),
                    "customer_impact": int(incident["customer_impact"]),
                    "recent_deploy": int(incident["recent_deploy"]),
                    "recurring": int(incident["recurring"]),
                    "financial_impact": int(incident["financial_impact"]),
                    "score": evaluation["score"],
                    "priority_label": priority["label"],
                    "priority_level": priority["level"],
                    "response_time": priority["response_time"],
                    "owner": priority["owner"],
                    "ticket_type": priority["ticket_type"],
                    "rules_fired": json.dumps(evaluation["rules_fired"], ensure_ascii=False),
                    "recommendations": json.dumps(evaluation["recommendations"], ensure_ascii=False),
                    "created_at": evaluation["evaluated_at"],
                },
            )
            row = connection.execute(
                "SELECT * FROM incidents WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            return row_to_dict(row) if row else {}

    def list(self, limit: int = 50) -> list[dict[str, Any]]:
        with session() as connection:
            rows = connection.execute(
                """
                SELECT * FROM incidents
                ORDER BY datetime(created_at) DESC, id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [row_to_dict(row) for row in rows]

    def get(self, incident_id: int) -> dict[str, Any] | None:
        with session() as connection:
            row = connection.execute(
                "SELECT * FROM incidents WHERE id = ?",
                (incident_id,),
            ).fetchone()
        return row_to_dict(row) if row else None

    def clear(self) -> None:
        with session() as connection:
            connection.execute("DELETE FROM incidents")


def row_to_dict(row: Any) -> dict[str, Any]:
    item = dict(row)
    for field in BOOL_FIELDS:
        item[field] = bool(item[field])
    item["rules_fired"] = json.loads(item["rules_fired"])
    item["recommendations"] = json.loads(item["recommendations"])
    return item
