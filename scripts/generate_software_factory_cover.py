import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_software_factory_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Kanban Nativo, Especificação de Requisitos, Mapeamento #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Orca ADE, Forja de Código, Git Worktrees #DFBA6B)
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
    col1_x = 75
    col_w = 52
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(90, 215, 245, 60), width=2)
    glow_draw.rectangle([col1_x - 14, 90, col1_x + col_w + 14, 120], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 740, col1_x + col_w + 16, 775], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Externa Direita (Ouro)
    col2_x = 1072
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(215, 190, 115, 60), width=2)
    glow_draw.rectangle([col2_x - 14, 90, col2_x + col_w + 14, 120], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 740, col2_x + col_w + 16, 775], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)

    # Coluna Interna Esquerda (Ciano)
    col3_x = 225
    col3_w = 38
    for fl in range(4):
        fl_x = col3_x + fl * 10
        glow_draw.line([(fl_x, 130), (fl_x, 730)], fill=(80, 200, 230, 45), width=2)
    glow_draw.rectangle([col3_x - 10, 115, col3_x + col3_w + 10, 140], fill=(10, 30, 42, 180), outline=(0, 210, 240, 170), width=2)
    glow_draw.rectangle([col3_x - 12, 715, col3_x + col3_w + 12, 745], fill=(10, 30, 42, 180), outline=(0, 210, 240, 170), width=2)

    # Coluna Interna Direita (Ouro)
    col4_x = 935
    for fl in range(4):
        fl_x = col4_x + fl * 10
        glow_draw.line([(fl_x, 130), (fl_x, 730)], fill=(205, 180, 105, 45), width=2)
    glow_draw.rectangle([col4_x - 10, 115, col4_x + col3_w + 10, 140], fill=(36, 30, 12, 180), outline=(215, 180, 105, 170), width=2)
    glow_draw.rectangle([col4_x - 12, 715, col4_x + col3_w + 12, 745], fill=(36, 30, 12, 180), outline=(215, 180, 105, 170), width=2)

    # Frontão Clássico Superior
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)
    
    # 3. ELEMENTOS THEMATICS: KANBAN NATIVO (ESQUERDA) & FORJA DE CÓDIGO ORCA ADE (DIREITA)
    # Lado Esquerdo: Painel Kanban Holográfico (Ciano #00E5FF)
    # Coluna Kanban 1: [BACKLOG]
    glow_draw.rectangle([135, 210, 215, 490], fill=(8, 22, 34, 170), outline=(0, 229, 255, 190), width=1)
    glow_draw.rectangle([135, 210, 215, 235], fill=(0, 229, 255, 60))
    # Cards no Backlog
    glow_draw.rectangle([142, 245, 208, 285], fill=(12, 32, 48, 200), outline=(0, 229, 255, 140), width=1)
    glow_draw.rectangle([142, 295, 208, 335], fill=(12, 32, 48, 200), outline=(0, 229, 255, 140), width=1)
    glow_draw.rectangle([142, 345, 208, 385], fill=(12, 32, 48, 200), outline=(0, 229, 255, 140), width=1)
    
    # Coluna Kanban 2: [DOING / WORKTREE]
    glow_draw.rectangle([275, 230, 355, 510], fill=(10, 28, 42, 180), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([275, 230, 355, 255], fill=(0, 229, 255, 90))
    # Cards em Doing com barra de progresso neon
    glow_draw.rectangle([282, 268, 348, 315], fill=(16, 42, 64, 220), outline=(0, 255, 230, 220), width=1)
    glow_draw.line([(286, 305), (336, 305)], fill=(0, 255, 230, 240), width=3)
    glow_draw.rectangle([282, 328, 348, 375], fill=(16, 42, 64, 220), outline=(0, 229, 255, 170), width=1)

    # Lado Direito: Terminal / Forja Orca ADE & Git Worktrees (Ouro #DFBA6B)
    glow_draw.rectangle([845, 230, 925, 510], fill=(32, 26, 12, 180), outline=(223, 186, 107, 220), width=2)
    glow_draw.rectangle([845, 230, 925, 255], fill=(223, 186, 107, 90))
    # Linhas de código / AST syntax blocks
    for cy_block in [270, 315, 360, 405, 450]:
        glow_draw.rectangle([852, cy_block, 918, cy_block + 32], fill=(48, 38, 16, 210), outline=(223, 186, 107, 180), width=1)
        glow_draw.line([(858, cy_block + 10), (895, cy_block + 10)], fill=(255, 235, 170, 220), width=2)
        glow_draw.line([(864, cy_block + 20), (908, cy_block + 20)], fill=(223, 186, 107, 180), width=1)

    # Painel de Worktree / Git Branch
    glow_draw.rectangle([985, 210, 1065, 490], fill=(24, 20, 10, 170), outline=(223, 186, 107, 190), width=1)
    glow_draw.rectangle([985, 210, 1065, 235], fill=(223, 186, 107, 60))
    # Nós de Git Branch / Commits
    for gy in [260, 310, 360, 410, 460]:
        glow_draw.ellipse([1020, gy, 1032, gy + 12], fill=(255, 230, 140, 240), outline=(223, 186, 107, 255))
        if gy < 460:
            glow_draw.line([(1026, gy + 12), (1026, gy + 50)], fill=(223, 186, 107, 160), width=2)

    # 4. CENTRO: BUSTO DE HERMES ARQUITETO & HALO DE ORQUESTRAÇÃO
    cx, cy = 600, 380
    
    # Halo de anéis concêntricos de orquestração agêntica (Kanban <-> Coder)
    for r in [280, 230, 180, 130]:
        alpha_ring = int(140 * (1 - r / 320))
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=100, end=260, fill=(0, 229, 255, alpha_ring), width=2)
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=280, end=80, fill=(223, 186, 107, alpha_ring), width=2)

    # Nós orbitais conectando Kanban e Orca
    for ang in [25, 70, 115, 160, 205, 250, 295, 340]:
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

    # 5. ÍCONE DE SOFTWARE FACTORY NO PEDESTAL: Simbolo de Código < / > com Chaves e Kanban Matrix
    code_y = cy + 62
    # < no lado esquerdo (Ciano)
    glow_draw.line([(cx - 24, code_y), (cx - 12, code_y - 14)], fill=(0, 229, 255, 255), width=3)
    glow_draw.line([(cx - 24, code_y), (cx - 12, code_y + 14)], fill=(0, 229, 255, 255), width=3)
    # / no meio (Split)
    glow_draw.line([(cx + 4, code_y - 16), (cx - 4, code_y + 16)], fill=(255, 255, 255, 240), width=2)
    # > no lado direito (Ouro)
    glow_draw.line([(cx + 24, code_y), (cx + 12, code_y - 14)], fill=(223, 186, 107, 255), width=3)
    glow_draw.line([(cx + 24, code_y), (cx + 12, code_y + 14)], fill=(223, 186, 107, 255), width=3)

    # 6. FILAMENTOS DE CONEXÃO NEURAL LIGANDO HERMES AO KANBAN E AO ORCA ADE
    for sy in [260, 320, 380, 440]:
        glow_draw.line([(cx - 75, cy + 40), (355, sy)], fill=(0, 229, 255, 80), width=2)
        glow_draw.line([(cx + 75, cy + 40), (845, sy)], fill=(223, 186, 107, 80), width=2)

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
        font_large = ImageFont.truetype("arialbd.ttf", 32)
        font_sub = ImageFont.truetype("arial.ttf", 17)
        font_tag = ImageFont.truetype("arialbd.ttf", 14)
    except Exception:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    tag_text = "ENGENHARIA AGÊNTICA • ORCA ADE & KANBAN NATIVO • HERMES AGENT"
    title_text = "FÁBRICA DE SOFTWARE AGÊNTICA: DA DEMANDA AO CÓDIGO"
    sub_text = "Como Criar Dashboards, Ferramentas e Automações com Agentes Autônomos Sem Saber Programar"
    
    draw.text((bx + 35, by + 16), tag_text, fill=(223, 186, 107), font=font_tag)
    draw.text((bx + 35, by + 42), title_text, fill=(255, 255, 255), font=font_large)
    draw.text((bx + 35, by + 86), sub_text, fill=(0, 229, 255), font=font_sub)
    
    # Salvar Imagem
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "fabrica-de-software-agentica-hermes-orca-kanban.jpg")
    im.save(out_path, quality=95)
    print(f"✅ Capa da Fábrica de Software gerada com sucesso em: {out_path} (Tamanho: {im.size})")

if __name__ == "__main__":
    create_software_factory_cover()
