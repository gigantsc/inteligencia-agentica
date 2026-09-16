# AGENTS.md — Instruções para Agentes de IA

Este repositório contém a **Landing Page** e o **Blog Otimizado para IAs (GEO/SEO)** do ecossistema [inteligenciaagentica.com.br](https://inteligenciaagentica.com.br).

## Contexto Operacional
- **Diretório:** `/mnt/dados/projetos/inteligencia-agentica`
- **Ambiente:** Servidor VPS `jepierre-ubuntu` (Docker Swarm).
- **Serviço Nginx:** `lp-inteligencia-agentica` conectado à rede `network_swarm_public`.
- **Cloudflare Tunnel:** `http://lp-inteligencia-agentica:80`.
- **Dono do Projeto:** Jean Pierre Schramm ([@gigantsc](https://github.com/gigantsc)).

## Regras Críticas para Agentes
1. **SEMPRE TESTE ANTES DE AFIRMAR:** Jean exige comprovação real via execução de comando com exit code 0 ou teste HTTP (`curl`/`wget`).
2. **NUNCA DESTRUA A HOSPEDAGEM:** Os arquivos locais são montados em `/usr/share/nginx/html` no container. Edições refletem em tempo real.
3. **APÓS EDITAR OU CRIAR POSTS EM `content/posts/*.md`:**
   - Execute `pnpm run build` para recompilar os arquivos estáticos (`/blog/`, `/tags/`, `sitemap.xml`, `robots.txt`, `llms.txt`, `feed.xml`).
   - Execute `pnpm run indexnow` para submeter ao IndexNow.
   - Faça `git add -A && git commit -m "..." && git push`.
4. **DESIGN SYSTEM:**
   - Dark Obsidian `#07070A`
   - Ciano Neon `#00E5FF`
   - Magenta Neon `#C000FF`
   - Dourado / Ouro `#DFBA6B`
   - Glassmorphism com bordas `border-white/10` e fundo `bg-white/5`.
5. **CHECKOUT HOTMART ATUAL:**
   - Mensal 2º Lote: `https://pay.hotmart.com/L107410278Y?checkoutMode=2&off=jm3etdun` (R$ 97/mês)
   - Anual: `https://pay.hotmart.com/L107410278Y?checkoutMode=2&off=yjri55cz` (R$ 497/ano)

Para documentação detalhada, consulte `MANUAL.md`.