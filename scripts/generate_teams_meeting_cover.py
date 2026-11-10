import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_teams_meeting_cover():
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
    # Coluna Esquerda (Mármore Ciano / Ingestão Microsoft Graph)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Ação e Downstream)
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
    
    # Inscrição clássica no frontão: MS TEAMS PIPELINE // SECRETARY EXECUTIVE
    glow_draw.rectangle([370, 92, 830, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(400, 102), (800, 102)], fill=(223, 186, 107), width=2)

    # 3. CENTRO: HERMES COM CALENDÁRIO HOLOGRÁFICO DE REUNIÃO
    cx, cy = 600, 420
    
    # Calendário Holográfico Flutuante (Representando o Pipeline de Reunião)
    cal_cx, cal_cy = cx, cy - 200
    cal_w, cal_h = 130, 110
    glow_draw.rectangle([cal_cx - cal_w, cal_cy - cal_h, cal_cx + cal_w, cal_cy + cal_h],
        fill=(12, 20, 32, 200), outline=(0, 229, 255, 220), width=2)
    # Barra de título do calendário
    glow_draw.rectangle([cal_cx - cal_w, cal_cy - cal_h, cal_cx + cal_w, cal_cy - cal_h + 28],
        fill=(0, 100, 140, 200), outline=(0, 229, 255), width=1)
    # Linhas de grade do calendário
    for row in range(5):
        row_y = cal_cy - cal_h + 35 + row * 15
        glow_draw.line([(cal_cx - cal_w + 10, row_y), (cal_cx + cal_w - 10, row_y)], 
            fill=(0, 229, 255, 60), width=1)
    for col in range(4):
        col_x = cal_cx - cal_w + 35 + col * 33
        glow_draw.line([(col_x, cal_cy - cal_h + 35), (col_x, cal_cy + cal_h - 10)],
            fill=(0, 229, 255, 60), width=1)
    # Ícone de calendário
    glow_draw.rectangle([cal_cx - 15, cal_cy + 25, cal_cx + 15, cal_cy + 55],
        fill=(8, 16, 28), outline=(223, 186, 107), width=2)
    glow_draw.arc([cal_cx - 12, cal_cy + 20, cal_cx + 12, cal_cy + 45], start=180, end=0,
        fill=(0, 229, 255), width=2)
    
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
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)],
            fill=(90, 140, 180, 130), width=2)

    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40],
        fill=(228, 235, 245, 250), outline=(0, 229, 255, 220), width=2)

    # Elmo Alado de Hermes (Petasos)
    glow_draw.ellipse([cx - 48, b_head_y - 52, cx + 48, b_head_y - 30],
        fill=(195, 210, 225), outline=(223, 186, 107), width=2)

    # Asa Esquerda do Elmo (Ciano Neon)
    wing_l = [(cx - 35, b_head_y - 40), (cx - 100, b_head_y - 95), (cx - 72, b_head_y - 38), (cx - 88, b_head_y - 20), (cx - 35, b_head_y - 15)]
    glow_draw.polygon(wing_l, fill=(15, 48, 68, 235), outline=(0, 229, 255, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx - 38, b_head_y - 35), (cx - 85 + w * 12, b_head_y - 78 + w * 18)],
            fill=(0, 229, 255, 200), width=2)

    # Asa Direita do Elmo (Ouro Âmbar)
    wing_r = [(cx + 35, b_head_y - 40), (cx + 100, b_head_y - 95), (cx + 72, b_head_y - 38), (cx + 88, b_head_y - 20), (cx + 35, b_head_y - 15)]
    glow_draw.polygon(wing_r, fill=(68, 52, 18, 235), outline=(223, 186, 107, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx + 38, b_head_y - 35), (cx + 85 - w * 12, b_head_y - 78 + w * 18)],
            fill=(223, 186, 107, 200), width=2)

    # 4. LADO ESQUERDO: INTEGRAÇÃO MICROSOFT GRAPH (Transcrição e Ingestão)
    # Microsoft Teams Client Interface (Ciano Neon)
    ms_cx, ms_cy = 280, 420
    
    # Monitor/Janela do Teams
    glow_draw.rectangle([ms_cx - 105, ms_cy - 130, ms_cx + 105, ms_cy + 130],
        fill=(10, 18, 30, 220), outline=(0, 229, 255, 220), width=2)
    # Barra superior do Teams (azul corporativo Microsoft)
    glow_draw.rectangle([ms_cx - 105, ms_cy - 130, ms_cx + 105, ms_cy - 100],
        fill=(0, 120, 212, 220), outline=(0, 80, 180, 180), width=1)
    # Barra de controles
    glow_draw.rectangle([ms_cx - 95, ms_cy - 90, ms_cx + 95, ms_cy - 65],
        fill=(14, 26, 42), outline=(0, 229, 255, 100), width=1)
    
    # Ícones de participantes (avatares)
    for icon_x in range(ms_cx - 70, ms_cx + 80, 35):
        glow_draw.ellipse([icon_x - 12, ms_cy - 75, icon_x + 12, ms_cy - 51],
            fill=(20, 40, 60), outline=(0, 229, 255), width=1)
    
    # Feed de fala / Transcrição com timestamps
    for line_y in range(ms_cy - 45, ms_cy + 100, 22):
        glow_draw.rectangle([ms_cx - 85, line_y, ms_cx - 85 + 60, line_y + 12],
            fill=(20, 50, 70), outline=(0, 229, 255, 60), width=1)
        glow_draw.line([(ms_cx + 30, line_y + 6), (ms_cx + 80, line_y + 6)],
            fill=(0, 229, 255, 60), width=3)
    
    # Rótulo: TRANSCRIPT INGESTION / GRAPH WEBHOOK
    glow_draw.rectangle([ms_cx - 90, ms_cy + 50, ms_cx + 90, ms_cy + 95],
        fill=(8, 14, 22), outline=(0, 229, 255, 180), width=1)
    glow_draw.line([(ms_cx - 75, ms_cy + 73), (ms_cx + 75, ms_cy + 73)], fill=(0, 229, 255), width=2)

    # 5. LADO DIREITO: ATO E DOWNSTREAM ACTION (Tarefas, Notion, Linear)
    # Painel de Ata e Plano de Ação (Âmbar/Ouro)
    act_cx, act_cy = 920, 420
    
    # Documento de Ata / Minuta
    glow_draw.rectangle([act_cx - 105, act_cy - 130, act_cx + 105, act_cx + 130],
        fill=(22, 18, 8, 220), outline=(223, 186, 107, 220), width=2)
    # Título da Ata
    glow_draw.rectangle([act_cx - 95, act_cy - 120, act_cx + 95, act_cy - 95],
        fill=(50, 42, 16, 200), outline=(223, 186, 107, 180), width=1)
    
    # Linhas de decisão (checkmarks) na ata
    for item_y in range(act_cy - 80, act_cy + 80, 28):
        # Checkbox
        glow_draw.rectangle([act_cx - 80, item_y, act_cx - 65, item_y + 12],
            fill=(28, 24, 10), outline=(223, 186, 107), width=1)
        glow_draw.line([(act_cx - 80, item_y), (act_cx - 65, item_y + 12)],
            fill=(223, 186, 107), width=2)
        glow_draw.line([(act_cx - 65, item_y), (act_cx - 80, item_y + 12)],
            fill=(223, 186, 107), width=2)
        # Linha de texto da tarefa
        glow_draw.line([(act_cx - 55, item_y + 6), (act_cx + 80, item_y + 6)],
            fill=(223, 186, 107, 160), width=6)
    
    # Rótulo: ACTION ITEMS / LINEAR / NOTION
    glow_draw.rectangle([act_cx - 90, act_cy + 50, act_cx + 90, act_cy + 95],
        fill=(20, 16, 8), outline=(223, 186, 107, 180), width=1)
    glow_draw.line([(act_cx - 75, act_cy + 73), (act_cx + 75, act_cy + 73)], fill=(223, 186, 107), width=2)

    # 6. SETAS DE FLUXO: Ingestão → Hermes → Ação
    # Seta Esquerda-Centro (Ingestão → Hermes) em ciano
    arrow_mid_ys = [280, 340, 400, 460, 520]
    for ay in arrow_mid_ys:
        glow_draw.line([(ms_cx + 110, ay), (cx - 90, ay)], fill=(0, 229, 255, 200), width=3)
        # Ponta da seta
        glow_draw.polygon([(cx - 90, ay - 8), (cx - 60, ay), (cx - 90, ay + 8)],
            fill=(0, 229, 255), outline=(255, 255, 255))
    
    # Seta Centro-Direita (Hermes → Ação) em dourado
    for ay in arrow_mid_ys:
        glow_draw.line([(cx + 90, ay), (act_cx - 110, ay)], fill=(223, 186, 107, 200), width=3)
        glow_draw.polygon([(act_cx - 110, ay - 8), (act_cx - 80, ay), (act_cx - 110, ay + 8)],
            fill=(223, 186, 107), outline=(255, 255, 255))

    # 7. FILAMENTOS NEURAIS DE FIBRA ÓPTICA
    for f in range(5):
        glow_draw.line([(150, 680 + f * 40), (cx - 120, 680 + f * 40)], fill=(0, 229, 255, 80), width=1)
        glow_draw.line([(cx + 120, 680 + f * 40), (1050, 680 + f * 40)], fill=(223, 186, 107, 80), width=1)

    # 8. RENDERIZAÇÃO FINAL E BLUR SUAVE
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=1.8))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Sharp overlay layer for crisp edges
    final_draw = ImageDraw.Draw(final_im)
    final_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], outline=(0, 229, 255, 255), width=2)
    
    # Save image
    output_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "teams-meeting-pipeline-microsoft-graph.jpg")
    
    final_im.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_teams_meeting_cover()
