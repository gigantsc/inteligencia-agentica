import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_goals_cover():
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

    # 3. CENTRO: O BUSTO CLÁSSICO DE HERMES (COMANDANTE DA METAS AUTÔNOMAS)
    cx, cy = 600, 410
    
    # Halo concêntrico de luz temporal e objetivo
    for r in range(270, 30, -12):
        alpha = int(40 * (1 - r / 270))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 20, 30, alpha), outline=(0, 229, 255, int(70 * (1 - r / 270))), width=1)
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 145
    glow_draw.rectangle([cx - 95, ped_y, cx + 95, ped_y + 45], fill=(18, 24, 34), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 115, ped_y + 45, cx + 115, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    
    # Inscrição / Emblema no Pedestal: PERSISTENT GOALS / RALPH LOOP
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
    # A. LADO ESQUERDO (CIANO): O RALPH LOOP AUTÔNOMO (Loop contínuo com nós de iteração e Juiz)
    loop_cx, loop_cy = 280, 410
    
    # Halo brilhante em volta do loop
    for r in range(160, 40, -10):
        glow_draw.ellipse([loop_cx - r, loop_cy - r, loop_cx + r, loop_cy + r], outline=(0, 229, 255, int(45 * (1 - r / 160))), width=1)
        
    # Anel toroidal principal do Loop
    r_outer = 110
    r_inner = 85
    glow_draw.ellipse([loop_cx - r_outer, loop_cy - r_outer, loop_cx + r_outer, loop_cy + r_outer], outline=(0, 229, 255, 220), width=3)
    glow_draw.ellipse([loop_cx - r_inner, loop_cy - r_inner, loop_cx + r_inner, loop_cy + r_inner], outline=(0, 200, 240, 150), width=2)
    
    # Setas orbitais de continuação no Ralph Loop (Sentido horário)
    for deg in [30, 120, 210, 300]:
        rad = math.radians(deg)
        r_mid = (r_outer + r_inner) / 2
        px = loop_cx + r_mid * math.cos(rad)
        py = loop_cy + r_mid * math.sin(rad)
        glow_draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(0, 229, 255, 230), outline=(255, 255, 255, 240), width=1)
        
        # Vetor direcional / ponta de seta
        tang_rad = rad + math.pi / 2
        p_arrow = (px + 12 * math.cos(tang_rad), py + 12 * math.sin(tang_rad))
        glow_draw.line([(px, py), p_arrow], fill=(255, 255, 255, 220), width=2)

    # Centro do Loop: O Olho Avaliador do Modelo Juiz (goal_judge)
    glow_draw.ellipse([loop_cx - 45, loop_cy - 45, loop_cx + 45, loop_cy + 45], fill=(10, 24, 38, 220), outline=(0, 229, 255, 240), width=2)
    # Pupila / Lente holográfica
    glow_draw.ellipse([loop_cx - 20, loop_cy - 20, loop_cx + 20, loop_cy + 20], fill=(0, 229, 255, 180), outline=(255, 255, 255, 255), width=2)
    glow_draw.ellipse([loop_cx - 6, loop_cy - 6, loop_cx + 6, loop_cy + 6], fill=(255, 255, 255, 255))
    
    # Placa de Identificação do Loop
    glow_draw.rectangle([loop_cx - 105, loop_cy + 130, loop_cx + 105, loop_cy + 165], fill=(8, 20, 32, 220), outline=(0, 229, 255, 200), width=2)
    # Linhas decorativas simulando tipografia clássica: RALPH LOOP - AUTONOMOUS TURNS
    glow_draw.line([(loop_cx - 85, loop_cy + 144), (loop_cx + 85, loop_cy + 144)], fill=(0, 229, 255, 220), width=3)
    glow_draw.line([(loop_cx - 65, loop_cy + 152), (loop_cx + 65, loop_cy + 152)], fill=(120, 220, 250, 180), width=2)

    # Conduíte neural conectando Ralph Loop ao Hermes Central
    glow_draw.line([(loop_cx + 110, loop_cy), (cx - 100, cy + 30)], fill=(0, 229, 255, 180), width=2)
    for p in range(5):
        kx = loop_cx + 110 + p * ((cx - 100) - (loop_cx + 110)) / 5
        ky = loop_cy + p * ((cy + 30) - loop_cy) / 5
        glow_draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=(0, 229, 255, 240))

    # B. LADO DIREITO (OURO): COMPLETION CONTRACTS & DETERMINISTIC QUALITY GATES
    gate_cx, gate_cy = 920, 410
    
    # Halo dourado
    for r in range(160, 40, -10):
        glow_draw.ellipse([gate_cx - r, gate_cy - r, gate_cx + r, gate_cy + r], outline=(223, 186, 107, int(45 * (1 - r / 160))), width=1)
        
    # Portal Clássico do Quality Gate (Portal em Arco)
    arch_w, arch_h = 170, 230
    ax1, ay1 = gate_cx - arch_w // 2, gate_cy - arch_h // 2
    ax2, ay2 = gate_cx + arch_w // 2, gate_cy + arch_h // 2
    
    # Retângulo base do portal
    glow_draw.rectangle([ax1, ay1 + 45, ax2, ay2], fill=(24, 20, 12, 200), outline=(223, 186, 107, 240), width=2)
    # Arco superior
    glow_draw.chord([ax1, ay1, ax2, ay1 + 90], 180, 360, fill=(24, 20, 12, 200), outline=(223, 186, 107, 240), width=2)
    
    # O Pergaminho Holográfico / Tablet do Contrato (5 Dimensões)
    glow_draw.rectangle([ax1 + 18, ay1 + 40, ax2 - 18, ay2 - 50], fill=(15, 14, 10, 220), outline=(223, 186, 107, 180), width=1)
    
    # 5 Linhas de Especificação do Contrato: Outcome, Verification, Constraints, Boundaries, Stop-When
    contract_y_starts = [ay1 + 55, ay1 + 75, ay1 + 95, ay1 + 115, ay1 + 135]
    colors = [(223, 186, 107), (0, 229, 255), (223, 186, 107), (180, 195, 215), (255, 120, 100)]
    for idx, y_pos in enumerate(contract_y_starts):
        # Marcador de ponto
        glow_draw.ellipse([ax1 + 28, y_pos - 3, ax1 + 34, y_pos + 3], fill=colors[idx])
        # Barra de dados
        glow_draw.line([(ax1 + 42, y_pos), (ax2 - 32, y_pos)], fill=colors[idx], width=2)
        
    # Emblema de Aprovação Determinística (Quality Gate: Exit Code 0 / SUCESSO)
    glow_draw.rectangle([gate_cx - 65, ay2 - 42, gate_cx + 65, ay2 - 12], fill=(12, 32, 22, 230), outline=(72, 230, 140, 240), width=2)
    # Marca de verificação / Checkmark estilizado
    chk_x, chk_y = gate_cx - 35, ay2 - 27
    glow_draw.line([(chk_x, chk_y), (chk_x + 8, chk_y + 8)], fill=(72, 230, 140), width=3)
    glow_draw.line([(chk_x + 8, chk_y + 8), (chk_x + 22, chk_y - 8)], fill=(72, 230, 140), width=3)
    # Linha dourada do Exit Code 0
    glow_draw.line([(chk_x + 30, chk_y), (gate_cx + 50, chk_y)], fill=(223, 186, 107), width=3)

    # Placa inferior do Quality Gate
    glow_draw.rectangle([gate_cx - 105, gate_cy + 130, gate_cx + 105, gate_cy + 165], fill=(30, 24, 12, 220), outline=(223, 186, 107, 200), width=2)
    glow_draw.line([(gate_cx - 85, gate_cy + 144), (gate_cx + 85, gate_cy + 144)], fill=(223, 186, 107, 220), width=3)
    glow_draw.line([(gate_cx - 65, gate_cy + 152), (gate_cx + 65, gate_cy + 152)], fill=(240, 210, 140, 180), width=2)

    # Conduíte neural conectando Hermes ao Quality Gate
    glow_draw.line([(cx + 100, cy + 30), (gate_cx - 100, gate_cy)], fill=(223, 186, 107, 180), width=2)
    for p in range(5):
        kx = (cx + 100) + p * ((gate_cx - 100) - (cx + 100)) / 5
        ky = (cy + 30) + p * (gate_cy - (cy + 30)) / 5
        glow_draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=(223, 186, 107, 240))

    # 5. Composite glow onto the base image
    final_img = Image.alpha_composite(im.convert("RGBA"), glow_layer).convert("RGB")
    
    # Destination path
    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "persistent-goals-ralph-loop-autonomia-agentes-ia.jpg")
    
    final_img.save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {out_path}")
    print(f"Dimensões: {final_img.size} (esperado: 1200x912)")

if __name__ == "__main__":
    create_goals_cover()
