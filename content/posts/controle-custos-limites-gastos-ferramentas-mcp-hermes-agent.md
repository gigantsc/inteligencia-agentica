---
title: "Como Controlar Custos de Ferramentas MCP no Hermes Agent: Limites por Conversa"
date: "2026-11-13"
lastmod: "2026-11-13"
summary: "O Hermes Agent permite declarar quanto cada ferramenta MCP custa e definir um limite por conversa. Quando uma chamada ultrapassa o teto, o agente pede autorização; isso reduz surpresas em ferramentas pagas, mas não substitui o controle da fatura, do orçamento diário ou do consumo de tokens."
tags: ["Agentes de IA", "Hermes Agent", "MCP", "Controle de Custos", "Automação"]
keywords: ["limite de gastos MCP Hermes", "custo de ferramentas MCP", "controle financeiro agente IA"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/mcp-model-context-protocol-hermes.jpg"
draft: true
---

> **Resposta Rápida (Answer-First / GEO):** No Hermes Agent, um servidor MCP pode declarar o custo de cada ferramenta e um limite de gastos por conversa. Antes de uma chamada que exceda esse limite, o Hermes pede autorização — inclusive no modo YOLO; em uma execução sem aprovador, como um cron, a chamada é recusada.[1][2] O limite não é teto financeiro consolidado de todas as conversas ou de todos os servidores.[2][3]

## O risco financeiro escondido nas integrações

Conectar o agente a um serviço externo é útil: ele pode gerar mídia, consultar APIs pagas ou acionar serviços de terceiros.[1][2] Mas, em algumas integrações, cada chamada pode consumir créditos ou gerar cobrança.[1][2] Sem um limite visível, uma automação pode repetir ações ou executar chamadas dispendiosas sem que a pessoa responsável esteja acompanhando — um risco operacional a avaliar em cada integração.

A partir do Hermes Agent v0.23.0, configurações de servidor MCP podem declarar custos por ferramenta e um `spend_limit` por conversa.[1][2][3] O Hermes apresenta o valor informado no fluxo de autorização e mantém um acumulado da conversa para decidir se a próxima chamada precisa de aprovação.[1][2]

> **Em termos de gestão:** você configura um limite operacional para as ferramentas MCP tarifadas que declarou. Não é uma trava universal de gastos do modelo, da API, da empresa ou de todos os servidores conectados.[2]

## O que o recurso controla — e o que não controla

| Item | Controle de custos MCP do Hermes | Limite importante |
|---|---|---|
| Ferramenta MCP com custo declarado | Mostra custo e contabiliza chamadas autorizadas/iniciadas | Custos precisam estar declarados corretamente pelo administrador |
| Limite por conversa e servidor | Solicita autorização se a chamada ultrapassar o teto | Não é um limite financeiro agregado de toda a conta |
| Ferramenta sem custo declarado | Não é afetada pelo contador de gastos MCP | Pode continuar tendo custo cobrado externamente |
| Uso de tokens do modelo | Não é descrito como parte de `spend_limit` | Exige medição e controle próprios |
| Fatura do fornecedor | Não é substituída por esse mecanismo | Conferir sempre no painel do fornecedor |

O contador usa o custo declarado; no caso de uma faixa, contabiliza o maior valor.[2] Chamadas recusadas ou bloqueadas não entram no total. Uma chamada aprovada e iniciada pode ser contabilizada mesmo se o servidor falhar antes de recebê-la, uma escolha conservadora para evitar subestimar o uso.[2]

## Como configurar a política de gastos

Os campos são configurados por servidor em `mcp_servers` no arquivo `config.yaml`.[2][3] Os nomes das ferramentas em `tool_costs` precisam ser os nomes que o próprio servidor MCP oferece.[2][3] Um exemplo didático, baseado na estrutura documentada, seria:

```yaml
mcp_servers:
  renderizador:
    command: "render-mcp"
    trust: untrusted
    tool_costs:
      criar_imagem: 20
      animar: {credits: [5, 20], note: "por animação"}
      consultar_status: 0
    spend_limit: 100
    cost_unit: credits
```

Os nomes `renderizador`, `criar_imagem` e `animar` acima são ilustrativos; substitua-os pelos nomes reais e pelos custos publicados pelo seu servidor.[2][3] A referência aceita custo numérico não negativo, faixa ou objeto com `credits` e nota, além de `spend_limit` e `cost_unit`.[2][3]

### A lógica operacional

```text
MCP recebe chamada
        │
        ├─ ferramenta sem custo declarado ──> segue a política de confiança normal
        │
        └─ ferramenta tarifada
                │
                ├─ acumulado + chamada <= teto ──> executa segundo trust/approval
                │
                └─ ultrapassaria teto ──> solicita aprovação
                                             ├─ aprovado: executa e registra custo declarado
                                             └─ negado/sem aprovador: não executa
```

A política de confiança e o limite de gastos são controles distintos.[2][3] Um servidor marcado como `untrusted` pode pedir autorização para ferramentas que escrevem; o limite de gastos continua exigindo confirmação quando a chamada tarifada cruzaria o teto, mesmo em YOLO.[2][3] Se a chamada acontecer em um cron ou `hermes chat -q`, onde não há uma pessoa para responder, a chamada acima do limite é recusada.[2][3]

## O contador tem escopo: conversa, não contabilidade corporativa

O acumulado acompanha a conversa quando ela continua sob um novo identificador por compactação de contexto ou `/branch`.[2] A nova conversa inicia outro total; em mensageria, o total pertence ao chat e permanece mesmo com `/new`.[2] Cada execução de cron tem seu próprio total.[2] Reiniciar Hermes limpa os totais mantidos em memória.[2]

| Situação | O que esperar |
|---|---|
| Continuação ou compactação da mesma conversa | O contador segue com a conversa |
| Nova conversa no Desktop/CLI | Começa um contador novo |
| Execução de cron separada | Cada execução tem um total independente |
| Reinício do Hermes | Os totais em memória são reiniciados |
| Serviço de terceiros cobra valor diferente do declarado | O sistema local pode divergir da cobrança real |

Essa distinção é importante para gestores: `spend_limit` reduz a chance de uma sequência de chamadas MCP declaradas ultrapassar o valor operacional definido naquela conversa.[2] Não produz um relatório financeiro por fornecedor, não contabiliza automaticamente ferramentas sem valor configurado e não consolida limites de várias conversas.[2] O valor que vale para a cobrança real continua sendo o registrado pelo provedor do serviço.[2]

## Boas práticas para a operação

1. **Cadastre custos com fonte:** use valores publicados pelo serviço ou verificados com o fornecedor; evite estimativas apresentadas como exatas.
2. **Dê nome claro à unidade:** configure `cost_unit` como créditos, requisições ou outra unidade que a equipe compreenda.[2][3]
3. **Comece com um servidor de teste:** valide o prompt, a contabilização e o que ocorre ao negar autorização antes de ligar a integração a fluxos reais.
4. **Proteja execuções sem supervisão:** configure limites coerentes e teste especificamente o que acontece em cron. Se não houver aprovador e a chamada cruzar o teto, ela não será executada.[2]
5. **Audite configurações:** erros de configuração nos campos de custo podem impedir o servidor de carregar, e nomes de ferramentas inválidos são indicados em avisos; trate esses sinais como falha de configuração, não como prova de que existe um orçamento efetivo.[2][3]
6. **Concilie com o fornecedor:** compare o uso declarado pelo Hermes com a fatura e o painel externo. Este mecanismo é um controle local por conversa, não o livro contábil da empresa.[2]

## MCP com previsibilidade, sem falsa sensação de teto total

O controle de custos por ferramenta é uma evolução útil na integração de agentes com serviços pagos: o operador pode ver valores, definir um limite por conversa e manter uma confirmação antes de ultrapassá-lo.[1][2] A segurança depende, porém, de valores configurados com cuidado e da compreensão do escopo: outras conversas, custos não declarados e consumo de tokens não passam a fazer parte desse limite por mágica.[2]

Na grade do curso, essa descoberta complementa o tema pendente **Integração com Servidores MCP**, que já prevê conectar agentes a bancos de dados, CRMs e APIs corporativas. Pode ser abordada junto da aula 3.5 (ferramentas) e dos Cron Jobs do Módulo 10 para discutir controle humano em operações pagas.

Para acompanhar aplicações reais e novas práticas de inteligência agêntica, participe da comunidade **Inteligência Agêntica**: https://inteligenciaagentica.com.br

## Sources

[1] https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0 — Hermes Agent v0.23.0 — The Hearth Release
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp — MCP — Hermes Agent official docs
[3] https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference — MCP Config Reference — Hermes Agent
