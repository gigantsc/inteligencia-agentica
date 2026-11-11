import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_multiplexing_gateway_cover():
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
    # Coluna Esquerda (Mármore Ciano / Inbound Messaging Ingress)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Isolated Profiles & Storage)
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
    
    # Inscrição clássica no frontão: MULTIPLEXING GATEWAY // SINGLE VPS MULTI-PROFILE
    glow_draw.rectangle([320, 92, 880, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(340, 102), (860, 102)], fill=(223, 186, 107), width=2)

    # 3. CENTRO: O CONSOLE CENTRAL E O BUSTO CLÁSSICO DE HERMES
    cx, cy = 600, 420

    # Campo de Força Elíptico / Aura Tecnológica
    for r in range(240, 30, -12):
        alpha = int(32 * (1 - r / 240))
        glow_draw.ellipse([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95], fill=(0, 229, 255, alpha))
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 140
    glow_draw.rectangle([cx - 110, ped_y, cx + 110, ped_y + 45], fill=(18, 25, 36), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 130, ped_y + 45, cx + 130, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([cx - 90, ped_y + 14, cx + 90, ped_y + 34], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 75, ped_y + 24), (cx + 75, ped_y + 24)], fill=(223, 186, 107), width=2)

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

    # 4. ELEMENTOS DO TEMA: PAINEL DE INGRESS (ESQUERDA) & ISOLATED PROFILES (DIREITA)
    
    # 4.1. Painel Flutuante Esquerdo: Inbound Multiplex Ingress (Cyan Glow)
    p1_x, p1_y = 260, 370
    p1_w, p1_h = 140, 185
    glow_draw.rectangle([p1_x - p1_w, p1_y - p1_h, p1_x + p1_w, p1_y + p1_h], fill=(10, 22, 34, 215), outline=(0, 229, 255, 220), width=2)
    # Header do painel
    glow_draw.rectangle([p1_x - p1_w, p1_y - p1_h, p1_x + p1_w, p1_y - p1_h + 32], fill=(0, 80, 120, 230), outline=(0, 229, 255), width=1)
    glow_draw.rectangle([p1_x - p1_w + 15, p1_y - p1_h + 8, p1_x + p1_w - 15, p1_y - p1_h + 24], fill=(4, 12, 18), outline=(0, 229, 255), width=1)
    # Título do Header: Inbound Adapters
    glow_draw.line([(p1_x - 55, p1_y - p1_h + 16), (p1_x + 55, p1_y - p1_h + 16)], fill=(0, 229, 255), width=2)
    
    # Adaptadores de Entrada: WhatsApp, Telegram, Slack, Webhooks
    channels = [
        ("WA", "WhatsApp (Baileys Bridge)"),
        ("TG", "Telegram Multi-Bot Ingress"),
        ("SL", "Slack Enterprise Socket"),
        ("WH", "Webhooks & Graph API")
    ]
    for idx, (code, label) in enumerate(channels):
        badge_y = p1_y - 105 + idx * 62
        # Caixa do canal
        glow_draw.rectangle([p1_x - p1_w + 14, badge_y - 18, p1_x + p1_w - 14, badge_y + 22], fill=(6, 16, 26, 200), outline=(0, 229, 255, 120), width=1)
        # Ícone badge [WA], [TG]...
        glow_draw.rectangle([p1_x - p1_w + 20, badge_y - 12, p1_x - p1_w + 58, badge_y + 16], fill=(0, 229, 255, 45), outline=(0, 229, 255), width=1)
        glow_draw.ellipse([p1_x - p1_w + 35, badge_y - 2, p1_x - p1_w + 43, badge_y + 6], fill=(0, 229, 255))
        # Linhas de sinal/dados
        glow_draw.line([(p1_x - p1_w + 68, badge_y - 3), (p1_x + p1_w - 24, badge_y - 3)], fill=(120, 220, 255, 200), width=2)
        glow_draw.line([(p1_x - p1_w + 68, badge_y + 8), (p1_x + p1_w - 55, badge_y + 8)], fill=(80, 160, 200, 130), width=1)
        
        # Filamento convergindo do canal para o Gateway Central
        glow_draw.line([(p1_x + p1_w - 14, badge_y + 2), (cx - 95, cy + idx * 22 - 35)], fill=(0, 229, 255, 150), width=2)
        glow_draw.ellipse([(cx - 98, cy + idx * 22 - 38), (cx - 92, cy + idx * 22 - 32)], fill=(0, 229, 255))

    # 4.2. Painel Flutuante Direito: Isolated Departmental Profiles (Gold Glow)
    p2_x, p2_y = 940, 370
    p2_w, p2_h = 140, 185
    glow_draw.rectangle([p2_x - p2_w, p2_y - p2_h, p2_x + p2_w, p2_y + p2_h], fill=(32, 26, 14, 215), outline=(223, 186, 107, 220), width=2)
    # Header do painel
    glow_draw.rectangle([p2_x - p2_w, p2_y - p2_h, p2_x + p2_w, p2_y - p2_h + 32], fill=(100, 80, 28, 230), outline=(223, 186, 107), width=1)
    glow_draw.rectangle([p2_x - p2_w + 15, p2_y - p2_h + 8, p2_x + p2_w - 15, p2_y - p2_h + 24], fill=(18, 14, 6), outline=(223, 186, 107), width=1)
    # Título do Header: Isolated Profiles
    glow_draw.line([(p2_x - 55, p2_y - p2_h + 16), (p2_x + 55, p2_y - p2_h + 16)], fill=(223, 186, 107), width=2)

    # Departamentos Isolados: Financeiro, Comercial, Suporte, DevOps (Parked)
    profiles = [
        ("FINANCEIRO", "state.db + Banking Keys", True),
        ("COMERCIAL", "state.db + CRM / Leads", True),
        ("SUPORTE", "state.db + FAQs / Ticket", True),
        ("DEVOPS", "state.db [HOT PARKED]", False)
    ]
    for idx, (p_name, p_desc, is_active) in enumerate(profiles):
        badge_y = p2_y - 105 + idx * 62
        glow_draw.rectangle([p2_x - p2_w + 14, badge_y - 18, p2_x + p2_w - 14, badge_y + 22], fill=(22, 18, 8, 200), outline=(223, 186, 107, 120), width=1)
        
        # Tag de Status: [ACTIVE] (Cyan/Gold) ou [PARKED] (Amber/Orange)
        if is_active:
            glow_draw.rectangle([p2_x + p2_w - 56, badge_y - 12, p2_x + p2_w - 20, badge_y + 6], fill=(12, 45, 30), outline=(0, 229, 255), width=1)
            glow_draw.line([(p2_x + p2_w - 50, badge_y - 3), (p2_x + p2_w - 26, badge_y - 3)], fill=(0, 229, 255), width=2)
        else:
            glow_draw.rectangle([p2_x + p2_w - 56, badge_y - 12, p2_x + p2_w - 20, badge_y + 6], fill=(50, 25, 10), outline=(245, 160, 60), width=1)
            glow_draw.line([(p2_x + p2_w - 50, badge_y - 3), (p2_x + p2_w - 26, badge_y - 3)], fill=(245, 160, 60), width=2)

        # Nome do Departamento e Linhas de Metadados
        glow_draw.line([(p2_x - p2_w + 24, badge_y - 3), (p2_x + p2_w - 65, badge_y - 3)], fill=(235, 205, 135, 200), width=2)
        glow_draw.line([(p2_x - p2_w + 24, badge_y + 8), (p2_x + p2_w - 40, badge_y + 8)], fill=(180, 145, 80, 130), width=1)
        
        # Filamento saindo do Gateway Central para cada Perfil
        glow_draw.line([(cx + 95, cy + idx * 22 - 35), (p2_x - p2_w + 14, badge_y + 2)], fill=(223, 186, 107, 150), width=2)
        glow_draw.ellipse([(cx + 92, cy + idx * 22 - 38), (cx + 98, cy + idx * 22 - 32)], fill=(223, 186, 107))

    # 4.3. NÚCLEO CENTRAL HOLOGRÁFICO: O MULTIPLEX PRISM
    prism_y = cy - 140
    # Anel externo e octaedro de multiplexação
    glow_draw.ellipse([cx - 50, prism_y - 50, cx + 50, prism_y + 50], outline=(0, 229, 255, 180), width=2)
    glow_draw.ellipse([cx - 36, prism_y - 36, cx + 36, prism_y + 36], outline=(223, 186, 107, 180), width=2)
    # Prisma central
    glow_draw.polygon([(cx, prism_y - 32), (cx + 28, prism_y), (cx, prism_y + 32), (cx - 28, prism_y)], fill=(12, 35, 52, 220), outline=(215, 235, 255), width=2)
    glow_draw.line([(cx, prism_y - 32), (cx, prism_y + 32)], fill=(0, 229, 255), width=2)
    glow_draw.line([(cx - 28, prism_y), (cx + 28, prism_y)], fill=(223, 186, 107), width=2)

    # 4.4. Rodapé Tecnológico: STATUS BAR (Zero Downtime / ContextVars Isolation)
    bar_y = 740
    glow_draw.rectangle([280, bar_y, 920, bar_y + 36], fill=(10, 15, 22, 230), outline=(0, 229, 255, 180), width=2)
    glow_draw.rectangle([286, bar_y + 6, 440, bar_y + 30], fill=(0, 60, 90), outline=(0, 229, 255), width=1)
    glow_draw.rectangle([455, bar_y + 6, 745, bar_y + 30], fill=(16, 24, 34), outline=(120, 200, 230), width=1)
    glow_draw.rectangle([760, bar_y + 6, 914, bar_y + 30], fill=(60, 48, 16), outline=(223, 186, 107), width=1)

    # Linhas de texto representativas no status bar
    glow_draw.line([(296, bar_y + 18), (430, bar_y + 18)], fill=(0, 229, 255), width=2)
    glow_draw.line([(470, bar_y + 18), (730, bar_y + 18)], fill=(215, 235, 250), width=2)
    glow_draw.line([(775, bar_y + 18), (900, bar_y + 18)], fill=(223, 186, 107), width=2)

    # 5. Partículas flutuantes de dados (Data Orbs)
    for px, py, pcol in [
        (190, 210, (0, 229, 255)), (330, 150, (0, 229, 255)), (470, 240, (0, 229, 255)),
        (730, 240, (223, 186, 107)), (870, 150, (223, 186, 107)), (1010, 210, (223, 186, 107)),
        (440, 530, (0, 229, 255)), (760, 530, (223, 186, 107))
    ]:
        glow_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=pcol)
        glow_draw.ellipse([px - 10, py - 10, px + 10, py + 10], outline=(pcol[0], pcol[1], pcol[2], 80), width=1)

    # 6. Composição final e suavização de glow
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=2))
    im.paste(blurred_glow, (0, 0), blurred_glow)
    
    # Sobrepõe linhas nítidas
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Salvar no diretório estático
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\multiplexing-gateway-hermes.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem contextual salva com sucesso em: {output_path}")
    print(f"📐 Dimensões: {im.size[0]}x{im.size[1]}px (Aspect Ratio 4:3 fit)")

if __name__ == "__main__":
    create_multiplexing_gateway_cover()
