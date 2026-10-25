import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_credential_vault_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Zero-Knowledge Ingestion & CDP Browser Protocol #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Cryptographic Vault & Fernet AES-256 #DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore com Conduítes Criptográficos)
    # Coluna Esquerda (Ciano)
    col1_x = 80
    col_w = 55
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 770)], fill=(90, 215, 245, 60), width=2)
    glow_draw.rectangle([col1_x - 14, 90, col1_x + col_w + 14, 120], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Direita (Ouro)
    col2_x = 1065
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 770)], fill=(215, 190, 115, 60), width=2)
    glow_draw.rectangle([col2_x - 14, 90, col2_x + col_w + 14, 120], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 750, col2_x + col_w + 16, 785], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)

    # Frontão Clássico Superior
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)
    
    # 3. CENTRO: O COFRE DE SEGURANÇA CRIPTOGRÁFICO (GRANDE CÂMARA EM FORMA DE COFRE OURO E CIANO)
    cx, cy = 600, 420
    
    # Halo concêntrico
    for r in range(260, 40, -12):
        alpha = int(40 * (1 - r / 260))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 20, 28, alpha), outline=(0, 229, 255, int(70 * (1 - r / 260))), width=1)
        
    # Grande Engrenagem de Cofre / Círculo de Blindagem
    vault_r = 175
    glow_draw.ellipse([cx - vault_r, cy - vault_r, cx + vault_r, cy + vault_r], fill=(10, 15, 22, 230), outline=(223, 186, 107, 240), width=4)
    glow_draw.ellipse([cx - vault_r + 15, cy - vault_r + 15, cx + vault_r - 15, cy + vault_r - 15], outline=(0, 229, 255, 200), width=2)
    
    # Dentes da engrenagem do cofre (8 raios mecânicos)
    for i in range(8):
        angle = i * (math.pi / 4)
        x1 = cx + math.cos(angle) * (vault_r - 5)
        y1 = cy + math.sin(angle) * (vault_r - 5)
        x2 = cx + math.cos(angle) * (vault_r + 20)
        y2 = cy + math.sin(angle) * (vault_r + 20)
        glow_draw.line([(x1, y1), (x2, y2)], fill=(223, 186, 107, 240), width=8)

    # Marcadores circulares ao redor da fechadura do cofre
    for i in range(16):
        angle = i * (math.pi / 8)
        px = cx + math.cos(angle) * (vault_r - 28)
        py = cy + math.sin(angle) * (vault_r - 28)
        glow_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(0, 229, 255, 220))

    # 4. BUSTO CLÁSSICO DE HERMES GUARDANDO O COFRE (SILHUETA NOBRE DENTRO DO COFRE)
    # Cabeça e Elmo Alado
    b_head_y = cy - 45
    glow_draw.ellipse([cx - 36, b_head_y - 45, cx + 36, b_head_y + 35], fill=(220, 225, 235, 240), outline=(0, 229, 255, 220), width=2)
    
    # Asas do Elmo de Hermes
    # Asa Esquerda (Ciano)
    wing_l = [(cx - 30, b_head_y - 35), (cx - 85, b_head_y - 85), (cx - 60, b_head_y - 35), (cx - 75, b_head_y - 20), (cx - 30, b_head_y - 12)]
    glow_draw.polygon(wing_l, fill=(20, 50, 70, 230), outline=(0, 229, 255, 255), width=2)
    # Asa Direita (Ouro)
    wing_r = [(cx + 30, b_head_y - 35), (cx + 85, b_head_y - 85), (cx + 60, b_head_y - 35), (cx + 75, b_head_y - 20), (cx + 30, b_head_y - 12)]
    glow_draw.polygon(wing_r, fill=(70, 55, 22, 230), outline=(223, 186, 107, 255), width=2)

    # Tronco clássico
    torso = [(cx - 75, b_head_y + 115), (cx - 45, b_head_y + 35), (cx + 45, b_head_y + 35), (cx + 75, b_head_y + 115), (cx, b_head_y + 135)]
    glow_draw.polygon(torso, fill=(18, 24, 34, 240), outline=(210, 220, 230, 200), width=2)

    # 5. CADEADO HOLOGRÁFICO E CHAVE CRIPTOGRÁFICA (Ícone central de blindagem)
    lock_y = cy + 50
    # Arco do cadeado
    glow_draw.arc([cx - 28, lock_y - 32, cx + 28, lock_y + 12], start=180, end=0, fill=(223, 186, 107, 255), width=5)
    # Corpo do cadeado
    glow_draw.rectangle([cx - 32, lock_y - 5, cx + 32, lock_y + 40], fill=(25, 20, 10, 240), outline=(223, 186, 107, 255), width=3)
    # Fechadura luminosa ciano
    glow_draw.ellipse([cx - 6, lock_y + 8, cx + 6, lock_y + 20], fill=(0, 229, 255, 255))
    glow_draw.polygon([(cx - 4, lock_y + 16), (cx + 4, lock_y + 16), (cx + 6, lock_y + 28), (cx - 6, lock_y + 28)], fill=(0, 229, 255, 255))

    # 6. CIRCUITOS DE FIBRA ÓPTICA E ENTRADAS DIGITAIS (CDP Ingestion)
    # Lado esquerdo: painel de login seguro simulado
    glow_draw.rectangle([180, 360, 370, 480], fill=(10, 24, 36, 210), outline=(0, 229, 255, 200), width=2)
    # Linhas de input simulando user e senha censurada com asteriscos holográficos
    glow_draw.rectangle([195, 385, 355, 410], fill=(6, 15, 22, 230), outline=(0, 229, 255, 140), width=1)
    glow_draw.rectangle([195, 425, 355, 450], fill=(6, 15, 22, 230), outline=(0, 229, 255, 140), width=1)
    # Asteriscos luminosos no campo de senha
    for dot in range(6):
        dot_x = 215 + dot * 20
        glow_draw.ellipse([dot_x - 3, 437 - 3, dot_x + 3, 437 + 3], fill=(0, 229, 255, 240))
        
    # Conduíte neural conectando login ao cofre
    glow_draw.line([(370, 420), (cx - vault_r, 420)], fill=(0, 229, 255, 220), width=2)
    for p in range(4):
        glow_draw.ellipse([380 + p * 12 - 3, 420 - 3, 380 + p * 12 + 3, 420 + 3], fill=(0, 229, 255, 255))

    # Lado direito: selo de aprovação humana e TOTP 2FA
    glow_draw.rectangle([830, 360, 1020, 480], fill=(32, 26, 12, 210), outline=(223, 186, 107, 200), width=2)
    # Caixa 2FA com contador temporal
    glow_draw.rectangle([845, 385, 1005, 425], fill=(20, 16, 6, 230), outline=(223, 186, 107, 160), width=1)
    # Dígitos do token 2FA
    for d in range(6):
        d_x = 865 + d * 22
        glow_draw.line([(d_x, 400), (d_x, 412)], fill=(223, 186, 107, 240), width=3)
    # Selo de Human-in-the-Loop na parte inferior
    glow_draw.rectangle([845, 440, 1005, 465], fill=(45, 36, 14, 230), outline=(223, 186, 107, 220), width=1)
    glow_draw.line([(870, 452), (980, 452)], fill=(255, 230, 170, 200), width=2)
    
    # Conduíte conectando 2FA ao cofre
    glow_draw.line([(cx + vault_r, 420), (830, 420)], fill=(223, 186, 107, 220), width=2)

    # 7. Composição final
    im.paste(glow_layer, (0, 0), glow_layer)
    im = im.filter(ImageFilter.SMOOTH_MORE)
    
    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cofre-de-credenciais-credential-vault-agentes-ia.jpg")
    im.save(out_path, format="JPEG", quality=95)
    print(f"✅ Capa gerada com sucesso: {out_path} ({width}x{height})")

if __name__ == "__main__":
    create_credential_vault_cover()
