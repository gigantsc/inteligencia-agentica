import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_egress_proxy_cover():
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
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO & BASTIÃO DE SEGURANÇA
    # Coluna Esquerda (Mármore Ciano / Defesa Perimetral)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Conexão Upstream)
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
    
    # Inscrição clássica no frontão: EGRESS PROXY // IRON-PROXY FIREWALL
    glow_draw.rectangle([390, 92, 810, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)

    # 3. CENTRO: O PORTAL DE FERRO & BASTIÃO (IRON-PROXY GATEWAY)
    # Portal em Arco Romano Fortificado (Portcullis)
    arc_x, arc_y, arc_r = 600, 390, 260
    for i in range(15):
        angle = math.pi * (i / 14)
        px = arc_x + int(arc_r * math.cos(angle))
        py = arc_y - int(arc_r * math.sin(angle))
        glow_draw.line([(px, py), (px, 670)], fill=(20, 40, 55, 160), width=3)
    
    # Grade de ferro / Portcullis transversal
    for gy in range(arc_y - 200, 670, 35):
        glow_draw.line([(arc_x - 240, gy), (arc_x + 240, gy)], fill=(40, 60, 80, 130), width=2)

    # 4. O BUSTO CLÁSSICO DE HERMES & O ESCUDO AEGIS DE ENERGIA
    cx, cy = 600, 420
    
    # Campo de Força Hexagonal / Aegis Energy Shield
    shield_pts = [
        (cx, cy - 250),
        (cx + 210, cy - 130),
        (cx + 185, cy + 170),
        (cx, cy + 280),
        (cx - 185, cy + 170),
        (cx - 210, cy - 130)
    ]
    for r in range(250, 40, -12):
        alpha = int(35 * (1 - r / 250))
        glow_draw.ellipse([cx - r, cy - r * 1.1, cx + r, cy + r * 1.1], fill=(0, 229, 255, alpha))
        
    glow_draw.polygon(shield_pts, outline=(0, 229, 255, 230), width=3)
    # Segundo anel concêntrico do escudo (Dourado)
    inner_shield = [
        (cx, cy - 230),
        (cx + 190, cy - 120),
        (cx + 165, cy + 155),
        (cx, cy + 255),
        (cx - 165, cy + 155),
        (cx - 190, cy - 120)
    ]
    glow_draw.polygon(inner_shield, outline=(223, 186, 107, 190), width=2)

    # Pedestal Clássico de Mármore
    ped_y = cy + 150
    glow_draw.rectangle([cx - 100, ped_y, cx + 100, ped_y + 45], fill=(18, 25, 36), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 120, ped_y + 45, cx + 120, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)

    # Inscrição no Pedestal: SECURE EGRESS BOUNDARY
    glow_draw.rectangle([cx - 85, ped_y + 12, cx + 85, ped_y + 32], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 70, ped_y + 22), (cx + 70, ped_y + 22)], fill=(223, 186, 107), width=2)

    # Tronco Esculpido de Hermes com Armadura e Toga de Mármore
    b_head_y = cy - 35
    torso = [(cx - 90, b_head_y + 145), (cx - 55, b_head_y + 45), (cx + 55, b_head_y + 45), (cx + 90, b_head_y + 145), (cx, b_head_y + 160)]
    glow_draw.polygon(torso, fill=(18, 26, 38, 240), outline=(210, 225, 240, 220), width=2)
    # Pregas da toga clássica
    for t_line in range(-40, 45, 18):
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)], fill=(90, 140, 180, 130), width=2)

    # Cabeça Esculpida em Mármore Nobre
    glow_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], fill=(228, 235, 245, 250), outline=(0, 229, 255, 220), width=2)

    # Elmo Alado de Hermes (Petasos Alado)
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

    # 5. CENÁRIO ESPECÍFICO DE DEFESA ANTI-EXFILTRAÇÃO (LADO ESQUERDO)
    # Container Docker Sandbox (Origem do tráfego interno)
    dock_cx, dock_cy = 280, 420
    # Caixa do Container Docker
    glow_draw.rectangle([dock_cx - 90, dock_cy - 110, dock_cx + 90, dock_cy + 110], fill=(10, 20, 32, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([dock_cx - 80, dock_cy - 100, dock_cx + 80, dock_cy - 70], fill=(16, 32, 48), outline=(0, 229, 255, 160), width=1)
    
    # Ícones de contêiner e token opaco dentro do Docker
    glow_draw.rectangle([dock_cx - 65, dock_cy - 50, dock_cx + 65, dock_cy - 20], fill=(12, 24, 38), outline=(0, 229, 255), width=1)
    glow_draw.rectangle([dock_cx - 65, dock_cy - 10, dock_cx + 65, dock_cy + 20], fill=(12, 24, 38), outline=(0, 229, 255), width=1)
    # Token opaco representado
    glow_draw.line([(dock_cx - 50, dock_cy - 35), (dock_cx + 50, dock_cy - 35)], fill=(0, 229, 255), width=2)
    glow_draw.line([(dock_cx - 50, dock_cy + 5), (dock_cx + 30, dock_cy + 5)], fill=(0, 229, 255), width=2)
    
    # Rótulo Docker Sandbox
    glow_draw.rectangle([dock_cx - 75, dock_cy + 40, dock_cx + 75, dock_cy + 90], fill=(8, 14, 22), outline=(100, 180, 220), width=1)
    glow_draw.line([(dock_cx - 60, dock_cy + 65), (dock_cx + 60, dock_cy + 65)], fill=(0, 229, 255), width=2)

    # Ataque de Prompt Injection & SSRF sendo defletido (Linhas vermelhas colidindo no escudo)
    for attack_y in [350, 410, 470]:
        glow_draw.line([(dock_cx + 95, attack_y), (cx - 195, attack_y)], fill=(255, 65, 85, 220), width=3)
        # Faísca de impacto no escudo
        glow_draw.ellipse([cx - 205, attack_y - 10, cx - 185, attack_y + 10], fill=(255, 90, 110, 255), outline=(255, 255, 255), width=2)
        # Ondas de deflexão
        glow_draw.arc([cx - 225, attack_y - 25, cx - 175, attack_y + 25], start=90, end=270, fill=(0, 229, 255), width=2)

    # 6. CENÁRIO DE INJEÇÃO DE CREDENCIAIS & UPSTREAM (LADO DIREITO)
    # Nuvem de Provedores Oficiais e Cofre de Chaves
    up_cx, up_cy = 920, 420
    # Base do Cofre / Provedores Oficiais
    glow_draw.rectangle([up_cx - 95, up_cy - 110, up_cx + 95, up_cy + 110], fill=(28, 24, 12, 220), outline=(223, 186, 107, 220), width=2)
    glow_draw.rectangle([up_cx - 85, up_cy - 100, up_cx + 85, up_cy - 70], fill=(42, 36, 16), outline=(223, 186, 107, 160), width=1)
    
    # Conexões seguras autorizadas saindo do Iron-Proxy em direção ao upstream (Linhas douradas)
    for out_y in [360, 420, 480]:
        glow_draw.line([(cx + 195, out_y), (up_cx - 100, out_y)], fill=(223, 186, 107, 240), width=3)
        # Pulso de dados criptografados válidos
        glow_draw.ellipse([up_cx - 110, out_y - 8, up_cx - 90, out_y + 8], fill=(255, 230, 150, 255), outline=(223, 186, 107), width=2)

    # Ícone do Cadeado Criptográfico no cofre upstream
    glow_draw.rectangle([up_cx - 50, up_cy - 20, up_cx + 50, up_cy + 30], fill=(36, 30, 14), outline=(223, 186, 107), width=2)
    glow_draw.arc([up_cx - 30, up_cy - 50, up_cx + 30, up_cy - 10], start=180, end=0, fill=(223, 186, 107), width=3)
    glow_draw.ellipse([up_cx - 10, up_cy - 3, up_cx + 10, up_cy + 17], fill=(223, 186, 107))
    
    # Inscrição Upstream: REAL SECRETS / BITWARDEN / OPENROUTER
    glow_draw.rectangle([up_cx - 80, up_cy + 45, up_cx + 80, up_cy + 90], fill=(20, 16, 8), outline=(215, 180, 100), width=1)
    glow_draw.line([(up_cx - 65, up_cy + 68), (up_cx + 65, up_cy + 68)], fill=(223, 186, 107), width=2)

    # 7. FILAMENTOS NEURAIS E TRILHAS DE FIBRA ÓPTICA (CONEXÃO GLOBAL)
    for f in range(5):
        glow_draw.line([(150, 680 + f * 40), (cx - 120, 680 + f * 40)], fill=(0, 229, 255, 80), width=1)
        glow_draw.line([(cx + 120, 680 + f * 40), (1050, 680 + f * 40)], fill=(223, 186, 107, 80), width=1)

    # 8. RENDERIZAÇÃO FINAL E BLUR SUAVE PARA ACABAMENTO CINEMATOGRÁFICO
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=1.8))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Sharp overlay layer for crisp edges
    final_draw = ImageDraw.Draw(final_im)
    final_draw.polygon(shield_pts, outline=(0, 229, 255, 255), width=2)
    final_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], outline=(0, 229, 255, 230), width=2)
    
    # Save image
    output_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "egress-proxy-iron-proxy-seguranca.jpg")
    
    final_im.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_egress_proxy_cover()
