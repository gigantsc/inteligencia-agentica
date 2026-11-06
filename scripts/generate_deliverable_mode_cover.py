import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_deliverable_mode_cover():
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
    # Coluna Esquerda (Mármore Ciano / Mobile Messaging Gateway)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Artifact Generation Engine)
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
    
    # Inscrição clássica no frontão: DELIVERABLE MODE // NATIVE ATTACHMENTS
    glow_draw.rectangle([370, 92, 830, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(390, 102), (810, 102)], fill=(223, 186, 107), width=2)

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

    # 4. LADO ESQUERDO: SMARTPHONE / INTERFACE DE CHAT MOBILE (RECEBENDO ANEXOS NATIVOS)
    phone_cx, phone_cy = 280, 410
    
    # Corpo do Smartphone (Moldura em vidro e ciano)
    glow_draw.rectangle([phone_cx - 120, phone_cy - 200, phone_cx + 120, phone_cy + 200], fill=(10, 20, 32, 235), outline=(0, 229, 255, 240), width=2)
    # Notch superior
    glow_draw.rectangle([phone_cx - 40, phone_cy - 198, phone_cx + 40, phone_cy - 184], fill=(6, 12, 18), outline=(0, 229, 255, 140), width=1)
    
    # Barra de status do chat (Telegram / WhatsApp)
    glow_draw.rectangle([phone_cx - 115, phone_cy - 180, phone_cx + 115, phone_cy - 145], fill=(14, 34, 52, 220), outline=(0, 229, 255, 160), width=1)
    glow_draw.ellipse([phone_cx - 100, phone_cy - 170, phone_cx - 84, phone_cy - 154], fill=(0, 229, 255, 220)) # Avatar
    glow_draw.line([(phone_cx - 75, phone_cy - 162), (phone_cx + 40, phone_cy - 162)], fill=(220, 240, 255), width=2)
    
    # Bolha de Mensagem do Agente
    glow_draw.rectangle([phone_cx - 110, phone_cy - 135, phone_cx + 110, phone_cy + 175], fill=(12, 28, 44, 210), outline=(0, 229, 255, 180), width=1)
    
    # 1º Item: Imagem do Gráfico Embutido (Inline Chart)
    glow_draw.rectangle([phone_cx - 98, phone_cy - 125, phone_cx + 98, phone_cy - 45], fill=(8, 16, 28), outline=(0, 229, 255, 200), width=1)
    # Linha de tendência do gráfico subindo
    chart_pts = [(phone_cx - 85, phone_cy - 60), (phone_cx - 50, phone_cy - 75), (phone_cx - 15, phone_cy - 65), (phone_cx + 25, phone_cy - 95), (phone_cx + 85, phone_cy - 110)]
    for cp in range(len(chart_pts) - 1):
        glow_draw.line([chart_pts[cp], chart_pts[cp+1]], fill=(0, 229, 255), width=2)
        glow_draw.ellipse([chart_pts[cp][0]-3, chart_pts[cp][1]-3, chart_pts[cp][0]+3, chart_pts[cp][1]+3], fill=(223, 186, 107))
    glow_draw.ellipse([chart_pts[-1][0]-3, chart_pts[-1][1]-3, chart_pts[-1][0]+3, chart_pts[-1][1]+3], fill=(223, 186, 107))
    
    # 2º Item: Card de Anexo Planilha Excel (.xlsx)
    glow_draw.rectangle([phone_cx - 98, phone_cy - 35, phone_cx + 98, phone_cy + 45], fill=(10, 24, 34), outline=(0, 229, 255, 220), width=1)
    # Ícone XLSX (Verde/Ciano)
    glow_draw.rectangle([phone_cx - 90, phone_cy - 25, phone_cx - 55, phone_cy + 35], fill=(15, 60, 50), outline=(0, 229, 255), width=1)
    # Grid interno do ícone de planilha
    glow_draw.line([(phone_cx - 90, phone_cy + 5), (phone_cx - 55, phone_cy + 5)], fill=(0, 229, 255), width=1)
    glow_draw.line([(phone_cx - 72, phone_cy - 25), (phone_cx - 72, phone_cy + 35)], fill=(0, 229, 255), width=1)
    # Nome do arquivo e tamanho
    glow_draw.line([(phone_cx - 45, phone_cy - 15), (phone_cx + 85, phone_cy - 15)], fill=(220, 240, 255), width=2)
    glow_draw.line([(phone_cx - 45, phone_cy + 5), (phone_cx + 45, phone_cy + 5)], fill=(0, 229, 255, 180), width=2)
    glow_draw.line([(phone_cx - 45, phone_cy + 22), (phone_cx + 10, phone_cy + 22)], fill=(120, 180, 210, 140), width=1)
    
    # 3º Item: Card de Anexo Relatório PDF (.pdf)
    glow_draw.rectangle([phone_cx - 98, phone_cy + 55, phone_cx + 98, phone_cy + 135], fill=(22, 18, 24), outline=(223, 186, 107, 220), width=1)
    # Ícone PDF (Vermelho/Dourado)
    glow_draw.rectangle([phone_cx - 90, phone_cy + 65, phone_cx - 55, phone_cy + 125], fill=(60, 25, 20), outline=(223, 186, 107), width=1)
    # Dobra da folha do documento
    glow_draw.polygon([(phone_cx - 65, phone_cy + 65), (phone_cx - 55, phone_cy + 75), (phone_cx - 65, phone_cy + 75)], fill=(223, 186, 107))
    # Nome do PDF e badge
    glow_draw.line([(phone_cx - 45, phone_cy + 78), (phone_cx + 85, phone_cy + 78)], fill=(240, 230, 210), width=2)
    glow_draw.line([(phone_cx - 45, phone_cy + 98), (phone_cx + 55, phone_cy + 98)], fill=(223, 186, 107, 180), width=2)
    glow_draw.line([(phone_cx - 45, phone_cy + 115), (phone_cx + 15, phone_cy + 115)], fill=(180, 160, 120, 140), width=1)

    # Selo no rodapé do celular: NATIVE DELIVERY
    glow_draw.rectangle([phone_cx - 95, phone_cy + 145, phone_cx + 95, phone_cy + 168], fill=(6, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(phone_cx - 75, phone_cy + 156), (phone_cx + 75, phone_cy + 156)], fill=(0, 229, 255), width=2)

    # 5. LADO DIREITO: MOTOR DE GERAÇÃO DE ARTEFATOS (BACKEND SERVER & SANDBOX)
    srv_cx, srv_cy = 920, 410
    
    # Rack / Console do Servidor Corporativo
    glow_draw.rectangle([srv_cx - 125, srv_cy - 190, srv_cx + 125, srv_cy + 190], fill=(24, 20, 12, 225), outline=(223, 186, 107, 230), width=2)
    # Header do Servidor: ARTIFACT PIPELINE
    glow_draw.rectangle([srv_cx - 125, srv_cy - 190, srv_cx + 125, srv_cy - 150], fill=(42, 34, 16), outline=(223, 186, 107, 180), width=1)
    for b in range(3):
        glow_draw.ellipse([srv_cx - 110 + b * 16, srv_cy - 173, srv_cx - 100 + b * 16, srv_cy - 163], fill=(223, 186, 107, 180))
    glow_draw.line([(srv_cx - 45, srv_cy - 168), (srv_cx + 105, srv_cy - 168)], fill=(223, 186, 107), width=2)
    
    # Bloco 1: Sandbox de Fórmulas e Processamento de Dados (xlsx skill)
    glow_draw.rectangle([srv_cx - 110, srv_cy - 135, srv_cx + 110, srv_cy - 40], fill=(18, 14, 8), outline=(223, 186, 107, 160), width=1)
    # Linhas de código / fórmulas de planilha
    for row in range(3):
        y_pos = srv_cy - 120 + row * 26
        glow_draw.line([(srv_cx - 95, y_pos), (srv_cx + 85 - (row % 2) * 45, y_pos)], fill=(223, 186, 107, 180), width=2)
    
    # Bloco 2: Compilador de PDF / Diagramação (pdf skill)
    glow_draw.rectangle([srv_cx - 110, srv_cy - 25, srv_cx + 110, srv_cy + 70], fill=(22, 16, 10), outline=(223, 186, 107, 160), width=1)
    # Linhas de layout e diagramação
    glow_draw.rectangle([srv_cx - 95, srv_cy - 12, srv_cx - 40, srv_cy + 55], fill=(35, 26, 14), outline=(223, 186, 107, 120), width=1)
    for row in range(3):
        y_pos = srv_cy - 5 + row * 20
        glow_draw.line([(srv_cx - 25, y_pos), (srv_cx + 90, y_pos)], fill=(210, 190, 140, 160), width=2)
        
    # Bloco 3: Disparo via Gateway (kanban_complete artifacts)
    glow_draw.rectangle([srv_cx - 110, srv_cy + 85, srv_cx + 110, srv_cy + 170], fill=(16, 12, 6), outline=(0, 229, 255, 180), width=1)
    glow_draw.line([(srv_cx - 95, srv_cy + 105), (srv_cx + 95, srv_cy + 105)], fill=(0, 229, 255), width=2)
    glow_draw.line([(srv_cx - 95, srv_cy + 128), (srv_cx + 60, srv_cy + 128)], fill=(223, 186, 107), width=2)
    # Botão de status DISPATCH READY
    glow_draw.rectangle([srv_cx - 80, srv_cy + 145, srv_cx + 80, srv_cy + 165], fill=(8, 18, 26), outline=(0, 229, 255), width=1)
    glow_draw.line([(srv_cx - 60, srv_cy + 155), (srv_cx + 60, srv_cy + 155)], fill=(0, 229, 255), width=2)

    # 6. FILAMENTOS DE CONEXÃO E ROTEAMENTO (CENTRO LIGANDO AS DUAS PONTAS)
    for l in range(4):
        # Do motor de artefatos para o Hermes (centro)
        glow_draw.line([(srv_cx - 125, srv_cy - 80 + l * 50), (cx + 90, cy - 20 + l * 25)], fill=(223, 186, 107, 180), width=2)
        # Do Hermes (centro) para o smartphone (esquerda)
        glow_draw.line([(cx - 90, cy - 20 + l * 25), (phone_cx + 120, phone_cy - 80 + l * 50)], fill=(0, 229, 255, 180), width=2)
        
        # Pulsos de dados (Data Packets)
        p1_x = cx + 90 + int((srv_cx - 125 - (cx + 90)) * 0.5)
        p1_y = cy - 20 + l * 25 + int((srv_cy - 80 + l * 50 - (cy - 20 + l * 25)) * 0.5)
        glow_draw.ellipse([p1_x - 5, p1_y - 5, p1_x + 5, p1_y + 5], fill=(223, 186, 107, 240), outline=(255, 255, 255), width=1)

        p2_x = phone_cx + 120 + int((cx - 90 - (phone_cx + 120)) * 0.5)
        p2_y = phone_cy - 80 + l * 50 + int((cy - 20 + l * 25 - (phone_cy - 80 + l * 50)) * 0.5)
        glow_draw.ellipse([p2_x - 5, p2_y - 5, p2_x + 5, p2_y + 5], fill=(0, 229, 255, 240), outline=(255, 255, 255), width=1)

    # 7. TRILHAS NEURAIS E FIBRA ÓPTICA INFERIOR
    for f in range(5):
        glow_draw.line([(150, 680 + f * 40), (cx - 120, 680 + f * 40)], fill=(0, 229, 255, 80), width=1)
        glow_draw.line([(cx + 120, 680 + f * 40), (1050, 680 + f * 40)], fill=(223, 186, 107, 80), width=1)

    # 8. RENDERIZAÇÃO FINAL COM BLUR CINEMATOGRÁFICO
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=1.8))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Sharp overlay layer for crisp edges
    final_draw = ImageDraw.Draw(final_im)
    final_draw.rectangle([phone_cx - 120, phone_cy - 200, phone_cx + 120, phone_cy + 200], outline=(0, 229, 255, 240), width=2)
    final_draw.rectangle([srv_cx - 125, srv_cy - 190, srv_cx + 125, srv_cy + 190], outline=(223, 186, 107, 240), width=2)
    final_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], outline=(0, 229, 255, 220), width=2)
    
    # Salvar imagem
    output_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "deliverable-mode-artefatos-chat-planilhas-pdf.jpg")
    
    final_im.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_deliverable_mode_cover()
