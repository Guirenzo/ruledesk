# Roteiro de apresentacao - RuleDesk

Tempo alvo: 10 minutos.

## 1. Abertura - 1 minuto

Boa noite. Nosso tema e Sistemas Baseados em Regras, uma abordagem classica de Inteligencia Artificial simbolica. Para demonstrar o conceito, criamos o RuleDesk, um sistema especialista para triagem inteligente de chamados de TI.

Ideia central: o sistema recebe fatos de um incidente, aplica regras de producao e devolve prioridade, justificativa e recomendacoes.

## 2. Conceito - 2 minutos

Explique:

- IA simbolica representa conhecimento explicitamente.
- Sistema especialista tenta simular parte do raciocinio de um especialista.
- Regras seguem a estrutura SE condicao, ENTAO conclusao ou acao.
- Encadeamento para frente parte dos fatos e chega em conclusoes.

Exemplo falado:

SE o chamado esta em producao E o servico esta indisponivel E impacta clientes, ENTAO a prioridade deve subir.

## 3. Problema escolhido - 1 minuto

O problema e triagem de chamados de TI.

Por que isso e bom:

- E comum em Engenharia de Software.
- Envolve SLA, impacto, risco e prioridade.
- Precisa de criterio padronizado.
- A decisao precisa ser explicavel.

## 4. Arquitetura - 1 minuto

Mostre a estrutura:

- Frontend React.
- Backend Python.
- SQLite.
- Motor de regras.
- Docker Compose opcional.

Fale que o backend nao e so tela: ele tem camadas, validacao, API, banco, regras e testes.

## 5. Demonstracao - 3 minutos

Roteiro na tela:

1. Abrir `http://127.0.0.1:5173`.
2. Clicar em "P1 indisponivel".
3. Clicar em "Avaliar chamado".
4. Mostrar prioridade P1, score e tempo alvo.
5. Mostrar regras disparadas.
6. Mostrar recomendacoes.
7. Mostrar historico e estatisticas.
8. Clicar em "Bug controlado" e avaliar.
9. Comparar como o score cai e as regras mudam.

Frase boa:

O ponto mais importante aqui e a explicabilidade: o sistema nao devolve so uma resposta, ele mostra quais regras foram ativadas.

## 6. Fechamento - 2 minutos

Conclusao:

- Sistemas baseados em regras ainda sao uteis.
- Sao bons quando o conhecimento do dominio e claro.
- Ajudam em padronizacao e auditoria.
- Em Engenharia de Software, podem apoiar suporte, incidentes, monitoramento e regras de negocio.

Limitacao:

Os pesos foram definidos manualmente. Em producao, seriam calibrados com dados historicos e especialistas.

Fecho:

O RuleDesk demonstra que uma aplicacao inteligente nao precisa obrigatoriamente treinar modelo. Em muitos cenarios, regras bem definidas entregam decisoes rapidas, explicaveis e uteis.

## Perguntas provaveis

### Isso e IA mesmo?

Sim. E IA simbolica. A IA nao e apenas aprendizado de maquina; tambem inclui representacao de conhecimento, raciocinio e inferencia.

### Por que nao usar machine learning?

Porque o problema exige explicabilidade e pode ser modelado com regras claras. Machine learning faria sentido se houvesse grande historico de chamados rotulados.

### O sistema aprende sozinho?

Nao nesta versao. Ele aplica conhecimento definido na base de regras. Uma evolucao seria ajustar pesos automaticamente com base no historico.

### Qual a vantagem no mundo real?

Padronizar prioridade, reduzir subjetividade, acelerar atendimento e justificar decisoes.
