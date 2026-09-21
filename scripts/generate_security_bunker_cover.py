import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_security_bunker_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Firewall / Shield / Secret Redaction)
    for r in range(550, 0, -15):
        alpha = int(45 * (1 - r / 550))
        glow_draw.ellipse([ -140 - r, 160 - r, 400 + r, 700 + r ], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Human-in-the-Loop Governance / Cryptographic Vault)
    for r in range(550, 0, -15):
        alpha = int(45 * (1 - r / 550))
        glow_draw.ellipse([ 800 - r, 160 - r, 1340 + r, 700 + r ], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid
    for y in range(660, height, 25):
        alpha = int(35 * ((y - 660) / (height - 660)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 200, 240, alpha), width=1)
    for x in range(80, width, 75):
        glow_draw.line([(x, 660), (int(600 + (x - 600) * 1.7), height)], fill=(0, 200, 240, 18), width=1)
        
    # 2. Classical Architecture: Fortified Bastion Columns & Bunker Portico
    # Left Fluted Column (Cyan Armor / Defense)
    col_left_x = 140
    col_w = 65
    for fl in range(7):
        fl_x = col_left_x + fl * 9
        glow_draw.line([(fl_x, 130), (fl_x, 790)], fill=(120, 220, 250, 60), width=2)
    glow_draw.rectangle([col_left_x - 15, 110, col_left_x + col_w + 15, 140], fill=(15, 40, 55, 190), outline=(0, 229, 255, 200), width=2)
    glow_draw.rectangle([col_left_x - 20, 770, col_left_x + col_w + 20, 810], fill=(15, 40, 55, 190), outline=(0, 229, 255, 200), width=2)

    # Right Fluted Column (Gold Vault / Governance)
    col_right_x = 1000
    for fl in range(7):
        fl_x = col_right_x + fl * 9
        glow_draw.line([(fl_x, 130), (fl_x, 790)], fill=(230, 200, 120, 60), width=2)
    glow_draw.rectangle([col_right_x - 15, 110, col_right_x + col_w + 15, 140], fill=(45, 38, 18, 190), outline=(223, 186, 107, 200), width=2)
    glow_draw.rectangle([col_right_x - 20, 770, col_right_x + col_w + 20, 810], fill=(45, 38, 18, 190), outline=(223, 186, 107, 200), width=2)

    # Fortified Pediment
    glow_draw.polygon([(600, 65), (110, 130), (1090, 130)], outline=(180, 210, 230, 130), width=2)
    glow_draw.line([(110, 130), (1090, 130)], fill=(0, 229, 255, 160), width=2)

    # 3. Centerpiece: Classical Hermes with Aegis Shield & Cybernetic Defense Fortress
    center_x = 600
    center_y = 430

    # Large Aegis Energy Shield (Concentric Radiant Hexagons & Curves)
    for r in range(240, 0, -12):
        alpha = int(35 * (1 - r / 240))
        glow_draw.ellipse([center_x - r, center_y - r * 1.15, center_x + r, center_y + r * 1.15], fill=(0, 229, 255, alpha))

    # Outer Shield Perimeter Lines (Cyan & Gold dual contour)
    glow_draw.polygon([
        (center_x, center_y - 250),
        (center_x + 190, center_y - 130),
        (center_x + 170, center_y + 160),
        (center_x, center_y + 270),
        (center_x - 170, center_y + 160),
        (center_x - 190, center_y - 130)
    ], outline=(0, 229, 255, 230), width=3)

    glow_draw.polygon([
        (center_x, center_y - 230),
        (center_x + 170, center_y - 120),
        (center_x + 150, center_y + 145),
        (center_x, center_y + 245),
        (center_x - 150, center_y + 145),
        (center_x - 170, center_y - 120)
    ], outline=(223, 186, 107, 190), width=2)

    # Hermes Marble Bust inside the Aegis
    # Head & Helmet
    glow_draw.ellipse([center_x - 65, center_y - 180, center_x + 65, center_y - 50], fill=(215, 220, 230, 240), outline=(0, 229, 255, 220), width=2)
    
    # Left Wing (Cyan)
    glow_draw.polygon([
        (center_x - 50, center_y - 150),
        (center_x - 130, center_y - 210),
        (center_x - 110, center_y - 130),
        (center_x - 60, center_y - 120)
    ], fill=(160, 235, 255, 220), outline=(0, 229, 255, 255), width=2)

    # Right Wing (Gold)
    glow_draw.polygon([
        (center_x + 50, center_y - 150),
        (center_x + 130, center_y - 210),
        (center_x + 110, center_y - 130),
        (center_x + 60, center_y - 120)
    ], fill=(245, 220, 160, 220), outline=(223, 186, 107, 255), width=2)

    # Shoulders & Armored Cuirass with Split-Lighting
    glow_draw.polygon([
        (center_x, center_y - 50),
        (center_x - 140, center_y + 70),
        (center_x - 110, center_y + 170),
        (center_x, center_y + 150)
    ], fill=(150, 210, 235, 235), outline=(0, 229, 255, 200), width=2)

    glow_draw.polygon([
        (center_x, center_y - 50),
        (center_x + 140, center_y + 70),
        (center_x + 110, center_y + 170),
        (center_x, center_y + 150)
    ], fill=(235, 205, 145, 235), outline=(223, 186, 107, 200), width=2)

    # Central Cryptographic Aegis Crest / Security Lock Hologram
    glow_draw.ellipse([center_x - 45, center_y + 20, center_x + 45, center_y + 110], fill=(10, 20, 30, 240), outline=(0, 229, 255, 255), width=3)
    glow_draw.rectangle([center_x - 22, center_y + 55, center_x + 22, center_y + 92], fill=(223, 186, 107, 240), outline=(255, 255, 255, 255), width=2)
    glow_draw.arc([center_x - 16, center_y + 35, center_x + 16, center_y + 65], start=180, end=0, fill=(0, 229, 255, 255), width=3)
    # Keyhole
    glow_draw.ellipse([center_x - 4, center_y + 65, center_x + 4, center_y + 73], fill=(10, 20, 30, 255))
    glow_draw.polygon([(center_x - 3, center_y + 70), (center_x + 3, center_y + 70), (center_x + 4, center_y + 83), (center_x - 4, center_y + 83)], fill=(10, 20, 30, 255))

    # 4. Security Firewall Circuitry & Floating Cryptographic Security Nodes
    # Left Security Nodes (Cyan Firewall / PII Masking)
    for i, offset in enumerate([( -340, -110 ), ( -380, 50 ), ( -320, 210 )]):
        nx = center_x + offset[0]
        ny = center_y + offset[1]
        glow_draw.rectangle([nx - 45, ny - 25, nx + 45, ny + 25], fill=(15, 35, 50, 200), outline=(0, 229, 255, 230), width=2)
        glow_draw.line([(nx + 45, ny), (center_x - 190, center_y + offset[1] * 0.6)], fill=(0, 229, 255, 140), width=2)
        # Pulse dot
        glow_draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(0, 229, 255, 255))

    # Right Security Nodes (Gold Human-in-the-Loop / Governance Vault)
    for i, offset in enumerate([( 340, -110 ), ( 380, 50 ), ( 320, 210 )]):
        nx = center_x + offset[0]
        ny = center_y + offset[1]
        glow_draw.rectangle([nx - 45, ny - 25, nx + 45, ny + 25], fill=(45, 38, 18, 200), outline=(223, 186, 107, 230), width=2)
        glow_draw.line([(nx - 45, ny), (center_x + 190, center_y + offset[1] * 0.6)], fill=(223, 186, 107, 140), width=2)
        # Pulse dot
        glow_draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(223, 186, 107, 255))

    # 5. Executive Header & Subtitle Typography
    # Try loading Arial / Roboto font, fallback to default
    try:
        font_main = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 20)
        font_tag = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    # Upper Badge
    glow_draw.rectangle([center_x - 180, 160, center_x + 180, 195], fill=(12, 24, 36, 220), outline=(0, 229, 255, 180), width=1)
    glow_draw.text((center_x, 177), "HERMES AGENT BUNKER ARCHITECTURE", fill=(0, 229, 255, 240), font=font_tag, anchor="mm")

    # Bottom Title Text
    glow_draw.text((center_x, 825), "GOVERNANÇA & BLINDAGEM AGÊNTICA", fill=(255, 255, 255, 250), font=font_main, anchor="mm")
    glow_draw.text((center_x, 865), "Isolamento de Segredos • Mascaramento PII (LGPD) • Human-in-the-Loop", fill=(223, 186, 107, 220), font=font_sub, anchor="mm")

    # Composite layers with slight gaussian blur for high-end glow
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(1.2))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Save image
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, "bunker-de-seguranca-governanca-agentes-ia.jpg")
    final_im.convert("RGB").save(out_path, "JPEG", quality=95)
    print(f"✅ Imagem salva com sucesso em: {out_path} ({width}x{height}px)")

if __name__ == "__main__":
    create_security_bunker_cover()
