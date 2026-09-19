import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_jev_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    draw = ImageDraw.Draw(im, "RGBA")
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Decision / Speed / 0.05s)
    for r in range(500, 0, -15):
        alpha = int(40 * (1 - r / 500))
        glow_draw.ellipse([ -120 - r, 180 - r, 380 + r, 680 + r ], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Architecture / Precision)
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
    col_left_x = 160
    col_w = 60
    for fl in range(6):
        fl_x = col_left_x + fl * 10
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(120, 220, 250, 60), width=2)
    glow_draw.rectangle([col_left_x - 15, 120, col_left_x + col_w + 15, 150], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)
    glow_draw.rectangle([col_left_x - 20, 760, col_left_x + col_w + 20, 800], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)

    col_right_x = 980
    for fl in range(6):
        fl_x = col_right_x + fl * 10
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(230, 200, 120, 60), width=2)
    glow_draw.rectangle([col_right_x - 15, 120, col_right_x + col_w + 15, 150], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)
    glow_draw.rectangle([col_right_x - 20, 760, col_right_x + col_w + 20, 800], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)

    # Top Pediment triangle
    glow_draw.polygon([(600, 80), (130, 140), (1070, 140)], outline=(180, 210, 230, 120), width=2)

    # 3. Decision Tree / Fast Optical Switchboard (Representing Jev System 1)
    center_x = 600
    center_y = 430

    # Luminous Central Decision Hub
    for r in range(120, 0, -10):
        a = int(60 * (1 - r / 120))
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(0, 229, 255, a))
        
    glow_draw.ellipse([center_x - 45, center_y - 45, center_x + 45, center_y + 45], fill=(10, 25, 35, 230), outline=(0, 229, 255, 255), width=3)
    glow_draw.ellipse([center_x - 15, center_y - 15, center_x + 15, center_y + 15], fill=(223, 186, 107, 240), outline=(255, 255, 255, 255), width=2)

    # Fast Laser Branching Lines (Binary Decision Paths)
    branches = [
        # Left branches (Cyan - Fast Classification)
        ((center_x - 45, center_y), (360, 280), (260, 280), "YES / TRUE", (0, 229, 255)),
        ((center_x - 45, center_y), (360, 430), (260, 430), "VENDAS", (0, 229, 255)),
        ((center_x - 45, center_y), (360, 580), (260, 580), "SCORE: 0.98", (0, 229, 255)),
        
        # Right branches (Gold - Fast Routing / Hermes Execution)
        ((center_x + 45, center_y), (840, 280), (940, 280), "SYSTEM 1: 0.05s", (223, 186, 107)),
        ((center_x + 45, center_y), (840, 430), (940, 430), "HERMES AGENT", (223, 186, 107)),
        ((center_x + 45, center_y), (840, 580), (940, 580), "400x CHEAPER", (223, 186, 107)),
    ]

    for p_start, p_mid, p_end, label, color in branches:
        # Draw high-tech routed lines
        glow_draw.line([p_start, p_mid], fill=(*color, 200), width=3)
        glow_draw.line([p_mid, p_end], fill=(*color, 220), width=3)
        
        # Node circles
        glow_draw.ellipse([p_mid[0] - 6, p_mid[1] - 6, p_mid[0] + 6, p_mid[1] + 6], fill=(255, 255, 255, 255))
        glow_draw.ellipse([p_end[0] - 8, p_end[1] - 8, p_end[0] + 8, p_end[1] + 8], fill=(*color, 255), outline=(255, 255, 255, 255), width=2)
        
        # Tag box
        box_w, box_h = 130, 28
        bx = p_end[0] - box_w - 15 if p_end[0] < center_x else p_end[0] + 15
        by = p_end[1] - box_h // 2
        glow_draw.rectangle([bx, by, bx + box_w, by + box_h], fill=(10, 15, 22, 220), outline=(*color, 180), width=1)

    # 4. Floating HUD badges & Title Elements
    # Badge Top: "TYPESAFE AI • JEV MODEL • SYSTEM 1"
    glow_draw.rectangle([430, 170, 770, 205], fill=(10, 20, 30, 210), outline=(0, 229, 255, 200), width=1)
    
    # Badge Bottom: "INTELIGÊNCIA AGÊNTICA • DECISÃO ESTRUTURADA"
    glow_draw.rectangle([390, 720, 810, 760], fill=(25, 20, 10, 220), outline=(223, 186, 107, 200), width=1)

    # Composite glow and base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # 5. Add Text using basic or default font with crisp fallback
    final_draw = ImageDraw.Draw(im)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 18)
        font_badge = ImageFont.truetype("arialbd.ttf", 15)
        font_node = ImageFont.truetype("arialbd.ttf", 13)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_badge = font_title
        font_node = font_title
        
    final_draw.text((600, 187), "TYPESAFE AI  •  JEV  •  SYSTEM 1", fill=(0, 229, 255), font=font_badge, anchor="mm")
    final_draw.text((600, 740), "INTELIGÊNCIA AGÊNTICA  •  ARQUITETURA DE DECISÃO", fill=(223, 186, 107), font=font_badge, anchor="mm")
    
    # Text on node labels
    final_draw.text((260 - 80, 280), "YES / TRUE", fill=(200, 245, 255), font=font_node, anchor="mm")
    final_draw.text((260 - 80, 430), "TRIAGEM VENDAS", fill=(200, 245, 255), font=font_node, anchor="mm")
    final_draw.text((260 - 80, 580), "SCORE: 0.98", fill=(200, 245, 255), font=font_node, anchor="mm")
    
    final_draw.text((940 + 80, 280), "LATÊNCIA: 0.05s", fill=(255, 235, 180), font=font_node, anchor="mm")
    final_draw.text((940 + 80, 430), "HERMES AGENT", fill=(255, 235, 180), font=font_node, anchor="mm")
    final_draw.text((940 + 80, 580), "CUSTO 400x MENOR", fill=(255, 235, 180), font=font_node, anchor="mm")

    # Save final image
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "jev-typesafe-ia-de-decisao-rapida-hermes.jpg")
    
    im.save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso em: {out_path}")
    return True

if __name__ == "__main__":
    create_jev_cover()
