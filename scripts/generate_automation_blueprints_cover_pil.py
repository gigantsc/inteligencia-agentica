"""Gera capa 1200x912px em estilo Hermes Cyber-Classicism via Pillow para:
automation-blueprints-fluxos-prontos-hermes-agent.jpg
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_PATH = r"D:\DevCod\inteligencia-agentica\static\images\automation-blueprints-fluxos-prontos-hermes-agent.jpg"
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


def draw_blueprint_card(d, x, y, w, h, border_color, badge, title, sub):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(11, 16, 26, 235), outline=border_color + (235,), width=2)
    # Blueprint corner ticks
    d.line([(x + 6, y + 6), (x + 16, y + 6)], fill=border_color + (160,), width=1)
    d.line([(x + 6, y + 6), (x + 6, y + 16)], fill=border_color + (160,), width=1)
    d.rectangle([x + 2, y + 2, x + w - 2, y + 32], fill=(border_color[0], border_color[1], border_color[2], 38))
    d.rounded_rectangle([x + w - 92, y + 6, x + w - 10, y + 26], radius=5, fill=border_color + (215,))
    d.text((x + w - 84, y + 9), badge, fill=(7, 7, 10, 255), font=get_font(11, bold=True))
    d.text((x + 14, y + 8), title, fill=border_color + (255,), font=get_font(15, bold=True))
    d.text((x + 14, y + 44), sub, fill=(215, 224, 236, 225), font=get_font(13, bold=False))


def draw_gear_ring(d, cx, cy, r_outer, r_inner, teeth, color):
    pts = []
    for i in range(teeth * 2):
        angle = (i * math.pi) / teeth
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    d.polygon(pts, outline=color)


def draw_blueprint_orbital(d, cx, cy):
    for r, col, w in [(182, CYAN + (85,), 2), (150, GOLD + (115,), 2), (120, CYAN + (155,), 2)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
    draw_gear_ring(d, cx, cy, 168, 158, 24, GOLD + (90,))


def draw_hermes_bust(d, cx, cy):
    d.polygon([(cx - 78, cy + 160), (cx + 78, cy + 160), (cx + 56, cy + 114), (cx - 56, cy + 114)], fill=(38, 42, 54, 245))
    d.polygon([(cx - 104, cy + 116), (cx + 104, cy + 116), (cx + 74, cy + 36), (cx + 28, cy + 16), (cx - 28, cy + 16), (cx - 74, cy + 36)], fill=(186, 192, 206, 248))
    d.rectangle([cx - 23, cy - 12, cx + 23, cy + 22], fill=(172, 178, 192, 248))
    d.ellipse([cx - 45, cy - 100, cx + 45, cy + 4], fill=(214, 218, 226, 252))
    d.pieslice([cx - 49, cy - 116, cx + 49, cy - 30], start=180, end=360, fill=(196, 202, 214, 252))
    d.polygon([(cx - 47, cy - 76), (cx - 96, cy - 126), (cx - 72, cy - 84), (cx - 43, cy - 62)], fill=CYAN + (235,))
    d.polygon([(cx + 47, cy - 76), (cx + 96, cy - 126), (cx + 72, cy - 84), (cx + 43, cy - 62)], fill=GOLD + (235,))
    d.arc([cx - 46, cy - 101, cx + 46, cy + 5], start=110, end=250, fill=CYAN + (225,), width=4)
    d.arc([cx - 46, cy - 101, cx + 46, cy + 5], start=290, end=70, fill=GOLD + (225,), width=4)


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    canvas = Image.new("RGBA", (W, H), BG + (255,))

    canvas = add_radial_glow(canvas, int(W * 0.24), int(H * 0.34), 390, CYAN, 95)
    canvas = add_radial_glow(canvas, int(W * 0.76), int(H * 0.34), 390, GOLD, 95)
    canvas = add_radial_glow(canvas, int(W * 0.50), int(H * 0.33), 260, (175, 220, 235), 60)

    scene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scene)

    # Blueprint fine grid
    for gx in range(0, W, 40):
        alpha = 18 if gx % 80 == 0 else 8
        d.line([(gx, 0), (gx, int(H * 0.65))], fill=(0, 229, 255, alpha), width=1)
    for gy in range(0, int(H * 0.65), 40):
        alpha = 18 if gy % 80 == 0 else 8
        d.line([(0, gy), (W, gy)], fill=(0, 229, 255, alpha), width=1)

    draw_column(d, 95, 60, 560, 46, CYAN)
    draw_column(d, 1105, 60, 560, 46, GOLD)

    draw_blueprint_orbital(d, 600, 305)

    left_cards = [
        (155, 82, "SCHEDULE", "/cron & /blueprint", "Rotinas sem sintaxe cron"),
        (155, 200, "GITHUB", "PRs, Issues & CI", "Webhook de código em tempo real"),
        (155, 318, "API CALL", "Stripe & Alertas", "POST JSON assinado (HMAC)"),
    ]
    for x, y, badge, title, sub in left_cards:
        draw_blueprint_card(d, x, y, 270, 84, CYAN, badge, title, sub)
        d.line([(x + 270, y + 42), (512, 295)], fill=CYAN + (195,), width=3)

    right_cards = [
        (775, 82, "[SILENT]", "Filtro Anti-Ruído", "Notifica só quando há anomalia"),
        (775, 200, "SKILL.MD", "Blueprints Próprios", "Bloco hermes.blueprint por perfil"),
        (775, 318, "DELIVERY", "Entrega Multi-Canal", "Telegram, Slack, Discord & SMS"),
    ]
    for x, y, badge, title, sub in right_cards:
        draw_blueprint_card(d, x, y, 270, 84, GOLD, badge, title, sub)
        d.line([(x, y + 42), (688, 295)], fill=GOLD + (195,), width=3)

    draw_hermes_bust(d, 600, 305)

    for y in range(int(H * 0.50), H):
        t = (y - int(H * 0.50)) / (H - int(H * 0.50))
        d.line([(0, y), (W, y)], fill=(7, 7, 10, int(238 * (t ** 1.2))))

    bar_x, y1, y2 = 64, 615, 845
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        d.line([(bar_x, y), (bar_x + 7, y)], fill=(int(223 * t), int(229 - 43 * t), int(255 - 148 * t), 255))

    d.text((92, 615), "INTELIGÊNCIA AGÊNTICA  •  AUTOMAÇÃO PRONTA", fill=CYAN + (255,), font=get_font(22))
    d.text((92, 655), "Automation Blueprints:", fill=(255, 255, 255, 255), font=get_font(54))
    d.text((92, 722), "Fluxos Prontos Sem Código", fill=GOLD + (255,), font=get_font(48))
    d.text((92, 804), "Agende rotinas, webhooks Stripe e watchdogs com /blueprint", fill=(215, 225, 235, 235), font=get_font(24, bold=False))

    final = Image.alpha_composite(canvas, scene).convert("RGB")
    final.save(OUT_PATH, format="JPEG", quality=94)
    print(f"OK: {OUT_PATH} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
