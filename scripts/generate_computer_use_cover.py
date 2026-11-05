import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_computer_use_cover():
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
    # Coluna Esquerda (Mármore Ciano / Background Non-Intrusive Engine)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Legacy ERP Systems)
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
    
    # Inscrição clássica no frontão: COMPUTER USE // NO-FOREGROUND CUA
    glow_draw.rectangle([380, 92, 820, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(400, 102), (800, 102)], fill=(223, 186, 107), width=2)

    # 3. CENTRO: O CONSOLE CENTRAL E O BUSTO CLÁSSICO DE HERMES
    cx, cy = 600, 410

    # Campo de Força Elíptico / Aura Tecnológica
    for r in range(240, 30, -12):
        alpha = int(32 * (1 - r / 240))
        glow_draw.ellipse([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95], fill=(0, 229, 255, alpha))
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 140
    glow_draw.rectangle([cx - 105, ped_y, cx + 105, ped_y + 45], fill=(18, 25, 36), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 125, ped_y + 45, cx + 125, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    # Placa do Pedestal
    glow_draw.rectangle([cx - 85, ped_y + 14, cx + 85, ped_y + 34], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 70, ped_y + 24), (cx + 70, ped_y + 24)], fill=(223, 186, 107), width=2)

    # Tronco Esculpido de Hermes com Toga Neoclássica
    b_head_y = cy - 35
    torso = [(cx - 90, b_head_y + 145), (cx - 55, b_head_y + 45), (cx + 55, b_head_y + 45), (cx + 90, b_head_y + 145), (cx, b_head_y + 160)]
    glow_draw.polygon(torso, fill=(18, 26, 38, 240), outline=(210, 225, 240, 220), width=2)
    for t_line in range(-40, 45, 18):
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)], fill=(90, 140, 180, 130), width=2)

    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], fill=(228, 235, 245, 250), outline=(0, 229, 255, 220), width=2)

    # Elmo Alado de Hermes (Petasos)
    glow_draw.ellipse([cx - 48, b_head_y - 52, cx + 48, b_head_y - 30], fill=(195, 210, 225), outline=(223, 186, 107), width=2)

    # Asa Esquerda do Elmo (Ciano Neon)
    wing_l = [(cx - 35, b_head_y - 40), (cx - 100, b_head_y - 95), (cx - 72, b_head_y - 38), (cx - 88, b_head_y - 20), (cx - 35, b_head_y - 15)]
    glow_draw.polygon(wing_l, fill=(15, 48, 68, 235), outline=(0, 229, 255, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx - 38, b_head_y - 35), (cx - 85 + w * 12, b_head_y - 78 + w * 18)], fill=(0, 229, 255, 200), width=2)

    # Asa Direita do Elmo (Ouro Âmbar)
    wing_r = [(cx + 35, b_head_y - 40), (cx + 100, b_head_y - 95), (cx + 72, b_head_y - 38), (cx + 88, b_head_y - 20), (cx + 35, b_head_y - 15)]
    glow_draw.polygon(wing_r, fill=(68, 52, 18, 235), outline=(223, 186, 107, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx + 38, b_head_y - 35), (cx + 85 - w * 12, b_head_y - 78 + w * 18)], fill=(223, 186, 107, 200), width=2)

    # 4. LADO ESQUERDO: ESTAÇÃO DO OPERADOR HUMANO (JANELA EM FOCO ATIVO)
    # Mostra a tela do usuário com Word/Editor intocada e cursor calmo
    user_cx, user_cy = 280, 410
    # Janela Principal do Usuário
    glow_draw.rectangle([user_cx - 120, user_cy - 130, user_cx + 120, user_cy + 130], fill=(10, 24, 38, 220), outline=(0, 229, 255, 230), width=2)
    # Barra de Título da Janela (Active Window)
    glow_draw.rectangle([user_cx - 120, user_cy - 130, user_cx + 120, user_cy - 95], fill=(16, 42, 64), outline=(0, 229, 255, 180), width=1)
    # Botões de controle da janela (Fechar, Minimizar, Maximizar)
    for b in range(3):
        glow_draw.ellipse([user_cx - 108 + b * 16, user_cy - 118, user_cx - 98 + b * 16, user_cy - 108], fill=(0, 229, 255, 180))
    # Título "HUMAN WORKSPACE // IN FOCUS"
    glow_draw.line([(user_cx - 45, user_cy - 113), (user_cx + 105, user_cy - 113)], fill=(0, 229, 255), width=2)

    # Linhas de texto digitadas pelo usuário (Word / Docs)
    for row in range(5):
        y_pos = user_cy - 70 + row * 24
        glow_draw.line([(user_cx - 100, y_pos), (user_cx + 80 - (row % 2) * 35, y_pos)], fill=(120, 200, 240, 180), width=2)

    # Cursor de edição do usuário piscando pacificamente (intocado)
    cur_y = user_cy + 55
    glow_draw.line([(user_cx - 100, cur_y), (user_cx - 20, cur_y)], fill=(120, 200, 240, 180), width=2)
    glow_draw.line([(user_cx - 15, cur_y - 8), (user_cx - 15, cur_y + 8)], fill=(0, 229, 255), width=3)
    
    # Selo "NO FOCUS STEAL"
    glow_draw.rectangle([user_cx - 105, user_cy + 85, user_cx + 105, user_cy + 115], fill=(8, 16, 26), outline=(0, 229, 255), width=1)
    glow_draw.line([(user_cx - 90, user_cy + 100), (user_cx + 90, user_cy + 100)], fill=(0, 229, 255), width=2)

    # 5. LADO DIREITO: SOFTWARE LEGADO / ERP DESKTOP (OPERADO EM SEGUNDO PLANO)
    # Mostra a janela do ERP recebendo automação via UIAutomation
    erp_cx, erp_cy = 920, 410
    # Janela Principal do ERP Legado
    glow_draw.rectangle([erp_cx - 125, erp_cy - 130, erp_cx + 125, erp_cy + 130], fill=(28, 22, 10, 220), outline=(223, 186, 107, 230), width=2)
    # Barra de Título do ERP (Background Window - SAP/TOTVS)
    glow_draw.rectangle([erp_cx - 125, erp_cy - 130, erp_cx + 125, erp_cy - 95], fill=(44, 34, 14), outline=(223, 186, 107, 180), width=1)
    for b in range(3):
        glow_draw.ellipse([erp_cx - 113 + b * 16, erp_cy - 118, erp_cx - 103 + b * 16, erp_cy - 108], fill=(223, 186, 107, 180))
    # Título "ERP DESKTOP // BACKGROUND PID:4892"
    glow_draw.line([(erp_cx - 50, erp_cy - 113), (erp_cx + 110, erp_cy - 113)], fill=(223, 186, 107), width=2)

    # Grid de dados e campos de formulário do ERP
    # Tabela com linhas e colunas
    glow_draw.rectangle([erp_cx - 110, erp_cy - 80, erp_cx + 110, erp_cy + 25], fill=(18, 14, 8), outline=(223, 186, 107, 140), width=1)
    for row in range(3):
        grid_y = erp_cy - 55 + row * 25
        glow_draw.line([(erp_cx - 110, grid_y), (erp_cx + 110, grid_y)], fill=(223, 186, 107, 90), width=1)
    for col in range(3):
        grid_x = erp_cx - 55 + col * 55
        glow_draw.line([(grid_x, erp_cy - 80), (grid_x, erp_cy + 25)], fill=(223, 186, 107, 90), width=1)

    # Injeção de dados sintéticos pelo agente (SendInput / PostMessage)
    glow_draw.rectangle([erp_cx - 110, erp_cy + 40, erp_cx + 40, erp_cy + 70], fill=(35, 28, 12), outline=(0, 229, 255), width=2)
    glow_draw.line([(erp_cx - 95, erp_cy + 55), (erp_cx + 25, erp_cy + 55)], fill=(0, 229, 255), width=2)
    # Botão de emissão/confirmação acionado pelo agente
    glow_draw.rectangle([erp_cx + 55, erp_cy + 40, erp_cx + 110, erp_cy + 70], fill=(50, 40, 16), outline=(223, 186, 107), width=2)
    glow_draw.line([(erp_cx + 65, erp_cy + 55), (erp_cx + 100, erp_cy + 55)], fill=(223, 186, 107), width=2)

    # Selo "NO-FOREGROUND CONTRACT // DISPATCHED"
    glow_draw.rectangle([erp_cx - 110, erp_cy + 85, erp_cx + 110, erp_cy + 115], fill=(16, 12, 6), outline=(223, 186, 107), width=1)
    glow_draw.line([(erp_cx - 95, erp_cy + 100), (erp_cx + 95, erp_cy + 100)], fill=(223, 186, 107), width=2)

    # 6. FILAMENTOS DE CONTROLE E PROTOCOLO MCP (CENTRO LIGANDO LADO ESQUERDO E DIREITO)
    # Linhas de telemetria e controle em background
    for l in range(4):
        # Do agente para a aplicação de fundo (ERP)
        glow_draw.line([(cx + 90, cy - 20 + l * 30), (erp_cx - 125, erp_cy - 50 + l * 35)], fill=(223, 186, 107, 180), width=2)
        # Pulsos de dados
        p_x = cx + 90 + int((erp_cx - 125 - (cx + 90)) * 0.5)
        p_y = cy - 20 + l * 30 + int((erp_cy - 50 + l * 35 - (cy - 20 + l * 30)) * 0.5)
        glow_draw.ellipse([p_x - 5, p_y - 5, p_x + 5, p_y + 5], fill=(0, 229, 255, 240), outline=(255, 255, 255), width=1)

    # Linha de blindagem isolando a janela do usuário
    glow_draw.arc([user_cx + 120, user_cy - 120, user_cx + 180, user_cy + 120], start=270, end=90, fill=(0, 229, 255, 140), width=2)

    # 7. TRILHAS NEURAIS E FIBRA ÓPTICA INFERIOR
    for f in range(5):
        glow_draw.line([(150, 680 + f * 40), (cx - 120, 680 + f * 40)], fill=(0, 229, 255, 80), width=1)
        glow_draw.line([(cx + 120, 680 + f * 40), (1050, 680 + f * 40)], fill=(223, 186, 107, 80), width=1)

    # 8. RENDERIZAÇÃO FINAL COM BLUR CINEMATOGRÁFICO
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=1.8))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Sharp overlay layer for crisp edges
    final_draw = ImageDraw.Draw(final_im)
    final_draw.rectangle([user_cx - 120, user_cy - 130, user_cx + 120, user_cy + 130], outline=(0, 229, 255, 240), width=2)
    final_draw.rectangle([erp_cx - 125, erp_cy - 130, erp_cx + 125, erp_cy + 130], outline=(223, 186, 107, 240), width=2)
    final_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], outline=(0, 229, 255, 220), width=2)
    
    # Salvar imagem
    output_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "computer-use-segundo-plano-automacao-desktop.jpg")
    
    final_im.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_computer_use_cover()
