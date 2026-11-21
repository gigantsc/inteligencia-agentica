---
title: "Context Files e Context References no Hermes Agent: Regras por Projeto, Zero Desperdício e Segurança"
date: "2026-11-21"
lastmod: "2026-11-21"
summary: "Aprenda a usar Context Files (.hermes.md, AGENTS.md e AGENTS.override.md) e Context References (@file, @folder, @diff, @url) no Hermes Agent para injetar contexto cirúrgico, preservar o prompt caching e bloquear vazamentos de credenciais."
tags: ["Hermes Agent", "Context Engineering", "AGENTS.md", "Produtividade", "Segurança", "Agentes de IA"]
keywords: ["context files hermes agent", "context references @file", "AGENTS.md hermes", ".hermes.md", "prompt caching ia", "governança agentes ia"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/context-files-context-references-hermes.jpg"
draft: false
---

> **Em resumo:** No **Hermes Agent**, os **Context Files** (`.hermes.md`, `AGENTS.md` e `AGENTS.override.md`) carregam automaticamente as regras de cada projeto com descoberta progressiva por subdiretório e varredura anti-*prompt injection*, enquanto as **Context References** (`@file`, `@folder`, `@diff`, `@staged`, `@git:N` e `@url`) injetam contexto cirúrgico direto na mensagem com trava automática para credenciais como `.env` e chaves SSH.[1][2]

Quando uma empresa começa a operar agentes de IA em projetos reais — sistemas financeiros, lojas virtuais, automações de backoffice ou monorepos com múltiplas equipes — surgem três gargalos imediatos:

1. **O agente esquece as regras específicas de cada projeto** (ou mistura padrões do setor financeiro com os do marketing).
2. **O custo de tokens dispara** porque o operador cola arquivos inteiros no chat ou carrega instruções gigantescas no prompt inicial mesmo quando não são necessárias.
3. **Risco silencioso de segurança:** alguém anexa um diretório errado e expõe `.env`, chaves SSH ou aceita um arquivo malicioso com instruções ocultas (*prompt injection*).

O Hermes Agent resolve esses três problemas de forma nativa combinando duas camadas complementares: **Context Files** (regras estruturais carregadas automaticamente) e **Context References** (anexos cirúrgicos sob demanda via `@`).[1][2]

---

## 1. Context Files: Como o Hermes Entende Cada Projeto Sem Inflar o Prompt

Diferente de chatbots comuns em que você precisa repetir "lembre que este projeto usa PostgreSQL e nunca altere migrações", o Hermes Agent descobre e carrega arquivos de contexto diretamente do diretório de trabalho.[1]

### Hierarquia e Prioridade de Carregamento

Apenas **um** tipo de arquivo de contexto de projeto é carregado por diretório (vence o primeiro encontrado nesta ordem), enquanto o `SOUL.md` permanece global e independente para toda a instância do Hermes em `$HERMES_HOME/SOUL.md`:[1]

| Arquivo | Escopo e Função | Descoberta |
|---|---|---|
| `SOUL.md` | Identidade, tom e estilo globais do agente | Apenas `$HERMES_HOME/SOUL.md` (não busca no projeto) [1] |
| `.hermes.md` / `HERMES.md` | Instruções de projeto com maior prioridade | Sobe até a raiz do repositório Git [1] |
| `AGENTS.override.md` | Sobrescrita pessoal/local (geralmente no `.gitignore`) | CWD na inicialização + subdiretórios progressivos [1] |
| `AGENTS.md` | Convenções, arquitetura e restrições do projeto | CWD na inicialização + subdiretórios progressivos [1] |
| `CLAUDE.md` | Compatibilidade nativa com projetos Claude Code | CWD na inicialização + subdiretórios progressivos [1] |
| `.cursorrules` / `.cursor/rules/*.mdc` | Compatibilidade com regras do Cursor IDE | Apenas diretório atual (CWD) [1] |

Se existir um `AGENTS.override.md` ao lado de um `AGENTS.md`, o Hermes carrega o arquivo de sobrescrita **no lugar** do arquivo versionado no Git — recurso ideal para gestores e desenvolvedores manterem ajustes individuais sem sujar o repositório da equipe.[1]

### Cadeia de Diretórios e Descoberta Progressiva

Em empresas com monorepos (por exemplo, um único repositório contendo `/financeiro`, `/frontend` e `/backend`), carregar tudo no início desperdiça janela de contexto e quebra o reaproveitamento de cache.[1]

```
empresa-monorepo/ (raiz Git)
├── AGENTS.md                 <-- Carregado na inicialização (regras gerais da empresa)
├── financeiro/
│   └── AGENTS.md             <-- Descoberto só quando o agente lê arquivos de /financeiro
├── frontend/
│   └── AGENTS.md             <-- Descoberto só quando o agente lê arquivos de /frontend
└── backend/
    └── AGENTS.md             <-- Descoberto só quando o agente lê arquivos de /backend
```

O `SubdirectoryHintTracker` monitora os caminhos usados pelas ferramentas (`read_file`, `terminal`, `search_files`) e injeta o `AGENTS.md` do subdiretório **exatamente no momento em que o agente entra naquela pasta** — cada subdiretório é verificado no máximo uma vez por sessão, mantendo o prompt de sistema estável e o **Prompt Caching** intacto.[1]

Vale destacar que a preservação do *prompt cache* é hoje uma das maiores alavancas de redução de custos no Hermes: a partir da versão `v0.23.3`, o framework passou a contar inclusive com um controlador dedicado de ciclo de vida do cache (`prompt_caching.cache_ttl` com padrão `auto`) e poda proativa de resultados antigos de ferramentas.[3]

### Proteção Nativa Contra Prompt Injection

Todo arquivo de contexto de projeto passa por um scanner de segurança antes de entrar no prompt, bloqueando padrões como:[1]

- Tentativas de sobrescrever instruções (*"ignore previous instructions"*, *"system prompt override"*);
- Comentários HTML ocultos (`<!-- ignore instructions -->`) e blocos invisíveis (`<div style="display:none">`);
- Caracteres Unicode invisíveis (*zero-width spaces*, *bidirectional overrides*);
- Comandos suspeitos de exfiltração (`curl ... $API_KEY`, `cat .env`).

Se um repositório de terceiros tiver código malicioso escondido no `AGENTS.md`, o Hermes bloqueia o carregamento e exibe `[BLOCKED: AGENTS.md contained potential prompt injection ...]`.[1] Além disso, arquivos gigantes são truncados automaticamente (70% início, 20% fim, 10% marcador) com timeout padrão de leitura de 5 segundos (`context_file_read_timeout`) para não travar sessões em pastas sincronizadas na nuvem como OneDrive ou iCloud.[1]

---

## 2. Context References (`@`): Injeção Cirúrgica na Hora da Execução

Enquanto os **Context Files** definem as regras permanentes do projeto, as **Context References** permitem anexar evidências exatas na sua pergunta dentro da CLI interativa — basta digitar `@` para acionar o autocompletar.[2]

### Tabela Completa de Referências Suportadas

| Sintaxe | O que injeta na mensagem | Limites e Comportamento |
|---|---|---|
| `@file:caminho/arquivo.py` | Conteúdo completo do arquivo | Rejeita binários; respeita limites de contexto [2] |
| `@file:caminho/arquivo.py:10-25` | Apenas as linhas 10 a 25 (inclusivo) | Economia máxima de tokens em arquivos longos [2] |
| `@folder:caminho/pasta` | Árvore de diretórios com metadados | Máximo de 200 entradas (excesso vira `- ...`) [2] |
| `@diff` | Alterações não preparadas (`git diff`) | Ideal para revisão rápida antes do commit [2] |
| `@staged` | Alterações em stage (`git diff --staged`) | Revisão final pré-deploy [2] |
| `@git:5` | Últimos N commits com seus patches | Limitado entre 1 e 10 commits [2] |
| `@url:https://exemplo.com` | Conteúdo extraído da página web | Comparação rápida de documentações/artigos [2] |

### Exemplos Práticos no Dia a Dia da Operação

```text
# Auditoria cirúrgica sem gastar tokens com o arquivo inteiro
Analise a lógica de cálculo de comissão em @file:src/faturamento.py:120-165

# Revisão de segurança antes de subir para produção
Revise @diff e aponte possíveis falhas de validação ou exposição de dados

# Comparação de configurações sem copiar e colar
Compare @file:config/producao.yaml e @file:config/homologacao.yaml

# Mapeamento rápido de estrutura
Explique a organização desta pasta: @folder:automacoes/financeiro
```

Pontuações finais como vírgula, ponto ou interrogação após a referência são removidas automaticamente pelo parser do Hermes, permitindo escrever frases naturais como `Verifique @file:main.py, e também @file:tests.py.` sem quebrar o caminho.[2]

### Travas de Segurança e Limites de Janela

Para impedir que um anexo acidental estoure o orçamento de tokens ou vaze segredos da VPS/estação de trabalho, o Hermes aplica três barreiras rígidas:[2]

1. **Orçamento de contexto:** acima de **25%** da janela do modelo, emite um aviso; acima de **50%**, recusa a expansão e mantém a mensagem original intacta.[2]
2. **Proteção contra Path Traversal:** qualquer referência que resolva fora do workspace permitido é bloqueada.[2]
3. **Lista de bloqueio de credenciais:** arquivos e diretórios sensíveis como `~/.ssh/`, `~/.aws/`, `~/.gnupg/`, `~/.kube/`, `~/.netrc`, `~/.pgpass` e `$HERMES_HOME/.env` são **sempre bloqueados** para `@file:` — mesmo que o operador tente anexá-los por engano.[2]

> **Nota de plataforma:** As referências `@` são expandidas diretamente na CLI interativa; em canais de mensageria como Telegram ou WhatsApp, o gateway repassa o texto como está, e o agente utiliza suas ferramentas internas (`read_file`, `search_files`, `web_extract`) para buscar o conteúdo quando necessário.[2]

---

## 3. Fluxo Recomendado para Empresas e Equipes

Para extrair o máximo de previsibilidade e menor custo por tarefa no Hermes Agent, combine os dois recursos em um fluxo simples:

```
+-------------------------------------------------------------------+
| 1. IDENTIDADE GLOBAL ($HERMES_HOME/SOUL.md)                       |
|    Tom executivo, idioma PT-BR, regras gerais de comunicação      |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 2. REGRAS DO PROJETO (AGENTS.md / .hermes.md + subdiretórios)     |
|    Stack, portas, convenções, o que NUNCA alterar (ex: migrações) |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 3. CONTEXTO CIRÚRGICO SOB DEMANDA (@file:linhas, @diff, @folder)  |
|    Injeta apenas o trecho exato da tarefa, sem estourar tokens    |
+-------------------------------------------------------------------+
```

Essa separação evita o erro clássico de transformar o prompt do sistema em um "manual de 40 páginas" que encarece cada turno de conversa. Regras globais ficam no `SOUL.md`, regras do projeto ficam no `AGENTS.md` (carregadas progressivamente por pasta) e os dados da tarefa entram na hora certa via `@`.[1][2]

---

## Conclusão

Dominar **Context Files** e **Context References** marca a diferença entre usar um agente de IA de forma amadora — repetindo instruções e pagando caro por contexto inútil — e operar uma infraestrutura disciplinada, segura e previsível. Com hierarquia clara entre `SOUL.md` e `AGENTS.md`, descoberta progressiva que preserva o *Prompt Cache* e travas automáticas contra *prompt injection* e vazamento de credenciais, sua equipe ganha velocidade sem abrir mão da governança.[1][2]

Quer implementar o Hermes Agent com arquitetura profissional de contexto, automações 24/7 e governança real na sua empresa? Conheça a comunidade e a formação **Inteligência Agêntica** em [https://inteligenciaagentica.com.br](https://inteligenciaagentica.com.br).

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files — Context Files | Hermes Agent
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references — Context References | Hermes Agent
[3] https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.3 — Hermes Agent v0.23.3 Release
