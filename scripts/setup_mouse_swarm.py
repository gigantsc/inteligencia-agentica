#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integra o enxame de cursores (@ruvector/mouse-swarm — github:ruvnet/mouse-swarm)
na Hero Section da landing page (index.html).

Princípio inegociável: a animação é 100% ADITIVA. Nada é escondido por CSS — se o
módulo não carregar (rede, bloqueio, navegador antigo) a página fica exatamente
como era. O próprio módulo esconde/revela os alvos durante a montagem e restaura
o conteúdo se ocorrer erro.

Idempotente: reexecutar não duplica atributos, controles, CSS nem script.
Se alguma âncora não for encontrada exatamente uma vez, aborta sem gravar.

- Marca 10 elementos da primeira dobra com data-swarm-item (+order/role/group/effect)
- Injeta o CSS dos controles (fora do fluxo: zero layout shift) no <head>
- Injeta <link rel="modulepreload"> para o módulo começar cedo
- Injeta a barra de controles (Pausar / Pular / Repetir), oculta por padrão
- Injeta o inicializador (script clássico, antes de </body>)
"""
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

# --------------------------------------------------------------- alvos da Hero
# Tags completas (com '>' final) presentes exatamente uma vez no HTML.
# (tag, atributos do enxame) — ordem = sequência de montagem da página.
TARGETS = [
    ('<div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--orange-soft)]'
     ' border border-[rgba(255,77,0,0.25)] text-[11px] sm:text-[12px] tracking-[0.14em] font-bold'
     ' text-orange-400 mb-3">',
     'data-swarm-item data-swarm-order="1" data-swarm-role="Scout"'),

    ('<h1 class="text-[28px] sm:text-[38px] lg:text-[44px] xl:text-[48px] leading-[1.04]'
     ' tracking-[-0.04em] font-[800] text-balance">',
     'data-swarm-item data-swarm-order="2" data-swarm-role="Copy"'),

    ('<div class="relative lg:sticky lg:top-[96px]">',
     'data-swarm-item data-swarm-order="3" data-swarm-role="Dev"'),

    ('<p class="mt-3 text-[14px] sm:text-[15px] lg:text-[16px] leading-[1.5] text-[var(--muted)]'
     ' max-w-[58ch] text-balance">',
     'data-swarm-item data-swarm-order="4" data-swarm-role="Copy"'),

    ('<a href="#oferta" class="group relative flex w-full sm:w-auto sm:inline-flex items-center'
     ' justify-center gap-3 px-8 h-[60px] rounded-[14px] bg-[var(--orange)] text-white font-bold'
     ' text-[14px] sm:text-[15px] tracking-[-0.01em] overflow-hidden hover:brightness-110 transition">',
     'data-swarm-item data-swarm-order="5" data-swarm-role="Growth" data-swarm-effect="drag"'),

    ('<div class="mt-3 flex flex-wrap items-center gap-3 text-[12px] text-[var(--muted)]">',
     'data-swarm-item data-swarm-order="6" data-swarm-group="proof" data-swarm-role="Ops"'),

    ('<div class="mt-4 inline-flex items-center gap-2 px-3 py-2 rounded-full bg-[var(--surface)]'
     ' border border-[var(--border)] text-[11px]">',
     'data-swarm-item data-swarm-order="7" data-swarm-group="proof"'),
]

# Cards de métricas: as três tags são idênticas, diferenciadas pelo texto interno.
CARD_TAG = '<div class="rounded-[12px] bg-[var(--surface)] border border-[var(--border)] px-4 py-3">'
CARD_TARGETS = [
    ('4x/mês</div>', 'data-swarm-item data-swarm-order="8" data-swarm-group="stats" data-swarm-role="Data"'),
    ('24/7</div>', 'data-swarm-item data-swarm-order="9" data-swarm-group="stats"'),
    ('7 dias</div>', 'data-swarm-item data-swarm-order="10" data-swarm-group="stats"'),
]

# ------------------------------------------------------------- CSS no <head>
# Os controles ficam fora do fluxo (absolute/fixed): aparecer e desaparecer não
# desloca nada na página (zero layout shift) e não cobrem conteúdo importante.
# Nenhuma regra aqui esconde conteúdo da Hero.
HEAD_CSS = """
    /* Mouse Swarm Reveal — controles da montagem (posicionados fora do fluxo).
       Nada aqui esconde conteúdo: a página segue visível mesmo sem o módulo. */
    #swarmControls {
      position: absolute; right: 0; bottom: -34px; z-index: 30;
      display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem;
      padding: 5px 10px; border-radius: 999px;
      background: rgba(10, 10, 10, 0.92); border: 1px solid var(--border);
      -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px);
      font-size: 11px; color: var(--muted);
    }
    #swarmControls[hidden] { display: none !important; }
    #swarmControls button:focus-visible { outline: 2px solid var(--orange); outline-offset: 2px; }
    @media (max-width: 1023px) {
      /* Mobile: pílula flutuante acima do rodapé (livra toast de prova social e barra de CTA) */
      #swarmControls:not([hidden]) { position: fixed; right: 12px; bottom: 150px; left: auto; }
    }
"""

HEAD_LINK = """  <!-- Mouse Swarm Reveal: pré-carrega o módulo do enxame de cursores -->
  <link rel="modulepreload" href="/static/js/mouse-swarm-v3.js">
"""

# ------------------------------------------------- controles (fora dos alvos)
CONTROLS = """<div id="swarmControls" role="group" aria-label="Controles da animação de montagem da página" hidden>
  <span class="inline-flex items-center gap-1.5" aria-hidden="true">
    <span class="h-1.5 w-1.5 rounded-full bg-[var(--orange)] animate-pulse"></span>
    <span id="swarmProgress">Montando a página com agentes…</span>
  </span>
  <span id="swarmStatus" role="status" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap"></span>
  <button type="button" id="swarmPause" class="px-2.5 py-1 rounded-full bg-[var(--surface-2)] border border-[var(--border)] font-semibold text-[var(--muted)] hover:text-white hover:border-[var(--orange)] transition cursor-pointer">Pausar</button>
  <button type="button" id="swarmSkip" class="px-2.5 py-1 rounded-full bg-[var(--surface-2)] border border-[var(--border)] font-semibold text-[var(--muted)] hover:text-white hover:border-[var(--orange)] transition cursor-pointer">Pular animação</button>
  <button type="button" id="swarmReplay" class="px-2.5 py-1 rounded-full bg-[var(--surface-2)] border border-[var(--border)] font-semibold text-[var(--muted)] hover:text-white hover:border-[var(--orange)] transition cursor-pointer" hidden>Repetir animação</button>
</div>"""

# ------------------------------------------------------ inicializador (clássico)
INIT_SCRIPT = """  <!-- Mouse Swarm Reveal — enxame de cursores montando a Hero Section.
       Script clássico (roda durante a análise do HTML) com import dinâmico do módulo.
       Nenhum conteúdo é escondido por CSS: se algo falhar, a página segue normal. -->
  <script>
    (function () {
      const track = (payload) => {
        try { window.dataLayer = window.dataLayer || []; window.dataLayer.push(Object.assign({ event: 'swarm_reveal' }, payload)); } catch (e) {}
      };
      const elControls = document.getElementById('swarmControls');
      const elProgress = document.getElementById('swarmProgress');
      const elAnnounce = document.getElementById('swarmStatus');
      const btnPause = document.getElementById('swarmPause');
      const btnSkip = document.getElementById('swarmSkip');
      const btnReplay = document.getElementById('swarmReplay');
      // Demonstração/depuração: ?swarm=1 (ou #swarm) mantém os controles após a montagem.
      // A preferência de movimento reduzido NÃO desativa a animação: o visitante
      // solicitou explicitamente uma Hero montada por cursores ao abrir a página.
      const force = location.search.indexOf('swarm=1') !== -1 || location.hash === '#swarm';

      const setPhase = (phase) => {
        if (!elControls) return;
        elControls.hidden = phase === 'done' && !force;
        if (btnPause) { btnPause.hidden = phase === 'done'; btnPause.textContent = phase === 'paused' ? 'Retomar' : 'Pausar'; }
        if (btnSkip) btnSkip.hidden = phase === 'done';
        if (btnReplay) btnReplay.hidden = phase !== 'done' || !force;
      };

      (async () => {
        try {
          const { createSwarmReveal } = await import('/static/js/mouse-swarm-v3.js');
          const narrow = window.matchMedia('(max-width: 767px)').matches;
          const reveal = createSwarmReveal({
            root: document,
            selector: '[data-swarm-item]',
            cursors: narrow ? 10 : 16,
            interval: narrow ? 220 : 240,
            colors: ['#ff4d00', '#ff9a5c', '#70c9f9', '#c9acff', '#8ee6ce'],
            botEvery: 4,
            cursorSize: 16,
            cursorSpeed: 620,
            labels: [],
            selection: true,
            typeText: false,
            autoScroll: false,
            forceMotion: true,
            onStep: ({ current, total }) => {
              if (elProgress) elProgress.textContent = 'Montando a página com agentes… ' + current + '/' + total;
            },
            onComplete: ({ reason, total }) => {
              const msg = reason === 'skipped' ? 'Montagem pulada — página liberada.'
                : reason === 'reduced-motion' ? 'Página pronta (movimento reduzido).'
                : 'Página montada pelos agentes.';
              if (elProgress) elProgress.textContent = msg;
              if (elAnnounce) elAnnounce.textContent = msg;
              setPhase('done');
              track({ swarm_action: reason, swarm_items: total });
            },
            onError: (error) => {
              console.warn('[mouse-swarm] animação interrompida:', error);
              setPhase('done');
            }
          });

          if (btnPause) btnPause.addEventListener('click', () => {
            const status = reveal.getState().status;
            if (status === 'running') { reveal.pause(); setPhase('paused'); }
            else if (status === 'paused') { reveal.resume(); setPhase('running'); }
          });
          if (btnSkip) btnSkip.addEventListener('click', () => reveal.skip());
          if (btnReplay) btnReplay.addEventListener('click', () => {
            setPhase('running');
            if (elProgress) elProgress.textContent = 'Montando a página com agentes…';
            track({ swarm_action: 'replay' });
            reveal.replay();
          });

          setPhase('running');
          reveal.start();
          track({ swarm_action: 'start', swarm_items: reveal.getState().total });
          window.__mouseSwarm = reveal;  // handle de inspeção (progresso/estado)
        } catch (error) {
          console.warn('[mouse-swarm] animação indisponível:', error);
          if (elControls) elControls.hidden = true;
        }
      })();
    })();
  </script>
"""


def read_source():
    """Le index.html normalizando CRLF->LF (o arquivo original usa CRLF)."""
    raw = open(INDEX, "rb").read()
    return raw.decode("utf-8").replace("\r\n", "\n"), (b"\r\n" in raw)


def write_source(text, crlf):
    data = text.replace("\n", "\r\n") if crlf else text
    with open(INDEX, "wb") as handle:
        handle.write(data.encode("utf-8"))


def replace_once(html, old, new, label):
    count = html.count(old)
    if count != 1:
        raise SystemExit("ERRO: âncora '%s' encontrada %d vez(es) (esperado 1)" % (label, count))
    return html.replace(old, new, 1)


def mark_tag(html, tag, attrs):
    """Insere os atributos do enxame logo após o fechamento do atributo class."""
    if re.search(r'data-swarm-item[ >]', tag):
        return html
    new = tag[:-1] + " " + attrs + ">"
    if new in html:
        return html
    return replace_once(html, tag, new, tag[:70])


def mark_card(html, inner_marker, attrs):
    """Marca a tag do card de métrica que antecede o texto interno exclusivo."""
    marker_at = html.find(">" + inner_marker)
    if marker_at == -1:
        raise SystemExit("ERRO: texto do card '%s' não encontrado" % inner_marker)
    marked_tag = CARD_TAG[:-1] + " " + attrs + ">"
    if marked_tag in html:
        return html  # este card já está marcado (os atributos são exclusivos de cada card)
    start = html.rfind(CARD_TAG, 0, marker_at)
    if start == -1:
        raise SystemExit("ERRO: tag do card anterior a '%s' não encontrada" % inner_marker)
    end = start + len(CARD_TAG)
    if CARD_TAG in html[end:marker_at]:
        raise SystemExit("ERRO: ambiguidade ao marcar o card '%s'" % inner_marker)
    return html[:start] + marked_tag + html[end:]


class SwarmItemCounter(HTMLParser):
    """Conta os elementos que realmente carregam o atributo data-swarm-item."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self.controls_hidden = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "data-swarm-item" in data:
            self.items.append({
                "tag": tag,
                "order": data.get("data-swarm-order"),
                "role": data.get("data-swarm-role"),
                "group": data.get("data-swarm-group"),
                "effect": data.get("data-swarm-effect"),
            })
        if data.get("id") == "swarmControls":
            self.controls_hidden = "hidden" in data


def verify(html):
    parser = SwarmItemCounter()
    parser.feed(html)
    items = parser.items
    print("elementos com data-swarm-item: %d" % len(items))
    for item in items:
        print("   <%-4s> ordem=%-4s role=%-7s grupo=%-6s efeito=%s" % (
            item["tag"], item["order"], item["role"] or "-", item["group"] or "-", item["effect"] or "-"))
    assert len(items) == 10, "esperado 10 alvos, encontrados %d" % len(items)
    assert sorted(int(i["order"]) for i in items) == list(range(1, 11)), "ordens 1..10"
    assert [i["group"] for i in items].count("proof") == 2, "grupo proof com 2 itens"
    assert [i["group"] for i in items].count("stats") == 3, "grupo stats com 3 itens"

    # REGRA CRÍTICA: nada pode esconder a Hero por CSS (foi isso que "quebrou" a página)
    assert "ms-boot" not in html, "sobrou mecanismo que esconde a Hero antes da animação"
    assert "[data-swarm-item] { opacity" not in html, "CSS não pode esconder os alvos"
    assert "opacity: 0" not in HEAD_CSS, "CSS dos controles não pode esconder conteúdo"
    assert parser.controls_hidden is True, "os controles devem nascer ocultos"
    css_at = html.find("#swarmControls {")
    assert css_at != -1 and css_at < html.find("</head>"), "CSS dos controles deve ficar no <head>"
    assert 'rel="modulepreload" href="/static/js/mouse-swarm-v3.js"' in html, "faltou o modulepreload do asset com URL nova"
    assert "forceMotion: true" in html, "a Hero não pode sofrer skip pelo prefers-reduced-motion"
    assert "swarm=1" in html, "faltou o opt-in ?swarm=1"
    assert '<script type="module">' not in html, "inicializador deve ser script clássico"
    assert "createSwarmReveal" in html and "mouse-swarm-v3.js" in html
    for leak in ("text-balance data-swarm-item", "mb-3 data-swarm-item", "text-[11px] data-swarm-item"):
        assert leak not in html, "atributos injetados dentro de class: %s" % leak
    for name in ("swarmControls", "swarmPause", "swarmSkip", "swarmReplay", "swarmProgress", "swarmStatus"):
        assert 'id="%s"' % name in html, "faltou #%s" % name
    print("verificação OK: 10 alvos, grupos, nada esconde a Hero, controles ocultos, módulo presente")


def main():
    html, crlf = read_source()
    original = html

    # 1) controles no fim da coluna esquerda da Hero
    #    (antes de marcar alvos, pois a âncora é o container da coluna do vídeo)
    if 'id="swarmControls"' not in html:
        anchor = TARGETS[2][0]
        html = replace_once(html, anchor, CONTROLS + anchor, "controles")
        print("controles injetados")

    # 2) atributos do enxame nos elementos da primeira dobra
    for tag, attrs in TARGETS:
        html = mark_tag(html, tag, attrs)
    for marker, attrs in CARD_TARGETS:
        html = mark_card(html, marker, attrs)
    print("alvos marcados")

    # 3) CSS dos controles dentro do <style> do <head> + modulepreload antes de </head>
    if "#swarmControls {" not in html:
        html = replace_once(html, "  </style>\n</head>", HEAD_CSS + "  </style>\n</head>", "css head")
        print("css dos controles injetado")
    if "modulepreload" not in html:
        html = replace_once(html, "</head>", HEAD_LINK + "</head>", "modulepreload")
        print("modulepreload injetado")
    elif HEAD_LINK not in html:
        html, n = re.subn(
            r'  <!-- Mouse Swarm Reveal:[^>]*-->\s*<link rel="modulepreload" href="/static/js/mouse-swarm[^"]*">\s*',
            HEAD_LINK,
            html,
            count=1,
        )
        if n != 1:
            raise SystemExit("ERRO: falha ao atualizar modulepreload existente")
        print("modulepreload atualizado")

    # 4) inicializador
    if "createSwarmReveal" not in html:
        html = replace_once(html, "</body>", INIT_SCRIPT + "</body>", "script init")
        print("inicializador injetado")
    elif INIT_SCRIPT not in html:
        html, n = re.subn(
            r'  <!-- Mouse Swarm Reveal — enxame de cursores[\s\S]*?</script>\s*(?=</body>)',
            INIT_SCRIPT,
            html,
            count=1,
        )
        if n != 1:
            raise SystemExit("ERRO: falha ao atualizar inicializador existente")
        print("inicializador atualizado")

    verify(html)

    if html == original:
        print("index.html já estava integrado — nada a fazer.")
        return

    write_source(html, crlf)
    print("OK: index.html gravado (%d bytes)" % len(html.encode("utf-8")))


if __name__ == "__main__":
    main()
