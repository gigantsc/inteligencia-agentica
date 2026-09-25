# -*- coding: utf-8 -*-
"""
Script de processamento e geracao da pagina /cases da Inteligencia Agentica.
Utiliza os 326 cases traduzidos para pt-BR com identidade visual oficial do projeto.
"""

import json
import os
import re
from datetime import datetime

INPUT_FILE = "D:/DevCod/inteligencia-agentica/use_cases_translated.json"
OUTPUT_DIR = "D:/DevCod/inteligencia-agentica/cases"
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "index.html")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    translated_cases = json.load(f)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'—\s*(u\/[\w-]+|@[\w-]+|[\w\s.-]+),\s*\d{4}-\d{2}-\d{2}.*$', '', text, flags=re.MULTILINE)
    return text.strip()

def map_sector_and_tags(c):
    title = (c.get("title") or "").lower()
    summary = (c.get("summary") or "").lower()
    detail = (c.get("detail") or "").lower()
    tags = [t.lower() for t in c.get("tags", [])]
    combined = f"{title} {summary} {detail} {' '.join(tags)}"

    if any(k in combined for k in ["docker", "vps", "server", "servidor", "infra", "deploy", "nginx", "self-host", "linux", "cloud", "homelab", "proxmox", "traefik", "portainer", "swarm"]):
        sector = "DevOps & Infraestrutura"
        tag_pt = "DevOps"
    elif any(k in combined for k in ["marketing", "youtube", "video", "vídeo", "copy", "conteúdo", "content", "social media", "blog", "seo", "thumbnail", "podcast", "áudio", "redator"]):
        sector = "Marketing & Conteúdo"
        tag_pt = "Marketing"
    elif any(k in combined for k in ["empresa", "cliente", "clientes", "business", "vendas", "sales", "crm", "enterprise", "agência", "contrato", "legal", "lead", "faturamento", "receita", "finance"]):
        sector = "Gestão & Operações"
        tag_pt = "Negócios"
    elif any(k in combined for k in ["pesquisa", "trading", "mercado", "ações", "crypto", "paper", "análise de dados", "scrape", "scraping", "rag", "benchmark", "dados"]):
        sector = "Pesquisa & Inteligência"
        tag_pt = "Pesquisa & Dados"
    elif any(k in combined for k in ["telegram", "whatsapp", "assistente", "voz", "calendário", "email", "tarefas", "obsidian", "notion", "rotina", "pessoal", "dia a dia"]):
        sector = "Assistentes & Rotinas"
        tag_pt = "Assistentes"
    else:
        sector = "Engenharia & Software"
        tag_pt = "Desenvolvimento"

    extra_tags = []
    if "telegram" in combined: extra_tags.append("Telegram")
    if "whatsapp" in combined: extra_tags.append("WhatsApp")
    if "github" in combined: extra_tags.append("GitHub")
    if "memória" in combined or "memory" in combined or "hindsight" in combined: extra_tags.append("Memória Persistente")
    if "cron" in combined or "rotina" in combined or "24h" in combined: extra_tags.append("Rotinas 24/7")
    if "vps" in combined or "servidor" in combined or "nuvem" in combined: extra_tags.append("VPS Nuvem")
    if "solo" in combined or "indie" in combined or "sozinho" in combined: extra_tags.append("Solo / Indie")

    if not extra_tags:
        extra_tags.append(tag_pt)

    return sector, [tag_pt] + [t for t in extra_tags if t != tag_pt]

processed_cases = []
for idx, c in enumerate(translated_cases):
    sector, tags_pt = map_sector_and_tags(c)
    source_raw = c.get("source", "Comunidade")
    source_map = {
        "reddit": "Reddit",
        "hn": "Hacker News",
        "discord": "Discord",
        "x": "X (Twitter)",
        "github": "GitHub",
        "blog": "Artigo Técnico",
        "podcast": "Podcast",
        "community": "Comunidade Global"
    }
    source_label = source_map.get(source_raw.lower(), source_raw.upper())
    
    author = c.get("author") or "Membro da Comunidade"
    date_str = c.get("date") or "2026-08-01"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = dt.strftime("%d/%m/%Y")
    except:
        formatted_date = date_str

    raw_title = c.get("title", f"Caso de Uso #{idx+1}")
    raw_summary = c.get("summary", "")
    raw_detail = c.get("detail", raw_summary)

    processed_cases.append({
        "id": c.get("id") or f"case-{idx+1}",
        "title": raw_title,
        "summary": clean_text(raw_summary),
        "detail": clean_text(raw_detail),
        "sector": sector,
        "tags": tags_pt[:4],
        "author": author,
        "source": source_label,
        "date": formatted_date
    })

cases_json_str = json.dumps(processed_cases, ensure_ascii=False)

# Salvar json de dados na pasta cases
with open("D:/DevCod/inteligencia-agentica/cases/cases-data.json", "w", encoding="utf-8") as f:
    json.dump(processed_cases, f, ensure_ascii=False, indent=2)

# Template HTML completo
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>326 Cases Reais de Agentes de IA em Produção — Inteligência Agêntica</title>
  <meta name="description" content="Explore 326 casos reais de agentes autônomos de IA em produção: DevOps, desenvolvimento, automação, atendimento e gestão de negócios traduzidos para português.">
  <link rel="canonical" href="https://inteligenciaagentica.com.br/cases">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="326 Cases Reais de Agentes de IA em Produção — Inteligência Agêntica">
  <meta property="og:description" content="Casos práticos de agentes autônomos operando 24 horas por dia em empresas, desenvolvimento, infraestrutura e marketing.">
  <meta property="og:url" content="https://inteligenciaagentica.com.br/cases">

  <!-- Fonts & Tailwind -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            obsidian: {{
              DEFAULT: '#07070A',
              light: '#0D0D12',
              card: '#12121A',
              border: '#1E1E2E',
            }},
            ciano: {{
              DEFAULT: '#00F0FF',
              light: '#5CF6FF',
              dark: '#00B4D8',
            }},
            magenta: {{
              DEFAULT: '#D946EF',
              light: '#E879F9',
              dark: '#A21CAF',
            }},
            ouro: {{
              DEFAULT: '#F59E0B',
              light: '#FCD34D',
              dark: '#D97706',
            }},
          }},
        }},
      }},
    }};
  </script>

  <style>
    body {{
      background-color: #07070A;
      color: #E2E8F0;
      font-family: 'Inter', system-ui, sans-serif;
    }}
    .glass {{
      background: rgba(18, 18, 26, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glass:hover {{
      border-color: rgba(0, 240, 255, 0.25);
    }}
    .top-bar {{
      background: rgba(7, 7, 10, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .gradient-text-gold {{
      background: linear-gradient(135deg, #F59E0B 0%, #FCD34D 50%, #F59E0B 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .gradient-text-ciano {{
      background: linear-gradient(135deg, #00F0FF 0%, #D946EF 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .btn-gold {{
      background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
      color: #000;
      font-weight: 700;
      transition: all 0.2s ease;
    }}
    .btn-gold:hover {{
      filter: brightness(1.1);
      transform: translateY(-1px);
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-ciano/20 selection:text-ciano">

  <!-- TOP BAR -->
  <nav class="top-bar fixed top-0 inset-x-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-14">
      <a href="/" class="flex items-center gap-2 group">
        <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-magenta to-ciano flex items-center justify-center shadow-lg shadow-ciano/20">
          <i data-lucide="brain" class="w-4 h-4 text-white"></i>
        </div>
        <span class="text-sm font-bold tracking-tight text-white group-hover:text-ciano transition-colors">Inteligência Agêntica</span>
      </a>
      <div class="flex items-center gap-5">
        <a href="/cases" class="text-xs font-bold text-ciano transition-colors border-b-2 border-ciano pb-0.5">
          Cases
        </a>
        <a href="/blog" class="text-xs font-semibold text-gray-300 hover:text-ciano transition-colors">
          Blog
        </a>
        <a href="/#oferta"
           class="inline-flex items-center gap-1.5 text-xs font-semibold text-ouro hover:text-ouro-light transition-colors duration-200">
          Assinar agora
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </div>
  </nav>

  <!-- MAIN CONTAINER -->
  <main class="flex-grow pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
    
    <!-- HERO HEADER -->
    <div class="text-center max-w-3xl mx-auto mb-12">
      <span class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wider text-ciano bg-ciano/10 border border-ciano/20 mb-4">
        <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
        Acervo Prático de Casos de Uso Traduzidos
      </span>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white leading-tight">
        Casos Reais de Agentes Autônomos <span class="gradient-text-ciano">em Produção</span>
      </h1>
      <p class="text-sm sm:text-base text-gray-400 mt-4 leading-relaxed">
        Explore <strong>326 experiências e fluxos de trabalho práticos</strong> de quem já colocou assistentes virtuais e equipes digitais trabalhando 24h na nuvem pelo celular.
      </p>

      <!-- NOTA DE TRANSPARÊNCIA & TRADUÇÃO -->
      <div class="mt-6 p-4 rounded-xl bg-obsidian-light border border-white/10 text-xs text-gray-400 max-w-2xl mx-auto text-left flex items-start gap-3">
        <i data-lucide="globe" class="w-4 h-4 text-ciano flex-shrink-0 mt-0.5"></i>
        <div class="leading-relaxed">
          <strong class="text-gray-200">Nota de Curadoria & Tradução:</strong> Estes relatos foram originalmente compartilhados pela comunidade internacional de IA em inglês e traduzidos/organizados em português brasileiro pela equipe da <strong>Inteligência Agêntica</strong> para servir como inspiração prática e cases reais de aplicação.
        </div>
      </div>
    </div>

    <!-- CONTROLS & SEARCH -->
    <div class="glass rounded-2xl p-5 mb-8 border border-white/10 shadow-xl">
      <!-- Search Input -->
      <div class="relative mb-5">
        <i data-lucide="search" class="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2"></i>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Buscar por palavras-chave (ex: Telegram, Docker, Rotina 24/7, Vendas, PostgreSQL, Deploy)..." 
          class="w-full pl-12 pr-4 py-3 rounded-xl bg-obsidian-light border border-white/10 text-white placeholder-gray-500 text-sm focus:outline-none focus:border-ciano transition-colors"
        >
      </div>

      <!-- Sector Badges Filter -->
      <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none" id="sectorFilters">
        <button class="filter-btn active px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-ciano text-black shadow-lg shadow-ciano/20" data-sector="all">
          Todos (326)
        </button>
        <button class="filter-btn px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-obsidian-card hover:bg-white/10 text-gray-300 border border-white/10" data-sector="DevOps & Infraestrutura">
          🚀 DevOps & Nuvem
        </button>
        <button class="filter-btn px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-obsidian-card hover:bg-white/10 text-gray-300 border border-white/10" data-sector="Engenharia & Software">
          💻 Engenharia & Código
        </button>
        <button class="filter-btn px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-obsidian-card hover:bg-white/10 text-gray-300 border border-white/10" data-sector="Assistentes & Rotinas">
          🤖 Assistentes Pessoais
        </button>
        <button class="filter-btn px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-obsidian-card hover:bg-white/10 text-gray-300 border border-white/10" data-sector="Gestão & Operações">
          📈 Negócios & Gestão
        </button>
        <button class="filter-btn px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-obsidian-card hover:bg-white/10 text-gray-300 border border-white/10" data-sector="Marketing & Conteúdo">
          🎨 Marketing & Mídia
        </button>
        <button class="filter-btn px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 bg-obsidian-card hover:bg-white/10 text-gray-300 border border-white/10" data-sector="Pesquisa & Inteligência">
          🔬 Pesquisa & Dados
        </button>
      </div>

      <div class="mt-3 flex items-center justify-between text-xs text-gray-400 pt-2 border-t border-white/5">
        <span id="caseCountText">Mostrando 326 casos</span>
        <span class="text-gray-500">Clique em qualquer card para ver a história completa</span>
      </div>
    </div>

    <!-- CASES GRID -->
    <div id="casesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Inserido dinamicamente via JS -->
    </div>

    <!-- PAGINATION -->
    <div class="mt-12 flex items-center justify-center gap-3" id="pagination">
      <!-- Inserido dinamicamente via JS -->
    </div>

  </main>

  <!-- MODAL DE DETALHES -->
  <div id="caseModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md opacity-0 pointer-events-none transition-opacity duration-200">
    <div class="glass rounded-2xl max-w-2xl w-full p-6 sm:p-8 border border-white/15 shadow-2xl relative max-h-[90vh] overflow-y-auto">
      <button id="closeModal" class="absolute top-5 right-5 text-gray-400 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
      
      <div id="modalSectorBadge" class="mb-3"></div>
      <h2 id="modalTitle" class="text-xl sm:text-2xl font-bold text-white mb-4 leading-snug"></h2>
      
      <div class="p-4 rounded-xl bg-obsidian-light border border-white/10 text-sm text-gray-300 leading-relaxed mb-6 whitespace-pre-line" id="modalDetail"></div>

      <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-white/10 text-xs text-gray-400">
        <div class="flex items-center gap-2" id="modalMeta">
          <!-- Autor e Fonte -->
        </div>
        <div class="flex items-center gap-1.5" id="modalTags">
          <!-- Tags -->
        </div>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="border-t border-white/5 bg-obsidian py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-gray-500 space-y-2">
      <p>© 2026 Inteligência Agêntica — Todos os direitos reservados.</p>
      <p class="text-gray-600">Curadoria e tradução de experiências práticas com sistemas de inteligência agêntica.</p>
    </div>
  </footer>

  <!-- DATA & APP LOGIC -->
  <script>
    const ALL_CASES = {cases_json_str};

    let currentSector = 'all';
    let searchQuery = '';
    let currentPage = 1;
    const ITEMS_PER_PAGE = 18;

    const sectorColors = {{
      'DevOps & Infraestrutura': 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
      'Engenharia & Software': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
      'Assistentes & Rotinas': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      'Gestão & Operações': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
      'Marketing & Conteúdo': 'bg-pink-500/10 text-pink-400 border-pink-500/20',
      'Pesquisa & Inteligência': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    }};

    function getFilteredCases() {{
      return ALL_CASES.filter(c => {{
        const matchesSector = currentSector === 'all' || c.sector === currentSector;
        const q = searchQuery.toLowerCase();
        const matchesSearch = !q || 
          c.title.toLowerCase().includes(q) || 
          c.summary.toLowerCase().includes(q) || 
          c.detail.toLowerCase().includes(q) || 
          c.tags.some(t => t.toLowerCase().includes(q)) ||
          c.author.toLowerCase().includes(q);
        return matchesSector && matchesSearch;
      }});
    }}

    function renderCases() {{
      const filtered = getFilteredCases();
      const grid = document.getElementById('casesGrid');
      const countEl = document.getElementById('caseCountText');
      countEl.textContent = `Mostrando ${{filtered.length}} de ${{ALL_CASES.length}} casos`;

      const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE) || 1;
      if (currentPage > totalPages) currentPage = 1;

      const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
      const paginated = filtered.slice(startIndex, startIndex + ITEMS_PER_PAGE);

      if (paginated.length === 0) {{
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-gray-500 glass rounded-2xl">
            <i data-lucide="inbox" class="w-10 h-10 mx-auto mb-3 opacity-40"></i>
            <p class="text-base font-semibold text-gray-400">Nenhum caso encontrado para os filtros selecionados.</p>
            <p class="text-xs text-gray-500 mt-1">Tente buscar por termos mais genéricos como "Telegram" ou "Docker".</p>
          </div>
        `;
        lucide.createIcons();
        renderPagination(0);
        return;
      }}

      grid.innerHTML = paginated.map(c => {{
        const colorClass = sectorColors[c.sector] || 'bg-white/10 text-white border-white/20';
        return `
          <div class="glass rounded-2xl p-5 sm:p-6 flex flex-col justify-between cursor-pointer hover:-translate-y-1 transition-all duration-200 group border border-white/10" onclick="openModal('${{c.id}}')">
            <div>
              <div class="flex items-center justify-between gap-2 mb-3">
                <span class="px-2.5 py-1 rounded-lg text-[11px] font-semibold border ${{colorClass}}">
                  ${{c.sector}}
                </span>
                <span class="text-[11px] text-gray-500">${{c.date}}</span>
              </div>
              <h3 class="text-base font-bold text-white group-hover:text-ciano transition-colors line-clamp-2 leading-snug">
                ${{c.title}}
              </h3>
              <p class="text-xs sm:text-sm text-gray-400 mt-2.5 line-clamp-3 leading-relaxed">
                ${{c.summary}}
              </p>
            </div>

            <div class="mt-5 pt-4 border-t border-white/5 flex flex-col gap-3">
              <div class="flex flex-wrap gap-1.5">
                ${{c.tags.map(t => `<span class="text-[10px] px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/5">${{t}}</span>`).join('')}}
              </div>
              <div class="flex items-center justify-between text-[11px] text-gray-500">
                <span>Por <strong class="text-gray-400 font-medium">${{c.author}}</strong></span>
                <span class="inline-flex items-center gap-1 text-gray-400">
                  <i data-lucide="layers" class="w-3 h-3 text-ciano"></i>
                  ${{c.source}}
                </span>
              </div>
            </div>
          </div>
        `;
      }}).join('');

      renderPagination(totalPages);
      lucide.createIcons();
    }}

    function renderPagination(totalPages) {{
      const pagEl = document.getElementById('pagination');
      if (totalPages <= 1) {{
        pagEl.innerHTML = '';
        return;
      }}

      let html = '';
      if (currentPage > 1) {{
        html += `<button onclick="changePage(${{currentPage - 1}})" class="px-3.5 py-2 rounded-xl text-xs font-semibold bg-obsidian-card hover:bg-white/10 border border-white/10 text-white">Anterior</button>`;
      }}
      html += `<span class="px-4 py-2 rounded-xl text-xs font-semibold bg-white/5 text-gray-300 border border-white/5">Página ${{currentPage}} de ${{totalPages}}</span>`;
      if (currentPage < totalPages) {{
        html += `<button onclick="changePage(${{currentPage + 1}})" class="px-3.5 py-2 rounded-xl text-xs font-semibold bg-obsidian-card hover:bg-white/10 border border-white/10 text-white">Próxima</button>`;
      }}
      pagEl.innerHTML = html;
    }}

    function changePage(page) {{
      currentPage = page;
      renderCases();
      window.scrollTo({{ top: 300, behavior: 'smooth' }});
    }}

    // Filter Buttons
    document.querySelectorAll('#sectorFilters .filter-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('#sectorFilters .filter-btn').forEach(b => {{
          b.classList.remove('bg-ciano', 'text-black', 'shadow-lg', 'shadow-ciano/20');
          b.classList.add('bg-obsidian-card', 'text-gray-300');
        }});
        btn.classList.add('bg-ciano', 'text-black', 'shadow-lg', 'shadow-ciano/20');
        btn.classList.remove('bg-obsidian-card', 'text-gray-300');
        currentSector = btn.dataset.sector;
        currentPage = 1;
        renderCases();
      }});
    }});

    // Search Input
    document.getElementById('searchInput').addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      currentPage = 1;
      renderCases();
    }});

    // Modal Handling
    const modal = document.getElementById('caseModal');
    function openModal(caseId) {{
      const c = ALL_CASES.find(item => item.id === caseId);
      if (!c) return;

      const colorClass = sectorColors[c.sector] || 'bg-white/10 text-white border-white/20';
      document.getElementById('modalSectorBadge').innerHTML = `
        <span class="px-3 py-1 rounded-lg text-xs font-semibold border ${{colorClass}}">
          ${{c.sector}}
        </span>
      `;
      document.getElementById('modalTitle').textContent = c.title;
      document.getElementById('modalDetail').textContent = c.detail || c.summary;
      document.getElementById('modalMeta').innerHTML = `
        <span>Relatado por <strong class="text-white">${{c.author}}</strong> via <strong>${{c.source}}</strong> em ${{c.date}}</span>
      `;
      document.getElementById('modalTags').innerHTML = c.tags.map(t => `<span class="text-xs px-2.5 py-1 rounded bg-white/5 text-gray-300 border border-white/10">${{t}}</span>`).join('');

      modal.classList.remove('opacity-0', 'pointer-events-none');
      document.body.style.overflow = 'hidden';
      lucide.createIcons();
    }}

    function closeModal() {{
      modal.classList.add('opacity-0', 'pointer-events-none');
      document.body.style.overflow = '';
    }}

    document.getElementById('closeModal').addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {{
      if (e.target === modal) closeModal();
    }});
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeModal();
    }});

    // Inicialização
    renderCases();
    lucide.createIcons();
  </script>
</body>
</html>"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Página de Cases gerada com sucesso em: {OUTPUT_HTML}")
