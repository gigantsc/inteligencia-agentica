import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_skills_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Knowledge / Learning)
    for r in range(560, 0, -12):
        alpha = int(40 * (1 - r / 560))
        glow_draw.ellipse([-120 - r, 200 - r, 400 + r, 700 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Mastery / Evolution)
    for r in range(560, 0, -12):
        alpha = int(40 * (1 - r / 560))
        glow_draw.ellipse([800 - r, 200 - r, 1320 + r, 700 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid
    for y in range(680, height, 22):
        alpha = int(30 * ((y - 680) / (height - 680)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 200, 240, alpha), width=1)
    for x in range(80, width, 65):
        glow_draw.line([(x, 680), (int(600 + (x - 600) * 1.6), height)], fill=(0, 200, 240, 16), width=1)
        
    # 2. GRAN BIBLIOTECA CLÁSSICA - Pórtico e Colunas
    # Far Left Column (Ciano)
    col1_x = 90
    col_w = 48
    for fl in range(5):
        fl_x = col1_x + fl * 10
        glow_draw.line([(fl_x, 120), (fl_x, 770)], fill=(100, 210, 240, 55), width=2)
    glow_draw.rectangle([col1_x - 14, 100, col1_x + col_w + 14, 130], fill=(12, 35, 50, 200), outline=(0, 229, 255, 200), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 50, 200), outline=(0, 229, 255, 200), width=2)
    
    # Far Right Column (Ouro)
    col2_x = 1060
    for fl in range(5):
        fl_x = col2_x + fl * 10
        glow_draw.line([(fl_x, 120), (fl_x, 770)], fill=(210, 185, 110, 55), width=2)
    glow_draw.rectangle([col2_x - 14, 100, col2_x + col_w + 14, 130], fill=(40, 35, 15, 200), outline=(223, 186, 107, 200), width=2)
    glow_draw.rectangle([col2_x - 16, 750, col2_x + col_w + 16, 785], fill=(40, 35, 15, 200), outline=(223, 186, 107, 200), width=2)

    # Inner Left Column (Ciano, smaller)
    col3_x = 240
    col3_w = 38
    for fl in range(4):
        fl_x = col3_x + fl * 9
        glow_draw.line([(fl_x, 140), (fl_x, 740)], fill=(80, 200, 230, 40), width=2)
    glow_draw.rectangle([col3_x - 10, 125, col3_x + col3_w + 10, 150], fill=(10, 30, 42, 180), outline=(0, 210, 240, 160), width=2)
    glow_draw.rectangle([col3_x - 12, 725, col3_x + col3_w + 12, 755], fill=(10, 30, 42, 180), outline=(0, 210, 240, 160), width=2)

    # Inner Right Column (Ouro, smaller)
    col4_x = 920
    for fl in range(4):
        fl_x = col4_x + fl * 9
        glow_draw.line([(fl_x, 140), (fl_x, 740)], fill=(200, 175, 100, 40), width=2)
    glow_draw.rectangle([col4_x - 10, 125, col4_x + col3_w + 10, 150], fill=(35, 30, 12, 180), outline=(210, 175, 100, 160), width=2)
    glow_draw.rectangle([col4_x - 12, 725, col4_x + col3_w + 12, 755], fill=(35, 30, 12, 180), outline=(210, 175, 100, 160), width=2)

    # Grand Pediment / Archway
    glow_draw.polygon([(600, 40), (70, 115), (1130, 115)], outline=(170, 200, 220, 100), width=2)
    glow_draw.polygon([(600, 55), (100, 115), (1100, 115)], outline=(200, 180, 110, 80), width=1)
    
    # Entablature (horizontal beam)
    glow_draw.rectangle([70, 115, 1130, 130], fill=(15, 18, 22, 160), outline=(150, 190, 210, 90), width=1)
    
    # 3. PRATELEIRAS DE SCROLLS / SKILLS (3 níveis = Progressive Disclosure)
    shelf_colors_cyan = [(0, 229, 255), (20, 200, 235), (40, 180, 220)]
    shelf_colors_gold = [(223, 186, 107), (200, 170, 95), (180, 155, 85)]
    shelf_y_positions = [200, 380, 540]
    
    for si, shelf_y in enumerate(shelf_y_positions):
        # Shelf beam (horizontal)
        beam_alpha = 80 - si * 15
        glow_draw.rectangle([160, shelf_y + 95, 500, shelf_y + 100], fill=(*shelf_colors_cyan[si], beam_alpha), width=0)
        glow_draw.rectangle([700, shelf_y + 95, 1040, shelf_y + 100], fill=(*shelf_colors_gold[si], beam_alpha), width=0)

        # Left side scrolls/books (Cyan hue - Knowledge)
        num_scrolls_left = 5 - si
        for j in range(num_scrolls_left):
            sx = 185 + j * 62
            scroll_h = 70 + (j % 3) * 15
            scroll_y = shelf_y + 95 - scroll_h
            c = shelf_colors_cyan[si]
            alpha_scroll = 120 - si * 25
            # Book body
            glow_draw.rectangle([sx, scroll_y, sx + 35, shelf_y + 94], fill=(c[0]//6, c[1]//6, c[2]//6, alpha_scroll + 40), outline=(*c, alpha_scroll), width=1)
            # Spine glow
            glow_draw.line([(sx + 2, scroll_y + 5), (sx + 2, shelf_y + 89)], fill=(*c, alpha_scroll + 30), width=2)
            # Neural dot on top
            if j % 2 == 0:
                glow_draw.ellipse([sx + 12, scroll_y - 8, sx + 23, scroll_y + 3], fill=(*c, 160), outline=(*c, 200))

        # Right side scrolls/books (Gold hue - Mastery)
        num_scrolls_right = 5 - si
        for j in range(num_scrolls_right):
            sx = 725 + j * 62
            scroll_h = 65 + ((j + 1) % 3) * 18
            scroll_y = shelf_y + 95 - scroll_h
            c = shelf_colors_gold[si]
            alpha_scroll = 120 - si * 25
            # Book body
            glow_draw.rectangle([sx, scroll_y, sx + 35, shelf_y + 94], fill=(c[0]//6, c[1]//6, c[2]//6, alpha_scroll + 40), outline=(*c, alpha_scroll), width=1)
            # Spine glow
            glow_draw.line([(sx + 33, scroll_y + 5), (sx + 33, shelf_y + 89)], fill=(*c, alpha_scroll + 30), width=2)
            # Neural dot on top
            if j % 2 == 1:
                glow_draw.ellipse([sx + 12, scroll_y - 8, sx + 23, scroll_y + 3], fill=(*c, 160), outline=(*c, 200))

    # Level labels along shelves (representing Progressive Disclosure levels)
    for si, (shelf_y, label) in enumerate(zip(shelf_y_positions, ["LEVEL 0", "LEVEL 1", "LEVEL 2"])):
        text_alpha = 90 - si * 15
        glow_draw.text((520, shelf_y + 40), label, fill=(180, 200, 215, text_alpha))

    # 4. CENTRAL FIGURE: Hermes as Scholar-Scribe
    # Bust/Head - marble texture suggestion
    cx, cy = 600, 440
    
    # Bust base pedestal
    glow_draw.polygon([(cx-60, cy+130), (cx+60, cy+130), (cx+75, cy+180), (cx-75, cy+180)], fill=(25, 28, 32, 200), outline=(150, 180, 200, 120), width=2)
    
    # Shoulders (trapezoidal classical form)
    glow_draw.polygon([(cx-100, cy+15), (cx+100, cy+15), (cx+120, cy+130), (cx-120, cy+130)], fill=(30, 33, 38, 220), outline=(140, 170, 195, 100), width=2)
    # Shoulder drape lines
    for i in range(5):
        glow_draw.line([(cx - 80 + i * 35, cy + 20), (cx - 100 + i * 40, cy + 125)], fill=(120, 150, 175, 60), width=1)

    # Neck
    glow_draw.rectangle([cx - 25, cy - 30, cx + 25, cy + 20], fill=(35, 38, 43, 200), outline=(145, 170, 190, 90), width=1)
    
    # Head (classical oval)
    glow_draw.ellipse([cx - 55, cy - 130, cx + 55, cy - 15], fill=(38, 41, 46, 230), outline=(160, 180, 200, 120), width=2)
    
    # Helmet (petasos/winged cap of Hermes - simplified)
    glow_draw.arc([cx - 65, cy - 150, cx + 65, cy - 80], 180, 0, fill=(180, 200, 220, 140), width=3)
    glow_draw.line([(cx - 65, cy - 115), (cx + 65, cy - 115)], fill=(180, 200, 220, 100), width=2)
    
    # Wings on helmet
    # Left wing
    glow_draw.polygon([(cx - 60, cy - 120), (cx - 110, cy - 155), (cx - 90, cy - 110)], 
                      fill=(0, 180, 220, 80), outline=(0, 229, 255, 150), width=1)
    glow_draw.polygon([(cx - 90, cy - 130), (cx - 130, cy - 160), (cx - 105, cy - 115)], 
                      fill=(0, 160, 200, 60), outline=(0, 210, 240, 120), width=1)
    # Right wing
    glow_draw.polygon([(cx + 60, cy - 120), (cx + 110, cy - 155), (cx + 90, cy - 110)], 
                      fill=(200, 170, 90, 80), outline=(223, 186, 107, 150), width=1)
    glow_draw.polygon([(cx + 90, cy - 130), (cx + 130, cy - 160), (cx + 105, cy - 115)], 
                      fill=(180, 155, 75, 60), outline=(210, 180, 100, 120), width=1)
    
    # Eyes (subtle glow)
    glow_draw.ellipse([cx - 25, cy - 85, cx - 10, cy - 72], fill=(0, 200, 240, 180))
    glow_draw.ellipse([cx + 10, cy - 85, cx + 25, cy - 72], fill=(200, 170, 90, 180))
    
    # 5. FLOATING SCROLLS / SKILL DOCUMENTS around Hermes (the learning aura)
    scroll_positions = [
        (cx - 180, cy - 60, 'cyan'),
        (cx + 160, cy - 50, 'gold'),
        (cx - 150, cy + 40, 'cyan'),
        (cx + 140, cy + 50, 'gold'),
        (cx - 200, cy - 140, 'cyan'),
        (cx + 180, cy - 130, 'gold'),
    ]
    
    for sx, sy, tone in scroll_positions:
        if tone == 'cyan':
            c = (0, 229, 255)
        else:
            c = (223, 186, 107)
        
        # Scroll body
        glow_draw.rounded_rectangle([sx - 22, sy - 15, sx + 22, sy + 15], radius=5, 
                                     fill=(c[0]//8, c[1]//8, c[2]//8, 160), outline=(*c, 130), width=1)
        # Text lines on scroll
        for line_i in range(3):
            ly = sy - 8 + line_i * 7
            lw = 28 - line_i * 5
            glow_draw.line([(sx - lw//2, ly), (sx + lw//2, ly)], fill=(*c, 80), width=1)
        
        # Connection filament from scroll to Hermes
        # Bezier-like line (simplified as segmented)
        mid_x = (sx + cx) / 2 + (10 if tone == 'cyan' else -10)
        mid_y = (sy + cy) / 2 - 20
        for seg in range(8):
            t = seg / 8
            x1 = sx * (1-t) + mid_x * t
            y1 = sy * (1-t) + mid_y * t
            t2 = (seg+1) / 8
            x2 = sx * (1-t2) + mid_x * t2
            y2 = sy * (1-t2) + mid_y * t2
            alpha_line = int(60 * (1 - t))
            glow_draw.line([(x1, y1), (x2, y2)], fill=(*c, alpha_line), width=1)
        for seg in range(8):
            t = seg / 8
            x1 = mid_x * (1-t) + cx * t
            y1 = mid_y * (1-t) + (cy - 30) * t
            t2 = (seg+1) / 8
            x2 = mid_x * (1-t2) + cx * t2
            y2 = mid_y * (1-t2) + (cy - 30) * t2
            alpha_line = int(40 * (1 - t * 0.5))
            glow_draw.line([(x1, y1), (x2, y2)], fill=(*c, alpha_line), width=1)
    
    # 6. QUILL / STYLUS OF LIGHT (writing new skills - bottom right)
    # Quill shaft
    qx, qy = cx + 170, cy + 90
    glow_draw.line([(qx, qy), (qx + 80, qy - 120)], fill=(223, 186, 107, 180), width=3)
    # Quill tip glow
    for r in range(25, 0, -3):
        a = int(80 * (1 - r / 25))
        glow_draw.ellipse([qx - r, qy - r, qx + r, qy + r], fill=(223, 186, 107, a))
    # Feather vanes
    glow_draw.polygon([(qx + 55, qy - 90), (qx + 105, qy - 140), (qx + 75, qy - 110)], 
                      fill=(223, 186, 107, 60), outline=(223, 186, 107, 100))
    glow_draw.polygon([(qx + 60, qy - 95), (qx + 30, qy - 145), (qx + 50, qy - 105)], 
                      fill=(0, 200, 230, 50), outline=(0, 229, 255, 90))
    
    # 7. CIRCULAR RUNES / DATA ORBIT around bust (knowledge cycle)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        orbit_r = 220
        ox = int(cx + orbit_r * math.cos(rad))
        oy = int(cy - 30 + orbit_r * 0.65 * math.sin(rad))
        if angle < 180:
            c = (0, 229, 255)
        else:
            c = (223, 186, 107)
        dot_alpha = 100 + int(55 * abs(math.sin(rad * 2)))
        glow_draw.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=(*c, dot_alpha))
    
    # Orbital ring
    glow_draw.ellipse([cx - 220, cy - 170, cx + 220, cy + 110], outline=(100, 160, 190, 50), width=1)
    
    # 8. PARTICLE / STAR FIELD (subtle background texture)
    import random
    random.seed(42)
    for _ in range(120):
        px = random.randint(0, width)
        py = random.randint(0, height - 150)
        ps = random.randint(1, 3)
        pa = random.randint(30, 90)
        if px < width // 2:
            glow_draw.ellipse([px, py, px + ps, py + ps], fill=(0, 200, 240, pa))
        else:
            glow_draw.ellipse([px, py, px + ps, py + ps], fill=(200, 175, 100, pa))
    
    # 9. Bottom glow horizon
    for y in range(height - 100, height):
        alpha = int(25 * ((y - (height - 100)) / 100))
        glow_draw.line([(0, y), (width // 2, y)], fill=(0, 200, 240, alpha), width=1)
        glow_draw.line([(width // 2, y), (width, y)], fill=(200, 175, 100, alpha), width=1)

    # Composite glow onto base
    im.paste(Image.alpha_composite(Image.new("RGBA", (width, height), (0, 0, 0, 255)), glow_layer).convert("RGB"))
    
    # 10. Subtle gaussian blur on full image for atmosphere 
    im_blurred = im.filter(ImageFilter.GaussianBlur(1.2))
    
    # Blend: 70% sharp, 30% blur for dreamy effect
    im = Image.blend(im, im_blurred, 0.25)
    
    return im

if __name__ == "__main__":
    img = create_skills_cover()
    out_path = os.path.join("D:/DevCod/inteligencia-agentica/static/images", "skills-sistema-auto-aperfeicoamento-agentes-ia.jpg")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "JPEG", quality=92)
    print(f"Cover image saved to {out_path}")
    print(f"Size: {img.size}")
