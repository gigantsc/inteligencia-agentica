import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_local_models_cover():
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
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
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

    # 3. CENTRO: O BUSTO CLÁSSICO DE HERMES (SOBERANO E PROTETOR)
    cx, cy = 600, 410
    
    # Halo concêntrico de luz (divina e digital)
    for r in range(270, 30, -12):
        alpha = int(38 * (1 - r / 270))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 20, 30, alpha), outline=(0, 229, 255, int(65 * (1 - r / 270))), width=1)
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 145
    glow_draw.rectangle([cx - 95, ped_y, cx + 95, ped_y + 45], fill=(18, 24, 34), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 115, ped_y + 45, cx + 115, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    # Inscrição / Emblema no Pedestal: GLIFO DO HERMES AGENT & OLLAMA
    glow_draw.rectangle([cx - 65, ped_y + 12, cx + 65, ped_y + 32], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 50, ped_y + 22), (cx + 50, ped_y + 22)], fill=(223, 186, 107), width=2)
    
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

    # 4. ELEMENTOS DO TEMA: SERVIDOR ON-PREMISE LOCAL (ESQUERDA) & COFRE/CUSTO ZERO LGPD (DIREITA)
    
    # A. LADO ESQUERDO (CIANO): WORKSTATION/SERVIDOR LOCAL & PROCESSADOR NEURAL ON-PREMISE
    srv_x, srv_y = 260, 410
    
    # Chassi do Servidor em Mármore e Grafite
    glow_draw.rectangle([srv_x - 90, srv_y - 140, srv_x + 90, srv_y + 150], fill=(12, 22, 34, 220), outline=(0, 229, 255, 220), width=2)
    # Topo do Servidor com Rótulo "ON-PREMISE"
    glow_draw.rectangle([srv_x - 75, srv_y - 130, srv_x + 75, srv_y - 105], fill=(8, 16, 26, 240), outline=(0, 229, 255, 180), width=1)
    glow_draw.line([(srv_x - 55, srv_y - 118), (srv_x + 55, srv_y - 118)], fill=(0, 229, 255, 230), width=2)
    
    # 3 Baias de Lâminas / GPU Acceleration Blades
    for blade_idx in range(3):
        by = srv_y - 85 + blade_idx * 45
        glow_draw.rectangle([srv_x - 75, by, srv_x + 75, by + 32], fill=(14, 28, 42, 230), outline=(0, 210, 245, 160), width=1)
        # LED indicators / VRAM status
        for led in range(4):
            lx = srv_x - 60 + led * 14
            glow_draw.ellipse([lx - 3, by + 16 - 3, lx + 3, by + 16 + 3], fill=(0, 229, 255, 240))
        # Grade de ventilação / dissipador
        for vent in range(5):
            vx = srv_x + 10 + vent * 11
            glow_draw.line([(vx, by + 8), (vx, by + 24)], fill=(0, 229, 255, 120), width=2)
            
    # Processador Neural Central (Chip AI On-Premise) na base do servidor
    chip_y = srv_y + 80
    glow_draw.rectangle([srv_x - 50, chip_y, srv_x + 50, chip_y + 50], fill=(10, 32, 48, 240), outline=(0, 229, 255, 240), width=2)
    # Pinos do Chip
    for p in range(5):
        px = srv_x - 40 + p * 20
        glow_draw.line([(px, chip_y - 6), (px, chip_y)], fill=(0, 229, 255, 200), width=2)
        glow_draw.line([(px, chip_y + 50), (px, chip_y + 56)], fill=(0, 229, 255, 200), width=2)
    # Núcleo luminoso do chip (Glifo Qwen/Gemma local)
    glow_draw.ellipse([srv_x - 18, chip_y + 7, srv_x + 18, chip_y + 43], fill=(0, 229, 255, 140), outline=(255, 255, 255, 230), width=1)
    
    # Conduítes Neurais ligando Servidor Local ao Busto Central (Air-gapped)
    for line_y in [-60, 10, 80]:
        glow_draw.line([(srv_x + 90, srv_y + line_y), (cx - 100, cy + line_y // 2)], fill=(0, 229, 255, 140), width=2)
        glow_draw.ellipse([srv_x + 120, srv_y + line_y - 3, srv_x + 126, srv_y + line_y + 3], fill=(0, 229, 255, 240))

    # B. LADO DIREITO (OURO ÂMBAR): COFRE DE SEGURANÇA LGPD & BALANÇA DE CUSTO ZERO (R$ 0,00)
    vault_x, vault_y = 940, 410
    
    # Câmara do Cofre de Soberania de Dados
    glow_draw.rectangle([vault_x - 90, vault_y - 140, vault_x + 90, vault_y + 150], fill=(32, 26, 12, 220), outline=(223, 186, 107, 220), width=2)
    # Topo com Rótulo "LGPD COMPLIANT"
    glow_draw.rectangle([vault_x - 75, vault_y - 130, vault_x + 75, vault_y - 105], fill=(24, 18, 8, 240), outline=(223, 186, 107, 180), width=1)
    glow_draw.line([(vault_x - 55, vault_y - 118), (vault_x + 55, vault_y - 118)], fill=(223, 186, 107, 230), width=2)
    
    # Grande Engrenagem de Segredo Comercial / Fechadura Criptográfica
    v_cr = 55
    glow_draw.ellipse([vault_x - v_cr, vault_y - 45 - v_cr, vault_x + v_cr, vault_y - 45 + v_cr], fill=(36, 28, 12, 240), outline=(223, 186, 107, 250), width=3)
    glow_draw.ellipse([vault_x - v_cr + 12, vault_y - 45 - v_cr + 12, vault_x + v_cr - 12, vault_y - 45 + v_cr - 12], outline=(255, 225, 140, 200), width=1)
    # Dentes de engrenagem da blindagem
    for i in range(8):
        angle = i * (math.pi / 4)
        gx1 = vault_x + math.cos(angle) * (v_cr - 4)
        gy1 = vault_y - 45 + math.sin(angle) * (v_cr - 4)
        gx2 = vault_x + math.cos(angle) * (v_cr + 10)
        gy2 = vault_y - 45 + math.sin(angle) * (v_cr + 10)
        glow_draw.line([(gx1, gy1), (gx2, gy2)], fill=(223, 186, 107, 240), width=4)
        
    # Cadeado Central Dourado (LGPD)
    lock_y = vault_y - 45
    glow_draw.arc([vault_x - 14, lock_y - 18, vault_x + 14, lock_y + 4], start=180, end=0, fill=(223, 186, 107, 255), width=3)
    glow_draw.rectangle([vault_x - 16, lock_y - 4, vault_x + 16, lock_y + 18], fill=(45, 35, 14, 255), outline=(223, 186, 107, 255), width=2)
    glow_draw.ellipse([vault_x - 3, lock_y + 2, vault_x + 3, lock_y + 8], fill=(223, 186, 107, 255))
    
    # Balança Clássica de Precisão de Mármore e Ouro (CUSTO ZERO / R$ 0,00)
    bal_y = vault_y + 75
    # Haste Vertical da balança
    glow_draw.line([(vault_x, bal_y - 25), (vault_x, bal_y + 45)], fill=(223, 186, 107, 240), width=3)
    # Travessão horizontal equilibrado
    glow_draw.line([(vault_x - 55, bal_y - 20), (vault_x + 55, bal_y - 20)], fill=(223, 186, 107, 240), width=3)
    # Prato Esquerdo (Tokens = 0)
    glow_draw.line([(vault_x - 55, bal_y - 20), (vault_x - 70, bal_y + 5)], fill=(223, 186, 107, 160), width=1)
    glow_draw.line([(vault_x - 55, bal_y - 20), (vault_x - 40, bal_y + 5)], fill=(223, 186, 107, 160), width=1)
    glow_draw.arc([vault_x - 75, bal_y - 5, vault_x - 35, bal_y + 15], start=0, end=180, fill=(223, 186, 107, 240), width=2)
    # Moeda de ouro / Símbolo $0
    glow_draw.ellipse([vault_x - 60, bal_y - 3, vault_x - 50, bal_y + 7], fill=(255, 225, 140, 240), outline=(223, 186, 107), width=1)
    
    # Prato Direito (Proteção)
    glow_draw.line([(vault_x + 55, bal_y - 20), (vault_x + 40, bal_y + 5)], fill=(223, 186, 107, 160), width=1)
    glow_draw.line([(vault_x + 55, bal_y - 20), (vault_x + 70, bal_y + 5)], fill=(223, 186, 107, 160), width=1)
    glow_draw.arc([vault_x + 35, bal_y - 5, vault_x + 75, bal_y + 15], start=0, end=180, fill=(223, 186, 107, 240), width=2)
    glow_draw.ellipse([vault_x + 50, bal_y - 3, vault_x + 60, bal_y + 7], fill=(255, 225, 140, 240), outline=(223, 186, 107), width=1)
    
    # Conduítes Dourados conectando Cofre ao Busto Central
    for line_y in [-60, 10, 80]:
        glow_draw.line([(cx + 100, cy + line_y // 2), (vault_x - 90, vault_y + line_y)], fill=(223, 186, 107, 140), width=2)
        glow_draw.ellipse([vault_x - 126, vault_y + line_y - 3, vault_x - 120, vault_y + line_y + 3], fill=(223, 186, 107, 240))

    # C. ESCUDO CENTRAL AEGIS DE SEGURANÇA HÍBRIDA & SOBERANIA
    shield_y = cy + 60
    shield_pts = [
        (cx, shield_y + 40),
        (cx + 38, shield_y + 15),
        (cx + 38, shield_y - 22),
        (cx - 38, shield_y - 22),
        (cx - 38, shield_y + 15)
    ]
    glow_draw.polygon(shield_pts, fill=(12, 20, 32, 230), outline=(223, 186, 107, 255), width=2)
    # Divisão Split-Lighting no Escudo Central
    glow_draw.line([(cx, shield_y - 22), (cx, shield_y + 40)], fill=(0, 229, 255, 255), width=2)
    # Glifo central de Proteção e Execução
    glow_draw.ellipse([cx - 10, shield_y - 2, cx + 10, shield_y + 18], fill=(16, 28, 44), outline=(0, 229, 255, 240), width=2)
    glow_draw.line([(cx - 5, shield_y + 8), (cx + 5, shield_y + 8)], fill=(223, 186, 107, 255), width=2)
    
    # D. PARTÍCULAS LUMINOSAS E GLIFOS DIGITAIS NO AR
    particles = [
        (180, 220, (0, 229, 255)), (220, 580, (0, 229, 255)), (380, 180, (0, 229, 255)),
        (980, 210, (223, 186, 107)), (1020, 590, (223, 186, 107)), (820, 170, (223, 186, 107)),
        (600, 160, (200, 230, 255)), (540, 640, (0, 229, 255)), (660, 640, (223, 186, 107))
    ]
    for px, py, pcol in particles:
        glow_draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=pcol)
        glow_draw.ellipse([px - 7, py - 7, px + 7, py + 7], outline=(pcol[0], pcol[1], pcol[2], 90), width=1)
        
    # 5. MERGE LAYERS E SALVAR
    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(1.5))
    final_img = Image.alpha_composite(im.convert("RGBA"), glow_blurred)
    final_rgb = final_img.convert("RGB")
    
    # Destino oficial
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    filename = "modelos-locais-ollama-agentes-ia-soberania-privacidade-custo-zero.jpg"
    dest_path = os.path.join(static_dir, filename)
    
    final_rgb.save(dest_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso: {dest_path}")
    print(f"Dimensões: {final_rgb.size} (esperado: 1200x912)")

if __name__ == "__main__":
    create_local_models_cover()
