import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_cinemaker_cover():
    width, height = 1280, 720
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Ambient color washes: Magenta / Purple on left, Electric Cyan on right, Amber Gold in center
    # Left Magenta wash (Criatividade, Direção de Arte #C000FF)
    for r in range(540, 0, -15):
        alpha = int(45 * (1 - r / 540))
        glow_draw.ellipse([-120 - r, 160 - r, 380 + r, 660 + r], fill=(192, 0, 255, alpha))
        
    # Right Cyan wash (Tecnologia, Motores VO3.1 / Omni #00E5FF)
    for r in range(540, 0, -15):
        alpha = int(45 * (1 - r / 540))
        glow_draw.ellipse([880 - r, 160 - r, 1400 + r, 660 + r], fill=(0, 229, 255, alpha))
        
    # Center Gold halo wash (Cinema de Alto Nível #DFBA6B)
    for r in range(380, 0, -12):
        alpha = int(35 * (1 - r / 380))
        glow_draw.ellipse([640 - r, 360 - r, 640 + r, 360 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic timeline & floor grid
    for y in range(520, height, 18):
        alpha = int(30 * ((y - 520) / (height - 520)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(40, width, 50):
        glow_draw.line([(x, 520), (int(640 + (x - 640) * 1.6), height)], fill=(0, 210, 245, 14), width=1)

    # 2. Top & Bottom Cinematic Filmstrip Borders
    film_h = 36
    # Top strip
    glow_draw.rectangle([0, 0, width, film_h], fill=(12, 12, 18, 220), outline=(255, 255, 255, 25), width=1)
    # Bottom strip
    glow_draw.rectangle([0, height - film_h, width, height], fill=(12, 12, 18, 220), outline=(255, 255, 255, 25), width=1)
    
    # Film sprockets
    sprocket_w, sprocket_h = 20, 14
    for sp_x in range(15, width, 32):
        glow_draw.rounded_rectangle([sp_x, 11, sp_x + sprocket_w, 11 + sprocket_h], radius=3, fill=(5, 5, 8, 240), outline=(0, 229, 255, 100), width=1)
        glow_draw.rounded_rectangle([sp_x, height - film_h + 11, sp_x + sprocket_w, height - film_h + 11 + sprocket_h], radius=3, fill=(5, 5, 8, 240), outline=(223, 186, 107, 100), width=1)

    # 3. Central Cinematic Lens / Aperture Graphic
    cx, cy = 640, 310
    
    # Outer glowing lens rings
    for rad, color, width_line in [(240, (0, 229, 255, 40), 1), (220, (192, 0, 255, 60), 2), (195, (223, 186, 107, 90), 2), (160, (0, 229, 255, 120), 2)]:
        glow_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=color, width=width_line)
        
    # Lens aperture blades (6 blades)
    for i in range(6):
        angle = i * (math.pi / 3)
        x1 = cx + int(155 * math.cos(angle))
        y1 = cy + int(155 * math.sin(angle))
        x2 = cx + int(80 * math.cos(angle + 0.65))
        y2 = cy + int(80 * math.sin(angle + 0.65))
        glow_draw.line([(x1, y1), (x2, y2)], fill=(223, 186, 107, 180), width=3)
        glow_draw.line([(x1, y1), (x2, y2)], fill=(0, 229, 255, 220), width=1)

    # Inner lens glow
    glow_draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill=(15, 15, 25, 210), outline=(0, 229, 255, 180), width=2)
    
    # Center Play Symbol
    poly = [(cx - 15, cy - 25), (cx - 15, cy + 25), (cx + 25, cy)]
    glow_draw.polygon(poly, fill=(223, 186, 107, 240), outline=(255, 255, 255, 200))

    # 4. Floating HUD badges (16:9 / 9:16, VO3.1, Omni, 4K HDR)
    # Badge 1: 16:9 & 9:16
    glow_draw.rounded_rectangle([180, 210, 310, 250], radius=8, fill=(17, 17, 24, 210), outline=(192, 0, 255, 140), width=1)
    # Badge 2: Motores VO3.1 / Omni
    glow_draw.rounded_rectangle([960, 210, 1100, 250], radius=8, fill=(17, 17, 24, 210), outline=(0, 229, 255, 140), width=1)
    # Badge 3: 7 Idiomas Legendas
    glow_draw.rounded_rectangle([180, 370, 330, 410], radius=8, fill=(17, 17, 24, 210), outline=(223, 186, 107, 140), width=1)
    # Badge 4: Áudio & Roteiro 1-Click
    glow_draw.rounded_rectangle([950, 370, 1110, 410], radius=8, fill=(17, 17, 24, 210), outline=(0, 229, 255, 140), width=1)

    # 5. Composite glow onto base
    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(1.2))
    im.paste(glow_blurred, (0, 0), glow_blurred)
    
    # 6. Text Elements using PIL Draw
    draw = ImageDraw.Draw(im)
    
    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 46)
        font_mid = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
        font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
    except Exception:
        font_large = ImageFont.load_default()
        font_mid = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Draw Badge texts
    draw.text((205, 222), "16:9 & 9:16 NATIVO", fill=(217, 102, 255), font=font_badge)
    draw.text((980, 222), "VO3.1 • OMNI ENGINE", fill=(0, 229, 255), font=font_badge)
    draw.text((202, 382), "7 IDIOMAS LEGENDAS", fill=(223, 186, 107), font=font_badge)
    draw.text((975, 382), "MIX & ROTEIRO 1-CLIQUE", fill=(0, 229, 255), font=font_badge)

    # Top Brand Header
    draw.text((cx, 80), "INTELIGÊNCIA AGÊNTICA • APP NATIVO FLOW", fill=(160, 160, 180), font=font_small, anchor="mm")
    
    # Title & Tagline below lens
    draw.text((cx, 475), "CineMaker", fill=(255, 255, 255), font=font_large, anchor="mm")
    draw.text((cx, 515), "MÁQUINA DE CRIAR VÍDEOS LONGOS COM IA", fill=(223, 186, 107), font=font_mid, anchor="mm")
    draw.text((cx, 545), "Produção Audiovisual Completa em 1 Clique • Sem Assinatura Paga no Flow", fill=(170, 190, 210), font=font_small, anchor="mm")

    # Bottom indicators
    draw.text((width // 2, height - 18), "• CONSISTÊNCIA VISUAL • ROTEIROS AUTOMÁTICOS • STORYBOARD 4S-10S • MIXAGEM DE ESTÚDIO •", fill=(110, 120, 140), font=font_badge, anchor="mm")

    # Output path
    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cinemaker-cover.jpg")
    im.save(out_path, quality=95)
    print(f"✅ Imagem gerada com sucesso: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    create_cinemaker_cover()
