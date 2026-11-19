---
title: "Managed Scope, Remote Config e Profile Distributions: Como Padronizar e Blindar Agentes de IA na Empresa"
date: "2026-11-19"
lastmod: "2026-11-19"
summary: "Aprenda a escalar agentes de IA para toda a empresa sem perder o controle: trave políticas de segurança com Managed Scope, gerencie frotas via Remote Config e distribua agentes prontos com Profile Distributions."
tags: ["Agentes de IA", "Governança", "Hermes Agent", "DevOps", "Segurança", "Negócios"]
keywords: ["Managed Scope Hermes Agent", "Remote Config agentes IA", "Profile Distributions Git", "padronização agentes corporativos", "governança IA empresas"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/managed-scope-remote-config-governanca-hermes.jpg"
draft: false
---

> **Em resumo:** Criar um bom agente de IA em uma máquina é relativamente fácil; o desafio real começa quando a empresa precisa replicar esse mesmo padrão para 5, 20 ou 100 colaboradores e servidores sem que cada usuário altere o modelo, desligue travas de segurança ou vaze credenciais. O Hermes Agent resolve esse gargalo com três camadas nativas: **Managed Scope** (travas imutáveis em nível de sistema)[1], **Remote Config** (plano de controle centralizado em modo *fail-closed*)[2] e **Profile Distributions** (distribuição e atualização de agentes completos via Git sem tocar em dados locais)[3].

Quando um empresário decide tirar os agentes de IA do experimento individual e levá-los para a operação diária da equipe, surge um problema clássico de infraestrutura: o **desvio de configuração** (*configuration drift*).

Sem governança, cada colaborador ou servidor acaba editando seu próprio `config.yaml`, trocando o provedor econômico por um modelo caro, desativando a redação de segredos ou copiando prompts desatualizados por WhatsApp e e-mail. O resultado é custo imprevisível, risco de conformidade e retrabalho constante para o gestor.

---

## O Problema da Escala Artesanal vs. Frota Governada

Compartilhar um agente "na mão" significa enviar `SOUL.md`, lista de skills, `config.yaml` sem senhas, servidores MCP e cron jobs por mensagem — torcendo para o destinatário montar tudo certo[3]. A cada melhoria no fluxo, todo esse processo manual precisa ser repetido[3].

A arquitetura do Hermes Agent separa claramente **três níveis de necessidade corporativa**:

| Camada | Mecanismo no Hermes | O que resolve na prática | Ideal para |
|---|---|---|---|
| **1. Empacotamento e Entrega** | **Profile Distributions** (`hermes profile install` / `update`) | Empacota `SOUL.md`, `skills/`, `cron/`, `mcp.json` e `config.yaml` em um repositório Git versionado, mantendo senhas e memórias fora do pacote[3]. | Times distribuídos, franquias, consultorias e implantação rápida em várias máquinas[3]. |
| **2. Trava Local de Política** | **Managed Scope** (`/etc/hermes/config.yaml` e `.env`) | Permite que a TI trave chaves específicas com permissão de `root` (`0644`); usuários comuns não conseguem sobrescrever via CLI ou arquivo local[1]. | Servidores Linux compartilhados, VPS departamentais e estações Linux gerenciadas[1]. |
| **3. Controle Centralizado de Frota** | **Remote Config** (`HERMES_CONFIG_BACKEND=remote`) | Substitui o `config.yaml` local por um plano de controle remoto com hierarquia (global, tenant, grupo, owner, agente, perfil) e bloqueio de chaves[2]. | Frotas de agentes em nuvem ou on-prem com dezenas de instâncias e auditoria central[2]. |

---

## Arquitetura de Governança em 3 Camadas

```
+-----------------------------------------------------------------------+
|                  PLANO DE CONTROLE / TI CORPORATIVA                   |
|                                                                       |
|  [1] Profile Distribution (Git)      [2] Managed Scope (/etc/hermes)  |
|      - SOUL.md, skills/, cron/           - config.yaml (root 0644)    |
|      - mcp.json, distribution.yaml       - .env (URL base / defaults) |
|      - Atualiza sem apagar memoria       - Sobrepoe ~/.hermes/*       |
|                                                                       |
|  [3] Remote Config (Config Plane - opcional para frotas maiores)      |
|      - Camadas: Global -> Tenant -> Grupo -> Owner -> Agente -> Perfil|
|      - Fail-closed na inicializacao + polling a cada 5 minutos        |
+-----------------------------------+-----------------------------------+
                                    |
          +-------------------------+-------------------------+
          v                         v                         v
+-------------------+     +-------------------+     +-------------------+
| Agente Financeiro |     |  Agente Comercial |     |   Agente DevOps   |
| ~/.hermes/        |     | ~/.hermes/        |     | ~/.hermes/        |
| - .env (chaves)   |     | - .env (chaves)   |     | - .env (chaves)   |
| - memories/       |     | - memories/       |     | - memories/       |
| - sessions/       |     | - sessions/       |     | - sessions/       |
+-------------------+     +-------------------+     +-------------------+
```

---

## 1. Profile Distributions: Entregue um Funcionário Digital em 1 Comando

Uma **Profile Distribution** transforma um perfil do Hermes em um pacote versionado em Git[3]. O autor cria um manifesto `distribution.yaml` declarando nome, versão, compatibilidade (`hermes_requires`) e quais variáveis de ambiente o instalador precisará preencher (`env_requires`)[3].

Quando um gestor ou colaborador precisa subir o agente em uma nova máquina ou VPS, basta rodar[3]:

```bash
hermes profile install git@github.com:sua-empresa/agente-financeiro.git --alias agente-fin
```

Durante a instalação e nas atualizações futuras (`hermes profile update agente-fin`), o Hermes aplica regras rígidas de segurança e isolamento[3]:

- **Nunca distribui segredos ou histórico:** `auth.json`, `.env`, `memories/`, `sessions/`, `state.db`, `logs/` e `workspace/` são estritamente excluídos pelo instalador[3].
- **Gera `.env.EXAMPLE` automaticamente:** o colaborador preenche apenas suas próprias chaves ou aponta para variáveis já existentes no shell[3].
- **Atualização não destrutiva:** ao rodar `hermes profile update`, o sistema atualiza `SOUL.md`, `mcp.json`, `skills/` e faz *merge* de `cron/jobs.json` por ID (preservando se o usuário pausou ou ativou um job, e mantendo o `config.yaml` local intacto salvo uso explícito de `--force-config`)[3].

### Distribution (Git) vs. Export (`.tar.gz`): Quando Usar Cada Um?

| Critério | Profile Distribution (Git) | Export File (`.tar.gz` via `/export`) |
|---|---|---|
| **Objetivo** | Produto vivo e versionado para equipes[3] | Snapshot pontual para backup ou troca rápida de máquina[3] |
| **Atualizações** | Contínuas via `hermes profile update`[3] | Requer gerar e reenviar novo arquivo[3] |
| **Inclui memórias e sessões?** | Nunca[3] | Sim (`memories/`, `sessions/`, `USER.md`), embora remova credenciais por nome de arquivo[3] |
| **Controle de versão** | Tags, branches e commits Git[3] | Nenhum[3] |

---

## 2. Managed Scope: Trave Regras Críticas Contra Alterações Locais

Mesmo com um perfil padronizado, um usuário comum pode tentar mudar o provedor de IA, desligar a redação de segredos ou apontar o agente para um endpoint não homologado. É aqui que entra o **Managed Scope**[1].

O Managed Scope lê políticas de um diretório de sistema (por padrão `/etc/hermes/`, ou outro caminho fixado pelo administrador via `HERMES_MANAGED_DIR` no unit de serviço/container)[1]:

```text
/etc/hermes/
├── config.yaml   # Chaves travadas (vencem sobre ~/.hermes/config.yaml)
└── .env          # Variáveis compartilhadas (vencem sobre ~/.hermes/.env e shell)
```

O diretório pertence ao `root` com permissão `0755` e os arquivos com `0644` — todos leem, apenas administradores editam[1]. Se um usuário tentar alterar uma chave travada, o Hermes bloqueia na hora[1]:

```bash
$ hermes config set model.default outro/modelo
Cannot set 'model.default': it is managed by your administrator (/etc/hermes/config.yaml) and cannot be changed.
```

> **Atenção aos limites da v1:** Na documentação oficial, o Managed Scope v1 é focado em Linux/POSIX e baseado em permissões de sistema de arquivos[1]. Como o `/etc/hermes/.env` tem leitura pública (`0644`), ele deve guardar valores compartilhados não sensíveis (como URL de proxy corporativo ou padrões de modelo), nunca senhas de alta criticidade[1]. Além disso, ele é uma barreira administrativa para usuários comuns — não substitui isolamento de rede ou container (*Egress Proxy*) contra *prompt injection*[1].

---

## 3. Remote Config: Governança Centralizada para Frotas em Produção

Quando a empresa opera dezenas de instâncias (em Hermes Cloud ou infraestrutura *on-prem*), gerenciar arquivos `/etc/hermes/config.yaml` em cada servidor deixa de escalar. O **Remote Config** substitui o arquivo local por um plano de controle centralizado[2].

Basta configurar as variáveis de inicialização no ambiente ou no `.env` gerenciado[2]:

```bash
HERMES_CONFIG_BACKEND=remote
HERMES_CONFIG_INSTANCE_ID=instancia-vendas-01
HERMES_CONFIG_REMOTE_URL=https://seu-config-plane.empresa.com
```

Para ambientes *on-prem*, o agente se autentica via OAuth2 *client-credentials* (`GATEWAY_RELAY_IDP_*`), e qualquer processo filho (como workers `hermes -p`, bots ou crons) herda o backend remoto automaticamente[2].

Os pilares operacionais do Remote Config são desenhados para compliance[2]:

1. **Fail-closed na inicialização:** Se o plano de controle estiver inacessível após ~30 segundos de tentativas ou recusar a instância, o processo encerra com erro — nunca faz *fallback* silencioso para um arquivo local desatualizado[2].
2. **Hierarquia com travas:** O plano resolve a configuração em camadas (global, tenant, grupo, owner, agente e perfil), impedindo que `hermes config set`, TUI ou Desktop alterem chaves travadas em níveis superiores[2].
3. **Sincronização contínua:** Cada instância verifica atualizações a cada 5 minutos e aplica mudanças sem derrubar o processo em execução[2].
4. **Zero segredos no plano:** Chaves sensíveis como `api_key` aceitam apenas referências `${VAR}` que continuam sendo resolvidas localmente via `.env` ou cofre de segredos[2].

*(Nota importante: no modo Remote Config, `/etc/hermes/config.yaml` é ignorado para evitar conflito de fontes de verdade, embora `/etc/hermes/.env` continue sendo aplicado[2].)*

---

## Como Implementar na Prática Sem Complicar a Operação

1. **Comece pequeno com Profile Distributions:** Crie um repositório Git privado para o primeiro agente validado (ex.: triagem comercial ou analista financeiro), adicione o `.gitignore` recomendado pela documentação para barrar `memories/`, `sessions/` e `.env`, e escreva o `distribution.yaml`[3].
2. **Adicione Managed Scope nos servidores Linux compartilhados:** Fixe `security.redact_secrets: true` e o provedor/modelo homologado em `/etc/hermes/config.yaml` para garantir teto de custo e conformidade[1].
3. **Escale para Remote Config apenas quando tiver frota:** Para 1 máquina ou 1 VPS dedicada, o `config.yaml` local (com ou sem Managed Scope) é mais simples e suficiente[2]. Só migre para plano remoto quando precisar governar múltiplos tenants, grupos e dezenas de instâncias simultaneamente[2].

Se você quer estruturar agentes de IA com padrão de engenharia corporativa, segurança e previsibilidade de custos para o seu negócio, conheça a comunidade **Inteligência Agêntica** em [https://inteligenciaagentica.com.br](https://inteligenciaagentica.com.br).

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/managed-scope — Hermes Agent Docs: Managed Scope
[2] https://hermes-agent.nousresearch.com/docs/user-guide/remote-config — Hermes Agent Docs: Remote Config
[3] https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions — Hermes Agent Docs: Profile Distributions
