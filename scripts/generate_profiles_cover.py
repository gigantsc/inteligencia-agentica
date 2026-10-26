import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_profiles_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient wash: Left Cyan (#00E5FF) and Right Amber-Gold (#DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(45 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    for r in range(580, 0, -12):
        alpha = int(45 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor perspective grid
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore Arquiteturais)
    # Coluna Esquerda (Ciano)
    col1_x = 75
    col_w = 48
    for fl in range(5):
        fl_x = col1_x + fl * 10
        glow_draw.line([(fl_x, 100), (fl_x, 760)], fill=(90, 215, 245, 55), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 745, col1_x + col_w + 16, 780], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Direita (Ouro)
    col2_x = 1075
    for fl in range(5):
        fl_x = col2_x + fl * 10
        glow_draw.line([(fl_x, 100), (fl_x, 760)], fill=(215, 190, 115, 55), width=2)
    glow_draw.rectangle([col2_x - 14, 85, col2_x + col_w + 14, 115], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 745, col2_x + col_w + 16, 780], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    
    # Frontão Clássico Superior
    glow_draw.polygon([(600, 30), (60, 95), (1140, 95)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 45), (90, 95), (1110, 95)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 95, 1140, 110], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)
    
    # 3. TRÊS BUSTOS CLÁSSICOS ISOLADOS EM COMPARTIMENTOS BLINDADOS (PERFIS DE AGENTES)
    # Compartimentos / Câmaras Estanques:
    # 1. Perfil Financeiro (Esquerda - Ciano Elétrico)
    # 2. Perfil Central / Executivo (Centro - Dual Ciano / Ouro)
    # 3. Perfil Operacional / Vendas (Direita - Âmbar Ouro)
    
    centers = [
        {"x": 290, "y": 410, "color": (0, 229, 255), "bg": (12, 28, 42), "role": "FINANCEIRO"},
        {"x": 600, "y": 380, "color": (160, 210, 245), "bg": (22, 26, 36), "role": "EXECUTIVO"},
        {"x": 910, "y": 410, "color": (223, 186, 107), "bg": (40, 32, 14), "role": "VENDAS / RH"}
    ]
    
    # Paredes de Vidro / Barreiras Criptográficas entre os perfis
    glow_draw.line([(445, 130), (445, 710)], fill=(0, 229, 255, 90), width=2)
    glow_draw.line([(755, 130), (755, 710)], fill=(223, 186, 107, 90), width=2)
    # Feixes de luz verticais nas barreiras de isolamento
    for by in range(150, 700, 40):
        glow_draw.ellipse([442, by, 448, by + 12], fill=(0, 229, 255, 180))
        glow_draw.ellipse([752, by, 758, by + 12], fill=(223, 186, 107, 180))
    
    for c in centers:
        cx, cy = c["x"], c["y"]
        col = c["color"]
        bg = c["bg"]
        
        # Halo de Isolamento Cilíndrico
        for r in range(130, 20, -10):
            glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 14, 20, int(35 * (1 - r/130))), outline=(col[0], col[1], col[2], int(50 * (1 - r/130))), width=1)
            
        # Pedestal Clássico com Moldura Tecnológica
        ped_y = cy + 140
        glow_draw.rectangle([cx - 70, ped_y, cx + 70, ped_y + 45], fill=bg, outline=col, width=2)
        glow_draw.rectangle([cx - 85, ped_y + 45, cx + 85, ped_y + 65], fill=(10, 12, 18), outline=col, width=2)
        
        # Etiqueta de Identificação do Perfil no Pedestal
        glow_draw.rectangle([cx - 55, ped_y + 12, cx + 55, ped_y + 32], fill=(8, 10, 14), outline=col, width=1)
        glow_draw.line([(cx - 40, ped_y + 22), (cx + 40, ped_y + 22)], fill=col, width=2)
        
        # Busto Clássico Esculpido
        head_y = cy - 40
        # Tronco
        torso = [(cx - 65, head_y + 140), (cx - 42, head_y + 45), (cx + 42, head_y + 45), (cx + 65, head_y + 140), (cx, head_y + 155)]
        glow_draw.polygon(torso, fill=bg, outline=col, width=2)
        # Cabeça / Busto
        glow_draw.ellipse([cx - 32, head_y - 38, cx + 32, head_y + 38], fill=(210, 220, 230, 240), outline=col, width=2)
        
        # Elmo Alado de Hermes em cada agente
        w_left = [(cx - 24, head_y - 28), (cx - 72, head_y - 75), (cx - 48, head_y - 30), (cx - 64, head_y - 15), (cx - 25, head_y - 10)]
        glow_draw.polygon(w_left, fill=(20, 35, 50), outline=col, width=2)
        w_right = [(cx + 24, head_y - 28), (cx + 72, head_y - 75), (cx + 48, head_y - 30), (cx + 64, head_y - 15), (cx + 25, head_y - 10)]
        glow_draw.polygon(w_right, fill=(50, 40, 20), outline=col, width=2)
        
        # Anel de Isolamento Holográfico / Sandboxing em volta da cabeça
        glow_draw.ellipse([cx - 60, head_y - 20, cx + 60, head_y + 20], outline=col, width=1)
        
        # Micro-ícones flutuantes específicos de cada perfil
        if c["role"] == "FINANCEIRO":
            # Gráfico de barras e cadeado fiscal
            glow_draw.rectangle([cx - 30, cy + 50, cx - 18, cy + 90], fill=(0, 229, 255, 200))
            glow_draw.rectangle([cx - 10, cy + 30, cx + 2, cy + 90], fill=(0, 229, 255, 200))
            glow_draw.rectangle([cx + 10, cy + 10, cx + 22, cy + 90], fill=(0, 229, 255, 240))
        elif c["role"] == "EXECUTIVO":
            # Estrela / Bússola Estratégica
            glow_draw.line([(cx, cy + 20), (cx, cy + 80)], fill=(200, 240, 255, 240), width=2)
            glow_draw.line([(cx - 30, cy + 50), (cx + 30, cy + 50)], fill=(200, 240, 255, 240), width=2)
            glow_draw.polygon([(cx, cy + 15), (cx + 15, cy + 50), (cx, cy + 85), (cx - 15, cy + 50)], outline=(223, 186, 107, 240), width=1)
        else:
            # Rede de contatos / Funil de leads
            glow_draw.polygon([(cx - 28, cy + 25), (cx + 28, cy + 25), (cx + 10, cy + 65), (cx - 10, cy + 65)], outline=(223, 186, 107, 240), width=2)
            glow_draw.line([(cx, cy + 65), (cx, cy + 85)], fill=(223, 186, 107, 240), width=2)

    # 4. FITA DE STATUS SUPERIOR & TEXTO DE RECONHECIMENTO
    # Caixa de comando do Hermes Profile no topo
    cmd_box = [370, 115, 830, 155]
    glow_draw.rectangle(cmd_box, fill=(10, 14, 20, 240), outline=(0, 229, 255, 220), width=2)
    glow_draw.line([(390, 135), (460, 135)], fill=(0, 229, 255, 240), width=2)
    glow_draw.line([(480, 135), (710, 135)], fill=(223, 186, 107, 220), width=2)
    glow_draw.line([(730, 135), (810, 135)], fill=(0, 229, 255, 240), width=2)
    
    # Marcador de comando prompt
    glow_draw.polygon([(380, 128), (388, 135), (380, 142)], fill=(0, 229, 255, 255))
    
    # Compor camada glow na imagem final
    im.paste(glow_layer, (0, 0), glow_layer)
    
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\hermes-profiles-ambientes-isolados-agentes-ia.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_profiles_cover()
