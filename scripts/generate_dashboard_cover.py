"""Gera capa 1200x912 no padrão Cyber-Classicism para o artigo Hermes Web Dashboard.

Base gerada pelo OmniRoute (/v1/images/generations, modelo antigravity/gemini-3.1-flash-image)
+ overlay editorial de título em Pillow.
"""

import base64
import io
import json
import os
import subprocess
import urllib.request

from PIL import Image, ImageDraw, ImageFont

API_URL = "https://omi.jepierre.com.br/v1/images/generations"
MODEL = "antigravity/gemini-3.1-flash-image"
OUT_PATH = r"D:\DevCod\inteligencia-agentica\static\images\hermes-web-dashboard-central-comando-agentes-ia.jpg"

ESTILO_BASE = (
    "High-end editorial dark cyber-classicism artwork for a technology blog cover, "
    "no text, no letters, no words. Deep obsidian black background (#07070A), "
    "electric neon cyan (#00E5FF) and luminous amber-gold (#DFBA6B) rim lighting, "
    "majestic classical Greco-Roman white marble sculpture, fine sculpted marble texture, "
    "dramatic chiaroscuro studio lighting, subtle holographic depth, "
    "minimalist luxury tech editorial aesthetic, photorealistic 8k render. "
)

PROMPT = ESTILO_BASE + (
    "A classical marble bust of Hermes with winged helmet at the center of an obsidian command sanctuary, "
    "surrounded by floating translucent holographic browser dashboard panels, glowing telemetry arcs, "
    "geometric MCP protocol node graphs, and golden security lock seals connected by cyan and gold "
    "fiber-optic conduits."
)

CFG = {
    "kicker": "INTELIGÊNCIA AGÊNTICA  •  PAINEL DE CONTROLE",
    "title1": "Hermes Web Dashboard:",
    "title2": "Central Visual de Agentes",
    "subtitle": "Gerencie perfis, chaves, MCPs e canais sem depender do terminal",
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
        d.line([(0, y), (w, y)], fill=(7, 7, 10, int(235 * (t ** 1.2))))

    bar_x, y1, y2 = 64, 615, 845
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        d.line(
            [(bar_x, y), (bar_x + 7, y)],
            fill=(int(223 * t), int(229 - 43 * t), int(255 - 148 * t), 255),
        )

    d.text((92, 615), cfg["kicker"], fill=(0, 229, 255, 255), font=get_font(22))
    d.text((92, 655), cfg["title1"], fill=(255, 255, 255, 255), font=get_font(56))
    d.text((92, 722), cfg["title2"], fill=(223, 186, 107, 255), font=get_font(56))
    d.text((92, 804), cfg["subtitle"], fill=(215, 225, 235, 235), font=get_font(26, bold=False))

    final = Image.alpha_composite(im, layer).convert("RGB")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final.save(out_path, format="JPEG", quality=94)
    print(f"OK: {out_path} ({final.size[0]}x{final.size[1]})")


def main():
    api_key = os.environ.get("OMI_API_KEY", "")
    if not api_key:
        raise SystemExit("Defina OMI_API_KEY no ambiente")
    print(f"Gerando base via {MODEL}...", flush=True)
    img_bytes = generate_base(PROMPT, api_key)
    build_cover(img_bytes, CFG, OUT_PATH)


if __name__ == "__main__":
    main()
