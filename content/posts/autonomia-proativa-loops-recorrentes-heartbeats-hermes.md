---
title: "Autonomia Proativa: Como /loop e /heartbeat Eliminam a Babá de IA no Hermes Agent"
date: "2026-11-18"
lastmod: "2026-11-18"
summary: "Veja como /loop (laços recorrentes com auto-backoff exponencial) e /heartbeat (batimento cardíaco de sessão) trabalham dentro de uma mesma conversa para monitorar deployments, acompanhar filas e manter vigilância autônoma — sem pedir \"keep going\" a cada turno e com o prompt cache preservado."
tags: ["Agentes de IA", "Hermes Agent", "Autonomia", "Automação", "VPS", "Cron Jobs"]
keywords: ["/loop hermes agent", "/heartbeat hermes agent", "recurring loops agent", "session heartbeat autonomia", "auto-backoff hermes", "proactive monitoring agents"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/autonomia-proativa-loops-recorrentes-heartbeats-hermes.jpg"
draft: false
---

> **Resposta Rápida (Answer-First / GEO):**
> O Hermes Agent oferece dois comandos internos para autonomia dentro da conversa: **`/loop`** repete um prompt em intervalos definidos ou numa cadência auto-paceada com backoff; **`/heartbeat`** executa uma instrução recorrente quando a sessão está ociosa. Cada wakeup é um turno real do agente, portanto pode consumir tokens; a cadência auto-paceada reduz chamadas repetidas quando a resposta não muda. Os wakeups preservam a estrutura da conversa e o prompt cache.[1][2]

---

## O Problema: "Keep Going" Não Escala

Quando um gestor ou desenvolvedor delega uma tarefa complexa ao Hermes — auditar 80 pull requests, acompanhar um deploy de 40 minutos ou monitorar uma fila de mensagens — o padrão convencional exige intervenção humana a cada turno: *"e aí, terminou?"*, *"continue"*, *"parece que travou"*. Isso funciona para uma pergunta. Não escala para automação operacional real.

A inteligência agêntica de produção exige que o agente **continue sozinho**, **perceba mudanças de estado** e **informe quando há algo relevante**. O `/loop` e o `/heartbeat` habilitam reexecuções dentro de uma sessão contextualizada. Como cada wakeup é um turno real do agente, escolha a frequência considerando custo e latência.[1][2]

---

## /loop: Laços Recorrentes com Detecção de Mudança

O `/loop` é o comando de **vigilância orientada a.timer** dentro de uma sessão Hermes. Ele agenda um prompt para reexecutar em intervalos regulares, com duas modalidades de cadência.[1]

### Modo Fixo

```
/loop 5m check the deploy status and ping me the moment it finishes
```

O agente recebe o wakeup a cada 5 minutos (ou no intervalo definido: 30s, 2h, 1d). A cada tick, Hermes lê o estado atual — resultado de CI, conteúdo de fila, resposta de API — e decide se há algo novo a reportar. Se nada mudou, mantém silêncio. Se mudou, envia o resultado para o chat.[1]

### Modo Auto-Paceado (Self-Paced)

```
/loop poll GitHub Actions job #42 and tell me when it completes
```

Quando você omite o intervalo, o Hermes **define a cadência sozinho**: começa no piso (1 minuto), dobra a cada wakeup se a resposta não mudou (2m → 4m → 8m → 15m), e reseta instantaneamente para o piso no momento em que detecta uma diferença. Isso elimina o custo de polling agressivo em sistemas que mudam raramente.[1]

```
↻ Loop set (every 5m): check the deploy status...
↻ Loop active · 2 runs · next 00:04:12
```

### Limites Configuráveis

Em `config.yaml`, você pode ajustar os pisos e tetos:

```yaml
loops:
  min_interval_seconds: 30      # piso mínimo (impede spam)
  max_ticks: 100               # backstop de segurança (0 = ilimitado)
  self_paced_floor_seconds: 60 # cadência inicial do auto-pace
  self_paced_ceiling_seconds: 900  # máximo backoff (15 min)
```

### Diferença Crucial: /loop vs /goal

| | `/loop` | `/goal` |
|---|---------|---------|
| **Gatilho** | Timer (intervalo fixo ou auto-pace) | Julgamento do judge após cada turno |
| **Vive em** | Sua sessão atual | Sua sessão atual |
| **Termina quando** | Condição de stop / limite de ticks / você | Meta atingida / orçamento / você |
| **Melhor para** | Polling, monitoramento, re-execuções periódicas | Iteração até resultado definido |

Se a tarefa tem definição de "pronto" — *"corrigir todos os testes"* — use `/goal`. Se a tarefa é monitorar algo que muda por conta própria — *"avise quando o deploy terminar"* — use `/loop`.[1][3]

---

## /heartbeat: A Sentinela do Idle

O `/heartbeat` é o comando de **vigilância passiva enquanto a sessão está ociosa**. Diferente do `/loop`, que agenda re-execuções ativas, o heartbeat é uma instrução que o agente verifica **somente quando ninguém mais está digitando**.[2]

### Uso Típico

```
/heartbeat every 10m Check the deployment and report meaningful changes
```

O agente mantém essa instrução em memória e, a cada 10 minutos de ociosidade, executa a verificação. Não interrompe trabalho ativo — se você está no meio de uma sessão, o heartbeat espera. Se a sessão está aberta no Telegram enquanto você está off-line, o heartbeat continua disparando e enviando replies para o chat.[2]

```
/hb every 10m Check for error spikes in the last hour
/heartbeat status   → mostra intervalo e próximo tick
/heartbeat pause    → suspende sem perder
/heartbeat resume   → retoma (reancora o timer)
/heartbeat clear    → remove definitivamente
```

### Heartbeat vs Cron: Qual Usar?

| | `/heartbeat` | `hermes cron` |
|---|-------------|--------------|
| **Executa em** | Esta conversa — contexto completo | Sessão isolada por tick |
| **Sobrevive a reinício** | Sim (SessionDB mantém) | Sim (scheduler durável) |
| **Quantos por sessão** | Um | Ilimitados |
| **Melhor para** | *"Fique de olho em X enquanto trabalhamos aqui"* | Tarefas auto-contidas, relatórios, watchdogs |

A regra prática: se a verificação precisa do contexto da conversa atual, use `/heartbeat`. Se é um trabalho auto-contido que deve rodar de verdade mesmo quando ninguém está logado, use cron.[2][3]

---

## Arquitetura Técnica: Por Que É Seguro e Barato

### Cada Wakeup É Um Turno de Usuário

Internamente, `/loop` e `/heartbeat` injetam uma mensagem com role `user` no histórico da sessão — **exatamente como se você tivesse digitado**. Isso significa:

- O prompt cache se mantém intacto (a sequência de prefixação do sistema não é modificada).
- O agente vê o estado atual como se você tivesse acabado de perguntar.
- Não há mutação de system prompt, não há toolset swap, não há efeitos colaterais no cache de contexto.[1][2]

### Missed Ticks Coalescem

Se a sessão estava ocupada (ou o processo não estava rodando) durante vários intervalos, **você recebe apenas um wakeup**, não uma fila de alertas acumulados. O timer se reancora a cada disparo. Isso previne a fadiga de notificações.[2]

### User Messages Win

Uma mensagem que o usuário digita **sempre tem prioridade** sobre o heartbeat em espera. A mensagem entra na fila, é processada primeiro, e o heartbeat espera o próximo ciclo de ociosidade.[2]

### Gateway Recovery

Se o gateway cai e volta, heartbeats ativos são restaurados com a sessão persistente e o thread routing atual. Sessões pausadas ou limpas não são restauradas — a recuperação é limpa.[2]

---

## Casos de Uso Corporativos Reais

### 1. Acompanhamento de Deploy de 40 Minutos

```
/goal Deploy our API to staging and run smoke tests

/loop 2m poll https://ci.company.com/job/api-deploy/status
```

O `/goal` executa o trabalho real. O `/loop` consulta o status do pipeline de CI no intervalo configurado; cada wakeup é um turno do agente e pode gerar custo, então ajuste a cadência ao ritmo esperado do job. Quando o estado muda, o agente pode reportar o resultado.[1]

### 2. Monitoramento de Fila de Mensagens (Telegram/WhatsApp)

```
/heartbeat every 15m Scan the support inbox for urgent tickets and escalate to @manager
```

Enquanto o agente trabalha em outras demandas na mesma sessão, o heartbeat verifica a caixa de entrada a cada 15 minutos. Só envia mensagem quando encontra tickets classificados como urgentes.[2]

### 3. Polling de Status Durante Sessão de Trabalho

```
/loop poll the queue depth endpoint and ping me if it exceeds 500
```

O `/loop` poll o CI com a cadência escolhida, e cada wakeup é um turno real do agente que pode consumir tokens; dimensione o intervalo considerando custo e frequência das mudanças.[1]

### 4. Retry Automático com Backoff Exponencial

```
/loop Check if the ML model endpoint is responding with 200
```

Cada wakeup do `/loop` é um turno real do agente, não um polling sem LLM. A cadência auto-paceada reduz a frequência quando as respostas não mudam, mas não elimina o custo dos turnos executados.[1]

---

## Diagrama de Arquitetura: Loop vs Heartbeat vs Cron

> **Observação:** Sessões do `/loop` e `/heartbeat` funcionam com a janela do Hermes aberta ou pelo gateway enquanto esse processo estiver ativo; jobs de cron são duráveis e independentes da sessão interativa.[2][3]

```
┌─────────────────────────────────────────────────────────┐
│                  HERMES SESSION (ativa)                  │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  /goal   │    │    /loop      │    │ /heartbeat   │ │
│  │ Ralph    │    │ Timer-driven  │    │ Idle-sentry  │ │
│  │ Loop     │    │ Wakeup       │    │ Wakeup       │ │
│  └────┬─────┘    └──────┬───────┘    └──────┬───────┘ │
│       │                 │                    │         │
│       │  judge verdict  │  interval timer    │ idle    │
│       │  after turn     │  (fixed or         │ timer   │
│       │                 │  self-paced)       │         │
│       ▼                 ▼                    ▼         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Same conversation context • Same session store   │ │
│  │  User messages always win over pending wakeups   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
              │                         │
              ▼                         ▼
     ┌──────────────────┐    ┌──────────────────────────┐
     │   hermes cron    │    │ External Systems          │
     │ Separate session │    │ Deploy / CI / Queue       │
     │ per fire         │    │ Webhook / API              │
     │ Survives restart │    │                            │
     └──────────────────┘    └────────────────────────────┘
```

---

## Comparativo: Autonomia em Três Camadas

| Característica | `/loop` | `/heartbeat` | `hermes cron` |
|---|---|---|---|
| Contexto da conversa | ✅ Sim | ✅ Sim | ❌ Não (sessão isolada) |
| Executa em ociosidade | ✅ Wakeup no próximo poll idle | ✅ Sim | ✅ Sim |
| Cadência fixa | ✅ Intervalo configurável | ✅ Intervalo configurável | ✅ Expressão cron |
| Auto-backoff | ✅ Sim | ❌ Não | ❌ Não |
| Limite de ticks | ✅ configurável | ❌ N/A | ✅ repeat count |
| Intersecção com `/goal` | ✅ Conflito (goal vence) | ✅ Coexiste | ✅ Paralelo |
| Sobrevive a reinício | ✅ SessionDB | ✅ SessionDB | ✅ Scheduler durável |
| Melhores para | Polling, monitoramento ativo | Verificações passivas | Tarefas auto-contidas |

---

## Exemplo Prático: Monitoramento de Deploy Completo

```bash
# Exemplo de combinações na mesma sessão
/goal Deploy service X to production and run smoke tests
/loop 2m check https://ci.company.com/api/v1/jobs/deploy-x/status
/heartbeat every 30m Verify all prod services return HTTP 200
```

Durante uma sessão com um `/goal` ativo, wakeups de `/loop` ficam deferidos até o goal terminar, pausar ou aguardar; cron jobs rodam em sessões próprias. Isso significa que loops e heartbeats não formam vários agentes executando paralelamente dentro da mesma sessão.[1][2][3]

---

## Conclusão

Autonomia real não é "ligar e ir embora". É construir um sistema onde o agente sabe quando agir, quando esperar e quando parar. `/loop` e `/heartbeat` fornecem as duas metades dessa equação: **proatividade orientada a.timer** (`/loop`) e **vigilância em ociosidade** (`/heartbeat`). Juntos, cobrem a lacuna entre o comando único e o cron job — mantendo o agente vivo e útil dentro da conversa, pronto para reportar o que importa no momento certo.

Junte-se à comunidade **Inteligência Agêntica** para acessar templates prontos, cron jobs de exemplo e discussões práticas sobre automação corporativa com agentes autônomos:
👉 [inteligenciaagentica.com.br](https://inteligenciaagentica.com.br)

---

## Fontes

[1] [Recurring Loops — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/loops)  
[2] [Session Heartbeats — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat)  
[3] [Cron Jobs & Scheduled Tasks — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/loops
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat
[3] https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
