---
title: "Automation Blueprints no Hermes Agent: Fluxos Prontos 24/7 Sem Sintaxe Cron"
date: "2026-11-28"
lastmod: "2026-11-28"
summary: "Os Automation Blueprints do Hermes Agent transformam rotinas agendadas, webhooks de pagamento e alertas de infraestrutura em fluxos prontos que operam 24/7 sem exigir sintaxe cron ou programação do zero."
tags: ["Agentes de IA", "Automação", "Hermes Agent", "Cron Jobs", "Webhooks", "Negócios"]
keywords: ["Automation Blueprints Hermes Agent", "comando blueprint Hermes", "automação empresarial sem código", "webhooks Stripe agente IA", "cron jobs inteligentes"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/automation-blueprints-fluxos-prontos-hermes-agent.jpg"
draft: false
---

> **Em resumo:** Os **Automation Blueprints** do Hermes Agent são modelos prontos de automação que permitem ativar rotinas recorrentes, alertas de infraestrutura e respostas a eventos de API (como falhas de pagamento no Stripe ou incidentes no GitHub) preenchendo apenas alguns campos no painel web, no aplicativo Desktop ou via comando `/blueprint` no chat — sem escrever expressões cron nem depender de um único provedor de IA.[1][2]

Empresários e gestores que implementam agentes de IA raramente travam na conversa inicial com o modelo. O gargalo aparece na segunda etapa: transformar tarefas repetitivas da operação — vigiar se o site caiu, monitorar cobranças recusadas, resumir notícias do setor às 8h da manhã ou revisar entregas da equipe técnica — em rotinas confiáveis que rodam sozinhas na nuvem.

É exatamente esse abismo técnico que o sistema de **Automation Blueprints** do Hermes Agent elimina.[1][2] Em vez de obrigar o gestor a decorar expressões como `0 9 * * 1-5` ou configurar servidores intermediários, o Hermes entrega receitas validadas que funcionam com **qualquer modelo de linguagem** e entregam resultados direto no Telegram, Slack, Discord, SMS, e-mail ou arquivos locais.[1][2]

---

## O que são Automation Blueprints e como ativá-los em qualquer interface

Um *blueprint* no Hermes Agent é uma automação parametrizada que encapsula o gatilho, as instruções do agente, as habilidades (*skills*) necessárias e o canal de entrega.[1][2] O recurso foi desenhado para funcionar em **todas as superfícies** do ecossistema, sem prender o operador ao terminal:[2]

- **Web Dashboard e Hermes Desktop:** basta abrir a página **Cron**, alternar para a aba **Blueprints**, preencher os campos do formulário (como horário e canal de destino) e clicar em *Schedule it*.[2] No aplicativo Desktop, o botão **Send to App** também carrega o comando já montado no compositor.[2]
- **CLI, TUI e Mensageiros (Telegram, Slack, Discord):** digite `/blueprint <nome>` (por exemplo, `/blueprint morning-brief`).[2] O Hermes faz as perguntas necessárias uma por vez e só cria a tarefa após confirmação explícita — nenhum blueprint agenda rotinas silenciosamente sem autorização.[2]
- **Modo direto para operadores avançados:** é possível pular o questionário passando os valores na mesma linha, como `/blueprint morning-brief time=08:00`.[2] A correspondência de nomes é tolerante a prefixos e pequenas variações de digitação.[2]

Depois de criado, o job passa a ser gerenciado normalmente pelo comando `/cron`, podendo ser pausado, editado ou auditado a qualquer momento.[2]

```
+-----------------------------------------------------------------------+
|                    INTERFACE DO GESTOR (QUALQUER CANAL)               |
|  Dashboard / Desktop (Aba Blueprints)  OU  Chat/CLI (/blueprint ...)  |
+-----------------------------------+-----------------------------------+
                                    |
                          Confirmação explícita
                                    v
+-----------------------------------------------------------------------+
|                   MOTOR DE GATILHOS DO HERMES AGENT                   |
|  [1] Schedule (Cron)   |   [2] GitHub Event   |   [3] API Webhook     |
+-----------------------------------+-----------------------------------+
                                    |
                  Execução com qualquer modelo + Skills
                                    v
+-----------------------------------------------------------------------+
|                  FILTRO DE RUÍDO & ENTREGA MULTI-CANAL                |
|  Sem novidades -> [SILENT] (zero spam)                                |
|  Ação exigida  -> Telegram | Slack | Discord | E-mail | SMS | Arquivo |
+-----------------------------------------------------------------------+
```

---

## Os 3 tipos de gatilhos dos Blueprints na prática

Todos os *Automation Blueprints* oficiais apoiam-se em três mecanismos nativos do Hermes: o agendador cron (`cronjob_manage`) para tarefas baseadas em tempo e a plataforma de webhooks (`hermes webhook subscribe` ou rotas no `config.yaml`) para eventos em tempo real.[1]

| Tipo de Gatilho | Como Funciona | Ferramenta / Comando | Exemplos Empresariais Reais |
|---|---|---|---|
| **Schedule (Agendado)** | Roda em cadência fixa (a cada 30 min, diário, dias úteis ou semanal) | `cronjob_manage` ou `/cron` | Monitor de disponibilidade do site, resumo executivo matinal, auditoria semanal de segurança [1] |
| **GitHub Event** | Dispara imediatamente quando um PR abre, um código é mesclado ou o CI falha | `hermes webhook subscribe` | Revisão automática de Pull Requests, diagnóstico de falhas de build, triagem de *issues* [1] |
| **API Call (Webhook)** | Sistema externo envia um `POST` JSON assinado para o endpoint do Hermes (porta padrão `8644`) | `hermes webhook subscribe` ou `config.yaml` | Falhas e disputas de pagamento no Stripe, triagem de alertas Datadog/Grafana, verificação pós-deploy [1] |

### O padrão `[SILENT]`: inteligência sem fadiga de alertas

Um dos maiores problemas de automações corporativas é inundar o celular do gestor com mensagens inúteis do tipo *"tudo funcionando normalmente"*. Os blueprints do Hermes resolvem isso com o padrão **`[SILENT]`**: sempre que a resposta do cron job contém `[SILENT]`, a entrega da notificação é suprimida automaticamente.[1]

Na prática, um monitor de infraestrutura ou triagem noturna verifica dezenas de métricas e só envia uma mensagem no Telegram ou Slack quando encontra uma queda real, um erro HTTP `>= 500` ou uma anomalia que exige decisão humana.[1]

---

## Receitas prontas para operações de negócios e tecnologia

A documentação oficial reúne blueprints prontos para copiar, adaptar e colocar em produção em minutos.[1] Abaixo estão os fluxos de maior impacto imediato para empresas:

| Blueprint | Gatilho | O que faz na operação | Entrega Recomendada |
|---|---|---|---|
| **Stripe Payment Monitoring** | Webhook API (`payment_intent.payment_failed`, `charge.dispute.created`) | Identifica o motivo da recusa no Stripe, diferencia erro transitório (tentar novamente) de permanente (contatar cliente) e sinaliza disputas/chargebacks como urgentes | Slack / Telegram (`ops`) [1] |
| **Uptime Monitor (Híbrido)** | Schedule (`every 30m`) + script Python | Testa API, site e docs via HTTP sem gastar tokens quando tudo está no ar; só aciona o LLM e notifica se detectar `OUTAGE DETECTED` | Telegram (`[SILENT]` se ok) [1] |
| **Daily Revenue & Market Briefing** | Schedule (`0 8 * * *`) | Consolida indicadores financeiros, cotações e principais notícias de IA/tecnologia das últimas 12 horas em 3 a 4 tópicos objetivos | Telegram matinal [1] |
| **Alert Triage** | Webhook API (Datadog, PagerDuty, Grafana) | Cruza o alerta recebido com deploys recentes e erros conhecidos na web, entregando causa raiz provável, primeiros passos e prioridade (P1–P4) | Canal de plantão Slack [1] |
| **Deploy Verification** | Webhook API (CI/CD) | Executa *smoke tests* automáticos logo após cada deploy, valida `/health` e versão ativa, reportando status (`healthy`, `degraded` ou `failed`) | Telegram [1] |
| **Competitive Repository Scout** | Schedule (`0 8 * * *`) | Monitora repositórios estratégicos no GitHub diariamente, filtrando mudanças arquiteturais e correções de segurança relevantes (ignorando ruído de dependências) | Telegram [1] |

### Exemplo real: Webhook de pagamentos Stripe em 1 comando

Para conectar eventos financeiros do Stripe ao canal operacional da equipe sem construir um microserviço separado, o gestor registra o blueprint diretamente via CLI:[1]

```bash
hermes webhook subscribe stripe-payments \
  --events "payment_intent.succeeded,payment_intent.payment_failed,charge.dispute.created" \
  --prompt "Stripe event received:
Event type: {type}
Amount: {data.object.amount} cents ({data.object.currency})
Customer: {data.object.customer}
Status: {data.object.status}

For payment_intent.payment_failed:
- Identify the failure reason from {data.object.last_payment_error}
- Suggest whether this is a transient issue (retry) or permanent (contact customer)

For charge.dispute.created:
- Flag as urgent and summarize the dispute details" \
  --deliver slack
```

O mesmo modelo funciona com assinaturas HMAC-SHA256 (`X-Webhook-Signature-V2` e `X-Webhook-Timestamp`) para validar webhooks de pipelines próprios ou ferramentas internas de monitoramento.[1]

---

## Como criar seus próprios Blueprints corporativos (via `SKILL.md` ou Plugins)

Para empresas que padronizam processos internos — como fechamento semanal de vendas, auditoria de contratos ou *standup* de equipe — o Hermes permite transformar qualquer **Skill** em um blueprint reutilizável.[2][4] Basta adicionar o bloco `blueprint` dentro da chave `hermes:` no cabeçalho YAML do arquivo `SKILL.md`:[2][4]

```yaml
---
name: fechamento-semanal-ops
description: Consolida métricas operacionais e pendências toda sexta-feira.
version: 1.0.0
hermes:
  tags: [Operações, Relatórios]
  blueprint:
    schedule: "0 17 * * 5"
    deliver: telegram
    prompt: "Compile os chamados abertos, entregas concluídas e gargalos da semana."
    no_agent: false
---
```

Além disso, plugins instalados por perfil também podem registrar blueprints próprios via `ctx.register_automation_blueprint()`.[2] Para garantir governança, os blueprints de plugins recebem automaticamente um prefixo com o nome do plugin (ex.: `/blueprint teamtools:standup`), impedindo que qualquer extensão de terceiros sobrescreva um blueprint nativo do sistema.[2] E há uma proteção operacional importante: mesmo que você desative o plugin depois, os cron jobs que já foram agendados a partir dele continuam rodando normalmente.[2]

---

## Automação Tradicional vs. Automation Blueprints no Hermes

| Critério | Cron Manual / Scripts Isolados | Automation Blueprints (Hermes Agent) |
|---|---|---|
| **Curva de configuração** | Exige sintaxe cron, scripts de entrega e tratamento de erros | Formulário visual no Dashboard/Desktop ou perguntas guiadas via `/blueprint` [2] |
| **Inteligência na triagem** | Nula — dispara alertas brutos ou exige regras rígidas `if/else` | Interpreta logs, falhas de pagamento e diffs antes de notificar [1] |
| **Controle de ruído** | Alto risco de spam de notificações | Suporte nativo ao padrão `[SILENT]` e modo script-first de custo zero [1] |
| **Portabilidade de modelo** | Muitas vezes acoplado a uma API específica | Funciona com qualquer provedor ou modelo configurado no Hermes [1] |
| **Governança por perfil** | Difícil de isolar por departamento | Plugins carregam por perfil sem sobrescrever blueprints nativos [2] |

Com a expansão contínua do catálogo de plugins — reforçada nas atualizações recentes até a linha `v0.23.4` — o padrão de blueprints consolida o Hermes como uma plataforma prática para gestores que querem menos código improvisado e mais processos auditáveis rodando 24 horas por dia.[2][3]

---

Se você quer dominar a arquitetura prática de agentes autônomos aplicados a operações reais de negócios, conheça a comunidade **Inteligência Agêntica** em [inteligenciaagentica.com.br](https://inteligenciaagentica.com.br).

## Sources

[1] https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints — Automation Blueprints | Hermes Agent
[2] https://hermes-agent.nousresearch.com/docs/reference/automation-blueprints-catalog — Automation Blueprints Catalog | Hermes Agent
[3] https://github.com/NousResearch/hermes-agent/releases — Releases · NousResearch/hermes-agent
[4] https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills — Creating Skills | Hermes Agent
