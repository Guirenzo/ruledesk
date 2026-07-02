from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

BASE_SCORE = 10


@dataclass(frozen=True)
class RuleHit:
    code: str
    title: str
    weight: int
    explanation: str
    recommendation: str | None = None


@dataclass(frozen=True)
class Priority:
    label: str
    level: str
    response_time: str
    owner: str
    ticket_type: str
    color: str


CATEGORY_LABELS = {
    "application": "Aplicação",
    "database": "Banco de dados",
    "network": "Rede",
    "security": "Segurança",
    "access": "Acesso",
    "infrastructure": "Infraestrutura",
}


def evaluate_incident(incident: dict[str, Any]) -> dict[str, Any]:
    hits: list[RuleHit] = []
    base_score = BASE_SCORE

    def fire(
        condition: bool,
        code: str,
        title: str,
        weight: int,
        explanation: str,
        recommendation: str | None = None,
    ) -> None:
        if condition:
            hits.append(RuleHit(code, title, weight, explanation, recommendation))

    fire(
        incident["environment"] == "production",
        "R01",
        "Ambiente produtivo",
        12,
        "Falhas em produção podem afetar usuários reais e contratos de atendimento.",
        "Manter comunicação ativa com suporte, produto e responsável técnico.",
    )
    fire(
        incident["service_down"],
        "R02",
        "Serviço indisponível",
        35,
        "Indisponibilidade é um dos sinais mais fortes de incidente crítico.",
        "Verificar monitoramento, logs do serviço e dependências externas.",
    )
    fire(
        incident["data_loss"],
        "R03",
        "Perda de dados",
        32,
        "Perda ou corrupção de dados aumenta risco operacional e jurídico.",
        "Preservar evidências, congelar alterações sensíveis e validar backups.",
    )
    fire(
        incident["security_risk"] or incident["category"] == "security",
        "R04",
        "Risco de segurança",
        35,
        "Incidentes de segurança exigem contenção antes de simples correção.",
        "Acionar responsável de segurança, isolar vetor e registrar evidências.",
    )
    fire(
        incident["affected_users"] >= 250,
        "R05",
        "Impacto massivo",
        24,
        "Mais de 250 usuários afetados indica impacto amplo no negócio.",
        "Priorizar comunicação e dividir investigação entre causa e mitigação.",
    )
    fire(
        50 <= incident["affected_users"] < 250,
        "R06",
        "Impacto relevante",
        14,
        "O volume de usuários afetados justifica atendimento acelerado.",
        "Agrupar chamados duplicados e atualizar status em lote.",
    )
    fire(
        incident["no_workaround"],
        "R07",
        "Sem contorno",
        15,
        "Sem alternativa de uso, o usuário permanece bloqueado.",
        "Buscar mitigação temporária enquanto a causa raiz é investigada.",
    )
    fire(
        incident["customer_impact"],
        "R08",
        "Impacto em cliente",
        16,
        "Afetar cliente externo aumenta urgência, reputação e custo de espera.",
        "Comunicar área de relacionamento e preparar mensagem de status.",
    )
    fire(
        incident["financial_impact"],
        "R09",
        "Impacto financeiro",
        16,
        "Sinais de perda financeira elevam a prioridade de resposta.",
        "Estimar perda por hora e envolver liderança de produto/operação.",
    )
    fire(
        incident["sla_hours"] <= 1,
        "R10",
        "SLA imediato",
        12,
        "SLA menor ou igual a uma hora reduz a janela de análise.",
        "Trabalhar primeiro em mitigação, depois em causa raiz.",
    )
    fire(
        1 < incident["sla_hours"] <= 4,
        "R11",
        "SLA curto",
        8,
        "SLA curto exige acompanhamento frequente do atendimento.",
        "Definir próximo checkpoint em até 30 minutos.",
    )
    fire(
        incident["recent_deploy"],
        "R12",
        "Falha após deploy",
        8,
        "Mudança recente é uma hipótese forte para regressão.",
        "Comparar versões, revisar pipeline e preparar rollback controlado.",
    )
    fire(
        incident["recurring"],
        "R13",
        "Incidente recorrente",
        8,
        "Recorrência indica que a causa raiz provavelmente ainda existe.",
        "Abrir item de problema para análise pós-incidente.",
    )
    fire(
        incident["category"] == "database",
        "R14",
        "Componente central",
        8,
        "Falhas em banco de dados podem se propagar para várias aplicações.",
        "Checar conexões, locks, queries lentas, disco e replicação.",
    )
    fire(
        incident["category"] == "network",
        "R15",
        "Dependência de rede",
        7,
        "Problemas de rede costumam afetar múltiplos serviços ao mesmo tempo.",
        "Validar DNS, latência, rotas, firewall e conectividade entre serviços.",
    )
    fire(
        not incident["no_workaround"]
        and not incident["service_down"]
        and not incident["data_loss"]
        and not incident["security_risk"],
        "R16",
        "Há contorno operacional",
        -8,
        "A existência de alternativa reduz a urgência imediata.",
        "Registrar contorno no chamado e seguir fluxo normal de correção.",
    )

    raw_score = base_score + sum(hit.weight for hit in hits)
    score = max(0, min(100, raw_score))
    priority = classify(score)

    return {
        "incident": incident,
        "base_score": base_score,
        "raw_score": raw_score,
        "score": score,
        "priority": priority.__dict__,
        "rules_fired": [hit.__dict__ for hit in hits],
        "recommendations": ordered_recommendations(priority, hits),
        "category_label": CATEGORY_LABELS.get(incident["category"], incident["category"]),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }


def classify(score: int) -> Priority:
    if score >= 85:
        return Priority(
            label="Crítica",
            level="P1",
            response_time="15 minutos",
            owner="Líder técnico + suporte N2",
            ticket_type="Incidente maior",
            color="#e11d48",
        )
    if score >= 60:
        return Priority(
            label="Alta",
            level="P2",
            response_time="1 hora",
            owner="Suporte N2",
            ticket_type="Incidente",
            color="#ea580c",
        )
    if score >= 35:
        return Priority(
            label="Média",
            level="P3",
            response_time="4 horas",
            owner="Suporte N1/N2",
            ticket_type="Incidente comum",
            color="#2563eb",
        )
    return Priority(
        label="Baixa",
        level="P4",
        response_time="1 dia útil",
        owner="Backlog de suporte",
        ticket_type="Solicitação ou melhoria",
        color="#059669",
    )


def ordered_recommendations(priority: Priority, hits: list[RuleHit]) -> list[str]:
    items: list[str] = []
    if priority.level == "P1":
        items.append("Abrir sala de crise, registrar linha do tempo e nomear responsável pela comunicação.")

    for hit in hits:
        if hit.recommendation and hit.recommendation not in items:
            items.append(hit.recommendation)

    items.append("Atualizar o chamado com prioridade, regras disparadas, responsável e próximo checkpoint.")
    return items[:7]


def priority_bands() -> list[dict[str, Any]]:
    """Faixas de classificação do score. Usado pela interface para explicar o corte."""
    return [
        {"level": "P4", "label": "Baixa", "min": 0, "max": 34, "color": "#059669"},
        {"level": "P3", "label": "Média", "min": 35, "max": 59, "color": "#2563eb"},
        {"level": "P2", "label": "Alta", "min": 60, "max": 84, "color": "#ea580c"},
        {"level": "P1", "label": "Crítica", "min": 85, "max": 100, "color": "#e11d48"},
    ]


def knowledge_base() -> list[dict[str, Any]]:
    return [
        {"code": "R01", "group": "Ambiente", "if": "ambiente = produção", "then": "aumentar criticidade", "weight": 12},
        {"code": "R02", "group": "Impacto", "if": "serviço indisponível", "then": "candidato forte a P1", "weight": 35},
        {"code": "R03", "group": "Dados", "if": "perda de dados", "then": "escalar e preservar evidências", "weight": 32},
        {"code": "R04", "group": "Segurança", "if": "risco de segurança", "then": "acionar resposta a incidente", "weight": 35},
        {"code": "R05", "group": "Impacto", "if": "usuários afetados ≥ 250", "then": "elevar por impacto massivo", "weight": 24},
        {"code": "R06", "group": "Impacto", "if": "usuários afetados entre 50 e 249", "then": "elevar por impacto relevante", "weight": 14},
        {"code": "R07", "group": "Operação", "if": "sem contorno", "then": "reduzir tolerância de espera", "weight": 15},
        {"code": "R08", "group": "Negócio", "if": "impacta cliente externo", "then": "elevar urgência", "weight": 16},
        {"code": "R09", "group": "Negócio", "if": "impacto financeiro", "then": "elevar prioridade de resposta", "weight": 16},
        {"code": "R10", "group": "SLA", "if": "SLA ≤ 1 hora", "then": "priorizar mitigação imediata", "weight": 12},
        {"code": "R11", "group": "SLA", "if": "SLA entre 1 e 4 horas", "then": "acompanhar com checkpoints", "weight": 8},
        {"code": "R12", "group": "Mudança", "if": "falha após deploy", "then": "sugerir rollback ou análise", "weight": 8},
        {"code": "R13", "group": "Operação", "if": "incidente recorrente", "then": "abrir análise de causa raiz", "weight": 8},
        {"code": "R14", "group": "Infra", "if": "categoria = banco de dados", "then": "tratar como componente central", "weight": 8},
        {"code": "R15", "group": "Infra", "if": "categoria = rede", "then": "verificar dependências de rede", "weight": 7},
        {"code": "R16", "group": "Atenuante", "if": "existe contorno e sem sinais críticos", "then": "reduzir prioridade", "weight": -8},
    ]
