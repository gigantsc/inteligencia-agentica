"""Gera capa 1200x912px em estilo Hermes Cyber-Classicism via Pillow para:
event-hooks-hermes-agent-governanca-auditoria-bloqueio-tempo-real.jpg
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_PATH = r"D:\DevCod\inteligencia-agentica\static\images\event-hooks-hermes-agent-governanca-auditoria-bloqueio-tempo-real.jpg"
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


def draw_hook_card(d, x, y, w, h, border_color, badge, title, lines):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(13, 17, 26, 232), outline=border_color + (235,), width=2)
    d.rectangle([x + 2, y + 2, x + w - 2, y + 34], fill=(border_color[0], border_color[1], border_color[2], 40))
    d.rounded_rectangle([x + w - 108, y + 7, x + w - 12, y + 28], radius=6, fill=border_color + (215,))
    d.text((x + w - 100, y + 10), badge, fill=(7, 7, 10, 255), font=get_font(12, bold=True))
    d.text((x + 16, y + 9), title, fill=border_color + (255,), font=get_font(15, bold=True))
    for idx, line in enumerate(lines):
        ly = y + 48 + idx * 24
        d.ellipse([x + 16, ly + 5, x + 23, ly + 12], fill=border_color + (220,))
        d.text((x + 32, ly), line, fill=(218, 226, 238, 225), font=get_font(14, bold=False))


def draw_aegis_shield(d, cx, cy):
    # Escudo energético hexagonal/clássico atrás do busto de Hermes
    pts = [
        (cx, cy - 165),
        (cx + 125, cy - 115),
        (cx + 105, cy + 55),
        (cx, cy + 165),
        (cx - 105, cy + 55),
        (cx - 125, cy - 115),
    ]
    d.polygon(pts, fill=(12, 18, 28, 120), outline=CYAN + (170,), width=3)
    inner_pts = [
        (cx, cy - 145),
        (cx + 105, cy - 100),
        (cx + 88, cy + 45),
        (cx, cy + 140),
        (cx - 88, cy + 45),
        (cx - 105, cy - 100),
    ]
    d.polygon(inner_pts, outline=GOLD + (140,), width=2)


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

    canvas = add_radial_glow(canvas, int(W * 0.25), int(H * 0.34), 390, CYAN, 95)
    canvas = add_radial_glow(canvas, int(W * 0.75), int(H * 0.34), 390, GOLD, 95)
    canvas = add_radial_glow(canvas, int(W * 0.50), int(H * 0.33), 260, (175, 220, 235), 60)

    scene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scene)

    for gx in range(0, W, 80):
        d.line([(gx, 0), (gx, int(H * 0.65))], fill=(255, 255, 255, 10), width=1)
    for gy in range(0, int(H * 0.65), 80):
        d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 10), width=1)

    draw_column(d, 105, 60, 560, 48, CYAN)
    draw_column(d, 1095, 60, 560, 48, GOLD)

    draw_aegis_shield(d, 600, 310)

    draw_hook_card(
        d, 165, 105, 285, 140, CYAN, "FAIL-CLOSED", "1. Shell Hooks",
        ["pre_tool_call & exit code 2", "Bloqueio determinístico", "Qualquer linguagem via stdin"],
    )
    draw_hook_card(
        d, 175, 275, 270, 130, CYAN, "GATEWAY", "2. Gateway Hooks & BOOT.md",
        ["Monitoramento 24/7 na VPS", "Checklist silencioso [SILENT]"],
    )
    draw_hook_card(
        d, 750, 105, 285, 140, GOLD, "CACHE-SAFE", "3. Plugin Hooks",
        ["pre_llm_call & Kanban", "Prompt cache preservado", "Timeout isolado em 30s"],
    )
    draw_hook_card(
        d, 755, 275, 270, 130, GOLD, "HMAC-SHA256", "4. Outbound Webhooks",
        ["Telemetria fire-and-forget", "Assinatura anti-replay"],
    )

    d.line([(450, 175), (535, 255)], fill=CYAN + (210,), width=3)
    d.line([(445, 340), (530, 310)], fill=CYAN + (185,), width=3)
    d.line([(750, 175), (665, 255)], fill=GOLD + (210,), width=3)
    d.line([(755, 340), (670, 310)], fill=GOLD + (185,), width=3)

    draw_hermes_bust(d, 600, 310)

    for y in range(int(H * 0.50), H):
        t = (y - int(H * 0.50)) / (H - int(H * 0.50))
        d.line([(0, y), (W, y)], fill=(7, 7, 10, int(238 * (t ** 1.2))))

    bar_x, y1, y2 = 64, 615, 845
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        d.line([(bar_x, y), (bar_x + 7, y)], fill=(int(223 * t), int(229 - 43 * t), int(255 - 148 * t), 255))

    d.text((92, 615), "INTELIGÊNCIA AGÊNTICA  •  GOVERNANÇA & SEGURANÇA", fill=CYAN + (255,), font=get_font(22))
    d.text((92, 655), "Event Hooks no Hermes Agent:", fill=(255, 255, 255, 255), font=get_font(52))
    d.text((92, 722), "4 Camadas de Controle em Tempo Real", fill=GOLD + (255,), font=get_font(48))
    d.text((92, 804), "Bloqueio fail-closed, BOOT.md, Plugin Hooks e Outbound Webhooks HMAC", fill=(215, 225, 235, 235), font=get_font(24, bold=False))

    final = Image.alpha_composite(canvas, scene).convert("RGB")
    final.save(OUT_PATH, format="JPEG", quality=94)
    print(f"OK: {OUT_PATH} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
