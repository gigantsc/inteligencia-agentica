---
title: "Mixture of Agents (MoA) no Hermes Agent: Como Criar um Conselho de Modelos de IA para Decisões Críticas"
date: "2026-11-20"
lastmod: "2026-11-20"
summary: "Aprenda a usar o Mixture of Agents (MoA) nativo do Hermes Agent para combinar múltiplos modelos consultores com um agregador executivo, elevando a precisão em tarefas complexas sem quebrar o prompt caching nem multiplicar a fatura."
tags: ["Hermes Agent", "Mixture of Agents", "MoA", "Agentes de IA", "Arquitetura", "Automação", "Custos de IA"]
keywords: ["Mixture of Agents Hermes Agent", "MoA IA empresas", "conselho de modelos de IA", "HermesBench MoA", "prompt caching multi modelo", "hermes moa configure"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/mixture-of-agents-moa-conselho-modelos-hermes-v2.jpg"
draft: false
---

> **Em resumo:**
> O **Mixture of Agents (MoA)** transforma o Hermes Agent em um provedor virtual (`moa`) onde modelos consultores (*reference models*) analisam o problema em paralelo e entregam suas recomendações para um modelo **agregador** (*acting model*), responsável por executar ferramentas e dar a resposta final.[1] No benchmark *HermesBench*, a combinação de `claude-opus-4.8` como agregador sobre uma referência `gpt-5.5` alcançou **0,8202**, superando em cerca de 6 pontos o melhor modelo isolado (`0,7607`).[1] Com cadência padrão `fanout: user_turn`, filtro de privacidade (`moa.privacy_filter`) e preservação integral do *prompt caching*, o MoA entrega qualidade de junta executiva com custo previsível.[1]

---

## O Dilema do Modelo Único em Decisões de Alto Impacto

Todo empresário ou gestor de operações que coloca agentes de IA em produção esbarra no mesmo teto: **nenhum modelo isolado é imbatível em tudo**. Um modelo pode ser excelente para estruturar arquitetura de software, outro para revisar cláusulas contratuais ou detectar riscos financeiros, e um terceiro para escrever código limpo.

Quando a decisão é crítica — como planejar a migração de um banco de dados em produção, auditar uma planilha de margens ou revisar uma política de segurança — depender da opinião única de uma IA aumenta o risco de pontos cegos. A solução intuitiva seria abrir três abas diferentes e copiar respostas manualmente entre elas, mas isso destrói a produtividade e desconecta o raciocínio do ambiente de ferramentas do agente.

O **Hermes Agent** resolve esse gargalo nativamente com o **Mixture of Agents (MoA)**, um provedor virtual integrado ao sistema de seleção de modelos.[1]

---

## Como Funciona o Conselho Virtual do MoA no Hermes Agent

Diferente de um *swarm* onde vários agentes independentes brigam pelo mesmo terminal, o MoA funciona como um **conselho consultivo acoplado a um único diretor executivo** dentro do mesmo loop de agente.[1]

```
FLUXO DE EXECUÇÃO — MIXTURE OF AGENTS (MoA) NO HERMES AGENT
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. PERGUNTA DO GESTOR / USUÁRIO                                           │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ 2. MODELOS DE REFERÊNCIA (Advisors — sem esquemas de ferramentas)         │
│    • Ex: gpt-5.5 + deepseek-v4-pro                                        │
│    • Recebem apenas o histórico conversacional limpo (custo reduzido)     │
│    • Rodam 1x por turno por padrão (fanout: user_turn)                    │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ 3. FILTRO DE PRIVACIDADE (Opcional: moa.privacy_filter)                   │
│    • Mascara e-mails, telefones formatados, API keys e JWTs               │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ 4. MODELO AGREGADOR (Acting Model — com ferramentas & cache intacto)      │
│    • Ex: anthropic/claude-opus-4.8                                        │
│    • Recebe o parecer dos consultores como bloco de orientação no final   │
│    • Executa bash, arquivos, MCPs, /goal e responde ao usuário            │
└───────────────────────────────────────────────────────────────────────────┘
```

Na prática, o fluxo segue sete etapas determinísticas a cada chamada principal:[1]
1. O Hermes resolve o *preset* MoA selecionado pelo nome.[1]
2. Os **modelos de referência** rodam **sem esquemas de ferramentas** (*tool schemas*), recebendo apenas o texto da conversa, o que mantém essas chamadas baratas e evita rejeições de provedores mais rígidos.[1]
3. As respostas dos consultores são anexadas como contexto privado ao final do prompt para o agregador.[1]
4. O **agregador** é chamado com o catálogo normal de ferramentas do Hermes.[1]
5. A resposta do agregador atua como a resposta oficial do agente na sessão.[1]
6. Se o agregador precisar executar ferramentas (ler arquivos, consultar bancos, rodar scripts), o Hermes executa normalmente.[1]
7. Em novas iterações, o ciclo se repete conforme a cadência `fanout` configurada.[1]

---

## Evidência Empírica: +6 Pontos no HermesBench

A combinação de perspectivas não gera apenas "uma média" das respostas — ela eleva o teto de capacidade do próprio modelo mais forte.[1] Nos testes do *HermesBench*, um preset MoA de dois modelos obteve ganho expressivo frente aos componentes individuais:[1]

| Configuração Avaliada | Pontuação no HermesBench | Diferença vs. Melhor Modelo Único |
|---|---|---|
| **MoA: `claude-opus-4.8` (Agregador) + `gpt-5.5` (Referência)** | **0,8202** | **+0,0595 (~6 pontos)** |
| `anthropic/claude-opus-4.8` isolado | 0,7607 | Linha de base |
| `openai/gpt-5.5` isolado | 0,7412 | -0,0195 |

---

## MoA vs. Modelo Único vs. Multi-Agente (Swarm)

Para o gestor decidir quando ativar o MoA em vez de usar um único modelo ou uma equipe completa de bots, vale comparar os três desenhos:

| Critério | Modelo Único Padrão | Mixture of Agents (MoA) | Multi-Agente / Swarm |
|---|---|---|---|
| **Estrutura** | 1 LLM executa tudo | N consultores + 1 agregador executor | Múltiplos agentes com sessões próprias |
| **Acesso a Ferramentas** | Sim (direto) | Apenas o Agregador executa ferramentas[1] | Cada agente tem seu escopo/worktree |
| **Uso Ideal** | Rotinas diárias e tarefas claras | Decisões críticas, revisões, arquitetura e `/goal`[1] | Projetos paralelos longos (front + back) |
| **Prompt Caching** | Preservado | **100% preservado** no prefixo principal[1] | Independente por agente |
| **Complexidade de Setup** | Nenhuma | Um bloco `moa:` no `config.yaml` ou `/moa`[1] | Orquestração via Kanban/Delegation |

---

## Controle de Custos, Cadência (`fanout`) e Faturamento

Um erro comum ao adotar arquiteturas multi-modelo é deixar o custo explodir em loops de ferramentas. O Hermes Agent protege o orçamento da operação com transparência total e três modos de cadência (*advisor cadence*):[1]

1. **Quem paga a conta:** O **agregador** é faturado por todo o loop de ferramentas, pois ele executa cada passo da tarefa.[1] Os modelos de referência apenas aconselham.[1] Quando o provedor do agregador difere do `model.provider` principal da sua assinatura, comandos como `hermes moa list` e `hermes moa configure` exibem um aviso explícito informando onde o faturamento cairá.[1]
2. **Cadência `fanout`:** Desde julho de 2026, o padrão é `user_turn` — a opção mais econômica para produção.[1]

| Modo `fanout` | Frequência dos Consultores | Perfil de Custo e Uso |
|---|---|---|
| `user_turn` *(padrão)* | Rodam **1 vez por mensagem do usuário**, planejando no início do turno[1] | **Mais barato:** custo dos consultores não multiplica com chamadas de ferramentas[1] |
| `every_n:3` *(ou qualquer N ≥ 2)* | Rodam na 1ª iteração e depois a cada **N** iterações de ferramentas[1] | **Equilíbrio:** revalida o plano em tarefas longas reutilizando orientação em cache[1] |
| `per_iteration` | Reavaliam a **cada iteração de ferramenta**[1] | **Máximo frescor, maior custo:** multiplica latência e gasto pelo nº de passos[1] |

Além da cadência, cada slot (consultor ou agregador) aceita seu próprio `reasoning_effort` (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, `ultra`), permitindo, por exemplo, que um consultor faça triagem rápida em `low` enquanto outro analisa profundamente em `xhigh`.[1]

---

## Como Configurar e Usar na Prática

Por ser um provedor nativo (`moa`), seus *presets* aparecem automaticamente na CLI, no TUI, no Desktop App, no Web Dashboard e no gateway de mensageria.[1]

### 1. Uso rápido (One-Shot) com `/moa`
Se você não quer trocar o modelo padrão da sessão, use o atalho `/moa` seguido da tarefa.[1] O Hermes executa aquele turno com o preset `default` e restaura seu modelo anterior logo em seguida:[1]

```text
/moa elabore um plano de contingência para migração do ERP sem janela de indisponibilidade
```

### 2. Troca de modelo para a sessão ou via `config.yaml`
Para fixar um preset na sessão atual, use o seletor normal:[1]

```text
/model default --provider moa
/model revisao_executiva --provider moa
```

Ou defina diretamente via terminal (`hermes moa configure revisao_executiva`) ou no `config.yaml` com filtros de privacidade ativos:[1]

```yaml
moa:
  default_preset: revisao_executiva
  privacy_filter: display # ou 'full' para mascarar também no prompt do agregador
  presets:
    revisao_executiva:
      fanout: every_n:3
      reference_models:
        - provider: openai-codex
          model: gpt-5.5
          reasoning_effort: high
        - provider: openrouter
          model: deepseek/deepseek-v4-pro
      aggregator:
        provider: openrouter
        model: anthropic/claude-opus-4.8
        reasoning_effort: high
      enabled: true
```

Você também pode usar um preset MoA como entrada de contingência em `fallback_providers` (`provider: moa`) para que o conselho assuma automaticamente caso seu provedor primário falhe.[1] E vale notar que o Hermes Agent segue evoluindo rapidamente na gestão de cache: no release **v0.23.3** (19/11/2026), o sistema ganhou um controlador dedicado de ciclo de vida de *prompt cache* (`prompt_caching.cache_ttl: auto`) e suporte aos novos modelos GPT-6.2 Astra e Sol.[2]

---

## Segurança, Privacidade e Cache Intacto

Dois detalhes de engenharia tornam o MoA seguro para ambientes corporativos:

- **Privacy Filter (`moa.privacy_filter`):** Pode mascarar e-mails, telefones formatados, prefixos de chaves de API, JWTs e strings de conexão de banco antes de exibir os blocos de referência na interface (`display`) ou até mesmo antes de injetá-los no agregador (`full`).[1]
- **Preservação do Prompt Caching:** Como as orientações dos consultores são inseridas como uma mensagem final separada na cauda da conversa (*tail*), o prefixo histórico (prompt de sistema, ferramentas e mensagens anteriores) permanece idêntico byte a byte, evitando que o cache do agregador seja invalidado a cada turno.[1]

---

Quer dominar a arquitetura de agentes autônomos em produção — da configuração de infraestrutura em VPS até orquestração avançada de múltiplos modelos e governança corporativa? Conheça a comunidade e o programa completo em **[Inteligência Agêntica](https://inteligenciaagentica.com.br)**.
## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents — Mixture of Agents | Hermes Agent Docs
[2] https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.3 — Hermes Agent v0.23.3 Release Notes
