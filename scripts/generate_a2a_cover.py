import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_a2a_cover():
    width, height = 1200, 912
    
    # 1. Imagem base com fundo obsidiana profunda (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Agente Cliente / Hermes Desktop / Descoberta A2A #00E5FF)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([-140 - r, 200 - r, 420 + r, 720 + r], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Agente Servidor / VPS Nuvem / Parceiro B2B #DFBA6B)
    for r in range(580, 0, -12):
        alpha = int(48 * (1 - r / 580))
        glow_draw.ellipse([780 - r, 200 - r, 1340 + r, 720 + r], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid (grade de perspectiva digital)
    for y in range(670, height, 20):
        alpha = int(35 * ((y - 670) / (height - 670)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 210, 245, alpha), width=1)
    for x in range(60, width, 60):
        glow_draw.line([(x, 670), (int(600 + (x - 600) * 1.65), height)], fill=(0, 210, 245, 18), width=1)
        
    # 2. PÓRTICO CLÁSSICO GRECO-ROMANO (Colunas de Mármore com Conduítes Digitais)
    # Coluna Externa Esquerda (Ciano)
    col1_x = 75
    col_w = 50
    for fl in range(6):
        fl_x = col1_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(90, 215, 245, 60), width=2)
    glow_draw.rectangle([col1_x - 14, 90, col1_x + col_w + 14, 120], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    glow_draw.rectangle([col1_x - 16, 740, col1_x + col_w + 16, 775], fill=(12, 35, 50, 210), outline=(0, 229, 255, 210), width=2)
    
    # Coluna Externa Direita (Ouro)
    col2_x = 1075
    for fl in range(6):
        fl_x = col2_x + fl * 9
        glow_draw.line([(fl_x, 110), (fl_x, 760)], fill=(215, 190, 115, 60), width=2)
    glow_draw.rectangle([col2_x - 14, 90, col2_x + col_w + 14, 120], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)
    glow_draw.rectangle([col2_x - 16, 740, col2_x + col_w + 16, 775], fill=(42, 36, 16, 210), outline=(223, 186, 107, 210), width=2)

    # Frontão Clássico Superior com Inscrição
    glow_draw.polygon([(600, 35), (60, 105), (1140, 105)], outline=(170, 205, 225, 110), width=2)
    glow_draw.polygon([(600, 50), (90, 105), (1110, 105)], outline=(210, 185, 115, 90), width=1)
    glow_draw.rectangle([60, 105, 1140, 120], fill=(15, 18, 24, 170), outline=(160, 195, 215, 100), width=1)
    
    # 3. DOIS BUSTOS CLÁSSICOS DE AGENTES EM PEDESTAIS (CLIENTE vs SERVIDOR)
    # BUSTO ESQUERDO: Agente Cliente / Empresa A (Ciano #00E5FF)
    b1_cx, b1_cy = 310, 390
    b1_head_y = b1_cy - 60
    
    # Pedestal Esquerdo
    glow_draw.rectangle([b1_cx - 75, b1_head_y + 190, b1_cx + 75, b1_head_y + 245], fill=(12, 30, 45, 230), outline=(0, 229, 255, 180), width=2)
    glow_draw.rectangle([b1_cx - 95, b1_head_y + 245, b1_cx + 95, b1_head_y + 270], fill=(8, 22, 34, 240), outline=(0, 229, 255, 200), width=2)
    # Rótulo digital no pedestal esquerdo
    glow_draw.rectangle([b1_cx - 50, b1_head_y + 205, b1_cx + 50, b1_head_y + 230], fill=(15, 45, 65, 220), outline=(0, 229, 255, 255), width=1)
    glow_draw.line([(b1_cx - 35, b1_head_y + 217), (b1_cx + 35, b1_head_y + 217)], fill=(200, 245, 255, 230), width=2)
    
    # Tronco e Cabeça Esquerda
    b1_torso = [(b1_cx - 85, b1_head_y + 160), (b1_cx - 50, b1_head_y + 40), (b1_cx + 50, b1_head_y + 40), (b1_cx + 85, b1_head_y + 160), (b1_cx, b1_head_y + 185)]
    glow_draw.polygon(b1_torso, fill=(14, 28, 42, 240), outline=(0, 229, 255, 210), width=2)
    glow_draw.ellipse([b1_cx - 38, b1_head_y - 48, b1_cx + 38, b1_head_y + 38], fill=(16, 32, 48, 245), outline=(0, 229, 255, 230), width=2)
    # Elmo Alado de Hermes
    w_l1 = [(b1_cx - 30, b1_head_y - 40), (b1_cx - 95, b1_head_y - 100), (b1_cx - 65, b1_head_y - 45), (b1_cx - 85, b1_head_y - 25), (b1_cx - 32, b1_head_y - 18)]
    glow_draw.polygon(w_l1, fill=(10, 45, 65, 230), outline=(0, 229, 255, 255), width=2)
    
    # BUSTO DIREITO: Agente Servidor / Parceiro B2B (Ouro #DFBA6B)
    b2_cx, b2_cy = 890, 390
    b2_head_y = b2_cy - 60
    
    # Pedestal Direito
    glow_draw.rectangle([b2_cx - 75, b2_head_y + 190, b2_cx + 75, b2_head_y + 245], fill=(38, 30, 12, 230), outline=(223, 186, 107, 180), width=2)
    glow_draw.rectangle([b2_cx - 95, b2_head_y + 245, b2_cx + 95, b2_head_y + 270], fill=(26, 20, 8, 240), outline=(223, 186, 107, 200), width=2)
    # Rótulo digital no pedestal direito
    glow_draw.rectangle([b2_cx - 50, b2_head_y + 205, b2_cx + 50, b2_head_y + 230], fill=(55, 42, 16, 220), outline=(223, 186, 107, 255), width=1)
    glow_draw.line([(b2_cx - 35, b2_head_y + 217), (b2_cx + 35, b2_head_y + 217)], fill=(255, 240, 190, 230), width=2)
    
    # Tronco e Cabeça Direita
    b2_torso = [(b2_cx - 85, b2_head_y + 160), (b2_cx - 50, b2_head_y + 40), (b2_cx + 50, b2_head_y + 40), (b2_cx + 85, b2_head_y + 160), (b2_cx, b2_head_y + 185)]
    glow_draw.polygon(b2_torso, fill=(35, 28, 12, 240), outline=(223, 186, 107, 210), width=2)
    glow_draw.ellipse([b2_cx - 38, b2_head_y - 48, b2_cx + 38, b2_head_y + 38], fill=(42, 34, 15, 245), outline=(223, 186, 107, 230), width=2)
    # Elmo Alado de Hermes Direito
    w_r2 = [(b2_cx + 30, b2_head_y - 40), (b2_cx + 95, b2_head_y - 100), (b2_cx + 65, b2_head_y - 45), (b2_cx + 85, b2_head_y - 25), (b2_cx + 32, b2_head_y - 18)]
    glow_draw.polygon(w_r2, fill=(60, 48, 18, 230), outline=(223, 186, 107, 255), width=2)
    
    # 4. NÚCLEO CENTRAL: PONTE A2A E HOLOGRAMA DO AGENT CARD (.well-known/agent-card.json)
    card_cx, card_cy = 600, 360
    card_w, card_h = 240, 280
    
    # Halo circular atrás do Agent Card
    for r in range(160, 20, -10):
        glow_draw.ellipse([card_cx - r, card_cy - r, card_cx + r, card_cy + r], fill=(12, 16, 24, 120), outline=(120, 210, 240, int(60 * (1 - r/160))), width=1)
        
    # Moldura holográfica do Agent Card
    glow_draw.rounded_rectangle([card_cx - card_w//2, card_cy - card_h//2, card_cx + card_w//2, card_cy + card_h//2], radius=14, fill=(10, 14, 20, 240), outline=(180, 210, 235, 220), width=2)
    # Borda bipartida ciano/ouro
    glow_draw.line([(card_cx - card_w//2, card_cy - card_h//2), (card_cx - card_w//2, card_cy + card_h//2)], fill=(0, 229, 255, 255), width=3)
    glow_draw.line([(card_cx + card_w//2, card_cy - card_h//2), (card_cx + card_w//2, card_cy + card_h//2)], fill=(223, 186, 107, 255), width=3)
    
    # Topo do Card (Header / Endpoint)
    glow_draw.rectangle([card_cx - card_w//2, card_cy - card_h//2, card_cx + card_w//2, card_cy - card_h//2 + 35], fill=(18, 26, 38, 245), outline=(140, 180, 220, 200), width=1)
    # 3 botões estilo interface
    glow_draw.ellipse([card_cx - card_w//2 + 12, card_cy - card_h//2 + 12, card_cx - card_w//2 + 22, card_cy - card_h//2 + 22], fill=(0, 229, 255, 220))
    glow_draw.ellipse([card_cx - card_w//2 + 28, card_cy - card_h//2 + 12, card_cx - card_w//2 + 38, card_cy - card_h//2 + 22], fill=(223, 186, 107, 220))
    glow_draw.ellipse([card_cx - card_w//2 + 44, card_cy - card_h//2 + 12, card_cx - card_w//2 + 54, card_cy - card_h//2 + 22], fill=(160, 190, 215, 220))
    # Título do Card
    glow_draw.line([(card_cx - 30, card_cy - card_h//2 + 17), (card_cx + 85, card_cy - card_h//2 + 17)], fill=(220, 240, 255, 230), width=2)
    
    # Linhas de código JSON / Capabilities do Agent Card
    for li, ly in enumerate(range(card_cy - card_h//2 + 55, card_cy + card_h//2 - 40, 26)):
        # Chave JSON (Ciano)
        glow_draw.line([(card_cx - card_w//2 + 20, ly), (card_cx - card_w//2 + 65, ly)], fill=(0, 229, 255, 210), width=2)
        # Separador ":"
        glow_draw.ellipse([card_cx - card_w//2 + 75, ly - 2, card_cx - card_w//2 + 79, ly + 2], fill=(255, 255, 255, 200))
        # Valor JSON (Ouro)
        v_len = 80 if li % 2 == 0 else 50
        glow_draw.line([(card_cx - card_w//2 + 90, ly), (card_cx - card_w//2 + 90 + v_len, ly)], fill=(223, 186, 107, 210), width=2)
        # Checkmark de capacidade ativa
        chk_x = card_cx + card_w//2 - 25
        glow_draw.line([(chk_x - 5, ly), (chk_x - 2, ly + 4), (chk_x + 5, ly - 4)], fill=(0, 255, 200, 230), width=2)
        
    # Selo Canônico A2A Protocol no rodapé do Card
    glow_draw.rectangle([card_cx - 70, card_cy + card_h//2 - 30, card_cx + 70, card_cy + card_h//2 - 10], fill=(22, 32, 46, 240), outline=(180, 210, 240, 210), width=1)
    glow_draw.line([(card_cx - 45, card_cy + card_h//2 - 20), (card_cx + 45, card_cy + card_h//2 - 20)], fill=(0, 229, 255, 230), width=2)
    
    # 5. FEIXES NEURAIS & TRANSMISSÃO BIDIRECIONAL DE DADOS (JSON-RPC 2.0 & SSE STREAMING)
    # Feixe Ciano saindo do Agente Cliente até o Agent Card
    for offset_y in [-15, 0, 15]:
        glow_draw.line([(b1_cx + 50, b1_head_y + 90 + offset_y), (card_cx - card_w//2, card_cy + offset_y)], fill=(0, 229, 255, 190 - abs(offset_y)*4), width=2)
        
    # Feixe Ouro saindo do Agente Servidor até o Agent Card
    for offset_y in [-15, 0, 15]:
        glow_draw.line([(b2_cx - 50, b2_head_y + 90 + offset_y), (card_cx + card_w//2, card_cy + offset_y)], fill=(223, 186, 107, 190 - abs(offset_y)*4), width=2)
        
    # Cubos de Dados Holográficos Flutuantes no Fluxo (JSON-RPC payloads)
    # Pacote 1 (Ciano, indo para a direita)
    p1_x, p1_y = 440, 320
    glow_draw.rectangle([p1_x - 14, p1_y - 14, p1_x + 14, p1_y + 14], fill=(10, 45, 65, 220), outline=(0, 229, 255, 255), width=2)
    glow_draw.line([(p1_x - 8, p1_y), (p1_x + 8, p1_y)], fill=(255, 255, 255, 230), width=2)
    # Seta direcional indicando a2a_call
    glow_draw.polygon([(p1_x + 22, p1_y), (p1_x + 15, p1_y - 6), (p1_x + 15, p1_y + 6)], fill=(0, 229, 255, 255))
    
    # Pacote 2 (Ouro, retornando para a esquerda - resposta SSE)
    p2_x, p2_y = 760, 400
    glow_draw.rectangle([p2_x - 14, p2_y - 14, p2_x + 14, p2_y + 14], fill=(50, 40, 15, 220), outline=(223, 186, 107, 255), width=2)
    glow_draw.line([(p2_x - 8, p2_y), (p2_x + 8, p2_y)], fill=(255, 245, 200, 230), width=2)
    # Seta direcional indicando resposta
    glow_draw.polygon([(p2_x - 22, p2_y), (p2_x - 15, p2_y - 6), (p2_x - 15, p2_y + 6)], fill=(223, 186, 107, 255))

    # 6. SÍMBOLOS DE GOVERNANÇA: ESCUDO DO BUNKER & ANTI-LOOP (PING-PONG CAP)
    # Escudo de Autenticação Bearer (Ciano / Inferior Esquerdo)
    sh1_cx, sh1_cy = 200, 520
    sh_pts1 = [(sh1_cx - 30, sh1_cy - 35), (sh1_cx + 30, sh1_cy - 35), (sh1_cx + 30, sh1_cy + 5), (sh1_cx, sh1_cy + 35), (sh1_cx - 30, sh1_cy + 5)]
    glow_draw.polygon(sh_pts1, fill=(12, 35, 50, 220), outline=(0, 229, 255, 240), width=2)
    glow_draw.rectangle([sh1_cx - 10, sh1_cy - 5, sh1_cx + 10, sh1_cy + 15], fill=(8, 24, 36, 230), outline=(0, 229, 255, 255), width=1)
    glow_draw.arc([sh1_cx - 7, sh1_cy - 16, sh1_cx + 7, sh1_cy - 3], start=180, end=0, fill=(0, 229, 255, 255), width=2)
    
    # Trava Anti-Loop / Símbolo de Limite Infinito Bloqueado (Ouro / Inferior Direito)
    sh2_cx, sh2_cy = 1000, 520
    sh_pts2 = [(sh2_cx - 30, sh2_cy - 35), (sh2_cx + 30, sh2_cy - 35), (sh2_cx + 30, sh2_cy + 5), (sh2_cx, sh2_cy + 35), (sh2_cx - 30, sh2_cy + 5)]
    glow_draw.polygon(sh_pts2, fill=(45, 36, 16, 220), outline=(223, 186, 107, 240), width=2)
    # Símbolo do Infinito cortado (Anti-Loop Ping-Pong Cap)
    glow_draw.ellipse([sh2_cx - 18, sh2_cy - 8, sh2_cx - 2, sh2_cy + 8], outline=(223, 186, 107, 255), width=2)
    glow_draw.ellipse([sh2_cx + 2, sh2_cy - 8, sh2_cx + 18, sh2_cy + 8], outline=(223, 186, 107, 255), width=2)
    glow_draw.line([(sh2_cx - 16, sh2_cy + 14), (sh2_cx + 16, sh2_cy - 14)], fill=(255, 100, 100, 230), width=2)

    # 7. PARTÍCULAS E POEIRA DIGITAL DUOCROMÁTICA
    for i in range(160):
        seed_x = (i * 137 + 53) % width
        seed_y = (i * 211 + 67) % (height - 200) + 90
        p_color = (0, 229, 255) if seed_x < 600 else (223, 186, 107)
        p_size = (i % 3) + 1
        p_alpha = 75 + (i % 120)
        glow_draw.ellipse([seed_x, seed_y, seed_x + p_size, seed_y + p_size], fill=(*p_color, p_alpha))

    # 8. MISTURA E COMPOSIÇÃO FINAL
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))
    im.paste(blurred_glow, (0, 0), blurred_glow)
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # Salvar imagem
    output_path = r"D:\DevCod\inteligencia-agentica\static\images\protocolo-a2a-comunicacao-agente-a-agente-b2b.jpg"
    im.save(output_path, "JPEG", quality=95)
    print(f"✅ Imagem gerada com sucesso e salva em: {output_path}")

if __name__ == "__main__":
    create_a2a_cover()
