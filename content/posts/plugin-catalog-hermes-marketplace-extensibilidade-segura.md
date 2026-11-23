---
title: "Plugin Catalog e Hermes Marketplace: Como Expandir Agentes de IA com Segurança e Zero Gambiarra"
date: "2026-11-23"
lastmod: "2026-11-23"
summary: "O Plugin Catalog do Hermes Agent (hermes plugins) permite instalar extensões, servidores MCP e hooks de segurança com revisão humana, travamento por commit SHA de 40 caracteres e lista de revogação automática, eliminando riscos de código não auditado em produção."
tags: ["Hermes Agent", "Plugin Catalog", "Segurança", "MCP", "DevOps", "Automação"]
keywords: ["hermes plugins", "plugin catalog hermes agent", "hermes marketplace", "extensibilidade segura agentes ia", "security-guidance disk-cleanup"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/plugin-catalog-hermes-marketplace-extensibilidade-segura.jpg"
draft: false
---

> **Em resumo:** O **Plugin Catalog** do Hermes Agent (`hermes plugins install <nome>`) é um diretório curado e revisado por humanos que permite adicionar novas ferramentas, conectores MCP e hooks de governança aos seus agentes sem editar o código-fonte principal.[1][2] Cada entrada fixa um commit SHA exato de 40 caracteres, declara previamente todas as variáveis de ambiente e permissões necessárias, passa por scanner automatizado de segurança e conta com lista de bloqueio remoto (`removed.yaml`) caso algum pacote seja comprometido.[1]

---

## O problema real de "turbinar" agentes em produção

Quando uma empresa começa a usar agentes autônomos no dia a dia, logo aparece a necessidade de ir além das funções padrão: integrar um scanner de vulnerabilidades, limpar arquivos temporários na VPS, conectar um banco de memória diferente ou adicionar regras de auditoria antes de gravar arquivos.[2][3][4]

O caminho improvisado — clonar repositórios aleatórios da internet ou alterar o código interno do agente — costuma cobrar caro em operação:

1. **Risco na cadeia de suprimentos (*supply chain*):** instalar a partir de uma *branch* aberta significa que qualquer alteração futura do autor entra na sua máquina sem aviso.[1]
2. **Conflito entre extensões:** duas integrações que alteram funções internas do sistema (*monkeypatching*) quebram uma à outra e travam futuras atualizações.[1]
3. **Poluição de contexto e disco:** scripts e arquivos temporários acumulados em sessões contínuas consomem espaço e dificultam a auditoria.[3]

O **Plugin Catalog** e o **Hermes Marketplace** (`https://hermes-agent.nousresearch.com/marketplace`) nasceram exatamente para resolver esse dilema: dar velocidade de instalação com um comando, mantendo governança de nível corporativo.[1]

```
+-----------------------------------------------------------------------+
|              CICLO DE CONFIANÇA DO HERMES PLUGIN CATALOG              |
+-----------------------------------------------------------------------+
|  1. Submissão via PR       -> Revisão humana por mantenedores         |
|  2. Pinning Imutável       -> Trava em commit SHA de 40 caracteres    |
|  3. CI Security Scan       -> `hermes plugins validate` + lint SDK    |
|  4. Regra No Core Override -> Proibido sobrescrever módulos do core   |
|  5. Instalação Explícita   -> Mostra capacidades antes de clonar      |
|  6. Instalado != Ativado   -> Exige `hermes plugins enable <nome>`    |
|  7. Kill-Switch Remoto     -> `removed.yaml` bloqueia uso posterior   |
+-----------------------------------------------------------------------+
```

---

## Como funciona o modelo de confiança do Plugin Catalog

Diferente de diretórios abertos onde qualquer pessoa publica pacotes sem filtro, cada item do catálogo oficial é um arquivo YAML versionado na pasta `plugin-catalog/` do repositório do Hermes Agent.[1] Na prática, cinco travas protegem a empresa:[1]

| Camada de Proteção | O que faz na prática | Benefício operacional |
|---|---|---|
| **Pinning por SHA exato** | Instala o commit exato de 40 caracteres revisado, nunca a ponta da branch (`main`).[1] | Código novo do autor não entra em produção sem nova revisão.[1] |
| **Declaração de capacidades** | Lista ferramentas, hooks, middlewares e variáveis de ambiente (`requires_env`) antes do clone.[1][2] | O gestor enxerga o raio de impacto antes de aprovar.[1] |
| **No Core Override** | A validação em CI recusa código Python que reescreva módulos ou classes internas do Hermes em runtime.[1] | Atualizações do Hermes não quebram seus plugins.[1] |
| **Instalado != Ativado** | `install` apenas baixa os arquivos; o plugin só carrega após `enable` explícito.[1] | Zero execução surpresa ao testar novas extensões.[1] |
| **Lista `removed.yaml`** | Plugins removidos por incidente param de atualizar e são bloqueados ao carregar.[1] | Resposta rápida contra pacotes comprometidos.[1] |

Além disso, o catálogo classifica os itens em três níveis de origem (`tier`): `official` (mantidos pela Nous Research), `verified` (verificados junto à empresa fabricante da integração) e `community` (mantidos pela comunidade após revisão de PR).[1] O catálogo local também se atualiza automaticamente a cada 6 horas a partir do índice publicado na documentação oficial, garantindo que eventuais remoções de segurança cheguem aos servidores mesmo sem atualizar toda a versão do Hermes.[1]

---

## Comandos essenciais para gerenciar plugins no dia a dia

Toda a descoberta, inspeção e manutenção acontece direto pela linha de comando (ou pela aba de Plugins no Desktop e no Web Dashboard):[1]

```bash
# Buscar no catálogo oficial (por nome, descrição ou ferramenta)
hermes plugins search snyk

# Navegar por todo o catálogo ou ver detalhes de uma entrada
hermes plugins browse
hermes plugins info snyk

# Instalar a partir do SHA revisado e ativar no perfil atual
hermes plugins install snyk
hermes plugins enable snyk

# Atualizar entradas respeitando os novos SHAs revisados ou remover
hermes plugins update
hermes plugins disable snyk
hermes plugins remove snyk
```

Um detalhe importante de arquitetura para quem roda múltiplos projetos na mesma VPS: o *gateway* do Hermes descobre os plugins uma única vez para o processo e **não carrega** plugins locais escondidos dentro de pastas de projeto (`./.hermes/plugins/`).[2] Extensões devem ser instaladas no escopo do usuário (`~/.hermes/plugins/` ou via `hermes plugins install`) e ativadas por perfil, mantendo previsibilidade e controle centralizado.[2]

---

## Pacotes portáteis (MCP + Skill) e a expansão da série v0.23.x

Um dos avanços mais práticos do catálogo é suportar pacotes portáteis (*Agent Plugins v1*) que entregam, em uma única instalação, o conector técnico (servidor MCP `stdio`) e a instrução operacional (*skill*) de como o agente deve usá-lo:[1]

- **Exemplo `snyk`:** fixa a versão da CLI da Snyk (`npx -y snyk@<version> mcp`) junto com a skill `snyk-security-scan`, dando ao agente capacidade imediata de auditar código, dependências, containers e infraestrutura como código (IaC).[1]
- **Exemplo `touchdesigner`:** empacota o servidor MCP correspondente com a skill `touchdesigner-mcp` sob o identificador curto `td`.[1]

Nos releases recentes da série `v0.23.2+canary` e na trilha atual `v0.23.3` (incluindo o build `canary.20261123T065600Z-v0.23.3`), o ritmo de adições ao catálogo acelerou com novas opções voltadas a segurança, memória e voz, como `hermes-safeguard`, `barrier-shield`, `relatedb-memory`, `hermes-voice-gateway`, `scansift` e `covsift`.[4][5]

---

## Dois plugins nativos (*Built-in*) que toda operação deveria ativar

Além do catálogo externo, o Hermes já traz plugins embutidos (*opt-in*, desligados por padrão) que resolvem dores imediatas de infraestrutura e segurança com um único comando:[3]

### 1. `disk-cleanup` — Higiene automática da VPS
Rastreia arquivos efêmeros criados durante sessões (`test_*`, `tmp_*`, `*.test.*`) dentro de `HERMES_HOME` ou `/tmp/hermes-*` e executa limpeza segura ao encerrar a sessão (`on_session_end`), mantendo um log auditável em `cleanup.log` sem jamais tocar nas pastas de código ou projetos do usuário.[3]

```bash
hermes plugins enable disk-cleanup
# Dentro da sessão, use: /disk-cleanup status ou /disk-cleanup dry-run
```

### 2. `security-guidance` — Sentinela de 25 regras ao escrever arquivos
Inspirado nas regras do `claude-plugins-official` (licença Apache-2.0), monitora chamadas de `write_file`, `patch` e `skill_manage` em busca de padrões perigosos — como `eval(`, `pickle.load`, `subprocess(..., shell=True)`, `dangerouslySetInnerHTML`, verificação TLS desabilitada e injeção em workflows do GitHub Actions.[3] Por padrão, anexa um aviso para o agente corrigir o código; em ambientes rígidos, basta definir `SECURITY_GUIDANCE_BLOCK=1` para bloquear a escrita automaticamente.[3]

```bash
hermes plugins enable security-guidance
```

---

## Quando usar Plugin do Catálogo, Skill ou Servidor MCP?

Para evitar complexidade desnecessária na arquitetura da empresa, vale seguir uma regra simples de decisão:[1][2]

| Necessidade do Negócio | Melhor Mecanismo | Motivo |
|---|---|---|
| Ensinar um processo de negócio ou passo a passo ao agente | **Skill (`SKILL.md`)** | Leve, editável em texto e carregada sob demanda.[2] |
| Conectar a API/banco externo padrão (CRM, ERP, Postgres) | **Servidor MCP** | Protocolo padronizado de acesso a dados e ferramentas.[1] |
| Interceptar ciclo de vida (hooks `post_tool_call`), adicionar comandos `/slash`, UI ou empacotar MCP + Skill com SHA fixo | **Plugin (`hermes plugins`)** | Roda com hooks determinísticos, validação de catálogo e zero alteração no core.[1][2] |

---

## Próximo passo prático para sua operação

Antes de instalar qualquer integração externa por conta própria ou pedir para o agente improvisar scripts soltos, rode `hermes plugins browse` no seu ambiente, avalie os plugins nativos `disk-cleanup` e `security-guidance` e padronize novas extensões sempre pelo fluxo revisado do catálogo.[1][3]

Se você quer estruturar agentes autônomos com governança real, segurança e foco em resultado operacional para sua empresa, conheça a comunidade e o ecossistema **Inteligência Agêntica** em [inteligenciaagentica.com.br](https://inteligenciaagentica.com.br).

---

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog — Plugin Catalog | Hermes Agent
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins — Plugins | Hermes Agent
[3] https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins — Built-in Plugins | Hermes Agent
[4] https://github.com/NousResearch/hermes-agent/releases — Releases · NousResearch/hermes-agent
[5] https://github.com/NousResearch/hermes-agent/releases/tag/canary.20261123T065600Z-v0.23.3 — Hermes Agent canary.20261123T065600Z-v0.23.3
