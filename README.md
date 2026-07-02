# RuleDesk

Sistema especialista para triagem inteligente de chamados de TI.

O projeto foi montado para o seminario de Aplicacoes Inteligentes no Dia-a-Dia, no tema Sistemas Baseados em Regras.

## Estrutura

```text
backend/   API Python, SQLite, motor de regras, testes e Dockerfile
frontend/  React + Vite, dashboard e integracao com API
docs/      material da apresentacao e relatorio
outputs/   entregaveis finais
```

## Rodar sem Docker

Terminal 1:

```powershell
cd backend
py -m app.main
```

Terminal 2:

```powershell
cd frontend
npm install
npm run dev
```

Abra:

```text
http://127.0.0.1:5173
```

## Rodar com Docker

```powershell
docker compose up --build
```

Abra:

```text
http://127.0.0.1:5173
```

## Testes

Backend:

```powershell
cd backend
py -m unittest discover -s tests
```

Frontend:

```powershell
cd frontend
npm run build
```

## Endpoints principais

- `GET /health`
- `GET /api/rules`
- `GET /api/incidents`
- `GET /api/stats`
- `POST /api/incidents`
- `POST /api/seed`

## Como defender na apresentacao

O sistema representa conhecimento especialista por regras de producao. Cada chamado gera fatos, como ambiente, usuarios afetados, impacto em cliente e risco de seguranca. O backend aplica encadeamento para frente: fatos ativam regras, regras somam evidencias e o sistema retorna prioridade, justificativa e recomendacoes.
