import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_document_extraction_cover():
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
    # Coluna Esquerda (Mármore Ciano / OCR & Forensic Scanning)
    col1_x = 75
    col_w = 54
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 105), (fl_x, 770)], fill=(90, 215, 245, 65), width=2)
    glow_draw.rectangle([col1_x - 14, 85, col1_x + col_w + 14, 115], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    glow_draw.rectangle([col1_x - 16, 750, col1_x + col_w + 16, 785], fill=(12, 35, 52, 220), outline=(0, 229, 255, 220), width=2)
    
    # Coluna Direita (Mármore Dourado / Structured Ledger & SQLite Vault)
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
    
    # Inscrição clássica no frontão: DOCUMENT EXTRACTION // COVERAGE GUARDIAN
    glow_draw.rectangle([350, 92, 850, 112], fill=(8, 14, 22), outline=(0, 229, 255), width=1)
    glow_draw.line([(370, 102), (830, 102)], fill=(223, 186, 107), width=2)

    # 3. CENTRO: O CONSOLE CENTRAL E O BUSTO CLÁSSICO DE HERMES
    cx, cy = 600, 410

    # Campo de Força Elíptico / Aura Tecnológica
    for r in range(240, 30, -12):
        alpha = int(32 * (1 - r / 240))
        glow_draw.ellipse([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95], fill=(0, 229, 255, alpha))
        
    # Pedestal Clássico de Mármore
    ped_y = cy + 140
    glow_draw.rectangle([cx - 105, ped_y, cx + 105, ped_y + 45], fill=(18, 25, 36), outline=(180, 210, 230), width=2)
    glow_draw.rectangle([cx - 125, ped_y + 45, cx + 125, ped_y + 70], fill=(12, 16, 24), outline=(223, 186, 107), width=2)
    # Placa do Pedestal
    glow_draw.rectangle([cx - 85, ped_y + 14, cx + 85, ped_y + 34], fill=(8, 12, 18), outline=(0, 229, 255), width=1)
    glow_draw.line([(cx - 70, ped_y + 24), (cx + 70, ped_y + 24)], fill=(223, 186, 107), width=2)

    # Tronco Esculpido de Hermes com Toga Neoclássica
    b_head_y = cy - 35
    torso = [(cx - 90, b_head_y + 145), (cx - 55, b_head_y + 45), (cx + 55, b_head_y + 45), (cx + 90, b_head_y + 145), (cx, b_head_y + 160)]
    glow_draw.polygon(torso, fill=(18, 26, 38, 240), outline=(210, 225, 240, 220), width=2)
    for t_line in range(-40, 45, 18):
        glow_draw.line([(cx + t_line, b_head_y + 55), (cx + t_line + 25, b_head_y + 140)], fill=(90, 140, 180, 130), width=2)

    # Cabeça Esculpida em Mármore
    glow_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], fill=(228, 235, 245, 250), outline=(0, 229, 255, 220), width=2)

    # Elmo Alado de Hermes (Petasos)
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

    # 4. LADO ESQUERDO: AUDITORIA FORENSE DE PDF ESCANEADO & COVERAGE WARNING
    doc_cx, doc_cy = 280, 410
    
    # Terminal de Ingestão de Documentos (Moldura em Vidro e Ciano Neon)
    glow_draw.rectangle([doc_cx - 125, doc_cy - 195, doc_cx + 125, doc_cy + 195], fill=(10, 22, 34, 235), outline=(0, 229, 255, 240), width=2)
    
    # Header da Folha de Documento: CONTRACT AUDIT // read_file()
    glow_draw.rectangle([doc_cx - 125, doc_cy - 195, doc_cx + 125, doc_cy - 155], fill=(14, 38, 58, 220), outline=(0, 229, 255, 180), width=1)
    glow_draw.ellipse([doc_cx - 110, doc_cy - 178, doc_cx - 96, doc_cy - 164], fill=(0, 229, 255, 220)) # Status LED
    glow_draw.line([(doc_cx - 85, doc_cy - 171), (doc_cx + 30, doc_cy - 171)], fill=(220, 245, 255), width=2)
    glow_draw.rectangle([doc_cx + 45, doc_cy - 180, doc_cx + 115, doc_cy - 162], fill=(6, 18, 28), outline=(0, 229, 255), width=1)
    glow_draw.line([(doc_cx + 55, doc_cy - 171), (doc_cx + 105, doc_cy - 171)], fill=(0, 229, 255), width=2)
    
    # Folha de Contrato / Pergaminho Digital
    glow_draw.rectangle([doc_cx - 110, doc_cy - 145, doc_cx + 110, doc_cy + 130], fill=(15, 25, 38), outline=(90, 180, 220, 180), width=1)
    
    # Linhas de Texto do Contrato (Camada Vetorial)
    for row in range(5):
        y_pos = doc_cy - 130 + row * 22
        w_len = 190 - (row % 3) * 35
        glow_draw.line([(doc_cx - 95, y_pos), (doc_cx - 95 + w_len, y_pos)], fill=(180, 220, 245, 180), width=2)
        
    # Faixa do Coverage Warning System (Alerta de Página Escaneada / Sem Camada de Texto)
    glow_draw.rectangle([doc_cx - 105, doc_cy - 15, doc_cx + 105, doc_cy + 45], fill=(42, 28, 12, 230), outline=(223, 186, 107, 240), width=1)
    glow_draw.rectangle([doc_cx - 98, doc_cy - 8, doc_cx - 75, doc_cy + 12], fill=(223, 186, 107), outline=(255, 240, 180), width=1) # Ícone Alerta
    glow_draw.line([(doc_cx - 65, doc_cy + 2), (doc_cx + 90, doc_cy + 2)], fill=(255, 225, 140), width=2)
    glow_draw.line([(doc_cx - 65, doc_cy + 20), (doc_cx + 60, doc_cy + 20)], fill=(223, 186, 107), width=2)
    glow_draw.line([(doc_cx - 65, doc_cy + 34), (doc_cx + 30, doc_cy + 34)], fill=(180, 150, 90), width=1)

    # Área Inferior: Visão Multimodal Direcionada (pdftoppm + vision_analyze)
    glow_draw.rectangle([doc_cx - 105, doc_cy + 55, doc_cx + 105, doc_cy + 120], fill=(8, 18, 30), outline=(0, 229, 255, 200), width=1)
    # Retícula de Foco Óptico
    ret_cx, ret_cy = doc_cx - 50, doc_cy + 87
    glow_draw.ellipse([ret_cx - 22, ret_cy - 22, ret_cx + 22, ret_cy + 22], outline=(0, 229, 255), width=2)
    glow_draw.line([(ret_cx - 28, ret_cy), (ret_cx + 28, ret_cy)], fill=(0, 229, 255), width=1)
    glow_draw.line([(ret_cx, ret_cy - 28), (ret_cx, ret_cy + 28)], fill=(0, 229, 255), width=1)
    # Linhas de Texto Auditado
    glow_draw.line([(doc_cx - 15, doc_cy + 75), (doc_cx + 90, doc_cy + 75)], fill=(0, 229, 255), width=2)
    glow_draw.line([(doc_cx - 15, doc_cy + 92), (doc_cx + 70, doc_cy + 92)], fill=(220, 240, 255), width=2)
    glow_draw.line([(doc_cx - 15, doc_cy + 108), (doc_cx + 40, doc_cy + 108)], fill=(120, 200, 230), width=1)

    # Feixe Laser Horizontal de Escaneamento (Glowing Scanline)
    scan_y = doc_cy - 45
    glow_draw.line([(doc_cx - 120, scan_y), (doc_cx + 120, scan_y)], fill=(0, 229, 255, 240), width=3)
    glow_draw.line([(doc_cx - 120, scan_y - 2), (doc_cx + 120, scan_y - 2)], fill=(180, 255, 255, 180), width=1)
    glow_draw.line([(doc_cx - 120, scan_y + 2), (doc_cx + 120, scan_y + 2)], fill=(180, 255, 255, 180), width=1)

    # Badge de Rodapé: ZERO HALLUCINATION GUARANTEE
    glow_draw.rectangle([doc_cx - 95, doc_cy + 145, doc_cx + 95, doc_cy + 172], fill=(6, 16, 26), outline=(0, 229, 255), width=1)
    glow_draw.line([(doc_cx - 75, doc_cy + 158), (doc_cx + 75, doc_cy + 158)], fill=(0, 229, 255), width=2)

    # 5. LADO DIREITO: EXCEL ANALYTICS & BANCO SQLITE IMUTÁVEL (mode=ro)
    data_cx, data_cy = 920, 410
    
    # Terminal de Dados Estruturados (Moldura Dourada / Bronze Clássico)
    glow_draw.rectangle([data_cx - 125, data_cy - 195, data_cx + 125, data_cy + 195], fill=(26, 22, 14, 235), outline=(223, 186, 107, 240), width=2)
    
    # Header do Terminal: STRUCTURED DATA // STDLIB PARSER
    glow_draw.rectangle([data_cx - 125, data_cy - 195, data_cx + 125, data_cy - 155], fill=(42, 34, 18, 220), outline=(223, 186, 107, 180), width=1)
    for b in range(3):
        glow_draw.ellipse([data_cx - 110 + b * 16, data_cy - 178, data_cx - 98 + b * 16, data_cy - 166], fill=(223, 186, 107, 200))
    glow_draw.line([(data_cx - 45, data_cy - 171), (data_cx + 105, data_cy - 171)], fill=(223, 186, 107), width=2)

    # Bloco 1: Planilha Excel (.xlsx) com Células e Fórmulas
    glow_draw.rectangle([data_cx - 110, data_cy - 145, data_cx + 110, data_cy - 40], fill=(20, 16, 10), outline=(223, 186, 107, 180), width=1)
    # Cabeçalho da Grade da Planilha
    glow_draw.rectangle([data_cx - 110, data_cy - 145, data_cx + 110, data_cy - 120], fill=(45, 36, 18), outline=(223, 186, 107, 140), width=1)
    glow_draw.line([(data_cx - 40, data_cy - 145), (data_cx - 40, data_cy - 40)], fill=(223, 186, 107, 100), width=1)
    glow_draw.line([(data_cx + 35, data_cy - 145), (data_cx + 35, data_cy - 40)], fill=(223, 186, 107, 100), width=1)
    # Linhas de células
    for r in range(3):
        y_r = data_cy - 100 + r * 20
        glow_draw.line([(data_cx - 110, y_r), (data_cx + 110, y_r)], fill=(223, 186, 107, 80), width=1)
        glow_draw.line([(data_cx - 95, y_r - 10), (data_cx - 50, y_r - 10)], fill=(255, 240, 200), width=2)
        glow_draw.line([(data_cx - 25, y_r - 10), (data_cx + 20, y_r - 10)], fill=(223, 186, 107), width=2)
        glow_draw.line([(data_cx + 50, y_r - 10), (data_cx + 95, y_r - 10)], fill=(0, 229, 255), width=2)

    # Bloco 2: Banco de Dados SQLite (.db / .sqlite) em modo mode=ro&immutable=1
    glow_draw.rectangle([data_cx - 110, data_cy - 25, data_cx + 110, data_cy + 75], fill=(18, 14, 8), outline=(223, 186, 107, 180), width=1)
    
    # Ícone do Cilindro de Banco de Dados
    cyl_x, cyl_y = data_cx - 70, data_cy + 25
    glow_draw.ellipse([cyl_x - 22, cyl_y - 28, cyl_x + 22, cyl_y - 14], fill=(48, 38, 18), outline=(223, 186, 107), width=2)
    glow_draw.rectangle([cyl_x - 22, cyl_y - 21, cyl_x + 22, cyl_y + 15], fill=(32, 25, 12), outline=(223, 186, 107), width=1)
    glow_draw.ellipse([cyl_x - 22, cyl_y + 8, cyl_x + 22, cyl_y + 22], fill=(48, 38, 18), outline=(223, 186, 107), width=2)
    
    # Cadeado de Proteção Imutável (mode=ro)
    glow_draw.rectangle([cyl_x - 8, cyl_y - 4, cyl_x + 8, cyl_y + 10], fill=(223, 186, 107), outline=(255, 255, 255), width=1)
    glow_draw.arc([cyl_x - 6, cyl_y - 12, cyl_x + 6, cyl_y - 2], start=180, end=0, fill=(223, 186, 107), width=2)

    # Schema Text: CREATE TABLE & 5 Rows Sample Preview
    glow_draw.line([(data_cx - 35, data_cy - 10), (data_cx + 95, data_cy - 10)], fill=(223, 186, 107), width=2)
    glow_draw.line([(data_cx - 35, data_cy + 10), (data_cx + 75, data_cy + 10)], fill=(255, 235, 180), width=2)
    glow_draw.line([(data_cx - 35, data_cy + 30), (data_cx + 85, data_cy + 30)], fill=(0, 229, 255), width=2)
    glow_draw.line([(data_cx - 35, data_cy + 50), (data_cx + 50, data_cy + 50)], fill=(180, 150, 100), width=1)

    # Bloco 3: Trava de Conflitos Git & Limite 50MB
    glow_draw.rectangle([data_cx - 110, data_cy + 90, data_cx + 110, data_cy + 172], fill=(14, 10, 6), outline=(0, 229, 255, 180), width=1)
    glow_draw.line([(data_cx - 95, data_cy + 110), (data_cx + 95, data_cy + 110)], fill=(0, 229, 255), width=2)
    glow_draw.line([(data_cx - 95, data_cy + 130), (data_cx + 60, data_cy + 130)], fill=(223, 186, 107), width=2)
    glow_draw.rectangle([data_cx - 85, data_cy + 145, data_cx + 85, data_cy + 165], fill=(8, 16, 24), outline=(0, 229, 255), width=1)
    glow_draw.line([(data_cx - 65, data_cy + 155), (data_cx + 65, data_cy + 155)], fill=(0, 229, 255), width=2)

    # 6. FILAMENTOS NEURAIS DE SINAPSE E FLUXO DE DADOS
    for l in range(4):
        # Do terminal de contratos (esquerda) para Hermes (centro)
        glow_draw.line([(doc_cx + 125, doc_cy - 80 + l * 50), (cx - 90, cy - 20 + l * 25)], fill=(0, 229, 255, 180), width=2)
        # Do terminal de dados estruturados (direita) para Hermes (centro)
        glow_draw.line([(data_cx - 125, data_cy - 80 + l * 50), (cx + 90, cy - 20 + l * 25)], fill=(223, 186, 107, 180), width=2)
        
        # Pulsos de Dados (Data Packets)
        p1_x = doc_cx + 125 + int((cx - 90 - (doc_cx + 125)) * 0.5)
        p1_y = doc_cy - 80 + l * 50 + int((cy - 20 + l * 25 - (doc_cy - 80 + l * 50)) * 0.5)
        glow_draw.ellipse([p1_x - 5, p1_y - 5, p1_x + 5, p1_y + 5], fill=(0, 229, 255, 240), outline=(255, 255, 255), width=1)

        p2_x = data_cx - 125 + int((cx + 90 - (data_cx - 125)) * 0.5)
        p2_y = data_cy - 80 + l * 50 + int((cy - 20 + l * 25 - (data_cy - 80 + l * 50)) * 0.5)
        glow_draw.ellipse([p2_x - 5, p2_y - 5, p2_x + 5, p2_y + 5], fill=(223, 186, 107, 240), outline=(255, 255, 255), width=1)

    # 7. TRILHAS FIBRA ÓPTICA INFERIOR
    for f in range(5):
        glow_draw.line([(150, 680 + f * 40), (cx - 120, 680 + f * 40)], fill=(0, 229, 255, 80), width=1)
        glow_draw.line([(cx + 120, 680 + f * 40), (1050, 680 + f * 40)], fill=(223, 186, 107, 80), width=1)

    # 8. RENDERIZAÇÃO FINAL COM BLUR CINEMATOGRÁFICO
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=1.8))
    final_im = Image.alpha_composite(im.convert("RGBA"), blurred_glow)
    
    # Sharp overlay layer for crisp edges
    final_draw = ImageDraw.Draw(final_im)
    final_draw.rectangle([doc_cx - 125, doc_cy - 195, doc_cx + 125, doc_cy + 195], outline=(0, 229, 255, 240), width=2)
    final_draw.rectangle([data_cx - 125, data_cy - 195, data_cx + 125, data_cy + 195], outline=(223, 186, 107, 240), width=2)
    final_draw.ellipse([cx - 40, b_head_y - 45, cx + 40, b_head_y + 40], outline=(0, 229, 255, 220), width=2)
    
    # Salvar imagem
    output_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "document-extraction-ingestao-pdf-excel-sqlite.jpg")
    
    final_im.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem de capa gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    create_document_extraction_cover()
