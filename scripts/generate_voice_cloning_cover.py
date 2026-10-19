import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_voice_cloning_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Amostra Acústica Humana, Captura de Frequências #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Omnivoice, Síntese Neural Hiper-Realista #DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid (perspective grid)
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore)
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
    
    # Anéis de ondas sonoras esféricas e emissão acústica
    for r in [250, 210, 170, 130, 90]:
        alpha_ring = int(130 * (1 - r / 280))
        # Hemisfério esquerdo em Ciano, direito em Ouro
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270, fill=(0, 229, 255, alpha_ring), width=2)
        glow_draw.arc([cx - r, cy - r, cx + r, cy + r], start=270, end=90, fill=(223, 186, 107, alpha_ring), width=2)
        
    # Halo luminoso atrás da cabeça de Hermes
    for r in range(95, 10, -5):
        glow_draw.ellipse([cx - r, head_y - r, cx + r, head_y + r], fill=(15, 25, 35, 170), outline=(0, 229, 255, int(110 * (1 - r / 95))), width=1)
        
    # Busto / Cabeça esculpida em Mármore Estilizado
    glow_draw.ellipse([cx - 45, head_y - 55, cx + 45, head_y + 45], fill=(22, 28, 38, 245), outline=(200, 220, 240, 210), width=2)
    # Split-lighting no perfil de Hermes
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=90, end=270, fill=(0, 229, 255, 255), width=3)
    glow_draw.arc([cx - 40, head_y - 50, cx + 40, head_y + 40], start=270, end=90, fill=(223, 186, 107, 255), width=3)
    
    # Elmo Alado de Hermes (Winged Helmet)
    # Asa Esquerda (Ciano)
    wing_left = [(cx - 35, head_y - 45), (cx - 110, head_y - 115), (cx - 75, head_y - 50), (cx - 100, head_y - 30), (cx - 40, head_y - 20)]
    glow_draw.polygon(wing_left, fill=(10, 45, 60, 225), outline=(0, 229, 255, 255))
    glow_draw.line([(cx - 35, head_y - 45), (cx - 105, head_y - 110)], fill=(255, 255, 255, 230), width=2)

    # Asa Direita (Ouro)
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
    
    # 4. ELEMENTOS CONTEXTUAIS DO TEMA: ONDAS ACÚSTICAS & ESPECTROGRAMA (ESQUERDA)
    # Lado Esquerdo: Captura Acústica de Voz Humana (Ciano #00E5FF)
    # Microfone Holográfico / Transdutor Acústico
    mic_x, mic_y = 170, 390
    glow_draw.ellipse([mic_x - 30, mic_y - 45, mic_x + 30, mic_y + 15], fill=(8, 30, 48, 210), outline=(0, 229, 255, 240), width=2)
    # Grade do microfone
    for gx in range(mic_x - 20, mic_x + 25, 8):
        glow_draw.line([(gx, mic_y - 40), (gx, mic_y + 10)], fill=(0, 229, 255, 160), width=1)
    glow_draw.line([(mic_x - 25, mic_y - 15), (mic_x + 25, mic_y - 15)], fill=(0, 229, 255, 180), width=1)
    glow_draw.rectangle([mic_x - 8, mic_y + 15, mic_x + 8, mic_y + 70], fill=(15, 24, 32, 230), outline=(0, 229, 255, 190), width=1)
    glow_draw.rectangle([mic_x - 25, mic_y + 70, mic_x + 25, mic_y + 82], fill=(12, 35, 50, 240), outline=(0, 229, 255, 220), width=2)

    # Espectrograma de Onda Sonora de Entrada (Voice Waveform)
    wave_pts_left = []
    for wx in range(275, 485, 6):
        freq = math.sin((wx - 275) * 0.08) * math.cos((wx - 275) * 0.03) * 45
        freq2 = math.sin((wx - 275) * 0.15) * 20
        wy = cy + int(freq + freq2)
        wave_pts_left.append((wx, wy))
        # Barras de espectro vertical em ciano
        h_bar = int(abs(freq + freq2) * 1.3)
        glow_draw.line([(wx, cy - h_bar), (wx, cy + h_bar)], fill=(0, 229, 255, int(180 * (wx - 270) / 215)), width=2)

    for i in range(len(wave_pts_left) - 1):
        glow_draw.line([wave_pts_left[i], wave_pts_left[i + 1]], fill=(180, 250, 255, 240), width=3)
        
    # Arcos de ondas sonoras irradiando do microfone em direção ao busto
    for ar in range(40, 150, 25):
        glow_draw.arc([mic_x - ar, mic_y - 15 - ar, mic_x + ar, mic_y - 15 + ar], start=300, end=60, fill=(0, 229, 255, int(200 * (1 - ar / 160))), width=2)
        
    # 5. ELEMENTOS CONTEXTUAIS DO TEMA: LIRA CLÁSSICA & SÍNTESE NEURAL OMNIVOICE (DIREITA)
    # Lado Direito: Lira Clássica com Cordas Laser de Frequência Harmônica (Ouro #DFBA6B)
    lyre_x, lyre_y = 1030, 390
    # Corpo em U da Lira clássica
    glow_draw.arc([lyre_x - 65, lyre_y - 50, lyre_x + 65, lyre_y + 80], start=0, end=180, fill=(223, 186, 107, 240), width=7)
    # Braços curvados da Lira
    glow_draw.arc([lyre_x - 85, lyre_y - 110, lyre_x - 30, lyre_y - 10], start=90, end=270, fill=(223, 186, 107, 230), width=6)
    glow_draw.arc([lyre_x + 30, lyre_y - 110, lyre_x + 85, lyre_y - 10], start=270, end=90, fill=(223, 186, 107, 230), width=6)
    # Barra transversal superior
    glow_draw.rectangle([lyre_x - 55, lyre_y - 95, lyre_x + 55, lyre_y - 83], fill=(42, 34, 14, 240), outline=(223, 186, 107, 255), width=2)
    # Base da lira
    glow_draw.rectangle([lyre_x - 35, lyre_y + 80, lyre_x + 35, lyre_y + 98], fill=(36, 28, 12, 240), outline=(223, 186, 107, 240), width=2)

    # Cordas de Laser Dourado da Lira (Laser Strings)
    for str_i in range(7):
        sx = lyre_x - 42 + str_i * 14
        glow_draw.line([(sx, lyre_y - 83), (sx, lyre_y + 60)], fill=(255, 235, 170, 240), width=2)
        glow_draw.line([(sx, lyre_y - 83), (sx, lyre_y + 60)], fill=(223, 186, 107, 100), width=5)

    # Espectrograma de Saída Sintetizada Hi-Fi (Direita do Busto)
    wave_pts_right = []
    for wx in range(715, 925, 6):
        freq = math.cos((wx - 715) * 0.09) * math.sin((wx - 715) * 0.04) * 48
        freq2 = math.cos((wx - 715) * 0.16) * 22
        wy = cy + int(freq + freq2)
        wave_pts_right.append((wx, wy))
        # Barras de espectro vertical em ouro
        h_bar = int(abs(freq + freq2) * 1.3)
        glow_draw.line([(wx, cy - h_bar), (wx, cy + h_bar)], fill=(223, 186, 107, int(180 * (930 - wx) / 215)), width=2)

    for i in range(len(wave_pts_right) - 1):
        glow_draw.line([wave_pts_right[i], wave_pts_right[i + 1]], fill=(255, 245, 200, 240), width=3)
        
    # Anéis de propagação de áudio sintetizado em direção à lira
    for ar in range(40, 150, 25):
        glow_draw.arc([lyre_x - ar, lyre_y - ar, lyre_x + ar, lyre_y + ar], start=120, end=240, fill=(223, 186, 107, int(200 * (1 - ar / 160))), width=2)

    # 6. SÍNTESE NEURAL CENTRAL: CONEXÃO ENTRE CAPTURA E VOZ CLONADA
    # Pontes de feixes neurais conectando o microfone, o busto e a lira
    glow_draw.line([(mic_x + 35, mic_y), (cx - 100, cy - 20)], fill=(0, 229, 255, 190), width=2)
    glow_draw.line([(cx + 100, cy - 20), (lyre_x - 65, lyre_y)], fill=(223, 186, 107, 190), width=2)

    # 7. PARTICULAS DE LUZ E POEIRA DIGITAL DUOCROMÁTICA
    for i in range(140):
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
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "clonagem-de-voz-omnivoice-agentes-ia.jpg")
    im.save(out_path, "JPEG", quality=95)
    print(f"✅ Capa gerada com sucesso em: {out_path} ({width}x{height})")

if __name__ == "__main__":
    create_voice_cloning_cover()
