import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_group_chats_cover():
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
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Council Chamber Colonnade)
    # Coluna Esquerda (Mármore Ciano / Specialised Agents & Ingress)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Executive Governance & Gateway)
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
    
    # Inscrição clássica no frontão: HERMES AGENT // GROUP CHATS & BOT COMMITTEE
    glow_draw.rectangle([300, 92, 900, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(320, 102), (880, 102)], fill=(223, 186, 107), width=2)

    # 3. CONSELHO MULTI-AGENTE: MESA / ALTAR HOLOGRÁFICO CENTRAL (Round Council Altar)
    altar_cx, altar_cy = 600, 580
    # Anéis concêntricos da mesa de deliberação
    for r in range(260, 40, -18):
        alpha = int(45 * (1 - r / 260))
        glow_draw.ellipse([altar_cx - r, altar_cy - int(r * 0.38), altar_cx + r, altar_cy + int(r * 0.38)], outline=(0, 229, 255, alpha * 2), width=2)
    
    # Conexões em teia neural entre os assentos do comitê
    glow_draw.line([(320, 450), (600, 370)], fill=(0, 229, 255, 180), width=2)
    glow_draw.line([(880, 450), (600, 370)], fill=(223, 186, 107, 180), width=2)
    glow_draw.line([(320, 450), (880, 450)], fill=(120, 210, 235, 120), width=2)

    # Glifo central do Gateway na mesa (Loop Guard Core)
    glow_draw.ellipse([altar_cx - 45, altar_cy - 18, altar_cx + 45, altar_cy + 18], fill=(10, 25, 40, 220), outline=(223, 186, 107), width=2)
    glow_draw.polygon([(altar_cx, altar_cy - 12), (altar_cx + 18, altar_cy), (altar_cx, altar_cy + 12), (altar_cx - 18, altar_cy)], fill=(0, 229, 255, 230), outline=(255, 255, 255), width=1)

    # 4. OS TRÊS BUSTOS CLÁSSICOS DO COMITÊ (Busts of the Council)
    
    # --- BUSTO 1: HERMES LÍDER (CENTRAL - Lead Bot & Gateway Coordinator) ---
    c_x, c_y = 600, 350
    # Halo do Líder
    for r in range(130, 20, -10):
        alpha = int(35 * (1 - r / 130))
        glow_draw.ellipse([c_x - r, c_y - r * 0.9, c_x + r, c_y + r * 0.9], fill=(223, 186, 107, alpha))
        
    # Pedestal de Mármore
    glow_draw.rectangle([c_x - 55, c_y + 90, c_x + 55, c_y + 130], fill=(18, 25, 36), outline=(223, 186, 107), width=2)
    # Torso & Toga Neoclássica
    glow_draw.polygon([(c_x - 70, c_y + 90), (c_x - 45, c_y + 25), (c_x + 45, c_y + 25), (c_x + 70, c_y + 90), (c_x, c_y + 105)], fill=(22, 32, 46, 240), outline=(220, 235, 250), width=2)
    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([c_x - 32, c_y - 45, c_x + 32, c_y + 15], fill=(28, 38, 52), outline=(215, 230, 245), width=2)
    # Elmo Alado de Hermes (Petasos com Asas Ciano e Ouro)
    glow_draw.arc([c_x - 42, c_y - 60, c_x + 42, c_y - 20], start=180, end=0, fill=(0, 229, 255), width=2)
    glow_draw.polygon([(c_x - 30, c_y - 35), (c_x - 65, c_y - 65), (c_x - 40, c_y - 48)], fill=(0, 229, 255, 200), outline=(220, 245, 255), width=1)
    glow_draw.polygon([(c_x + 30, c_y - 35), (c_x + 65, c_y - 65), (c_x + 40, c_y - 48)], fill=(223, 186, 107, 200), outline=(255, 235, 180), width=1)

    # --- BUSTO 2: ATENA (ESQUERDA - Operações, Inteligência & Suporte) ---
    l_x, l_y = 320, 430
    # Halo Ciano
    for r in range(110, 15, -10):
        alpha = int(32 * (1 - r / 110))
        glow_draw.ellipse([l_x - r, l_y - r * 0.9, l_x + r, l_y + r * 0.9], fill=(0, 229, 255, alpha))
    # Pedestal
    glow_draw.rectangle([l_x - 45, l_y + 80, l_x + 45, l_y + 115], fill=(14, 22, 32), outline=(0, 229, 255), width=2)
    # Torso & Toga
    glow_draw.polygon([(l_x - 60, l_y + 80), (l_x - 38, l_y + 20), (l_x + 38, l_y + 20), (l_x + 60, l_y + 80), (l_x, l_y + 95)], fill=(18, 28, 42, 230), outline=(180, 220, 245), width=2)
    # Cabeça & Elmo Coríntio
    glow_draw.ellipse([l_x - 28, l_y - 40, l_x + 28, l_y + 12], fill=(24, 34, 48), outline=(190, 225, 250), width=2)
    glow_draw.polygon([(l_x - 32, l_y - 30), (l_x, l_y - 65), (l_x + 32, l_y - 30)], fill=(0, 229, 255, 160), outline=(180, 230, 255), width=2)

    # --- BUSTO 3: APOLO / MERCÚRIO FINANÇAS (DIREITA - Finanças & Estratégia) ---
    r_x, r_y = 880, 430
    # Halo Dourado
    for r in range(110, 15, -10):
        alpha = int(32 * (1 - r / 110))
        glow_draw.ellipse([r_x - r, r_y - r * 0.9, r_x + r, r_y + r * 0.9], fill=(223, 186, 107, alpha))
    # Pedestal
    glow_draw.rectangle([r_x - 45, r_y + 80, r_x + 45, r_y + 115], fill=(28, 24, 14), outline=(223, 186, 107), width=2)
    # Torso & Toga
    glow_draw.polygon([(r_x - 60, r_y + 80), (r_x - 38, r_y + 20), (r_x + 38, r_y + 20), (r_x + 60, r_y + 80), (r_x, r_y + 95)], fill=(34, 28, 16, 230), outline=(240, 215, 160), width=2)
    # Cabeça & Coroa de Louros Radiante
    glow_draw.ellipse([r_x - 28, r_y - 40, r_x + 28, r_y + 12], fill=(36, 30, 18), outline=(245, 220, 165), width=2)
    for la in range(-35, 40, 15):
        rad = math.radians(la - 90)
        glow_draw.line([(r_x, r_y - 40), (r_x + int(35 * math.cos(rad)), r_y - 40 + int(35 * math.sin(rad)))], fill=(223, 186, 107), width=2)

    # 5. CARDS HOLOGRÁFICOS DE DIÁLOGO E GOVERNANÇA (Group Chat Dialogue Nodes)
    # Card 1: Mensagem do Lead Bot (Centro-Esquerda)
    glow_draw.rectangle([410, 260, 560, 310], fill=(10, 20, 30, 230), outline=(0, 229, 255), width=2)
    glow_draw.line([(425, 275), (545, 275)], fill=(0, 229, 255), width=2)
    glow_draw.line([(425, 290), (510, 290)], fill=(223, 186, 107), width=2)
    glow_draw.ellipse([540, 290, 548, 298], fill=(0, 229, 255))
    
    # Card 2: Deliberação do Especialista (Centro-Direita)
    glow_draw.rectangle([640, 260, 790, 310], fill=(25, 20, 10, 230), outline=(223, 186, 107), width=2)
    glow_draw.line([(655, 275), (775, 275)], fill=(223, 186, 107), width=2)
    glow_draw.line([(655, 290), (740, 290)], fill=(0, 229, 255), width=2)
    glow_draw.ellipse([770, 290, 778, 298], fill=(223, 186, 107))

    # Badge de Proteção Anti-Loop (Loop Guard: max_hops = 4)
    glow_draw.rectangle([480, 680, 720, 725], fill=(8, 16, 24, 240), outline=(0, 229, 255), width=2)
    glow_draw.rectangle([495, 695, 705, 710], fill=(14, 30, 45), outline=(223, 186, 107), width=1)
    glow_draw.line([(520, 702), (680, 702)], fill=(0, 229, 255), width=2)
    
    # Escalonamento Humano-no-Loop (@user badge)
    glow_draw.ellipse([585, 740, 615, 770], fill=(223, 186, 107, 230), outline=(255, 255, 255), width=2)
    glow_draw.polygon([(600, 746), (608, 762), (592, 762)], fill=(10, 10, 15))

    # Fusão com imagem base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Aplica um suave anti-aliasing / filtro de refinamento
    im = im.filter(ImageFilter.SMOOTH_MORE)
    
    # Salva no diretório de imagens do blog
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\group-chats-autonomos-salas-multi-bot-hermes.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_group_chats_cover()
