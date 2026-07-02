# RuleDesk: Sistema Especialista para Triagem Inteligente de Chamados de TI

## 1. Introducao

A Inteligencia Artificial nao se limita a redes neurais e modelos generativos. Uma das abordagens classicas da IA e a construcao de sistemas capazes de raciocinar a partir de conhecimento explicito. Nesse contexto, os sistemas baseados em regras representam conhecimento por meio de condicoes e consequencias, normalmente no formato "SE uma situacao ocorre, ENTAO uma acao deve ser tomada".

Este trabalho apresenta o RuleDesk, um prototipo funcional de sistema especialista para triagem de chamados de TI. A aplicacao recebe informacoes sobre um incidente, como ambiente afetado, numero de usuarios impactados, risco de seguranca, perda de dados e existencia de contorno. Em seguida, um motor de regras calcula prioridade, nivel de atendimento, tempo alvo, responsavel e recomendacoes.

O tema escolhido foi Sistemas Baseados em Regras, pois ele se conecta diretamente com Engenharia de Software: regras de negocio, suporte tecnico, SLA, incidentes, auditoria, explicabilidade e automacao de decisoes operacionais.

## 2. Objetivo

O objetivo do projeto e demonstrar como um sistema especialista pode apoiar a tomada de decisao em um fluxo realista de Engenharia de Software. O sistema nao substitui a equipe tecnica, mas ajuda a padronizar criterios de classificacao e a explicar por que um chamado foi considerado critico, alto, medio ou baixo.

Objetivos especificos:

- Representar conhecimento especialista em uma base de regras.
- Aplicar inferencia para frente a partir dos fatos de um chamado.
- Classificar automaticamente prioridade e tipo de incidente.
- Registrar historico das avaliacoes em banco de dados.
- Apresentar regras disparadas e recomendacoes de forma visual.
- Criar uma demonstracao full-stack com backend, frontend, persistencia e Docker.

## 3. Fundamentos Teoricos

Sistemas baseados em regras sao sistemas de IA simbolica. Diferente de modelos estatisticos, que aprendem padroes a partir de dados, sistemas de regras dependem de conhecimento definido explicitamente por especialistas, analistas ou engenheiros.

Um sistema especialista normalmente possui:

- Base de conhecimento: conjunto de regras, conceitos e criterios.
- Base de fatos: dados observados em um problema especifico.
- Motor de inferencia: mecanismo que combina fatos com regras.
- Explicacao: justificativa da decisao tomada.
- Interface: meio pelo qual o usuario informa fatos e recebe conclusoes.

O RuleDesk usa regras de producao com pesos. Cada regra disparada soma ou reduz pontos no score final. O score e entao convertido em prioridades:

- P1 Critica: resposta em 15 minutos.
- P2 Alta: resposta em 1 hora.
- P3 Media: resposta em 4 horas.
- P4 Baixa: resposta em 1 dia util.

## 4. Encadeamento para Frente

O prototipo usa encadeamento para frente. Nesse modelo, o raciocinio comeca nos fatos conhecidos e avanca ate conclusoes. Por exemplo:

Fatos:

- Ambiente = producao.
- Servico indisponivel = verdadeiro.
- Impacta cliente = verdadeiro.
- Sem contorno = verdadeiro.

Regras disparadas:

- R01: ambiente produtivo aumenta criticidade.
- R02: servico indisponivel indica alto impacto operacional.
- R07: ausencia de contorno reduz tolerancia de espera.
- R08: impacto no cliente aumenta urgencia.

Conclusao:

- Prioridade P1 ou P2, dependendo do score acumulado.

Esse modelo combina bem com triagem de incidentes porque a decisao parte de evidencias objetivas.

## 5. Tecnicas, Ferramentas e Frameworks

### Tecnicas

- Regras de producao.
- Inferencia para frente.
- Pontuacao por evidencias.
- Classificacao por faixas.
- Explicabilidade por regras disparadas.
- Persistencia de historico para analise.

### Ferramentas do projeto

- Backend: Python com biblioteca padrao.
- API: HTTP REST sem dependencia externa.
- Banco de dados: SQLite.
- Frontend: React com Vite.
- Interface: componentes React e icones lucide-react.
- Empacotamento: Docker e Docker Compose.
- Testes: unittest.

### Ferramentas relacionadas ao tema

- CLIPS: linguagem baseada em regras criada para construcao de sistemas especialistas.
- Drools: motor de regras de negocio usado no ecossistema Java/KIE.
- Jess: ambiente de regras inspirado em CLIPS para Java.
- Experta/PyKnow: opcoes em Python para regras e motores simples.

## 6. Estudos de Caso e Aplicacoes Reais

Sistemas baseados em regras sao usados quando a decisao precisa ser rastreavel e auditavel.

Exemplos:

- Suporte tecnico: classificar prioridade de chamados.
- Saude: apoio a triagem clinica e verificacao de protocolos.
- Financas: validacao de risco, compliance e regras antifraude.
- Industria: diagnostico de falhas em equipamentos.
- Seguranca da informacao: resposta a incidentes e classificacao de alertas.
- Sistemas corporativos: regras de aprovacao, beneficios e politicas internas.

No caso de Engenharia de Software, regras sao comuns em sistemas de SLA, triagem de bugs, roteamento de tickets, pipelines de deploy e monitoramento.

## 7. Proposta da Aplicacao

O RuleDesk simula uma central de operacoes de TI. O usuario registra um incidente e informa fatos objetivos:

- titulo;
- categoria;
- ambiente;
- usuarios afetados;
- SLA restante;
- indisponibilidade;
- perda de dados;
- risco de seguranca;
- impacto em cliente;
- deploy recente;
- recorrencia;
- impacto financeiro.

O backend avalia esses fatos por meio do motor de regras. A resposta contem:

- score final;
- prioridade;
- nivel P1, P2, P3 ou P4;
- tempo alvo de resposta;
- responsavel indicado;
- regras disparadas;
- recomendacoes;
- registro persistido no historico.

## 8. Arquitetura do Sistema

```text
Usuario
  |
  v
Frontend React
  |
  v
API Python REST
  |
  +--> Validacao de entrada
  +--> Motor de regras
  +--> Repositorio SQLite
  +--> Estatisticas
  |
  v
Resposta explicavel
```

### Backend

O backend foi dividido em camadas:

- `app/api`: rotas e handlers HTTP.
- `app/core`: configuracoes e helpers.
- `app/db`: conexao SQLite e schema.
- `app/repositories`: persistencia de chamados.
- `app/schemas`: validacao dos dados.
- `app/services`: motor de regras e analytics.
- `tests`: testes automatizados.

### Frontend

O frontend React possui:

- formulario de chamado;
- cenarios rapidos de demonstracao;
- painel de diagnostico;
- score visual;
- regras disparadas;
- recomendacoes;
- historico;
- estatisticas;
- base de conhecimento.

## 9. Base de Regras

Exemplos de regras usadas:

| Codigo | Condicao | Acao | Peso |
| --- | --- | --- | --- |
| R01 | Ambiente em producao | Aumentar criticidade | +12 |
| R02 | Servico indisponivel | Forte candidato a P1 | +35 |
| R03 | Perda de dados | Escalar e preservar evidencias | +32 |
| R04 | Risco de seguranca | Acionar resposta a incidente | +35 |
| R05 | Usuarios afetados >= 250 | Impacto massivo | +24 |
| R07 | Sem contorno | Reduzir tolerancia de espera | +15 |
| R08 | Impacta cliente | Elevar urgencia | +16 |
| R12 | Falha apos deploy | Sugerir rollback ou analise | +8 |
| R16 | Existe contorno e nao ha sinais criticos | Reduzir prioridade | -8 |

## 10. Demonstracao Pratica

A demonstracao apresenta quatro cenarios prontos:

- P1 indisponivel: checkout fora do ar em producao.
- Seguranca: possivel vazamento de dados.
- Banco lento: locks e impacto em pedidos.
- Bug controlado: erro visual com contorno.

Ao avaliar um chamado, a aplicacao salva o resultado no SQLite e atualiza indicadores da operacao. Isso permite mostrar nao apenas a decisao individual, mas tambem uma visao de historico e estatisticas.

## 11. Resultados

O prototipo atende aos objetivos propostos:

- Funciona como aplicacao full-stack.
- Possui backend, frontend e banco de dados.
- Explica as decisoes por regras disparadas.
- Permite rodar localmente ou com Docker.
- Inclui testes automatizados do backend.
- Possui interface visual adequada para apresentacao.

O principal ponto forte e a explicabilidade: cada decisao exibe os motivos que levaram ao score final. Isso e importante em ambientes corporativos, nos quais decisoes automatizadas precisam ser compreendidas e auditadas.

## 12. Limitacoes

O sistema usa pesos definidos manualmente. Em um ambiente real, esses pesos deveriam ser calibrados com dados historicos, entrevistas com especialistas e validacao operacional. Tambem seria possivel adicionar regras por perfil de negocio, diferentes SLAs por cliente e integracao com ferramentas como Jira, ServiceNow ou GLPI.

## 13. Conclusao

Sistemas baseados em regras continuam relevantes em problemas nos quais explicabilidade, controle e padronizacao sao importantes. O RuleDesk demonstra que IA simbolica pode ser aplicada de forma pratica em Engenharia de Software, especialmente em fluxos de suporte, incidentes e operacoes.

O projeto mostra que uma aplicacao inteligente nao precisa necessariamente treinar uma rede neural. Quando o conhecimento do dominio e claro, regras bem definidas podem gerar decisoes uteis, rapidas e justificaveis.

## 14. Referencias

- Russell, S.; Norvig, P. Artificial Intelligence: A Modern Approach, 4th US ed. Site oficial: https://aima.cs.berkeley.edu/
- CLIPS. A Tool for Building Expert Systems. Site oficial: https://www.clipsrules.net/
- Apache KIE / Drools. Documentacao e ecossistema de regras de negocio: https://kie.apache.org/
- NIST. SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management. https://csrc.nist.gov/pubs/sp/800/61/r3/final
- Forgy, C. L. Rete: A Fast Algorithm for the Many Pattern/Many Object Pattern Match Problem. Artificial Intelligence, 1982.
