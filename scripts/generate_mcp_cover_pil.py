import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_mcp_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    draw = ImageDraw.Draw(im, "RGBA")
    
    # 2. Add dramatic radial and gradient lighting
    # Left side: Electric Cyan (#00E5FF) glow
    # Right side: Warm Amber-Gold (#DFBA6B) glow
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash
    for r in range(450, 0, -15):
        alpha = int(35 * (1 - r / 450))
        glow_draw.ellipse([ -100 - r, 200 - r, 350 + r, 650 + r ], fill=(0, 229, 255, alpha))
        
    # Right Gold ambient wash
    for r in range(450, 0, -15):
        alpha = int(35 * (1 - r / 450))
        glow_draw.ellipse([ 850 - r, 200 - r, 1300 + r, 650 + r ], fill=(223, 186, 107, alpha))
        
    # Bottom subtle cyber floor gradient
    for y in range(600, height):
        progress = (y - 600) / (height - 600)
        c_alpha = int(25 * progress)
        glow_draw.line([(0, y), (width, y)], fill=(0, 180, 220, c_alpha))
        
    # 3. Draw Classical Architectural Columns (Greco-Roman Corinthian Pillars)
    # Left Column (Cyan-lit)
    col_left_x = 180
    col_w = 70
    # Column shaft with vertical fluting
    for fl in range(7):
        fl_x = col_left_x + fl * 10
        glow_draw.line([(fl_x, 150), (fl_x, 800)], fill=(120, 210, 240, 70), width=2)
    # Column base and capital
    glow_draw.rectangle([col_left_x - 20, 130, col_left_x + col_w + 20, 160], fill=(20, 45, 60, 160), outline=(0, 229, 255, 180), width=2)
    glow_draw.rectangle([col_left_x - 25, 780, col_left_x + col_w + 25, 830], fill=(20, 45, 60, 160), outline=(0, 229, 255, 180), width=2)
    
    # Right Column (Gold-lit)
    col_right_x = 950
    for fl in range(7):
        fl_x = col_right_x + fl * 10
        glow_draw.line([(fl_x, 150), (fl_x, 800)], fill=(230, 200, 130, 70), width=2)
    glow_draw.rectangle([col_right_x - 20, 130, col_right_x + col_w + 20, 160], fill=(50, 40, 20, 160), outline=(223, 186, 107, 180), width=2)
    glow_draw.rectangle([col_right_x - 25, 780, col_right_x + col_w + 25, 830], fill=(50, 40, 20, 160), outline=(223, 186, 107, 180), width=2)

    # 4. Central Classical Bust Silhouette & Marble Geometry
    center_x = 600
    center_y = 440
    
    # Elegant Greco-Roman pediment / portico arch above
    glow_draw.polygon([
        (center_x, 100),
        (col_left_x - 30, 140),
        (col_right_x + col_w + 30, 140)
    ], fill=(15, 18, 26, 180), outline=(100, 180, 220, 140))
    
    # Central Hermes Classical Bust & Winged Helm Geometric Silhouette
    # Head & Neck
    glow_draw.ellipse([center_x - 90, center_y - 170, center_x + 90, center_y + 10], fill=(210, 215, 225, 230), outline=(0, 229, 255, 200), width=2)
    # Winged helmet left wing (Cyan)
    glow_draw.polygon([
        (center_x - 70, center_y - 120),
        (center_x - 170, center_y - 200),
        (center_x - 150, center_y - 110),
        (center_x - 80, center_y - 90)
    ], fill=(160, 235, 255, 210), outline=(0, 229, 255, 255), width=2)
    
    # Winged helmet right wing (Gold)
    glow_draw.polygon([
        (center_x + 70, center_y - 120),
        (center_x + 170, center_y - 200),
        (center_x + 150, center_y - 110),
        (center_x + 80, center_y - 90)
    ], fill=(245, 220, 160, 210), outline=(223, 186, 107, 255), width=2)

    # Bust Torso / Shoulders with Split Lighting
    # Left shoulder (Cyan marble)
    glow_draw.polygon([
        (center_x, center_y + 10),
        (center_x - 220, center_y + 190),
        (center_x - 180, center_y + 260),
        (center_x, center_y + 240)
    ], fill=(150, 210, 235, 240), outline=(0, 229, 255, 200), width=2)
    
    # Right shoulder (Gold marble)
    glow_draw.polygon([
        (center_x, center_y + 10),
        (center_x + 220, center_y + 190),
        (center_x + 180, center_y + 260),
        (center_x, center_y + 240)
    ], fill=(235, 205, 145, 240), outline=(223, 186, 107, 200), width=2)

    # 5. MCP Circuit Conduits & Fiber-Optic Neural Streams
    # Intertwining fiber lines connecting columns to bust and floating data matrices
    for offset in range(-30, 40, 15):
        # Left cyan conduits
        glow_draw.line([(col_left_x + 35, 450 + offset), (center_x - 140, center_y + 80 + offset)], fill=(0, 229, 255, 180), width=2)
        # Right gold conduits
        glow_draw.line([(col_right_x + 35, 450 + offset), (center_x + 140, center_y + 80 + offset)], fill=(223, 186, 107, 180), width=2)

    # 6. Floating Holographic Database Tables & MCP Schemas
    # Left Holographic Table (PostgreSQL / Relational Data)
    tbl_l_x, tbl_l_y = 110, 280
    tbl_w, tbl_h = 240, 160
    glow_draw.rectangle([tbl_l_x, tbl_l_y, tbl_l_x + tbl_w, tbl_l_y + tbl_h], fill=(10, 25, 35, 200), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([tbl_l_x, tbl_l_y, tbl_l_x + tbl_w, tbl_l_y + 35], fill=(0, 180, 220, 120))
    glow_draw.line([(tbl_l_x, tbl_l_y + 75), (tbl_l_x + tbl_w, tbl_l_y + 75)], fill=(0, 229, 255, 100), width=1)
    glow_draw.line([(tbl_l_x, tbl_l_y + 115), (tbl_l_x + tbl_w, tbl_l_y + 115)], fill=(0, 229, 255, 100), width=1)
    glow_draw.line([(tbl_l_x + 80, tbl_l_y + 35), (tbl_l_x + 80, tbl_l_y + tbl_h)], fill=(0, 229, 255, 100), width=1)
    
    # Right Holographic Table (ERP / Financials Schema)
    tbl_r_x, tbl_r_y = 850, 280
    glow_draw.rectangle([tbl_r_x, tbl_r_y, tbl_r_x + tbl_w, tbl_r_y + tbl_h], fill=(35, 28, 15, 200), outline=(223, 186, 107, 220), width=2)
    glow_draw.rectangle([tbl_r_x, tbl_r_y, tbl_r_x + tbl_w, tbl_r_y + 35], fill=(200, 160, 70, 120))
    glow_draw.line([(tbl_r_x, tbl_r_y + 75), (tbl_r_x + tbl_w, tbl_r_y + 75)], fill=(223, 186, 107, 100), width=1)
    glow_draw.line([(tbl_r_x, tbl_r_y + 115), (tbl_r_x + tbl_w, tbl_r_y + 115)], fill=(223, 186, 107, 100), width=1)
    glow_draw.line([(tbl_r_x + 80, tbl_r_y + 35), (tbl_r_x + 80, tbl_r_y + tbl_h)], fill=(223, 186, 107, 100), width=1)

    # 7. MCP Hub Node / Connector Ring in Center Foreground
    hub_y = 670
    for ring_r in range(65, 0, -10):
        glow_draw.ellipse([center_x - ring_r, hub_y - ring_r, center_x + ring_r, hub_y + ring_r], outline=(0, 229, 255, 150 if ring_r > 30 else 220), width=2)
    glow_draw.ellipse([center_x - 25, hub_y - 25, center_x + 25, hub_y + 25], fill=(223, 186, 107, 220), outline=(255, 255, 255, 255), width=2)
    
    # Connecting rays from MCP hub
    glow_draw.line([(center_x, hub_y - 65), (center_x, center_y + 240)], fill=(0, 229, 255, 220), width=3)
    glow_draw.line([(center_x - 65, hub_y), (tbl_l_x + tbl_w, tbl_l_y + tbl_h - 20)], fill=(0, 229, 255, 160), width=2)
    glow_draw.line([(center_x + 65, hub_y), (tbl_r_x, tbl_r_y + tbl_h - 20)], fill=(223, 186, 107, 160), width=2)

    # 8. Merge and add subtle bloom / softening
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Final sharpen & output save
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\mcp-model-context-protocol-hermes.jpg"
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Capa contextual gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_mcp_cover()
