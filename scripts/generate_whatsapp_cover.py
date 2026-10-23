import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_whatsapp_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (WhatsApp Chat, Áudio Whisper, QR Code #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Enquetes Polls, Despacho Docs, Governança #DFBA6B)
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

    # 4. ELEMENTOS CONTEXTUAIS DO TEMA (ESQUERDA): WHATSAPP CHAT BUBBLE & ÁUDIO TRANSCRIÇÃO (CIANO #00E5FF)
    # Balão de Fala Holográfico WhatsApp
    b_cx, b_cy = 360, 290
    b_w, b_h = 160, 95
    # Caixa principal do balão
    glow_draw.rounded_rectangle([b_cx - b_w//2, b_cy - b_h//2, b_cx + b_w//2, b_cy + b_h//2], radius=16, fill=(10, 36, 52, 225), outline=(0, 229, 255, 240), width=2)
    # Rabicho do balão apontando para o centro
    bubble_tail = [(b_cx + b_w//2 - 6, b_cy + 15), (b_cx + b_w//2 + 22, b_cy + 28), (b_cx + b_w//2 - 6, b_cy + 36)]
    glow_draw.polygon(bubble_tail, fill=(10, 36, 52, 225), outline=(0, 229, 255, 240))

    # Ícone de Áudio / Transcrição Whisper dentro do Balão
    # Botão Play do Áudio
    play_cx, play_cy = b_cx - 52, b_cy
    glow_draw.ellipse([play_cx - 18, play_cy - 18, play_cx + 18, play_cy + 18], fill=(0, 160, 200, 230), outline=(0, 229, 255, 255), width=2)
    glow_draw.polygon([(play_cx - 5, play_cy - 8), (play_cx + 8, play_cy), (play_cx - 5, play_cy + 8)], fill=(255, 255, 255, 255))
    
    # Onda Sonora (Waveform) de Áudio no WhatsApp
    wave_start_x = b_cx - 24
    for i in range(12):
        bx = wave_start_x + i * 7
        # Altura modulada da onda de voz
        bh = int(12 + 16 * math.sin(i * 0.7) * math.cos(i * 0.3))
        bh = max(6, bh)
        glow_draw.line([(bx, play_cy - bh//2), (bx, play_cy + bh//2)], fill=(0, 229, 255, 230), width=3)
    
    # Duração do áudio holográfico
    glow_draw.line([(b_cx - 20, b_cy + 25), (b_cx + 55, b_cy + 25)], fill=(120, 210, 240, 140), width=2)
    # Duas setas azuis de mensagem lida (Blue Ticks)
    tick_x, tick_y = b_cx + 62, b_cy + 25
    glow_draw.line([(tick_x - 6, tick_y), (tick_x - 3, tick_y + 4), (tick_x + 3, tick_y - 4)], fill=(0, 229, 255, 255), width=2)
    glow_draw.line([(tick_x - 2, tick_y), (tick_x + 1, tick_y + 4), (tick_x + 7, tick_y - 4)], fill=(0, 229, 255, 255), width=2)

    # Holograma de QR Code de Pareamento (hermes whatsapp / Baileys)
    qr_cx, qr_cy = 330, 480
    qr_s = 100
    glow_draw.rectangle([qr_cx - qr_s//2, qr_cy - qr_s//2, qr_cx + qr_s//2, qr_cy + qr_s//2], fill=(8, 28, 44, 235), outline=(0, 229, 255, 240), width=2)
    # Molduras dos 3 cantos do QR Code
    for qx, qy in [(qr_cx - 36, qr_cy - 36), (qr_cx + 16, qr_cy - 36), (qr_cx - 36, qr_cy + 16)]:
        glow_draw.rectangle([qx, qy, qx + 20, qy + 20], fill=(12, 45, 68, 240), outline=(0, 229, 255, 255), width=2)
        glow_draw.rectangle([qx + 6, qy + 6, qx + 14, qy + 14], fill=(0, 229, 255, 255))
    # Padrão digital interno simulando QR
    for dot_r in range(3):
        for dot_c in range(3):
            dx = qr_cx + 6 + dot_c * 9
            dy = qr_cy + 6 + dot_r * 9
            if (dot_r + dot_c) % 2 == 0:
                glow_draw.rectangle([dx - 2, dy - 2, dx + 2, dy + 2], fill=(140, 235, 255, 220))
    # Moldura de escaneamento / laser ciano sobre o QR Code
    glow_draw.line([(qr_cx - qr_s//2 + 8, qr_cy), (qr_cx + qr_s//2 - 8, qr_cy)], fill=(255, 255, 255, 220), width=2)

    # Conexão neural ciano do WhatsApp/QR Code até o busto de Hermes
    glow_draw.line([(b_cx + b_w//2 + 22, b_cy + 28), (cx - 90, head_y + 40)], fill=(0, 229, 255, 210), width=2)
    glow_draw.line([(qr_cx + qr_s//2, qr_cy), (cx - 100, head_y + 110)], fill=(0, 229, 255, 180), width=2)

    # 5. ELEMENTOS CONTEXTUAIS DO TEMA (DIREITA): ENQUETES NATIVAS & DESPACHO DE DOCUMENTOS (OURO #DFBA6B)
    # Card de Enquete Nativa WhatsApp (Polls & Clarify)
    p_cx, p_cy = 830, 290
    p_w, p_h = 160, 115
    glow_draw.rounded_rectangle([p_cx - p_w//2, p_cy - p_h//2, p_cx + p_w//2, p_cy + p_h//2], radius=14, fill=(35, 28, 12, 230), outline=(223, 186, 107, 240), width=2)
    # Cabeçalho da Enquete
    glow_draw.rectangle([p_cx - p_w//2, p_cy - p_h//2, p_cx + p_w//2, p_cy - p_h//2 + 22], fill=(62, 50, 20, 240), outline=(223, 186, 107, 255), width=1)
    glow_draw.line([(p_cx - 55, p_cy - p_h//2 + 11), (p_cx + 40, p_cy - p_h//2 + 11)], fill=(255, 235, 170, 220), width=2)
    
    # 3 Opções de Enquete com Barras de Progresso e Checkbox
    for opt_i in range(3):
        oy = p_cy - p_h//2 + 36 + opt_i * 26
        # Caixa de opção de voto
        glow_draw.ellipse([p_cx - p_w//2 + 14, oy - 7, p_cx - p_w//2 + 28, oy + 7], fill=(24, 18, 8, 220), outline=(223, 186, 107, 240), width=1)
        if opt_i == 0:
            glow_draw.ellipse([p_cx - p_w//2 + 17, oy - 4, p_cx - p_w//2 + 25, oy + 4], fill=(223, 186, 107, 255))
        # Linha de texto da opção
        glow_draw.line([(p_cx - p_w//2 + 36, oy - 2), (p_cx + p_w//2 - 20, oy - 2)], fill=(223, 186, 107, 180), width=2)
        # Barra de porcentagem de votos
        bar_w = 90 if opt_i == 0 else (45 if opt_i == 1 else 20)
        glow_draw.rectangle([p_cx - p_w//2 + 36, oy + 5, p_cx - p_w//2 + 36 + bar_w, oy + 9], fill=(223, 186, 107, 180 if opt_i == 0 else 100))

    # Escudo de Criptografia e Governança Anti-Ban (Direita Inferior)
    sh_cx, sh_cy = 860, 480
    sh_w, sh_h = 110, 115
    # Forma clássica de escudo heráldico / Aegis
    shield_pts = [
        (sh_cx - sh_w//2, sh_cy - sh_h//2),
        (sh_cx + sh_w//2, sh_cy - sh_h//2),
        (sh_cx + sh_w//2, sh_cy + 10),
        (sh_cx, sh_cy + sh_h//2),
        (sh_cx - sh_w//2, sh_cy + 10)
    ]
    glow_draw.polygon(shield_pts, fill=(40, 32, 14, 235), outline=(223, 186, 107, 240), width=2)
    # Linha interna do escudo
    shield_inner = [
        (sh_cx - sh_w//2 + 8, sh_cy - sh_h//2 + 8),
        (sh_cx + sh_w//2 - 8, sh_cy - sh_h//2 + 8),
        (sh_cx + sh_w//2 - 8, sh_cy + 8),
        (sh_cx, sh_cy + sh_h//2 - 10),
        (sh_cx - sh_w//2 + 8, sh_cy + 8)
    ]
    glow_draw.polygon(shield_inner, outline=(255, 235, 170, 190), width=1)
    
    # Cadeado / Ícone de Criptografia no centro do Escudo
    glow_draw.rectangle([sh_cx - 16, sh_cy - 4, sh_cx + 16, sh_cy + 22], fill=(24, 18, 8, 240), outline=(223, 186, 107, 255), width=2)
    glow_draw.arc([sh_cx - 12, sh_cy - 22, sh_cx + 12, sh_cy + 2], start=180, end=0, fill=(255, 235, 170, 255), width=3)
    glow_draw.ellipse([sh_cx - 4, sh_cy + 4, sh_cx + 4, sh_cy + 12], fill=(223, 186, 107, 255))

    # Conexão neural ouro da Enquete/Escudo até o busto de Hermes
    glow_draw.line([(p_cx - p_w//2, p_cy), (cx + 90, head_y + 40)], fill=(223, 186, 107, 210), width=2)
    glow_draw.line([(sh_cx - sh_w//2, sh_cy), (cx + 100, head_y + 110)], fill=(223, 186, 107, 180), width=2)

    # 6. SÍMBOLO CENTRAL: VINCULAÇÃO DE SOCKET E BAILEYS BRIDGE
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
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\whatsapp-agentes-ia-automacao-atendimento-baileys.jpg"
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {output_path}")

if __name__ == "__main__":
    create_whatsapp_cover()
