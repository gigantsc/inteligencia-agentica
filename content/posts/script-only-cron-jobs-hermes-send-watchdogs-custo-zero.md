---
title: "Script-Only Cron Jobs e hermes send: Watchdogs de Infraestrutura e Alertas de Custo Zero com Hermes Agent"
date: "2026-11-17"
lastmod: "2026-11-17"
summary: "Aprenda a orquestrar rotinas de monitoramento 24/7 na VPS usando cron jobs sem LLM (no-agent mode) e o utilitário hermes send. Telemetria de hardware, alertas de banco de dados e pipelines com zero consumo de tokens e entrega direta no Telegram, Discord e WhatsApp."
tags: ["Cron Jobs", "DevOps", "Hermes Agent", "Infraestrutura", "Automação", "VPS", "Telegram"]
keywords: ["Script-Only Cron Jobs", "hermes send", "no-agent mode Hermes", "Watchdog de infraestrutura IA", "Monitoramento VPS Telegram", "Alertas custo zero Hermes", "Cron jobs sem LLM"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/script-only-cron-jobs-hermes-send-custo-zero-v2.jpg"
draft: false
---

> **Em resumo:**  
> Os **Script-Only Cron Jobs** (executados em modo `no_agent=True` ou flag `--no-agent`) e o comando utilitário **`hermes send`** compõem a camada de automação determinística e custo zero do ecossistema **Hermes Agent**.[1][2] Em vez de acionar um modelo de linguagem (LLM) a cada minuto ou hora para verificar tarefas previsíveis — como consumo de RAM, espaço em disco, status de containers Docker ou métricas financeiras via API —, o agendador nativo executa scripts locais em Bash ou Python e encaminha o `stdout` diretamente para mais de 21 canais de mensageria (Telegram, WhatsApp, Discord, Slack, Signal).[1][2][3] Essa arquitetura elimina o consumo de tokens de API, opera sob o princípio *silent when empty* (silêncio absoluto quando não há falhas) e dispensa que o gateway ou o agente estejam carregados na memória RAM para disparar notificações corporativas imediatas.[1][2]

---

## O Dilema Operacional: Por que Colocar LLM em Tarefas Determinísticas Destrói o Orçamento

Na esteira do entusiasmo com inteligência artificial agêntica, muitas equipes de engenharia e operações cometeram um erro arquitetural básico: colocar modelos de fronteira (como GPT-4o, Claude 3.5 Sonnet ou DeepSeek-V3) para rodar a cada 5 minutos em laços de repetição apenas para checar se uma porta de rede respondeu ou se o disco de um servidor está cheio.

O resultado dessa abordagem é duplo:
1. **Faturas Desnecessárias de API:** Um cron job de IA que roda a cada 5 minutos acumula 8.640 execuções mensais. Mesmo com prompts curtos, o overhead de contexto, schemas de ferramentas e histórico pode facilmente custar centenas de dólares ao mês para realizar checagens que um script Bash de 4 linhas resolve em 2 milissegundos.[1][3]
2. **Risco de Falsos Positivos e Alucinações:** Um modelo probabilístico pode parafrasear um status técnico com ambiguidades ou inventar causas inexistentes quando lê logs brutos volumosos sem necessidade.[1]

No entanto, abandonar o ecossistema do agente e voltar para o `crontab` tradicional do Linux cria outro problema: a perda da integração com mensageria moderna. Configurar envio de alertas confiáveis para grupos de WhatsApp, tópicos categorizados de Telegram ou canais de operações no Slack a partir de scripts shell clássicos exige gerenciar dezenas de chaves de API dispersas, lidar com bibliotecas HTTP e tratar falhas de rede na mão.

O **Hermes Agent** resolveu esse atrito através de uma separação elegante entre **tarefas cognitivas** (que exigem raciocínio) e **tarefas determinísticas** (que exigem precisão mecânica).[1][2]

---

## O que São Script-Only Cron Jobs (`no_agent=True`)

No Hermes Agent, o agendador de tarefas (`cronjob`) suporta nativamente o **modo sem agente** (*no-agent mode*).[1] 

Quando uma tarefa é agendada com `no_agent=True` (pelo chat) ou `--no-agent` (pela CLI), o agendador do Hermes executa o script configurado sem inicializar o loop de raciocínio, sem montar o system prompt e sem fazer qualquer chamada HTTP para provedores de LLM.[1][3]

```
┌─────────────────────────────────────────────────────────────┐
│              SCHEDULER NATIVO (CRONJOB TICK)               │
│                   (Ex: "every 5m" ou cron "0 9 * * *")      │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
   [MODO LLM CONVENCIONAL]               [MODO SCRIPT-ONLY]
   (no_agent = False)                    (no_agent = True / --no-agent)
            │                                     │
   Inicializa AIAgent                    Executa Script Local Direto
   Carrega SOUL / Skills                 (~/.hermes/scripts/watchdog.sh)
   Chama Provedor LLM (Tokens)                    │
   Gera Síntese Cognitiva                Captura stdout + Exit Code
            │                                     │
            └──────────────────┬──────────────────┘
                               ▼
            ┌─────────────────────────────────────┐
            │          DELIVERY ROUTER            │
            │  (Telegram, WhatsApp, Slack, etc.) │
            └─────────────────────────────────────┘
```

### Características Centrais do Modo Sem Agente:
- **Custo Zero de IA:** Zero tokens consumidos, zero latência de inferência e zero gasto com provedores.[1]
- **Mesmo Agendador Unificado:** As tarefas sem agente convivem lado a lado com os agentes inteligentes na mesma base SQLite (`~/.hermes/cron/executions.db`), respondendo aos mesmos comandos de pausa, retomada, edição e auditoria (`hermes cron list`, `hermes cron pause <id>`).[1][3]
- **Scripts em Bash ou Python:** Arquivos com terminação `.sh` ou `.bash` rodam via interpretador de sistema; qualquer outra extensão roda no interpretador Python do Hermes ou em um ambiente virtual isolado indicado pelo operador.[1]

---

## O Utilitário CLI `hermes send`: O "curl" da Mensageria Corporativa

Complementando o agendador de tarefas, o Hermes disponibiliza o comando CLI **`hermes send`**.[2] Ele funciona como um canivete suíço para injeção de mensagens, arquivos e logs em qualquer canal de mensageria configurado na máquina.[2]

O grande diferencial do `hermes send` é que **ele não exige que o processo do gateway esteja ativo** para plataformas baseadas em tokens de bot (Telegram, Discord, Slack, Signal, SMS e WhatsApp Cloud API).[2] O comando lê as credenciais diretamente do arquivo `.env` ou `config.yaml` da máquina e dispara a requisição diretamente para os endpoints REST oficiais da plataforma.[2]

```bash
# Envio de mensagem simples para o canal principal do Telegram
hermes send --to telegram "Backup do PostgreSQL concluído com sucesso."

# Pipe de saída de logs diretamente do terminal
cat /var/log/nginx/error.log | tail -n 20 | hermes send --to discord:#ops --subject "🚨 Alertas Nginx"

# Envio de relatório PDF gerado por rotina local
hermes send --to telegram:-1001928374650:42 --file relatorio_mensal.pdf
```

### Formatos de Destino Suportados pelo `hermes send`

| Formato do Alvo | Exemplo Prático | Comportamento Operacional |
|---|---|---|
| `platform` | `--to telegram` | Envia para o chat/canal principal configurado no perfil |
| `platform:chat_id` | `--to telegram:-100123456789` | Envia para um grupo, canal ou usuário numérico específico |
| `platform:chat_id:thread_id` | `--to telegram:-100123456789:17585` | Direciona cirurgicamente para um tópico específico de fórum |
| `platform:#canal` | `--to discord:#infraestrutura` | Resolve dinamicamente o nome legível do canal via cache de diretório |
| `platform:+E164` | `--to whatsapp:+5511999998888` | Direciona para o número internacional no WhatsApp ou Signal |

---

## A Filosofia "Silent When Empty": Erradicando a Fadiga de Alertas

Um dos maiores problemas em monitoramento de servidores e bancos de dados é a **fadiga de alertas**: sistemas que enviam mensagens a cada 5 minutos dizendo "Tudo OK" treinam os gestores a ignorar as notificações no celular. Quando um desastre real acontece, o alerta crítico se perde no meio de 200 mensagens triviais.

Os Script-Only Cron Jobs do Hermes Agent implementam nativamente a política **Silent When Empty**:[1]

```
   ┌─────────────────────────────────────────────────────────────┐
   │             EXECUÇÃO DO WATCHDOG NA VPS                    │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
         [CONDIÇÃO NORMAL]                [ANOMALIA DETECTADA]
        (RAM < 85%, Disco OK)            (RAM = 94%, Erro no Nginx)
                 │                                 │
           stdout VAZIO                     stdout COM TEXTO
                 │                                 │
                 ▼                                 ▼
        [SILÊNCIO ABSOLUTO]             [DISPARO INSTANTÂNEO]
      Nenhuma mensagem gerada           Notificação entregue no
      Zero ruído no Telegram           Telegram / WhatsApp / Slack
```

### Matriz de Mapeamento de Saída e Entrega

| Comportamento do Script | Código de Retorno | Resultado de Entrega no Chat |
|---|:---:|---|
| **Saída vazia no stdout** | `Exit 0` | **Silêncio total.** Nenhuma mensagem é despachada.[1] |
| **Texto gerado no stdout** | `Exit 0` | **Entrega imediata.** O texto emitido é entregue verbatim no canal configurado.[1] |
| **Supressão explícita** | `Exit 0` | Se a última linha contiver `{"wakeAgent": false}`, o tick permanece mudo.[1] |
| **Erro de execução** | `Exit != 0` | **Alerta de falha entregue.** Erros de script são notificados para evitar falha cega.[1] |
| **Timeout de processo** | Interrupção | **Alerta crítico entregue.** Avisa que o monitor travou ou excedeu o limite.[1] |

Essa arquitetura garante que a equipe operacional receba mensagens no Telegram ou WhatsApp **apenas quando houver uma ação necessária**, restaurando a autoridade e a urgência de cada notificação.

---

## Isolamento de Ambientes: Ambientes Virtuais com `--interpreter`

Em cenários corporativos, scripts de automação frequentemente dependem de bibliotecas Python que não fazem parte do runtime padrão do Hermes (como drivers Oracle, conectores SAP, bibliotecas de automação de planilhas como `openpyxl` ou frameworks de scraping).[1]

Para evitar a poluição do ambiente Python global do agente e prevenir que uma atualização do sistema quebre as dependências do monitor, o agendador permite parametrizar interpretadores independentes através da flag `--interpreter`:[1]

```bash
# 1. Criação de um ambiente virtual isolado para monitoramento financeiro
uv venv ~/venvs/financeiro-monitor --python 3.11
uv pip install --python ~/venvs/financeiro-monitor/bin/python psycopg2-binary requests

# 2. Agendamento do cron job apontando para o binário isolado
hermes cron create "0 8 * * *" \
  --no-agent \
  --script reconciliacao-bancaria.py \
  --interpreter ~/venvs/financeiro-monitor/bin/python \
  --deliver telegram:-1001928374650 \
  --name "reconciliacao-diaria"
```

### Regras de Segurança e Execução:
- **Resolução de Diretório:** Por segurança operacional, todos os scripts do agendador devem obrigatoriamente residir dentro do diretório `~/.hermes/scripts/`.[1] Tentativas de navegação relativa fora da pasta (*path traversal*) ou symlinks maliciosos são bloqueadas pelo runtime.[1]
- **Validação em Tempo de Execução:** O executável do interpretador é validado a cada disparo, garantindo que o cron continue funcionando mesmo se a VPS for migrada de container.[1]

---

## Três Casos Práticos para Implementar Hoje na sua Operação

### Caso 1: Watchdog de Memória RAM e Espaço em Disco (VPS 24/7)

Crie o arquivo em `~/.hermes/scripts/vps-health-watchdog.sh`:

```bash
#!/usr/bin/env bash
# Monitor silencioso de recursos da VPS
# Dispara alerta apenas se a RAM exceder 85% ou o disco / passar de 90%

RAM_THRESHOLD=85
DISK_THRESHOLD=90

# Checagem de Memória RAM
RAM_PCT=$(free | awk '/^Mem:/ {printf "%d", $3 * 100 / $2}')
if [ "$RAM_PCT" -ge "$RAM_THRESHOLD" ]; then
  echo "⚠️ [ALERTA VPS] Memória RAM em ${RAM_PCT}% no host $(hostname)"
fi

# Checagem de Partição Raiz
DISK_PCT=$(df / --output=pcent | tail -n 1 | tr -d ' %')
if [ "$DISK_PCT" -ge "$DISK_THRESHOLD" ]; then
  echo "🚨 [CRÍTICO] Partição Raiz ocupando ${DISK_PCT}% no host $(hostname)"
fi

# Se nada for impresso, o stdout é vazio e o Hermes não envia mensagem alguma.
```

Agende a execução a cada 10 minutos via CLI:

```bash
chmod +x ~/.hermes/scripts/vps-health-watchdog.sh

hermes cron create "every 10m" \
  --no-agent \
  --script vps-health-watchdog.sh \
  --deliver telegram \
  --name "vps-resources-watchdog"
```

---

### Caso 2: Verificador de Saúde de APIs e Containers Docker

Crie o script Python em `~/.hermes/scripts/docker-health.py`:

```python
import subprocess
import json
import sys

def check_containers():
    # Coleta lista de containers que não estão com status "running"
    cmd = ["docker", "ps", "-a", "--filter", "status=exited", "--format", "{{.Names}}: {{.Status}}"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        failed = res.stdout.strip()
        if failed:
            print("🔴 **[Falha em Containers Docker Detectada]**")
            print("Os seguintes containers foram encerrados inesperadamente:")
            for line in failed.split("\n"):
                print(f"• `{line}`")
            print("\nAcesse o terminal para investigar os logs com `docker logs <nome>`.")
    except Exception as e:
        print(f"⚠️ Erro ao consultar o daemon do Docker: {e}")

if __name__ == "__main__":
    check_containers()
```

Agende a rotina a cada 15 minutos:

```bash
hermes cron create "every 15m" \
  --no-agent \
  --script docker-health.py \
  --deliver discord:#alertas-infra \
  --name "docker-containers-watchdog"
```

---

### Caso 3: Pipeline de Deploy com `hermes send` sem Gateway Ativo

Em esteiras de CI/CD (GitHub Actions, GitLab CI ou scripts locais de atualização na VPS), você pode injetar notificações no Telegram ou Slack no encerramento da compilação:

```bash
#!/usr/bin/env bash
set -e

echo "Iniciando build do sistema..."
npm run build

echo "Reiniciando serviço no systemd..."
sudo systemctl restart meu-servico-api

# Notifica o time diretamente pelo Telegram sem depender de gateway do agente
hermes send --to telegram \
  --subject "🚀 DEPLOY PRODUÇÃO CONCLUÍDO" \
  "Aplicação atualizada com sucesso no commit $(git rev-parse --short HEAD) às $(date +'%H:%M:%S')."
```

---

## Criando Watchdogs via Linguagem Natural no Chat

A grande conveniência dessa arquitetura é que o próprio **Hermes Agent sabe quando usar o modo sem agente**.[1] Você não precisa acessar o terminal ou memorizar parâmetros da CLI; basta descrever a necessidade operacional no chat do Telegram, Desktop ou terminal.[1]

Quando você solicita comandos como:
> *"Hermes, me avisa no Telegram se o disco passar de 90% a cada 10 minutos."*

O agente analisa a solicitação e identifica que a regra de disparo é determinística.[1] Em vez de agendar uma consulta cara com IA, ele executa duas ferramentas nativas sob o capô:[1]
1. `write_file(path="~/.hermes/scripts/disk-alert.sh", content="...")` para criar o código de verificação.[1]
2. `cronjob(action="create", schedule="every 10m", script="disk-alert.sh", no_agent=True, deliver="telegram")` para agendar a rotina com custo zero de tokens.[1]

---

## Matriz de Decisão: Quando Usar Cron com LLM vs. Script-Only

| Dimensão Operacional | Modo com IA (`no_agent: false`) | Modo Script-Only (`no_agent: true`) |
|---|---|---|
| **Natureza da Tarefa** | Cognitiva (síntese, triagem, redação) | Mecânica (métricas, integridade, pings) |
| **Consumo de Tokens** | Proporcional ao contexto e modelo | **Zero tokens** (processamento 100% local) |
| **Tempo de Execução** | 5 a 60 segundos por turno | 2 a 50 milissegundos |
| **Geração de Mensagens** | Sínteses em prosa e relatórios formatados | `stdout` verbatim emitido pelo script |
| **Critério de Disparo** | Sempre gera relatório, salvo com `[SILENT]` | **Silent when empty:** calado se `stdout` for vazio |
| **Dependência Externa** | Requer conexão com provedor de LLM | Roda localmente mesmo sem internet |
| **Exemplo de Aplicação** | Resumo diário de notícias do setor | Alerta de estouro de memória RAM e disco |

---

## Conclusão: Eficiência Agêntica com Governança de Custos

A maturidade de uma infraestrutura de inteligência agêntica não é medida pela quantidade de chamadas que você faz a um modelo de linguagem, mas sim pela inteligência de saber **quando não chamá-lo**.

Ao combinar **Script-Only Cron Jobs** para sentinelas de hardware e serviços com o utilitário **`hermes send`** para notificações cirúrgicas, sua empresa constrói uma esteira de monitoramento 24/7 na VPS com estabilidade militar, zero ruído desnecessário e custo de API rigorosamente sob controle.

Quer estruturar seus próprios agentes autônomos, configurar sentinelas na VPS e dominar a arquitetura completa do Hermes Agent para o seu negócio? Participe da nossa formação executiva e comunidade exclusiva:  
👉 **[Conheça o ecossistema Inteligência Agêntica](https://inteligenciaagentica.com.br)**

---

## Sources
[1] https://hermes-agent.nousresearch.com/docs/guides/cron-script-only  
[2] https://hermes-agent.nousresearch.com/docs/guides/pipe-script-output  
[3] https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
