import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_devops_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Telemetria, Linux Terminals, Cloud Streams #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Infraestrutura Segura, Escudo de Auto-Cura #DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid (perspective grid)
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore com Conduítes Digitais)
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

    # Frontão Clássico Superior
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)
    
    # 3. PAINÉIS LATERAIS DE INFRAESTRUTURA & TELEMETRIA DEVOPS
    # Lado Esquerdo: Terminal Linux / Docker Telemetry (Ciano)
    glow_draw.rectangle([135, 220, 225, 480], fill=(8, 22, 32, 160), outline=(0, 229, 255, 180), width=1)
    for ly in range(240, 470, 18):
        lw = 40 + (ly * 17) % 45
        glow_draw.line([(145, ly), (145 + lw, ly)], fill=(0, 229, 255, 140), width=2)
        
    # Lado Direito: Server Racks / Health Metrics (Ouro)
    glow_draw.rectangle([975, 220, 1065, 480], fill=(30, 25, 12, 160), outline=(223, 186, 107, 180), width=1)
    for ly in range(240, 470, 24):
        glow_draw.rectangle([985, ly, 1055, ly + 14], fill=(45, 38, 16, 180), outline=(223, 186, 107, 160), width=1)
        # Server status LEDs
        glow_draw.ellipse([990, ly + 4, 996, ly + 10], fill=(0, 255, 180, 220))
        glow_draw.ellipse([1002, ly + 4, 1008, ly + 10], fill=(223, 186, 107, 220))
        glow_draw.ellipse([1014, ly + 4, 1020, ly + 10], fill=(0, 229, 255, 220))
    
    # 4. CENTRO: BUSTO DE HERMES COM CAPACETE ALADO + ANÉIS DE AUTO-CURA & TELEMETRIA
    cx, cy = 600, 380
    
    # Halo de anéis concêntricos de telemetria e auto-cura (Docker / Infra Rotação)
    for r in [280, 230, 180, 130]:
        alpha_ring = int(140 * (1 - r / 320))
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=100, end=260, fill=(0, 229, 255, alpha_ring), width=2)
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=280, end=80, fill=(223, 186, 107, alpha_ring), width=2)

    # Nós orbitais de telemetria nos anéis
    for ang in [30, 75, 120, 165, 210, 255, 300, 345]:
        rad = math.radians(ang)
        nx = int(cx + 230 * math.cos(rad))
        ny = int(cy + 230 * math.sin(rad))
        color = (0, 229, 255, 200) if math.cos(rad) < 0 else (223, 186, 107, 200)
        glow_draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=color)

    # Busto de Hermes no centro superior
    head_y = cy - 70
    
    # Halo atrás da cabeça
    for r in range(95, 10, -5):
        glow_draw.ellipse([cx - r, head_y - r, cx + r, head_y + r], fill=(15, 25, 35, 170), outline=(0, 229, 255, int(110 * (1 - r / 95))), width=1)
        
    # Cabeça e Rosto em Mármore Estilizado
    glow_draw.ellipse([cx - 45, head_y - 55, cx + 45, head_y + 45], fill=(22, 28, 38, 240), outline=(200, 220, 240, 200), width=2)
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=90, end=270, fill=(0, 229, 255, 255), width=3)
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=270, end=90, fill=(223, 186, 107, 255), width=3)
    
    # Elmo Alado de Hermes
    wing_left = [(cx - 35, head_y - 45), (cx - 110, head_y - 115), (cx - 75, head_y - 50), (cx - 100, head_y - 30), (cx - 40, head_y - 20)]
    glow_draw.polygon(wing_left, fill=(10, 45, 60, 220), outline=(0, 229, 255, 255))
    glow_draw.line([(cx - 35, head_y - 45), (cx - 105, head_y - 110)], fill=(255, 255, 255, 220), width=2)
    
    wing_right = [(cx + 35, head_y - 45), (cx + 110, head_y - 115), (cx + 75, head_y - 50), (cx + 100, head_y - 30), (cx + 40, head_y - 20)]
    glow_draw.polygon(wing_right, fill=(55, 45, 18, 220), outline=(223, 186, 107, 255))
    glow_draw.line([(cx + 35, head_y - 45), (cx + 110, head_y - 110)], fill=(255, 255, 255, 220), width=2)

    # Ombro e Púlpito do Busto
    chest = [(cx - 85, cy + 30), (cx + 85, cy + 30), (cx + 50, head_y + 45), (cx - 50, head_y + 45)]
    glow_draw.polygon(chest, fill=(20, 26, 36, 230), outline=(180, 210, 230, 160))
    # Pedestal de Mármore
    glow_draw.rectangle([cx - 55, cy + 30, cx + 55, cy + 95], fill=(16, 22, 30, 240), outline=(180, 210, 230, 180), width=2)
    glow_draw.rectangle([cx - 75, cy + 95, cx + 75, cy + 120], fill=(22, 28, 38, 250), outline=(0, 229, 255, 200), width=2)

    # 5. ÍCONE DE DEVOPS / AUTO-CURA NO PEDESTAL (Símbolo do Infinito & Container)
    # Infinito DevOps estilizado
    inf_y = cy + 62
    glow_draw.arc([cx - 42, inf_y - 16, cx - 6, inf_y + 16], start=45, end=315, fill=(0, 229, 255, 255), width=3)
    glow_draw.arc([cx + 6, inf_y - 16, cx + 42, inf_y + 16], start=225, end=135, fill=(223, 186, 107, 255), width=3)
    glow_draw.line([(cx - 18, inf_y - 11), (cx + 18, inf_y + 11)], fill=(180, 240, 255, 230), width=2)
    glow_draw.line([(cx - 18, inf_y + 11), (cx + 18, inf_y - 11)], fill=(255, 235, 180, 230), width=2)

    # 6. FILAMENTOS NEURAIS DE INFRAESTRUTURA LIGANDO O AGENTE AOS SERVIDORES
    for sy in [260, 320, 380, 440]:
        glow_draw.line([(cx - 75, cy + 40), (225, sy)], fill=(0, 229, 255, 75), width=2)
        glow_draw.line([(cx + 75, cy + 40), (975, sy)], fill=(223, 186, 107, 75), width=2)

    # 7. BLUR & COMPOSIÇÃO FINAL
    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(1.0))
    im.paste(glow_blurred, (0, 0), glow_blurred)
    
    # Sharp overlay layer
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # 8. TIPOGRAFIA EXECUTIVA DE RODAPÉ
    draw = ImageDraw.Draw(im)
    
    # Box do Título Inferior
    box_w, box_h = 920, 125
    bx = (width - box_w) // 2
    by = 735
    
    draw.rectangle([bx, by, bx + box_w, by + box_h], fill=(7, 10, 15), outline=(0, 229, 255), width=2)
    draw.rectangle([bx + 4, by + 4, bx + box_w - 4, by + box_h - 4], outline=(223, 186, 107), width=1)
    
    # Textos
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 34)
        font_sub = ImageFont.truetype("arial.ttf", 18)
        font_tag = ImageFont.truetype("arialbd.ttf", 15)
    except Exception:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    tag_text = "INFRAESTRUTURA RESILIENTE 24/7 • SELF-HEALING DEVOPS • HERMES AGENT"
    title_text = "AGENTE DEVOPS AUTÔNOMO: AUTO-CURA NA NUVEM"
    sub_text = "Monitoramento Ativo, Diagnóstico Semântico e Recuperação de Servidores Sem Plantão Humano"
    
    draw.text((bx + 35, by + 16), tag_text, fill=(223, 186, 107), font=font_tag)
    draw.text((bx + 35, by + 42), title_text, fill=(255, 255, 255), font=font_large)
    draw.text((bx + 35, by + 86), sub_text, fill=(0, 229, 255), font=font_sub)
    
    # Salvar Imagem
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "agente-devops-auto-recuperacao-infraestrutura.jpg")
    im.save(out_path, quality=95)
    print(f"✅ Capa DevOps gerada com sucesso em: {out_path} (Tamanho: {im.size})")

if __name__ == "__main__":
    create_devops_cover()
