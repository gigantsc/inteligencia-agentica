import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_checkpoints_cover():
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

    # 3. CENTRO: O BUSTO CLÁSSICO DE HERMES (GUARDIÃO DA INTEGRIDADE)
    cx, cy = 600, 410
    
    # Halo concêntrico de luz temporal e digital
    for r in range(270, 30, -12):
        alpha = int(38 * (1 - r / 270))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 20, 30, alpha), outline=(0, 229, 255, int(65 * (1 - r / 270))), width=1)
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 145
    glow_draw.rectangle([cx - 95, ped_y, cx + 95, ped_y + 45], fill=(18, 24, 34), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 115, ped_y + 45, cx + 115, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    
    # Inscrição / Emblema no Pedestal: CHECKPOINTS & ROLLBACK
    glow_draw.rectangle([cx - 70, ped_y + 12, cx + 70, ped_y + 32], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 55, ped_y + 22), (cx + 55, ped_y + 22)], fill=(223, 186, 107), width=2)
    
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
    # A. LADO ESQUERDO (CIANO): MÁQUINA DO TEMPO / AMPULHETA HOLOGRÁFICA / CHECKPOINTS REWIND
    time_x, time_y = 260, 410
    
    # Câmara Temporal de Snapshots
    glow_draw.rectangle([time_x - 95, time_y - 145, time_x + 95, time_y + 155], fill=(10, 24, 38, 220), outline=(0, 229, 255, 220), width=2)
    # Topo da Câmara: "ROLLBACK ENGINE"
    glow_draw.rectangle([time_x - 80, time_y - 135, time_x + 80, time_y - 110], fill=(6, 18, 28, 240), outline=(0, 229, 255, 180), width=1)
    glow_draw.line([(time_x - 60, time_y - 122), (time_x + 60, time_y - 122)], fill=(0, 229, 255, 240), width=2)
    
    # Ampulheta Clássica Holográfica de Reversão de Tempo
    hg_y = time_y - 25
    # Prato superior e inferior da ampulheta
    glow_draw.rectangle([time_x - 45, hg_y - 65, time_x + 45, hg_y - 55], fill=(16, 42, 60), outline=(0, 229, 255), width=2)
    glow_draw.rectangle([time_x - 45, hg_y + 55, time_x + 45, hg_y + 65], fill=(16, 42, 60), outline=(0, 229, 255), width=2)
    # Bulbos de vidro da ampulheta (triângulos invertidos que se tocam no centro)
    bulb_top = [(time_x - 40, hg_y - 55), (time_x + 40, hg_y - 55), (time_x, hg_y)]
    bulb_bot = [(time_x, hg_y), (time_x + 40, hg_y + 55), (time_x - 40, hg_y + 55)]
    glow_draw.polygon(bulb_top, fill=(12, 34, 52, 200), outline=(0, 229, 255, 240), width=2)
    glow_draw.polygon(bulb_bot, fill=(12, 34, 52, 200), outline=(0, 229, 255, 240), width=2)
    # Partículas de areia temporal ciano fluindo no sentido inverso (para cima)
    for p_sand in range(-25, 26, 8):
        glow_draw.ellipse([time_x + p_sand - 2, hg_y - 35 - abs(p_sand)//2, time_x + p_sand + 2, hg_y - 31 - abs(p_sand)//2], fill=(200, 245, 255, 230))
    glow_draw.line([(time_x, hg_y - 10), (time_x, hg_y + 20)], fill=(255, 255, 255, 250), width=2)
    
    # Seta Circular de Rewind / Rollback (⟲) ao redor da ampulheta
    glow_draw.arc([time_x - 58, hg_y - 58, time_x + 58, hg_y + 58], start=45, end=300, fill=(0, 229, 255, 240), width=3)
    # Ponta da seta do rollback
    arrow_tip = [(time_x + 22, hg_y - 50), (time_x + 36, hg_y - 38), (time_x + 10, hg_y - 34)]
    glow_draw.polygon(arrow_tip, fill=(0, 229, 255, 255))
    
    # Linha do Tempo de Checkpoints (Nós [CP-1], [CP-2], [CP-3]) na base da câmara
    tl_y = time_y + 95
    glow_draw.line([(time_x - 70, tl_y), (time_x + 70, tl_y)], fill=(0, 229, 255, 180), width=2)
    for idx, cp_offset in enumerate([-50, 0, 50]):
        cx_node = time_x + cp_offset
        glow_draw.ellipse([cx_node - 12, tl_y - 12, cx_node + 12, tl_y + 12], fill=(10, 30, 48), outline=(0, 229, 255), width=2)
        glow_draw.ellipse([cx_node - 5, tl_y - 5, cx_node + 5, tl_y + 5], fill=(200, 245, 255, 255))
        # Linha vertical indicadora
        glow_draw.line([(cx_node, tl_y - 20), (cx_node, tl_y - 14)], fill=(0, 229, 255, 220), width=1)
        
    # Conduítes Neurais ligando a Câmara Temporal ao Busto de Hermes
    for line_y in [-70, 0, 75]:
        glow_draw.line([(time_x + 95, time_y + line_y), (cx - 100, cy + line_y // 2)], fill=(0, 229, 255, 140), width=2)
        glow_draw.ellipse([time_x + 125, time_y + line_y - 3, time_x + 131, time_y + line_y + 3], fill=(0, 229, 255, 240))

    # B. LADO DIREITO (OURO ÂMBAR): SHADOW GIT REPO & AGENT-WRITE LEDGER
    git_x, git_y = 940, 410
    
    # Câmara do Shadow Git Store
    glow_draw.rectangle([git_x - 95, git_y - 145, git_x + 95, git_y + 155], fill=(32, 26, 12, 220), outline=(223, 186, 107, 220), width=2)
    # Topo da Câmara: "SHADOW GIT STORE"
    glow_draw.rectangle([git_x - 80, git_y - 135, git_x + 80, git_y - 110], fill=(24, 18, 8, 240), outline=(223, 186, 107, 180), width=1)
    glow_draw.line([(git_x - 60, git_y - 122), (git_x + 60, git_y - 122)], fill=(223, 186, 107, 240), width=2)
    
    # Árvore de Branches e Commits Git Desduplicados
    tree_top_y = git_y - 85
    # Linha principal (trunk branch)
    glow_draw.line([(git_x - 35, tree_top_y + 15), (git_x - 35, tree_top_y + 115)], fill=(223, 186, 107, 220), width=3)
    # Ramo secundário (feature / shadow ref branch)
    glow_draw.line([(git_x - 35, tree_top_y + 35), (git_x + 25, tree_top_y + 65)], fill=(223, 186, 107, 180), width=2)
    glow_draw.line([(git_x + 25, tree_top_y + 65), (git_x + 25, tree_top_y + 115)], fill=(223, 186, 107, 220), width=2)
    
    # Nós de Commit Dourados Luminosos
    commits = [
        (git_x - 35, tree_top_y + 20),
        (git_x - 35, tree_top_y + 65),
        (git_x - 35, tree_top_y + 110),
        (git_x + 25, tree_top_y + 75),
        (git_x + 25, tree_top_y + 110)
    ]
    for cm_x, cm_y in commits:
        glow_draw.ellipse([cm_x - 9, cm_y - 9, cm_x + 9, cm_y + 9], fill=(42, 32, 14), outline=(223, 186, 107), width=2)
        glow_draw.ellipse([cm_x - 4, cm_y - 4, cm_x + 4, cm_y + 4], fill=(255, 235, 160))
        
    # O Livro-Razão de Escrita (Agent-Write Ledger) na base da câmara
    leg_y = git_y + 75
    # Placa / Livro de Mármore e Ouro
    glow_draw.rectangle([git_x - 70, leg_y - 25, git_x + 70, leg_y + 55], fill=(36, 28, 12, 240), outline=(223, 186, 107), width=2)
    # Linhas de verificação do Ledger (Human vs Machine hashes)
    for l_idx in range(3):
        ly = leg_y - 12 + l_idx * 20
        # Indicador de integridade (check verde-ouro)
        glow_draw.ellipse([git_x - 55, ly - 4, git_x - 45, ly + 6], fill=(223, 186, 107))
        glow_draw.line([(git_x - 35, ly), (git_x + 55, ly)], fill=(215, 190, 115, 160), width=2)
        
    # Conduítes Dourados conectando Shadow Git ao Busto de Hermes
    for line_y in [-70, 0, 75]:
        glow_draw.line([(cx + 100, cy + line_y // 2), (git_x - 95, git_y + line_y)], fill=(223, 186, 107, 140), width=2)
        glow_draw.ellipse([git_x - 131, git_y + line_y - 3, git_x - 125, git_y + line_y + 3], fill=(223, 186, 107, 240))

    # C. ESCUDO CENTRAL AEGIS DE SEGURANÇA E INTEGRIDADE
    shield_y = cy + 60
    shield_pts = [
        (cx, shield_y + 45),
        (cx + 42, shield_y + 18),
        (cx + 42, shield_y - 25),
        (cx - 42, shield_y - 25),
        (cx - 42, shield_y + 18)
    ]
    glow_draw.polygon(shield_pts, fill=(12, 20, 32, 230), outline=(223, 186, 107, 255), width=2)
    # Divisão Split-Lighting no Escudo Central
    glow_draw.line([(cx, shield_y - 25), (cx, shield_y + 45)], fill=(0, 229, 255, 255), width=2)
    # Glifo central de Proteção: Ícone de Snapshot / Restauração
    glow_draw.ellipse([cx - 12, shield_y - 4, cx + 12, shield_y + 20], fill=(16, 28, 44), outline=(0, 229, 255, 240), width=2)
    glow_draw.line([(cx - 7, shield_y + 8), (cx + 7, shield_y + 8)], fill=(223, 186, 107, 255), width=2)

    # D. PARTÍCULAS LUMINOSAS E GLIFOS DIGITAIS NO AR
    particles = [
        (180, 220, (0, 229, 255)), (220, 580, (0, 229, 255)), (380, 180, (0, 229, 255)),
        (980, 210, (223, 186, 107)), (1020, 590, (223, 186, 107)), (820, 170, (223, 186, 107)),
        (600, 160, (200, 230, 255)), (540, 640, (0, 229, 255)), (660, 640, (223, 186, 107)),
        (260, 230, (0, 229, 255)), (940, 230, (223, 186, 107))
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
    filename = "checkpoints-rollback-seguranca-anti-alucinacao-agentes-ia.jpg"
    dest_path = os.path.join(static_dir, filename)
    
    final_rgb.save(dest_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso: {dest_path}")
    print(f"Dimensões: {final_rgb.size} (esperado: 1200x912)")

if __name__ == "__main__":
    create_checkpoints_cover()
