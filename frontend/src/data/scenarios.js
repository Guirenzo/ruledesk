export const defaultIncident = {
  title: "Checkout com falha intermitente em produção",
  category: "application",
  environment: "production",
  affected_users: 86,
  sla_hours: 2,
  service_down: false,
  no_workaround: true,
  data_loss: false,
  security_risk: false,
  customer_impact: true,
  recent_deploy: true,
  recurring: false,
  financial_impact: true,
  reported_by: "Suporte N1"
};

export const scenarios = {
  outage: {
    name: "Queda em produção",
    tone: "critical",
    summary: "Checkout fora do ar para todos os clientes.",
    expected: "Tende a P1 (crítica)",
    payload: {
      title: "Checkout indisponível para todos os clientes",
      category: "application",
      environment: "production",
      affected_users: 320,
      sla_hours: 1,
      service_down: true,
      no_workaround: true,
      data_loss: false,
      security_risk: false,
      customer_impact: true,
      recent_deploy: true,
      recurring: false,
      financial_impact: true,
      reported_by: "Monitoramento"
    }
  },
  security: {
    name: "Incidente de segurança",
    tone: "critical",
    summary: "Suspeita de vazamento de dados de clientes.",
    expected: "Tende a P1 (crítica)",
    payload: {
      title: "Possível vazamento de dados de clientes",
      category: "security",
      environment: "production",
      affected_users: 180,
      sla_hours: 1,
      service_down: false,
      no_workaround: true,
      data_loss: true,
      security_risk: true,
      customer_impact: true,
      recent_deploy: false,
      recurring: false,
      financial_impact: true,
      reported_by: "Segurança"
    }
  },
  database: {
    name: "Banco lento",
    tone: "high",
    summary: "Locks no banco degradando pedidos.",
    expected: "Tende a P2/P3",
    payload: {
      title: "Banco de dados com locks em pedidos",
      category: "database",
      environment: "production",
      affected_users: 70,
      sla_hours: 4,
      service_down: false,
      no_workaround: true,
      data_loss: false,
      security_risk: false,
      customer_impact: true,
      recent_deploy: false,
      recurring: true,
      financial_impact: false,
      reported_by: "DBA"
    }
  },
  minor: {
    name: "Bug controlado",
    tone: "low",
    summary: "Erro visual interno, com contorno disponível.",
    expected: "Tende a P4 (baixa)",
    payload: {
      title: "Erro visual em tela interna com contorno",
      category: "application",
      environment: "development",
      affected_users: 4,
      sla_hours: 72,
      service_down: false,
      no_workaround: false,
      data_loss: false,
      security_risk: false,
      customer_impact: false,
      recent_deploy: false,
      recurring: false,
      financial_impact: false,
      reported_by: "QA"
    }
  }
};

export const categories = [
  ["application", "Aplicação"],
  ["database", "Banco de dados"],
  ["network", "Rede"],
  ["security", "Segurança"],
  ["access", "Acesso"],
  ["infrastructure", "Infraestrutura"]
];

export const environments = [
  ["production", "Produção"],
  ["homologation", "Homologação"],
  ["development", "Desenvolvimento"]
];

// Rótulos e descrições curtas dos fatos booleanos, usados no formulário e nos "chips" de fatos.
export const booleanFields = [
  ["service_down", "Serviço indisponível", "O serviço está fora do ar"],
  ["no_workaround", "Sem contorno", "Não há alternativa de uso"],
  ["data_loss", "Perda de dados", "Há perda ou corrupção de dados"],
  ["security_risk", "Risco de segurança", "Suspeita de incidente de segurança"],
  ["customer_impact", "Impacta cliente", "Afeta cliente externo"],
  ["recent_deploy", "Após deploy", "Ocorreu após uma mudança recente"],
  ["recurring", "Recorrente", "Já aconteceu antes"],
  ["financial_impact", "Impacto financeiro", "Há perda financeira envolvida"]
];

// Faixas de score -> prioridade. Espelham a função classify() do backend.
export const priorityBands = [
  { level: "P4", label: "Baixa", min: 0, max: 34, tone: "low" },
  { level: "P3", label: "Média", min: 35, max: 59, tone: "medium" },
  { level: "P2", label: "Alta", min: 60, max: 84, tone: "high" },
  { level: "P1", label: "Crítica", min: 85, max: 100, tone: "critical" }
];
