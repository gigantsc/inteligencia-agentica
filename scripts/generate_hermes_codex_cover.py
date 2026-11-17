import os
import math
from PIL import Image, ImageDraw, ImageFont


def load_font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\segoeui.ttf" if not bold else r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arial.ttf" if not bold else r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\consola.ttf" if not bold else r"C:\Windows\Fonts\consolab.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_hermes_codex_cover():
    width, height = 1200, 912

    # 1. Fundo Obsidian (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # 2. Split Ambient Wash: Ciano Esquerda (#00E5FF) e Ouro Direita (#DFBA6B)
    for r in range(580, 0, -14):
        alpha = int(46 * (1 - r / 580))
        draw.ellipse([-150 - r, 180 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
    for r in range(580, 0, -14):
        alpha = int(46 * (1 - r / 580))
        draw.ellipse([780 - r, 180 - r, 1350 + r, 720 + r], fill=(223, 186, 107, alpha))

    # 3. Grade Cibernética em Perspectiva no Piso
    for y in range(660, height, 18):
        alpha = int(42 * ((y - 660) / (height - 660)))
        draw.line([(0, y), (width, y)], fill=(0, 215, 245, alpha), width=1)
    for x in range(40, width, 55):
        draw.line([(x, 660), (int(600 + (x - 600) * 1.8), height)], fill=(0, 215, 245, 18), width=1)

    # 4. Pórtico Greco-Romano (Colunas de Mármore Ciano e Dourado + Frontão)
    col1_x, col2_x, col_w = 75, 1070, 54
    for fl in range(6):
        draw.line([(col1_x + fl * 9, 105), (col1_x + fl * 9, 770)], fill=(90, 215, 245, 70), width=2)
        draw.line([(col2_x + fl * 9, 105), (col2_x + fl * 9, 770)], fill=(215, 190, 115, 70), width=2)

    draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 225), outline=(0, 229, 255, 220), width=2)
    draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 225), outline=(0, 229, 255, 220), width=2)

    draw.rectangle([col2_x - 14, 85, col2_x + col_w + 14, 115], fill=(42, 36, 16, 225), outline=(223, 186, 107, 220), width=2)
    draw.rectangle([col2_x - 16, 750, col2_x + col_w + 16, 785], fill=(42, 36, 16, 225), outline=(223, 186, 107, 220), width=2)

    # Frontão Clássico
    draw.polygon([(600, 28), (55, 100), (1145, 100)], outline=(170, 205, 225, 130), width=2)
    draw.polygon([(600, 44), (85, 100), (1115, 100)], outline=(223, 186, 107, 110), width=1)
    draw.rectangle([55, 100, 1145, 118], fill=(12, 16, 24, 210), outline=(160, 195, 215, 120), width=1)

    font_tag = load_font(15, bold=True)
    font_title = load_font(26, bold=True)
    font_sub = load_font(16, bold=False)

    # Faixa do frontão
    draw.rectangle([280, 90, 920, 116], fill=(8, 14, 22, 240), outline=(0, 229, 255, 220), width=1)
    draw.text((600, 103), "HERMES AGENT  //  ORQUESTRADOR + CODEX CLI", fill=(223, 186, 107, 245), font=font_tag, anchor="mm")

    # 5. Pedestal Neoclássico Central
    base_x, base_y = 600, 685
    draw.rectangle([base_x - 190, base_y, base_x + 190, base_y + 38], fill=(18, 26, 38, 235), outline=(223, 186, 107, 230), width=2)
    draw.rectangle([base_x - 220, base_y + 38, base_x + 220, base_y + 70], fill=(10, 16, 26, 245), outline=(0, 229, 255, 230), width=2)
    draw.text((base_x, base_y + 19), "20+ CHATS  •  MEMÓRIA ATIVA  •  ZERO TELEMETRIA", fill=(235, 245, 255, 235), font=font_tag, anchor="mm")

    # 6. Núcleo Orbital Central + Dois Polos (Hermes Esquerda / Codex Direita)
    cx, cy = 600, 395
    for r in range(215, 40, -12):
        alpha = int(28 * (1 - r / 215))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 229, 255, alpha))
    for r in range(155, 40, -12):
        alpha = int(26 * (1 - r / 155))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(223, 186, 107, alpha))

    draw.ellipse([cx - 210, cy - 210, cx + 210, cy + 210], outline=(0, 229, 255, 170), width=2)
    draw.ellipse([cx - 155, cy - 155, cx + 155, cy + 155], outline=(223, 186, 107, 190), width=2)

    # Nó Esquerdo: HERMES AGENT (Ciano)
    hx, hy = 315, 395
    for r in range(110, 15, -10):
        draw.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(0, 229, 255, int(35 * (1 - r / 110))))
    draw.rectangle([hx - 115, hy - 95, hx + 115, hy + 95], fill=(8, 18, 30, 242), outline=(0, 229, 255, 245), width=2)
    draw.rectangle([hx - 107, hy - 87, hx + 107, hy + 87], outline=(255, 255, 255, 55), width=1)
    draw.text((hx, hy - 48), "HERMES", fill=(0, 229, 255, 255), font=font_title, anchor="mm")
    draw.text((hx, hy - 14), "ORQUESTRADOR", fill=(230, 245, 255, 230), font=font_tag, anchor="mm")
    draw.line([(hx - 75, hy + 10), (hx + 75, hy + 10)], fill=(0, 229, 255, 180), width=1)
    draw.text((hx, hy + 34), "Skill: codex", fill=(180, 235, 255, 230), font=font_sub, anchor="mm")
    draw.text((hx, hy + 58), "hermes migrate codex", fill=(223, 186, 107, 230), font=font_sub, anchor="mm")

    # Nó Direito: OPENAI CODEX CLI (Ouro)
    ox, oy = 885, 395
    for r in range(110, 15, -10):
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(223, 186, 107, int(35 * (1 - r / 110))))
    draw.rectangle([ox - 115, oy - 95, ox + 115, oy + 95], fill=(24, 20, 10, 242), outline=(223, 186, 107, 245), width=2)
    draw.rectangle([ox - 107, oy - 87, ox + 107, oy + 87], outline=(255, 255, 255, 55), width=1)
    draw.text((ox, oy - 48), "CODEX CLI", fill=(223, 186, 107, 255), font=font_title, anchor="mm")
    draw.text((ox, oy - 14), "EXECUTOR DE CÓDIGO", fill=(255, 245, 225, 230), font=font_tag, anchor="mm")
    draw.line([(ox - 75, oy + 10), (ox + 75, oy + 10)], fill=(223, 186, 107, 180), width=1)
    draw.text((ox, oy + 34), "Features & PRs", fill=(255, 230, 180, 230), font=font_sub, anchor="mm")
    draw.text((ox, oy + 58), "Login ChatGPT", fill=(0, 229, 255, 230), font=font_sub, anchor="mm")

    # Ponte Central Bidirecional (Conduíte + Hub)
    draw.line([(hx + 115, hy - 14), (ox - 115, oy - 14)], fill=(0, 229, 255, 220), width=3)
    draw.line([(hx + 115, hy + 14), (ox - 115, oy + 14)], fill=(223, 186, 107, 220), width=3)

    # Hub Central
    draw.ellipse([cx - 56, cy - 56, cx + 56, cy + 56], fill=(10, 16, 26, 250), outline=(255, 255, 255, 220), width=2)
    draw.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=(0, 229, 255, 220), width=2)
    draw.text((cx, cy - 8), "2-WAY", fill=(223, 186, 107, 255), font=font_tag, anchor="mm")
    draw.text((cx, cy + 12), "SYNC", fill=(0, 229, 255, 255), font=font_tag, anchor="mm")

    # Feixe Superior para o Cristal de Síntese
    draw.polygon([(cx - 24, cy - 56), (cx + 24, cy - 56), (cx + 8, 130), (cx - 8, 130)], fill=(223, 186, 107, 65))
    draw.ellipse([cx - 18, 135 - 18, cx + 18, 135 + 18], fill=(223, 186, 107, 225), outline=(255, 255, 255, 240), width=2)

    final_img = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")

    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "hermes-agent-vs-codex-orquestracao-codigo.jpg")
    final_img.save(out_path, format="JPEG", quality=95)
    print(f"OK: {out_path}")
    return out_path


if __name__ == "__main__":
    create_hermes_codex_cover()
