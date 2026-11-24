---
title: "Subscription Proxy e Nous Tool Gateway: Como Unificar Modelos, Busca Web, Voz e Navegadores em Uma Única Assinatura"
date: "2026-11-24"
lastmod: "2026-11-24"
summary: "Aprenda a eliminar a proliferação de faturas e chaves de API usando o Nous Tool Gateway e o Subscription Proxy (hermes proxy) para centralizar mais de 300 modelos, busca web, geração de imagens, voz e navegador em nuvem em um único login OAuth."
tags: ["Hermes Agent", "Subscription Proxy", "Nous Tool Gateway", "Agentes de IA", "FinOps", "Segurança", "Negócios"]
keywords: ["hermes proxy", "nous tool gateway", "subscription proxy", "nous portal", "centralizar chaves api ia", "hermes agent v0.23.4"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/subscription-proxy-tool-gateway-uma-assinatura-hermes-agent.jpg"
draft: false
---

> **Em resumo:** Em vez de contratar cinco fornecedores separados e espalhar dezenas de chaves estáticas em arquivos `.env`, o **Nous Tool Gateway** e o **Subscription Proxy** (`hermes proxy`) permitem centralizar mais de 300 modelos de fronteira, busca web, geração de imagens, síntese de voz (TTS) e automação de navegador na nuvem sob uma única assinatura OAuth — além de expor um servidor local OpenAI-compatível (`http://127.0.0.1:8645/v1`) para outros aplicativos da empresa sem precisar distribuir chaves de API [2][3][5].

---

## O Problema Silencioso da Proliferação de APIs nas Empresas

Quando um gestor ou equipe técnica decide colocar um agente de IA em produção para valer, a conta raramente para no modelo de linguagem. Para que o agente pesquise concorrentes, leia PDFs, gere relatórios em áudio no Telegram e preencha formulários web, a operação acaba acumulando um mosaico caro e frágil de fornecedores:

1. Uma conta na OpenAI ou Anthropic para raciocínio;
2. Uma assinatura de busca web (Tavily, Firecrawl ou similar);
3. Uma conta na FAL.ai ou equivalente para geração de imagens;
4. Uma chave separada de Text-to-Speech (TTS) para notas de voz;
5. Um serviço de navegador headless na nuvem (como Browserbase);
6. E, muitas vezes, um segundo lote de chaves para aplicativos internos como Open WebUI, OpenViking ou Karakeep [2][3][5].

O resultado prático é previsível: **cinco faturas diferentes**, **cinco painéis de cobrança**, risco constante de uma automação parar por falta de saldo em um dos cartões e arquivos `.env` recheados de credenciais de longa duração espalhadas por servidores [3][5].

É exatamente esse gargalo que o ecossistema **Nous Portal** — composto pelo **Nous Tool Gateway** e pelo **Subscription Proxy** (`hermes proxy`) — resolve nativamente dentro do Hermes Agent [2][3][5].

---

## Arquitetura Unificada: Como Tudo se Conecta

Em vez de cada ferramenta ou aplicativo externo guardar sua própria chave estática, o Hermes atua como **corretor de autenticação OAuth** (`~/.hermes/auth.json`), emitindo tokens JWT de curta duração por requisição e renovando-os em segundo plano antes que expirem [2][5].

```
+-----------------------------------------------------------------------+
|                    SUA EMPRESA / VPS DE PRODUÇÃO                      |
|                                                                       |
|  [ Open WebUI / Karakeep / OpenViking / Scripts Internos ]            |
|                         |                                             |
|                         v  (qualquer Bearer; sem chave estática)      |
|          +------------------------------+                             |
|          |  Subscription Proxy          |  http://127.0.0.1:8645/v1   |
|          |  (hermes proxy start)        |  (OpenAI-compatible)        |
|          +--------------+---------------+                             |
|                         |                                             |
|  [ Hermes Agent ]       |   OAuth Refresh Token (~/.hermes/auth.json) |
|  (CLI/Telegram/Cron) ---+---> JWT de curta duração (auto-refresh)     |
+-------------------------|---------------------------------------------+
                          |
                          v
+-----------------------------------------------------------------------+
|                    NOUS PORTAL & TOOL GATEWAY                         |
|                                                                       |
|  * 300+ Modelos (Claude, GPT, Gemini 4, DeepSeek, Qwen, Grok, Hermes) |
|  * Busca Web & Extração   * Imagens (Krea 3, FLUX 2, GPT Image...)    |
|  * Text-to-Speech (TTS)   * Cloud Browser (Browser Use via CDP)       |
|  * Terminal Serverless (Modal - add-on opcional)                      |
+-----------------------------------------------------------------------+
```

---

## 1. Nous Tool Gateway: Cinco Backends em Uma Única Assinatura

O **Nous Tool Gateway** vem incluído nas assinaturas pagas do Nous Portal (e em contas elegíveis com cota gratuita inicial de ferramentas) [3]. Ele roteia as chamadas de ferramentas do Hermes através de infraestrutura gerenciada pela Nous, mantendo a mesma qualidade dos provedores diretos, porém com faturamento consolidado [3][5]:

| Ferramenta | O que Entrega via Gateway | Substitui Conta Separada em |
|---|---|---|
| **Busca Web & Extração** | Pesquisa web agêntica e extração completa de páginas sem dor de cabeça com *rate limits* [3][5] | Provedores de Search API dedicados |
| **Geração de Imagens** | Catálogo unificado com **Krea 3**, **Krea 2**, **FLUX 2**, **GPT Image**, **Nano Banana Pro**, **Ideogram**, **Recraft** e **Qwen** [3][5] | Conta separada na FAL.ai / Krea |
| **Text-to-Speech (TTS)** | Vozes OpenAI TTS integradas à ferramenta `text_to_speech` para áudios no Telegram e pipelines [3][5] | Chave separada de áudio OpenAI |
| **Cloud Browser** | Sessões headless de Chromium via Browser Use controladas pelo `browser_exec` sobre CDP [3][5] | Conta separada no Browserbase |
| **Cloud Terminal (Add-on)** | Sandboxes serverless para execução remota via Modal (`hermes setup terminal`) [3][5] | Infraestrutura avulsa de sandbox |

### Sem Lock-in: O Modo *Mix-and-Match*

Um detalhe fundamental para gestores que já têm contratos ou créditos em algum fornecedor específico é que **o Tool Gateway não impõe aprisionamento** [3]. Pelo comando interativo `hermes tools`, você escolhe ferramenta por ferramenta o que vai pela **Nous Subscription** e o que continua usando sua chave própria (por exemplo: usar sua conta existente do Browserbase para navegador, mas rotear busca web e imagens pelo Portal) [3][5]. Suas chaves antigas no `.env` permanecem intactas e voltam a valer no instante em que você trocar o provedor de volta [3].

### Ativação e Inspeção Rápida

```bash
# Instalação nova: OAuth + modelo + Tool Gateway em um comando
hermes setup --portal

# Ou ativar por ferramenta em instalação existente
hermes tools

# Verificar o roteamento ativo e o catálogo do gateway
hermes portal info
hermes portal tools
```

Além disso, o catálogo de modelos acessíveis pelo Portal continua crescendo em ritmo acelerado — incluindo os recém-incorporados **Gemini 4 Hydrogen, Neon e Carbon** lançados na janela do **Hermes Agent v0.23.4** (novembro de 2026), além de famílias como Anthropic Claude, OpenAI GPT-5.x, DeepSeek V4 Pro, Qwen e xAI Grok [4][5].

---

## 2. Subscription Proxy (`hermes proxy`): Compartilhe Modelos com Outros Apps Sem Expor Chaves

Muitas empresas rodam ferramentas complementares ao lado do Hermes Agent: um **Open WebUI** para atendimento interno, um **OpenViking** como banco de contexto ou um **Karakeep** para resumir links e documentos [2]. Tradicionalmente, cada um desses softwares exige uma `OPENAI_API_KEY` estática gravada em arquivo de configuração.

O **Subscription Proxy** resolve isso com um servidor HTTP minimalista que roda localmente (`http://127.0.0.1:8645/v1`) [2]:

```bash
# 1. Autenticar uma única vez no Portal (salva o refresh token em ~/.hermes/auth.json)
hermes portal

# 2. Iniciar o proxy local
hermes proxy start
# Listening on: http://127.0.0.1:8645/v1
```

Qualquer aplicativo compatível com a API da OpenAI passa a apontar para `http://127.0.0.1:8645/v1` usando qualquer string simbólica como chave (ex.: `sk-unused`) [2]. O proxy ignora o cabeçalho `Authorization` enviado pelo cliente, anexa a credencial real da sua assinatura (`nous` ou `xai`) e cuida da renovação automática antes do vencimento [2].

### Subscription Proxy vs. API Server do Hermes

É comum confundir `hermes proxy` com o `api-server` do Hermes. Embora ambos falem HTTP OpenAI-compatível, eles servem propósitos distintos [2]:

| Critério | `hermes proxy` (Subscription Proxy) | Hermes API Server |
|---|---|---|
| **O que entrega** | Inferência pura do modelo (*passthrough*) [2] | O agente completo (ferramentas, memória e skills) [2] |
| **Caso de uso** | "Quero usar minha assinatura do Portal/xAI em outro app" [2] | "Quero usar o Hermes como backend agêntico" [2] |
| **Autenticação cliente** | Qualquer bearer (o proxy injeta a credencial real) [2] | Sua `API_SERVER_KEY` configurada [2] |
| **Execução de ferramentas** | Não — apenas repassa chamadas de modelo [2] | Sim — o agente executa ferramentas localmente [2] |

---

## 3. Segurança Operacional e Boas Práticas em Produção

Centralizar credenciais exige disciplina de segurança. A arquitetura do Hermes implementa proteções importantes por padrão:

* **Token de curta duração e quarentena automática:** Em vez de manter chaves estáticas de API no `.env`, o Hermes gera JWTs efêmeros a partir de `~/.hermes/auth.json` [5]. Se um refresh token for revogado no portal, ele entra em quarentena local para evitar tempestades de erros `401` e solicita reautenticação limpa (`hermes auth add nous`) [5].
* **Proteção contra requisições de navegador no Proxy:** Por padrão, `hermes proxy start` escuta apenas em `127.0.0.1`, recusa cabeçalhos `Host` estranhos e bloqueia requisições de páginas web (`Origin` externo ou `Sec-Fetch-Site` cross-site/same-site) [2].
* **Cuidado ao expor na rede local (`--host 0.0.0.0`):** Como o proxy aceita qualquer token bearer por design, jamais o exponha na internet aberta sem VPN, firewall ou proxy reverso com autenticação real [2].
* **Uso correto dos modelos Hermes 4:** Modelos como `Hermes-4-70B` e `Hermes-4-405B` possuem ótimo custo-benefício no Portal para pesquisa, raciocínio e uso via `hermes proxy` em ferramentas externas; porém, para o loop rápido de *tool calling* dentro do próprio agente, a Nous Research recomenda selecionar modelos agênticos dedicados via `/model` (como Claude Sonnet 4.6, GPT-5.5 Pro, Gemini ou DeepSeek) [5].
* **Múltiplas contas por conector:** Ao conectar aplicativos externos pelo Tool Gateway (como duas contas Gmail `work` e `home`), o Hermes exige nomes explícitos (`connector_alias`), evitando envios acidentais pela conta errada [3].

---

## Checklist Rápido de Implantação

1. Atualize seu ambiente para a versão mais recente (`hermes update`) para contar com o suporte aos novos modelos e correções da série **v0.23.4** [1][4].
2. Execute `hermes setup --portal` (ou `hermes portal` em instalações existentes) para autenticar sua conta via OAuth [5].
3. Rode `hermes tools` para definir quais capacidades (busca web, imagem, TTS, navegador) usarão a assinatura unificada e quais permanecerão com chaves próprias [3].
4. Valide o estado da arquitetura com `hermes portal info` e `hermes proxy status` [2][5].
5. Se utilizar Open WebUI, OpenViking ou Karakeep no mesmo servidor, suba `hermes proxy start` (via `tmux` ou `systemd`) e aponte os clientes para `http://127.0.0.1:8645/v1` [2].

---

Quer dominar a construção, governança e otimização de custos de agentes de IA em produção real? Conheça a comunidade e o treinamento completo em **[inteligenciaagentica.com.br](https://inteligenciaagentica.com.br)**.

## Sources

[1] https://github.com/NousResearch/hermes-agent/releases — Releases · NousResearch/hermes-agent (v0.23.4)
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/subscription-proxy — Subscription Proxy | Hermes Agent
[3] https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway — Nous Tool Gateway | Hermes Agent
[4] https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.4 — Release Hermes Agent v0.23.4
[5] https://hermes-agent.nousresearch.com/docs/integrations/nous-portal — Nous Portal | Hermes Agent
