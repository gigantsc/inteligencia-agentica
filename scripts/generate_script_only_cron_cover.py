import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_script_only_cron_cover():
    width, height = 1200, 912
    
    # 1. Base obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient wash: Left Cyan (#00E5FF) and Right Amber-Gold (#DFBA6B)
    for r in range(580, 0, -14):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-150 - r, 180 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    for r in range(580, 0, -14):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 180 - r, 1350 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor perspective grid (from horizon y=660 to height)
    for y in range(660, height, 18):
        alpha = int(42 * ((y - 660) / (height - 660)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 215, 245, alpha), width=1)
    for x in range(40, width, 55):
        glow_draw.line([(x, 660), (int(600 + (x - 600) * 1.8), height)], fill=(0, 215, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunata de Mármore e Frontão)
    # Coluna Esquerda (Mármore Ciano / Watchdogs e Telemetria)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Custo Zero & hermes send)
    col2_x = 1070
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(215, 190, 115, 65), width=2)
    glow_draw.rectangle([col2_x - 14, 85, col2_x + col_w + 14, 115], fill=(42, 36, 16, 220), outline=(223, 186, 107, 220), width=2)
    glow_draw.rectangle([col2_x - 16, 750, col2_x + col_w + 16, 785], fill=(42, 36, 16, 220), outline=(223, 186, 107, 220), width=2)

    # Frontão Clássico Superior (Triangular Pediment)
    glow_draw.polygon([(600, 30), (55, 100), (1145, 100)], outline=(170, 205, 225, 120), width=2)
    glow_draw.polygon([(600, 45), (85, 100), (1115, 100)], outline=(210, 185, 115, 100), width=1)
    glow_draw.rectangle([55, 100, 1145, 115], fill=(15, 18, 26, 180), outline=(160, 195, 215, 110), width=1)
    
    # Inscrição clássica no frontão: HERMES AGENT // SCRIPT-ONLY CRON & HERMES SEND
    glow_draw.rectangle([250, 92, 950, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(270, 102), (930, 102)], fill=(223, 186, 107), width=2)

    # 3. PEDESTAL NEOCLÁSSICO CENTRAL DE MÁRMORE (The Base of Deterministic Execution)
    base_x, base_y = 600, 680
    glow_draw.rectangle([base_x - 180, base_y, base_x + 180, base_y + 40], fill=(18, 26, 38, 230), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([base_x - 210, base_y + 40, base_x + 210, base_y + 70], fill=(12, 18, 28, 240), outline=(0, 229, 255), width=2)
    
    # Rótulo de Mármore no Pedestal: "DETERMINISTIC WATCHDOGS // ZERO TOKEN OVERHEAD"
    glow_draw.rectangle([base_x - 160, base_y + 10, base_x + 160, base_y + 30], fill=(5, 10, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(base_x - 140, base_y + 20), (base_x + 140, base_y + 20)], fill=(223, 186, 107), width=2)

    # 4. O CRONÔMETRO CELESTE / ASTROLÁBIO DO SCHEDULER CENTRAL
    cx, cy = 600, 390
    
    # Anéis Concéntricos do Scheduler (Glow Orbital)
    for r in range(220, 50, -10):
        alpha = int(30 * (1 - r / 220))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 229, 255, alpha))
    for r in range(170, 50, -10):
        alpha = int(28 * (1 - r / 170))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(223, 186, 107, alpha))
        
    # Anel Externo do Relógio Cósmico (Ciano) com marcas de minutos
    glow_draw.ellipse([cx - 215, cy - 215, cx + 215, cy + 215], outline=(0, 229, 255, 190), width=2)
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        r_out = 215
        r_in = 202 if deg % 30 == 0 else 208
        x1 = cx + int(r_out * math.cos(rad))
        y1 = cy + int(r_out * math.sin(rad))
        x2 = cx + int(r_in * math.cos(rad))
        y2 = cy + int(r_in * math.sin(rad))
        glow_draw.line([(x1, y1), (x2, y2)], fill=(0, 229, 255, 230), width=2 if deg % 30 == 0 else 1)
        
    # Anel Interno Dourado com ponteiros astronômicos do Cron
    glow_draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=(223, 186, 107, 210), width=2)
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        px = cx + int(150 * math.cos(rad))
        py = cy + int(150 * math.sin(rad))
        glow_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(223, 186, 107), outline=(255, 255, 255))
        
    # Terminal Holográfico Central (The Watchdog Core: Bash/Python Execution Engine)
    card_w, card_h = 320, 200
    card_x1, card_y1 = cx - card_w // 2, cy - card_h // 2
    card_x2, card_y2 = cx + card_w // 2, cy + card_h // 2
    
    glow_draw.rectangle([card_x1, card_y1, card_x2, card_y2], fill=(8, 14, 24, 235), outline=(0, 229, 255, 240), width=2)
    glow_draw.rectangle([card_x1 + 4, card_y1 + 4, card_x2 - 4, card_y1 + 28], fill=(15, 25, 40), outline=(223, 186, 107, 180), width=1)
    
    # Botões de janela do terminal
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        glow_draw.ellipse([card_x1 + 12 + i * 16, card_y1 + 10, card_x1 + 22 + i * 16, card_y1 + 20], fill=col)
        
    # Linhas de código esquemáticas dentro do terminal (no_agent=True & hermes send)
    code_lines = [
        ((card_x1 + 20, card_y1 + 44), (card_x1 + 140, card_y1 + 44), (0, 229, 255)),   # #!/usr/bin/env bash
        ((card_x1 + 20, card_y1 + 64), (card_x1 + 220, card_y1 + 64), (223, 186, 107)), # RAM_PCT=$(free | awk ...)
        ((card_x1 + 20, card_y1 + 84), (card_x1 + 180, card_y1 + 84), (200, 225, 240)), # if [ "$RAM_PCT" -ge 85 ]; then
        ((card_x1 + 40, card_y1 + 104), (card_x1 + 260, card_y1 + 104), (0, 229, 255)), #   echo "ALERTA RAM ${RAM_PCT}%"
        ((card_x1 + 20, card_y1 + 124), (card_x1 + 60, card_y1 + 124), (200, 225, 240)), # fi
        ((card_x1 + 20, card_y1 + 148), (card_x1 + 250, card_y1 + 148), (39, 201, 63)),  # [EXIT 0: SILENT WHEN EMPTY]
        ((card_x1 + 20, card_y1 + 172), (card_x1 + 210, card_y1 + 172), (223, 186, 107)) # 0 TOKENS // ZERO API SPEND
    ]
    for start, end, col in code_lines:
        glow_draw.line([start, end], fill=col, width=3)

    # 5. SATÉLITES TELEMÉTRICOS DE MONITORAMENTO (RAM, DISK, DOCKER, HERMES SEND)
    satellites = [
        {"x": cx - 290, "y": cy - 100, "label": "RAM WATCHDOG", "color": (0, 229, 255), "icon": "ram"},
        {"x": cx - 290, "y": cy + 90,  "label": "DISK STORAGE", "color": (0, 229, 255), "icon": "disk"},
        {"x": cx + 290, "y": cy - 100, "label": "DOCKER HEALTH", "color": (223, 186, 107), "icon": "docker"},
        {"x": cx + 290, "y": cy + 90,  "label": "HERMES SEND CLI", "color": (223, 186, 107), "icon": "send"}
    ]
    
    for sat in satellites:
        sx, sy = sat["x"], sat["y"]
        scol = sat["color"]
        
        # Conexão de fibra óptica ao núcleo central
        glow_draw.line([(sx, sy), (cx, cy)], fill=(scol[0], scol[1], scol[2], 70), width=2)
        
        # Glow do satélite
        for r in range(45, 10, -5):
            glow_draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(scol[0], scol[1], scol[2], int(25 * (1 - r / 45))))
            
        glow_draw.ellipse([sx - 36, sy - 36, sx + 36, sy + 36], fill=(10, 16, 26), outline=scol, width=2)
        
        # Ícones vetoriais nos satélites
        if sat["icon"] == "ram":
            # Chip de RAM
            glow_draw.rectangle([sx - 18, sy - 14, sx + 18, sy + 14], outline=scol, width=2)
            glow_draw.line([(sx - 10, sy - 18), (sx - 10, sy - 14)], fill=scol, width=2)
            glow_draw.line([(sx, sy - 18), (sx, sy - 14)], fill=scol, width=2)
            glow_draw.line([(sx + 10, sy - 18), (sx + 10, sy - 14)], fill=scol, width=2)
            glow_draw.line([(sx - 10, sy + 14), (sx - 10, sy + 18)], fill=scol, width=2)
            glow_draw.line([(sx, sy + 14), (sx, sy + 18)], fill=scol, width=2)
            glow_draw.line([(sx + 10, sy + 14), (sx + 10, sy + 18)], fill=scol, width=2)
        elif sat["icon"] == "disk":
            # Prato de disco rígido
            glow_draw.ellipse([sx - 18, sy - 14, sx + 18, sy + 14], outline=scol, width=2)
            glow_draw.ellipse([sx - 6, sy - 4, sx + 6, sy + 4], fill=scol)
            glow_draw.line([(sx + 6, sy), (sx + 16, sy + 8)], fill=(255, 255, 255), width=2)
        elif sat["icon"] == "docker":
            # Container modular
            glow_draw.rectangle([sx - 16, sy - 12, sx + 16, sy + 12], outline=scol, width=2)
            glow_draw.line([(sx - 16, sy - 4), (sx + 16, sy - 4)], fill=scol, width=1)
            glow_draw.line([(sx - 16, sy + 4), (sx + 16, sy + 4)], fill=scol, width=1)
            glow_draw.line([(sx - 5, sy - 12), (sx - 5, sy + 12)], fill=scol, width=1)
            glow_draw.line([(sx + 5, sy - 12), (sx + 5, sy + 12)], fill=scol, width=1)
        elif sat["icon"] == "send":
            # Avião de papel / Símbolo de despacho universal
            glow_draw.polygon([(sx - 14, sy - 12), (sx + 16, sy), (sx - 14, sy + 12), (sx - 6, sy)], outline=scol, width=2)
            glow_draw.line([(sx - 6, sy), (sx + 16, sy)], fill=(255, 255, 255), width=2)
            
        # Rótulo de apoio abaixo do satélite
        glow_draw.rectangle([sx - 48, sy + 42, sx + 48, sy + 56], fill=(8, 12, 20), outline=scol, width=1)
        glow_draw.line([(sx - 35, sy + 49), (sx + 35, sy + 49)], fill=scol, width=2)

    # 6. FEIXE DE LUZ ASCENDENTE (DISPARO INSTANTÂNEO DE NOTIFICAÇÕES)
    # Feixe ascendente conectando o topo do terminal à cúpula do frontão
    glow_draw.polygon([
        (cx - 30, card_y1),
        (cx + 30, card_y1),
        (cx + 10, 120),
        (cx - 10, 120)
    ], fill=(223, 186, 107, 75))
    glow_draw.line([(cx, card_y1), (cx, 120)], fill=(255, 255, 255, 220), width=2)
    
    # Orbe / Cristal de Conexão no Topo (Universal Messaging Router)
    glow_draw.ellipse([cx - 24, 120 - 24, cx + 24, 120 + 24], fill=(223, 186, 107, 220), outline=(255, 255, 255), width=2)
    glow_draw.ellipse([cx - 10, 120 - 10, cx + 10, 120 + 10], fill=(255, 255, 255))
    
    # Badge Executivo Superior: "ZERO TOKENS // 21+ MESSAGING PLATFORMS"
    glow_draw.rectangle([cx - 150, 150, cx + 150, 182], fill=(12, 22, 34, 240), outline=(223, 186, 107), width=2)
    glow_draw.line([(cx - 130, 166), (cx + 130, 166)], fill=(0, 229, 255), width=2)

    # 7. COMPOSE E SALVA A IMAGEM
    final_img = Image.alpha_composite(im.convert("RGBA"), glow_layer).convert("RGB")
    
    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "script-only-cron-jobs-hermes-send-custo-zero.jpg")
    final_img.save(out_path, format="JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {out_path}")
    return out_path

if __name__ == "__main__":
    create_script_only_cron_cover()
