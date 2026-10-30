import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_email_triage_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient wash: Left Cyan (#00E5FF) and Right Amber-Gold (#DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor perspective grid
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore e Frontão)
    # Coluna Esquerda (Ciano)
    col1_x = 75
    col_w = 52
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(90, 215, 245, 60), width=2)
    glow_draw.rectangle([col1_x - 14, 90, col1_x + col_w + 14, 120], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 740, col1_x + col_w + 16, 775], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Direita (Ouro)
    col2_x = 1072
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(215, 190, 115, 60), width=2)
    glow_draw.rectangle([col2_x - 14, 90, col2_x + col_w + 14, 120], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 740, col2_x + col_w + 16, 775], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)

    # Frontão Clássico Superior (Triangular Pediment)
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)

    # 3. CENTRO: O BUSTO CLÁSSICO DE HERMES (MENSAGEIRO DOS DEUSES / HERALD)
    cx, cy = 600, 410
    
    # Halo concêntrico de luz (divina e digital)
    for r in range(270, 30, -12):
        alpha = int(38 * (1 - r / 270))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 20, 30, alpha), outline=(0, 229, 255, int(65 * (1 - r / 270))), width=1)
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 145
    glow_draw.rectangle([cx - 95, ped_y, cx + 95, ped_y + 45], fill=(18, 24, 34), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 115, ped_y + 45, cx + 115, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    # Inscrição / Emblema no Pedestal
    glow_draw.rectangle([cx - 65, ped_y + 12, cx + 65, ped_y + 32], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 50, ped_y + 22), (cx + 50, ped_y + 22)], fill=(223, 186, 107), width=2)
    
    # Busto Esculpido de Hermes
    b_head_y = cy - 40
    # Tronco Clássico com Toga de Mármore
    torso = [(cx - 85, b_head_y + 145), (cx - 50, b_head_y + 45), (cx + 50, b_head_y + 45), (cx + 85, b_head_y + 145), (cx, b_head_y + 160)]
    glow_draw.polygon(torso, fill=(18, 26, 38, 240), outline=(210, 225, 240, 220), width=2)
    # Toga plissada em linhas diagonais
    for t_line in range(-35, 45, 18):
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)], fill=(90, 140, 180, 120), width=2)
    
    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([cx - 38, b_head_y - 45, cx + 38, b_head_y + 40], fill=(225, 232, 242, 245), outline=(0, 229, 255, 220), width=2)
    
    # Elmo Alado de Hermes (Petasos Alado)
    glow_draw.ellipse([cx - 45, b_head_y - 52, cx + 45, b_head_y - 30], fill=(190, 205, 220), outline=(223, 186, 107), width=2)
    
    # Asa Esquerda (Ciano Neon)
    wing_l = [(cx - 32, b_head_y - 40), (cx - 95, b_head_y - 92), (cx - 68, b_head_y - 38), (cx - 84, b_head_y - 20), (cx - 32, b_head_y - 15)]
    glow_draw.polygon(wing_l, fill=(15, 45, 65, 230), outline=(0, 229, 255, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx - 35, b_head_y - 35), (cx - 80 + w * 12, b_head_y - 75 + w * 18)], fill=(0, 229, 255, 200), width=2)
        
    # Asa Direita (Ouro Âmbar)
    wing_r = [(cx + 32, b_head_y - 40), (cx + 95, b_head_y - 92), (cx + 68, b_head_y - 38), (cx + 84, b_head_y - 20), (cx + 32, b_head_y - 15)]
    glow_draw.polygon(wing_r, fill=(65, 50, 18, 230), outline=(223, 186, 107, 255), width=2)
    for w in range(3):
        glow_draw.line([(cx + 35, b_head_y - 35), (cx + 80 - w * 12, b_head_y - 75 + w * 18)], fill=(223, 186, 107, 200), width=2)

    # 4. ELEMENTOS DO TEMA: ENVELOPES HOLOGRÁFICOS, DISPOSIÇÕES DE E-MAIL E TRIAGEM
    
    # A. PAINEL DE ENTRADA / INBOX STREAM (Lado Esquerdo - Ciano Elétrico)
    # Caixa Postal de Entrada com Múltiplos Envelopes Flutuantes
    inbox_x, inbox_y = 260, 390
    
    # Bandeja de Entrada Holográfica
    glow_draw.rectangle([inbox_x - 110, inbox_y - 130, inbox_x + 110, inbox_y + 160], fill=(8, 20, 32, 190), outline=(0, 229, 255, 180), width=2)
    # Rótulo de Cabeçalho: INBOX STREAM
    glow_draw.rectangle([inbox_x - 90, inbox_y - 120, inbox_x + 90, inbox_y - 95], fill=(12, 32, 48, 230), outline=(0, 229, 255, 220), width=1)
    glow_draw.line([(inbox_x - 70, inbox_y - 108), (inbox_x + 70, inbox_y - 108)], fill=(0, 229, 255, 230), width=3)
    
    # 3 Envelopes Holográficos na Fila de Entrada
    envelopes_left = [
        {"y": inbox_y - 50, "color": (0, 229, 255), "label": "NEW"},
        {"y": inbox_y + 15, "color": (80, 210, 245), "label": "PARSE"},
        {"y": inbox_y + 80, "color": (120, 230, 255), "label": "THREAD"}
    ]
    for env in envelopes_left:
        ey = env["y"]
        ecol = env["color"]
        # Retângulo do envelope
        glow_draw.rectangle([inbox_x - 85, ey - 22, inbox_x + 85, ey + 22], fill=(10, 24, 38, 230), outline=ecol, width=2)
        # Aba dobrada do envelope (Triângulo superior)
        glow_draw.polygon([(inbox_x - 85, ey - 22), (inbox_x, ey + 4), (inbox_x + 85, ey - 22)], fill=(14, 34, 52, 210), outline=ecol, width=2)
        # Linhas de dobras inferiores
        glow_draw.line([(inbox_x - 85, ey + 22), (inbox_x - 25, ey + 4)], fill=ecol, width=1)
        glow_draw.line([(inbox_x + 85, ey + 22), (inbox_x + 25, ey + 4)], fill=ecol, width=1)
        # Marcador luminoso de status no envelope
        glow_draw.ellipse([inbox_x + 65, ey - 14, inbox_x + 75, ey - 4], fill=ecol)

    # Linhas de feixe neural conectando Inbox de Entrada ao Busto Central
    for by in [-50, 15, 80]:
        glow_draw.line([(inbox_x + 85, inbox_y + by), (cx - 100, cy + by // 2)], fill=(0, 229, 255, 140), width=2)
        glow_draw.ellipse([inbox_x + 120, inbox_y + by - 3, inbox_x + 126, inbox_y + by + 3], fill=(0, 229, 255, 230))

    # B. PAINEL DE DESPACHO SEGURO / RASCUNHOS & PRIORIDADES (Lado Direito - Ouro Âmbar)
    # Caixa de Saída / Triagem Decidida (P0 Urgente, Human-in-the-Loop, Drafts)
    outbox_x, outbox_y = 940, 390
    
    glow_draw.rectangle([outbox_x - 110, outbox_y - 130, outbox_x + 110, outbox_y + 160], fill=(30, 24, 12, 190), outline=(223, 186, 107, 180), width=2)
    # Rótulo de Cabeçalho: DRAFT-FIRST / GOVERNANÇA
    glow_draw.rectangle([outbox_x - 90, outbox_y - 120, outbox_x + 90, outbox_y - 95], fill=(42, 34, 16, 230), outline=(223, 186, 107, 220), width=1)
    glow_draw.line([(outbox_x - 70, outbox_y - 108), (outbox_x + 70, outbox_y - 108)], fill=(223, 186, 107, 230), width=3)
    
    # 3 Envelopes Classificados com Selo de Ouro e Cadeado de Rascunho Seguro
    envelopes_right = [
        {"y": outbox_y - 50, "color": (223, 186, 107), "tag": "P0 URGENTE", "seal": True},
        {"y": outbox_y + 15, "color": (240, 205, 130), "tag": "DRAFT #1", "seal": False},
        {"y": outbox_y + 80, "color": (210, 170, 90), "tag": "ACTION CRM", "seal": False}
    ]
    for env in envelopes_right:
        ey = env["y"]
        ecol = env["color"]
        glow_draw.rectangle([outbox_x - 85, ey - 22, outbox_x + 85, ey + 22], fill=(28, 22, 10, 230), outline=ecol, width=2)
        glow_draw.polygon([(outbox_x - 85, ey - 22), (outbox_x, ey + 4), (outbox_x + 85, ey - 22)], fill=(38, 30, 14, 210), outline=ecol, width=2)
        glow_draw.line([(outbox_x - 85, ey + 22), (outbox_x - 25, ey + 4)], fill=ecol, width=1)
        glow_draw.line([(outbox_x + 85, ey + 22), (outbox_x + 25, ey + 4)], fill=ecol, width=1)
        
        # Selo Dourado de Cera (Sinete Clássico) no envelope P0
        if env["seal"]:
            glow_draw.ellipse([outbox_x - 12, ey - 4, outbox_x + 12, ey + 18], fill=(223, 186, 107, 255), outline=(255, 230, 160), width=2)
            glow_draw.ellipse([outbox_x - 6, ey + 2, outbox_x + 6, ey + 12], fill=(120, 90, 30, 255))
        else:
            # Marcador de Rascunho Seguro (Cadeado / Lock)
            glow_draw.rectangle([outbox_x + 58, ey - 16, outbox_x + 76, ey - 2], fill=(42, 34, 16), outline=ecol, width=1)
            glow_draw.arc([outbox_x + 61, ey - 24, outbox_x + 73, ey - 14], start=180, end=0, fill=ecol, width=2)

    # Linhas de feixe neural conectando Busto Central à Caixa de Saída/Drafts
    for by in [-50, 15, 80]:
        glow_draw.line([(cx + 100, cy + by // 2), (outbox_x - 85, outbox_y + by)], fill=(223, 186, 107, 140), width=2)
        glow_draw.ellipse([outbox_x - 126, outbox_y + by - 3, outbox_x - 120, outbox_y + by + 3], fill=(223, 186, 107, 230))

    # C. ESCUDO CENTRAL HOLOGRÁFICO DE SEGURANÇA (HUMAN-IN-THE-LOOP & ANTI-PHISHING)
    # Posicionado acima do peito de Hermes
    shield_y = cy + 60
    shield_pts = [
        (cx, shield_y + 40),
        (cx + 36, shield_y + 15),
        (cx + 36, shield_y - 20),
        (cx - 36, shield_y - 20),
        (cx - 36, shield_y + 15)
    ]
    glow_draw.polygon(shield_pts, fill=(12, 18, 28, 220), outline=(223, 186, 107, 240), width=2)
    # Marca de verificação / checkmark no escudo
    glow_draw.line([(cx - 16, shield_y + 2), (cx - 4, shield_y + 16)], fill=(0, 229, 255, 255), width=3)
    glow_draw.line([(cx - 4, shield_y + 16), (cx + 18, shield_y - 10)], fill=(0, 229, 255, 255), width=3)

    # D. PARTÍCULAS LUMINOSAS E CARTAS FLUTUANTES NO ESPAÇO
    # E-mails flutuando em órbita com efeito de perspectiva
    orb_emails = [
        (430, 240, -18, (0, 229, 255)),
        (770, 240, 18, (223, 186, 107)),
        (470, 560, 12, (0, 210, 240)),
        (730, 560, -12, (215, 180, 100)),
    ]
    for ox, oy, rot, col in orb_emails:
        # Mini envelope flutuante
        glow_draw.rectangle([ox - 30, oy - 18, ox + 30, oy + 18], fill=(14, 20, 28, 210), outline=col, width=2)
        glow_draw.polygon([(ox - 30, oy - 18), (ox, oy), (ox + 30, oy - 18)], outline=col, width=1)
        glow_draw.ellipse([ox - 4, oy - 4, ox + 4, oy + 4], fill=col)

    # Partículas cintilantes no ar
    particles = [
        (180, 220, (0, 229, 255)), (220, 580, (0, 229, 255)), (380, 180, (0, 229, 255)),
        (980, 210, (223, 186, 107)), (1020, 590, (223, 186, 107)), (820, 170, (223, 186, 107)),
        (600, 160, (200, 230, 255)), (540, 640, (0, 229, 255)), (660, 640, (223, 186, 107))
    ]
    for px, py, pcol in particles:
        glow_draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=pcol)
        glow_draw.ellipse([px - 7, py - 7, px + 7, py + 7], outline=(pcol[0], pcol[1], pcol[2], 90), width=1)

    # 5. MERGE LAYERS E SALVAR
    # Aplicar leve desfoque no glow para atmosfera cinematográfica
    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(1.5))
    final_img = Image.alpha_composite(im.convert("RGBA"), glow_blurred)
    final_rgb = final_img.convert("RGB")
    
    # Destino oficial
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    filename = "triagem-inteligente-de-emails-corporativos-agentes-ia.jpg"
    dest_path = os.path.join(static_dir, filename)
    
    final_rgb.save(dest_path, "JPEG", quality=95)
    print(f"✅ Capa de Email Inbox Triage gerada com sucesso: {dest_path}")
    print(f"Dimensões: {final_rgb.size[0]}x{final_rgb.size[1]}px")
    return dest_path

if __name__ == "__main__":
    create_email_triage_cover()
