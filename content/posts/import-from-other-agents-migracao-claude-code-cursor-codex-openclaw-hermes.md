---
title: "Import from Other Agents: Migre Claude Code, Cursor, Codex e OpenClaw para o Hermes em 1 Comando"
date: "2026-11-27"
lastmod: "2026-11-27"
summary: "Aprenda a migrar regras, memórias, servidores MCP, skills e rotinas do Claude Code, Cursor, OpenAI Codex CLI, OpenClaw, Grok Bot e OpenBot para o Hermes Agent sem recomeçar do zero e sem expor credenciais."
tags: ["Hermes Agent", "Migração", "Claude Code", "Cursor", "OpenClaw", "MCP", "Automação"]
keywords: ["hermes import-agent", "migrar claude code para hermes", "migrar cursor para hermes", "migrar openclaw", "agent-importers", "sincronização agentes ia"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/import-from-other-agents-migracao-claude-code-cursor-codex-openclaw-hermes.jpg"
draft: false
---

> **Em resumo:** O maior freio para empresas adotarem uma arquitetura agêntica 24/7 é o medo de perder meses de regras, *skills*, memórias e servidores MCP configurados em outras ferramentas. Com o plugin oficial **`agent-importers`** (`hermes import-agent` / `hermes migrate`), o Hermes Agent importa em um único comando ambientes inteiros do **Claude Code**, **OpenAI Codex CLI**, **Cursor**, **OpenClaw**, **Grok Bot** e **OpenBot** — com prévia obrigatória (`--dry-run`), bloqueio automático de credenciais sensíveis e sincronização contínua por hash (`--sync`).[1][2]

---

## O Custo Oculto do *Vendor Lock-in* em Ferramentas de IA

Empresários e líderes de tecnologia que começaram a usar IA no dia a dia enfrentam um problema silencioso: o conhecimento operacional da empresa fica espalhado em múltiplos silos.

A equipe de desenvolvimento mantém instruções em `CLAUDE.md` no **Claude Code** ou regras `.mdc` no **Cursor**.[1] O time de engenharia testa fluxos no **OpenAI Codex CLI** (`AGENTS.md` e `config.toml`), enquanto operações ou automações pessoais rodam rotinas no **OpenClaw**, **Grok Bot** ou **OpenBot**.[1][2]

Quando a empresa decide consolidar tudo em um agente autônomo rodando 24/7 em servidor próprio ou VPS com acesso a Telegram, WhatsApp, Slack e cron jobs, surge a objeção clássica: *"Vamos ter que reescrever tudo do zero?"*

A resposta no **Hermes Agent** é não.[1] O comando `hermes import-agent` (alimentado pelo plugin oficial `agent-importers` do catálogo mantido pela Nous Research) lê esses diretórios locais, exibe um plano item por item antes de gravar qualquer arquivo e traduz cada componente para a estrutura nativa do Hermes.[1]

---

## Arquitetura da Migração: Como Funciona o `agent-importers`

O processo segue três princípios de segurança operacional: **descoberta automática**, **auditoria prévia** e **isolamento de segredos**.[1][2]

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FONTES DETECTADAS AUTOMATICAMENTE                    │
│  ~/.claude (Claude Code)  │  ~/.codex (Codex CLI)  │  ~/.cursor (Cursor)│
│  ~/.openclaw (OpenClaw)   │  grok-bot-export.json  │  openbot.db        │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  PLUGIN OFICIAL: agent-importers                        │
│  1. Varredura + Plano detalhado (--dry-run não toca no disco)           │
│  2. Snapshot de segurança em ~/.hermes/backups/pre-migration-*.zip      │
│  3. Expurgo automático de chaves (*_TOKEN, *_API_KEY, Authorization)    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ MEMÓRIA & ALMA   │  │ REGRAS & MCP     │  │ SKILLS & CRON    │
│ MEMORY.md        │  │ config.yaml      │  │ skills/*-imports │
│ USER.md          │  │ command_allowlist│  │ Cron jobs        │
│ SOUL.md          │  │ mcp_servers      │  │ (pausados)       │
└──────────────────┘  └──────────────────┘  └──────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│             SINCRONIZAÇÃO CONTÍNUA (~/.hermes/import-sync.json)         │
│       hermes import-agent --sync  (atualiza apenas o que mudou)         │
└─────────────────────────────────────────────────────────────────────────┘
```

Em uma instalação nova, o próprio assistente `hermes setup` verifica automaticamente a existência dessas pastas no computador e pergunta se você deseja importar os dados encontrados antes mesmo de configurar provedores manualmente.[1] Em ambientes já configurados, basta rodar `hermes migrate` ou instalar o plugin manualmente:[1]

```bash
# Instalar o plugin oficial no perfil atual
hermes plugins install agent-importers

# Detectar automaticamente agentes instalados e exibir plano
hermes import-agent

# Apenas simular sem alterar nenhum arquivo no disco
hermes import-agent claude-code --dry-run
```

---

## O Que é Importado de Cada Plataforma

Cada ferramenta armazena contexto, permissões e integrações em formatos diferentes. A tabela abaixo resume o mapeamento exato executado pelo Hermes Agent:[1][2]

| Origem | Instruções & Memória | Permissões & MCP | Skills & Rotinas |
|---|---|---|---|
| **Claude Code** (`~/.claude`) | `CLAUDE.md` → `~/.hermes/memories/MEMORY.md`[1] | `settings.json` (`Bash(...)`) → `command_allowlist` / `approvals.deny`; `mcpServers` → `mcp_servers`[1] | `skills/<nome>/` → `skills/claude-code-imports/<nome>/`[1] |
| **Codex CLI** (`~/.codex`) | `AGENTS.md` e `memories/*.md` → `MEMORY.md`[1] | `config.toml` (`[mcp_servers.*]`) → `mcp_servers`[1] | `skills/<nome>/` → `skills/codex-imports/<nome>/`[1] |
| **Cursor** (`~/.cursor`) | `AGENTS.md` e `rules/*.md` / `.mdc` (remove frontmatter de roteamento) → `MEMORY.md`[1] | `mcp.json` (`mcpServers`) → `mcp_servers`[1] | `skills/**/<nome>/` → `skills/cursor-imports/<nome>/`[1] |
| **OpenClaw** (`~/.openclaw`) | `SOUL.md`, `USER.md`, `MEMORY.md` e `memory/*.md` (com merge e deduplicação)[2] | `mcp.servers.*` → `mcp_servers`; provedores, `max_turns`, `reasoning_effort`, TTS e Docker sandbox[2] | 4 diretórios de skills → `skills/openclaw-imports/`[2] |
| **Grok Bot** (`grok-bot-export.json`) | Papel do bot → `SOUL.md`; fatos e memória → `MEMORY.md` / `USER.md`[1] | URLs remotas de MCP → `mcp_servers`[1] | Rotinas agendadas → Cron jobs **pausados**; rotinas de evento documentadas em Markdown[1] |
| **OpenBot** (`openbot.db`) | Descrição → `SOUL.md`; memórias → `MEMORY.md` (leitura somente-leitura do banco)[1] | Servidores MCP → `config.yaml` (sem variáveis secretas)[1] | `~/OpenBot/Agents` → `skills/openbot-imports/`; rotinas → Cron jobs **pausados**[1] |

### Detalhes Importantes na Conversão

1. **Regras de Segurança do Claude Code:** Regras de terminal no formato `Bash(npm run test:*)` são convertidas automaticamente para globs equivalentes (`npm run test*`) no `command_allowlist` do Hermes.[1] Regras exclusivas de ferramentas proprietárias do Claude (`Read(...)`, `WebFetch`) são sinalizadas no relatório como não mapeadas, evitando falsas permissões.[1]
2. **Prevenção de Execução Duplicada (Grok Bot e OpenBot):** Ao importar rotinas agendadas do Grok Bot ou OpenBot, o Hermes cria os cron jobs no estado **pausado**.[1] Assim, o fluxo antigo e o novo não disparam ações duplicadas em paralelo. Quando estiver pronto para virar a chave, basta executar `hermes cron resume <id>` ou usar `--activate-routines` na importação.[1]
3. **Backup e Limpeza no OpenClaw:** Antes de aplicar mudanças na migração do OpenClaw (ou legados `~/.clawdbot` / `~/.moltbot`), o Hermes gera um arquivo de restauração em `~/.hermes/backups/pre-migration-*.zip`.[2] Após validar que tudo está operando, o comando `hermes claw cleanup` renomeia os diretórios antigos para `.pre-migration/`, evitando conflitos de estado.[2]

---

## Segurança: O Que Nunca é Importado Silenciosamente

Em operações corporativas, migrar configurações não pode significar copiar arquivos de credenciais sem critério. O `agent-importers` aplica regras rígidas de proteção:[1]

- **Arquivos de credenciais são ignorados:** `~/.claude/.credentials.json`, `~/.codex/auth.json` e `~/.cursor/cli-config.json` nunca são lidos.[1]
- **Expurgo de segredos em servidores MCP:** Variáveis de ambiente e cabeçalhos com nomes sensíveis (`*_TOKEN`, `*_API_KEY`, `Authorization`) são removidos durante a importação e listados no relatório final para que o administrador os adicione conscientemente em `~/.hermes/.env`.[1]
- **Exceção explícita no OpenClaw:** Chaves de API e tokens de bots (Telegram, Discord, Slack) só são migrados quando o operador informa explicitamente a flag `--migrate-secrets`.[2] Mesmo `--preset full` não copia segredos de forma silenciosa.[2]
- **Bloqueio de exportações inseguras no Grok Bot:** Se o JSON exportado contiver chaves com formato de credencial, o importador recusa o arquivo e aplica redação automática em textos com padrão de token.[1]

Para ambientes que desejam simplificar múltiplas chaves antigas após a migração, o Hermes também permite consolidar provedores via `hermes setup --portal`, centralizando acesso a modelos e ferramentas em uma única autenticação.[2]

---

## Sincronização Contínua (`--sync`): Use a IDE e Opere no Hermes

Um dos recursos mais subestimados do `agent-importers` é que ele não serve apenas para uma migração única de saída.[1]

Toda importação bem-sucedida de **Claude Code**, **Codex CLI** ou **Cursor** registra a origem e o resumo criptográfico (*digest*) de cada arquivo lido no manifesto `~/.hermes/import-sync.json`.[1]

Isso permite que sua equipe continue editando regras no Cursor ou adicionando skills no Claude Code durante a semana, enquanto o Hermes puxa apenas o que foi modificado:[1]

```bash
# Visualizar o que mudou desde a última importação
hermes import-agent --sync --dry-run

# Sincronizar apenas arquivos cujo digest mudou
hermes import-agent --sync
```

Como a verificação compara *digests* locais sem acionar modelos de linguagem, a operação é praticamente gratuita e determinística — podendo inclusive rodar como um cron job diário para manter o agente da empresa sempre alinhado às regras mais recentes dos repositórios.[1]

Além disso, o manifesto é isolado por perfil.[1] Ao clonar um ambiente departamental com `hermes profile create financeiro --clone --sync-imports`, o novo perfil herda o vínculo de sincronização e pode ser atualizado de forma independente via `hermes -p financeiro import-agent --sync`.[1]

---

## Checklist Prático de Migração para Empresas

Para realizar a transição sem interromper a operação atual, siga esta sequência validada:

1. **Simule primeiro:** Execute `hermes import-agent <agente> --dry-run` (ou `hermes import-agent` para detecção automática) e revise o plano de itens.[1]
2. **Separe por perfil se houver múltiplos bots:** Para Grok Bot ou OpenBot com vários assistentes especializados, direcione cada um para seu próprio perfil com `hermes -p <perfil> import-agent ...`.[1]
3. **Revise segredos e permissões:** Verifique a lista de variáveis de MCP removidas no relatório final e cadastre as chaves necessárias em `~/.hermes/.env`.[1]
4. **Valide conectividade e canais:** Execute `hermes status` para confirmar provedores e, no caso de WhatsApp (que usa pareamento por QR Code via Baileys), execute `hermes whatsapp`.[2]
5. **Ative rotinas somente após desativar a origem:** Desligue o agendamento na ferramenta anterior e libere os cron jobs importados com `hermes cron resume <id>`.[1]

Consolidar a inteligência operacional da empresa em uma infraestrutura única reduz retrabalho, elimina o risco de perder prompts críticos quando um colaborador troca de editor e dá à gestão controle real sobre custos, permissões e auditoria.

Se você quer estruturar agentes corporativos 24/7 com governança, segurança e foco em resultado operacional real, conheça a comunidade e o programa completo em **[inteligenciaagentica.com.br](https://inteligenciaagentica.com.br)**.

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents — Import from Other Agents | Hermes Agent
[2] https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw — Migrate from OpenClaw | Hermes Agent
