import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_bi_finance_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Data Queries / Analytics Streams)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Capital / Profit / Financial Prosperity)
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
    
    # 3. CENTRO: BUSTO DE HERMES & BALANÇA CLÁSSICA DE PRECISÃO FINANCEIRA
    cx, cy = 600, 380
    
    # Halo de energia e anéis de dados financeiros em órbita
    for r in [260, 210, 160, 110]:
        alpha_ring = int(130 * (1 - r / 300))
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=100, end=260, fill=(0, 229, 255, alpha_ring), width=2)
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=280, end=80, fill=(223, 186, 107, alpha_ring), width=2)

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
    glow_draw.line([(cx + 35, head_y - 45), (cx + 105, head_y - 110)], fill=(255, 255, 255, 220), width=2)

    # Base do Busto / Tronco Clássico
    chest = [(cx - 55, head_y + 40), (cx + 55, head_y + 40), (cx + 70, head_y + 115), (cx - 70, head_y + 115)]
    glow_draw.polygon(chest, fill=(20, 25, 34, 230), outline=(180, 200, 220, 180), width=2)
    
    # Pedestal de Mármore
    ped_top = head_y + 115
    glow_draw.rectangle([cx - 85, ped_top, cx + 85, ped_top + 30], fill=(28, 34, 45, 240), outline=(200, 220, 240, 190), width=2)
    glow_draw.rectangle([cx - 70, ped_top + 30, cx + 70, ped_top + 140], fill=(20, 25, 35, 240), outline=(170, 195, 220, 170), width=2)
    glow_draw.rectangle([cx - 95, ped_top + 140, cx + 95, ped_top + 175], fill=(28, 34, 45, 240), outline=(200, 220, 240, 190), width=2)

    # 4. ELEMENTO CENTRAL DO TEMA: BALANÇA CLÁSSICA DE PRECISÃO & GRÁFICOS HOLOGRÁFICOS
    # Haste da balança
    scale_y = head_y + 160
    # Eixo horizontal da balança
    scale_left_x = cx - 210
    scale_right_x = cx + 210
    
    # Barra da Balança
    glow_draw.line([(scale_left_x, scale_y - 20), (scale_right_x, scale_y + 20)], fill=(223, 186, 107, 240), width=4)
    glow_draw.ellipse([cx - 10, scale_y - 10, cx + 10, scale_y + 10], fill=(255, 215, 0, 255), outline=(255, 255, 255, 255), width=2)
    
    # Fios da Balança Esquerda (Prato Ciano - Dados / BI / Consultas)
    glow_draw.line([(scale_left_x, scale_y - 20), (scale_left_x - 45, scale_y + 90)], fill=(0, 229, 255, 210), width=2)
    glow_draw.line([(scale_left_x, scale_y - 20), (scale_left_x + 45, scale_y + 90)], fill=(0, 229, 255, 210), width=2)
    # Prato Esquerdo
    glow_draw.arc([scale_left_x - 55, scale_y + 80, scale_left_x + 55, scale_y + 110], start=0, end=180, fill=(0, 229, 255, 240), width=3)
    glow_draw.line([(scale_left_x - 55, scale_y + 95), (scale_left_x + 55, scale_y + 95)], fill=(0, 229, 255, 240), width=2)
    
    # Cubos e Tabelas Holográficas de Dados no Prato Esquerdo
    for offset_box, h_box in [(-25, 25), (0, 38), (25, 20)]:
        bx = scale_left_x + offset_box
        by = scale_y + 90 - h_box
        glow_draw.rectangle([bx - 10, by, bx + 10, scale_y + 92], fill=(10, 45, 60, 200), outline=(0, 229, 255, 240), width=2)
        # Linhas de dados dentro do bloco
        for ly in range(by + 5, scale_y + 90, 6):
            glow_draw.line([(bx - 7, ly), (bx + 7, ly)], fill=(0, 240, 255, 180), width=1)
            
    # Fios da Balança Direita (Prato Ouro - Lucro / Margem / Capital)
    glow_draw.line([(scale_right_x, scale_y + 20), (scale_right_x - 45, scale_y + 130)], fill=(223, 186, 107, 210), width=2)
    glow_draw.line([(scale_right_x, scale_y + 20), (scale_right_x + 45, scale_y + 130)], fill=(223, 186, 107, 210), width=2)
    # Prato Direito
    glow_draw.arc([scale_right_x - 55, scale_y + 120, scale_right_x + 55, scale_y + 150], start=0, end=180, fill=(223, 186, 107, 240), width=3)
    glow_draw.line([(scale_right_x - 55, scale_y + 135), (scale_right_x + 55, scale_y + 135)], fill=(223, 186, 107, 240), width=2)
    
    # Moedas de Ouro Holográficas no Prato Direito
    for offset_coin, coin_y_offset in [(-20, 10), (0, 18), (20, 8), (-8, 26), (12, 28)]:
        coin_cx = scale_right_x + offset_coin
        coin_cy = scale_y + 132 - coin_y_offset
        glow_draw.ellipse([coin_cx - 14, coin_cy - 7, coin_cx + 14, coin_cy + 7], fill=(50, 42, 15, 230), outline=(255, 215, 0, 255), width=2)
        glow_draw.ellipse([coin_cx - 8, coin_cy - 4, coin_cx + 8, coin_cy + 4], outline=(223, 186, 107, 200), width=1)

    # 5. GRÁFICOS HOLOGRÁFICOS FLUTUANTES (BI Analytics)
    # Painel Holográfico Esquerdo (Ciano - Gráfico de Linhas de Desempenho)
    panel1_x, panel1_y = 120, 320
    glow_draw.rectangle([panel1_x, panel1_y, panel1_x + 160, panel1_y + 110], fill=(8, 25, 35, 180), outline=(0, 229, 255, 200), width=2)
    # Linhas de grade do gráfico
    for gy in range(panel1_y + 20, panel1_y + 100, 20):
        glow_draw.line([(panel1_x + 10, gy), (panel1_x + 150, gy)], fill=(0, 180, 210, 50), width=1)
    # Linha de tendência analítica ascendente
    pts = [(panel1_x + 15, panel1_y + 85), (panel1_x + 45, panel1_y + 70), (panel1_x + 80, panel1_y + 75), 
           (panel1_x + 115, panel1_y + 40), (panel1_x + 145, panel1_y + 25)]
    for i in range(len(pts) - 1):
        glow_draw.line([pts[i], pts[i+1]], fill=(0, 240, 255, 255), width=3)
        glow_draw.ellipse([pts[i][0]-3, pts[i][1]-3, pts[i][0]+3, pts[i][1]+3], fill=(255, 255, 255, 255))
    glow_draw.ellipse([pts[-1][0]-4, pts[-1][1]-4, pts[-1][0]+4, pts[-1][1]+4], fill=(255, 255, 255, 255))

    # Painel Holográfico Direito (Ouro - Gráfico de Barras Financeiras)
    panel2_x, panel2_y = 920, 320
    glow_draw.rectangle([panel2_x, panel2_y, panel2_x + 160, panel2_y + 110], fill=(32, 26, 12, 180), outline=(223, 186, 107, 200), width=2)
    # Barras de crescimento financeiro
    bars = [35, 50, 42, 68, 85]
    for idx, b_val in enumerate(bars):
        bx = panel2_x + 20 + idx * 26
        by = panel2_y + 95 - b_val
        glow_draw.rectangle([bx, by, bx + 16, panel2_y + 95], fill=(70, 58, 22, 220), outline=(255, 215, 0, 240), width=2)
        glow_draw.line([(bx + 3, by + 3), (bx + 13, by + 3)], fill=(255, 255, 255, 200), width=1)

    # Conectar os painéis ao busto central com filamentos de luz
    glow_draw.line([(panel1_x + 160, panel1_y + 55), (cx - 95, head_y + 140)], fill=(0, 229, 255, 120), width=2)
    glow_draw.line([(panel2_x, panel2_y + 55), (cx + 95, head_y + 140)], fill=(223, 186, 107, 120), width=2)

    # 6. TÍTULO E SELO INFERIOR
    # Banner estilizado
    glow_draw.rectangle([280, 780, 920, 850], fill=(12, 16, 22, 230), outline=(180, 205, 225, 160), width=2)
    # Borda split ciano e ouro
    glow_draw.line([(280, 780), (600, 780)], fill=(0, 229, 255, 240), width=3)
    glow_draw.line([(600, 780), (920, 780)], fill=(223, 186, 107, 240), width=3)
    glow_draw.line([(280, 850), (600, 850)], fill=(0, 229, 255, 240), width=3)
    glow_draw.line([(600, 850), (920, 850)], fill=(223, 186, 107, 240), width=3)
    
    # Texto executivo no banner
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 28)
        font_sub = ImageFont.truetype("arial.ttf", 16)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    text_main = "BI CONVERSACIONAL & FINANÇAS AUTÔNOMAS"
    text_sub = "HERMES AGENT • ANÁLISE EM TEMPO REAL • PROTOCOLO MCP SQL"
    
    glow_draw.text((600, 804), text_main, fill=(255, 255, 255, 240), font=font_main, anchor="mm")
    glow_draw.text((600, 832), text_sub, fill=(180, 215, 235, 200), font=font_sub, anchor="mm")

    # Blend glow with base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Salvar em static/images
    dest_path = r"D:\DevCod\inteligencia-agentica\static\images\bi-conversacional-analise-financeira-agentes-ia.jpg"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    im.save(dest_path, "JPEG", quality=95)
    print(f"✅ Imagem salva com sucesso em: {dest_path}")
    return dest_path

if __name__ == "__main__":
    create_bi_finance_cover()
