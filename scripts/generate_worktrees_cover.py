import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_worktrees_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
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
    # Coluna Esquerda (Mármore Ciano / Isolamento de Execução)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Repositório Central & Governança)
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
    
    # Inscrição clássica no frontão: HERMES AGENT // PARALLEL GIT WORKTREES
    glow_draw.rectangle([280, 92, 920, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(300, 102), (900, 102)], fill=(223, 186, 107), width=2)

    # 3. TRONCO CENTRAL DA ÁRVORE GIT (The Marble Root of .git)
    # Pedestal Neoclássico do Repositório Central (.git Root Core)
    tree_base_x, tree_base_y = 600, 680
    glow_draw.rectangle([tree_base_x - 90, tree_base_y - 20, tree_base_x + 90, tree_base_y + 35], fill=(18, 26, 38, 230), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([tree_base_x - 110, tree_base_y + 35, tree_base_x + 110, tree_base_y + 60], fill=(12, 18, 28, 240), outline=(0, 229, 255), width=2)
    
    # Rótulo do Pedestal .git Core
    glow_draw.rectangle([tree_base_x - 70, tree_base_y, tree_base_x + 70, tree_base_y + 18], fill=(5, 10, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(tree_base_x - 55, tree_base_y + 9), (tree_base_x + 55, tree_base_y + 9)], fill=(223, 186, 107), width=2)

    # Tronco de Mármore bifurcado ascendente (Y=680 até Y=420)
    glow_draw.polygon([
        (tree_base_x - 35, tree_base_y - 20),
        (tree_base_x + 35, tree_base_y - 20),
        (tree_base_x + 24, 460),
        (tree_base_x - 24, 460)
    ], fill=(22, 34, 48, 220), outline=(180, 215, 240), width=2)
    
    # Filamentos de fibra óptica no tronco
    glow_draw.line([(tree_base_x - 12, tree_base_y - 20), (tree_base_x - 8, 460)], fill=(0, 229, 255), width=2)
    glow_draw.line([(tree_base_x + 12, tree_base_y - 20), (tree_base_x + 8, 460)], fill=(223, 186, 107), width=2)

    # 4. OS TRÊS RAMOS PARALELOS DE WORKTREES (Branches & Execution Lanes)
    # Ponto de bifurcação central (Fork Nexus)
    nexus_x, nexus_y = 600, 450
    glow_draw.ellipse([nexus_x - 25, nexus_y - 25, nexus_x + 25, nexus_y + 25], fill=(15, 30, 45, 240), outline=(255, 255, 255), width=2)
    glow_draw.ellipse([nexus_x - 10, nexus_y - 10, nexus_x + 10, nexus_y + 10], fill=(0, 229, 255))

    # --- RAMO 1: WORKTREE ESQUERDO (.worktrees/backend - Ciano) ---
    b1_x, b1_y = 260, 310
    # Curva do galho estrutural
    glow_draw.line([(nexus_x - 18, nexus_y - 10), (410, 390), (b1_x + 80, b1_y + 50)], fill=(0, 229, 255, 220), width=4)
    # Nós de commit no galho esquerdo
    glow_draw.ellipse([460 - 8, 410 - 8, 460 + 8, 410 + 8], fill=(0, 229, 255), outline=(255, 255, 255), width=1)
    glow_draw.ellipse([360 - 8, 370 - 8, 360 + 8, 370 + 8], fill=(0, 229, 255), outline=(255, 255, 255), width=1)
    
    # Plataforma / Card do Worktree Backend
    glow_draw.rectangle([b1_x - 90, b1_y - 50, b1_x + 90, b1_y + 50], fill=(10, 25, 38, 230), outline=(0, 229, 255), width=2)
    # Header do card
    glow_draw.rectangle([b1_x - 85, b1_y - 45, b1_x + 85, b1_y - 20], fill=(0, 229, 255, 45), outline=(0, 229, 255), width=1)
    glow_draw.line([(b1_x - 70, b1_y - 32), (b1_x + 40, b1_y - 32)], fill=(0, 229, 255), width=2)
    # Linhas de código / diff holográfico
    glow_draw.line([(b1_x - 70, b1_y), (b1_x + 60, b1_y)], fill=(120, 220, 245), width=2)
    glow_draw.line([(b1_x - 70, b1_y + 18), (b1_x + 20, b1_y + 18)], fill=(223, 186, 107), width=2)
    glow_draw.line([(b1_x - 70, b1_y + 34), (b1_x + 50, b1_y + 34)], fill=(120, 220, 245), width=2)

    # Mini-busto de Agente Backend sobre o card
    glow_draw.ellipse([b1_x - 18, b1_y - 85, b1_x + 18, b1_y - 52], fill=(24, 38, 52), outline=(0, 229, 255), width=2)
    glow_draw.polygon([(b1_x - 22, b1_y - 52), (b1_x + 22, b1_y - 52), (b1_x, b1_y - 40)], fill=(18, 30, 44), outline=(0, 229, 255), width=1)

    # --- RAMO 2: WORKTREE DIREITO (.worktrees/frontend - Dourado) ---
    b2_x, b2_y = 940, 310
    # Curva do galho estrutural
    glow_draw.line([(nexus_x + 18, nexus_y - 10), (790, 390), (b2_x - 80, b2_y + 50)], fill=(223, 186, 107, 220), width=4)
    # Nós de commit no galho direito
    glow_draw.ellipse([740 - 8, 410 - 8, 740 + 8, 410 + 8], fill=(223, 186, 107), outline=(255, 255, 255), width=1)
    glow_draw.ellipse([840 - 8, 370 - 8, 840 + 8, 370 + 8], fill=(223, 186, 107), outline=(255, 255, 255), width=1)
    
    # Plataforma / Card do Worktree Frontend
    glow_draw.rectangle([b2_x - 90, b2_y - 50, b2_x + 90, b2_y + 50], fill=(32, 26, 14, 230), outline=(223, 186, 107), width=2)
    # Header do card
    glow_draw.rectangle([b2_x - 85, b2_y - 45, b2_x + 85, b2_y - 20], fill=(223, 186, 107, 45), outline=(223, 186, 107), width=1)
    glow_draw.line([(b2_x - 70, b2_y - 32), (b2_x + 40, b2_y - 32)], fill=(223, 186, 107), width=2)
    # Linhas de código / diff holográfico
    glow_draw.line([(b2_x - 70, b2_y), (b2_x + 60, b2_y)], fill=(240, 215, 160), width=2)
    glow_draw.line([(b2_x - 70, b2_y + 18), (b2_x + 20, b2_y + 18)], fill=(0, 229, 255), width=2)
    glow_draw.line([(b2_x - 70, b2_y + 34), (b2_x + 50, b2_y + 34)], fill=(240, 215, 160), width=2)

    # Mini-busto de Agente Frontend sobre o card
    glow_draw.ellipse([b2_x - 18, b2_y - 85, b2_x + 18, b2_y - 52], fill=(42, 34, 18), outline=(223, 186, 107), width=2)
    glow_draw.polygon([(b2_x - 22, b2_y - 52), (b2_x + 22, b2_y - 52), (b2_x, b2_y - 40)], fill=(32, 26, 14), outline=(223, 186, 107), width=1)

    # --- RAMO 3: WORKTREE CENTRAL SUPERIOR (.worktrees/devops-qa - Ciano e Ouro) ---
    b3_x, b3_y = 600, 230
    glow_draw.line([(nexus_x, nexus_y - 20), (b3_x, b3_y + 60)], fill=(170, 210, 235, 220), width=4)
    glow_draw.ellipse([b3_x - 8, 340 - 8, b3_x + 8, 340 + 8], fill=(255, 255, 255), outline=(0, 229, 255), width=1)
    
    # Card Central Superior (QA / Tests / CI)
    glow_draw.rectangle([b3_x - 80, b3_y - 45, b3_x + 80, b3_y + 45], fill=(16, 22, 32, 235), outline=(255, 255, 255), width=2)
    glow_draw.rectangle([b3_x - 75, b3_y - 40, b3_x + 75, b3_y - 18], fill=(20, 40, 60), outline=(0, 229, 255), width=1)
    glow_draw.line([(b3_x - 55, b3_y - 29), (b3_x + 35, b3_y - 29)], fill=(0, 229, 255), width=2)
    glow_draw.line([(b3_x - 55, b3_y), (b3_x + 45, b3_y)], fill=(223, 186, 107), width=2)
    glow_draw.line([(b3_x - 55, b3_y + 18), (b3_x + 15, b3_y + 18)], fill=(0, 229, 255), width=2)

    # Mini-busto QA com auréola superior
    glow_draw.ellipse([b3_x - 18, b3_y - 80, b3_x + 18, b3_y - 48], fill=(30, 40, 55), outline=(255, 255, 255), width=2)
    for r in range(40, 10, -8):
        glow_draw.ellipse([b3_x - r, b3_y - 65 - r * 0.7, b3_x + r, b3_y - 65 + r * 0.7], outline=(0, 229, 255, 75), width=1)

    # 5. O BUSTO CLÁSSICO DE HERMES EM MÁRMORE (The Master Architect)
    # Posicionado elegantemente ao centro-baixo, como guardião da arquitetura
    c_x, c_y = 600, 520
    # Halo Dourado & Ciano de Hermes
    for r in range(95, 15, -10):
        alpha = int(32 * (1 - r / 95))
        glow_draw.ellipse([c_x - r, c_y - r * 0.9, c_x + r, c_y + r * 0.9], fill=(223, 186, 107, alpha))
        
    # Torso & Manto Neoclássico
    glow_draw.polygon([
        (c_x - 50, c_y + 65), (c_x - 30, c_y + 15), (c_x + 30, c_y + 15), 
        (c_x + 50, c_y + 65), (c_x, c_y + 75)
    ], fill=(22, 32, 46, 240), outline=(220, 235, 250), width=2)
    
    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([c_x - 24, c_y - 35, c_x + 24, c_y + 10], fill=(28, 38, 52), outline=(215, 230, 245), width=2)
    
    # Elmo Alado de Hermes (Petasos com Asas Ciano e Ouro)
    glow_draw.arc([c_x - 32, c_y - 48, c_x + 32, c_y - 15], start=180, end=0, fill=(0, 229, 255), width=2)
    glow_draw.polygon([(c_x - 22, c_y - 28), (c_x - 50, c_y - 52), (c_x - 30, c_y - 38)], fill=(0, 229, 255, 210), outline=(220, 245, 255), width=1)
    glow_draw.polygon([(c_x + 22, c_y - 28), (c_x + 50, c_y - 52), (c_x + 30, c_y - 38)], fill=(223, 186, 107, 210), outline=(255, 235, 180), width=1)

    # 6. BADGES DE GOVERNANÇA (Stale Worktree Sweep & Auto-Archive)
    # Badge Esquerda: hermes -w: ZERO LOCK COLLISION
    glow_draw.rectangle([180, 725, 430, 765], fill=(8, 16, 26, 240), outline=(0, 229, 255), width=2)
    glow_draw.line([(195, 745), (415, 745)], fill=(0, 229, 255), width=2)
    glow_draw.ellipse([410, 741, 418, 749], fill=(0, 229, 255))
    
    # Badge Direita: STALE SWEEP // 6H AUTO-ARCHIVE
    glow_draw.rectangle([770, 725, 1020, 765], fill=(26, 20, 10, 240), outline=(223, 186, 107), width=2)
    glow_draw.line([(785, 745), (1005, 745)], fill=(223, 186, 107), width=2)
    glow_draw.ellipse([785, 741, 793, 749], fill=(223, 186, 107))
    
    # Fusão com imagem base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Aplica um suave anti-aliasing / filtro de refinamento
    im = im.filter(ImageFilter.SMOOTH_MORE)
    
    # Salva no diretório de imagens do blog
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\git-worktrees-paralelismo-multi-agente-hermes.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_worktrees_cover()
