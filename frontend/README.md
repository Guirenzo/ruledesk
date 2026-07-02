# RuleDesk Frontend

Interface React para operar a demonstracao do sistema especialista.

## Rodar localmente

```powershell
cd frontend
npm install
npm run dev
```

Abra:

```text
http://127.0.0.1:5173
```

O frontend espera a API em:

```text
http://127.0.0.1:8000
```

Para mudar:

```powershell
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
npm run dev
```

## Build

```powershell
cd frontend
npm run build
```
