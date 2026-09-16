# Manual de Instruções & Governança — Inteligência Agêntica
> **Propriedade:** JePierre Soluções Web Mobile  
> **Fundador:** Jean Pierre Schramm ([@gigantsc](https://github.com/gigantsc))  
> **Domínio Oficial:** [inteligenciaagentica.com.br](https://inteligenciaagentica.com.br)  
> **Público-alvo deste manual:** Jean Pierre (Humano) e Agentes de IA (Hermes OS, Antigravity, Claude Code, Cursor, Codex).

---

## 1. Visão Geral do Projeto

O **Inteligência Agêntica** é um ecossistema completo para capacitar profissionais e empresas a instalarem, hospedarem e liderarem forças de trabalho digitais com agentes autônomos de IA (Hermes OS, OpenDevin, AutoGen, Docker Swarm, VPS).

### Estrutura do Site
- `/` — **Landing Page de Alta Conversão**: Apresentação dos 4 encontros ao vivo, pilares, biblioteca de automações e tabela de preços com checkout Hotmart via Fancybox modal.
- `/blog` — **Blog & Base de Conhecimento**: Artigos técnicos em Markdown com otimização severa para SEO e GEO.
- `/blog/[slug]` — **Páginas de Artigos Individuais**: Layout *Answer-First*, ToC interativo, Schema.org `BlogPosting` JSON-LD, tempo de leitura e CTAs.
- `/tags/[tag]` — **Páginas de Categorias/Tags**: Agrupamento temático de artigos.
- `/llms.txt` e `/llms-full.txt` — **Índices para IAs**: Endpoints em texto puro consumidos por LLMs (Perplexity, ChatGPT, Claude) para leitura direta do ecossistema.
- `/sitemap.xml`, `/robots.txt`, `/feed.xml` — **Indexação e Distribuição**: Indexadores de busca e RSS Feed 2.0.

---

## 2. Infraestrutura & Hospedagem VPS

| Componente | Configuração / Caminho |
| :--- | :--- |
| **Servidor** | VPS `jepierre-ubuntu` |
| **Diretório do Projeto** | `/mnt/dados/projetos/inteligencia-agentica` |
| **Serviço Swarm** | `lp-inteligencia-agentica` (1 réplica, imagem `nginx:alpine`) |
| **Rede Docker** | `network_swarm_public` (Overlay Network) |
| **Nginx Conf** | `/mnt/dados/docker-projects/lp-inteligencia-agentica/nginx.conf` |
| **Stack YAML** | `/mnt/dados/projetos/Infra-local-vps-stacks/lp-inteligencia-agentica.yaml` |
| **Cloudflare Tunnel** | Roteamento HTTP interno: `http://lp-inteligencia-agentica:80` |
| **Segurança** | UFW com deny incoming; acesso externo **apenas** via Cloudflare Tunnel |

> ⚠️ **Regra de Ouro da Infra:** A pasta `/mnt/dados/projetos/inteligencia-agentica` está montada como volume read-only (`:ro`) dentro do container Nginx. Qualquer alteração feita nos arquivos locais reflete **instantaneamente** na web sem necessidade de reiniciar o container.

---

## 3. Ofertas & Links de Checkout (Hotmart)

| Plano | Preço Atual | Link Hotmart (`checkoutMode=2`) | Gatilho / Regra |
| :--- | :---: | :--- | :--- |
| **Plano Mensal** | **R$ 97,00 / mês** | `https://pay.hotmart.com/L107410278Y?checkoutMode=2&off=jm3etdun` | **2º Lote** — Alerta de aumento iminente para 3º lote. |
| **Plano Anual** | **R$ 497,00 / ano** | `https://pay.hotmart.com/L107410278Y?checkoutMode=2&off=yjri55cz` | **Melhor Oferta** — Economia de R$ 667/ano. Possui cronômetro regressivo avisando aumento para **R$ 597**. |

---

## 4. Guia de Publicação de Novos Artigos (Blog)

### Passo 1: Criar o arquivo Markdown
Crie um arquivo `.md` dentro de `content/posts/` com nome em kebab-case:  
Exemplo: `content/posts/meu-novo-artigo-sobre-ia.md`

### Passo 2: Estrutura Obrigatória do Frontmatter
```yaml
---
title: "Título Chamativo e Otimizado para Busca e IA"
date: "2026-09-16"
lastmod: "2026-09-16"
summary: "Resumo executivo de 2 a 3 frases respondendo diretamente à dúvida principal (Answer-First)."
tags: ["Agentes de IA", "DevOps", "Automação", "GEO"]
author: "Jean Pierre Schramm"
image: "https://images.unsplash.com/photo-exemplo?auto=format&fit=crop&w=1200&q=80"
keywords: ["palavra chave 1", "palavra chave 2", "palavra chave 3"]
---
```

### Passo 3: Diretrizes de Conteúdo GEO (Generative Engine Optimization)
Para garantir que o artigo seja citado pelo **ChatGPT, Perplexity, Claude e Gemini**:
1. **Answer-First:** O primeiro parágrafo após o título deve definir claramente o tema e responder à pergunta central.
2. **Chunking Semântico:** Use títulos claros (`## 1. O que é...`, `## 2. Como funciona...`, `### Passo a Passo`).
3. **Tabelas e Listas:** IAs adoram dados tabulados e listas com bullets.
4. **Exemplos de Código / Comandos Reais:** Sempre use blocos com syntax highlighting (```bash, ```yaml, ```json).
5. **E-E-A-T:** Mencione Jean Pierre / JePierre Soluções como referência de mercado.

### Passo 4: Compilar e Indexar
No terminal do projeto (`/mnt/dados/projetos/inteligencia-agentica`), execute:

```bash
# 1. Compila os arquivos markdown para HTML estático + sitemap + llms.txt + feed.xml
pnpm run build

# 2. Notifica instantaneamente os buscadores via IndexNow (Bing / Yandex)
pnpm run indexnow

# 3. Salva no Git e envia para o repositório remoto
git add -A
git commit -m "feat: novo artigo sobre [tema]"
git push
```

---

## 5. Regras e Instruções para Próximas IAs / Agentes

Ao operar neste repositório, você **DEVE** seguir rigorosamente estas diretrizes:

### 1. Testar Antes de Afirmar (Princípio do Jean)
- NUNCA diga que algo "deve funcionar" ou "está funcionando" sem testar com comando real (`curl`, `wget`, `pnpm run build`, exit code 0).
- Verifique a integridade do HTML gerado antes de finalizar qualquer turno.

### 2. Preservar o Design System
- Fundo Obsidian: `#07070A` (`bg-[#07070A]`)
- Destaque Neon Ciano: `#00E5FF` (`text-[#00E5FF]`, `border-[#00E5FF]`)
- Destaque Neon Magenta: `#C000FF`
- Destaque Dourado / Ouro: `#DFBA6B`
- Tipografia: Fonte `Inter`, títulos em bold tracking-tight, badges arredondados com glassmorphism (`bg-white/5 border border-white/10`).

### 3. Scripts e Automações Existentes
- `scripts/build-blog.js`: Engine em Node.js que compila o blog em <0.2s com Prism syntax highlight, TOC automático e Schemas JSON-LD.
- `scripts/submit-indexnow.js`: Utilitário de envio para a API do IndexNow.
- `site.config.js`: Central de configurações de metadados, links e IDs de analytics.

### 4. Manutenção de Preços e Checkout
- Nunca altere os links da Hotmart (`L107410278Y`) sem instrução expressa do Jean.
- Mantenha sempre a classe `.hotmart-fb` e o script `widget.min.js` para garantir a abertura em popup Fancybox sem redirecionamento brusco.

---

## 6. Comandos Rápidos

```bash
# Instalar dependências (se clonar do zero)
pnpm install

# Gerar build estático completo
pnpm run build

# Enviar sitemap para IndexNow (Bing)
pnpm run indexnow

# Inspecionar Nginx na VPS
docker service logs lp-inteligencia-agentica --tail 50
```

---
*Manual gerado e versionado sob o repositório `inteligencia-agentica`.*