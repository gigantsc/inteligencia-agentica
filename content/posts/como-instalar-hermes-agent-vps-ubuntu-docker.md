---
title: "Como Instalar e Hospedar o Hermes Agent 24/7 na sua VPS Ubuntu com Docker"
date: "2026-08-30"
lastmod: "2026-09-01"
summary: "Guia passo a passo para colocar seu agente autônomo Hermes OS rodando na nuvem com segurança, persistência de dados e túnel Cloudflare seguro."
tags: ["Hermes OS", "VPS", "DevOps", "Docker", "Agentes de IA"]
keywords: ["Hermes Agent", "Hermes OS", "como instalar Hermes na VPS", "Docker Swarm agentes de IA", "Cloudflare Tunnel", "Nous Research Hermes"]
author: "Jean Pierre Schramm"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
draft: false
---

> **Resposta Rápida:**  
> Hospedar o **Hermes Agent** em uma **VPS Ubuntu** permite que seus robôs autônomos executem tarefas ininterruptas (cron jobs, monitoramento de servidores, prospecção e geração de conteúdo) 24 horas por dia, com isolamento seguro via Docker e sem sobrecarregar sua máquina local.

---

## Por que Rodar seu Agente na Nuvem?

Ter agentes rodando apenas no computador pessoal traz limitações óbvias:
- Se você desligar o notebook, a operação inteira para.
- Conexões instáveis de internet doméstica interrompem fluxos longos.
- Falta de isolamento de processos e firewall dedicado.

Com uma VPS (Virtual Private Server) e Docker, seu agente ganha **IP fixo, uptime de 99.9%, cron jobs automatizados e conectividade direta com APIs**.

---

## Arquitetura Recomendada

A estrutura mais resiliente e segura para rodar múltiplos agentes envolve:

1. **Host Linux (Ubuntu 24.04+ LTS)**: Sistema operacional base com kernel estável.
2. **Docker & Docker Swarm**: Orquestração de containers com auto-healing (se o container cair, ele reinicia sozinho).
3. **Cloudflare Tunnel (Zero Trust)**: O agente não expõe portas públicas (nem 80, nem 443). O tráfego passa por um túnel criptografado seguro.
4. **Volume Persistente**: Dados, históricos de sessão e memória semântica armazenados em diretórios montados.

```
[ Usuário / Telegram / Webhook ]
               │
               ▼
   [ Cloudflare Zero Trust Tunnel ]
               │
               ▼ (Túnel Criptografado)
   [ VPS Ubuntu + UFW Firewall ]
         ┌───────────────┐
         │  Hermes Agent │
         │   (Docker)    │
         └───────┬───────┘
                 │
       [ Volume Persistente ]
```

---

## 3 Passos Principais de Instalação

### 1. Preparação da VPS
Atualize o sistema e instale as dependências essenciais do Docker:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl ufw git
```

### 2. Configuração do Firewall
Mantenha a postura de segurança padrão:
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

### 3. Deploy do Container Hermes
Crie o arquivo de configuração de inicialização e inicialize o serviço com persistência de perfil e memória:
```bash
docker run -d \
  --name hermes-agent \
  --restart unless-stopped \
  -v /mnt/dados/hermes-data:/root/.hermes \
  -e HERMES_API_KEY="sua_chave_aqui" \
  ghcr.io/nousresearch/hermes-agent:latest
```

---

## Dica de Ouro: Notificações no Telegram

Ao integrar o Hermes Agent com a API de bots do Telegram, você pode enviar comandos por áudio ou texto direto pelo celular e receber relatórios diários de execução.

Quer aprender a configurar essa arquitetura completa com acompanhamento ao vivo e suporte técnico? Conheça os planos da comunidade **Inteligência Agêntica**.
