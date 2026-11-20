"""Gera capa 1200x912px em estilo Hermes Cyber-Classicism via Pillow para:
mixture-of-agents-moa-conselho-modelos-hermes.jpg
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_PATH = r"D:\DevCod\inteligencia-agentica\static\images\mixture-of-agents-moa-conselho-modelos-hermes.jpg"
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
    d.rectangle([x - width // 2, top_y, x + width // 2, bot_y], fill=(24, 26, 34, 210))
    d.rectangle([x - width // 2 - 10, top_y - 14, x + width // 2 + 10, top_y + 4], fill=(42, 46, 58, 230))
    d.rectangle([x - width // 2 - 12, bot_y - 4, x + width // 2 + 12, bot_y + 14], fill=(38, 42, 54, 230))
    for fx in range(x - width // 2 + 8, x + width // 2 - 4, 12):
        d.line([(fx, top_y + 8), (fx, bot_y - 8)], fill=(12, 14, 20, 180), width=3)
        d.line([(fx + 3, top_y + 8), (fx + 3, bot_y - 8)], fill=(tint_color[0], tint_color[1], tint_color[2], 42), width=1)


def draw_advisor_bust(d, cx, cy, scale, rim_color):
    s = scale
    # Pedestal
    d.polygon([
        (cx - int(55 * s), cy + int(125 * s)),
        (cx + int(55 * s), cy + int(125 * s)),
        (cx + int(40 * s), cy + int(92 * s)),
        (cx - int(40 * s), cy + int(92 * s)),
    ], fill=(32, 36, 46, 235))
    # Shoulders
    d.polygon([
        (cx - int(74 * s), cy + int(94 * s)),
        (cx + int(74 * s), cy + int(94 * s)),
        (cx + int(54 * s), cy + int(28 * s)),
        (cx + int(20 * s), cy + int(12 * s)),
        (cx - int(20 * s), cy + int(12 * s)),
        (cx - int(54 * s), cy + int(28 * s)),
    ], fill=(158, 164, 178, 235))
    # Neck & head
    d.rectangle([cx - int(16 * s), cy - int(10 * s), cx + int(16 * s), cy + int(18 * s)], fill=(148, 154, 168, 235))
    d.ellipse([cx - int(34 * s), cy - int(80 * s), cx + int(34 * s), cy + int(2 * s)], fill=(188, 194, 206, 245))
    # Rim light
    d.ellipse([cx - int(35 * s), cy - int(81 * s), cx + int(35 * s), cy + int(3 * s)], outline=rim_color + (200,), width=3)
    # Holographic node halo above advisor
    d.ellipse([cx - int(18 * s), cy - int(115 * s), cx + int(18 * s), cy - int(79 * s)], outline=rim_color + (210,), width=2)
    d.ellipse([cx - int(6 * s), cy - int(103 * s), cx + int(6 * s), cy - int(91 * s)], fill=rim_color + (255,))


def draw_hermes_aggregator(d, cx, cy):
    # Central winged-helmet Hermes bust (Aggregator)
    d.polygon([(cx - 76, cy + 156), (cx + 76, cy + 156), (cx + 55, cy + 112), (cx - 55, cy + 112)], fill=(38, 42, 54, 245))
    d.polygon([(cx - 102, cy + 114), (cx + 102, cy + 114), (cx + 72, cy + 36), (cx + 28, cy + 16), (cx - 28, cy + 16), (cx - 72, cy + 36)], fill=(186, 192, 206, 248))
    d.rectangle([cx - 23, cy - 12, cx + 23, cy + 22], fill=(172, 178, 192, 248))
    d.ellipse([cx - 44, cy - 98, cx + 44, cy + 4], fill=(214, 218, 226, 252))
    d.pieslice([cx - 48, cy - 114, cx + 48, cy - 30], start=180, end=360, fill=(196, 202, 214, 252))
    # Winged helmet
    d.polygon([(cx - 46, cy - 76), (cx - 94, cy - 124), (cx - 70, cy - 84), (cx - 42, cy - 62)], fill=CYAN + (235,))
    d.polygon([(cx + 46, cy - 76), (cx + 94, cy - 124), (cx + 70, cy - 84), (cx + 42, cy - 62)], fill=GOLD + (235,))
    d.arc([cx - 45, cy - 99, cx + 45, cy + 5], start=110, end=250, fill=CYAN + (220,), width=4)
    d.arc([cx - 45, cy - 99, cx + 45, cy + 5], start=290, end=70, fill=GOLD + (220,), width=4)

    # Crystalline decision prism hovering above Hermes
    py = cy - 165
    prism = [(cx, py - 42), (cx + 36, py), (cx, py + 42), (cx - 36, py)]
    d.polygon(prism, fill=(22, 28, 40, 220), outline=GOLD + (245,))
    d.line([(cx, py - 42), (cx, py + 42)], fill=CYAN + (200,), width=2)
    d.line([(cx - 36, py), (cx + 36, py)], fill=GOLD + (180,), width=2)
    d.ellipse([cx - 8, py - 8, cx + 8, py + 8], fill=(255, 248, 225, 255))


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    canvas = Image.new("RGBA", (W, H), BG + (255,))

    # Split-lighting glows
    canvas = add_radial_glow(canvas, int(W * 0.23), int(H * 0.36), 410, CYAN, 90)
    canvas = add_radial_glow(canvas, int(W * 0.77), int(H * 0.36), 410, GOLD, 90)
    canvas = add_radial_glow(canvas, int(W * 0.50), int(H * 0.28), 260, (160, 215, 230), 55)

    scene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scene)

    # Subtle architectural grid
    for gx in range(0, W, 80):
        d.line([(gx, 0), (gx, int(H * 0.65))], fill=(255, 255, 255, 10), width=1)
    for gy in range(0, int(H * 0.65), 80):
        d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 10), width=1)

    # Classical flanking marble columns
    draw_column(d, 110, 65, 560, 50, CYAN)
    draw_column(d, 1090, 65, 560, 50, GOLD)

    # Council positions
    cx, cy = W // 2, 325
    left_ax, left_ay = 290, 340
    right_ax, right_ay = 910, 340
    prism_y = cy - 165

    # Neural light filaments from both advisor nodes to the central decision prism & Hermes
    for offset in (-8, 0, 8):
        d.line([(left_ax, left_ay - 75), (cx, prism_y + offset)], fill=CYAN + (165,), width=2 if offset == 0 else 1)
        d.line([(right_ax, right_ay - 75), (cx, prism_y + offset)], fill=GOLD + (165,), width=2 if offset == 0 else 1)
    d.line([(cx, prism_y + 42), (cx, cy - 114)], fill=(240, 245, 255, 210), width=3)

    # Orbital council arc
    d.arc([230, 140, 970, 520], start=195, end=345, fill=(255, 255, 255, 45), width=2)

    # Draw the two Advisor busts and the central Hermes Aggregator bust
    draw_advisor_bust(d, left_ax, left_ay, 0.82, CYAN)
    draw_advisor_bust(d, right_ax, right_ay, 0.82, GOLD)
    draw_hermes_aggregator(d, cx, cy)

    # Editorial bottom gradient & typography (matching generate_cover_omniroute.py)
    for y in range(int(H * 0.48), H):
        t = (y - int(H * 0.48)) / (H - int(H * 0.48))
        d.line([(0, y), (w := W, y)], fill=(7, 7, 10, int(235 * (t ** 1.2))))

    bar_x, y1, y2 = 64, 615, 845
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        d.line([(bar_x, y), (bar_x + 7, y)], fill=(int(223 * t), int(229 - 43 * t), int(255 - 148 * t), 255))

    d.text((92, 615), "INTELIGÊNCIA AGÊNTICA  •  MIXTURE OF AGENTS", fill=(0, 229, 255, 255), font=get_font(22))
    d.text((92, 655), "Mixture of Agents (MoA):", fill=(255, 255, 255, 255), font=get_font(56))
    d.text((92, 722), "Conselho de IAs no Hermes", fill=(223, 186, 107, 255), font=get_font(56))
    d.text((92, 804), "Múltiplas perspectivas, +6 pontos no HermesBench e cache intacto", fill=(215, 225, 235, 235), font=get_font(26, bold=False))

    final = Image.alpha_composite(canvas, scene).convert("RGB")
    final.save(OUT_PATH, format="JPEG", quality=94)
    print(f"OK: {OUT_PATH} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
