---
title: "Event Hooks no Hermes Agent: Os 4 Sistemas de Governança, Bloqueio e Auditoria em Tempo Real"
date: "2026-11-26"
lastmod: "2026-11-26"
summary: "Entenda como os 4 sistemas de Event Hooks do Hermes Agent (Gateway, Plugin, Shell e Outbound Webhooks) permitem auditar ações, bloquear comandos perigosos com fail-closed e integrar agentes de IA à governança corporativa em tempo real."
tags: ["Agentes de IA", "Hermes Agent", "Event Hooks", "Governança", "Segurança", "Auditoria"]
keywords: ["Event Hooks Hermes Agent", "Shell Hooks pre_tool_call", "fail-closed IA", "Outbound Webhooks HMAC", "governança agentes de IA"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/event-hooks-hermes-agent-governanca-auditoria-bloqueio-tempo-real.jpg"
draft: false
---

> **Em resumo:** Os **Event Hooks** do Hermes Agent formam uma arquitetura de quatro camadas — **Gateway Hooks**, **Plugin Hooks**, **Shell Hooks** e **Outbound Webhooks** — que interceptam o ciclo de vida do agente em tempo real.[1] Com eles, empresas podem bloquear chamadas de ferramentas perigosas antes da execução (`pre_tool_call` com `fail_closed: true` ou código de saída `2`), injetar contexto dinâmico antes da inferência (`pre_llm_call`), executar checklists automáticos na inicialização (`BOOT.md`) e enviar eventos assinados por HMAC-SHA256 para sistemas externos sem travar a conversa.[1]

---

## O fim da "caixa-preta": por que empresários travam na hora de colocar agentes em produção

Para quem gerencia operações reais — seja uma equipe comercial, um setor financeiro ou uma infraestrutura de servidores — o maior receio ao adotar um agente autônomo de IA não é a inteligência do modelo, mas a **previsibilidade**.

Sem pontos de interceptação determinísticos, o gestor fica refém de torcer para que o *prompt* seja obedecido. Basta uma instrução ambígua ou uma injeção de texto externa para que um agente tente apagar arquivos críticos, vazar dados de clientes ou rodar um loop infinito de ferramentas.

O Hermes Agent resolve esse impasse com **quatro sistemas de Event Hooks** que operam fora da boa vontade do modelo de linguagem: são regras de código, scripts de shell e notificações HTTP executadas diretamente pelo runtime nos pontos exatos do ciclo de vida.[1] Além disso, erros em callbacks de hooks são isolados e registrados em log, evitando que uma falha de observabilidade derrube o agente principal.[1]

```
+-----------------------------------------------------------------------------+
|                CICLO DE VIDA DO HERMES AGENT & EVENT HOOKS                  |
+-----------------------------------------------------------------------------+
  [ Mensagem / Gateway ]
           |
           v
  1. pre_llm_call (Shell / Plugin) ----> Pode injetar contexto ou BLOQUEAR turno
           |
           v
  [ Decisão do Modelo (LLM) ]
           |
           v
  2. pre_tool_call (Shell / Plugin) ---> Pode modificar args, pedir aprovação
           |                             ou BLOQUEAR (exit 2 / fail_closed)
           v
  [ Execução da Ferramenta ]
           |
           v
  3. post_tool_call (Shell / Plugin) --> Auto-formata arquivos, registra logs
           |
           +---> 4. Gateway Hooks (HOOK.yaml) & Outbound Webhooks (HMAC-SHA256)
                    Notificam Slack/Telegram/CI em segundo plano (fire-and-forget)
+-----------------------------------------------------------------------------+
```

---

## Os 4 sistemas de Event Hooks frente a frente

Cada camada de hook no Hermes Agent atende a um nível distinto de controle, linguagem e isolamento.[1]

| Dimensão | Gateway Hooks | Plugin Hooks | Shell Hooks | Outbound Webhooks |
|---|---|---|---|---|
| **Onde é declarado** | `HOOK.yaml` + `handler.py` em `~/.hermes/hooks/`[1] | `ctx.register_hook()` no `plugin.yaml`[1] | Bloco `hooks:` no `config.yaml` do perfil[1] | Lista `hooks.outbound:` no `config.yaml`[1] |
| **Onde executa** | Apenas no Gateway (Telegram, WhatsApp, Slack, Teams, Discord)[1] | CLI + Gateway[1] | CLI + Gateway + Desktop/TUI/Dashboard[1] | CLI + Gateway[1] |
| **Linguagem** | Python (`def` ou `async def`)[1] | Python[1] | Qualquer linguagem (Bash, Python, binário Go, etc.)[1] | HTTP POST JSON para URL externa[1] |
| **Pode bloquear ferramenta?** | Não[1] | Sim (`pre_tool_call`)[1] | Sim (`pre_tool_call`)[1] | Não (apenas notificação *fire-and-forget*)[1] |
| **Pode injetar contexto no LLM?** | Não[1] | Sim (`pre_llm_call`)[1] | Sim (`pre_llm_call`)[1] | Não[1] |
| **Isolamento** | *In-process* no processo do Gateway[1] | *In-process*[1] | Subprocesso isolado por execução[1] | Fila assíncrona em thread separada[1] |
| **Modelo de consentimento** | Implícito por diretório (*trusted-by-placement*)[1] | Explícito (`plugins.enabled`)[1] | Prompt de primeiro uso por par `(evento, comando)`[1] | Sem prompt de consentimento (desativado em `HERMES_SAFE_MODE=1`)[1] |

---

## 1. Shell Hooks: travas corporativas sem precisar escrever plugins em Python

Os **Shell Hooks** são a via mais rápida para equipes de operações criarem guardrails rígidos. Declarados no `config.yaml` do perfil, eles disparam qualquer script executável (Bash, Python, binário compilado) como subprocesso, enviando um payload JSON via `stdin` e lendo a decisão via `stdout`.[1]

Dois mecanismos tornam os Shell Hooks especialmente poderosos para ambientes corporativos:

1. **Bloqueio instantâneo com Exit Code 2:** compatível com o padrão de Claude Code e Cursor, qualquer script em `pre_tool_call` que retorne código de saída `2` bloqueia imediatamente a ferramenta, mesmo sem emitir JSON estruturado — usando o JSON de bloqueio, os primeiros 400 caracteres de `stderr` ou uma mensagem padrão.[1]
2. **Modo `fail_closed: true` (Falha Segura):** por padrão, hooks operam em *fail-open* (se o script travar ou der timeout, o agente prossegue para não parar a operação).[1] Para verificações de segurança — como um scanner de segredos ou bloqueio de comandos destrutivos — ativar `fail_closed: true` inverte essa lógica: se o script não for encontrado, der timeout ou retornar saída inválida, o Hermes bloqueia a ferramenta automaticamente.[1]

| Cenário de Falha | Comportamento Padrão (`fail_open`) | Com `fail_closed: true` |
|---|---|---|
| Comando não encontrado / sem permissão | Loga aviso e prossegue[1] | **Bloqueia a chamada**[1] |
| Timeout excedido | Loga aviso e prossegue[1] | **Bloqueia a chamada**[1] |
| Saída não-JSON (ex.: *stack trace*) | Loga aviso e prossegue[1] | **Bloqueia a chamada**[1] |
| JSON vazio válido (`{}`) | Prossegue[1] | Prossegue[1] |

Além de bloquear (`action: "block"`), um Shell Hook em `pre_tool_call` também pode **reescrever argumentos** (`action: "modify"`) antes da execução ou **escalar para aprovação humana** (`action: "approve"`).[1] No evento `pre_llm_call`, pode injetar contexto atualizado (como `git status` ou regras do dia) ou bloquear o turno antes mesmo de gastar tokens com a API do modelo.[1]

```yaml
# Exemplo prático no ~/.hermes/config.yaml
hooks:
  pre_tool_call:
    - matcher: "terminal|write_file|patch"
      command: "~/.hermes/agent-hooks/secret-scan.sh"
      timeout: 10
      fail_closed: true
```

---

## 2. Gateway Hooks & o padrão `BOOT.md`: vigilância automática na nuvem

Quando o Hermes roda 24/7 em uma VPS atendendo equipes no Telegram, WhatsApp, Discord, Slack ou Microsoft Teams, os **Gateway Hooks** (`~/.hermes/hooks/<nome>/HOOK.yaml` + `handler.py`) monitoram eventos de conversa sem bloquear o fluxo principal.[1]

Entre os eventos disponíveis estão `gateway:startup`, `session:start`, `session:end`, `session:reset`, `session:compress`, `agent:start`, `agent:step` (a cada iteração de ferramenta), `agent:end`, `reaction:added`/`reaction:removed` (no Slack) e o curinga `command:*` para auditar todos os comandos de barra.[1]

Um caso de uso consagrado para gestores é o padrão **`BOOT.md`**: um hook conectado ao `gateway:startup` lê um checklist em linguagem natural em `~/.hermes/BOOT.md` toda vez que o gateway sobe, verifica se algum *cron job* noturno falhou ou se há erros nos logs de deploy e envia um resumo ao canal de operações — respondendo apenas `[SILENT]` quando está tudo saudável para evitar ruído.[1]

---

## 3. Plugin Hooks: interceptação profunda e seções cache-safe

Para extensões distribuídas em equipe ou publicadas no catálogo, os **Plugin Hooks** registram callbacks via `ctx.register_hook()` e cobrem todo o espectro do runtime: `pre_tool_call`, `post_tool_call`, `pre_llm_call`, `post_llm_call`, `pre_verify`, `subagent_start`, `subagent_stop`, eventos de aprovação humana (`pre_approval_request`, `post_approval_response`), transcrição de áudio (`pre_transcription`) e ciclo de vida do Kanban multi-agente (`kanban_task_claimed`, `kanban_task_completed`, `kanban_task_blocked`).[1]

Para evitar que injeções repetitivas destruam o *prompt caching* dos provedores de LLM, o Hermes oferece ainda `ctx.register_system_prompt_section(..., position="after_memory")`, garantindo regras corporativas fixas e ordenadas sem invalidar o cache a cada turno.[1] Callbacks com limite de tempo (`plugins.hook_callback_timeout`, padrão de 30 segundos) são encerrados se travarem: em `pre_tool_call`, o timeout falha de forma fechada (*fail-closed*) e bloqueia a ferramenta; nos demais observadores, falha aberto (*fail-open*) para preservar a disponibilidade.[1]

---

## 4. Outbound Webhooks: telemetria assinada sem latência no agente

Enquanto webhooks de entrada acordam o agente quando algo muda fora dele, os **Outbound Webhooks** (`hooks.outbound:` no `config.yaml`) notificam sistemas externos — como pipelines de CI/CD, painéis de BI, SIEMs de segurança ou outra instância do Hermes — sempre que ocorre um evento interno.[1]

Sua arquitetura foi desenhada para produção:

- **Zero impacto na latência:** os eventos são serializados e enfileirados instantaneamente em uma thread separada (*fire-and-forget*), garantindo que um servidor externo lento ou fora do ar nunca trave o agente.[1]
- **Autenticação HMAC-SHA256:** usando `secret_env` (apontando para uma variável no `~/.hermes/.env`), cada requisição inclui o cabeçalho `X-Hermes-Signature-256`, além de `delivery_id` e `timestamp` dentro do corpo assinado para proteção contra ataques de repetição (*replay attacks*).[1]
- **Multi-perfil nativo:** o campo `profile` identifica qual perfil departamental disparou o evento, permitindo que um único gateway multiplexado alimente painéis distintos.[1]

```yaml
# Exemplo de Outbound Webhook assinado no ~/.hermes/config.yaml
hooks:
  outbound:
    - name: auditoria-corporativa
      url: https://siem.suaempresa.com.br/hermes-events
      events: [pre_tool_call, on_session_end, subagent_stop]
      matcher: "terminal|delegate_task"
      secret_env: HERMES_OUTBOUND_WEBHOOK_SECRET
      timeout: 10
```

---

## Como auditar e testar suas travas antes de ir para produção

O Hermes oferece comandos nativos na CLI para inspecionar e validar hooks configurados sem precisar esperar um incidente real:[1]

- `hermes hooks list` — lista todos os Shell Hooks e Outbound Webhooks configurados no perfil ativo, indicando inclusive alvos sem assinatura (`UNSIGNED`).[1]
- `hermes hooks test <evento>` — testa o comportamento do hook localmente e exibe exatamente o payload normalizado (`parsed`) que o dispatcher receberia.[1]

---

## Conclusão

Colocar agentes de IA para operar rotinas reais de negócio exige a mesma disciplina de engenharia aplicada a servidores e sistemas financeiros: **observabilidade, travas determinísticas e separação entre quem executa e quem audita**. Os quatro sistemas de **Event Hooks** do Hermes Agent entregam exatamente essa camada de controle, permitindo que você saia dos experimentos isolados e opere agentes confiáveis 24/7.[1]

Para aprofundar sua arquitetura de agentes autônomos em produção com foco em resultados reais de negócio, conheça a comunidade **Inteligência Agêntica** em [https://inteligenciaagentica.com.br](https://inteligenciaagentica.com.br).

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks — Event Hooks | Hermes Agent - Nous Research
