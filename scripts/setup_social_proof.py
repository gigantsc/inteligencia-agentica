#!/usr/bin/env python3
"""Instala o banco de prova social (mensagens de venda aleatorias) no index.html.

Geracao deterministica das mensagens + injecao idempotente do bloco do toast.
Rode: python scripts/setup_social_proof.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "index.html"

MARKER = "SOCIAL PROOF V2"

NAMES = [
    "Marcos", "Rafaela", "Diego", "Juliana", "Patrícia", "Anderson", "Camila", "Rodrigo",
    "Fernanda", "Leandro", "Bruna", "Thiago", "Vanessa", "Everton", "Aline", "Gustavo",
    "Joice", "Marcelo", "Tatiane", "Fábio", "Priscila", "Sandro", "Cristiane", "Wagner",
    "Débora", "Adilson", "Simone", "Rogério", "Michele", "Cléber", "Larissa", "Vitor",
    "Eliane", "Jonas", "Késsia", "Rafael", "Sabrina", "Gilberto", "Mônica", "Tiago",
    "Andréia", "Felipe", "Carolina", "Renato",
]

CITIES = [
    "Brusque", "Blumenau", "Joinville", "Itajaí", "Florianópolis", "Balneário Camboriú",
    "Jaraguá do Sul", "Chapecó", "São José", "Palhoça", "Curitiba", "Maringá",
    "Londrina", "São Paulo", "Campinas", "Santos", "Rio de Janeiro", "Niterói",
    "Belo Horizonte", "Uberlândia", "Goiânia", "Brasília", "Salvador", "Recife",
    "Fortaleza", "Natal", "Porto Alegre", "Caxias do Sul", "Vitória", "Belém",
    "Manaus", "Campo Grande",
]

ACTIONS = [
    "comprou o curso Inteligência Agêntica",
    "adquiriu o curso Inteligência Agêntica",
    "garantiu o 2º lote do plano anual",
    "travou o preço de R$497/ano",
    "entrou na Comunidade Agêntica",
    "assinou o plano anual",
    "comprou o plano anual",
    "garantiu o acesso aos 7 agentes",
    "liberou o acesso imediato",
    "pegou o 2º lote",
    "comprou o acesso vitalício",
    "garantiu a vaga no 2º lote",
    "adquiriu o plano anual",
    "ativou os funcionários de IA",
]

TOTAL = 120


def build_proofs():
    proofs = []
    seen = set()
    i = 0
    while len(proofs) < TOTAL:
        name = NAMES[i % len(NAMES)]
        city = CITIES[(i * 5 + 3) % len(CITIES)]
        action = ACTIONS[(i * 3 + 1) % len(ACTIONS)]
        key = (name, city, action)
        if key not in seen:
            seen.add(key)
            proofs.append({
                "name": "%s de %s" % (name, city),
                "action": action,
                "min": 1 + (i % 11),
            })
        i += 1
    return proofs


BLOCK_TEMPLATE = """    // 6. Social Proof Toast Cycler — {marker}: mensagens de venda em ordem aleatoria
    (() => {{
      const toast = document.getElementById('socialProofToast');
      const toastInitial = document.getElementById('toastInitial');
      const toastName = document.getElementById('toastName');
      const toastAction = document.getElementById('toastAction');
      if (!toast || !toastName) return;

      const proofs = {proofs};

      let queue = [];
      let lastIndex = -1;
      const shuffled = (n) => {{
        const a = Array.from({{ length: n }}, (_, i) => i);
        for (let i = n - 1; i > 0; i--) {{
          const j = Math.floor(Math.random() * (i + 1));
          const t = a[i]; a[i] = a[j]; a[j] = t;
        }}
        return a;
      }};
      // Sorteio em "saco": percorre todas as mensagens antes de repetir e nunca
      // repete a mesma logo em seguida — ordem diferente a cada visita.
      const pickNext = () => {{
        if (!queue.length) {{
          queue = shuffled(proofs.length);
          if (queue.length > 1 && queue[0] === lastIndex) {{
            const t = queue[0]; queue[0] = queue[1]; queue[1] = t;
          }}
        }}
        lastIndex = queue.shift();
        return proofs[lastIndex];
      }};
      const when = (min) => (min <= 0 ? 'agora mesmo' : (min === 1 ? 'há 1 min' : 'há ' + min + ' min'));
      const render = (item) => {{
        if (toastInitial) toastInitial.textContent = item.name.charAt(0);
        if (toastName) toastName.textContent = item.name;
        if (toastAction) toastAction.textContent = item.action + ' ' + when(item.min);
      }};
      const show = () => {{
        toast.classList.remove('opacity-0', 'translate-y-3');
        toast.classList.add('opacity-100', 'translate-y-0');
      }};
      const hide = () => {{
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-3');
      }};

      // Exposto para inspecao/teste em sessao de navegador.
      window.__socialProof = {{ proofs: proofs, next: pickNext, render: render }};

      // Aparece depois de 4 s (para nao colidir com a Hero) e troca em intervalos variaveis.
      setTimeout(() => {{
        render(pickNext());
        show();
        const step = () => {{
          hide();
          setTimeout(() => {{
            const item = pickNext();
            render({{ name: item.name, action: item.action, min: item.min + Math.floor(Math.random() * 3) }});
            show();
            setTimeout(step, 4200 + Math.floor(Math.random() * 2600));
          }}, 420);
        }};
        setTimeout(step, 4500 + Math.floor(Math.random() * 2000));
      }}, 4000);
    }})();
"""

START = "    // 6. Social Proof Toast Cycler"
END = "    // 7. DataLayer Event Tracking"


def main():
    html = HTML_PATH.read_text(encoding="utf-8")
    proofs = build_proofs()

    if MARKER in html:
        print("bloco de prova social já instalado — nada a fazer.")
        return 0

    start = html.find(START)
    end = html.find(END)
    if start == -1 or end == -1 or end <= start:
        print("ERRO: âncoras do bloco do toast não encontradas (arquivo mudou?)")
        return 1

    new_block = BLOCK_TEMPLATE.format(
        marker=MARKER,
        proofs=json.dumps(proofs, ensure_ascii=False, indent=8).replace("\n}", "\n      }"),
    )
    html = html[:start] + new_block + "\n" + html[end:]

    # ---------------- verificações antes de gravar ----------------
    assert MARKER in html, "marcador ausente"
    names = {p["name"] for p in proofs}
    combos = {(p["name"], p["action"]) for p in proofs}
    assert len(proofs) == TOTAL, "esperado %d mensagens, obtido %d" % (TOTAL, len(proofs))
    assert len(combos) == TOTAL, "mensagens repetidas: %d únicas de %d" % (len(combos), TOTAL)
    assert len(names) >= 60, "pouca variedade de nomes/cidades: %d" % len(names)
    sales_verbs = ("comprou", "adquiriu", "garantiu", "travou", "assinou", "pegou", "liberou", "ativou", "entrou")
    for p in proofs:
        assert any(v in p["action"] for v in sales_verbs), "ação sem sentido de venda: %s" % p["action"]
    assert "pickNext" in html and "shuffled" in html, "sorteador ausente"
    used_actions = {p["action"] for p in proofs}
    assert len(used_actions) == len(ACTIONS), (
        "só %d de %d ações foram usadas (multiplicador e módulo não são coprimos): %s"
        % (len(used_actions), len(ACTIONS), sorted(used_actions))
    )

    HTML_PATH.write_text(html, encoding="utf-8")
    print("mensagens instaladas: %d (nomes/cidades distintos: %d)" % (len(proofs), len(names)))
    print("exemplos:", " | ".join(p["name"] + " — " + p["action"] for p in proofs[:3]))
    print("OK: index.html gravado (%d bytes)" % len(html.encode("utf-8")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
