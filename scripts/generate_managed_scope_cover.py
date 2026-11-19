"""Gera capa 1200x912px em estilo Hermes Cyber-Classicism via Pillow para:
managed-scope-remote-config-governanca-hermes.jpg
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_PATH = r"D:\DevCod\inteligencia-agentica\static\images\managed-scope-remote-config-governanca-hermes.jpg"
W, H = 1200, 912
BG = (7, 7, 10)
CYAN = (0, 229, 255)
GOLD = (223, 186, 107)


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


def add_radial_glow(canvas, cx, cy, radius, color, peak_alpha):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    steps = 36
    for i in range(steps, 0, -1):
        r = int(radius * (i / steps))
        a = int(peak_alpha * ((1 - i / steps) ** 1.7))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(color[0], color[1], color[2], a))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(canvas, glow)


def draw_column(d, x, top_y, bot_y, width, tint_color):
    # Classical fluted marble column
    d.rectangle([x - width // 2, top_y, x + width // 2, bot_y], fill=(24, 26, 34, 210))
    # Capital & base
    d.rectangle([x - width // 2 - 10, top_y - 14, x + width // 2 + 10, top_y + 4], fill=(42, 46, 58, 230))
    d.rectangle([x - width // 2 - 12, bot_y - 4, x + width // 2 + 12, bot_y + 14], fill=(38, 42, 54, 230))
    # Flutes
    for fx in range(x - width // 2 + 8, x + width // 2 - 4, 12):
        d.line([(fx, top_y + 8), (fx, bot_y - 8)], fill=(12, 14, 20, 180), width=3)
        d.line([(fx + 3, top_y + 8), (fx + 3, bot_y - 8)], fill=(tint_color[0], tint_color[1], tint_color[2], 40), width=1)


def draw_seal(d, cx, cy, r, color, label_symbol):
    # Outer holographic ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(color[0], color[1], color[2], 220), width=3)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], outline=(color[0], color[1], color[2], 120), width=1)
    d.ellipse([cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18], fill=(14, 18, 26, 210))
    # Geometric lock / node emblem inside
    if label_symbol == "lock":
        d.rounded_rectangle([cx - 16, cy - 4, cx + 16, cy + 20], radius=4, outline=color + (240,), width=3)
        d.arc([cx - 11, cy - 20, cx + 11, cy + 2], start=180, end=360, fill=color + (240,), width=3)
    elif label_symbol == "git":
        d.line([(cx - 14, cy + 14), (cx - 14, cy - 14)], fill=color + (240,), width=3)
        d.line([(cx - 14, cy + 4), (cx + 12, cy - 10)], fill=color + (240,), width=3)
        for px, py in [(cx - 14, cy - 14), (cx - 14, cy + 14), (cx + 12, cy - 10)]:
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=color + (255,))
    elif label_symbol == "plane":
        pts = [(cx, cy - 18), (cx + 18, cy), (cx, cy + 18), (cx - 18, cy)]
        d.polygon(pts, outline=color + (240,))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color + (255,))


def draw_hermes_bust(d, cx, cy):
    # Stylized classical marble bust with winged helmet and split lighting
    # Pedestal
    d.polygon([(cx - 72, cy + 150), (cx + 72, cy + 150), (cx + 52, cy + 110), (cx - 52, cy + 110)], fill=(36, 40, 50, 240))
    # Shoulders / torso
    d.polygon([(cx - 95, cy + 112), (cx + 95, cy + 112), (cx + 68, cy + 36), (cx + 26, cy + 16), (cx - 26, cy + 16), (cx - 68, cy + 36)], fill=(180, 186, 198, 245))
    # Neck
    d.rectangle([cx - 22, cy - 12, cx + 22, cy + 22], fill=(168, 174, 186, 245))
    # Head / classical profile silhouette
    d.ellipse([cx - 42, cy - 96, cx + 42, cy + 4], fill=(210, 214, 222, 250))
    # Helmet dome
    d.pieslice([cx - 46, cy - 112, cx + 46, cy - 30], start=180, end=360, fill=(192, 198, 210, 250))
    # Winged helmet accents (left cyan, right gold)
    d.polygon([(cx - 44, cy - 74), (cx - 88, cy - 118), (cx - 66, cy - 82), (cx - 40, cy - 60)], fill=CYAN + (230,))
    d.polygon([(cx + 44, cy - 74), (cx + 88, cy - 118), (cx + 66, cy - 82), (cx + 40, cy - 60)], fill=GOLD + (230,))
    # Split-lighting rim on bust
    d.arc([cx - 43, cy - 97, cx + 43, cy + 5], start=110, end=250, fill=CYAN + (210,), width=4)
    d.arc([cx - 43, cy - 97, cx + 43, cy + 5], start=290, end=70, fill=GOLD + (210,), width=4)


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    canvas = Image.new("RGBA", (W, H), BG + (255,))

    # Split-lighting glows
    canvas = add_radial_glow(canvas, int(W * 0.24), int(H * 0.36), 420, CYAN, 85)
    canvas = add_radial_glow(canvas, int(W * 0.76), int(H * 0.36), 420, GOLD, 85)
    canvas = add_radial_glow(canvas, int(W * 0.50), int(H * 0.34), 240, (120, 210, 230), 45)

    scene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scene)

    # Subtle architectural grid lines
    for gx in range(0, W, 80):
        d.line([(gx, 0), (gx, int(H * 0.65))], fill=(255, 255, 255, 10), width=1)
    for gy in range(0, int(H * 0.65), 80):
        d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 10), width=1)

    # Classical flanking marble columns
    draw_column(d, 130, 70, 560, 54, CYAN)
    draw_column(d, 240, 105, 560, 42, CYAN)
    draw_column(d, 960, 105, 560, 42, GOLD)
    draw_column(d, 1070, 70, 560, 54, GOLD)

    # Governance conduits linking seals to central Hermes bust
    cx, cy = W // 2, 310
    seals = [
        (340, 260, 48, CYAN, "git"),
        (600, 125, 48, (130, 220, 240), "plane"),
        (860, 260, 48, GOLD, "lock"),
    ]
    for sx, sy, sr, scol, _ in seals:
        d.line([(sx, sy), (cx, cy - 20)], fill=(scol[0], scol[1], scol[2], 150), width=3)
        d.line([(sx, sy + 4), (cx, cy - 16)], fill=(255, 255, 255, 70), width=1)

    # Central Hermes bust & 3 governance seals
    draw_hermes_bust(d, cx, cy)
    for sx, sy, sr, scol, sym in seals:
        draw_seal(d, sx, sy, sr, scol, sym)

    canvas = Image.alpha_composite(canvas, scene)

    # Editorial overlay (exact match to generate_cover_omniroute.py)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(layer)

    for y in range(int(H * 0.48), H):
        t = (y - int(H * 0.48)) / (H - int(H * 0.48))
        od.line([(0, y), (W, y)], fill=(7, 7, 10, int(235 * (t ** 1.2))))

    bar_x, y1, y2 = 64, 615, 845
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        od.line([(bar_x, y), (bar_x + 7, y)], fill=(int(223 * t), int(229 - 43 * t), int(255 - 148 * t), 255))

    od.text((92, 615), "INTELIGÊNCIA AGÊNTICA  •  GOVERNANÇA", fill=(0, 229, 255, 255), font=get_font(22))
    od.text((92, 655), "Managed Scope & Remote Config:", fill=(255, 255, 255, 255), font=get_font(54))
    od.text((92, 722), "Padronize Agentes na Empresa", fill=(223, 186, 107, 255), font=get_font(54))
    od.text((92, 804), "Trave políticas, distribua perfis via Git e controle frotas 24/7", fill=(215, 225, 235, 235), font=get_font(26, bold=False))

    final = Image.alpha_composite(canvas, layer).convert("RGB")
    final.save(OUT_PATH, format="JPEG", quality=94)
    print(f"OK: {OUT_PATH} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
