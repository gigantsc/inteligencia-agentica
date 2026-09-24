import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_webhooks_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Incoming Streams / Real-time Webhooks)
    for r in range(580, 0, -12):
        alpha = int(45 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Autonomous Execution / Dispatched Actions)
    for r in range(580, 0, -12):
        alpha = int(45 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid (perspective grid)
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore)
    # Coluna Externa Esquerda (Ciano)
    col1_x = 80
    col_w = 52
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(90, 215, 245, 60), width=2)
    glow_draw.rectangle([col1_x - 14, 90, col1_x + col_w + 14, 120], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 740, col1_x + col_w + 16, 775], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Externa Direita (Ouro)
    col2_x = 1068
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(215, 190, 115, 60), width=2)
    glow_draw.rectangle([col2_x - 14, 90, col2_x + col_w + 14, 120], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 740, col2_x + col_w + 16, 775], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)

    # Coluna Interna Esquerda (Ciano)
    col3_x = 230
    col3_w = 40
    for fl in range(4):
        fl_x = col3_x + fl * 10
        glow_draw.line([(fl_x, 130), (fl_x, 730)], fill=(80, 200, 230, 45), width=2)
    glow_draw.rectangle([col3_x - 10, 115, col3_x + col3_w + 10, 140], fill=(10, 30, 42, 180), outline=(0, 210, 240, 170), width=2)
    glow_draw.rectangle([col3_x - 12, 715, col3_x + col3_w + 12, 745], fill=(10, 30, 42, 180), outline=(0, 210, 240, 170), width=2)

    # Coluna Interna Direita (Ouro)
    col4_x = 930
    for fl in range(4):
        fl_x = col4_x + fl * 10
        glow_draw.line([(fl_x, 130), (fl_x, 730)], fill=(205, 180, 105, 45), width=2)
    glow_draw.rectangle([col4_x - 10, 115, col4_x + col3_w + 10, 140], fill=(36, 30, 12, 180), outline=(215, 180, 105, 170), width=2)
    glow_draw.rectangle([col4_x - 12, 715, col4_x + col3_w + 12, 745], fill=(36, 30, 12, 180), outline=(215, 180, 105, 170), width=2)

    # Grande Frontão / Pediment Clássico Superior
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    # Viga horizontal do frontão
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)
    
    # 3. NÓ CENTRAL DE EVENTOS & RELÂMPAGOS DE WEBHOOKS (Event-Driven Architecture)
    cx, cy = 600, 400
    
    # Círculos concêntricos do barramento de eventos (Event Bus Hub)
    for r in [220, 180, 140, 100, 60]:
        alpha_ring = int(140 * (1 - r / 260))
        # Left half cyan, right half gold
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270, fill=(0, 229, 255, alpha_ring), width=2)
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=270, end=90, fill=(223, 186, 107, alpha_ring), width=2)

    # 4. BUSTO ESCULPIDO DE HERMES NO CENTRO
    # Cabeça e Elmo Alado
    head_y = cy - 70
    
    # Halo de energia atrás da cabeça
    for r in range(90, 10, -5):
        glow_draw.ellipse([cx - r, head_y - r, cx + r, head_y + r], fill=(15, 25, 35, 180), outline=(0, 229, 255, int(120 * (1 - r / 90))), width=1)
    
    # Busto / Cabeça (Mármore estilizado)
    glow_draw.ellipse([cx - 45, head_y - 55, cx + 45, head_y + 45], fill=(22, 28, 38, 240), outline=(200, 220, 240, 200), width=2)
    # Rosto / Perfil Clássico com Split-lighting
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=90, end=270, fill=(0, 229, 255, 255), width=3)
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=270, end=90, fill=(223, 186, 107, 255), width=3)
    
    # Elmo Alado de Hermes (Winged Helmet)
    # Asa Esquerda (Ciano)
    wing_left = [(cx - 35, head_y - 45), (cx - 110, head_y - 115), (cx - 75, head_y - 50), (cx - 100, head_y - 30), (cx - 40, head_y - 20)]
    glow_draw.polygon(wing_left, fill=(10, 45, 60, 220), outline=(0, 229, 255, 255))
    glow_draw.line([(cx - 35, head_y - 45), (cx - 105, head_y - 110)], fill=(255, 255, 255, 220), width=2)
    
    # Asa Direita (Ouro)
    wing_right = [(cx + 35, head_y - 45), (cx + 110, head_y - 115), (cx + 75, head_y - 50), (cx + 100, head_y - 30), (cx + 40, head_y - 20)]
    glow_draw.polygon(wing_right, fill=(50, 40, 15, 220), outline=(223, 186, 107, 255))
    glow_draw.line([(cx + 35, head_y - 45), (cx + 105, head_y - 110)], fill=(255, 245, 200, 220), width=2)

    # Ombros e Tronco de Mármore (Drapeado clássico)
    torso = [(cx - 110, head_y + 160), (cx - 65, head_y + 40), (cx + 65, head_y + 40), (cx + 110, head_y + 160), (cx, head_y + 190)]
    glow_draw.polygon(torso, fill=(18, 22, 30, 245), outline=(180, 200, 225, 180), width=2)
    # Linhas de sombra clássica no peito
    glow_draw.line([(cx, head_y + 40), (cx, head_y + 185)], fill=(120, 150, 180, 120), width=2)
    glow_draw.line([(cx - 70, head_y + 120), (cx, head_y + 150)], fill=(0, 229, 255, 140), width=2)
    glow_draw.line([(cx + 70, head_y + 120), (cx, head_y + 150)], fill=(223, 186, 107, 140), width=2)

    # Pedestal / Base da estátua
    glow_draw.rectangle([cx - 95, head_y + 190, cx + 95, head_y + 245], fill=(14, 18, 25, 240), outline=(150, 180, 210, 180), width=2)
    glow_draw.rectangle([cx - 120, head_y + 245, cx + 120, head_y + 270], fill=(10, 14, 20, 250), outline=(180, 210, 235, 200), width=2)

    # 5. RELÂMPAGOS HOLOGRÁFICOS & CONDUÍTES DE EVENTOS (Incoming Webhooks & Dispatched Actions)
    # Feixes de entrada à esquerda (Incoming HTTP Webhooks - Cyan)
    webhook_sources = [
        ("STRIPE", 160, 240),
        ("HOTMART", 190, 360),
        ("GITHUB", 170, 480),
        ("TYPEFORM", 210, 600),
    ]
    for name, sx, sy in webhook_sources:
        # Nodo de origem
        glow_draw.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(5, 30, 45, 230), outline=(0, 229, 255, 240), width=2)
        glow_draw.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(0, 229, 255, 255))
        
        # Relâmpago / Raio de dados conectando ao núcleo de Hermes
        mid_x = (sx + cx - 90) // 2 + (sy % 30) - 15
        mid_y = (sy + cy - 20) // 2 - 20
        # Multi-segment lightning
        glow_draw.line([(sx + 18, sy), (mid_x - 20, mid_y + 10), (mid_x + 15, mid_y - 15), (cx - 95, cy - 30)], fill=(0, 229, 255, 220), width=2)
        # Glow around lightning
        glow_draw.line([(sx + 18, sy), (mid_x - 20, mid_y + 10), (mid_x + 15, mid_y - 15), (cx - 95, cy - 30)], fill=(150, 240, 255, 100), width=5)

    # Feixes de saída à direita (Dispatched Autonomous Actions - Gold)
    action_targets = [
        ("TELEGRAM", 1040, 240),
        ("WHATSAPP", 1010, 360),
        ("SUBAGENT", 1030, 480),
        ("DATABASE", 990, 600),
    ]
    for name, tx, ty in action_targets:
        # Nodo de destino
        glow_draw.ellipse([tx - 18, ty - 18, tx + 18, ty + 18], fill=(45, 35, 10, 230), outline=(223, 186, 107, 240), width=2)
        glow_draw.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=(223, 186, 107, 255))
        
        # Relâmpago dourado conectando o núcleo ao destino
        mid_x = (cx + 90 + tx) // 2 + (ty % 30) - 15
        mid_y = (cy - 20 + ty) // 2 - 20
        glow_draw.line([(cx + 95, cy - 30), (mid_x - 15, mid_y - 15), (mid_x + 20, mid_y + 10), (tx - 18, ty)], fill=(223, 186, 107, 220), width=2)
        glow_draw.line([(cx + 95, cy - 30), (mid_x - 15, mid_y - 15), (mid_x + 20, mid_y + 10), (tx - 18, ty)], fill=(255, 235, 170, 100), width=5)

    # 6. GLOW DE NÓS DE BARRAMENTO ORBITAIS
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    for i, ang in enumerate(angles):
        rad = math.radians(ang)
        orbit_r = 180
        nx = int(cx + orbit_r * math.cos(rad))
        ny = int(cy + orbit_r * math.sin(rad))
        c = (0, 229, 255) if nx < cx else (223, 186, 107)
        glow_draw.ellipse([nx - 7, ny - 7, nx + 7, ny + 7], fill=(*c, 240), outline=(255, 255, 255, 200), width=1)
        # Pulsing radar ring around node
        glow_draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], outline=(*c, 100), width=1)

    # 7. PARTICULAS DE LUZ E POEIRA DIGITAL
    for i in range(120):
        seed_x = (i * 137 + 43) % width
        seed_y = (i * 211 + 79) % (height - 200) + 80
        p_color = (0, 229, 255) if seed_x < 600 else (223, 186, 107)
        p_size = (i % 3) + 1
        p_alpha = 70 + (i % 120)
        glow_draw.ellipse([seed_x, seed_y, seed_x + p_size, seed_y + p_size], fill=(*p_color, p_alpha))

    # 8. MISTURA E COMPOSIÇÃO FINAL
    # Suavização do glow layer
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))
    im.paste(blurred_glow, (0, 0), blurred_glow)
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Salvar imagem
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "webhooks-agentes-ia-arquitetura-orientada-a-eventos.jpg")
    im.save(out_path, "JPEG", quality=95)
    print(f"✅ Capa gerada com sucesso em: {out_path}")
    return out_path

if __name__ == "__main__":
    create_webhooks_cover()
