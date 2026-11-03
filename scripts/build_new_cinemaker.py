import os
import re

def main():
    art_path = "C:/Users/Jean/AppData/Local/hermes/profiles/devops/attachments/Cinemaker-Nova-Pagina-Campea-4.html"
    scratch_sections_path = "C:/Users/Jean/AppData/Local/hermes/profiles/devops/cache/scratch/cinemaker_new_sections.html"
    old_index_path = "D:/DevCod/inteligencia-agentica/cinemaker/index.html"
    new_index_path = "D:/DevCod/inteligencia-agentica/cinemaker/index.html"
    copy_dir_path = "D:/DevCod/Inteligencia_agentica/cinemaker/index.html"

    with open(art_path, "r", encoding="utf-8") as f:
        art_html = f.read()

    with open(scratch_sections_path, "r", encoding="utf-8") as f:
        sections_html = f.read()

    with open(old_index_path, "r", encoding="utf-8") as f:
        old_html = f.read()

    # 1. Extract CSS from artifact
    style_match = re.search(r"<style>(.*?)</style>", art_html, re.DOTALL)
    artifact_css = style_match.group(1) if style_match else ""

    # 2. Extract Navbar from old_html
    nav_start = old_html.find('<nav class="top-bar fixed top-0 inset-x-0 z-50">')
    nav_end = old_html.find('</nav>') + len('</nav>')
    navbar_html = old_html[nav_start:nav_end]

    # 3. Extract Community Callout and Footer from old_html
    comm_start = old_html.find('<!-- ============================================================\n       BOTTOM COMMUNITY CALLOUT')
    if comm_start == -1:
        comm_start = old_html.find('<!-- BOTTOM COMMUNITY CALLOUT')
    if comm_start == -1:
        comm_start = old_html.find('<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 mb-20">')

    footer_end = old_html.find('</footer>') + len('</footer>')
    footer_and_comm_html = old_html[comm_start:footer_end]

    # 4. Prepare FAQ data with full questions and answers
    faq_data = [
        {
            "q": "Preciso saber de ComfyUI, Python ou Flow?",
            "a": "Não. Zero. O CineMaker é app nativo Flow já configurado. Você faz login no navegador e clica. Sem instalar nada, sem GPU local. Toda a engenharia já está otimizada por dentro. Você só descreve o que precisa ou cola um roteiro pronto da sua IA favorita."
        },
        {
            "q": "Consistência visual funciona mesmo para produto físico?",
            "a": "Sim, é o nosso maior diferencial. Usamos lock visual neural: cor, textura, logo, embalagem são ancorados. Preservação alta mesmo em vídeos de 2 a 10 minutos. Seu cliente não vê produto trocando de cor."
        },
        {
            "q": "Preciso pagar Flow ou outras assinaturas?",
            "a": "Não. Sem assinatura de Flow, sem ElevenLabs, sem CapCut Pro. Um pagamento de R$49,90, acesso ao app nativo + aula + presets personalizáveis. Roda 100% na nuvem, dentro do Flow."
        },
        {
            "q": "Posso usar meu áudio externo?",
            "a": "Não, e esse é o ponto. O CineMaker foi otimizado para usar os motores nativos do Flow (VO3.1, Omni, etc) que já geram voz neural e trilha de estúdio com ducking automático. Zero fricção. Você economiza R$300+/mês de ElevenLabs e não precisa sincronizar áudio externo. Tudo acontece dentro do motor, sem gambiarras. Voz e trilha são gerados DENTRO do próprio Flow."
        },
        {
            "q": "Quanto tempo para criar meu primeiro vídeo longo?",
            "a": "Média dos nossos usuários: 7 a 10 minutos do zero ao filme de 3 minutos pronto para postar. Se já tiver roteiro pronto da sua IA favorita (ChatGPT, Claude), menos de 5 min. Render em nuvem, você não precisa de PC gamer."
        },
        {
            "q": "Funciona para e-commerce, afiliado, agência e dark?",
            "a": "Foi feito para quem vende. E-commerce mantém produto idêntico, afiliado testa ângulos/dia sem aparecer, agência escala entrega, canal dark cria filmes de 2-10 min consistentes sem rosto. Mesma fábrica, ângulos diferentes."
        },
        {
            "q": "E se eu não gostar?",
            "a": "Garantia de 7 dias incondicional. Ative, crie seus filmes. Se achar que não é a produtora mais rápida que já usou, manda um e-mail e devolvemos 100%. Risco zero. O produto custa R$49,90 e entrega o que promete: app nativo + aula + presets."
        }
    ]

    items_html = []
    for i, item in enumerate(faq_data):
        is_first = (i == 0)
        border_bg = "border-[#FF4D12]/40 bg-[#151518]" if is_first else "border-white/10 bg-[#121214] hover:border-white/20"
        icon_cls = "bg-white text-black border-white rotate-180" if is_first else "border-white/10 text-white/40"
        ans_hidden = "" if is_first else "hidden "
        
        item_block = f'''        <div class="faq-item rounded-[14px] border transition-colors {border_bg}">
          <button type="button" class="faq-btn w-full flex items-center justify-between gap-4 p-5 text-left cursor-pointer">
            <span class="font-bold text-[14px] md:text-[15px] leading-[1.3] text-white">{item['q']}</span>
            <span class="faq-icon-wrapper h-7 w-7 rounded-full border flex items-center justify-center shrink-0 transition-transform {icon_cls}">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down h-4 w-4"><path d="m6 9 6 6 6-6"></path></svg>
            </span>
          </button>
          <div class="faq-answer {ans_hidden}px-5 pb-5 -mt-1 text-[13px] md:text-[14px] leading-[1.6] text-white/50">{item['a']}</div>
        </div>'''
        items_html.append(item_block)

    full_faq_items = '<div class="space-y-2">\n' + '\n'.join(items_html) + '\n      </div>'

    # Replace FAQ items in sections_html
    faq_start = sections_html.find('05 — DÚVIDAS QUE TRAVAM VENDA')
    sy2_start = sections_html.find('<div class="space-y-2">', faq_start)
    sy2_end = sections_html.find('</div><div class="mt-12 text-center">', sy2_start) + len('</div>')
    sections_html = sections_html[:sy2_start] + full_faq_items + sections_html[sy2_end:]

    # Adjust alert bar from sticky top-0 to standard flow under navbar
    sections_html = sections_html.replace(
        'class="sticky top-0 z-50 border-b border-[var(--border)] bg-[#0A0A0B]/90 backdrop-blur-xl" style="top: var(--safe-area-inset-top);"',
        'class="border-b border-[var(--border)] bg-[#0A0A0B]/90 backdrop-blur-xl"'
    )

    # Update timer in section #oferta
    timer_old = '<span class="bg-white text-black rounded-[8px] px-3 py-1">13</span><span class="pt-1">:</span><span class="bg-white text-black rounded-[8px] px-3 py-1">14</span>'
    timer_new = '<span id="timer-min" class="bg-white text-black rounded-[8px] px-3 py-1">14</span><span class="pt-1">:</span><span id="timer-sec" class="bg-white text-black rounded-[8px] px-3 py-1">47</span>'
    sections_html = sections_html.replace(timer_old, timer_new)

    # Update checkout link in section #oferta
    checkout_old = 'href="#checkout" class="mt-6 w-full rounded-full bg-[#FF4D12] hover:bg-[#FF5A26] text-black font-[800] text-[16px] md:text-[18px] uppercase tracking-[-0.01em] py-[18px] md:py-[20px] flex items-center justify-center gap-3 transition-colors cursor-pointer" style="box-shadow: 0 0 40px -10px var(--accent-glow);"'
    checkout_new = 'href="https://pay.hotmart.com/C108132324U?checkoutMode=2&off=zpo5cf1n" target="_blank" rel="noopener noreferrer" id="mainBuyButton" class="mt-6 w-full rounded-full bg-[#FF4D12] hover:bg-[#FF5A26] text-black font-[800] text-[16px] md:text-[18px] uppercase tracking-[-0.01em] py-[18px] md:py-[20px] flex items-center justify-center gap-3 transition-colors cursor-pointer" style="box-shadow: 0 0 40px -10px var(--accent-glow);"'
    sections_html = sections_html.replace(checkout_old, checkout_new)

    # Remove 12x de (produto com pagamento unico de R$49,90)
    sections_html = sections_html.replace(
        '<div class="text-[11px] text-white/30">12x de</div>',
        ''
    )
    sections_html = sections_html.replace(
        '<div class="mono text-[10px] text-white/30">12x de</div>',
        ''
    )

    # Remove dummy checkout feedback
    sections_html = sections_html.replace(
        '<div id="checkout-feedback" class="hidden mt-3 rounded-full bg-[#22C55E] px-4 py-2 text-center mono text-[11px] font-bold text-black"></div>',
        ''
    )

    # Update Hero CTA with id
    sections_html = sections_html.replace(
        'class="group relative w-full md:w-auto inline-flex items-center justify-center gap-3 rounded-full bg-white px-8 md:px-10 py-[18px] md:py-[20px] text-[15px] md:text-[18px] font-[800] tracking-[-0.01em] text-black uppercase transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer" style="animation: 2.2s ease 0s infinite normal none running pulse-glow;"',
        'id="hero-cta" class="group relative w-full md:w-auto inline-flex items-center justify-center gap-3 rounded-full bg-white px-8 md:px-10 py-[18px] md:py-[20px] text-[15px] md:text-[18px] font-[800] tracking-[-0.01em] text-black uppercase transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer" style="animation: 2.2s ease 0s infinite normal none running pulse-glow;"'
    )

    # Extract <head> scripts & metadata from old_html (up to tailwind comment)
    head_end = old_html.find('<!-- Tailwind CSS CDN -->')
    head_start_html = old_html[:head_end]

    # Assemble complete page
    final_html = f'''{head_start_html}  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">

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

  <!-- Pre-compiled Tailwind & Custom Styles for CineMaker -->
  <style>
{artifact_css}

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
    .top-bar, .top-bar *, footer, footer *, #community-callout, #community-callout * {{
      font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }}
    .cinemaker-content, .cinemaker-content * {{
      font-family: 'Bricolage Grotesque', system-ui, -apple-system, sans-serif;
    }}
    .mono, .mono * {{
      font-family: 'Geist Mono', monospace !important;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased bg-[#0A0A0B] text-white selection:bg-[#FF4D12] selection:text-white">
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-M5JDK6W4"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  <!-- ============================================================
       TOP BAR (Navbar Fixa)
       ============================================================ -->
{navbar_html}

  <!-- ============================================================
       CINEMAKER — NOVA PÁGINA CAMPEÃ (CONTEÚDO PRINCIPAL)
       ============================================================ -->
  <main class="flex-grow pt-16 sm:pt-20 cinemaker-content">
{sections_html}

    <!-- ============================================================
         BOTTOM COMMUNITY CALLOUT (CTA DA COMUNIDADE — PADRÃO OBRIGATÓRIO)
         ============================================================ -->
    <div id="community-callout">
{footer_and_comm_html}

  <!-- ============================================================
       SCRIPTS: MOBILE MENU, FAQ, TIMER, HERO CTA, LUCIDE ICONS
       ============================================================ -->
  <script>
    // 1. Inicialização do Lucide Icons
    function renderLucideIcons() {{
      if (window.lucide && typeof window.lucide.createIcons === 'function') {{
        window.lucide.createIcons();
      }} else {{
        setTimeout(renderLucideIcons, 40);
      }}
    }}
    renderLucideIcons();
    window.addEventListener('load', renderLucideIcons);

    document.addEventListener('DOMContentLoaded', () => {{
      renderLucideIcons();

      // 2. Mobile Menu
      const mobileMenuBtn = document.getElementById('mobileMenuBtn');
      const mobileMenu = document.getElementById('mobileMenu');
      const openIcon = mobileMenuBtn?.querySelector('.menu-open-icon');
      const closeIcon = mobileMenuBtn?.querySelector('.menu-close-icon');

      if (mobileMenuBtn && mobileMenu) {{
        mobileMenuBtn.addEventListener('click', () => {{
          const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
          mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
          mobileMenu.classList.toggle('hidden');
          openIcon?.classList.toggle('hidden');
          closeIcon?.classList.toggle('hidden');
        }});

        // Close on link click
        document.querySelectorAll('.mobile-nav-link').forEach(link => {{
          link.addEventListener('click', () => {{
            mobileMenu.classList.add('hidden');
            mobileMenuBtn.setAttribute('aria-expanded', 'false');
            openIcon?.classList.remove('hidden');
            closeIcon?.classList.add('hidden');
          }});
        }});
      }}

      // 3. FAQ Accordion Toggle
      document.querySelectorAll('.faq-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const item = btn.closest('.faq-item');
          const answer = item.querySelector('.faq-answer');
          const iconWrapper = item.querySelector('.faq-icon-wrapper');
          const isOpen = !answer.classList.contains('hidden');

          // Close all FAQ items
          document.querySelectorAll('.faq-item').forEach(other => {{
            other.classList.remove('border-[#FF4D12]/40', 'bg-[#151518]');
            other.classList.add('border-white/10', 'bg-[#121214]');
            const otherAns = other.querySelector('.faq-answer');
            if (otherAns) otherAns.classList.add('hidden');
            const otherIcon = other.querySelector('.faq-icon-wrapper');
            if (otherIcon) {{
              otherIcon.classList.remove('bg-white', 'text-black', 'border-white', 'rotate-180');
              otherIcon.classList.add('border-white/10', 'text-white/40');
            }}
          }});

          // If clicked item was not open, open it
          if (!isOpen) {{
            item.classList.remove('border-white/10', 'bg-[#121214]');
            item.classList.add('border-[#FF4D12]/40', 'bg-[#151518]');
            answer.classList.remove('hidden');
            iconWrapper.classList.remove('border-white/10', 'text-white/40');
            iconWrapper.classList.add('bg-white', 'text-black', 'border-white', 'rotate-180');
          }}
        }});
      }});

      // 4. Countdown Timer Regressivo
      let m = 14;
      let s = 47;
      const minEl = document.getElementById('timer-min');
      const secEl = document.getElementById('timer-sec');
      setInterval(() => {{
        if (s <= 0) {{
          if (m <= 0) {{
            m = 14;
            s = 59;
          }} else {{
            m--;
            s = 59;
          }}
        }} else {{
          s--;
        }}
        if (minEl) minEl.textContent = String(m).padStart(2, '0');
        if (secEl) secEl.textContent = String(s).padStart(2, '0');
      }}, 1000);

      // 5. Hero CTA Smooth Scroll & Feedback
      const heroBtn = document.getElementById('hero-cta');
      if (heroBtn) {{
        heroBtn.addEventListener('click', (e) => {{
          const label = heroBtn.querySelector('[data-label]');
          const heroFeedback = document.getElementById('hero-feedback');
          if (label) {{
            const orig = label.textContent;
            label.textContent = '✓ REDIRECIONANDO PARA OFERTA...';
            setTimeout(() => {{ label.textContent = orig; }}, 2500);
          }}
          if (heroFeedback) {{
            heroFeedback.classList.remove('hidden');
            setTimeout(() => {{ heroFeedback.classList.add('hidden'); }}, 2500);
          }}
        }});
      }}
    }});
  </script>
</body>
</html>
'''

    with open(new_index_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    # Sync to D:\DevCod\Inteligencia_agentica\cinemaker\index.html
    os.makedirs(os.path.dirname(copy_dir_path), exist_ok=True)
    with open(copy_dir_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Successfully generated {new_index_path} and synced to {copy_dir_path}! Total length: {len(final_html)} bytes.")

if __name__ == "__main__":
    main()
