import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_google_workspace_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Gmail, Calendar, Daily Briefing, Triagem #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Google Sheets, Drive, Documentos, Gestão #DFBA6B)
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
    
    # 3. NÚCLEO CENTRAL & BUSTO DE HERMES
    cx, cy = 600, 400
    head_y = cy - 70
    
    # Anéis de sincronização e órbitas neurais
    for r in [250, 210, 170, 130, 90]:
        alpha_ring = int(120 * (1 - r / 280))
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270, fill=(0, 229, 255, alpha_ring), width=2)
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=270, end=90, fill=(223, 186, 107, alpha_ring), width=2)
        
    # Halo luminoso atrás da cabeça
    for r in range(95, 10, -5):
        glow_draw.ellipse([cx - r, head_y - r, cx + r, head_y + r], fill=(15, 25, 35, 170), outline=(0, 229, 255, int(110 * (1 - r / 95))), width=1)
        
    # Cabeça esculpida em Mármore
    glow_draw.ellipse([cx - 45, head_y - 55, cx + 45, head_y + 45], fill=(22, 28, 38, 245), outline=(200, 220, 240, 210), width=2)
    # Split-lighting no perfil de Hermes
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=90, end=270, fill=(0, 229, 255, 255), width=3)
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=270, end=90, fill=(223, 186, 107, 255), width=3)
    
    # Elmo Alado de Hermes
    wing_left = [(cx - 35, head_y - 45), (cx - 110, head_y - 115), (cx - 75, head_y - 50), (cx - 100, head_y - 30), (cx - 40, head_y - 20)]
    glow_draw.polygon(wing_left, fill=(10, 45, 60, 225), outline=(0, 229, 255, 255))
    glow_draw.line([(cx - 35, head_y - 45), (cx - 105, head_y - 110)], fill=(255, 255, 255, 230), width=2)

    wing_right = [(cx + 35, head_y - 45), (cx + 110, head_y - 115), (cx + 75, head_y - 50), (cx + 100, head_y - 30), (cx + 40, head_y - 20)]
    glow_draw.polygon(wing_right, fill=(50, 40, 15, 225), outline=(223, 186, 107, 255))
    glow_draw.line([(cx + 35, head_y - 45), (cx + 105, head_y - 110)], fill=(255, 245, 200, 230), width=2)

    # Ombros e Tronco em Mármore
    torso = [(cx - 110, head_y + 160), (cx - 65, head_y + 40), (cx + 65, head_y + 40), (cx + 110, head_y + 160), (cx, head_y + 190)]
    glow_draw.polygon(torso, fill=(18, 22, 30, 245), outline=(180, 200, 225, 190), width=2)
    glow_draw.line([(cx, head_y + 40), (cx, head_y + 185)], fill=(120, 150, 180, 130), width=2)
    glow_draw.line([(cx - 70, head_y + 120), (cx, head_y + 150)], fill=(0, 229, 255, 160), width=2)
    glow_draw.line([(cx + 70, head_y + 120), (cx, head_y + 150)], fill=(223, 186, 107, 160), width=2)

    # Pedestal Clássico de Mármore
    glow_draw.rectangle([cx - 95, head_y + 190, cx + 95, head_y + 245], fill=(14, 18, 25, 240), outline=(150, 180, 210, 180), width=2)
    glow_draw.rectangle([cx - 120, head_y + 245, cx + 120, head_y + 270], fill=(10, 14, 20, 250), outline=(180, 210, 235, 200), width=2)

    # 4. ELEMENTOS CONTEXTUAIS DO TEMA (ESQUERDA): GMAIL & GOOGLE CALENDAR (CIANO #00E5FF)
    # Holograma de Envelope / Mensagem Executiva Gmail
    env_cx, env_cy = 380, 290
    env_w, env_h = 130, 85
    # Caixa do envelope
    glow_draw.rectangle([env_cx - env_w//2, env_cy - env_h//2, env_cx + env_w//2, env_cy + env_h//2], fill=(10, 36, 52, 220), outline=(0, 229, 255, 240), width=2)
    # Dobra superior do envelope
    glow_draw.line([(env_cx - env_w//2, env_cy - env_h//2), (env_cx, env_cy + 8)], fill=(0, 229, 255, 255), width=2)
    glow_draw.line([(env_cx + env_w//2, env_cy - env_h//2), (env_cx, env_cy + 8)], fill=(0, 229, 255, 255), width=2)
    # Linhas de texto interno / email
    glow_draw.line([(env_cx - 40, env_cy + 18), (env_cx + 40, env_cy + 18)], fill=(160, 240, 255, 190), width=2)
    glow_draw.line([(env_cx - 40, env_cy + 28), (env_cx + 20, env_cy + 28)], fill=(160, 240, 255, 140), width=2)
    
    # Calendário Holográfico / Daily Briefing Dial
    cal_cx, cal_cy = 340, 470
    cal_w, cal_h = 120, 100
    glow_draw.rectangle([cal_cx - cal_w//2, cal_cy - cal_h//2, cal_cx + cal_w//2, cal_cy + cal_h//2], fill=(8, 30, 45, 230), outline=(0, 229, 255, 230), width=2)
    # Topo do calendário (barra de agendamento)
    glow_draw.rectangle([cal_cx - cal_w//2, cal_cy - cal_h//2, cal_cx + cal_w//2, cal_cy - cal_h//2 + 22], fill=(15, 60, 85, 240), outline=(0, 229, 255, 255), width=2)
    # Anéis de espiral do calendário
    for bx in [-35, -12, 12, 35]:
        glow_draw.rectangle([cal_cx + bx - 4, cal_cy - cal_h//2 - 6, cal_cx + bx + 4, cal_cy - cal_h//2 + 4], fill=(220, 245, 255, 255), outline=(0, 229, 255, 255))
    # Grade de dias do calendário
    for row in range(3):
        gy = cal_cy - cal_h//2 + 36 + row * 18
        for col in range(4):
            gx = cal_cx - cal_w//2 + 18 + col * 26
            glow_draw.rectangle([gx - 7, gy - 6, gx + 7, gy + 6], fill=(12, 42, 60, 180), outline=(0, 210, 240, 150), width=1)
    # Marcador de reunião ativa em Ciano pulsante
    glow_draw.rectangle([cal_cx - cal_w//2 + 18 + 2 * 26 - 7, cal_cy - cal_h//2 + 36 + 1 * 18 - 6, cal_cx - cal_w//2 + 18 + 2 * 26 + 7, cal_cy - cal_h//2 + 36 + 1 * 18 + 6], fill=(0, 229, 255, 240), outline=(255, 255, 255, 255), width=1)

    # Conexão neural ciano do Gmail/Calendar até o busto de Hermes
    glow_draw.line([(env_cx + env_w//2, env_cy), (cx - 90, head_y + 40)], fill=(0, 229, 255, 210), width=2)
    glow_draw.line([(cal_cx + cal_w//2, cal_cy), (cx - 100, head_y + 110)], fill=(0, 229, 255, 180), width=2)

    # 5. ELEMENTOS CONTEXTUAIS DO TEMA (DIREITA): GOOGLE SHEETS & GOOGLE DRIVE (OURO #DFBA6B)
    # Tabela Holográfica Google Sheets (Planilha de Gestão Financeira / Operacional)
    sht_cx, sht_cy = 820, 290
    sht_w, sht_h = 140, 95
    glow_draw.rectangle([sht_cx - sht_w//2, sht_cy - sht_h//2, sht_cx + sht_w//2, sht_cy + sht_h//2], fill=(35, 28, 12, 230), outline=(223, 186, 107, 240), width=2)
    # Cabeçalho da planilha
    glow_draw.rectangle([sht_cx - sht_w//2, sht_cy - sht_h//2, sht_cx + sht_w//2, sht_cy - sht_h//2 + 20], fill=(65, 52, 20, 240), outline=(223, 186, 107, 255), width=1)
    # Linhas de grade da planilha
    for row in range(1, 4):
        gy = sht_cy - sht_h//2 + row * 24
        glow_draw.line([(sht_cx - sht_w//2, gy), (sht_cx + sht_w//2, gy)], fill=(223, 186, 107, 180), width=1)
    for col in range(1, 3):
        gx = sht_cx - sht_w//2 + col * 46
        glow_draw.line([(gx, sht_cy - sht_h//2), (gx, sht_cy + sht_h//2)], fill=(223, 186, 107, 180), width=1)
    # Dados celulares holográficos em ouro
    glow_draw.rectangle([sht_cx - sht_w//2 + 6, sht_cy - sht_h//2 + 26, sht_cx - sht_w//2 + 40, sht_cy - sht_h//2 + 42], fill=(223, 186, 107, 180))
    glow_draw.rectangle([sht_cx - sht_w//2 + 52, sht_cy - sht_h//2 + 26, sht_cx - sht_w//2 + 86, sht_cy - sht_h//2 + 42], fill=(223, 186, 107, 120))
    glow_draw.rectangle([sht_cx - sht_w//2 + 6, sht_cy - sht_h//2 + 50, sht_cx - sht_w//2 + 40, sht_cy - sht_h//2 + 66], fill=(223, 186, 107, 120))
    glow_draw.rectangle([sht_cx - sht_w//2 + 98, sht_cy - sht_h//2 + 74, sht_cx - sht_w//2 + 132, sht_cy - sht_h//2 + 90], fill=(255, 235, 170, 220))

    # Documento / Pasta Holográfica Google Drive & Docs
    drv_cx, drv_cy = 860, 470
    drv_w, drv_h = 125, 105
    # Aba de pasta clássica
    glow_draw.polygon([
        (drv_cx - drv_w//2, drv_cy - drv_h//2 + 14),
        (drv_cx - drv_w//2, drv_cy - drv_h//2),
        (drv_cx - drv_w//2 + 45, drv_cy - drv_h//2),
        (drv_cx - drv_w//2 + 60, drv_cy - drv_h//2 + 14),
        (drv_cx + drv_w//2, drv_cy - drv_h//2 + 14),
        (drv_cx + drv_w//2, drv_cy + drv_h//2),
        (drv_cx - drv_w//2, drv_cy + drv_h//2)
    ], fill=(42, 32, 14, 230), outline=(223, 186, 107, 240), width=2)
    # Folha de documento Docs projetando para fora da pasta
    glow_draw.rectangle([drv_cx - 30, drv_cy - drv_h//2 - 18, drv_cx + 45, drv_cy + 20], fill=(25, 20, 10, 240), outline=(255, 235, 170, 230), width=2)
    # Linhas de texto do documento Docs
    for ly in range(drv_cy - drv_h//2 - 8, drv_cy + 10, 8):
        glow_draw.line([(drv_cx - 20, ly), (drv_cx + 35, ly)], fill=(255, 235, 170, 170), width=2)

    # Conexão neural ouro do Sheets/Drive até o busto de Hermes
    glow_draw.line([(sht_cx - sht_w//2, sht_cy), (cx + 90, head_y + 40)], fill=(223, 186, 107, 210), width=2)
    glow_draw.line([(drv_cx - drv_w//2, drv_cy), (cx + 100, head_y + 110)], fill=(223, 186, 107, 180), width=2)

    # 6. SÍMBOLOS FLUTUANTES & ORBITAIS DE SINCRONIZAÇÃO
    # Engrenagem / Ícone de Sincronização e OAuth2 no centro superior
    sync_cx, sync_cy = cx, 170
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        ox = sync_cx + int(math.cos(rad) * 22)
        oy = sync_cy + int(math.sin(rad) * 22)
        glow_draw.ellipse([ox - 4, oy - 4, ox + 4, oy + 4], fill=(255, 255, 255, 210))
    glow_draw.arc([sync_cx - 22, sync_cy - 22, sync_cx + 22, sync_cy + 22], start=45, end=225, fill=(0, 229, 255, 255), width=3)
    glow_draw.arc([sync_cx - 22, sync_cy - 22, sync_cx + 22, sync_cy + 22], start=225, end=45, fill=(223, 186, 107, 255), width=3)

    # 7. PARTÍCULAS E POEIRA DIGITAL DUOCROMÁTICA
    for i in range(160):
        seed_x = (i * 137 + 53) % width
        seed_y = (i * 211 + 67) % (height - 200) + 90
        p_color = (0, 229, 255) if seed_x < 600 else (223, 186, 107)
        p_size = (i % 3) + 1
        p_alpha = 75 + (i % 120)
        glow_draw.ellipse([seed_x, seed_y, seed_x + p_size, seed_y + p_size], fill=(*p_color, p_alpha))

    # 8. MISTURA E COMPOSIÇÃO FINAL
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))
    im.paste(blurred_glow, (0, 0), blurred_glow)
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Salvar imagem
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\google-workspace-agentes-ia-automacao-backoffice-gmail-sheets.jpg"
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {output_path}")

if __name__ == "__main__":
    create_google_workspace_cover()
