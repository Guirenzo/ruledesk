SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    environment TEXT NOT NULL,
    affected_users INTEGER NOT NULL,
    sla_hours INTEGER NOT NULL,
    service_down INTEGER NOT NULL,
    no_workaround INTEGER NOT NULL,
    data_loss INTEGER NOT NULL,
    security_risk INTEGER NOT NULL,
    customer_impact INTEGER NOT NULL,
    recent_deploy INTEGER NOT NULL,
    recurring INTEGER NOT NULL,
    financial_impact INTEGER NOT NULL,
    reported_by TEXT NOT NULL,
    score INTEGER NOT NULL,
    priority_label TEXT NOT NULL,
    priority_level TEXT NOT NULL,
    response_time TEXT NOT NULL,
    owner TEXT NOT NULL,
    ticket_type TEXT NOT NULL,
    rules_fired TEXT NOT NULL,
    recommendations TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_incidents_created_at ON incidents(created_at);
CREATE INDEX IF NOT EXISTS idx_incidents_priority ON incidents(priority_level);
CREATE INDEX IF NOT EXISTS idx_incidents_category ON incidents(category);
"""
