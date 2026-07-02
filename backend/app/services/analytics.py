from __future__ import annotations

from collections import Counter
from typing import Any


def build_stats(incidents: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(incidents)
    priorities = Counter(item["priority_level"] for item in incidents)
    categories = Counter(item["category"] for item in incidents)
    rules = Counter(
        rule["code"]
        for item in incidents
        for rule in item.get("rules_fired", [])
    )
    avg_score = round(sum(item["score"] for item in incidents) / total, 1) if total else 0

    return {
        "total": total,
        "average_score": avg_score,
        "by_priority": dict(sorted(priorities.items())),
        "by_category": dict(sorted(categories.items())),
        "top_rules": [{"code": code, "count": count} for code, count in rules.most_common(8)],
        "latest": incidents[0] if incidents else None,
    }
