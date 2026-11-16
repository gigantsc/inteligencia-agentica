import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_code_execution_cover():
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
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunata de Mármore e Frontão)
    # Coluna Esquerda (Mármore Ciano / Isolamento de Execução e RPC)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Governança e Economia de Tokens)
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
    
    # Inscrição clássica no frontão: HERMES AGENT // CODE EXECUTION & RPC SOCKET
    glow_draw.rectangle([260, 92, 940, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(280, 102), (920, 102)], fill=(223, 186, 107), width=2)

    # 3. PEDESTAL NEOCLÁSSICO CENTRAL DE MÁRMORE (The Foundation of Execution)
    base_x, base_y = 600, 680
    glow_draw.rectangle([base_x - 160, base_y, base_x + 160, base_y + 40], fill=(18, 26, 38, 230), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([base_x - 190, base_y + 40, base_x + 190, base_y + 70], fill=(12, 18, 28, 240), outline=(0, 229, 255), width=2)
    
    # Rótulo de Mármore no Pedestal: "LOCAL RPC KERNEL // UNIX & TCP SOCKET"
    glow_draw.rectangle([base_x - 140, base_y + 10, base_x + 140, base_y + 30], fill=(5, 10, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(base_x - 120, base_y + 20), (base_x + 120, base_y + 20)], fill=(223, 186, 107), width=2)

    # 4. O NÚCLEO ALGORÍTMICO CENTRAL (THE PYTHON RPC NEXUS)
    cx, cy = 600, 390
    
    # Anéis Concéntricos de Execução / Loops em Python (Glow Orbital)
    for r in range(210, 40, -10):
        alpha = int(32 * (1 - r / 210))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 229, 255, alpha))
    for r in range(160, 40, -10):
        alpha = int(30 * (1 - r / 160))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(223, 186, 107, alpha))
        
    # Anel Orbital Maior (Ciano) com marcadores de pulso
    glow_draw.ellipse([cx - 210, cy - 210, cx + 210, cy + 210], outline=(0, 229, 255, 180), width=2)
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        px = cx + int(210 * math.cos(rad))
        py = cy + int(210 * math.sin(rad))
        glow_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(0, 229, 255), outline=(255, 255, 255))
        
    # Anel Orbital Interno (Dourado)
    glow_draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=(223, 186, 107, 200), width=2)
    for deg in range(15, 375, 45):
        rad = math.radians(deg)
        px = cx + int(150 * math.cos(rad))
        py = cy + int(150 * math.sin(rad))
        glow_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(223, 186, 107), outline=(255, 255, 255))

    # O Terminal Holográfico Central (Python Kernel IDE / Code Matrix)
    card_w, card_h = 320, 200
    card_x1, card_y1 = cx - card_w // 2, cy - card_h // 2
    card_x2, card_y2 = cx + card_w // 2, cy + card_h // 2
    
    # Fundo do terminal holográfico
    glow_draw.rectangle([card_x1, card_y1, card_x2, card_y2], fill=(8, 14, 24, 235), outline=(0, 229, 255, 240), width=2)
    
    # Barra de título do terminal
    glow_draw.rectangle([card_x1, card_y1, card_x2, card_y1 + 28], fill=(15, 30, 48, 250), outline=(0, 229, 255, 200), width=1)
    # Botões da janela (vermelho/amarelo/verde estilizados)
    glow_draw.ellipse([card_x1 + 10, card_y1 + 9, card_x1 + 20, card_y1 + 19], fill=(255, 95, 86))
    glow_draw.ellipse([card_x1 + 26, card_y1 + 9, card_x1 + 36, card_y1 + 19], fill=(255, 189, 46))
    glow_draw.ellipse([card_x1 + 42, card_y1 + 9, card_x1 + 52, card_y1 + 19], fill=(39, 201, 63))
    # Título da janela
    glow_draw.line([(card_x1 + 75, card_y1 + 14), (card_x1 + 240, card_y1 + 14)], fill=(180, 220, 245), width=2)
    
    # Linhas de Código Python Fluorescentes dentro do Terminal
    code_y = card_y1 + 45
    # Linha 1: from hermes_tools import ...
    glow_draw.line([(card_x1 + 20, code_y), (card_x1 + 70, code_y)], fill=(223, 186, 107), width=3)      # "from"
    glow_draw.line([(card_x1 + 76, code_y), (card_x1 + 175, code_y)], fill=(0, 229, 255), width=3)     # "hermes_tools"
    glow_draw.line([(card_x1 + 182, code_y), (card_x1 + 230, code_y)], fill=(223, 186, 107), width=3)    # "import"
    glow_draw.line([(card_x1 + 236, code_y), (card_x1 + 295, code_y)], fill=(255, 255, 255), width=3)    # "..."
    
    # Linha 2: for item in web_search(...):
    code_y += 24
    glow_draw.line([(card_x1 + 20, code_y), (card_x1 + 45, code_y)], fill=(223, 186, 107), width=3)      # "for"
    glow_draw.line([(card_x1 + 52, code_y), (card_x1 + 88, code_y)], fill=(180, 220, 245), width=3)     # "item"
    glow_draw.line([(card_x1 + 95, code_y), (card_x1 + 112, code_y)], fill=(223, 186, 107), width=3)     # "in"
    glow_draw.line([(card_x1 + 118, code_y), (card_x1 + 225, code_y)], fill=(0, 229, 255), width=3)    # "web_search()"
    
    # Linha 3:     data = read_file(item)
    code_y += 24
    glow_draw.line([(card_x1 + 42, code_y), (card_x1 + 75, code_y)], fill=(180, 220, 245), width=3)     # "data ="
    glow_draw.line([(card_x1 + 82, code_y), (card_x1 + 165, code_y)], fill=(0, 229, 255), width=3)     # "read_file()"
    glow_draw.line([(card_x1 + 172, code_y), (card_x1 + 215, code_y)], fill=(223, 186, 107), width=3)   # "item"
    
    # Linha 4:     if match in data: patch(...)
    code_y += 24
    glow_draw.line([(card_x1 + 42, code_y), (card_x1 + 56, code_y)], fill=(223, 186, 107), width=3)      # "if"
    glow_draw.line([(card_x1 + 62, code_y), (card_x1 + 110, code_y)], fill=(180, 220, 245), width=3)    # "match"
    glow_draw.line([(card_x1 + 118, code_y), (card_x1 + 178, code_y)], fill=(223, 186, 107), width=3)   # "patch()"
    
    # Linha 5: print(consolidated_summary)
    code_y += 26
    glow_draw.line([(card_x1 + 20, code_y), (card_x1 + 62, code_y)], fill=(0, 229, 255), width=4)       # "print("
    glow_draw.line([(card_x1 + 68, code_y), (card_x1 + 230, code_y)], fill=(223, 186, 107), width=4)    # "consolidated_summary"
    glow_draw.line([(card_x1 + 234, code_y), (card_x1 + 242, code_y)], fill=(0, 229, 255), width=4)     # ")"

    # 5. OS 4 NÓS SATÉLITES DE FERRAMENTAS RPC (ORBITING TOOL SATELLITES)
    nodes = [
        {"name": "WEB SEARCH", "x": 240, "y": 250, "color": (0, 229, 255), "icon": "web"},
        {"name": "FILE SYSTEM", "x": 240, "y": 530, "color": (0, 229, 255), "icon": "file"},
        {"name": "CODE PATCH", "x": 960, "y": 250, "color": (223, 186, 107), "icon": "patch"},
        {"name": "TERMINAL", "x": 960, "y": 530, "color": (223, 186, 107), "icon": "terminal"}
    ]
    
    for node in nodes:
        nx, ny = node["x"], node["y"]
        col = node["color"]
        
        # Conduíte de fibra óptica até o terminal central
        glow_draw.line([(nx, ny), (card_x1 if nx < cx else card_x2, ny)], fill=(col[0], col[1], col[2], 140), width=2)
        # Pulsos de dados no conduíte
        mid_x = (nx + (card_x1 if nx < cx else card_x2)) // 2
        glow_draw.ellipse([mid_x - 6, ny - 6, mid_x + 6, ny + 6], fill=(255, 255, 255), outline=col)
        
        # Halo de brilho do satélite
        for r in range(65, 10, -8):
            alpha = int(40 * (1 - r / 65))
            glow_draw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(col[0], col[1], col[2], alpha))
            
        # Plataforma do nó (Card Hexagonal / Retângulo Chanfrado)
        glow_draw.rectangle([nx - 65, ny - 45, nx + 65, ny + 45], fill=(12, 18, 30, 240), outline=col, width=2)
        # Borda interna de destaque
        glow_draw.rectangle([nx - 58, ny - 38, nx + 58, ny + 38], outline=(255, 255, 255, 60), width=1)
        
        # Ícone esquemático dentro do card
        if node["icon"] == "web":
            # Globo / antena
            glow_draw.ellipse([nx - 18, ny - 25, nx + 18, ny + 11], outline=col, width=2)
            glow_draw.line([(nx - 18, ny - 7), (nx + 18, ny - 7)], fill=col, width=1)
            glow_draw.line([(nx, ny - 25), (nx, ny + 11)], fill=col, width=1)
        elif node["icon"] == "file":
            # Documento dobrado
            glow_draw.rectangle([nx - 15, ny - 24, nx + 15, ny + 12], outline=col, width=2)
            glow_draw.line([(nx - 10, ny - 14), (nx + 10, ny - 14)], fill=col, width=2)
            glow_draw.line([(nx - 10, ny - 5), (nx + 10, ny - 5)], fill=col, width=2)
            glow_draw.line([(nx - 10, ny + 4), (nx + 5, ny + 4)], fill=col, width=2)
        elif node["icon"] == "patch":
            # Chaves / brackets de código
            glow_draw.line([(nx - 14, ny - 20), (nx - 6, ny - 20), (nx - 6, ny + 8), (nx - 14, ny + 8)], fill=col, width=2)
            glow_draw.line([(nx + 14, ny - 20), (nx + 6, ny - 20), (nx + 6, ny + 8), (nx + 14, ny + 8)], fill=col, width=2)
            glow_draw.line([(nx - 2, ny - 6), (nx + 2, ny - 6)], fill=(255, 255, 255), width=2)
        elif node["icon"] == "terminal":
            # Prompt de comando >_
            glow_draw.line([(nx - 16, ny - 16), (nx - 4, ny - 6), (nx - 16, ny + 4)], fill=col, width=2)
            glow_draw.line([(nx, ny + 4), (nx + 14, ny + 4)], fill=(255, 255, 255), width=2)
            
        # Rótulo esquemático no rodapé do satélite
        glow_draw.rectangle([nx - 45, ny + 20, nx + 45, ny + 32], fill=(6, 10, 16), outline=col, width=1)
        glow_draw.line([(nx - 35, ny + 26), (nx + 35, ny + 26)], fill=col, width=2)

    # 6. FEIXE DE LUZ ASCENDENTE (CONSOLIDAÇÃO EM 1 TURNO & 95% MENOS TOKENS)
    # Feixe saindo do topo do terminal até o ápice do frontão
    glow_draw.polygon([
        (cx - 30, card_y1),
        (cx + 30, card_y1),
        (cx + 10, 120),
        (cx - 10, 120)
    ], fill=(223, 186, 107, 75))
    glow_draw.line([(cx, card_y1), (cx, 120)], fill=(255, 255, 255, 220), width=2)
    
    # Orbe / Cristal de Síntese no topo (1 Único Turno Consolidado)
    glow_draw.ellipse([cx - 24, 120 - 24, cx + 24, 120 + 24], fill=(223, 186, 107, 220), outline=(255, 255, 255), width=2)
    glow_draw.ellipse([cx - 10, 120 - 10, cx + 10, 120 + 10], fill=(255, 255, 255))
    
    # Badge Executivo Superior: "1 SINGLE TURN // -95% TOKENS"
    glow_draw.rectangle([cx - 130, 155, cx + 130, 185], fill=(12, 22, 34, 240), outline=(223, 186, 107), width=2)
    glow_draw.line([(cx - 110, 170), (cx + 110, 170)], fill=(0, 229, 255), width=2)

    # 7. COMPOSE E SALVA A IMAGEM
    final_img = Image.alpha_composite(im.convert("RGBA"), glow_layer).convert("RGB")
    
    # Salvar em D:\DevCod\inteligencia-agentica\static\images\code-execution-chamada-programatica-hermes.jpg
    out_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "code-execution-chamada-programatica-hermes.jpg")
    final_img.save(out_path, format="JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {out_path}")
    return out_path

if __name__ == "__main__":
    create_code_execution_cover()
