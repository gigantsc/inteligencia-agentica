import os
import re

def build():
    rendered_path = r"C:\Users\Jean\AppData\Local\Temp\landing_anual_rendered.html"
    art_path = r"C:\Users\Jean\AppData\Local\hermes\profiles\devops\attachments\Landing-Inteligencia-Agentica-Anual.html"
    old_index_path = r"D:\DevCod\inteligencia-agentica\index.html"
    out_git_index = r"D:\DevCod\inteligencia-agentica\index.html"
    out_copy_index = r"D:\DevCod\Inteligencia_agentica\index.html"
    out_page_html = r"D:\DevCod\Inteligencia_agentica\page.html"

    with open(rendered_path, "r", encoding="utf-8") as f:
        rendered_html = f.read()

    with open(art_path, "r", encoding="utf-8") as f:
        art_html = f.read()

    with open(old_index_path, "r", encoding="utf-8") as f:
        old_html = f.read()

    # 1. Extract CSS from attachment
    style_match = re.search(r"<style>(.*?)</style>", art_html, re.DOTALL)
    artifact_css = style_match.group(1) if style_match else ""

    # 2. Extract Head start from old_html (Consent, GTM, Meta, JSON-LD, etc.)
    head_end_pos = old_html.find("<!-- Tailwind CSS CDN -->")
    if head_end_pos == -1:
        head_end_pos = old_html.find("<script src=\"https://cdn.tailwindcss.com\">")
    head_start_html = old_html[:head_end_pos]

    # Ensure title and description are accurate
    head_start_html = re.sub(
        r"<title>.*?</title>",
        "<title>Inteligência Agêntica — Agentes de IA Autônomos Trabalhando 24h para sua Empresa</title>",
        head_start_html
    )
    head_start_html = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Chega de prompt. Instale funcionários de IA que trabalham 24h por você enquanto você dorme. Comunidade, 4 encontros ao vivo/mês e agentes prontos.">',
        head_start_html
    )

    # 3. Extract Navbar from old_html
    nav_start = old_html.find('<nav class="top-bar fixed top-0 inset-x-0 z-50">')
    nav_end = old_html.find('</nav>') + len('</nav>')
    navbar_html = old_html[nav_start:nav_end]
    navbar_html = navbar_html.replace(
        'src="/static/images/logo.png"',
        'src="static/images/logo.png" onerror="if(!this.dataset.retried){this.dataset.retried=1;this.src=\'/static/images/logo.png\';}"'
    )
    navbar_html = re.sub(
        r'<a href="#oferta"\s+class="btn-gold inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold tracking-wide">.*?</a>',
        '''<a href="#oferta" class="inline-flex items-center gap-2 h-10 px-5 rounded-full bg-[var(--orange)] text-white text-[13px] font-bold tracking-wide hover:brightness-110 transition-all shadow-[0_4px_15px_rgba(255,77,0,0.35)]">
          <span>Assinar agora</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </a>''',
        navbar_html,
        flags=re.DOTALL
    )

    # 4. Extract Footer from old_html
    footer_start = old_html.find('<footer class="border-t border-white/5 py-12 bg-obsidian-light/50 mt-20">')
    footer_end = old_html.find('</footer>') + len('</footer>')
    footer_html = old_html[footer_start:footer_end]
    footer_html = footer_html.replace(
        'src="/static/images/logo.png"',
        'src="static/images/logo.png" onerror="if(!this.dataset.retried){this.dataset.retried=1;this.src=\'/static/images/logo.png\';}"'
    )

    # 5. Extract Sections from rendered_html
    # Sec 1: 3491 to 15749
    # Sec 2: 15749 to 22840
    # Sec 3: 22840 to 33517
    # Sec 4: 33517 to 38123
    # Sec 5: 38123 to 41709
    # Sec 6: 41709 to 46559
    # Sec 7: 46559 to 55299
    # Sec 8: 55299 to 58687
    # Sec 9: 58687 to 62965
    # Toast & Sticky Bar: 62965 to end

    # Section 1 (Hero): We need to split into left col and right col
    sec1_raw = rendered_html[3491:15749]
    right_col_marker = '<div class="relative lg:sticky lg:top-[96px]">'
    r_idx = sec1_raw.find(right_col_marker)
    left_col_html = sec1_raw[:r_idx]

    # Refine H1, Eyebrow and spacing in left_col_html for optimal proportions
    left_col_html = left_col_html.replace(
        'py-[56px] lg:py-[96px]',
        'pt-6 pb-12 sm:pt-8 sm:pb-16 lg:pt-10 lg:pb-20'
    )
    left_col_html = left_col_html.replace(
        'text-[11px] tracking-[0.14em] font-semibold text-[var(--orange)] mb-6',
        'text-[11px] sm:text-[12px] tracking-[0.14em] font-bold text-orange-400 mb-3'
    )
    left_col_html = left_col_html.replace(
        'text-[34px] sm:text-[48px] lg:text-[64px] leading-[0.95]',
        'text-[28px] sm:text-[38px] lg:text-[44px] xl:text-[48px] leading-[1.04]'
    )
    left_col_html = left_col_html.replace(
        'mt-6 text-[16px] lg:text-[18px] leading-[1.6]',
        'mt-3 text-[14px] sm:text-[15px] lg:text-[16px] leading-[1.5]'
    )
    left_col_html = left_col_html.replace(
        '<div class="mt-8">',
        '<div class="mt-5">'
    )
    left_col_html = left_col_html.replace(
        'mt-10 grid grid-cols-3 gap-3 max-w-[520px]',
        'mt-5 grid grid-cols-3 gap-3 max-w-[520px]'
    )

    # Video Player markup with custom captions, unmute button, alert overlay, replay overlay
    video_markup = '''    <!-- Video Player Element -->
    <div class="relative aspect-video bg-black flex items-center justify-center cursor-pointer group" id="videoWrapper">
      <video 
        id="heroVideo"
        class="w-full h-full object-cover" 
        playsinline
        preload="auto"
        poster="poster.jpg"
      >
        <source src="video-inicial.mp4" type="video/mp4">
        Seu navegador não suporta a tag de vídeo HTML5.
      </video>

      <!-- Dynamic Custom Captions Container (Abaixo do vídeo, sem cobrir o Jean) -->
      <div id="captionsBox" class="absolute bottom-2 sm:bottom-3 left-3 right-3 sm:left-4 sm:right-4 flex justify-center pointer-events-none z-25 transition-opacity duration-200">
        <p id="captionText" class="max-w-[92%] sm:max-w-[85%] bg-black/90 backdrop-blur-md border border-white/20 text-white font-medium text-[11px] sm:text-xs md:text-sm px-3.5 py-1.5 sm:px-4 sm:py-2 rounded-lg sm:rounded-xl text-center shadow-2xl leading-snug transition-all duration-150 opacity-0"></p>
      </div>

      <!-- Unmute overlay button (aparece se áudio for bloqueado) -->
      <button id="unmuteOverlay" type="button" class="absolute bottom-3 right-3 sm:bottom-4 sm:right-4 bg-black/90 hover:bg-black border border-white/20 text-white text-xs sm:text-sm font-semibold px-3.5 py-2 sm:px-4 sm:py-2.5 rounded-xl backdrop-blur flex items-center gap-2 transition-all duration-200 z-30 shadow-lg cursor-pointer opacity-0 pointer-events-none">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 text-[var(--orange)]" id="soundIcon"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>
        <span id="soundText">Clique para ativar o som</span>
      </button>

      <!-- Play & Alert Callout Overlay (Inicial - Vídeo pausado) -->
      <div id="playOverlay" class="absolute inset-0 bg-black/60 backdrop-blur-[2px] flex flex-col items-center justify-center p-4 sm:p-6 text-center z-[35] transition-all duration-300">
        <!-- Chamada de Alerta -->
        <div class="inline-flex items-center gap-2 px-3.5 sm:px-4 py-1.5 sm:py-2 rounded-full text-[11px] sm:text-xs font-bold text-amber-300 bg-amber-500/20 border border-amber-400/40 mb-3 sm:mb-4 shadow-lg shadow-amber-500/10 backdrop-blur-md animate-pulse">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-amber-400 flex-shrink-0"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <span>⚠️ ATENÇÃO: Assista com o som ligado</span>
        </div>

        <!-- Botão de Iniciar Vídeo -->
        <button id="startVideoBtn" type="button" class="group relative flex items-center gap-3 px-6 sm:px-8 py-3.5 sm:py-4 rounded-[14px] bg-[var(--orange)] text-white font-extrabold text-xs sm:text-base tracking-wide shadow-[0_10px_30px_rgba(255,77,0,0.5)] hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer">
          <span class="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-3.5 h-3.5 sm:w-4 sm:h-4 fill-white text-white ml-0.5"><polygon points="6 3 20 12 6 21 6 3"></polygon></svg>
          </span>
          <span>CLIQUE PARA INICIAR O VÍDEO</span>
        </button>

        <p class="mt-2.5 sm:mt-3 text-[11px] sm:text-xs text-gray-300 font-medium drop-shadow">
          Apresentação rápida • 1 minuto 🔊
        </p>
      </div>

      <!-- Replay & CTA Overlay (surge quando o vídeo termina) -->
      <div id="replayOverlay" class="absolute inset-0 bg-[#0A0A0A]/95 backdrop-blur-md flex flex-col items-center justify-center p-6 text-center z-40 transition-all duration-300 opacity-0 pointer-events-none">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold text-[var(--orange)] bg-[var(--orange-soft)] border border-[rgba(255,77,0,0.25)] mb-3">
          Apresentação Concluída
        </span>
        <h3 class="text-xl sm:text-2xl font-bold text-white mb-2">Pronto para criar sua equipe de agentes?</h3>
        <p class="text-xs sm:text-sm text-gray-300 max-w-md mb-6 leading-relaxed">
          Comece hoje mesmo com modelos prontos, aulas práticas e encontros semanais ao vivo.
        </p>
        <div class="flex flex-col sm:flex-row items-center gap-3">
          <button id="replayBtn" type="button" class="bg-white/10 hover:bg-white/15 border border-white/20 text-white text-xs sm:text-sm font-bold px-5 py-3 rounded-xl flex items-center gap-2 transition-transform duration-200 cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
            Assistir Novamente
          </button>
          <a href="#oferta" class="px-6 py-3 rounded-xl text-xs sm:text-sm font-bold text-white bg-[var(--orange)] hover:brightness-110 shadow-[0_10px_25px_rgba(255,77,0,0.4)] transition-all flex items-center gap-2">
            Entrar para a Comunidade
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
          </a>
        </div>
      </div>
    </div>'''

    right_col_html = f'''<div class="relative lg:sticky lg:top-[96px]">
  <div class="absolute -inset-[1px] rounded-[20px] bg-gradient-to-b from-[var(--orange)]/40 to-transparent blur-[1px]"></div>
  <div class="relative rounded-[20px] overflow-hidden bg-[var(--surface)] border border-[var(--border-2)] shadow-[0_20px_80px_rgba(0,0,0,0.6)]">
    <!-- Window Header -->
    <div class="h-[44px] flex items-center justify-between px-4 border-b border-[var(--border)] bg-[var(--surface-2)]">
      <div class="flex items-center gap-2">
        <div class="flex gap-1.5">
          <div class="h-3 w-3 rounded-full bg-[#FF5F57]"></div>
          <div class="h-3 w-3 rounded-full bg-[#FFBD2E]"></div>
          <div class="h-3 w-3 rounded-full bg-[#28CA42]"></div>
        </div>
        <span class="ml-3 text-[12px] font-mono text-[var(--muted)]">hermes-agent — demonstração oficial • 1 min</span>
      </div>
      <div class="h-5 px-2 rounded-full bg-[#0f0f0f] border border-[var(--border)] flex items-center gap-1.5 text-[10px] font-mono">
        <div class="h-1.5 w-1.5 rounded-full bg-[var(--green)] animate-pulse"></div> ONLINE
      </div>
    </div>

{video_markup}

    <!-- Live Telegram Simulation / Docker VPS Status -->
    <div class="p-4 bg-[#0E0E0E] font-mono text-[13px] border-t border-[var(--border)]">
      <div class="flex items-center gap-2 text-[11px] text-[var(--muted-2)] mb-3">
        <span>[09:41:12]</span>
        <span class="text-[var(--muted)]">agente inicializado</span>
        <span class="ml-auto px-2 py-0.5 rounded bg-[var(--surface-2)] border border-[var(--border)]">vps: hermes-prod-01</span>
      </div>
      <div class="space-y-3">
        <!-- Step 0: Audio message -->
        <div id="simStep0" class="transition-all duration-500 opacity-100 translate-y-0">
          <div class="flex justify-end">
            <div class="max-w-[85%] rounded-[16px] rounded-br-[4px] bg-[var(--surface-2)] border border-[var(--border)] px-3 py-2.5 flex items-center gap-2.5">
              <div class="h-7 w-7 rounded-full bg-[var(--orange)] grid place-items-center text-white shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3.5 w-3.5 fill-white"><polygon points="6 3 20 12 6 21 6 3"></polygon></svg>
              </div>
              <div>
                <div class="text-[10px] text-[var(--muted)]">Você • áudio 0:04</div>
                <div class="text-[12px] text-white mt-0.5 font-medium">“Hermes, manda relatório de ontem”</div>
              </div>
            </div>
          </div>
        </div>
        <!-- Step 1: Hermes thinking -->
        <div id="simStep1" class="transition-all duration-700 opacity-100 translate-y-0">
          <div class="flex gap-2">
            <div class="h-6 w-6 rounded-full bg-white text-black grid place-items-center font-bold text-[10px] shrink-0">H</div>
            <div class="max-w-[88%] rounded-[16px] rounded-bl-[4px] bg-[var(--surface-3)] border border-[var(--border)] px-3 py-2 text-[12px] text-[var(--text)]">
              Puxando dados do GA4 + Ads + CRM...
            </div>
          </div>
        </div>
        <!-- Step 2: PDF report card -->
        <div id="simStep2" class="transition-all duration-700 opacity-100 translate-y-0">
          <div class="flex gap-2">
            <div class="h-6 w-6 rounded-full bg-white text-black grid place-items-center font-bold text-[10px] shrink-0">H</div>
            <div class="max-w-[90%] rounded-[16px] rounded-bl-[4px] bg-white text-black p-3 shadow-lg">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="h-8 w-8 rounded-[6px] bg-[#111] grid place-items-center text-white shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><path d="M3 3v16a2 2 0 0 0 2 2h16"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>
                  </div>
                  <div>
                    <div class="text-[12px] font-bold">relatorio_ontem.pdf</div>
                    <div class="text-[10px] opacity-70">Lucro: +18% • ROAS 3.4</div>
                  </div>
                </div>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-black text-white">✓ Enviado</span>
              </div>
              <div class="mt-2 grid grid-cols-3 gap-1.5 text-center">
                <div class="rounded bg-[#F5F5F0] p-1.5"><div class="text-[9px] opacity-60">Vendas</div><div class="text-[11px] font-bold">R$8.4k</div></div>
                <div class="rounded bg-[#F5F5F0] p-1.5"><div class="text-[9px] opacity-60">Leads</div><div class="text-[11px] font-bold">127</div></div>
                <div class="rounded bg-[#111] text-white p-1.5"><div class="text-[9px] opacity-60">Ação IA</div><div class="text-[10px] font-bold">+20% Ads</div></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mt-4 flex items-center gap-2 text-[11px] text-[var(--muted-2)]">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3.5 w-3.5"><rect width="16" height="16" x="4" y="4" rx="2"></rect><rect width="6" height="6" x="9" y="9" rx="1"></rect><path d="M15 2v2"></path><path d="M15 20v2"></path><path d="M2 15h2"></path><path d="M2 9h2"></path><path d="M20 15h2"></path><path d="M20 9h2"></path><path d="M9 2v2"></path><path d="M9 20v2"></path></svg>
        <span>Executando em Docker • firewall ativo • custo VPS $6/mês</span>
      </div>
    </div>

    <!-- Window Footer -->
    <div class="px-4 py-3 bg-[var(--surface-2)] border-t border-[var(--border)] flex items-center justify-between">
      <div class="text-[11px] text-[var(--muted)]">
        ⚡ Agentes ativos: <b class="text-white">7</b> • Uptime 99.9%
      </div>
      <div class="text-[10px] tracking-widest px-2 py-1 rounded-full bg-[var(--orange)] text-white font-bold">
        PILOTO AUTOMÁTICO
      </div>
    </div>
  </div>

  <!-- Floating pill -->
  <div class="absolute -right-3 -bottom-6 hidden lg:flex items-center gap-2 px-3 py-2 rounded-full bg-white text-black text-[11px] font-semibold shadow-xl rotate-[-2deg]">
    <span class="h-5 w-5 rounded-full bg-black text-white grid place-items-center text-[10px]">↗</span>
    sem prompt. só resultado.
  </div>
</div>'''

    sec1_final = left_col_html + right_col_html + '</div></div></section>'

    # Section 2
    sec2_html = rendered_html[15749:22840]

    # Section 3
    sec3_html = rendered_html[22840:33517]
    # Update "Instalar em 15 min" links to href="#oferta"
    sec3_html = re.sub(
        r'<div class="mt-5 flex items-center gap-2 text-\[12px\] font-semibold\">(.*?)</div>',
        r'<a href="#oferta" class="mt-5 flex items-center gap-2 text-[12px] font-semibold text-white/80 hover:text-[var(--orange)] transition cursor-pointer">\1</a>',
        sec3_html
    )

    # Section 4
    sec4_html = rendered_html[33517:38123]

    # Section 5
    sec5_html = rendered_html[38123:41709]

    # Section 6 (Custo comparação)
    sec6_html = rendered_html[41709:46559]
    # In Card 3 (Comunidade Agêntica), add CTA button
    sec6_card3_needle = 'Economize R$29.500 vs humano</li></ul></div>'
    sec6_card3_subst = 'Economize R$29.500 vs humano</li></ul><a href="#oferta" class="mt-6 block w-full py-3 px-4 rounded-xl bg-[var(--orange)] text-white text-xs font-bold text-center tracking-wide hover:brightness-110 transition shadow-lg shadow-[rgba(255,77,0,0.3)]">TRAVAR R$497/ANO →</a></div>'
    sec6_html = sec6_html.replace(sec6_card3_needle, sec6_card3_subst)

    # Section 7 (#oferta - Plano Anual)
    sec7_html = rendered_html[46559:55299]
    # Replace dummy checkout link with Hotmart annual checkout link
    hotmart_anual_url = "https://pay.hotmart.com/L107410278Y?checkoutMode=2&off=yjri55cz"
    sec7_html = re.sub(
        r'<a href="#checkout"[^>]*>.*?</a>',
        f'''<a href="{hotmart_anual_url}" target="_blank" rel="noopener noreferrer" id="mainBuyButton" data-event="cta_anual_click" class="mt-7 group relative flex w-full items-center justify-center h-[56px] rounded-[14px] bg-[var(--orange)] text-white font-[800] tracking-[-0.01em] text-[15px] hover:brightness-110 transition overflow-hidden shadow-[0_10px_30px_rgba(255,77,0,0.4)]">
  <span class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></span>
  SIM, QUERO TRAVAR MEU PREÇO POR R$497/ANO
</a>''',
        sec7_html,
        flags=re.DOTALL
    )
    # Remove dummy checkout feedback if present
    sec7_html = re.sub(
        r'<div class="mt-3 rounded-\[10px\] bg-white text-black px-3 py-2\.5.*?</div>',
        '',
        sec7_html,
        flags=re.DOTALL
    )
    # Add id to timer spans
    sec7_html = re.sub(
        r'<span class="h-8 min-w-\[36px\] grid place-items-center rounded-\[8px\] bg-white text-black px-2">14</span><span class="opacity-50">:</span><span class="h-8 min-w-\[36px\] grid place-items-center rounded-\[8px\] bg-white text-black px-2">47</span>',
        r'<span id="timerMinutes" class="h-8 min-w-[36px] grid place-items-center rounded-[8px] bg-white text-black px-2">14</span><span class="opacity-50">:</span><span id="timerSeconds" class="h-8 min-w-[36px] grid place-items-center rounded-[8px] bg-white text-black px-2">47</span>',
        sec7_html
    )

    # Section 8 (FAQ)
    sec8_html = rendered_html[55299:58687]
    # Re-structure FAQ with faq-item and faq-accordion-btn classes
    faq_items = [
        {
            "q": "Preciso saber programar?",
            "a": "Não. O Hermes Desktop é 100% visual, arrasta-e-solta. Você não abre terminal. Na aula 1 você já instala seu primeiro agente e vê ele postando. O DevOps (Docker+Firewall) já vem pronto."
        },
        {
            "q": "Preciso de PC potente?",
            "a": "Não. Você monta no seu PC em 15 min e depois manda pra VPS de $6/mês com 1 clique. Seu PC pode ser fraco e pode desligar. A operação fica 24/7 na nuvem."
        },
        {
            "q": "E se eu travar?",
            "a": "Você tem 4 encontros ao vivo por mês pra compartilhar tela e destravar na hora. Além da comunidade que responde rápido. Ninguém fica sozinho às 3h da manhã."
        },
        {
            "q": "É curso de prompt?",
            "a": "Não. Prompt é o jeito antigo: você trabalha pra IA. Aqui é agêntico: a IA trabalha pra você. Agentes autônomos que executam, publicam, corrigem e te mandam relatório sozinhos."
        }
    ]
    faq_rendered = []
    for i, fq in enumerate(faq_items):
        is_first = (i == 0)
        grid_cls = "grid-rows-[1fr] opacity-100" if is_first else "grid-rows-[0fr] opacity-0"
        icon_char = "−" if is_first else "+"
        icon_wrapper_cls = "bg-white text-black border-white" if is_first else "bg-transparent border-[var(--border)] text-[var(--muted)]"
        faq_rendered.append(f'''      <div class="faq-item">
        <button type="button" class="faq-accordion-btn w-full text-left px-6 py-5 flex items-start justify-between gap-6 hover:bg-[var(--surface-2)] transition cursor-pointer">
          <div>
            <div class="text-[15px] font-semibold">{fq['q']}</div>
            <div class="faq-content grid transition-all duration-300 {grid_cls} mt-2">
              <div class="overflow-hidden">
                <div class="text-[13px] leading-[1.6] text-[var(--muted)] pb-1">{fq['a']}</div>
              </div>
            </div>
          </div>
          <div class="faq-icon-wrapper h-8 w-8 shrink-0 rounded-full border grid place-items-center transition {icon_wrapper_cls}">
            <span class="faq-icon text-[18px] leading-none">{icon_char}</span>
          </div>
        </button>
      </div>''')
    faq_box_html = '<div class="mt-8 divide-y divide-[var(--border)] rounded-[18px] border border-[var(--border)] overflow-hidden bg-[#121212]">\n' + '\n'.join(faq_rendered) + '\n    </div>'
    sec8_html = f'''<section class="border-t border-[var(--border)] bg-[var(--surface)]/60">
  <div class="mx-auto max-w-[900px] px-5 lg:px-8 py-[64px] lg:py-[88px]">
    <h2 class="text-[26px] lg:text-[36px] font-[800] tracking-[-0.03em] text-center">Tira as pedras do caminho</h2>
    {faq_box_html}
  </div>
</section>'''

    # Section 9
    sec9_html = rendered_html[58687:62965]

    # Toast & Mobile Sticky Bar
    toast_html = '''  <!-- Floating Social Proof Toast -->
  <div id="socialProofToast" class="fixed left-4 bottom-[84px] md:bottom-6 z-30 transition-all duration-500 translate-y-3 opacity-0 pointer-events-none">
    <div class="flex items-center gap-3 px-4 py-3 rounded-full bg-[var(--surface)] border border-[var(--border-2)] shadow-[0_12px_40px_rgba(0,0,0,0.6)] backdrop-blur">
      <div id="toastInitial" class="h-8 w-8 rounded-full bg-white text-black grid place-items-center font-bold text-[11px]">M</div>
      <div class="text-[12px] leading-[1.2]">
        <b id="toastName" class="font-semibold text-white">Marcos de Brusque</b> 
        <span id="toastAction" class="text-[var(--muted)]">garantiu o 2º lote há 1 min</span>
      </div>
      <div class="ml-2 h-2 w-2 rounded-full bg-[var(--green)] animate-pulse"></div>
    </div>
  </div>

  <!-- Sticky Mobile Bottom Bar -->
  <div class="lg:hidden fixed bottom-0 inset-x-0 z-40 border-t border-[var(--border)] bg-[rgba(10,10,10,0.92)] backdrop-blur-xl p-3" style="padding-bottom: calc(12px + var(--safe-area-inset-bottom, 0px));">
    <div class="flex items-center gap-3">
      <div class="flex-1">
        <div class="text-[11px] text-[var(--muted)] line-through">De R$2.364</div>
        <div class="text-[18px] font-[800] -mt-1 text-white">R$497/ano <span class="text-[11px] font-normal text-[var(--muted)]">• 2º lote</span></div>
      </div>
      <a href="#oferta" class="flex-1 h-[48px] rounded-[12px] bg-[var(--orange)] text-white font-bold text-[13px] grid place-items-center hover:brightness-110 transition shadow-[0_8px_20px_rgba(255,77,0,0.4)]">
        TRAVAR PREÇO →
      </a>
    </div>
  </div>'''

    # Complete scripts
    scripts_html = '''  <!-- ============================================================
       SCRIPTS: LUCIDE, VIDEO CONTROLLER, TIMERS, ACCORDIONS, TRACKING
       ============================================================ -->
  <script>
    // 1. Initialize Lucide Icons
    function renderLucideIcons() {
      if (typeof lucide !== 'undefined' && typeof lucide.createIcons === 'function') {
        lucide.createIcons();
      } else {
        setTimeout(renderLucideIcons, 40);
      }
    }
    renderLucideIcons();
    window.addEventListener('load', renderLucideIcons);
    document.addEventListener('DOMContentLoaded', renderLucideIcons);

    // 2. Mobile Menu Controller
    (() => {
      const btn = document.getElementById('mobileMenuBtn');
      const menu = document.getElementById('mobileMenu');
      if (!btn || !menu) return;

      const openIcon = btn.querySelector('.menu-open-icon');
      const closeIcon = btn.querySelector('.menu-close-icon');

      function toggleMenu(forceOpen) {
        const isCurrentlyOpen = !menu.classList.contains('hidden');
        const shouldOpen = forceOpen !== undefined ? forceOpen : !isCurrentlyOpen;

        if (shouldOpen) {
          menu.classList.remove('hidden');
          btn.setAttribute('aria-expanded', 'true');
          if (openIcon) openIcon.classList.add('hidden');
          if (closeIcon) closeIcon.classList.remove('hidden');
        } else {
          menu.classList.add('hidden');
          btn.setAttribute('aria-expanded', 'false');
          if (openIcon) openIcon.classList.remove('hidden');
          if (closeIcon) closeIcon.classList.add('hidden');
        }
      }

      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
      });

      menu.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => toggleMenu(false));
      });

      document.addEventListener('click', (e) => {
        if (!menu.contains(e.target) && !btn.contains(e.target) && !menu.classList.contains('hidden')) {
          toggleMenu(false);
        }
      });

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !menu.classList.contains('hidden')) {
          toggleMenu(false);
        }
      });
    })();

    // 3. Hero Video Controller, Subtitle Sync, Replay Overlay & Unmute
    (() => {
      const video = document.getElementById('heroVideo');
      const unmuteBtn = document.getElementById('unmuteOverlay');
      const replayOverlay = document.getElementById('replayOverlay');
      const replayBtn = document.getElementById('replayBtn');
      const captionText = document.getElementById('captionText');
      const wrapper = document.getElementById('videoWrapper');
      const playOverlay = document.getElementById('playOverlay');
      const startVideoBtn = document.getElementById('startVideoBtn');
      if (!video) return;

      let hasStarted = false;

      // Legendas com timestamps exatos sincronizados
      const subtitles = [
        { start: 0.5, end: 4.2, text: "Seja muito bem-vinda, seja muito bem-vindo à Inteligência Agêntica!" },
        { start: 4.3, end: 9.5, text: "Esse é o lugar onde você finalmente vai parar de perder tempo..." },
        { start: 9.6, end: 14.5, text: "...copiando e colando prompts em caixinhas de chat da internet." },
        { start: 14.8, end: 18.2, text: "Chega de ser o digitador da sua inteligência artificial!" },
        { start: 18.4, end: 23.0, text: "Aqui, você vai aprender a colocar assistentes virtuais inteligentes..." },
        { start: 23.1, end: 27.5, text: "...trabalhando pra você no piloto automático: 24 horas por dia, direto na nuvem..." },
        { start: 27.6, end: 32.8, text: "...com você no comando pelo celular e sem precisar escrever nenhuma linha de código." },
        { start: 33.2, end: 37.0, text: "Você vai ter acesso a aulas práticas e direto ao ponto..." },
        { start: 37.1, end: 41.5, text: "...modelos 100% prontos de agentes pra você simplesmente copiar e ativar..." },
        { start: 41.6, end: 45.8, text: "...nossa comunidade exclusiva de alunos e encontros semanais ao vivo comigo..." },
        { start: 45.9, end: 50.0, text: "...pra gente construir e destravar soluções juntos." },
        { start: 50.4, end: 55.2, text: "Se você quer parar de perder horas com trabalho manual..." },
        { start: 55.3, end: 59.8, text: "...e ter a sua própria equipe de robôs trabalhando por você todos os dias..." },
        { start: 60.0, end: 62.8, text: "...o seu próximo passo tá logo aqui." },
        { start: 63.0, end: 66.0, text: "Clique no botão abaixo, garanta a sua vaga e venha fazer parte!" },
        { start: 66.1, end: 67.5, text: "Te vejo lá dentro!" }
      ];

      // Sincronização de Legendas
      video.addEventListener('timeupdate', () => {
        if (!captionText) return;
        const ct = video.currentTime;
        const currentSub = subtitles.find(s => ct >= s.start && ct <= s.end);
        if (currentSub) {
          if (captionText.textContent !== currentSub.text) {
            captionText.textContent = currentSub.text;
          }
          captionText.style.opacity = '1';
        } else {
          captionText.style.opacity = '0';
        }
      });

      // Iniciar reprodução com som pelo botão de alerta / play
      const startVideo = (e) => {
        if (e) e.stopPropagation();
        hasStarted = true;
        if (playOverlay) {
          playOverlay.style.opacity = '0';
          playOverlay.style.pointerEvents = 'none';
        }
        video.muted = false;
        const playPromise = video.play();
        if (playPromise !== undefined) {
          playPromise.catch(() => {
            video.muted = true;
            video.play().catch(() => {});
            if (unmuteBtn) {
              unmuteBtn.style.opacity = '1';
              unmuteBtn.style.pointerEvents = 'auto';
            }
          });
        }
      };

      if (startVideoBtn) {
        startVideoBtn.addEventListener('click', startVideo);
      }
      if (playOverlay) {
        playOverlay.addEventListener('click', startVideo);
      }

      // Ativar Áudio (Fallback)
      const toggleSound = (e) => {
        if (e) e.stopPropagation();
        if (video.muted) {
          video.muted = false;
          video.play().catch(() => {});
          if (unmuteBtn) {
            unmuteBtn.style.opacity = '0';
            unmuteBtn.style.pointerEvents = 'none';
          }
        }
      };

      if (unmuteBtn) {
        unmuteBtn.addEventListener('click', toggleSound);
      }

      // Pausar / Despausar
      if (wrapper) {
        wrapper.addEventListener('click', (e) => {
          if (e.target.closest('#replayOverlay') || e.target.closest('#unmuteOverlay') || e.target.closest('#playOverlay')) return;
          if (!hasStarted) {
            startVideo(e);
            return;
          }
          if (video.ended) {
            if (replayBtn) replayBtn.click();
          } else if (video.paused) {
            video.play().catch(() => {});
          } else {
            video.pause();
          }
        });
      }

      // Vídeo concluído
      video.addEventListener('ended', () => {
        if (captionText) captionText.style.opacity = '0';
        if (replayOverlay) {
          replayOverlay.style.pointerEvents = 'auto';
          replayOverlay.style.opacity = '1';
        }
      });

      // Assistir Novamente
      if (replayBtn) {
        replayBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          if (replayOverlay) {
            replayOverlay.style.opacity = '0';
            replayOverlay.style.pointerEvents = 'none';
          }
          video.currentTime = 0;
          video.muted = false;
          video.play().catch(() => {});
          if (unmuteBtn) {
            unmuteBtn.style.opacity = '0';
            unmuteBtn.style.pointerEvents = 'none';
          }
        });
      }
    })();

    // 4. Urgency 30-Minute Countdown Timer
    (() => {
      const minEl = document.getElementById('timerMinutes');
      const secEl = document.getElementById('timerSeconds');
      if (!minEl || !secEl) return;

      const STORAGE_KEY = 'ia_anual_offer_deadline_v2';
      const DURATION_MS = 30 * 60 * 1000;

      let deadline = parseInt(localStorage.getItem(STORAGE_KEY), 10);
      const now = Date.now();

      if (!deadline || isNaN(deadline) || (now - deadline > 24 * 60 * 60 * 1000)) {
        deadline = now + DURATION_MS;
        localStorage.setItem(STORAGE_KEY, deadline.toString());
      }

      function updateTimer() {
        const remaining = Math.max(0, deadline - Date.now());
        const totalSec = Math.floor(remaining / 1000);
        const mins = Math.floor(totalSec / 60);
        const secs = totalSec % 60;

        minEl.textContent = String(mins).padStart(2, '0');
        secEl.textContent = String(secs).padStart(2, '0');

        if (remaining <= 0) {
          clearInterval(interval);
        }
      }

      updateTimer();
      const interval = setInterval(updateTimer, 1000);
    })();

    // 5. FAQ Accordion Toggle
    (() => {
      const btns = document.querySelectorAll('.faq-accordion-btn');
      btns.forEach((btn) => {
        btn.addEventListener('click', () => {
          const parent = btn.closest('.faq-item');
          const content = parent.querySelector('.faq-content');
          const icon = parent.querySelector('.faq-icon');
          const isOpen = content.classList.contains('grid-rows-[1fr]');

          // Close all items
          document.querySelectorAll('.faq-item').forEach(item => {
            const c = item.querySelector('.faq-content');
            const ic = item.querySelector('.faq-icon');
            const wr = item.querySelector('.faq-icon-wrapper');
            if (c) {
              c.classList.remove('grid-rows-[1fr]', 'opacity-100');
              c.classList.add('grid-rows-[0fr]', 'opacity-0');
            }
            if (ic) ic.textContent = '+';
            if (wr) {
              wr.classList.remove('bg-white', 'text-black', 'border-white');
              wr.classList.add('bg-transparent', 'border-[var(--border)]', 'text-[var(--muted)]');
            }
          });

          // Toggle current
          if (!isOpen) {
            content.classList.remove('grid-rows-[0fr]', 'opacity-0');
            content.classList.add('grid-rows-[1fr]', 'opacity-100');
            if (icon) icon.textContent = '−';
            const wr = parent.querySelector('.faq-icon-wrapper');
            if (wr) {
              wr.classList.remove('bg-transparent', 'border-[var(--border)]', 'text-[var(--muted)]');
              wr.classList.add('bg-white', 'text-black', 'border-white');
            }
          }
        });
      });
    })();

    // 6. Social Proof Toast Cycler
    (() => {
      const toast = document.getElementById('socialProofToast');
      const toastInitial = document.getElementById('toastInitial');
      const toastName = document.getElementById('toastName');
      const toastAction = document.getElementById('toastAction');
      if (!toast || !toastName) return;

      const proofs = [
        { name: "Marcos de Brusque", action: "garantiu o 2º lote", min: 1 },
        { name: "Rafaela de Curitiba", action: "ativou o Hermes CMO", min: 2 },
        { name: "Diego de Floripa", action: "hospedou na VPS em 1 clique", min: 3 },
        { name: "Juliana de SP", action: "travou R$497/ano", min: 4 }
      ];
      let idx = 0;

      // Start after 4 seconds to prevent initial content overlap
      setTimeout(() => {
        toast.classList.remove('opacity-0', 'translate-y-3');
        toast.classList.add('opacity-100', 'translate-y-0');

        setInterval(() => {
          toast.classList.remove('opacity-100', 'translate-y-0');
          toast.classList.add('opacity-0', 'translate-y-3');
          setTimeout(() => {
            idx = (idx + 1) % proofs.length;
            const item = proofs[idx];
            if (toastInitial) toastInitial.textContent = item.name.charAt(0);
            if (toastName) toastName.textContent = item.name;
            if (toastAction) toastAction.textContent = item.action + " há " + item.min + " min";
            toast.classList.remove('opacity-0', 'translate-y-3');
            toast.classList.add('opacity-100', 'translate-y-0');
          }, 400);
        }, 4500);
      }, 4000);
    })();

    // 7. DataLayer Event Tracking
    window.dataLayer = window.dataLayer || [];
    document.querySelectorAll('[data-event]').forEach(el => {
      el.addEventListener('click', () => {
        window.dataLayer.push({
          event: el.dataset.event,
          timestamp: new Date().toISOString()
        });
      });
    });
  </script>'''

    # Complete HTML assembly
    assembled_html = f'''{head_start_html}  <!-- Fonts: Inter, Sora & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            obsidian: '#07070A',
            'obsidian-light': '#0E0E14',
            'obsidian-card': '#111118',
            magenta: '#C000FF',
            'magenta-dim': '#8B00B8',
            ciano: '#00E5FF',
            'ciano-dim': '#009DB8',
            ouro: '#DFBA6B',
            'ouro-light': '#F0D48A',
            'ouro-dark': '#B8952E',
          }},
          fontFamily: {{
            sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
          }},
        }},
      }},
    }}
  </script>

  <!-- Lucide Icons -->
  <script defer src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

  <!-- Proteção e Estabilidade dos Botões de Checkout -->
  <script>
    (function() {{
      var _origRemove = Element.prototype.remove;
      Element.prototype.remove = function() {{
        if (this && (
          (this.matches && this.matches('a[href*="hotmart.com"]')) ||
          (this.classList && this.classList.contains('hotmart-fb')) ||
          this.id === 'mainBuyButton'
        )) {{
          console.warn('[Checkout Guard] Tentativa indevida de remoção de botão de checkout bloqueada:', this);
          return;
        }}
        return _origRemove.apply(this, arguments);
      }};
    }})();
  </script>

  <!-- Pre-compiled Tailwind & Design System Styles -->
  <style>
{artifact_css}

    /* Custom Design Tokens */
    :root {{
      --bg: #0A0A0A;
      --surface: #141414;
      --surface-2: #1C1C1C;
      --surface-3: #232323;
      --border: #262626;
      --border-2: #2E2E2E;
      --orange: #FF4D00;
      --orange-soft: rgba(255,77,0,0.12);
      --orange-glow: rgba(255,77,0,0.35);
      --text: #F5F5F0;
      --muted: #9A9A94;
      --muted-2: #5A5A56;
      --red: #FF3B30;
      --green: #22C55E;
    }}

    * {{ scrollbar-width: thin; scrollbar-color: var(--border) transparent; }}
    html {{ scroll-behavior: smooth; }}
    .text-balance {{ text-wrap: balance; }}
    .glow-orange {{ box-shadow: 0 0 0 1px var(--orange), 0 0 40px var(--orange-glow); }}
    .glow-hover:hover {{ box-shadow: 0 0 0 1px var(--orange), 0 0 30px rgba(255,77,0,0.25); transform: translateY(-2px); }}
    .grid-lines {{
      background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
      background-size: 32px 32px;
      mask-image: radial-gradient(ellipse at center, black 60%, transparent 90%);
    }}

    /* Brand Header & Footer Styles */
    .glass {{
      background: rgba(17, 17, 24, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .top-bar {{
      background: rgba(7, 7, 10, 0.85);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .btn-gold {{
      background: linear-gradient(135deg, #B8952E 0%, #DFBA6B 35%, #F0D48A 50%, #DFBA6B 65%, #B8952E 100%);
      color: #07070A;
      font-weight: 800;
      transition: all 0.2s ease;
    }}
    .btn-gold:hover {{
      filter: brightness(1.1);
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(223, 186, 107, 0.4);
    }}
    .cta-pulse {{
      animation: ctaGlow 2.5s infinite;
    }}
    @keyframes ctaGlow {{
      0%, 100% {{ box-shadow: 0 0 15px rgba(223, 186, 107, 0.35); }}
      50% {{ box-shadow: 0 0 32px rgba(223, 186, 107, 0.7); }}
    }}
    .on-air-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.25rem 0.65rem;
      border-radius: 0.375rem;
      background: #7f1d1d;
      border: 1.5px solid #ef4444;
      box-shadow: 0 0 10px rgba(239, 68, 68, 0.5), inset 0 0 8px rgba(239, 68, 68, 0.3);
      color: #fee2e2;
      font-size: 0.6875rem;
      font-weight: 900;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      animation: onAirPulse 1.8s infinite ease-in-out;
      user-select: none;
      transition: transform 0.2s ease;
    }}
    .on-air-badge:hover {{
      transform: scale(1.05);
    }}
    .on-air-dot {{
      width: 0.5rem;
      height: 0.5rem;
      border-radius: 9999px;
      background-color: #ef4444;
      box-shadow: 0 0 8px #ef4444, 0 0 14px #ef4444;
      animation: onAirDot 1.8s infinite ease-in-out;
    }}
    @keyframes onAirPulse {{
      0%, 100% {{
        box-shadow: 0 0 8px rgba(239, 68, 68, 0.4), inset 0 0 6px rgba(239, 68, 68, 0.3);
        border-color: #ef4444;
      }}
      50% {{
        box-shadow: 0 0 18px rgba(239, 68, 68, 0.85), inset 0 0 12px rgba(239, 68, 68, 0.6);
        border-color: #f87171;
      }}
    }}
    @keyframes onAirDot {{
      0%, 100% {{ opacity: 0.45; transform: scale(0.9); }}
      50% {{ opacity: 1; transform: scale(1.15); }}
    }}

    /* Font isolation */
    .top-bar, .top-bar *, footer, footer * {{
      font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }}
    body, .landing-content {{
      font-family: 'Sora', system-ui, -apple-system, sans-serif;
    }}
    .font-mono, .font-mono * {{
      font-family: 'JetBrains Mono', monospace !important;
    }}
  </style>
</head>
<body class="min-h-screen bg-[var(--bg)] text-[var(--text)] selection:bg-[var(--orange)] selection:text-white antialiased overflow-x-clip">
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-M5JDK6W4"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  <!-- ============================================================
       TOP BAR (Navbar Fixa Padrão)
       ============================================================ -->
{navbar_html}

  <!-- ============================================================
       LANDING PAGE PRINCIPAL: INTELIGÊNCIA AGÊNTICA — PLANO ANUAL
       ============================================================ -->
  <main class="flex-grow pt-16 sm:pt-20 landing-content">
{sec1_final}
{sec2_html}
{sec3_html}
{sec4_html}
{sec5_html}
{sec6_html}
{sec7_html}
{sec8_html}
{sec9_html}
  </main>

{toast_html}

  <!-- ============================================================
       FOOTER (Rodapé Oficial Padrão)
       ============================================================ -->
{footer_html}

{scripts_html}
</body>
</html>'''

    with open(out_git_index, "w", encoding="utf-8") as f:
        f.write(assembled_html)
    print(f"Wrote {out_git_index} (len {len(assembled_html)})")

    with open(out_copy_index, "w", encoding="utf-8") as f:
        f.write(assembled_html)
    print(f"Wrote {out_copy_index}")

    with open(out_page_html, "w", encoding="utf-8") as f:
        f.write(assembled_html)
    print(f"Wrote {out_page_html}")

if __name__ == "__main__":
    build()
