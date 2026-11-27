"""Gera capas 1200x912 no padrão Cyber-Classicism aprovado para o blog.

Padrão: base gerada pelo OmniRoute (/v1/images/generations, modelo
antigravity/gemini-3.1-flash-image) + overlay editorial de título em Pillow.

Uso:
  OMI_API_KEY=<chave> uv run --with pillow python generate_cover_omniroute.py <slug> [<slug> ...]

Slugs disponíveis: hermes-codex | 7-tendencias | hype-cycle
"""

import base64
import io
import json
import os
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

API_URL = "https://omi.jepierre.com.br/v1/images/generations"
MODEL = "antigravity/gemini-3.1-flash-image"
STATIC_DIR = r"D:\DevCod\inteligencia-agentica\static\images"
SHARED_DIR = r"C:\Users\Jean\OpenBot\Shared"

ESTILO_BASE = (
    "High-end editorial dark cyber-classicism artwork for a technology blog cover, "
    "no text, no letters, no words. Deep obsidian black background (#07070A), "
    "electric neon cyan (#00E5FF) and luminous amber-gold (#DFBA6B) rim lighting, "
    "majestic classical Greco-Roman white marble sculpture, fine sculpted marble texture, "
    "dramatic chiaroscuro studio lighting, subtle holographic depth, "
    "minimalist luxury tech editorial aesthetic, photorealistic 8k render. "
)

TARGETS = {
    "hermes-codex": {
        "file": "hermes-agent-vs-codex-orquestracao-codigo.jpg",
        "prompt": ESTILO_BASE + (
            "A classical marble bust of Hermes with winged helmet on the left, linked by glowing "
            "fiber-optic neural conduits to a sleek obsidian-and-gold crystalline code monolith on the right."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  HERMES + CODEX",
        "title1": "Hermes Agent vs. Codex:",
        "title2": "Orquestre Sem Perder Controle",
        "subtitle": "Memória persistente, 20+ chats e zero telemetria acima da Codex CLI",
    },
    "7-tendencias": {
        "file": "7-tendencias-ia-agentica-2026-producao-empresas.jpg",
        "prompt": ESTILO_BASE + (
            "One central marble bust of Hermes illuminated in cyan, surrounded by seven smaller "
            "floating marble busts in an orbital ring, all linked by golden geometric protocol "
            "conduits to a luminous holographic network grid."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  TENDÊNCIAS 2026",
        "title1": "7 Tendências de IA Agêntica",
        "title2": "Que Vão Definir 2026",
        "subtitle": "Multi-agente, MCP/A2A, FinOps e governança em produção",
    },
    "hype-cycle": {
        "file": "hype-cycle-gartner-2026-ia-agentica-empresas.jpg",
        "prompt": ESTILO_BASE + (
            "A marble bust of Hermes ascending a sweeping arc of glowing light toward a brilliant "
            "cyan-and-gold apex, flanked by layered classical columns and a translucent golden "
            "scale of balance."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  GARTNER 2026",
        "title1": "Hype Cycle de IA Agêntica",
        "title2": "Separando Hype de Adoção Real",
        "subtitle": "17% em produção, +60% planejando adotar em 2 anos",
    },
    "faq-30": {
        "file": "guia-completo-faq-hermes-agent-funcionarios-digitais.jpg",
        "prompt": ESTILO_BASE + (
            "A majestic classical marble bust of Hermes with winged helmet at the center, "
            "surrounded by four floating luminous holographic stone tablets representing "
            "knowledge and architecture, connected by fine cyan and gold neural filaments "
            "in a grand obsidian sanctuary."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  GUIA DEFINITIVO",
        "title1": "Guia do Hermes Agent:",
        "title2": "30 Respostas Essenciais",
        "subtitle": "Arquitetura, memória, modelos econômicos e operação 24/7",
    },
    "loops-heartbeat": {
        "file": "autonomia-proativa-loops-recorrentes-heartbeats-hermes.jpg",
        "prompt": ESTILO_BASE + (
            "A classical marble bust of Hermes in profile, illuminated in cyan on the left "
            "and gold on the right, surrounded by concentric luminous orbital rings and a "
            "glowing golden pulse wave representing continuous autonomous heartbeat and self-paced loops."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  AUTONOMIA 24/7",
        "title1": "Autonomia Proativa:",
        "title2": "/loop e /heartbeat no Hermes",
        "subtitle": "Vigilância contínua sem intervenção humana e com cache preservado",
    },
    "script-cron": {
        "file": "script-only-cron-jobs-hermes-send-custo-zero.jpg",
        "prompt": ESTILO_BASE + (
            "A classical marble bust of Hermes wearing a winged helmet, standing sentinel "
            "before a glowing golden astronomical clockwork astrolabe and cyan fiber-optic "
            "telemetry conduits, symbolizing zero-cost deterministic watchdogs."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  CUSTO ZERO",
        "title1": "Script-Only Cron Jobs:",
        "title2": "Watchdogs com hermes send",
        "subtitle": "Alertas de infraestrutura 24/7 no Telegram e WhatsApp sem gastar tokens",
    },
    "code-execution": {
        "file": "code-execution-chamada-programatica-hermes.jpg",
        "prompt": ESTILO_BASE + (
            "A classical marble bust of Hermes channeling a concentrated beam of cyan and "
            "golden light into a translucent crystalline Python execution core, compressing "
            "dozens of glowing holographic data threads into a single luminous stream."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  PERFORMANCE",
        "title1": "Code Execution no Hermes:",
        "title2": "50 Passos em 1 Único Turno",
        "subtitle": "Chamada programática via RPC com até 95% menos tokens",
    },
    "git-worktrees": {
        "file": "git-worktrees-paralelismo-multi-agente-hermes.jpg",
        "prompt": ESTILO_BASE + (
            "A central classical marble bust of Hermes connected by branching golden and cyan "
            "fiber-optic roots to three parallel glowing crystalline obelisks, representing "
            "isolated Git worktree branches operating without collision."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  MULTI-AGENTE",
        "title1": "Git Worktrees no Hermes:",
        "title2": "Paralelismo Sem Conflitos",
        "subtitle": "Árvores isoladas para subagentes e limpeza automática na VPS",
    },
    "managed-scope": {
        "file": "managed-scope-remote-config-governanca-hermes-v2.jpg",
        "prompt": ESTILO_BASE + (
            "A classical marble bust of Hermes wearing a winged helmet at the apex of a dark "
            "obsidian command hall, flanked by three glowing translucent golden and cyan "
            "architectural seals and classical marble pillars linked by centralized holographic "
            "governance conduits, symbolizing fleet-wide policy locks and standardized agent deployment."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  GOVERNANÇA",
        "title1": "Managed Scope & Remote Config:",
        "title2": "Padronize Agentes na Empresa",
        "subtitle": "Trave políticas, distribua perfis via Git e controle frotas 24/7",
    },
    "moa": {
        "file": "mixture-of-agents-moa-conselho-modelos-hermes-v2.jpg",
        "prompt": ESTILO_BASE + (
            "A council of three classical Greco-Roman white marble busts arranged in a dark obsidian "
            "sanctuary: two luminous advisor busts on the left and right bathed in electric cyan (#00E5FF) "
            "rim light projecting neural light filaments into a central golden (#DFBA6B) Hermes bust "
            "with a winged helmet and a glowing crystalline decision prism above, symbolizing Mixture of Agents."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  MIXTURE OF AGENTS",
        "title1": "Mixture of Agents (MoA):",
        "title2": "Conselho de IAs no Hermes",
        "subtitle": "Múltiplas perspectivas, +6 pontos no HermesBench e cache intacto",
    },
    "subscription-proxy": {
        "file": "subscription-proxy-tool-gateway-uma-assinatura-hermes-agent.jpg",
        "prompt": ESTILO_BASE + (
            "A classical Greco-Roman white marble bust of Hermes with winged helmet at the center of a "
            "dark obsidian temple, holding a luminous cyan-and-gold crystalline portal ring that unifies "
            "five glowing holographic fiber-optic conduits (web search, acoustic voice wave, image prism, "
            "cloud browser window, and local API gateway), symbolizing one unified subscription."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  CONSOLIDAÇÃO DE CUSTOS",
        "title1": "Subscription Proxy & Gateway:",
        "title2": "1 Assinatura, Todas as Ferramentas",
        "subtitle": "Unifique LLMs, busca web, voz, imagens e navegador sem espalhar chaves",
    },
    "tool-search": {
        "file": "tool-search-tiered-disclosure-mcp-hermes-agent.jpg",
        "prompt": ESTILO_BASE + (
            "A classical Greco-Roman white marble bust of Hermes with winged helmet at the center of a "
            "dark obsidian archive, holding a glowing golden magnifying prism that illuminates three "
            "floating crystalline MCP tool tablets out of hundreds of dim holographic tool cards arranged "
            "in tiered orbital rings, connected by electric cyan (#00E5FF) search filaments."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  ESCALA & EFICIÊNCIA",
        "title1": "Tool Search & Tiered Disclosure:",
        "title2": "3.000 Ferramentas Sem Estourar Tokens",
        "subtitle": "Carregamento sob demanda, BM25 e Connectors sem poluir o contexto",
    },
    "import-agents": {
        "file": "import-from-other-agents-migracao-claude-code-cursor-codex-openclaw-hermes.jpg",
        "prompt": ESTILO_BASE + (
            "A majestic classical Greco-Roman white marble bust of Hermes with winged helmet at the center "
            "of a dark obsidian sanctuary, receiving six glowing electric cyan (#00E5FF) and luminous gold (#DFBA6B) "
            "fiber-optic data bridges converging from six floating crystalline stone tablets into a unified "
            "holographic memory and protocol core, symbolizing seamless multi-agent migration."
        ),
        "kicker": "INTELIGÊNCIA AGÊNTICA  •  MIGRAÇÃO SEM ATRITO",
        "title1": "Import from Other Agents:",
        "title2": "Migre Tudo em 1 Comando",
        "subtitle": "Claude Code, Cursor, Codex, OpenClaw, Grok Bot e OpenBot no Hermes",
    },
}


def get_font(size, bold=True):
    paths = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_base(prompt, api_key):
    payload = json.dumps(
        {"model": MODEL, "prompt": prompt, "n": 1, "size": "1024x1024"}
    ).encode("utf-8")
    cmd = [
        "curl", "-sS", "-w", "\nHTTP:%{http_code}", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-H", "User-Agent: Mozilla/5.0",
        "--data-binary", "@-",
    ]
    res = subprocess.run(cmd, input=payload, capture_output=True, timeout=180)
    out = res.stdout.decode("utf-8", errors="replace")
    if "\nHTTP:" not in out:
        raise RuntimeError(f"Sem resposta HTTP: {out[:300]}")
    body, code = out.rsplit("\nHTTP:", 1)
    if code.strip() != "200":
        raise RuntimeError(f"HTTP {code.strip()}: {body[:300]}")
    data = json.loads(body)
    item = data["data"][0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    raise RuntimeError("Resposta sem imagem")


def build_cover(img_bytes, cfg, out_path):
    im = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = 1200, 912
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((int(sw * scale), int(sh * scale)), Image.Resampling.LANCZOS)
    nw, nh = im.size
    im = im.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))

    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    for y in range(int(h * 0.48), h):
        t = (y - int(h * 0.48)) / (h - int(h * 0.48))
        d.line([(0, y), (w, y)], fill=(7, 7, 10, int(230 * (t ** 1.25))))

    bar_x, y1, y2 = 64, 615, 845
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        d.line([(bar_x, y), (bar_x + 7, y)],
               fill=(int(223 * t), int(229 - 43 * t), int(255 - 148 * t), 255))

    d.text((92, 615), cfg["kicker"], fill=(0, 229, 255, 255), font=get_font(22))
    d.text((92, 655), cfg["title1"], fill=(255, 255, 255, 255), font=get_font(56))
    d.text((92, 722), cfg["title2"], fill=(223, 186, 107, 255), font=get_font(56))
    d.text((92, 804), cfg["subtitle"], fill=(215, 225, 235, 235), font=get_font(26, bold=False))

    final = Image.alpha_composite(im, layer).convert("RGB")
    final.save(out_path, format="JPEG", quality=94)
    return final


def main():
    api_key = os.environ.get("OMI_API_KEY", "")
    if not api_key:
        raise SystemExit("Defina OMI_API_KEY no ambiente")

    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(SHARED_DIR, exist_ok=True)
    names = sys.argv[1:] or ["7-tendencias", "hype-cycle"]

    for name in names:
        cfg = TARGETS[name]
        print(f"Gerando base: {name} ({MODEL})", flush=True)
        img_bytes = generate_base(cfg["prompt"], api_key)
        path = os.path.join(STATIC_DIR, cfg["file"])
        build_cover(img_bytes, cfg, path)
        shared = os.path.join(SHARED_DIR, cfg["file"])
        Image.open(path).convert("RGB").save(shared, format="JPEG", quality=94)
        print(f"OK: {path}", flush=True)


if __name__ == "__main__":
    main()
