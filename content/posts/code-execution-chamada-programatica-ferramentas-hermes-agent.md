---
title: "Code Execution no Hermes Agent: Como Executar Workflows de 50 Passos em 1 Único Turno com Custo Quase Zero"
date: "2026-11-16"
lastmod: "2026-11-16"
summary: "Descubra como o execute_code e a chamada programática de ferramentas eliminam a explosão de contexto em agentes de IA, colapsando loops complexos em scripts Python locais com economia de até 95% de tokens."
tags: ["Code Execution", "Hermes Agent", "Automação", "Economia de Tokens", "Engenharia de Prompt", "Negócios"]
keywords: ["execute_code", "programmatic tool calling", "hermes agent", "economia de tokens", "ia agentica empresas", "chamada de ferramentas python", "react loop otimizacao"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/code-execution-chamada-programatica-hermes-v2.jpg"
draft: false
---

> **Em resumo:**  
> O **Code Execution** (chamada programática de ferramentas via ferramenta `execute_code`) é a capacidade de um agente autônomo escrever e executar scripts Python em tempo real na própria máquina ou VPS para orquestrar múltiplas ferramentas (`web_search`, `read_file`, `patch`, `terminal`) de forma programática. Ao contrário do padrão convencional ReAct — no qual cada ação gera uma resposta textual bruta de 20KB a 50KB que é reinjetada na janela de contexto do LLM a cada turno —, o `execute_code` roda loops, condicionais e filtros localmente em milissegundos via socket RPC interno. Somente o resultado final consolidado pelo comando `print()` é devolvido ao modelo de IA. Essa arquitetura reduz em até **95% o consumo de tokens**, encurta o tempo de execução de 4 minutos para 8 segundos e impede que o agente se perca em alucinações por excesso de ruído no histórico da conversa.

---

## O Paradoxo do Loop ReAct: Quando a Autonomia Custa Caro Demais

Nos últimos dois anos, a imensa maioria dos frameworks de agentes autônomos (como LangChain, AutoGen, CrewAI e assistentes tradicionais) adotou o consagrado padrão **ReAct (Reasoning + Acting)**. O funcionamento teórico parece elegante:
1. O usuário faz uma pergunta ou passa uma tarefa complexa;
2. O modelo de linguagem raciocina e decide chamar uma ferramenta (ex: buscar arquivos);
3. O sistema executa a ferramenta e devolve o texto bruto gerado;
4. O modelo lê a resposta, raciocina novamente e decide chamar outra ferramenta (ex: ler o primeiro arquivo);
5. O ciclo se repete até a tarefa ser considerada concluída.

Para tarefas triviais de 2 ou 3 passos, esse método funciona. Porém, quando você coloca um agente para rodar em uma operação corporativa real — como auditar 30 contratos em PDF, investigar 15 páginas de concorrentes para montar um relatório de inteligência de mercado ou refatorar 25 arquivos de código legado —, o padrão ReAct tradicional colapsa por três motivos fatais:

1. **Explosão Exponencial de Contexto:** Cada chamada de ferramenta traz retornos volumosos (JSONs imensos, dumps de logs, árvores de diretórios). Ao final de 20 turnos, o histórico acumulado ultrapassa 80.000 tokens. A cada novo turno, você paga para enviar esses 80.000 tokens novamente para a API do modelo.
2. **Latência Insuportável:** Cada turno exige uma requisição HTTP completa aos servidores de inferência (OpenRouter, Anthropic, Google). Vinte chamadas sequenciais com 6 a 12 segundos por turno totalizam entre 2 e 4 minutos de espera ociosa.
3. **Degradação Cognitiva (Context Rot):** Quanto mais dados intermediários inúteis (como tags HTML, metadados irrelevantes ou erros de parsing) poluem a janela de contexto, maior é a probabilidade de o modelo "alucinar", ignorar instruções originais do sistema ou esquecer a restrição que o usuário colocou no primeiro parágrafo.

```
PADRÃO TRADICIONAL (ReAct Sequencial — Alto Custo e Lentidão):
[Usuário] ──► [LLM: Turno 1] ──► Tool 1 (Search) ──► Retorno 40KB
                     ▲                                      │
                     └──────── Reinjeta 40KB no Contexto ───┘
              [LLM: Turno 2] ──► Tool 2 (Read Doc 1) ──► Retorno 30KB
                     ▲                                      │
                     └──────── Reinjeta 70KB acumulados ────┘
              [LLM: Turno 3] ──► Tool 3 (Read Doc 2) ──► Retorno 25KB
                     ▲                                      │
                     └──────── Reinjeta 95KB acumulados ────┘
              ... (Repete por 30 turnos = Custo de Tokens Astronômico)

PADRÃO HERMES AGENT (Programmatic Tool Calling via execute_code):
[Usuário] ──► [LLM: Turno Único]
                     │
                     ▼ (Gera script Python com loop e filtro)
              [Processo Python / Kernel Local]
                     │
                     ├─► RPC Socket ─► web_search() ──► Filtra em RAM
                     ├─► RPC Socket ─► read_file()   ──► Processa em RAM
                     ├─► RPC Socket ─► patch()       ──► Aplica em RAM
                     │
                     ▼ (Somente a saída print() retorna)
              [LLM recebe apenas o resumo executivo de 300 palavras]
              (Resultado: 1 Único Turno | 95% Menos Tokens | Execução em Segundos)
```

No ecossistema **Hermes Agent**, desenvolvido pela Nous Research, essa fragilidade foi solucionada com a implementação nativa de **Chamada Programática de Ferramentas** através da ferramenta `execute_code`.

---

## Como Funciona o `execute_code`: O Canal RPC Interno

Em vez de devolver o controle ao modelo a cada leitura de linha ou chamada de API, o Hermes Agent permite que o modelo gere um script Python completo contendo lógica procedural: laços de repetição (`for`), verificações condicionais (`if/else`), estruturas de dados em memória (`dict`, `list`) e tratamento de exceções (`try/except`).

Dentro desse script, o agente importa ferramentas do sistema exatamente como se fossem bibliotecas locais:

```python
from hermes_tools import web_search, web_extract, read_file, write_file, search_files, patch, terminal
```

Quando o script é disparado, o Hermes executa o código em um subprocesso dedicado na VPS corporativa e estabelece uma ponte de comunicação de altíssima velocidade:
- No **Linux e macOS**, a comunicação utiliza um **Unix Domain Socket** de latência quase zero;
- No **Windows**, onde sockets Unix apresentam variações de compatibilidade, o Hermes automaticamente aciona um socket TCP de loopback local (`127.0.0.1`), garantindo integridade idêntica.

### O Que Acontece Passo a Passo no Sistema
1. O agente decide consolidar o workflow e invoca `execute_code(code=...)`.
2. O Hermes cria um diretório temporário de isolamento e gera o módulo de stub `hermes_tools.py`.
3. O listener de RPC escuta os pedidos de ferramentas vindos do script.
4. Quando o script Python executa `search_files("*.conf")`, o pedido é serializado em JSON, viaja pelo socket local, é executado pelo núcleo do Hermes com as permissões da sessão e retorna o resultado em memória para a variável do Python.
5. O script itera sobre os 50 arquivos encontrados, faz filtros regex, seleciona apenas as 3 linhas relevantes de cada um e monta um dicionário final.
6. A função `print(json.dumps(resumo_final))` envia para o `stdout` estritamente o que importa.
7. **O contexto do LLM recebe unicamente o texto impresso no `print()`.** As centenas de kilobytes de arquivos lidos e descartados nunca chegaram a entrar na fatura de tokens da sua empresa.

---

## Comparativo Direto: ReAct Convencional vs. Programmatic Tool Calling

A tabela abaixo sintetiza o impacto financeiro e operacional de executar um fluxo típico de pesquisa e consolidação de dados em uma operação real:

| Dimensão de Análise | Padrão ReAct Tradicional (LangChain / CrewAI) | Programmatic Tool Calling (`execute_code`) | Impacto no Negócio |
|---|---|---|---|
| **Turnos de LLM** | 20 a 50 requisições sequenciais | 1 único turno consolidado | Redução de até 98% nas chamadas de rede |
| **Consumo Total de Tokens** | 80.000 a 150.000 tokens acumulados | 2.500 a 6.000 tokens totais | Economia direta de até 95% na fatura de API |
| **Tempo de Resposta (Latência)** | 120 a 300 segundos | 5 a 15 segundos | Respostas instantâneas para o usuário final |
| **Poluição de Janela de Contexto** | Altíssima (HTML, logs e JSONs brutos) | Zero (apenas o resultado do `print()`) | Máxima precisão e retenção das regras de negócio |
| **Tratamento de Exceções** | Depende de nova reinterpretação do LLM | Tratado diretamente no código (`try/except`) | Estabilidade determinística e menos falhas |
| **Governança de Custos** | Difícil de prever (loops podem se prolongar) | Travamento rígido por limite de chamadas locais | Previsibilidade orçamentária para a gestão |

---

## Stateful Session Kernel: A Memória RAM Viva entre Turnos

Uma das inovações mais poderosas do Hermes Agent é o **Session Kernel Persistente**. 

Em ferramentas convencionais de execução de código (como Code Interpreters de chatbots de navegador), cada execução ocorre em um ambiente descartável que destrói todas as variáveis assim que o script encerra. Se o agente carregar uma planilha de 50.000 linhas no Turno 1, ele é obrigado a recarregar o arquivo do zero no Turno 2 caso o usuário faça uma pergunta complementar.

No Hermes Agent, o `execute_code` em backend local mantém um **kernel Python persistente por sessão**:
- Bibliotecas importadas (`import pandas as pd`, `import sqlite3`) permanecem prontas para uso;
- Variáveis, tabelas e estruturas carregadas em memória persistem entre mensagens consecutivas do usuário;
- O agente pode carregar um extrato bancário de 100MB na memória RAM da VPS no primeiro comando e, em seguida, passar os próximos 30 minutos respondendo a dúvidas pontuais do diretor financeiro em frações de segundo, sem reprocessar o arquivo original e sem reenviar o documento pela rede.

```
ARQUITETURA DO SESSION KERNEL NO HERMES:

[Sessão do Usuário (CLI / Telegram / Desktop)]
                     │
         Turno 1: "Carregue a base de clientes e filtre inadimplentes"
                     ▼
         [execute_code] ──► Inicializa Kernel Python (PID 4082)
                             │
                             ├─► import pandas as pd
                             ├─► df = pd.read_csv('clientes.csv')  <── (120MB na RAM)
                             └─► df_inadimplentes = df[df['status'] == 'atraso']
                             │
         ◄───────────────────┴── print("Encontrados 48 clientes em atraso.")

         Turno 2: "Qual o total de dívida desses clientes?"
                     ▼
         [execute_code] ──► Reutiliza Kernel Ativo (PID 4082)
                             │
                             ├─► total = df_inadimplentes['valor'].sum()  <── (Sem re-leitura!)
                             └─► print(f"Total: R$ {total:,.2f}")
                             │
         ◄───────────────────┴── print("R$ 145.890,00")
```

Se o ambiente precisar ser limpo ou caso novas variáveis de sistema sejam adicionadas, o agente simplesmente passa a flag `reset: true`, reiniciando o interpretador com estado completamente novo.

---

## Modos de Execução: `project` vs. `strict`

Para atender tanto a flexibilidade operacional de pequenas equipes quanto as exigências de conformidade e segurança da informação de ambientes corporativos, o Hermes permite alternar o modo de execução no arquivo de configuração `~/.hermes/config.yaml`:

```yaml
# ~/.hermes/config.yaml
code_execution:
  mode: project        # "project" (padrão) ou "strict"
  timeout: 300         # Tempo limite máximo por script em segundos (padrão: 300)
  max_tool_calls: 50   # Teto máximo de chamadas RPC por script
```

### 1. Modo `project` (Pragmatismo e Integração Operacional)
- **Como opera:** O script é executado no diretório de trabalho atual da sessão (o mesmo utilizado pelo `terminal`), aproveitando o ambiente virtual ativo (`VIRTUAL_ENV` ou `CONDA_PREFIX`).
- **Vantagem:** O agente tem acesso imediato a todas as dependências instaladas no projeto da empresa (`pip install -r requirements.txt`), módulos locais desenvolvidos internamente e arquivos de dados no diretório corrente.
- **Indicação:** Ideal para fábricas de software agênticas, rotinas de desenvolvimento e automações internas da VPS.

### 2. Modo `strict` (Quarentena e Isolamento de Diretório)
- **Como opera:** O script é executado em um diretório temporário totalmente isolado da árvore do projeto, utilizando estritamente o interpretador Python do próprio Hermes (`sys.executable`).
- **Vantagem:** Impede que scripts de leitura acessem inadvertidamente arquivos sensíveis fora do escopo através de caminhos relativos mal calibrados, garantindo máxima reprodutibilidade.
- **Indicação:** Ideal para agentes que processam tarefas públicas, assistentes expostos ao atendimento externo de clientes ou triagens de dados não confiáveis.

---

## Governança Corporativa e Blindagem de Segurança

Executar código gerado por inteligência artificial em servidores de produção é um tema que exige rigor absoluto de governança. O Hermes Agent implementa salvaguardas que operam independentemente do modo escolhido:

### 1. Higienização Ativa de Variáveis de Ambiente (Environment Scrubbing)
Por padrão, o subprocesso onde o Python é executado tem suas variáveis de ambiente completamente limpas. Chaves de API mestras (OpenAI, Anthropic, OpenRouter), senhas de banco de dados e tokens de acesso são **removidos do ambiente do subprocesso**. Um script malicioso ou código alucinado não tem como ler `os.environ["OPENAI_API_KEY"]` para vazar dados. Somente as variáveis operacionais estritas (`HERMES_HOME`, `HERMES_PROFILE`, `HERMES_CONFIG`, `HERMES_ENV`) são repassadas. Caso um script específico precise de uma variável autorizada, o administrador deve declará-la expressamente na lista `terminal.env_passthrough` no `config.yaml`.

### 2. Guardrails Rígidos de Hardware e Recursos
- **Timeout Automático de 300 Segundos:** Se um script entrar em loop infinito matemático ou aguardar resposta de uma conexão travada, o Hermes envia um sinal `SIGTERM` e, após 5 segundos, elimina o processo com `SIGKILL`.
- **Teto de Captura de Stdout (50 KB):** Se o script acidentalmente imprimir um arquivo binário de 10 megabytes, o Hermes trunca a exibição no terminal para evitar colapso de memória, salva o dump completo no disco local (`~/.hermes/cache/exec/`) e devolve apenas o caminho para leitura paginada segura via `read_file`.
- **Teto de 50 Chamadas de Ferramentas por Execução:** Impede que um loop desenfreado sobrecarregue APIs externas ou o disco da máquina. Ao atingir 50 invocações de RPC, o canal é bloqueado e o erro é reportado com clareza.

---

## 3 Exemplos Reais de Automação com `execute_code`

### Caso 1: Varredura de Configurações e Auditoria de Segurança
Em vez de ler arquivo por arquivo em dezenas de turnos, o agente executa uma varredura completa em milissegundos:

```python
from hermes_tools import search_files, read_file
import json

# Localiza todos os arquivos de configuração do ecossistema
matches = search_files("password", path="/etc/app", file_glob="*.yaml", limit=25)
findings = []

for match in matches.get("matches", []):
    content = read_file(match["path"])
    lines = content.get("content", "").split("\n")
    for idx, line in enumerate(lines, 1):
        if "password:" in line.lower() and not line.strip().endswith("''"):
            findings.append({
                "file": match["path"],
                "line": idx,
                "alert": "Possível credencial em texto puro detectada"
            })

print(json.dumps(findings, indent=2))
```

### Caso 2: Pesquisa de Mercado com Deduplicação e Resumo em 1 Turno
O agente pesquisa notícias sobre um tema, baixa o conteúdo de 5 páginas concorrentes, remove ruídos de layout e entrega o briefing consolidado:

```python
from hermes_tools import web_search, web_extract
import json

search_res = web_search("novas regulamentações tributárias automação 2026", limit=5)
briefings = []

for item in search_res.get("data", {}).get("web", []):
    doc = web_extract([item["url"]])
    results = doc.get("results", [])
    if results and results[0].get("content"):
        texto_limpo = results[0]["content"][:600]
        briefings.append({
            "titulo": item["title"],
            "link": item["url"],
            "destaque": texto_limpo
        })

print(json.dumps(briefings, indent=2, ensure_ascii=False))
```

### Caso 3: Refatoração em Massa de Legado com Verificação de Erros
O agente corrige chamadas de bibliotecas depreciadas em 30 arquivos de backend em uma única passada atômica:

```python
from hermes_tools import search_files, patch

files = search_files("db_query_v1", path="src/", file_glob="*.py")
total_modificados = 0

for file_info in files.get("matches", []):
    res = patch(
        path=file_info["path"],
        old_string="db_query_v1(",
        new_string="db_query_v2(",
        replace_all=True
    )
    if "error" not in str(res).lower():
        total_modificados += 1

print(f"Refatoração concluída com sucesso em {total_modificados} arquivos.")
```

---

## Conclusão: Eficiência Técnica Transforma Custo em Vantagem Competitiva

Para quem utiliza agentes de IA apenas como brinquedo conversacional, gastar 50 turnos de LLM para ler três arquivos é uma ineficiência tolerável. Mas para empresários, gestores de tecnologia e analistas de infraestrutura que dependem de agentes rodando 24 horas por dia, 7 dias por semana em servidores VPS, essa diferença é o divisor de águas entre uma operação viável e um projeto inviabilizado pela fatura de tokens.

A chamada programática de ferramentas com `execute_code` transforma o agente de IA de um mero gerador de texto em um **verdadeiro orquestrador de engenharia de software**. Ao transferir o processamento bruto de dados para onde ele deve estar — no processador local da sua VPS —, você conquista velocidade em tempo real, precisão matemática e governança absoluta de custos.

Se você deseja dominar a instalação, configuração e automação de agentes corporativos resilientes com o ecossistema Hermes Agent, venha conhecer nossa formação completa na comunidade [Inteligência Agêntica](https://inteligenciaagentica.com.br).
