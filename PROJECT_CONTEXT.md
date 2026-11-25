# PROJECT_CONTEXT.md — Inteligência Agêntica

## Visão Geral
- **Domínio oficial:** `https://inteligenciaagentica.com.br`
- **Objetivo:** Landing Page principal, blog técnico otimizado para SEO/GEO, acervo `/cases`, páginas de produto (`/cinemaker`, `/mediaflowmz`, `/ao-vivo`, `/obrigado`) e índices para LLMs (`/llms.txt`, `/llms-full.txt`, `/sitemap.xml`, `/feed.xml`).

## Arquitetura, Tecnologias e Pastas
- **Frontend:** HTML estático + Tailwind CDN + JS vanilla/ES modules (`static/js/`, `static/cookieconsent-v3.js`).
- **Build do Blog / GEO:** Node.js ESM (`scripts/build-blog.js` via `pnpm run build`) compilando `content/posts/*.md` para `/blog/`, `/tags/`, `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt` e `feed.xml`.
- **Automações Python (`scripts/`):** `setup_mouse_swarm.py` (injeção idempotente da animação Hero), `sync_deploy.py` (cópia via SMB para a VPS), geradores de capas e páginas.

## Hospedagem, Portas e Deploy
- **VPS:** `jepierre-ubuntu` (Tailscale SSH `100.97.222.112`), diretório `/mnt/dados/projetos/inteligencia-agentica` montado `:ro` em `/usr/share/nginx/html` no serviço Docker Swarm `lp-inteligencia-agentica` (`nginx:alpine`, porta interna `80`, rede `network_swarm_public`).
- **Exposição:** Cloudflare Tunnel (`http://lp-inteligencia-agentica:80`). Sem Traefik.
- **Deploy ativo via Windows:** share SMB `\\100.97.222.112\D\projetos\inteligencia-agentica`. `git push` no repo local não atualiza a VPS automaticamente.
- **Regra de cache:** Nginx aplica `Cache-Control: public, no-transform, immutable` (30 dias) em assets estáticos e a Cloudflare faz cache de `404` por 4 horas (`max-age=14400`). Sempre subir assets novos/versionados (`?v=YYYYMMDD`) antes de atualizar `index.html` e antes de testar a URL pública.

## Analytics & Variáveis/Identificadores Públicos
- **GTM Container:** `GTM-M5JDK6W4` (gerencia GA4 `G-18FQCREKV5` e Meta Pixel `1419116247084635`).
- **Consent Mode V2:** inicializado inline no `<head>` com `window.__consentDefaultInitialized = true` antes do GTM; gerenciado por `static/cookieconsent-v3.js` + `static/cookieconsent-v3.css` (`autoLoadGtm: false`).
- **Segredos/Chaves:** não versionar tokens ou credenciais no repositório (uso exclusivo de IDs públicos de tracking e variáveis locais de ambiente quando aplicável).

## Pontos Críticos e Pendências Conhecidas
- **Hero Mouse Swarm:** controlado por `scripts/setup_mouse_swarm.py` com `/static/js/mouse-swarm-v3.js?v=20261125` e `forceMotion: true` (necessário para rodar mesmo com `prefers-reduced-motion: reduce` / Windows `MinAnimate=0`, sem nunca ocultar a Hero por CSS).
- **Pendência Cloudflare (painel):** ativar `Always Use HTTPS` + `HSTS` em *SSL/TLS → Edge Certificates* e criar `CNAME www` + *Redirect Rule* para a raiz (atualmente `http://` responde `200 OK` na borda antes do redirect JS e `www` retorna `NXDOMAIN`).
- **Pendência GTM `GTM-M5JDK6W4` (painel):** Tag 14 (`Meta Pixel 1419116247084635`) está vinculada apenas a `generate_lead` e `lead_conversion`; falta adicionar `All Pages` e mapear os eventos `view_item`, `begin_checkout`, `cta_click` e `consent_updated`.
