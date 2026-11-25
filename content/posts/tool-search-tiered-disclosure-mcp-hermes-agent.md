---
title: "Tool Search e Tiered Disclosure: Como Conectar 3.000 Ferramentas MCP Sem Estourar o Contexto nem a Fatura"
date: "2026-11-25"
lastmod: "2026-11-25"
summary: "Entenda como o Tool Search e o Tiered Disclosure do Hermes Agent substituem milhares de schemas JSON por três ferramentas-ponte (tool_search, tool_describe e tool_call), usando busca BM25 e degradação inteligente em 3 camadas para escalar servidores MCP e Connectors sem desperdiçar tokens."
tags: ["Agentes de IA", "MCP", "Tool Search", "FinOps", "Hermes Agent", "Negócios"]
keywords: ["tool search hermes agent", "tiered disclosure mcp", "reduzir tokens mcp", "tool_search tool_describe tool_call", "inteligencia agentica"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/tool-search-tiered-disclosure-mcp-hermes-agent.jpg"
draft: false
---

> **Em resumo:** Conectar dezenas de servidores MCP e plugins a um agente corporativo costuma gerar um gargalo silencioso: os schemas JSON de todas as ferramentas são enviados em cada turno da conversa, consumindo dezenas de milhares de tokens antes mesmo do usuário fazer uma pergunta.[1] Com o **Tool Search** (`tool_search`, `tool_describe`, `tool_call`) e o **Tiered Disclosure** do Hermes Agent, o agente mantém apenas as ferramentas essenciais carregadas diretamente e descobre, descreve e invoca ferramentas MCP, plugins e Connectors remotos sob demanda — reduzindo drasticamente o custo de contexto mesmo em catálogos com milhares de endpoints.[1][3]

---

## O Gargalo Oculto das Empresas que Escalam Agentes com MCP

Quando uma empresa começa a integrar seu agente de IA ao mundo real via **MCP (Model Context Protocol)** — conectando GitHub, Slack, CRM, banco de dados, sistema de tickets e infraestrutura em nuvem — o primeiro protótipo funciona perfeitamente.[3]

O problema aparece na escala. Cada ferramenta MCP exposta ao modelo carrega um schema JSON com nome, descrição e definição de parâmetros.[1] Em servidores corporativos amplos, esse peso explode rapidamente: segundo a documentação oficial do Hermes Agent, apenas a superfície plana da API do servidor MCP da Cloudflare reúne cerca de **3.300 ferramentas**, cujos nomes sozinhos já consomem aproximadamente **32.000 tokens**.[1]

Enviar todos esses schemas em **todo turno de conversa** gera três impactos diretos na operação:

1. **Custo inflado por mensagem:** o prefixo de ferramentas é faturado repetidamente a cada interação.[1]
2. **Degradação de precisão:** modelos perdem foco quando precisam escolher entre centenas de definições concorrentes.[1]
3. **Estouro de janela de contexto:** sobra menos espaço útil para documentos, histórico de atendimento e código.[1]

---

## Como Funciona o Tool Search no Hermes Agent

O **Tool Search** é a camada opcional de divulgação progressiva (*progressive disclosure*) do Hermes Agent para resolver esse problema.[1] Ativado por padrão (`enabled: auto`), ele mantém o conjunto central de ferramentas de trabalho carregado diretamente — como `terminal`, `read_file`, `write_file`, `patch`, `search_files`, `memory`, `web_search`, `web_extract`, `execute_code` e `delegate_task` — e substitui ferramentas MCP, plugins não centrais e ferramentas frias listadas em `tools.tool_search.defer` por apenas **três ferramentas-ponte**:[1]

- **`tool_search(queries, limit?)`**: pesquisa o catálogo de ferramentas adiadas (*deferred*) aceitando múltiplas consultas em paralelo.[1]
- **`tool_describe(names)`**: carrega o schema completo de parâmetros apenas das ferramentas selecionadas.[1]
- **`tool_call(calls)`**: invoca a ferramenta adiada após o carregamento do schema.[1]

```text
Fluxo de Descoberta e Execução (Tool Search)
───────────────────────────────────────────────────────────────────
[1] Usuário pede: "Abra uma issue no GitHub e avise no Slack"
        │
        ▼
[2] Modelo chama: tool_search(["create github issue", "send slack"])
        │  └── Índice BM25 + Snowball stemming + regra do token raro
        ▼
[3] Modelo chama: tool_describe(["mcp_github_create_issue", "mcp_slack_post"])
        │  └── Carrega APENAS os 2 schemas JSON necessários no turno
        ▼
[4] Modelo chama: tool_call([{name: "mcp_github_create_issue", ...}])
        │  └── Hermes "desembrulha" a ponte e executa hooks, aprovações
        │      e logs com o nome REAL da ferramenta subjacente
        ▼
[5] Resultado retornado ao usuário sem poluir o prompt com 500 schemas
```

Um detalhe arquitetural importante para auditoria e segurança: ao executar `tool_call`, o Hermes **desembrulha a ponte** e despacha a ferramenta real.[1] Isso significa que *hooks* pré e pós-execução, *guardrails*, pedidos de aprovação humana e o feed de atividades no CLI ou Gateway registram o nome verdadeiro da ferramenta (ex.: `mcp_github_create_issue`), e não um genérico `tool_call`.[1]

---

## Tiered Disclosure: Degradação Inteligente em 3 Camadas

Para equilibrar economia de tokens e taxa de acerto do modelo, o Hermes não esconde tudo cegamente. Ele aplica um sistema de **divulgação em camadas (*Tiered Disclosure*)** recalculado dinamicamente a cada montagem da lista de ferramentas, respeitando o orçamento `min(threshold_pct% do contexto, listing_max_tokens)`:[1]

| Camada (Tier) | Condição de Ativação | O que o Modelo Enxerga | Impacto Operacional |
|---|---|---|---|
| **Tier 0** | Nenhuma ferramenta adiada (*deferred*) | Todas as ferramentas carregadas diretamente (*eager*), sem ponte.[1] | Zero latência extra; ideal para conjuntos pequenos.[1] |
| **Tier 1** | A listagem do catálogo cabe no orçamento configurado | Ponte + manifesto estilo *skills* (nome + descrição curta de até 60 caracteres por ferramenta, agrupados por servidor MCP).[1] | O modelo já vê o nome exato na listagem e pode pular `tool_search`, indo direto para `tool_describe`.[1] |
| **Tier 2** | Mesmo apenas os nomes excedem o orçamento (ex.: Cloudflare com ~3.300 tools) | Ponte + resumo de uma linha por servidor (nome do servidor + contagem de ferramentas).[1] | Economia extrema de contexto; descoberta feita estritamente via `tool_search`.[1] |

A degradação entre os tiers ocorre **por servidor**.[1] Se a empresa conecta um servidor gigante como Cloudflare junto com um servidor enxuto como Linear, apenas o servidor gigante colapsa para uma linha de resumo, enquanto o servidor menor preserva a listagem detalhada de suas ferramentas.[1]

Por que manter essa listagem no Tier 1? Testes comparativos citados na documentação mostraram que, sem visibilidade mínima, modelos tendem a recorrer a ferramentas visíveis (como rodar `gh` no terminal) ou afirmar que uma capacidade não existe em vez de pesquisar.[1] Com o manifesto resumido, a taxa de sucesso iguala o carregamento completo (*eager*) custando muito menos tokens.[1]

---

## Motor de Busca BM25, Stemming e Regra do Token Mais Raro

Internamente, o `tool_search` não faz uma busca ingênua por substring. Ele executa um motor **BM25** sobre o nome da ferramenta, o servidor de origem, a descrição e os nomes dos parâmetros, aplicando **Snowball stemming** (assim, buscar `"issues"` encontra `create_issue`).[1]

Dois mecanismos evitam resultados inúteis que fazem o agente entrar em loops de tentativas:

- **Regra do token mais raro (*rarest-token rule*):** uma ferramenta só entra nos resultados se contiver o termo mais específico da consulta (ex.: `gmail`, `github` ou `incident`, e não verbos genéricos como `send` ou `create`).[1] Se o termo mais raro não existir no catálogo, o retorno traz o grupo vazio junto com a lista de servidores conectados (`available_sources`) para o agente corrigir a busca.[1]
- **Piso de relevância (*relevance floor*):** em consultas com quatro ou mais termos respondíveis, a ferramenta precisa combinar pelo menos metade deles para ser exibida — evitando falsos positivos por coincidência de uma única palavra.[1]

Além disso, o catálogo é **sem estado entre turnos** (*stateless*) e **restrito aos toolsets da sessão**: um subagente, worker do Kanban ou sessão de gateway com permissões limitadas nunca consegue usar a ponte para descobrir ou invocar ferramentas fora do seu escopo.[1]

---

## Connectors Remotos e Múltiplas Contas Corporativas

A mesma ponte `tool_search` / `tool_describe` / `tool_call` também acessa **Connectors** — ferramentas hospedadas no **Nous Tool Gateway** (identificadas pelo prefixo `connectors__<connector>__<tool>`).[1][3]

Na prática corporativa, isso traz duas vantagens imediatas:

1. **Busca unificada:** ferramentas locais (MCPs na sua VPS) e conectores remotos passam pelo mesmo ranqueamento BM25 em uma única chamada, com *timeout* de 30 segundos para chamadas ao gateway (degradando graciosamente para resultados locais se o gateway estiver indisponível).[1]
2. **Múltiplas contas por aplicativo (`connector_alias`):** quando a empresa vincula duas ou mais contas do mesmo serviço (por exemplo, `home` e `work`), as ferramentas passam a expor o parâmetro `connector_alias` para direcionar exatamente em qual conta a ação deve ser executada.[1]

---

## Configuração Recomendada e Trade-offs Reais

No arquivo `~/.hermes/config.yaml`, o comportamento pode ser ajustado com precisão conforme o perfil de custo e latência da operação:[1]

```yaml
tools:
  tool_search:
    enabled: auto            # auto (padrão), on ou off
    threshold_pct: 5         # orçamento da listagem (% da janela do modelo)
    search_default_limit: 5  # resultados padrão por query
    max_search_limit: 25     # limite máximo por query
    listing: auto            # auto, on ou off para o manifesto embutido
    listing_max_tokens: 4000 # teto absoluto de tokens para a listagem
    defer:                   # substitui a lista padrão; [] mantém tudo eager
      - computer_use
      - session_search
      - image_generate
      - todo_list
      - process_manage
      - cronjob_manage
      - text_to_speech
      - manage_connections
      - manage_catalog
```

### Quando usar e quando desativar (`enabled: off`)

Como toda arquitetura de divulgação progressiva, existem *trade-offs* reais que o gestor técnico precisa considerar:[1]

| Cenário | Recomendação | Motivo |
|---|---|---|
| **Múltiplos MCPs / catálogos médios e grandes** | Manter `enabled: auto` | Economiza milhares de tokens por turno e evita poluição da janela de contexto.[1] |
| **Conjunto pequeno (ex.: 5 a 10 tools fixas)** | Avaliar `enabled: off` | Evita o *round trip* extra (`tool_describe` → `tool_call`) em ferramentas frias e mantém tudo no prefixo de *prompt cache*.[1] |
| **Modelos muito pequenos / locais** | Testar acurácia antes de escalar | Modelos menores formulam queries de busca piores; dados da Anthropic citados na doc mostram salto de 49% → 74% no Opus 4 com tool search, mas ainda com margem de falha de recuperação.[1] |
| **Edições frequentes de toolset no meio da sessão** | Evitar em produção | Adicionar/remover ferramentas no meio da conversa altera o contador da ponte e invalida o *prompt cache*.[1] |

---

## Conclusão: Escala Sem Desperdício

O avanço recente do Hermes Agent — que acaba de receber a release estável **v0.23.4** com 229 PRs consolidados, suporte aos modelos Gemini 4 e melhorias contínuas de gateway e catálogo — reforça um princípio claro de engenharia em produção: **agentes empresariais não quebram por falta de ferramentas, mas por excesso de contexto mal gerenciado**.[1][2]

Adotar o **Tool Search** com **Tiered Disclosure** permite conectar toda a pilha de sistemas da empresa via MCP e Connectors pagando apenas pelos schemas que o agente realmente utiliza em cada tarefa.[1][3]

Se você quer estruturar agentes autônomos em produção com controle real de custos, governança de ferramentas e arquitetura validada para negócios, conheça a comunidade **[Inteligência Agêntica](https://inteligenciaagentica.com.br)**.

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search — Tool Search | Hermes Agent
[2] https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.4 — Release Hermes Agent v0.23.4 | GitHub
[3] https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp — MCP (Model Context Protocol) | Hermes Agent
