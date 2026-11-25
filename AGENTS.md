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

6. **REGRAS OPERACIONAIS DESCOBERTAS (DEPLOY, CACHE, SWARM E TRACKING):**
   - **Deploy real na VPS:** o volume servido pelo Nginx (`lp-inteligencia-agentica`) está acessível via SMB em `\\100.97.222.112\D\projetos\inteligencia-agentica` (usado por `scripts/sync_deploy.py`). `git push` sozinho **não** atualiza a VPS sem `git pull` ou cópia para o share SMB.
   - **Cache Cloudflare `immutable` (30 dias) e cache de 404 (4h):** o Nginx serve `css`/`js`/imagens com `Cache-Control: public, no-transform, immutable` (30d). Sempre versionar novos assets JS/CSS (ou usar `?v=YYYYMMDD`) e **copiar os assets para o share antes de copiar `index.html` e antes de testar qualquer URL**, evitando que a Cloudflare faça cache de `404 Not Found` por 4 horas (`max-age=14400`).
   - **Hero Mouse Swarm:** usar `scripts/setup_mouse_swarm.py` com `/static/js/mouse-swarm-v3.js?v=20261125` e `forceMotion: true` (Windows com `MinAnimate=0` / `prefers-reduced-motion: reduce` abortava na v1; nunca esconder a Hero via CSS).
   - **Tracking & Consent Mode V2:** `index.html` inicializa `consent:default` + `window.__consentDefaultInitialized = true` antes do `GTM-M5JDK6W4` e usa `/static/cookieconsent-v3.js` + `/static/cookieconsent-v3.css`; GA4 (`G-18FQCREKV5`) roda exclusivamente via GTM (sem snippet estático duplicado). Pendência conhecida no painel do GTM: Tag 14 (Meta Pixel `1419116247084635`) só dispara em `generate_lead`/`lead_conversion` (falta `All Pages` + eventos `view_item`, `begin_checkout`, `cta_click`, `consent_updated`).
   - **HTTPS / DNS:** `index.html` inclui fallback client-side `http:` → `https://inteligenciaagentica.com.br`; pendência conhecida na Cloudflare: ativar `Always Use HTTPS` + `HSTS` e criar registro DNS `CNAME www` + redirect para a raiz.

Para documentação detalhada, consulte `MANUAL.md` e `PROJECT_CONTEXT.md`.