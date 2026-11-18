import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_loops_heartbeat_cover():
    width, height = 1200, 912
    
    im = Image.new("RGB", (width, height), (7, 7, 10))
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    for r in range(580, 0, -14):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-150 - r, 180 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
    for r in range(580, 0, -14):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 180 - r, 1350 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    for y in range(660, height, 18):
        alpha = int(42 * ((y - 660) / (height - 660)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 215, 245, alpha), width=1)
    for x in range(40, width, 55):
        glow_draw.line([(x, 660), (int(600 + (x - 600) * 1.8), height)], fill=(0, 215, 245, 18), width=1)
        
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    col2_x = 1070
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(215, 190, 115, 65), width=2)
    glow_draw.rectangle([col2_x - 14, 85, col2_x + col_w + 14, 115], fill=(42, 36, 16, 220), outline=(223, 186, 107, 220), width=2)
    glow_draw.rectangle([col2_x - 16, 750, col2_x + col_w + 16, 785], fill=(42, 36, 16, 220), outline=(223, 186, 107, 220), width=2)

    glow_draw.polygon([(600, 30), (55, 100), (1145, 100)], outline=(170, 205, 225, 120), width=2)
    glow_draw.polygon([(600, 45), (85, 100), (1115, 100)], outline=(210, 185, 115, 100), width=1)
    glow_draw.rectangle([55, 100, 1145, 115], fill=(15, 18, 26, 180), outline=(160, 195, 215, 110), width=1)
    glow_draw.rectangle([250, 92, 950, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(270, 102), (930, 102)], fill=(223, 186, 107), width=2)

    base_x, base_y = 600, 680
    glow_draw.rectangle([base_x - 180, base_y, base_x + 180, base_y + 40], fill=(18, 26, 38, 230), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([base_x - 210, base_y + 40, base_x + 210, base_y + 70], fill=(12, 18, 28, 240), outline=(0, 229, 255), width=2)
    glow_draw.rectangle([base_x - 160, base_y + 10, base_x + 160, base_y + 30], fill=(5, 10, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(base_x - 140, base_y + 20), (base_x + 140, base_y + 20)], fill=(223, 186, 107), width=2)

    cx, cy = 600, 390
    
    for r in range(240, 40, -10):
        alpha = int(28 * (1 - r / 240))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 229, 255, alpha))
    for r in range(180, 40, -10):
        alpha = int(26 * (1 - r / 180))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(223, 186, 107, alpha))
        
    glow_draw.ellipse([cx - 220, cy - 220, cx + 220, cy + 220], outline=(0, 229, 255, 200), width=3)
    for deg in range(0, 360, 20):
        rad = math.radians(deg)
        x1 = cx + int(220 * math.cos(rad))
        y1 = cy + int(220 * math.sin(rad))
        x2 = cx + int(204 * math.cos(rad))
        y2 = cy + int(204 * math.sin(rad))
        glow_draw.line([(x1, y1), (x2, y2)], fill=(0, 229, 255, 220), width=2)
        
    for deg in range(0, 360, 3):
        rad = math.radians(deg)
        rx = 200 * math.cos(rad)
        ry = 90 * math.sin(rad)
        rot_rad = math.radians(35)
        nx = cx + int(rx * math.cos(rot_rad) - ry * math.sin(rot_rad))
        ny = cy + int(rx * math.sin(rot_rad) + ry * math.cos(rot_rad))
        glow_draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=(223, 186, 107, 210))
        
    for deg in range(0, 360, 3):
        rad = math.radians(deg)
        rx = 200 * math.cos(rad)
        ry = 90 * math.sin(rad)
        rot_rad = math.radians(-35)
        nx = cx + int(rx * math.cos(rot_rad) - ry * math.sin(rot_rad))
        ny = cy + int(rx * math.sin(rot_rad) + ry * math.cos(rot_rad))
        glow_draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=(0, 229, 255, 180))

    hb_pts = []
    x_start = cx - 260
    x_end = cx + 260
    for x in range(x_start, x_end, 4):
        dx = x - cx
        y = cy + 70
        if -160 < dx < -120:
            p = (dx + 140) / 20.0
            y += int(math.sin(p * math.pi * 2) * 35)
        elif -30 < dx < 30:
            if -20 < dx < -10:
                y += 15
            elif -10 <= dx <= 5:
                y -= 60
            elif 5 < dx < 15:
                y += 25
            elif 15 <= dx <= 25:
                y -= 12
        elif 120 < dx < 160:
            p = (dx - 140) / 20.0
            y += int(math.sin(p * math.pi * 2) * 35)
        hb_pts.append((x, y))
        
    for i in range(len(hb_pts) - 1):
        glow_draw.line([hb_pts[i], hb_pts[i+1]], fill=(0, 229, 255, 230), width=3)
        glow_draw.line([(hb_pts[i][0], hb_pts[i][1] - 1), (hb_pts[i+1][0], hb_pts[i+1][1] - 1)], fill=(223, 186, 107, 200), width=1)

    card_w, card_h = 340, 200
    card_x1, card_y1 = cx - card_w // 2, cy - 90
    card_x2, card_y2 = cx + card_w // 2, cy + 110
    
    glow_draw.rectangle([card_x1, card_y1, card_x2, card_y2], fill=(10, 15, 24, 235), outline=(0, 229, 255), width=2)
    glow_draw.rectangle([card_x1 + 4, card_y1 + 4, card_x2 - 4, card_y2 - 4], outline=(223, 186, 107, 120), width=1)
    glow_draw.rectangle([card_x1, card_y1, card_x2, card_y1 + 30], fill=(16, 24, 36, 255), outline=(0, 229, 255), width=1)
    glow_draw.ellipse([card_x1 + 10, card_y1 + 10, card_x1 + 20, card_y1 + 20], fill=(0, 229, 255))
    glow_draw.ellipse([card_x1 + 26, card_y1 + 10, card_x1 + 36, card_y1 + 20], fill=(223, 186, 107))
    glow_draw.ellipse([card_x1 + 42, card_y1 + 10, card_x1 + 52, card_y1 + 20], fill=(70, 90, 110))
    glow_draw.line([(card_x1 + 65, card_y1 + 15), (card_x2 - 15, card_y1 + 15)], fill=(223, 186, 107), width=2)
    glow_draw.line([(card_x1 + 20, card_y1 + 50), (card_x1 + 180, card_y1 + 50)], fill=(0, 229, 255), width=2)
    glow_draw.line([(card_x1 + 195, card_y1 + 50), (card_x2 - 20, card_y1 + 50)], fill=(90, 140, 160), width=2)
    glow_draw.line([(card_x1 + 20, card_y1 + 80), (card_x1 + 220, card_y1 + 80)], fill=(223, 186, 107), width=2)
    glow_draw.line([(card_x1 + 235, card_y1 + 80), (card_x2 - 20, card_y1 + 80)], fill=(0, 229, 255), width=2)
    glow_draw.line([(card_x1 + 20, card_y1 + 110), (card_x1 + 140, card_y1 + 110)], fill=(0, 229, 255), width=2)
    glow_draw.line([(card_x1 + 155, card_y1 + 110), (card_x2 - 20, card_y1 + 110)], fill=(223, 186, 107), width=2)
    glow_draw.line([(card_x1 + 20, card_y1 + 140), (card_x2 - 20, card_y1 + 140)], fill=(0, 215, 245), width=2)
    glow_draw.rectangle([card_x1 + 12, card_y2 - 24, card_x2 - 12, card_y2 - 10], fill=(6, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.rectangle([card_x1 + 14, card_y2 - 22, card_x1 + 180, card_y2 - 12], fill=(0, 229, 255, 200))

    wing_l = [(cx - 180, cy - 130), (cx - 240, cy - 180), (cx - 210, cy - 130), (cx - 250, cy - 110), (cx - 190, cy - 100)]
    glow_draw.polygon(wing_l, outline=(0, 229, 255, 220), fill=(0, 229, 255, 40))
    wing_r = [(cx + 180, cy - 130), (cx + 240, cy - 180), (cx + 210, cy - 130), (cx + 250, cy - 110), (cx + 190, cy - 100)]
    glow_draw.polygon(wing_r, outline=(223, 186, 107, 220), fill=(223, 186, 107, 40))

    im.paste(glow_layer, (0, 0), glow_layer)
    im_final = im.filter(ImageFilter.SMOOTH_MORE)
    
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\autonomia-proativa-loops-recorrentes-heartbeats-hermes.jpg"
    im_final.save(output_path, "JPEG", quality=95)
    print(f"OK {output_path} {im_final.size[0]}x{im_final.size[1]}")

if __name__ == "__main__":
    create_loops_heartbeat_cover()
