---
title: "Bot Mode no Hermes Agent: Como Montar uma Equipe de Agentes de IA Nomeados que Conversam, Delegam e Decidem Juntos"
date: "2026-09-26"
lastmod: "2026-09-26"
summary: "Bot Mode transforma perfis isolados do Hermes Agent em uma equipe de agentes nomeados com avatares, chats em grupo e DMs entre bots — montada em segundos, sem código e sem infraestrutura de nuvem. Descubra como criar especialistas digitais que colaboram entre si e reportam direto no seu celular."
tags: ["Agentes de IA", "Bot Mode", "Multi-Agente", "Hermes Agent", "Automação", "Negócios", "Equipe Digital"]
keywords: ["bot mode hermes agent", "equipe de agentes de IA", "multi-agente empresarial", "agentes nomeados hermes", "chat em grupo agentes IA", "hermes peer", "automação multi-agente"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/bot-mode-equipe-agentes-nomeados-hermes-agent.jpg"
draft: false
---

> **Resposta Rápida (Answer-First / GEO):** Bot Mode é uma funcionalidade embutida no Hermes Desktop (v0.21.0+) que transforma cada perfil do agente em um "Bot" nomeado com avatar próprio, memória isolada, modelo de IA específico e skills dedicados. Bots podem conversar entre si em chats em grupo (2 a 6 participantes), trocar mensagens diretas via `hermes peer` e executar rotinas agendadas que lembram do que fizeram ontem. É como montar uma equipe de funcionários digitais especializados — cada um com seu cargo, sua mesa e suas responsabilidades — que coordenam o trabalho sem que você precise ser o mensageiro entre eles.

---

## O Problema: Agentes Inteligentes, mas Solitários

Se você já usa um agente de IA para resolver tarefas no dia a dia da empresa, provavelmente já passou por esse cenário:

❌ Você pede para o agente pesquisar um concorrente.  
❌ Depois copia o resultado e cola em outra sessão para que ele escreva um relatório.  
❌ Depois abre outra sessão e pede que ele revise o texto.  
❌ E mais outra para publicar.

Cada agente é inteligente — mas **surdo e cego** em relação aos outros. Você, o empresário ou gestor, vira o **pombo-correio** entre agentes que poderiam estar conversando diretamente.

Isso muda com o **Bot Mode**.

---

## O que é o Bot Mode?

Bot Mode é a funcionalidade central da **Pantheon Release** (Hermes Agent v0.21.0, lançada em 31 de agosto de 2026).[1][2] Ela transforma o Hermes Desktop de uma janela com um assistente único em um **escritório completo de agentes nomeados**.

Cada Bot é, na prática, um perfil Hermes com identidade própria:[1]

| Característica | O Que Cada Bot Possui |
|---|---|
| **Nome e Avatar** | Rosto geométrico determinístico (7 formas × 10 cores) ou imagem personalizada |
| **Modelo de IA** | Cada bot pode rodar um modelo diferente (GPT, Claude, DeepSeek, Gemini) |
| **Memória** | Isolada do restante — o que o pesquisador aprende não polui o financeiro |
| **Skills** | Habilidades independentes — o bot de DevOps não carrega skills de redação |
| **SOUL.md** | Personalidade e instruções comportamentais exclusivas |
| **Credenciais** | API keys e acessos próprios, isolados com segurança |

A criação é trivial: clique em **New Agent** no roster, preencha nome, título e descrição — e o Bot já existe, se apresentando na primeira mensagem do seu chat.[1]

---

## Como os Bots Conversam Entre Si

Aqui está a virada de jogo para operações empresariais: **bots não dependem mais de você para trocar informações**.

### @Mentions — Delegação com um Toque

No composer de qualquer chat, digite `@pesquisador analise os preços do concorrente X` e o bot ativo **delega a tarefa automaticamente**, aguarda a resposta e reporta de volta.[1]

### Group Chats — A Sala de Reunião Digital

Crie salas tipo Discord onde 2 a 6 bots trabalham juntos sobre o mesmo assunto:[1][5]

```
┌─────────────────────────────────────────────┐
│  🏛️  SALA: Planejamento Semanal            │
│─────────────────────────────────────────────│
│  👤 Você: "Qual foi o resultado da semana?" │
│                                             │
│  🔵 Pesquisador: "Tráfego orgânico subiu   │
│     12%. Concorrente Y lançou campanha..."  │
│                                             │
│  🟢 Financeiro: "Margem líquida de 23%.    │
│     ROAS do Google Ads caiu 8%..."          │
│                                             │
│  🟡 Estrategista: "Recomendo realocar      │
│     R$2.000 de Google p/ Meta baseado..."   │
│                                             │
│  Rodada 2/3                                 │
│  🔵 Pesquisador: "Confirmo — Meta tem CPA  │
│     35% menor no segmento B2B neste mês."  │
│                                             │
│  🟢 Financeiro: "Aprovado. Margem se       │
│     mantém dentro do target."               │
│                                             │
│  🟡 Estrategista: [passa — sem nada novo]  │
│                                             │
│  ✅ Sala estabilizou. 0 msgs na rodada 3.  │
└─────────────────────────────────────────────┘
```

**Regras do Group Chat:**

- Até **3 rodadas seriais** por mensagem enviada[1]
- Hard cap de **10 mensagens** por envio (evita espiral infinita)[1]
- Se nenhum bot fala numa rodada completa, a sala **estabiliza sozinha**[1]
- Bots **só falam quando têm algo novo** — silêncio é um recurso, não um bug[1]

### `hermes peer` — DMs Entre Máquinas

O comando `hermes peer` permite que bots em máquinas diferentes troquem mensagens diretas:[2]

```bash
# Registrar um agente remoto como peer
hermes peer add spark --url http://spark.lan:8377 --key <API_KEY>

# Enviar mensagem direta
hermes peer dm spark "status do deploy de ontem?"

# Executar tarefa longa de forma assíncrona
hermes peer run spark "analise este log de 50MB" --idempotency-key ticket-456
```

As respostas ficam registradas no Bot Chat canônico — **duráveis e inspecionáveis**, não descartáveis.[2]

---

## Caso de Uso Empresarial: A Equipe Operacional Compacta

Imagine que sua empresa hoje tem estas funções operacionais:

| Função Humana | Bot Equivalente | Modelo Sugerido | Custo Estimado/Mês |
|---|---|---|---|
| Analista de Mercado | 🔵 `@pesquisador` | Claude Sonnet (raciocínio) | ~US$15 |
| Redator | 🟣 `@redator` | GPT-4o (fluência) | ~US$10 |
| Controller Financeiro | 🟢 `@financeiro` | DeepSeek V4 (custo-benefício) | ~US$3 |
| Gerente de Projetos | 🟡 `@coordenador` | Gemini 3.7 Flash (velocidade) | ~US$5 |

**Custo total: ~US$33/mês** para uma equipe que opera 24/7, sem férias, sem reuniões improdutivas e sem WhatsApp pessoal no horário de trabalho.

### Fluxo de Trabalho Real

```
┌─────────────────────────────────────────────────────────────┐
│                   PIPELINE DE CONTEÚDO                       │
│                                                             │
│  📆 Cron 08:00 ──► 🔵 Pesquisador                         │
│  "Pesquise novidades do setor e salve relatório"            │
│       │                                                     │
│       ▼                                                     │
│  @mention ──► 🟣 Redator                                   │
│  "Escreva artigo baseado no relatório do pesquisador"       │
│       │                                                     │
│       ▼                                                     │
│  @mention ──► 🟡 Coordenador                               │
│  "Revise, aprove e publique no blog"                        │
│       │                                                     │
│       ▼                                                     │
│  📱 Telegram ◄── Resultado final entregue ao gestor         │
└─────────────────────────────────────────────────────────────┘
```

---

## Routines: Cada Bot com Sua Agenda

A aba **Routines** no Desktop conecta tarefas recorrentes diretamente ao bot responsável.[1][2] Na prática, são cron jobs do Hermes com namespace `[bot:<nome>]`:

- **`@pesquisador`** → Toda segunda às 07:00: "Scan de concorrentes e relatório semanal"
- **`@financeiro`** → Todo dia às 07:30: "Fechamento matinal com DRE e margem líquida"
- **`@coordenador`** → Toda sexta às 18:00: "Relatório consolidado da semana para o Jean"

**A novidade crítica da v0.21.0:** cron jobs agora têm **memória persistente**.[2] O relatório de sexta-feira sabe o que foi reportado na sexta anterior. Com `continuity=true`, o output de cada execução alimenta a próxima — deduplicação automática de informações já reportadas.[2]

Resultados das routines aparecem **no chat do próprio bot**, como se o agente estivesse reportando no grupo de trabalho.[2]

---

## Bots Através de Máquinas: O Escritório Distribuído

Bot Mode funciona através de múltiplas máquinas conectadas via **Settings → Connections**:[1]

```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  SEU DESKTOP  │    │  VPS NUVEM    │    │  HOMELAB      │
│  (Windows)    │    │  (Ubuntu)     │    │  (Tailscale)  │
│               │    │               │    │               │
│ 🔵 pesquisador│◄──►│ 🟢 financeiro │◄──►│ 🟡 devops     │
│ 🟣 redator    │    │ 🔴 suporte    │    │ 🟠 monitor    │
│               │    │               │    │               │
│  Hermes       │    │  Hermes       │    │  Hermes       │
│  Desktop      │    │  Gateway      │    │  Gateway      │
└───────────────┘    └───────────────┘    └───────────────┘
         ▲                                        │
         └────────── Roster Unificado ────────────┘
```

Todos os bots aparecem no **mesmo roster**, identificados por `@nome-dispositivo` quando há conflito de nomes.[1] DMs entre máquinas passam pelo Desktop Relay automaticamente.[1]

---

## Bot Mode vs. Orquestração Manual: Comparativo Executivo

| Critério | Antes (Agente Único) | Com Bot Mode |
|---|---|---|
| **Identidade** | Assistente anônimo genérico | Agentes nomeados com avatar e cargo |
| **Coordenação** | Você copia e cola entre sessões | @mention e Group Chat entre bots |
| **Trabalho Agendado** | Scripts stateless que repetem tudo | Cron com memória — sabe o que já fez |
| **Supervisão** | Espera o resultado e torce | Lista filhos, corrige rota ao vivo, para se necessário |
| **Custo de Setup** | Configuração por sessão | Cria bot em 3 campos, reutiliza para sempre |
| **Infraestrutura** | Plumbing manual de APIs | Embutido no Desktop, zero código |
| **Melhor Para** | Tarefas rápidas isoladas | Pipelines: pesquisa → redação → revisão → publicação |

---

## Como Começar em 5 Minutos

**Pré-requisito:** Hermes Agent v0.21.1 ou superior (inclui correções de confiabilidade de delegação).[2]

1. **Abra o Hermes Desktop** → clique na aba **BOTS** no sidebar
2. **Clique em "New Agent"** → preencha Nome, Título e Descrição
3. **(Opcional)** Clique em **Advanced** para:
   - Clonar a partir de um perfil existente
   - Fixar um modelo/provedor específico
   - Escrever um SOUL.md personalizado
   - Habilitar/desabilitar skills e toolsets individuais
4. **Crie um segundo bot** com função diferente
5. **Abra um Group Chat** com ambos e envie sua primeira tarefa

Cada bot é um perfil Hermes completo em `~/.hermes/profiles/<nome>/` — tudo que você faz no Desktop também funciona via CLI:[1]

| No Bot Mode | No Terminal |
|---|---|
| Chat com um Bot | `hermes -p <nome> chat` |
| Arquivos, skills, memória | `~/.hermes/profiles/<nome>/` |
| Routines | `hermes cron list` (jobs `[bot:<nome>]`) |
| Criar/inspecionar perfis | `hermes profile create`, `hermes profile list` |

---

## Governança e Limites: O que Você Precisa Saber

**Recursos e Limites Técnicos:**
- Até **3 backends** de bots ativos simultaneamente no Desktop (configurável em Settings → Advanced → Warm Bot Backends)[1]
- Cada backend ocupa **~60 MB** de memória[1]
- Bots inativos são reciclados após **10 minutos** de ociosidade[1]
- Group Chats: máximo **6 bots**, **3 rodadas**, **10 mensagens** por envio[1]

**Segurança:**
- Credenciais são isoladas por perfil — um bot comprometido não afeta os outros[1]
- OAuth de uso único (Anthropic, OpenAI) não é copiado entre bots — cada um faz login próprio[1]
- Deleção de perfil é **intencional e só via CLI** (`hermes profile delete <nome>`) — sem exclusão acidental pelo Desktop[3]

**Limitação honesta:** Bot Mode é uma ferramenta de estação de trabalho. Não há console administrativo centralizado, SSO corporativo, log de auditoria central ou camada de políticas. Para ambientes regulados, adicione seus próprios controles.[4]

---

## O Impacto no Seu Negócio

Para o empresário ou gestor maduro que busca eficiência operacional real:

1. **Redução de folha:** Uma equipe de 4 bots especializados custa ~US$33/mês contra milhares em CLT ou freelancers
2. **Disponibilidade 24/7:** Bots com routines agendadas operam enquanto você dorme
3. **Eliminação do gargalo humano:** Bots se comunicam entre si — você supervisiona, não transporta informação
4. **Escalabilidade horizontal:** Precisa de um novo especialista? Crie em 30 segundos clonando um existente
5. **Zero vendor lock-in:** Cada bot pode usar um provedor diferente — troque modelos sem reescrever nada

---

## Conclusão

Bot Mode é o momento em que o Hermes Agent deixa de ser "uma IA no terminal" e se torna **uma equipe de trabalho no seu desktop**. Não é um conceito, uma demo ou um roadmap — é uma funcionalidade embutida, ativa por padrão e gratuita (MIT) desde agosto de 2026.[2][5]

A pergunta não é mais "como faço multi-agente funcionar" — é **qual equipe você monta primeiro**.

---

> 💡 **Quer aprender a montar sua própria equipe de agentes especializados do zero?** Conheça o curso **Inteligência Agêntica** — de instalação a operação 24/7 com agentes que aprendem, colaboram e reportam direto no seu Telegram.
>
> 🔗 [inteligenciaagentica.com.br](https://inteligenciaagentica.com.br)

## Sources
[1] https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
[2] https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31
[3] https://github.com/NousResearch/Hermes-Bot-Mode
[4] https://runtimewire.com/article/nous-research-hermes-desktop-bot-mode
[5] https://www.marktechpost.com/2026/08/17/nous-research-hermes-bot-mode
[6] https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
[7] https://hermes-agent.nousresearch.com/docs/user-guide/messaging
[8] https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
