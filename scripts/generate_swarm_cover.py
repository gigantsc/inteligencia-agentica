import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_swarm_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Specialist Agents & Data Conduits)
    for r in range(580, 0, -15):
        alpha = int(45 * (1 - r / 580))
        glow_draw.ellipse([ -150 - r, 180 - r, 420 + r, 720 + r ], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Hierarchical Leadership & Executive Governance)
    for r in range(580, 0, -15):
        alpha = int(45 * (1 - r / 580))
        glow_draw.ellipse([ 780 - r, 180 - r, 1350 + r, 720 + r ], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid
    for y in range(670, height, 24):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 200, 240, alpha), width=1)
    for x in range(70, width, 70):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.7), height)], fill=(0, 200, 240, 18), width=1)
        
    # 2. Classical Architecture: Grand Hellenic Colonnade & Assembly Hall
    # Far Left Column
    col1_x = 110
    col_w = 55
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(120, 220, 250, 50), width=2)
    glow_draw.rectangle([col1_x - 12, 120, col1_x + col_w + 12, 145], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)
    glow_draw.rectangle([col1_x - 15, 760, col1_x + col_w + 15, 795], fill=(15, 40, 55, 180), outline=(0, 229, 255, 190), width=2)

    # Far Right Column
    col2_x = 1030
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 140), (fl_x, 780)], fill=(230, 200, 120, 50), width=2)
    glow_draw.rectangle([col2_x - 12, 120, col2_x + col_w + 12, 145], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)
    glow_draw.rectangle([col2_x - 15, 760, col2_x + col_w + 15, 795], fill=(45, 38, 18, 180), outline=(223, 186, 107, 190), width=2)

    # Grand Hellenic Archway / Pediment
    glow_draw.polygon([(600, 60), (90, 135), (1110, 135)], outline=(180, 210, 230, 120), width=2)
    glow_draw.line([(90, 135), (1110, 135)], fill=(0, 229, 255, 150), width=2)

    # 3. Central Assembly: The Marble Council of Swarm Agents
    # Center: Hermes Leader / Orchestrator
    cx, cy = 600, 390
    
    # Leader Halo / Orchestration Field
    for r in range(160, 0, -10):
        alpha = int(40 * (1 - r / 160))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(223, 186, 107, alpha))

    # Hermes Bust (Leader - Center)
    # Head & Winged Helmet
    glow_draw.ellipse([cx - 55, cy - 150, cx + 55, cy - 40], fill=(225, 230, 240, 245), outline=(223, 186, 107, 255), width=2)
    # Wing Left (Cyan)
    glow_draw.polygon([(cx - 40, cy - 130), (cx - 105, cy - 180), (cx - 90, cy - 110), (cx - 45, cy - 100)], fill=(170, 240, 255, 230), outline=(0, 229, 255, 255), width=2)
    # Wing Right (Gold)
    glow_draw.polygon([(cx + 40, cy - 130), (cx + 105, cy - 180), (cx + 90, cy - 110), (cx + 45, cy - 100)], fill=(255, 230, 170, 230), outline=(223, 186, 107, 255), width=2)
    # Laurel Crown / Caduceus Crest
    glow_draw.arc([cx - 35, cy - 175, cx + 35, cy - 135], start=180, end=0, fill=(223, 186, 107, 255), width=3)
    # Shoulders / Toga
    glow_draw.polygon([(cx, cy - 40), (cx - 115, cy + 65), (cx - 85, cy + 150), (cx, cy + 130)], fill=(160, 215, 235, 240), outline=(0, 229, 255, 200), width=2)
    glow_draw.polygon([(cx, cy - 40), (cx + 115, cy + 65), (cx + 85, cy + 150), (cx, cy + 130)], fill=(240, 210, 150, 240), outline=(223, 186, 107, 200), width=2)
    # Leader Core Emblem (Orchestration Hub)
    glow_draw.ellipse([cx - 28, cy + 20, cx + 28, cy + 76], fill=(12, 24, 36, 250), outline=(223, 186, 107, 255), width=3)
    glow_draw.polygon([(cx, cy + 30), (cx + 16, cy + 50), (cx, cy + 68), (cx - 16, cy + 50)], fill=(0, 229, 255, 255), outline=(255, 255, 255, 255), width=1)

    # 4. Flanking Specialist Agents (Marble Busts)
    # Left Specialist: Athena / Market Intelligence Agent
    lx, ly = 320, 440
    for r in range(110, 0, -10):
        alpha = int(30 * (1 - r / 110))
        glow_draw.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(0, 229, 255, alpha))
    # Helmet & Head
    glow_draw.ellipse([lx - 42, ly - 120, lx + 42, ly - 30], fill=(200, 225, 240, 235), outline=(0, 229, 255, 230), width=2)
    # Corinthian Helmet Crest
    glow_draw.polygon([(lx, ly - 155), (lx - 25, ly - 120), (lx + 25, ly - 120)], fill=(0, 229, 255, 220), outline=(255, 255, 255, 240), width=2)
    # Shoulders
    glow_draw.polygon([(lx - 85, ly + 50), (lx + 85, ly + 50), (lx + 60, ly + 120), (lx - 60, ly + 120)], fill=(140, 195, 220, 220), outline=(0, 229, 255, 180), width=2)
    # Badge (Research Node)
    glow_draw.ellipse([lx - 20, ly + 10, lx + 20, ly + 50], fill=(10, 30, 45, 240), outline=(0, 229, 255, 255), width=2)
    glow_draw.text((lx, ly + 30), "DATA", fill=(0, 229, 255, 255), anchor="mm")

    # Right Specialist: Hephaestus / DevOps & Code Agent
    rx, ry = 880, 440
    for r in range(110, 0, -10):
        alpha = int(30 * (1 - r / 110))
        glow_draw.ellipse([rx - r, ry - r, rx + r, ry + r], fill=(223, 186, 107, alpha))
    # Head & Crown
    glow_draw.ellipse([rx - 42, ry - 120, rx + 42, ry - 30], fill=(235, 225, 205, 235), outline=(223, 186, 107, 230), width=2)
    # Helmet Crest
    glow_draw.polygon([(rx, ry - 150), (rx - 22, ry - 120), (rx + 22, ry - 120)], fill=(223, 186, 107, 220), outline=(255, 255, 255, 240), width=2)
    # Shoulders
    glow_draw.polygon([(rx - 85, ly + 50), (rx + 85, ly + 50), (rx + 60, ly + 120), (rx - 60, ly + 120)], fill=(215, 190, 140, 220), outline=(223, 186, 107, 180), width=2)
    # Badge (Code Node)
    glow_draw.ellipse([rx - 20, ry + 10, rx + 20, ry + 50], fill=(45, 35, 15, 240), outline=(223, 186, 107, 255), width=2)
    glow_draw.text((rx, ry + 30), "DEV", fill=(223, 186, 107, 255), anchor="mm")

    # 5. Neural Swarm Conduits, A2A Bus & Delegation Filaments
    # Flow lines from Leader to Specialists
    glow_draw.line([(cx - 70, cy + 50), (lx + 60, ly + 20)], fill=(0, 229, 255, 220), width=3)
    glow_draw.line([(cx + 70, cy + 50), (rx - 60, ry + 20)], fill=(223, 186, 107, 220), width=3)
    
    # Inter-agent sync bus (Bottom connection between specialists)
    glow_draw.line([(lx + 40, ly + 100), (cx - 40, cy + 120)], fill=(0, 200, 240, 160), width=2)
    glow_draw.line([(cx + 40, cy + 120), (rx - 40, ry + 100)], fill=(220, 180, 100, 160), width=2)

    # Floating Subagent Tasks / Data Nodes
    node_positions = [
        (460, 270, "TASK: EXTRACT", (0, 229, 255)),
        (740, 270, "TASK: ANALYZE", (223, 186, 107)),
        (330, 610, "SUBAGENT 01", (0, 229, 255)),
        (600, 630, "QA & COMPLIANCE", (255, 255, 255)),
        (870, 610, "SUBAGENT 02", (223, 186, 107))
    ]
    for nx, ny, label, col in node_positions:
        glow_draw.rectangle([nx - 70, ny - 16, nx + 70, ny + 16], fill=(12, 20, 30, 220), outline=col, width=1)
        glow_draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=col)
        # Pulse connection
        glow_draw.line([(nx, ny), (cx if "TASK" in label or "QA" in label else (lx if "01" in label else rx), cy if "TASK" in label else 560)], fill=col + (100,), width=1)

    # 6. Executive Header & Subtitle Typography
    try:
        font_main = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 20)
        font_tag = ImageFont.truetype("arial.ttf", 16)
        font_node = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_node = ImageFont.load_default()

    # Draw node labels
    for nx, ny, label, col in node_positions:
        glow_draw.text((nx, ny - 1), label, fill=col, font=font_node, anchor="mm")

    # Upper Badge
    glow_draw.rectangle([cx - 190, 160, cx + 190, 195], fill=(12, 24, 36, 220), outline=(0, 229, 255, 180), width=1)
    glow_draw.text((cx, 177), "HERMES MULTI-AGENT SWARM FACTORY", fill=(0, 229, 255, 240), font=font_tag, anchor="mm")

    # Bottom Title Text
    glow_draw.text((cx, 825), "FÁBRICA DE SWARMS & MULTI-AGENTES", fill=(255, 255, 255, 250), font=font_main, anchor="mm")
    glow_draw.text((cx, 865), "Orquestração Hierárquica • Isolamento de Tarefas • Protocolo A2A", fill=(223, 186, 107, 220), font=font_sub, anchor="mm")

    # Composite layers with slight gaussian blur for high-end glow
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(1.2))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Save image
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "fabrica-de-swarms-orquestracao-multi-agentes.jpg")
    final_im.convert("RGB").save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa salva com sucesso em: {out_path} ({width}x{height}px)")

if __name__ == "__main__":
    create_swarm_cover()