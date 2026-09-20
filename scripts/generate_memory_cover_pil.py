import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_memory_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient Lighting
    # Left Cyan ambient wash (Short-term / Active Neural Retrieval)
    for r in range(500, 0, -15):
        alpha = int(40 * (1 - r / 500))
        glow_draw.ellipse([ -120 - r, 180 - r, 380 + r, 680 + r ], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Long-term / Persistent Knowledge Graph)
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
    col_left_x = 140
    col_w = 60
    for fl in range(6):
        fl_x = col_left_x + fl * 10
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(120, 220, 250, 60), width=2)
    glow_draw.rectangle([col_left_x - 15, 120, col_left_x + col_w + 15, 150], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)
    glow_draw.rectangle([col_left_x - 20, 760, col_left_x + col_w + 20, 800], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)

    col_right_x = 1000
    for fl in range(6):
        fl_x = col_right_x + fl * 10
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(230, 200, 120, 60), width=2)
    glow_draw.rectangle([col_right_x - 15, 120, col_right_x + col_w + 15, 150], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)
    glow_draw.rectangle([col_right_x - 20, 760, col_right_x + col_w + 20, 800], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)

    # Top Pediment triangle
    glow_draw.polygon([(600, 70), (110, 140), (1090, 140)], outline=(180, 210, 230, 120), width=2)

    # 3. Memory Knowledge Graph & 9 Memory Crystals
    center_x = 600
    center_y = 430

    # Luminous Core Brain / Hermes Memory Nexus
    for r in range(140, 0, -10):
        a = int(50 * (1 - r / 140))
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(0, 229, 255, a))
        
    glow_draw.ellipse([center_x - 55, center_y - 55, center_x + 55, center_y + 55], fill=(12, 28, 40, 240), outline=(0, 229, 255, 255), width=3)
    glow_draw.ellipse([center_x - 25, center_y - 25, center_x + 25, center_y + 25], fill=(223, 186, 107, 240), outline=(255, 255, 255, 255), width=2)

    # 8 Surrounding Memory Nodes (Forming the 9 Memory System)
    nodes = [
        # (angle, distance, label, color)
        (0, 240, "HINDSIGHT (GRAPH)", (223, 186, 107)),
        (45, 220, "HONCHO (MULTI-AGENT)", (223, 186, 107)),
        (90, 190, "SUPERMEMORY", (223, 186, 107)),
        (135, 220, "RETAINDB (FILES)", (0, 229, 255)),
        (180, 240, "BUILT-IN (LOCAL MD)", (0, 229, 255)),
        (225, 220, "HOLOGRAPHIC (SQLITE)", (0, 229, 255)),
        (270, 190, "BYTEROVER (CODE/TREE)", (0, 229, 255)),
        (315, 220, "MEM0 (AUTO-EXTRACTION)", (223, 186, 107)),
    ]

    for angle_deg, dist, label, color in nodes:
        rad = math.radians(angle_deg)
        nx = int(center_x + dist * math.cos(rad) * 1.35)
        ny = int(center_y + dist * math.sin(rad) * 0.95)
        
        # Line connecting to center
        glow_draw.line([(center_x, center_y), (nx, ny)], fill=(*color, 140), width=2)
        
        # Outer Node circle
        glow_draw.ellipse([nx - 18, ny - 18, nx + 18, ny + 18], fill=(10, 18, 25, 240), outline=(*color, 255), width=2)
        glow_draw.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(255, 255, 255, 255))
        
        # Box for label
        bw, bh = 145, 26
        bx = nx - bw // 2
        by = ny + 22 if ny < center_y + 100 else ny - 38
        glow_draw.rectangle([bx, by, bx + bw, by + bh], fill=(8, 14, 20, 230), outline=(*color, 160), width=1)

    # 4. Floating HUD badges
    glow_draw.rectangle([410, 160, 790, 198], fill=(10, 20, 30, 210), outline=(0, 229, 255, 200), width=1)
    glow_draw.rectangle([370, 720, 830, 760], fill=(25, 20, 10, 220), outline=(223, 186, 107, 200), width=1)

    # Composite glow and base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    final_draw = ImageDraw.Draw(im)
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 15)
        font_node = ImageFont.truetype("arialbd.ttf", 11)
        font_core = ImageFont.truetype("arialbd.ttf", 13)
    except:
        font_badge = ImageFont.load_default()
        font_node = font_badge
        font_core = font_badge
        
    final_draw.text((600, 179), "HERMES AGENT  •  ARQUITETURA DE MEMÓRIA", fill=(0, 229, 255), font=font_badge, anchor="mm")
    final_draw.text((600, 740), "OS 9 TIPOS DE MEMÓRIA  •  INTELIGÊNCIA AGÊNTICA", fill=(223, 186, 107), font=font_badge, anchor="mm")
    final_draw.text((600, 430), "HERMES\nNEXUS", fill=(255, 255, 255), font=font_core, anchor="mm", align="center")

    for angle_deg, dist, label, color in nodes:
        rad = math.radians(angle_deg)
        nx = int(center_x + dist * math.cos(rad) * 1.35)
        ny = int(center_y + dist * math.sin(rad) * 0.95)
        by = ny + 35 if ny < center_y + 100 else ny - 25
        final_draw.text((nx, by), label, fill=(240, 245, 255), font=font_node, anchor="mm")

    # Save final image
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "como-o-hermes-agent-lembra-de-tudo-os-9-tipos-de-memoria-ia.jpg")
    
    im.save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa gerada com sucesso em: {out_path}")
    return True

if __name__ == "__main__":
    create_memory_cover()
