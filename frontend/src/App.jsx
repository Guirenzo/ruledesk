import {
  Activity,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  ClipboardList,
  Database,
  FlaskConical,
  Gauge,
  History,
  Layers,
  Lightbulb,
  ListChecks,
  Moon,
  Play,
  RefreshCw,
  Search,
  Server,
  ShieldAlert,
  Sparkles,
  Sun,
  Workflow,
  Zap
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import {
  checkHealth,
  createIncident,
  getRules,
  getStats,
  listIncidents,
  seedIncidents
} from "./services/api.js";
import {
  booleanFields,
  categories,
  defaultIncident,
  environments,
  priorityBands,
  scenarios
} from "./data/scenarios.js";

const priorityClass = {
  P1: "critical",
  P2: "high",
  P3: "medium",
  P4: "low"
};

const categoryLabel = Object.fromEntries(categories);
const environmentLabel = Object.fromEntries(environments);
const booleanLabel = Object.fromEntries(booleanFields.map(([field, label]) => [field, label]));

const TABS = [
  ["simulator", "Simulador", ClipboardList],
  ["how", "Como funciona", BookOpen],
  ["knowledge", "Base de conhecimento", Layers]
];

function App() {
  const [tab, setTab] = useState("simulator");
  const [theme, setTheme] = useState("light");
  const [incident, setIncident] = useState(defaultIncident);
  const [evaluation, setEvaluation] = useState(null);
  const [history, setHistory] = useState([]);
  const [rules, setRules] = useState([]);
  const [stats, setStats] = useState(null);
  const [apiStatus, setApiStatus] = useState("checking");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [activeScenario, setActiveScenario] = useState(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const selectedPriority = evaluation?.priority?.level || "P4";
  const score = evaluation?.score || 0;

  async function refreshData() {
    try {
      const [health, rulesData, incidentsData, statsData] = await Promise.all([
        checkHealth(),
        getRules(),
        listIncidents(10),
        getStats()
      ]);
      setApiStatus(health.status === "ok" ? "online" : "offline");
      setRules(rulesData.rules || []);
      setHistory(incidentsData.items || []);
      setStats(statsData);
    } catch (error) {
      setApiStatus("offline");
      setMessage(error.message);
    }
  }

  useEffect(() => {
    refreshData();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const data = await createIncident(incident);
      setEvaluation(data.evaluation);
      await refreshData();
      setMessage("Chamado avaliado e salvo no histórico.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSeed() {
    setLoading(true);
    setMessage("");
    try {
      await seedIncidents();
      await refreshData();
      setMessage("Cenários de exemplo carregados.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  function updateField(field, value) {
    setIncident((current) => ({ ...current, [field]: value }));
    setActiveScenario(null);
  }

  function applyScenario(key) {
    const scenario = scenarios[key];
    setIncident(scenario.payload);
    setEvaluation(null);
    setActiveScenario(key);
    setMessage(`Cenário "${scenario.name}" carregado. Clique em Avaliar para inferir.`);
  }

  const firedCodes = useMemo(
    () => new Set((evaluation?.rules_fired || []).map((rule) => rule.code)),
    [evaluation]
  );

  return (
    <div className="app">
      <div className="bg-orbs" aria-hidden="true">
        <span className="orb orb-a" />
        <span className="orb orb-b" />
      </div>

      <header className="shell header-shell">
        <div className="brand-block">
          <div className="brand-mark">
            <BrainCircuit size={26} />
          </div>
          <div>
            <div className="brand-title">
              <h1>RuleDesk</h1>
              <span className="brand-tag">IA Simbólica</span>
            </div>
            <p>Sistema especialista para triagem inteligente de chamados de TI</p>
          </div>
        </div>

        <div className="header-actions">
          <div className={`status-pill ${apiStatus}`}>
            <span className="status-dot" />
            <Server size={15} />
            <span>
              {apiStatus === "online"
                ? "API online"
                : apiStatus === "checking"
                ? "Verificando..."
                : "API offline"}
            </span>
          </div>
          <button
            type="button"
            className="icon-button"
            onClick={() => setTheme((t) => (t === "light" ? "dark" : "light"))}
            title={theme === "light" ? "Tema escuro" : "Tema claro"}
          >
            {theme === "light" ? <Moon size={18} /> : <Sun size={18} />}
          </button>
        </div>
      </header>

      <nav className="shell tab-bar">
        {TABS.map(([key, label, Icon]) => (
          <button
            key={key}
            type="button"
            className={`tab ${tab === key ? "active" : ""}`}
            onClick={() => setTab(key)}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </nav>

      <main className="shell page">
        {tab === "simulator" ? (
          <SimulatorView
            incident={incident}
            evaluation={evaluation}
            stats={stats}
            history={history}
            rules={rules}
            loading={loading}
            message={message}
            activeScenario={activeScenario}
            selectedPriority={selectedPriority}
            score={score}
            firedCodes={firedCodes}
            onSubmit={handleSubmit}
            onSeed={handleSeed}
            onField={updateField}
            onScenario={applyScenario}
          />
        ) : null}

        {tab === "how" ? <HowItWorks /> : null}

        {tab === "knowledge" ? <KnowledgeBase rules={rules} firedCodes={firedCodes} /> : null}
      </main>

      <footer className="shell foot">
        <span>RuleDesk · Seminário de Aplicações Inteligentes no Dia-a-Dia</span>
        <span>Tema: Sistemas Baseados em Regras · Encadeamento para frente</span>
      </footer>
    </div>
  );
}

function SimulatorView({
  incident,
  evaluation,
  stats,
  history,
  rules,
  loading,
  message,
  activeScenario,
  selectedPriority,
  score,
  firedCodes,
  onSubmit,
  onSeed,
  onField,
  onScenario
}) {
  return (
    <>
    <div className="workspace">
      <section className="left-column">
        <div className="panel scenarios-panel">
          <div className="section-heading">
            <Zap size={18} />
            <div>
              <h2>Cenários rápidos</h2>
              <p>Casos prontos para demonstração</p>
            </div>
          </div>
          <div className="scenario-grid">
            {Object.entries(scenarios).map(([key, scenario]) => (
              <button
                key={key}
                type="button"
                className={`scenario-card ${scenario.tone} ${activeScenario === key ? "active" : ""}`}
                onClick={() => onScenario(key)}
              >
                <strong>{scenario.name}</strong>
                <span>{scenario.summary}</span>
                <em className={`tag ${scenario.tone}`}>{scenario.expected}</em>
              </button>
            ))}
          </div>
        </div>

        <form className="panel form-panel" onSubmit={onSubmit}>
          <div className="section-heading">
            <ClipboardList size={18} />
            <div>
              <h2>Novo chamado</h2>
              <p>Informe os fatos observados</p>
            </div>
          </div>

          <label className="field wide">
            <span>Título</span>
            <input
              value={incident.title}
              onChange={(event) => onField("title", event.target.value)}
              maxLength={140}
            />
          </label>

          <div className="field-grid">
            <label className="field">
              <span>Categoria</span>
              <select value={incident.category} onChange={(event) => onField("category", event.target.value)}>
                {categories.map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Ambiente</span>
              <select
                value={incident.environment}
                onChange={(event) => onField("environment", event.target.value)}
              >
                {environments.map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>

            <label className="field range-field">
              <span>
                Usuários afetados <b>{incident.affected_users}</b>
              </span>
              <input
                type="range"
                min="1"
                max="1000"
                value={incident.affected_users}
                onChange={(event) => onField("affected_users", Number(event.target.value))}
              />
            </label>

            <label className="field">
              <span>SLA restante</span>
              <select
                value={incident.sla_hours}
                onChange={(event) => onField("sla_hours", Number(event.target.value))}
              >
                <option value={1}>1 hora</option>
                <option value={2}>2 horas</option>
                <option value={4}>4 horas</option>
                <option value={24}>24 horas</option>
                <option value={72}>72 horas</option>
              </select>
            </label>
          </div>

          <div className="switch-grid">
            {booleanFields.map(([field, label, hint]) => (
              <label className={`switch ${incident[field] ? "on" : ""}`} key={field} title={hint}>
                <input
                  type="checkbox"
                  checked={incident[field]}
                  onChange={(event) => onField(field, event.target.checked)}
                />
                <span className="switch-track" aria-hidden="true">
                  <i />
                </span>
                <span className="switch-label">{label}</span>
              </label>
            ))}
          </div>

          <label className="field wide">
            <span>Reportado por</span>
            <input
              value={incident.reported_by}
              onChange={(event) => onField("reported_by", event.target.value)}
              maxLength={80}
            />
          </label>

          <div className="form-actions">
            <button className="primary" type="submit" disabled={loading}>
              {loading ? <RefreshCw size={17} className="spin" /> : <Play size={17} />}
              Avaliar chamado
            </button>
            <button type="button" onClick={onSeed} disabled={loading}>
              <Database size={17} />
              Popular demo
            </button>
          </div>

          {message ? <p className="message">{message}</p> : null}
        </form>
      </section>

      <section className="right-column">
        <DiagnosisCard evaluation={evaluation} priority={selectedPriority} score={score} />
        <InferenceTrace evaluation={evaluation} />
        <RecommendationsCard evaluation={evaluation} />
      </section>
    </div>

    <section className="ops-dashboard">
      <div className="section-heading ops-heading">
        <Activity size={18} />
        <div>
          <h2>Painel operacional</h2>
          <p>Histórico e indicadores das avaliações salvas</p>
        </div>
      </div>
      <div className="ops-grid">
        <StatsPanel stats={stats} />
        <HistoryPanel history={history} />
        <TopRulesPanel stats={stats} rules={rules} firedCodes={firedCodes} />
      </div>
    </section>
    </>
  );
}

function DiagnosisCard({ evaluation, priority, score }) {
  const tone = priorityClass[priority];
  const facts = evaluation ? buildFacts(evaluation.incident) : [];

  return (
    <div className={`panel diagnosis-panel ${tone}`}>
      <div className="diagnosis-top">
        <div className="diagnosis-lead">
          <div className="eyebrow">
            <Gauge size={15} /> Diagnóstico
          </div>
          <h2>{evaluation ? `Prioridade ${evaluation.priority.label}` : "Aguardando avaliação"}</h2>
          <p>
            {evaluation
              ? `${evaluation.priority.level} · ${evaluation.priority.ticket_type}`
              : "Nenhum chamado avaliado nesta sessão."}
          </p>
        </div>

        <div className="score-ring" style={{ "--score": `${score * 3.6}deg` }}>
          <strong>{score}</strong>
          <span>score</span>
        </div>
      </div>

      <ScoreBands score={score} active={evaluation ? priority : null} />

      <div className="metric-row">
        <Metric label="Tempo alvo" value={evaluation?.priority?.response_time || "—"} />
        <Metric label="Responsável" value={evaluation?.priority?.owner || "—"} />
        <Metric label="Categoria" value={evaluation?.category_label || "—"} />
      </div>

      {facts.length ? (
        <div className="facts-strip">
          <span className="facts-title">Fatos coletados</span>
          <div className="fact-chips">
            {facts.map((fact) => (
              <span className={`fact-chip ${fact.strong ? "strong" : ""}`} key={fact.label}>
                {fact.label}
              </span>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}

function ScoreBands({ score, active }) {
  return (
    <div className="score-bands">
      <div className="band-track">
        {priorityBands.map((band) => (
          <div
            key={band.level}
            className={`band ${band.tone} ${active === band.level ? "active" : ""}`}
            style={{ flex: band.max - band.min + 1 }}
          >
            <b>{band.level}</b>
            <span>{band.label}</span>
          </div>
        ))}
        {active ? <div className="band-marker" style={{ left: `${score}%` }} /> : null}
      </div>
      <div className="band-scale">
        <span>0</span>
        <span>35</span>
        <span>60</span>
        <span>85</span>
        <span>100</span>
      </div>
    </div>
  );
}

function InferenceTrace({ evaluation }) {
  if (!evaluation) {
    return (
      <div className="panel trace-panel">
        <div className="section-heading">
          <Workflow size={18} />
          <div>
            <h2>Motor de inferência</h2>
            <p>Encadeamento para frente</p>
          </div>
        </div>
        <div className="empty-state large">
          Avalie um chamado para ver o raciocínio: fatos → regras disparadas → cálculo do score → prioridade.
        </div>
      </div>
    );
  }

  const hits = evaluation.rules_fired || [];
  const base = evaluation.base_score ?? 10;
  const raw = evaluation.raw_score ?? evaluation.score;
  const clamped = raw !== evaluation.score;

  return (
    <div className="panel trace-panel">
      <div className="section-heading">
        <Workflow size={18} />
        <div>
          <h2>Motor de inferência</h2>
          <p>Encadeamento para frente, passo a passo</p>
        </div>
      </div>

      <ol className="trace-steps">
        <li className="trace-step">
          <div className="trace-index">1</div>
          <div className="trace-body">
            <h3>Base de fatos</h3>
            <p>O motor parte dos fatos objetivos informados no chamado.</p>
          </div>
        </li>

        <li className="trace-step">
          <div className="trace-index">2</div>
          <div className="trace-body">
            <h3>
              Regras disparadas <span className="count">{hits.length}</span>
            </h3>
            <ul className="rule-hit-list">
              {hits.length ? (
                hits.map((rule) => (
                  <li key={rule.code} className={rule.weight < 0 ? "negative" : ""}>
                    <span className="weight">{rule.weight > 0 ? `+${rule.weight}` : rule.weight}</span>
                    <div>
                      <strong>
                        {rule.code} · {rule.title}
                      </strong>
                      <p>{rule.explanation}</p>
                    </div>
                  </li>
                ))
              ) : (
                <li>
                  <span className="weight">0</span>
                  <div>
                    <strong>Nenhuma regra disparou</strong>
                    <p>Os fatos informados não ativaram nenhuma condição da base.</p>
                  </div>
                </li>
              )}
            </ul>
          </div>
        </li>

        <li className="trace-step">
          <div className="trace-index">3</div>
          <div className="trace-body">
            <h3>Cálculo do score</h3>
            <div className="calc-tokens">
              <span className="token base">base {base}</span>
              {hits.map((rule) => (
                <span className={`token ${rule.weight < 0 ? "neg" : "pos"}`} key={rule.code}>
                  {rule.weight > 0 ? `+${rule.weight}` : rule.weight}
                  <em>{rule.code}</em>
                </span>
              ))}
              <span className="token equals">= {raw}</span>
            </div>
            {clamped ? (
              <p className="calc-note">
                Score limitado à faixa 0–100 → <b>{evaluation.score}</b>
              </p>
            ) : null}
          </div>
        </li>

        <li className="trace-step">
          <div className="trace-index">4</div>
          <div className="trace-body">
            <h3>Classificação</h3>
            <p className="conclusion">
              Score <b>{evaluation.score}</b>
              <ArrowRight size={15} />
              <span className={`pill-priority ${priorityClass[evaluation.priority.level]}`}>
                {evaluation.priority.level} · {evaluation.priority.label}
              </span>
            </p>
          </div>
        </li>
      </ol>
    </div>
  );
}

function RecommendationsCard({ evaluation }) {
  const items = evaluation?.recommendations || [];
  if (!items.length) return null;

  return (
    <div className="panel rec-panel">
      <div className="section-heading">
        <ListChecks size={18} />
        <div>
          <h2>Ações recomendadas</h2>
          <p>Geradas a partir das regras disparadas</p>
        </div>
      </div>
      <ol className="recommendation-list">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ol>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function StatsPanel({ stats }) {
  const total = stats?.total || 0;
  const p1 = stats?.by_priority?.P1 || 0;
  const p2 = stats?.by_priority?.P2 || 0;

  return (
    <div className="panel compact-panel">
      <div className="section-heading">
        <Activity size={18} />
        <div>
          <h2>Operação</h2>
          <p>Indicadores salvos</p>
        </div>
      </div>
      <div className="kpi-grid">
        <Metric label="Chamados" value={total} />
        <Metric label="Score médio" value={stats?.average_score ?? 0} />
        <Metric label="P1 + P2" value={p1 + p2} />
      </div>
      <div className="mini-bars">
        {["P1", "P2", "P3", "P4"].map((level) => {
          const value = stats?.by_priority?.[level] || 0;
          const width = total ? `${Math.max(6, (value / total) * 100)}%` : "6%";
          return (
            <div className="mini-bar" key={level}>
              <span>{level}</span>
              <div className={`mini-track ${priorityClass[level]}`}>
                <i style={{ width }} />
              </div>
              <b>{value}</b>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function HistoryPanel({ history }) {
  return (
    <div className="panel compact-panel">
      <div className="section-heading">
        <History size={18} />
        <div>
          <h2>Histórico</h2>
          <p>Últimas avaliações</p>
        </div>
      </div>
      <div className="history-list">
        {history.length ? (
          history.slice(0, 5).map((item) => (
            <div className="history-item" key={item.id}>
              <span className={`level-dot ${priorityClass[item.priority_level]}`} />
              <div>
                <strong>{item.title}</strong>
                <p>
                  {item.priority_level} · score {item.score}
                </p>
              </div>
              {item.priority_level === "P1" ? (
                <ShieldAlert size={17} className="ic-alert" />
              ) : (
                <CheckCircle2 size={17} className="ic-ok" />
              )}
            </div>
          ))
        ) : (
          <div className="empty-state">Sem histórico salvo ainda.</div>
        )}
      </div>
    </div>
  );
}

function TopRulesPanel({ stats, rules, firedCodes }) {
  const top = stats?.top_rules || [];
  const titleByCode = Object.fromEntries(rules.map((r) => [r.code, r.if]));
  const max = top.reduce((acc, item) => Math.max(acc, item.count), 0) || 1;

  return (
    <div className="panel rules-panel">
      <div className="section-heading">
        <Sparkles size={18} />
        <div>
          <h2>Regras mais disparadas</h2>
          <p>Padrões recorrentes no histórico</p>
        </div>
      </div>
      {top.length ? (
        <div className="top-rules">
          {top.map((item) => (
            <div className={`top-rule ${firedCodes.has(item.code) ? "active" : ""}`} key={item.code}>
              <span className="code">{item.code}</span>
              <p>{titleByCode[item.code] || "condição"}</p>
              <div className="top-track">
                <i style={{ width: `${Math.max(8, (item.count / max) * 100)}%` }} />
              </div>
              <b>{item.count}</b>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">Avalie chamados ou popule a demo para ver estatísticas.</div>
      )}
    </div>
  );
}

const BUILDING_BLOCKS = [
  [Layers, "Base de conhecimento", "As 16 regras de produção no formato SE condição ENTÃO ação, com pesos definidos por especialistas."],
  [ClipboardList, "Base de fatos", "Os dados objetivos do chamado: ambiente, usuários afetados, indisponibilidade, risco, SLA."],
  [Workflow, "Motor de inferência", "Combina fatos com regras por encadeamento para frente e acumula um score de criticidade."],
  [Lightbulb, "Explicação", "Cada decisão mostra quais regras dispararam e por quê — decisão rastreável e auditável."]
];

const PIPELINE = [
  [ClipboardList, "Fatos", "Entrada do chamado"],
  [Workflow, "Regras", "Condições avaliadas"],
  [Gauge, "Score", "Soma de evidências"],
  [ShieldAlert, "Prioridade", "P1 · P2 · P3 · P4"]
];

function HowItWorks() {
  return (
    <div className="how-view">
      <div className="panel hero-panel">
        <div className="hero-badge">
          <FlaskConical size={15} /> IA Simbólica
        </div>
        <h2>O que é um sistema baseado em regras?</h2>
        <p>
          Diferente de modelos que aprendem padrões a partir de dados, um sistema especialista raciocina
          sobre conhecimento definido explicitamente. O RuleDesk representa a experiência de um time de TI
          em regras do tipo <b>SE</b> uma situação ocorre <b>ENTÃO</b> uma conclusão é reforçada — e explica
          cada decisão que toma.
        </p>
      </div>

      <div className="blocks-grid">
        {BUILDING_BLOCKS.map(([Icon, title, text]) => (
          <div className="block-card" key={title}>
            <div className="block-icon">
              <Icon size={20} />
            </div>
            <h3>{title}</h3>
            <p>{text}</p>
          </div>
        ))}
      </div>

      <div className="panel pipeline-panel">
        <div className="section-heading">
          <Workflow size={18} />
          <div>
            <h2>Encadeamento para frente</h2>
            <p>Do fato à conclusão, em quatro etapas</p>
          </div>
        </div>
        <div className="pipeline">
          {PIPELINE.map(([Icon, title, text], index) => (
            <div className="pipeline-step" key={title}>
              <div className="pipeline-node">
                <Icon size={22} />
              </div>
              <strong>{title}</strong>
              <span>{text}</span>
              {index < PIPELINE.length - 1 ? <ArrowRight className="pipeline-arrow" size={20} /> : null}
            </div>
          ))}
        </div>
      </div>

      <div className="panel example-panel">
        <div className="section-heading">
          <Lightbulb size={18} />
          <div>
            <h2>Exemplo de raciocínio</h2>
            <p>Uma queda de serviço em produção</p>
          </div>
        </div>
        <div className="example-flow">
          <div className="example-col">
            <h4>Fatos</h4>
            <ul>
              <li>Ambiente = produção</li>
              <li>Serviço indisponível</li>
              <li>Impacta cliente</li>
              <li>Sem contorno</li>
            </ul>
          </div>
          <ArrowRight className="example-arrow" size={22} />
          <div className="example-col">
            <h4>Regras disparadas</h4>
            <ul>
              <li>R01 ambiente produtivo (+12)</li>
              <li>R02 serviço indisponível (+35)</li>
              <li>R07 sem contorno (+15)</li>
              <li>R08 impacta cliente (+16)</li>
            </ul>
          </div>
          <ArrowRight className="example-arrow" size={22} />
          <div className="example-col">
            <h4>Conclusão</h4>
            <p className="example-result">
              Score alto → <span className="pill-priority critical">P1 · Crítica</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function KnowledgeBase({ rules, firedCodes }) {
  const [query, setQuery] = useState("");
  const [group, setGroup] = useState("all");

  const groups = useMemo(() => {
    const set = new Set(rules.map((r) => r.group).filter(Boolean));
    return ["all", ...Array.from(set)];
  }, [rules]);

  const filtered = rules.filter((rule) => {
    const matchesGroup = group === "all" || rule.group === group;
    const text = `${rule.code} ${rule.if} ${rule.then} ${rule.group}`.toLowerCase();
    const matchesQuery = text.includes(query.trim().toLowerCase());
    return matchesGroup && matchesQuery;
  });

  return (
    <div className="knowledge-view">
      <div className="panel kb-header">
        <div className="section-heading">
          <Layers size={18} />
          <div>
            <h2>Base de conhecimento</h2>
            <p>{rules.length} regras de produção · pesos definidos por especialistas</p>
          </div>
        </div>
        <div className="kb-controls">
          <div className="kb-search">
            <Search size={16} />
            <input
              placeholder="Buscar regra, condição ou grupo..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
          <div className="kb-groups">
            {groups.map((g) => (
              <button
                key={g}
                type="button"
                className={`chip-btn ${group === g ? "active" : ""}`}
                onClick={() => setGroup(g)}
              >
                {g === "all" ? "Todas" : g}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="kb-grid">
        {filtered.map((rule) => (
          <div className={`kb-card ${firedCodes.has(rule.code) ? "active-rule" : ""}`} key={rule.code}>
            <div className="kb-card-top">
              <span className="kb-code">{rule.code}</span>
              {rule.group ? <span className="kb-group">{rule.group}</span> : null}
              <b className={`kb-weight ${rule.weight < 0 ? "neg" : "pos"}`}>
                {rule.weight > 0 ? `+${rule.weight}` : rule.weight}
              </b>
            </div>
            <p className="kb-rule">
              <span className="kw">SE</span> {rule.if}
            </p>
            <p className="kb-rule">
              <span className="kw then">ENTÃO</span> {rule.then}
            </p>
          </div>
        ))}
      </div>
      {filtered.length === 0 ? <div className="empty-state">Nenhuma regra encontrada.</div> : null}
    </div>
  );
}

function buildFacts(incident) {
  if (!incident) return [];
  const facts = [
    { label: `Ambiente: ${environmentLabel[incident.environment] || incident.environment}`, strong: incident.environment === "production" },
    { label: `Categoria: ${categoryLabel[incident.category] || incident.category}` },
    { label: `${incident.affected_users} usuários`, strong: incident.affected_users >= 250 },
    { label: `SLA ${incident.sla_hours}h`, strong: incident.sla_hours <= 1 }
  ];
  for (const [field, label] of Object.entries(booleanLabel)) {
    if (incident[field]) {
      facts.push({ label, strong: ["service_down", "data_loss", "security_risk"].includes(field) });
    }
  }
  return facts;
}

export default App;
