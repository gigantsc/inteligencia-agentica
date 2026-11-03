import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_ha_resilience_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient wash: Left Cyan (#00E5FF) and Right Amber-Gold (#DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor perspective grid
    for y in range(670, height, 18):
        alpha = int(40 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 215, 245, alpha), width=1)
    for x in range(50, width, 55):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.7), height)], fill=(0, 215, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore e Frontão)
    # Coluna Esquerda (Ciano)
    col1_x = 75
    col_w = 52
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(90, 215, 245, 60), width=2)
    glow_draw.rectangle([col1_x - 14, 90, col1_x + col_w + 14, 120], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 740, col1_x + col_w + 16, 775], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Direita (Ouro)
    col2_x = 1072
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(215, 190, 115, 60), width=2)
    glow_draw.rectangle([col2_x - 14, 90, col2_x + col_w + 14, 120], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 740, col2_x + col_w + 16, 775], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)

    # Frontão Clássico Superior (Triangular Pediment)
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)

    # 3. CENTRO: O BUSTO CLÁSSICO DE HERMES (COMANDANTE DA ALTA DISPONIBILIDADE)
    cx, cy = 600, 410
    
    # Halo concêntrico de resiliência e proteção (Escudo de Campo de Força)
    for r in range(280, 40, -12):
        alpha = int(45 * (1 - r / 280))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 20, 30, alpha), outline=(0, 229, 255, int(65 * (1 - r / 280))), width=1)
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 145
    glow_draw.rectangle([cx - 95, ped_y, cx + 95, ped_y + 45], fill=(18, 24, 34), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 115, ped_y + 45, cx + 115, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    
    # Inscrição / Emblema no Pedestal: HIGH AVAILABILITY / ZERO DOWNTIME
    glow_draw.rectangle([cx - 75, ped_y + 12, cx + 75, ped_y + 32], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 60, ped_y + 22), (cx + 60, ped_y + 22)], fill=(223, 186, 107), width=2)
    
    # Busto Esculpido de Hermes
    b_head_y = cy - 40
    # Tronco Clássico com Toga de Mármore
    torso = [(cx - 85, b_head_y + 145), (cx - 50, b_head_y + 45), (cx + 50, b_head_y + 45), (cx + 85, b_head_y + 145), (cx, b_head_y + 160)]
    glow_draw.polygon(torso, fill=(18, 26, 38, 240), outline=(210, 225, 240, 220), width=2)
    # Toga plissada em linhas diagonais
    for t_line in range(-35, 45, 18):
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)], fill=(90, 140, 180, 120), width=2)
    
    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([cx - 38, b_head_y - 45, cx + 38, b_head_y + 40], fill=(225, 232, 242, 245), outline=(0, 229, 255, 220), width=2)
    
    # Elmo Alado de Hermes (Petasos Alado)
    glow_draw.ellipse([cx - 45, b_head_y - 52, cx + 45, b_head_y - 30], fill=(190, 205, 220), outline=(223, 186, 107), width=2)
    
    # Asa Esquerda (Ciano Neon)
    wing_l = [(cx - 32, b_head_y - 40), (cx - 95, b_head_y - 92), (cx - 68, b_head_y - 38), (cx - 84, b_head_y - 20), (cx - 32, b_head_y - 15)]
    glow_draw.polygon(wing_l, fill=(15, 45, 65, 230), outline=(0, 229, 255, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx - 35, b_head_y - 35), (cx - 80 + w * 12, b_head_y - 75 + w * 18)], fill=(0, 229, 255, 200), width=2)
        
    # Asa Direita (Ouro Âmbar)
    wing_r = [(cx + 32, b_head_y - 40), (cx + 95, b_head_y - 92), (cx + 68, b_head_y - 38), (cx + 84, b_head_y - 20), (cx + 32, b_head_y - 15)]
    glow_draw.polygon(wing_r, fill=(65, 50, 18, 230), outline=(223, 186, 107, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx + 35, b_head_y - 35), (cx + 80 - w * 12, b_head_y - 75 + w * 18)], fill=(223, 186, 107, 200), width=2)

    # 4. ELEMENTOS DO TEMA ESPECÍFICO:
    # A. LADO ESQUERDO (CIANO): CREDENTIAL POOLS (Anel de Chaves & Rotação Inteligente)
    pool_cx, pool_cy = 280, 410
    
    # Halo brilhante em volta do pool
    for r in range(160, 40, -10):
        glow_draw.ellipse([pool_cx - r, pool_cy - r, pool_cx + r, pool_cy + r], outline=(0, 229, 255, int(45 * (1 - r / 160))), width=1)
        
    # Anel orbital do Credential Pool
    r_outer = 110
    r_inner = 85
    glow_draw.ellipse([pool_cx - r_outer, pool_cy - r_outer, pool_cx + r_outer, pool_cy + r_outer], outline=(0, 229, 255, 220), width=3)
    glow_draw.ellipse([pool_cx - r_inner, pool_cy - r_inner, pool_cx + r_inner, pool_cy + r_inner], outline=(0, 200, 240, 140), width=2)
    
    # Chaves criptográficas / Tokens distribuídos orbitalmente (3 Chaves no Pool)
    angles = [0, 120, 240]
    labels_colors = [(0, 229, 255), (72, 230, 140), (223, 186, 107)]
    for idx, deg in enumerate(angles):
        rad = math.radians(deg)
        r_mid = (r_outer + r_inner) / 2
        kx = pool_cx + r_mid * math.cos(rad)
        ky = pool_cy + r_mid * math.sin(rad)
        
        # Token / Cartão de Chave
        glow_draw.rectangle([kx - 18, ky - 14, kx + 18, ky + 14], fill=(10, 24, 38, 240), outline=labels_colors[idx], width=2)
        # Símbolo da chave (Círculo + Dentes)
        glow_draw.ellipse([kx - 10, ky - 6, kx - 2, ky + 6], outline=(255, 255, 255), width=2)
        glow_draw.line([(kx - 2, ky), (kx + 10, ky)], fill=(255, 255, 255), width=2)
        glow_draw.line([(kx + 6, ky), (kx + 6, ky + 4)], fill=(255, 255, 255), width=2)
        glow_draw.line([(kx + 9, ky), (kx + 9, ky + 4)], fill=(255, 255, 255), width=2)
        
        # Setas orbitais de rotação (sentido horário)
        tang_rad = rad + math.pi / 2
        p_arrow = (kx + 22 * math.cos(tang_rad), ky + 22 * math.sin(tang_rad))
        glow_draw.line([(kx, ky), p_arrow], fill=(0, 229, 255, 200), width=2)

    # Centro do Pool: O Núcleo de Seleção Atômica (round_robin / fill_first)
    glow_draw.ellipse([pool_cx - 40, pool_cy - 40, pool_cx + 40, pool_cy + 40], fill=(8, 22, 36, 230), outline=(0, 229, 255, 240), width=2)
    # Glifo central de Lock de Concorrência (Thread-Safe Lock)
    glow_draw.rectangle([pool_cx - 16, pool_cy - 4, pool_cx + 16, pool_cy + 18], fill=(0, 229, 255, 190), outline=(255, 255, 255), width=2)
    glow_draw.arc([pool_cx - 11, pool_cy - 20, pool_cx + 11, pool_cy + 2], 180, 360, fill=(255, 255, 255), width=3)
    glow_draw.ellipse([pool_cx - 3, pool_cy + 3, pool_cx + 3, pool_cy + 9], fill=(10, 24, 38))
    
    # Placa de Identificação do Pool
    glow_draw.rectangle([pool_cx - 110, pool_cy + 130, pool_cx + 110, pool_cy + 165], fill=(8, 20, 32, 220), outline=(0, 229, 255, 200), width=2)
    glow_draw.line([(pool_cx - 90, pool_cy + 144), (pool_cx + 90, pool_cy + 144)], fill=(0, 229, 255, 220), width=3)
    glow_draw.line([(pool_cx - 70, pool_cy + 152), (pool_cx + 70, pool_cy + 152)], fill=(120, 220, 250, 180), width=2)

    # Conduíte neural conectando Pool ao Hermes Central
    glow_draw.line([(pool_cx + 110, pool_cy), (cx - 100, cy + 30)], fill=(0, 229, 255, 180), width=2)
    for p in range(5):
        kx = pool_cx + 110 + p * ((cx - 100) - (pool_cx + 110)) / 5
        ky = pool_cy + p * ((cy + 30) - pool_cy) / 5
        glow_draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=(0, 229, 255, 240))

    # B. LADO DIREITO (OURO): FALLBACK PROVIDERS (Cascata Hierárquica Multiprovedor)
    fall_cx, fall_cy = 920, 410
    
    # Halo dourado
    for r in range(160, 40, -10):
        glow_draw.ellipse([fall_cx - r, fall_cy - r, fall_cx + r, fall_cy + r], outline=(223, 186, 107, int(45 * (1 - r / 160))), width=1)
        
    # Estrutura em Cascata / Pirâmide de Provedores (3 Níveis)
    # Nível 1: Primário (Claude / Anthropic)
    glow_draw.rectangle([fall_cx - 85, fall_cy - 95, fall_cx + 85, fall_cy - 55], fill=(35, 28, 12, 230), outline=(223, 186, 107, 240), width=2)
    glow_draw.ellipse([fall_cx - 70, fall_cy - 75, fall_cx - 56, fall_cy - 61], fill=(223, 186, 107))
    glow_draw.line([(fall_cx - 45, fall_cy - 75), (fall_cx + 70, fall_cy - 75)], fill=(223, 186, 107), width=3)
    glow_draw.line([(fall_cx - 45, fall_cy - 65), (fall_cx + 40, fall_cy - 65)], fill=(240, 210, 140), width=2)
    
    # Seta de Failover Nível 1 -> Nível 2
    glow_draw.line([(fall_cx, fall_cy - 55), (fall_cx, fall_cy - 30)], fill=(255, 120, 100), width=2)
    glow_draw.polygon([(fall_cx - 5, fall_cy - 33), (fall_cx + 5, fall_cy - 33), (fall_cx, fall_cy - 27)], fill=(255, 120, 100))

    # Nível 2: Secundário (DeepSeek / OpenRouter)
    glow_draw.rectangle([fall_cx - 95, fall_cy - 25, fall_cx + 95, fall_cy + 15], fill=(28, 22, 10, 230), outline=(223, 186, 107, 220), width=2)
    glow_draw.ellipse([fall_cx - 80, fall_cy - 5, fall_cx - 66, fall_cy + 9], fill=(0, 229, 255))
    glow_draw.line([(fall_cx - 55, fall_cy - 5), (fall_cx + 80, fall_cy - 5)], fill=(0, 229, 255), width=3)
    glow_draw.line([(fall_cx - 55, fall_cy + 5), (fall_cx + 50, fall_cy + 5)], fill=(150, 235, 255), width=2)
    
    # Seta de Failover Nível 2 -> Nível 3
    glow_draw.line([(fall_cx, fall_cy + 15), (fall_cx, fall_cy + 40)], fill=(255, 120, 100), width=2)
    glow_draw.polygon([(fall_cx - 5, fall_cy + 37), (fall_cx + 5, fall_cy + 37), (fall_cx, fall_cy + 43)], fill=(255, 120, 100))

    # Nível 3: Bunker Local (Ollama / llama.cpp / Soberania)
    glow_draw.rectangle([fall_cx - 105, fall_cy + 45, fall_cx + 105, fall_cy + 85], fill=(20, 16, 8, 230), outline=(72, 230, 140, 230), width=2)
    glow_draw.ellipse([fall_cx - 90, fall_cy + 65, fall_cx - 76, fall_cy + 79], fill=(72, 230, 140))
    glow_draw.line([(fall_cx - 65, fall_cy + 65), (fall_cx + 90, fall_cy + 65)], fill=(72, 230, 140), width=3)
    glow_draw.line([(fall_cx - 65, fall_cy + 75), (fall_cx + 60, fall_cy + 75)], fill=(160, 245, 195), width=2)

    # Circuito de Retorno Reset-Aware (Volta ao topo quando rate limit expira)
    loop_pts = [(fall_cx + 115, fall_cy + 65), (fall_cx + 135, fall_cy + 65), (fall_cx + 135, fall_cy - 75), (fall_cx + 95, fall_cy - 75)]
    glow_draw.line(loop_pts, fill=(223, 186, 107, 180), width=2)
    glow_draw.polygon([(fall_cx + 97, fall_cy - 79), (fall_cx + 97, fall_cy - 71), (fall_cx + 90, fall_cy - 75)], fill=(223, 186, 107))

    # Placa de Identificação do Fallback
    glow_draw.rectangle([fall_cx - 110, fall_cy + 130, fall_cx + 110, fall_cy + 165], fill=(30, 24, 12, 220), outline=(223, 186, 107, 200), width=2)
    glow_draw.line([(fall_cx - 90, fall_cy + 144), (fall_cx + 90, fall_cy + 144)], fill=(223, 186, 107, 220), width=3)
    glow_draw.line([(fall_cx - 70, fall_cy + 152), (fall_cx + 70, fall_cy + 152)], fill=(240, 210, 140, 180), width=2)

    # Conduíte neural conectando Hermes ao Fallback
    glow_draw.line([(cx + 100, cy + 30), (fall_cx - 100, fall_cy)], fill=(223, 186, 107, 180), width=2)
    for p in range(5):
        kx = (cx + 100) + p * ((fall_cx - 100) - (cx + 100)) / 5
        ky = (cy + 30) + p * (fall_cy - (cy + 30)) / 5
        glow_draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=(223, 186, 107, 240))

    # C. BASE INFERIOR (CENTRO): PROVIDER ROUTING & LGPD SHIELD (data_collection: "deny")
    base_cx, base_cy = 600, 715
    # Escudo de conformidade de dados
    glow_draw.rectangle([base_cx - 130, base_cy - 20, base_cx + 130, base_cy + 20], fill=(12, 18, 26, 230), outline=(0, 229, 255, 210), width=2)
    glow_draw.line([(base_cx - 110, base_cy - 6), (base_cx + 110, base_cy - 6)], fill=(223, 186, 107), width=2)
    glow_draw.line([(base_cx - 90, base_cy + 6), (base_cx + 90, base_cy + 6)], fill=(72, 230, 140), width=2)
    # Glifo do Escudo
    glow_draw.polygon([(base_cx - 150, base_cy - 12), (base_cx - 140, base_cy - 12), (base_cx - 145, base_cy + 10)], fill=(0, 229, 255))
    glow_draw.polygon([(base_cx + 140, base_cy - 12), (base_cx + 150, base_cy - 12), (base_cx + 145, base_cy + 10)], fill=(223, 186, 107))

    # 5. Composite glow onto the base image
    final_img = Image.alpha_composite(im.convert("RGBA"), glow_layer).convert("RGB")
    
    # Destination path
    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "credential-pools-fallback-providers-alta-disponibilidade-agentes-ia.jpg")
    
    final_img.save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {out_path}")
    print(f"Dimensões: {final_img.size} (esperado: 1200x912)")

if __name__ == "__main__":
    create_ha_resilience_cover()
