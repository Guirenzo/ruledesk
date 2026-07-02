# RuleDesk Backend

API HTTP em Python puro para demonstrar um sistema especialista baseado em regras.

## Rodar localmente

```powershell
cd backend
py -m app.main
```

A API sobe em:

- `GET /health`
- `GET /api/rules`
- `GET /api/incidents`
- `GET /api/stats`
- `POST /api/incidents`
- `POST /api/seed`

## Popular dados de exemplo

Com a API desligada ou ligada:

```powershell
cd backend
py -m scripts.seed
```

Ou pela API:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/seed
```

## Testes

```powershell
cd backend
py -m unittest discover -s tests
```

## Arquitetura

- `app/api`: rotas e handlers HTTP.
- `app/core`: configuracao e helpers HTTP.
- `app/db`: conexao SQLite e schema.
- `app/repositories`: acesso aos chamados persistidos.
- `app/schemas`: validacao e normalizacao de entrada.
- `app/services`: motor de regras e analytics.
- `scripts`: seeds e smoke test.

## Ideia de IA usada

O projeto representa conhecimento especialista por regras de producao. O motor recebe fatos do incidente, dispara regras, soma evidencias e devolve uma decisao explicavel: prioridade, regras ativadas e recomendacoes.
