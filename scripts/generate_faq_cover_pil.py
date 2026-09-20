import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_faq_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient Lighting
    # Left Cyan ambient wash (Intelligence / Questions / Execution)
    for r in range(500, 0, -15):
        alpha = int(40 * (1 - r / 500))
        glow_draw.ellipse([ -120 - r, 180 - r, 380 + r, 680 + r ], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Architecture / Mastery / Manual)
    for r in range(500, 0, -15):
        alpha = int(40 * (1 - r / 500))
        glow_draw.ellipse([ 820 - r, 180 - r, 1320 + r, 680 + r ], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid
    for y in range(650, height, 25):
        alpha = int(35 * ((y - 650) / (height - 650)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 200, 240, alpha), width=1)
    for x in range(100, width, 80):
        glow_draw.line([(x, 650), (int(600 + (x - 600) * 1.6), height)], fill=(0, 200, 240, 18), width=1)
        
    # 2. Draw Classical Columns & Arch
    col_left_x = 130
    col_w = 60
    for fl in range(6):
        fl_x = col_left_x + fl * 10
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(120, 220, 250, 60), width=2)
    glow_draw.rectangle([col_left_x - 15, 120, col_left_x + col_w + 15, 150], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)
    glow_draw.rectangle([col_left_x - 20, 760, col_left_x + col_w + 20, 800], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)

    col_right_x = 1010
    for fl in range(6):
        fl_x = col_right_x + fl * 10
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(230, 200, 120, 60), width=2)
    glow_draw.rectangle([col_right_x - 15, 120, col_right_x + col_w + 15, 150], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)
    glow_draw.rectangle([col_right_x - 20, 760, col_right_x + col_w + 20, 800], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)

    # Top Pediment triangle
    glow_draw.polygon([(600, 65), (100, 140), (1100, 140)], outline=(180, 210, 230, 120), width=2)

    # 3. Central Classical Architectural Portal / 30 Questions Shield
    center_x = 600
    center_y = 430

    # Luminous Core
    for r in range(150, 0, -10):
        a = int(45 * (1 - r / 150))
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(0, 229, 255, a))
        
    glow_draw.ellipse([center_x - 70, center_y - 70, center_x + 70, center_y + 70], fill=(12, 25, 35, 240), outline=(0, 229, 255, 255), width=3)
    glow_draw.ellipse([center_x - 35, center_y - 35, center_x + 35, center_y + 35], fill=(223, 186, 107, 240), outline=(255, 255, 255, 255), width=2)

    # 4 Foundation Pillars / 4 Brain Files
    pillars = [
        ((320, 290), "SOUL.md", "Identidade do Agente", (0, 229, 255)),
        ((320, 560), "AGENTS.md", "Regras do Projeto", (0, 229, 255)),
        ((880, 290), "MEMORY.md", "Aprendizado Contínuo", (223, 186, 107)),
        ((880, 560), "USER.md", "Perfil do Fundador", (223, 186, 107)),
    ]

    for (px, py), title, desc, color in pillars:
        # Link line to center
        glow_draw.line([(center_x, center_y), (px, py)], fill=(*color, 150), width=2)
        
        # Card Box
        bw, bh = 210, 65
        glow_draw.rectangle([px - bw//2, py - bh//2, px + bw//2, py + bh//2], fill=(10, 18, 25, 240), outline=(*color, 220), width=2)
        glow_draw.ellipse([px - 6, py - bh//2 - 6, px + 6, py - bh//2 + 6], fill=(255, 255, 255, 255))

    # 4. Floating HUD badges
    glow_draw.rectangle([390, 160, 810, 198], fill=(10, 20, 30, 210), outline=(0, 229, 255, 200), width=1)
    glow_draw.rectangle([340, 720, 860, 760], fill=(25, 20, 10, 220), outline=(223, 186, 107, 200), width=1)

    # Composite glow and base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    final_draw = ImageDraw.Draw(im)
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 15)
        font_core_num = ImageFont.truetype("arialbd.ttf", 32)
        font_core_txt = ImageFont.truetype("arialbd.ttf", 11)
        font_pill_t = ImageFont.truetype("arialbd.ttf", 14)
        font_pill_d = ImageFont.truetype("arial.ttf", 11)
    except:
        font_badge = ImageFont.load_default()
        font_core_num = font_badge
        font_core_txt = font_badge
        font_pill_t = font_badge
        font_pill_d = font_badge
        
    final_draw.text((600, 179), "HERMES AGENT  •  MANUAL DEFINITIVO", fill=(0, 229, 255), font=font_badge, anchor="mm")
    final_draw.text((600, 740), "AS 30 RESPOSTAS ESSENCIAIS  •  GUIA PRÁTICO", fill=(223, 186, 107), font=font_badge, anchor="mm")
    
    # Core Center Text
    final_draw.text((600, 420), "30", fill=(255, 255, 255), font=font_core_num, anchor="mm")
    final_draw.text((600, 448), "RESPOSTAS", fill=(255, 235, 180), font=font_core_txt, anchor="mm")

    # Pillar texts
    for (px, py), title, desc, color in pillars:
        final_draw.text((px, py - 12), title, fill=(255, 255, 255), font=font_pill_t, anchor="mm")
        final_draw.text((px, py + 12), desc, fill=(180, 210, 230), font=font_pill_d, anchor="mm")

    # Save final image
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "guia-completo-faq-hermes-agent-funcionarios-digitais.jpg")
    
    im.save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso em: {out_path}")
    return True

if __name__ == "__main__":
    create_faq_cover()
