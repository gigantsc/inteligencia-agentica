import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_grounded_citations_cover():
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
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO
    # Coluna Esquerda (Mármore Ciano / Evidence Intake & Ledger)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Verbatim Proof & Audit Gate)
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
    
    # Inscrição clássica no frontão: GROUNDED CITATIONS // FACT-CHECKING CHAIN
    glow_draw.rectangle([340, 92, 860, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(360, 102), (840, 102)], fill=(223, 186, 107), width=2)

    # 3. CENTRO: O CONSOLE CENTRAL E O BUSTO CLÁSSICO DE HERMES
    cx, cy = 600, 420

    # Campo de Força Elíptico / Aura Tecnológica
    for r in range(240, 30, -12):
        alpha = int(32 * (1 - r / 240))
        glow_draw.ellipse([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95], fill=(0, 229, 255, alpha))
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 140
    glow_draw.rectangle([cx - 105, ped_y, cx + 105, ped_y + 45], fill=(18, 25, 36), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 125, ped_y + 45, cx + 125, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([cx - 85, ped_y + 14, cx + 85, ped_y + 34], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 70, ped_y + 24), (cx + 70, ped_y + 24)], fill=(223, 186, 107), width=2)

    # Tronco Esculpido de Hermes com Toga Neoclássica
    b_head_y = cy - 35
    torso = [(cx - 90, b_head_y + 145), (cx - 55, b_head_y + 45), (cx + 55, b_head_y + 45), (cx + 90, b_head_y + 145), (cx, b_head_y + 160)]
    glow_draw.polygon(torso, fill=(18, 26, 38, 240), outline=(210, 225, 240, 220), width=2)
    for t_line in range(-40, 45, 18):
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)], fill=(90, 180, 220, 50), width=1)

    # Pescoço e Cabeça Esculpida em Mármore
    glow_draw.rectangle([cx - 18, b_head_y + 20, cx + 18, b_head_y + 50], fill=(24, 32, 44), outline=(180, 210, 230), width=1)
    glow_draw.ellipse([cx - 38, b_head_y - 45, cx + 38, b_head_y + 25], fill=(26, 36, 50), outline=(210, 230, 245), width=2)
    
    # Elmo Alado Clássico (Petasos com Asas Ciano e Douradas)
    glow_draw.arc([cx - 48, b_head_y - 65, cx + 48, b_head_y - 20], start=180, end=0, fill=(0, 229, 255), width=2)
    glow_draw.polygon([(cx - 38, b_head_y - 35), (cx - 78, b_head_y - 65), (cx - 48, b_head_y - 50)], fill=(0, 229, 255, 180), outline=(220, 245, 255), width=1)
    glow_draw.polygon([(cx + 38, b_head_y - 35), (cx + 78, b_head_y - 65), (cx + 48, b_head_y - 50)], fill=(223, 186, 107, 180), outline=(255, 235, 180), width=1)

    # Circuitos Neurais Fluindo do Busto
    for angle in range(0, 360, 40):
        rad = math.radians(angle)
        x1 = cx + int(55 * math.cos(rad))
        y1 = cy - 20 + int(55 * math.sin(rad))
        x2 = cx + int(115 * math.cos(rad))
        y2 = cy - 20 + int(115 * math.sin(rad))
        glow_draw.line([(x1, y1), (x2, y2)], fill=(0, 229, 255, 140), width=1)
        glow_draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(223, 186, 107, 200))

    # 4. ELEMENTOS DO TEMA: LIVRO-RAZÃO HOLOGRÁFICO & BALANÇA DA VERDADE (PROVAS AUDITÁVEIS)
    
    # 4.1. Painel Flutuante Esquerdo: Mechanical Ledger [1], [2], [3] (Cyan Glow)
    p1_x, p1_y = 260, 360
    p1_w, p1_h = 135, 170
    glow_draw.rectangle([p1_x - p1_w, p1_y - p1_h, p1_x + p1_w, p1_y + p1_h], fill=(10, 22, 34, 210), outline=(0, 229, 255, 220), width=2)
    # Header do painel
    glow_draw.rectangle([p1_x - p1_w, p1_y - p1_h, p1_x + p1_w, p1_y - p1_h + 30], fill=(0, 80, 120, 230), outline=(0, 229, 255), width=1)
    glow_draw.rectangle([p1_x - p1_w + 15, p1_y - p1_h + 8, p1_x + p1_w - 15, p1_y - p1_h + 22], fill=(4, 12, 18), outline=(0, 229, 255), width=1)
    
    # Registros do Ledger [1], [2], [3]
    for idx, badge_y in enumerate([p1_y - 100, p1_y - 35, p1_y + 30, p1_y + 95]):
        # Caixa de tag numérica [1], [2]...
        glow_draw.rectangle([p1_x - p1_w + 16, badge_y - 14, p1_x - p1_w + 48, badge_y + 14], fill=(0, 229, 255, 45), outline=(0, 229, 255), width=1)
        glow_draw.ellipse([p1_x - p1_w + 28, badge_y - 4, p1_x - p1_w + 36, badge_y + 4], fill=(0, 229, 255))
        # Linhas de metadados simulando URLs auditadas
        glow_draw.line([(p1_x - p1_w + 58, badge_y - 6), (p1_x + p1_w - 18, badge_y - 6)], fill=(120, 220, 255, 190), width=2)
        glow_draw.line([(p1_x - p1_w + 58, badge_y + 6), (p1_x + p1_w - 40, badge_y + 6)], fill=(80, 160, 200, 120), width=1)
        
    # Filamentos conectando o Ledger esquerdo ao Busto
    glow_draw.line([(p1_x + p1_w, p1_y - 35), (cx - 90, cy - 20)], fill=(0, 229, 255, 160), width=2)
    glow_draw.line([(p1_x + p1_w, p1_y + 30), (cx - 70, cy + 30)], fill=(0, 229, 255, 120), width=1)

    # 4.2. Painel Flutuante Direito: Verbatim Proof & Audit Checkpoint (Gold Glow)
    p2_x, p2_y = 940, 360
    p2_w, p2_h = 135, 170
    glow_draw.rectangle([p2_x - p2_w, p2_y - p2_h, p2_x + p2_w, p2_y + p2_h], fill=(32, 26, 14, 210), outline=(223, 186, 107, 220), width=2)
    # Header do painel
    glow_draw.rectangle([p2_x - p2_w, p2_y - p2_h, p2_x + p2_w, p2_y - p2_h + 30], fill=(100, 80, 28, 230), outline=(223, 186, 107), width=1)
    glow_draw.rectangle([p2_x - p2_w + 15, p2_y - p2_h + 8, p2_x + p2_w - 15, p2_y - p2_h + 22], fill=(18, 14, 6), outline=(223, 186, 107), width=1)
    
    # Bloco Verbatim Quotes & Selo de Aprovação Auditado [✓]
    for idx, v_y in enumerate([p2_y - 95, p2_y - 30, p2_y + 35]):
        glow_draw.rectangle([p2_x - p2_w + 16, v_y - 12, p2_x + p2_w - 16, v_y + 16], fill=(16, 12, 6, 180), outline=(223, 186, 107, 100), width=1)
        # Símbolo de aspas / verbatim quote
        glow_draw.arc([p2_x - p2_w + 24, v_y - 8, p2_x - p2_w + 34, v_y + 2], start=180, end=0, fill=(223, 186, 107), width=2)
        glow_draw.line([(p2_x - p2_w + 40, v_y + 2), (p2_x + p2_w - 24, v_y + 2)], fill=(235, 205, 135, 180), width=2)

    # Selo de Verificação Inferior: VERIFIED --MIN-COVERAGE 100%
    glow_draw.rectangle([p2_x - 85, p2_y + 88, p2_x + 85, p2_y + 138], fill=(28, 22, 10), outline=(223, 186, 107), width=2)
    # Ícone Checkmark em Ouro
    glow_draw.line([(p2_x - 22, p2_y + 112), (p2_x - 6, p2_y + 126)], fill=(223, 186, 107), width=3)
    glow_draw.line([(p2_x - 6, p2_y + 126), (p2_x + 22, p2_y + 98)], fill=(223, 186, 107), width=3)

    # Filamentos conectando o Busto ao Painel de Auditoria direito
    glow_draw.line([(cx + 90, cy - 20), (p2_x - p2_w, p2_y - 30)], fill=(223, 186, 107, 160), width=2)
    glow_draw.line([(cx + 70, cy + 30), (p2_x - p2_w, p2_y + 35)], fill=(223, 186, 107, 120), width=1)

    # 4.3. SÍMBOLO CENTRAL: A BALANÇA DA VERDADE HOLOGRÁFICA (METÁFORA DA PRECISÃO FACTUAL)
    # Haste central da balança flutuando acima do peito de Hermes
    scale_y = cy - 135
    glow_draw.line([(cx, scale_y - 45), (cx, scale_y + 35)], fill=(215, 230, 245), width=3)
    glow_draw.ellipse([cx - 9, scale_y - 54, cx + 9, scale_y - 36], fill=(0, 229, 255), outline=(223, 186, 107), width=2)
    # Travessão horizontal equilibrado
    glow_draw.line([(cx - 85, scale_y - 30), (cx + 85, scale_y - 30)], fill=(223, 186, 107), width=3)
    
    # Prato Esquerdo (Ciano / Evidência)
    glow_draw.line([(cx - 80, scale_y - 30), (cx - 105, scale_y + 15)], fill=(0, 229, 255, 160), width=1)
    glow_draw.line([(cx - 80, scale_y - 30), (cx - 55, scale_y + 15)], fill=(0, 229, 255, 160), width=1)
    glow_draw.arc([cx - 110, scale_y + 10, cx - 50, scale_y + 28], start=0, end=180, fill=(0, 229, 255), width=2)
    glow_draw.ellipse([cx - 84, scale_y + 10, cx - 76, scale_y + 18], fill=(0, 229, 255))
    
    # Prato Direito (Dourado / Fato Comprovado)
    glow_draw.line([(cx + 80, scale_y - 30), (cx + 55, scale_y + 15)], fill=(223, 186, 107, 160), width=1)
    glow_draw.line([(cx + 80, scale_y - 30), (cx + 105, scale_y + 15)], fill=(223, 186, 107, 160), width=1)
    glow_draw.arc([cx + 50, scale_y + 10, cx + 110, scale_y + 28], start=0, end=180, fill=(223, 186, 107), width=2)
    glow_draw.ellipse([cx + 76, scale_y + 10, cx + 84, scale_y + 18], fill=(223, 186, 107))

    # 5. Partículas flutuantes de dados (Data Orbs)
    for px, py, pcol in [
        (200, 220, (0, 229, 255)), (340, 160, (0, 229, 255)), (480, 250, (0, 229, 255)),
        (720, 250, (223, 186, 107)), (860, 160, (223, 186, 107)), (1000, 220, (223, 186, 107)),
        (450, 520, (0, 229, 255)), (750, 520, (223, 186, 107))
    ]:
        glow_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=pcol)
        glow_draw.ellipse([px - 10, py - 10, px + 10, py + 10], outline=(pcol[0], pcol[1], pcol[2], 80), width=1)

    # 6. Composição final e suavização de glow
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=2))
    im.paste(blurred_glow, (0, 0), blurred_glow)
    
    # Sobrepõe linhas nítidas
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Salvar no diretório estático
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\grounded-citations-fact-checking-hermes.jpg"
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem contextual salva com sucesso em: {output_path}")
    print(f"📐 Dimensões: {im.size[0]}x{im.size[1]}px (Aspect Ratio 4:3 fit)")

if __name__ == "__main__":
    create_grounded_citations_cover()
