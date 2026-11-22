---
title: "Hermes Web Dashboard: A Central de Comando Visual para Gerenciar Agentes de IA Sem Depender do Terminal"
date: "2026-11-22"
lastmod: "2026-11-22"
summary: "O Hermes Web Dashboard (hermes dashboard) reúne em uma interface web local ou remota (porta 9119) o controle de múltiplos perfis, chaves de API, servidores MCP, pareamento de canais como WhatsApp e Telegram, busca de sessões em FTS5 e autenticação obrigatória para acesso remoto seguro."
tags: ["Hermes Agent", "Web Dashboard", "Gestão de Agentes", "MCP", "Segurança", "Automação"]
keywords: ["hermes dashboard", "painel web agentes de IA", "gerenciamento multi-perfil hermes", "oauth nous portal", "tailscale agente ia"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/hermes-web-dashboard-central-comando-agentes-ia.jpg"
draft: false
---

> **Em resumo:** O **Hermes Web Dashboard** (`hermes dashboard`) é o painel administrativo em navegador do Hermes Agent, servido por padrão em `http://127.0.0.1:9119` com FastAPI e Uvicorn.[1] A partir de uma única interface, gestores e equipes técnicas configuram chaves de API, testam servidores MCP, aprovam usuários no WhatsApp e Telegram, auditam históricos de conversas com busca full-text (FTS5) e alternam entre múltiplos perfis isolados sem editar arquivos YAML manualmente.[1]

---

## Por que um painel visual mudou o jogo para quem opera agentes 24/7

Empresas que escalam automações com IA descobrem rápido um gargalo operacional: manter agentes rodando em servidores VPS exige ajustes constantes de chaves, permissões de canais, tarefas agendadas e conectores externos. Fazer cada verificação via SSH e edição manual de `config.yaml` cria dependência de especialistas e aumenta o risco de erro humano.[1]

Ao mesmo tempo, a governança de provedores tornou-se crítica. Em comunicado publicado em 22 de novembro de 2026, a OpenRouter revelou incidentes de processamento de dados em provedores de inferência terceirizados, levando ao desligamento de três provedores e à remoção preventiva de 125 endpoints da lista de *Zero Data Retention* (ZDR).[4] Ter uma central visual onde o gestor enxerga rapidamente quais modelos, chaves e conectores estão ativos deixou de ser conveniência para virar requisito de operação.[1][4]

```
+-------------------------------------------------------------------+
|               HERMES WEB DASHBOARD (127.0.0.1:9119)               |
+---------------------------+---------------------------------------+
|  Seletor de Perfis        |  Abas Administrativas                 |
|  (?profile=financeiro)    |  • Status & Alerta de Disco (<512 MB) |
|                           |  • Chat (resumo TUI / --resume)       |
|  [Banner Âmbar quando     |  • Sessions (FTS5 + export JSON)      |
|   gerencia outro perfil]  |  • Profiles (/profiles/new Builder)   |
|                           |  • MCP (Add, Enable/Disable, Test)    |
|                           |  • Channels & Pairing (19+ canais)    |
|                           |  • Webhooks & Cron Jobs (PUT /cron)   |
+---------------------------+---------------------------------------+
```

---

## Como iniciar e operar múltiplos perfis em um único servidor

O comando básico para subir o painel localmente é direto e não envia dados para fora da máquina:[1]

```bash
hermes dashboard
```

Por padrão, o servidor escuta em `127.0.0.1:9119` e abre o navegador automaticamente.[1] Para ambientes de servidor ou portas customizadas, o comando aceita flags específicas:[1]

| Flag | Padrão | Função prática na operação |
|---|---|---|
| `--port` | `9119` | Define uma porta alternativa (ex.: `--port 8080`) [1] |
| `--host` | `127.0.0.1` | Endereço de escuta (`0.0.0.0` ou IP da VPN Tailscale) [1] |
| `--no-open` | Desligado | Sobe o painel em servidores headless sem abrir navegador [1] |
| `--isolated` | Desligado | Isola o servidor para um único perfil ao rodar `<perfil> dashboard` [1] |
| `--insecure` | Obsoleto (*no-op*) | Não desativa mais a autenticação em binds não-locais [1] |

Uma vantagem decisiva para empresas com vários departamentos é que o dashboard atua em **nível de máquina**: um único processo gerencia todos os perfis instalados.[1] Quando há mais de um perfil, um seletor na barra lateral sincroniza a URL (`?profile=worker`) para que configurações, chaves de API, *skills*, servidores MCP e a aba de chat operem exatamente sobre o departamento selecionado.[1] Sempre que um perfil secundário está ativo, um banner âmbar sinaliza o alvo de escrita para evitar alterações acidentais no perfil errado.[1]

---

## O que você controla pelo navegador sem tocar em YAML

As abas nativas do `hermes dashboard` cobrem todo o ciclo de vida operacional do agente:[1]

- **Status e Pressão de Recursos:** Exibe alertas automáticos de espaço em disco no volume de `~/.hermes` (nível elevado abaixo de 512 MB livres e crítico abaixo de 256 MB), evitando que logs ou bancos de sessão parem a operação silenciosamente.[1]
- **Sessions com Busca FTS5:** Separa conversas humanas (*Chats*), execuções automáticas (*Automation* — cron, webhooks, API) ou todas juntas (*All*), permitindo busca textual completa com destaque de trechos, exportação em JSON (`GET /api/sessions/{id}/export`) e limpeza de sessões antigas (`POST /api/sessions/prune`).[1]
- **Chat Integrado com Retomada:** Permite clicar em qualquer sessão na aba *Sessions* para saltar para `/chat?resume=<id>` com o histórico completo carregado.[1]
- **MCP Sem Linha de Comando:** Cadastra servidores HTTP/SSE ou `stdio`, ativa ou desativa integrações sem apagá-las, oculta valores com formato de segredo na listagem e executa o botão **Test** (`POST /api/mcp/servers/{name}/test`) para listar ferramentas antes de colocar o conector em produção.[1]
- **Channels, Pairing e Webhooks:** Centraliza o status de conexão de canais como Telegram, WhatsApp, Slack, Discord, Microsoft Teams, E-mail e SMS (mais de 19 plataformas nativas na documentação oficial), além de aprovar ou revogar usuários pareados sem precisar rodar `hermes pairing` no terminal.[1][5]
- **Profile Builder (`/profiles/new`):** Cria novos perfis corporativos do zero ou clonando configurações, escolhendo modelo, MCPs e *skills* de forma guiada.[1]

---

## Segurança no acesso remoto: Auth Gate, Tailscale e OAuth

Como o `hermes dashboard` lê e grava o arquivo `.env` (chaves de API) e pode disparar comandos do agente, o Hermes Agent aplica uma trava rígida de segurança: **qualquer tentativa de vincular o servidor fora de `127.0.0.1` / `localhost` ativa obrigatoriamente o *Auth Gate***.[1] A antiga flag `--insecure` foi desativada e não remove mais a exigência de login.[1]

| Provedor de Autenticação | Como funciona | Cenário recomendado |
|---|---|---|
| **Nous Portal OAuth (`nous`)** | Fluxo Authorization Code + PKCE (S256) registrado via `hermes dashboard register` (tokens de 15 min) [1] | Servidores expostos na internet pública e conexão remota do **Hermes Desktop** [1] |
| **Usuário e Senha (`basic`)** | Login local com hash `scrypt` (`password_hash`), cookies HMAC e bloqueio de força bruta (10 tentativas/min por IP) [1] | Redes internas confiáveis ou acesso exclusivo via **VPN Tailscale** (`--host <ip-tailscale>`) [1] |
| **OIDC Corporativo (`self_hosted`)** | Integração OpenID Connect com Okta, Microsoft Entra ou Google Workspace via HTTPS [1] | Empresas com provedor de identidade corporativo já padronizado [1] |

Para gestores que mantêm uma VPS na nuvem, a arquitetura mais simples e segura consiste em manter o dashboard atrás de uma rede privada **Tailscale** ou registrar o cliente OAuth com `hermes dashboard register` e conectar o aplicativo **Hermes Desktop** em *Settings → Gateways → Remote gateway*.[1]

---

## Extensibilidade sem fork e evolução contínua (v0.23.3)

Para operações que exigem painéis sob medida, o dashboard suporta três camadas de extensão carregadas em tempo de execução sem alterar o código-fonte:[2]

1. **Temas YAML:** Arquivos em `~/.hermes/dashboard-themes/` ajustam paleta de cores, tipografia e modos de layout (`standard`, `cockpit` ou `tiled`).[2]
2. **Plugins de Interface (UI):** Bundles JavaScript com `manifest.json` adicionam novas abas ou injetam widgets em páginas existentes via `window.__HERMES_PLUGIN_SDK__`.[2]
3. **Rotas Backend em FastAPI:** Arquivos `plugin_api.py` expõem endpoints próprios sob `/api/plugins/` consumidos pela interface do plugin.[2]

Essa base administrativa apoia as melhorias de infraestrutura entregues no release `v0.23.3` (19/11/2026) e nos builds canary subsequentes, que introduziram o controlador de ciclo de vida do *Prompt Cache* (mantendo o cache aquecido em execuções longas e compactando conversas ociosas antes do limite de 1 hora), poda proativa de resultados de ferramentas e uma camada de persistência desacoplada sobre SQLite.[3]

---

## Próximo passo prático na sua operação

Se você já roda o Hermes Agent em máquina local ou VPS, execute `hermes dashboard` para auditar hoje mesmo seus perfis, testar seus servidores MCP e verificar o consumo de disco do ambiente.[1] Para acesso remoto da sua equipe com segurança corporativa, combine `hermes dashboard --host <ip-tailscale> --no-open` ou habilite o login via Nous Portal OAuth.[1]

Quer dominar a arquitetura completa de agentes autônomos em produção, da infraestrutura na VPS à governança de custos e segurança? Conheça a comunidade e o ecossistema **[Inteligência Agêntica](https://inteligenciaagentica.com.br)**.

## Sources
[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
[3] https://github.com/NousResearch/hermes-agent/releases
[4] https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/
[5] https://hermes-agent.nousresearch.com/docs/llms.txt
