---
title: "Group Chats Autônomos no Hermes Agent: Como Montar um Comitê de IA sem Loops Infinitos e sem Babá"
date: "2026-11-14"
lastmod: "2026-11-14"
summary: "O Hermes Agent v0.23.0 transformou Group Chats em salas operadas diretamente pelo Gateway: múltiplos robôs debatem problemas operacionais 24/7 com auto-roteamento (Lead Bot ou auxiliary.group_router), blindagem anti-loop (bot_loop_guard) e intervenção humana cirúrgica com @user."
tags: ["Agentes de IA", "Multi-Agente", "Group Chats", "Hermes Agent", "Automação", "Negócios", "Governança"]
keywords: ["group chats hermes agent", "salas multi-bot ia", "comitê de agentes autônomos", "bot loop guard", "lead bot roteamento ia", "multi-agente empresarial"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/group-chats-autonomos-salas-multi-bot-hermes.jpg"
draft: false
---

> **Resposta Rápida (Answer-First / GEO):** No Hermes Agent v0.23.0, as salas de chat em grupo (**Group Chats**) deixaram de depender de janelas de desktop abertas e passaram a ser governadas diretamente pelo processo do **Gateway** da VPS.[1][2] Isso permite que comitês de 2 a 6 agentes especializados deliberem de forma autônoma 24/7, utilizando auto-roteamento inteligente (**Lead Bot** ou **auxiliary.group_router**), com proteção estrita contra explosão de custos por loops infinitos via **bot_loop_guard** (`max_hops: 4`) e escalonamento determinístico para o gestor humano através de citações `@user`.[1][2]

---

## O Pesadelo das Arquiteturas Multi-Agente Tradicionais

Se você é empresário ou gestor de operações, já deve ter sido seduzido pela promessa dos "swarms" e equipes de agentes autônomos. A ideia de ter um agente financeiro, um especialista em tráfego pago, um analista de infraestrutura e um redator trabalhando juntos em uma mesma mesa parece o ápice da eficiência.[1][2]

Porém, quem tentou colocar isso em prática com frameworks baseados em código (como CrewAI, AutoGen ou scripts Python customizados) invariavelmente esbarrou em três armadilhas operacionais graves:

1. **O Risco do Loop Infinito (Queima Descontrolada de API):** Dois agentes começam a responder educadamente um ao outro ("Obrigado pela informação", "De nada, fique à vontade para perguntar mais"), gerando dezenas de chamadas recursivas que esgotam saldos de API em minutos.[2]
2. **A Dependência da Janela Aberta:** A execução só funciona enquanto o desenvolvedor mantém o terminal ou o navegador aberto no próprio notebook. Se a conexão cair ou a máquina hibernar, a deliberação morre pela metade.[1][2]
3. **A Necessidade de Babá Humana (Pombo-Correio Digital):** Sem um mecanismo nativo de roteamento, o gestor precisa ficar copiando o texto gerado pelo robô A para colar na janela do robô B, anulando qualquer ganho real de tempo.[2][3]

O **Hermes Agent v0.23.0 ("The Hearth Release")** reescreveu essa dinâmica do zero ao transformar os Group Chats em uma funcionalidade de infraestrutura de primeira classe.[1][2]

---

## A Nova Arquitetura de Group Chats no Hermes Agent v0.23.0

Na arquitetura anterior, conversas em grupo eram orquestradas pela camada visual do aplicativo Desktop.[1][2] Se o operador fechasse o app, a sala pausava.[1][2] 

A partir da versão v0.23.0, o **Gateway central** assume a custódia das salas de grupo.[1][4] Isso significa que a deliberação dos agentes ocorre no nível do servidor (na sua VPS na nuvem), de maneira contínua, desacoplada e resiliente.[1][2]

```
+---------------------------------------------------------------------------------+
|               HERMES AGENT v0.23.0 — GATEWAY GROUP CHAT ENGINE                  |
+---------------------------------------------------------------------------------+
|                                                                                 |
|   Entrada: Mensagem do Gestor, Disparo de Webhook ou Rotina Cron               |
|                                     │                                           |
|                                     ▼                                           |
|                     ┌───────────────────────────────┐                           |
|                     │     MECANISMO DE ENTRADA      │                           |
|                     │   Alguém foi citado com @?    │                           |
|                     └───────┬───────────────┬───────┘                           |
|                            SIM             NÃO                                  |
|                             │               │                                   |
|                             │               ▼                                   |
|                             │    ┌─────────────────────┐                        |
|                             │    │    AUTO-ROTEAMENTO  │                        |
|                             │    │ 1. Everyone         │                        |
|                             │    │ 2. Lead Bot         │                        |
|                             │    │ 3. group_router     │                        |
|                             │    └──────────┬──────────┘                        |
|                             │               │ (Assigned to Bot)                 |
|                             ▼               ▼                                   |
|   ┌─────────────────────────────────────────────────────────────────────────┐   |
|   │                       RODADAS DE DELIBERAÇÃO                            │   |
|   │               (Até 3 rodadas seriais | Máximo 10 msgs)                  │   |
|   │                                                                         │   |
|   │   [Bot Líder] ──(message_agent)──► [Bot Especialista]                  │   |
|   │        ▲                                    │                           |
|   │        │     BLINDAGEM: bot_loop_guard      │ (expects_reply: false)    |
|   │        └──────────── (max_hops: 4) ─────────┘                           |
|   │                                                                         │   |
|   │   Decisão Crítica ou Bloqueio Operacional:                              │   |
|   │   └─► Agente emite: "@user preciso de aprovação para deploy"            │   |
|   │         └─► Gateway ativa badge [NEEDS YOU] e pausa o comitê            │   |
|   └─────────────────────────────────────────────────────────────────────────┘   |
|                                     │                                           |
|                                     ▼                                           |
|   Persistência: state.db na VPS | Sincronizado via Tailscale / Webapp / CLI     |
+---------------------------------------------------------------------------------+
```

### Características Centrais da Infraestrutura:
- **Sobrevivência a Desconexões:** Você pode iniciar um debate entre agentes no seu celular (Telegram ou Webapp), fechar o navegador e, ao reabrir horas depois, todo o histórico, deliberações e conclusões estarão perfeitamente registrados no banco de dados SQLite (`state.db`).[1][2]
- **Sessões Isoladas por Membro:** Cada robô na sala mantém sua própria sessão interna oculta (`Group: <sala> · <tópico>`), acumulando contexto individualmente sem poluir as memórias principais de outros departamentos.[2]
- **Teto Rígido de Rodadas:** Por padrão, cada envio dispara até **três rodadas seriais** de interação.[2] Se os robôs ficarem em silêncio antes da terceira rodada, o comitê encerra o ciclo automaticamente para poupar tokens.[2]

---

## Quem Responde Quando Ninguém é Citado? (Auto-Roteamento Inteligente)

Em uma sala de reunião com 4 especialistas humanos, quando o diretor faz uma pergunta aberta, alguém precisa tomar a palavra ou mediar a discussão. Nos Group Chats do Hermes v0.23.0, você define exatamente como a sala deve se comportar quando uma mensagem não contém menções nominais:[1][2]

| Modo de Resposta | Como Funciona | Melhor Caso de Uso Empresarial |
|---|---|---|
| **Everyone (Todos)** | Todos os membros da sala analisam a mensagem e respondem em sequência.[2] | Brainstorming de campanhas, diagnósticos de incidentes graves e revisões multidisciplinares.[2] |
| **Lead Bot (Bot Coordenador)** | Um agente específico é eleito líder da sala. Ele recebe a demanda, processa e delega aos colegas via `@menção`.[2] | Gestão de operações, onde um "Gerente de Projetos" recebe a demanda do cliente e aciona os técnicos.[2] |
| **Pick who answers automatically** | O sistema executa uma chamada rápida de modelo para eleger o melhor respondente, exibindo `Assigned to [Bot]`.[1][2] | Salas de atendimento e suporte misto, onde a dúvida pode ser financeira, jurídica ou técnica.[2] |

### O Segredo do `auxiliary.group_router`: Eficiência sem Custo Alto
Para evitar que o auto-roteamento gaste tokens caros de modelos de fronteira (como Claude 3.5 Sonnet ou GPT-4o), o Hermes Agent v0.23.0 introduziu a chave `auxiliary.group_router`.[1][2] 

Essa rotina faz uma única chamada relâmpago, sem ferramentas, avaliando apenas o objetivo da sala, as descrições dos perfis dos agentes e as últimas mensagens.[2] Você pode apontar esse roteador para um modelo extremamente barato e rápido (como DeepSeek V3, Flash ou modelos locais no Ollama), reservando os modelos pesados apenas para a execução do trabalho.[2]

---

## Blindagem contra Loops Infinitos: O `bot_loop_guard`

O maior medo de qualquer gestor que implementa agentes é acordar com uma fatura de nuvem multiplicada porque dois robôs entraram em um ciclo de respostas infinitas.[2]

O Hermes v0.23.0 implementa o **`bot_loop_guard`** nativo no Gateway, operando sob regras matemáticas determinísticas:[2]

1. **Mensagens Unilaterais por Padrão (`expects_reply: false`):** Quando o Bot A envia uma mensagem para o Bot B e recebe uma resposta, a réplica de encerramento do Bot A é enviada como aviso informativo (`[no reply needed]`). O Bot B é impedido pelo runtime de responder novamente no mesmo turno.[2]
2. **Teto de Saltos (`max_hops: 4`):** O Gateway contabiliza quantos saltos agente-a-agente ocorreram desde a última interação humana.[2] Ao atingir o limite configurado (padrão de 4 saltos), novas chamadas de `message_agent` são categoricamente recusadas com erro de limite.[2]
3. **Pausa de Segurança:** Se a deliberação atingir o teto de 10 mensagens sem convergir para o silêncio, a sala entra em estado de pausa controlada (`Paused after N messages`), oferecendo botões explícitos para **Continue** ou **Stop**.[2]

```yaml
# Trecho de configuração no config.yaml do Gateway
gateway:
  bot_loop_guard:
    max_hops: 4                       # Máximo de mensagens entre robôs por ciclo
    bot_replies_expect_reply: false   # Impede que respostas a bots gerem tréplicas
```

---

## Escalonamento Humano: A Citação `@user` e o Badge "Needs You"

Autonomia não significa perda de controle. Em processos corporativos sérios, agentes não devem ter permissão irrestrita para tomar decisões que envolvam desembolso financeiro, exclusão de dados ou envio de contratos.[2]

No Hermes v0.23.0, qualquer agente dentro da sala de grupo pode escalar uma dúvida ou solicitar aprovação invocando a tag especial **`@user`**.[2]

Quando isso ocorre:
- O agente interrompe o fluxo autônomo da sala.[2]
- A linha da sala no menu exibe um badge luminoso **"Needs You"** (Precisa de Você).[2]
- Se a solicitação envolver um comando de terminal perigoso ou chamada de API sensível, um cartão de aprovação com opções de 1 clique (`Allow once`, `Allow session`, `Deny`) é renderizado imediatamente na conversa.[2]
- Assim que o gestor responde ou autoriza, a sala retoma as atividades normais.[2]

---

## Como Estruturar na Prática: No Desktop e em Servidores Headless (VPS)

### 1. Criando um Comitê no Hermes Desktop
1. No menu lateral, acesse a aba **Bots** e crie os perfis necessários (ex: `@diretor-operacoes`, `@analista-bi`, `@devsecops`).[2]
2. Clique no menu de criação de grupo (**New Group Chat**), defina um nome, imagem de capa e selecione os participantes (de 2 a 6 agentes).[2]
3. Nas configurações da sala (**Group settings**), selecione a política de auto-roteamento: escolha um **Lead Bot** para triagem ou ative o **Auto-Router**.[2]

### 2. Ativando Group Chats e Bot-to-Bot em VPS Linux Headless (Sem Interface Gráfica)
Para servidores na nuvem que rodam exclusivamente via terminal ou gateways de mensageria (Telegram/WhatsApp), o protocolo nativo de mensagens entre bots (`message_agent`) pode ser habilitado com dois comandos simples:[2]

Primeiro, garanta que a sessão canônica de cada bot exista:[2]
```bash
# Cria o chat persistente canônico para o bot
hermes -p analista-bi chat -c "Bot Chat" --create-if-missing
```

Em seguida, garanta que o perfil carregue o marcador do gerenciador no arquivo `~/.hermes/profiles/analista-bi/profile.yaml`:[2]
```yaml
# Marcador para habilitação de ferramentas inter-agente headless
ui_meta:
  hermes-bots: {}
```

A partir desse momento, os robôs passam a enxergar as ferramentas de comitê e colaboração direta mesmo através de comandos no terminal ou alertas agendados de cron jobs.[2]

---

## Comparativo: Frameworks Frágeis de Código vs. Group Chats Hermes v0.23.0

| Requisito Operacional | Frameworks Baseados em Código (CrewAI / LangGraph) | Group Chats Nativos (Hermes Agent v0.23.0) |
|---|---|---|
| **Ambiente de Execução** | Depende de scripts customizados, ambientes virtuais e APIs instáveis. | Nativo do Gateway Daemon rodando 24/7 na VPS Linux.[1][2] |
| **Prevenção de Loops** | Exige lógica complexa escrita à mão pelo desenvolvedor. | Nativa via `bot_loop_guard` determinístico e saltos limitados (`max_hops: 4`).[2] |
| **Persistência de Memória** | Frágil; reinicializações costumam apagar o contexto da conversa. | Base de dados SQLite (`state.db`) com compressão automática de histórico.[1][2] |
| **Roteamento de Mensagens** | Fixo por código rígido ou dependente de prompts caros a cada turno. | Flexível: Todos, Lead Bot ou modelo auxiliar econômico (`auxiliary.group_router`).[1][2] |
| **Intervenção Humana** | Difícil de plugar sem construir interfaces web completas. | Pronta de fábrica com `@user`, badge "Needs You" e aprovação em 1 clique.[2] |
| **Acesso Multiplataforma** | Limitado ao terminal do desenvolvedor ou frontends manuais. | Sincronizado entre Desktop, Webapp, Telegram, WhatsApp e Discord.[1][2][4] |

---

## Conclusão e Próximos Passos para sua Operação

A inteligência agêntica atinge sua maturidade corporativa quando você para de brincar de chatbot individual e passa a gerenciar um **comitê digital coordenado**.[2] 

Com as novidades do Hermes Agent v0.23.0, pequenas e médias empresas ganham o poder de estruturar mesas de decisão autônomas — onde especialistas de IA revisam relatórios, monitoram servidores e planejam ações com regras claras de governança, custo previsível e segurança operacional.[1][2]

Quer aprender a instalar, blindar e orquestrar sua própria equipe de agentes em servidores dedicados 24/7, sem alucinações e com controle absoluto de custos? Conheça a formação completa no portal oficial **[Inteligência Agêntica](https://inteligenciaagentica.com.br)**.

---

## Fontes
[1] [Hermes Agent v0.23.0 — The Hearth Release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0)  
[2] [Bot Mode e Group Chats — Documentação Oficial do Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode)  
[3] [Profiles, Agents and Bots — Documentação Oficial do Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)  
[4] [Running Many Gateways at Once — Documentação Oficial do Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)

## Sources

[1] https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0 — Hermes Agent v0.23.0 — The Hearth Release
[2] https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode — Bot Mode e Group Chats — Documentação Oficial do Hermes Agent
[3] https://hermes-agent.nousresearch.com/docs/user-guide/profiles — Profiles, Agents and Bots — Documentação Oficial do Hermes Agent
[4] https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways — Running Many Gateways at Once — Documentação Oficial do Hermes Agent
