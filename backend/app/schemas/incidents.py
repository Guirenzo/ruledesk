from __future__ import annotations

from typing import Any


CATEGORIES = {
    "application",
    "database",
    "network",
    "security",
    "access",
    "infrastructure",
}

ENVIRONMENTS = {
    "production",
    "homologation",
    "development",
}

BOOLEAN_FIELDS = {
    "service_down",
    "no_workaround",
    "data_loss",
    "security_risk",
    "customer_impact",
    "recent_deploy",
    "recurring",
    "financial_impact",
}


def validate_incident_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []

    title = str(payload.get("title") or "").strip()
    if len(title) < 5:
        errors.append("title deve ter pelo menos 5 caracteres.")
    if len(title) > 140:
        errors.append("title deve ter no maximo 140 caracteres.")

    category = str(payload.get("category") or "application").strip()
    if category not in CATEGORIES:
        errors.append(f"category invalida. Use uma destas: {', '.join(sorted(CATEGORIES))}.")

    environment = str(payload.get("environment") or "production").strip()
    if environment not in ENVIRONMENTS:
        errors.append(f"environment invalido. Use uma destas: {', '.join(sorted(ENVIRONMENTS))}.")

    affected_users = to_int(payload.get("affected_users"), fallback=1)
    if not 1 <= affected_users <= 5000:
        errors.append("affected_users deve estar entre 1 e 5000.")

    sla_hours = to_int(payload.get("sla_hours"), fallback=24)
    if not 1 <= sla_hours <= 168:
        errors.append("sla_hours deve estar entre 1 e 168.")

    sanitized: dict[str, Any] = {
        "title": title,
        "category": category,
        "environment": environment,
        "affected_users": affected_users,
        "sla_hours": sla_hours,
        "reported_by": str(payload.get("reported_by") or "Equipe de suporte").strip()[:80],
    }

    for field in BOOLEAN_FIELDS:
        sanitized[field] = to_bool(payload.get(field))

    return sanitized, errors


def to_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "sim", "s"}
    return bool(value)


def sample_incidents() -> list[dict[str, Any]]:
    return [
        {
            "title": "Checkout indisponível em produção",
            "category": "application",
            "environment": "production",
            "affected_users": 320,
            "sla_hours": 1,
            "service_down": True,
            "no_workaround": True,
            "data_loss": False,
            "security_risk": False,
            "customer_impact": True,
            "recent_deploy": True,
            "recurring": False,
            "financial_impact": True,
            "reported_by": "Monitoramento",
        },
        {
            "title": "Possível vazamento de dados de clientes",
            "category": "security",
            "environment": "production",
            "affected_users": 180,
            "sla_hours": 1,
            "service_down": False,
            "no_workaround": True,
            "data_loss": True,
            "security_risk": True,
            "customer_impact": True,
            "recent_deploy": False,
            "recurring": False,
            "financial_impact": True,
            "reported_by": "Segurança",
        },
        {
            "title": "Erro visual em tela interna com contorno",
            "category": "application",
            "environment": "development",
            "affected_users": 4,
            "sla_hours": 72,
            "service_down": False,
            "no_workaround": False,
            "data_loss": False,
            "security_risk": False,
            "customer_impact": False,
            "recent_deploy": False,
            "recurring": False,
            "financial_impact": False,
            "reported_by": "QA",
        },
    ]
