import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_jarvis_voice_cover():
    width, height = 1200, 912
    
    # 1. Base image with deep obsidian background (#07070A)
    im = Image.new("RGB", (width, height), (7, 7, 10))
    draw = ImageDraw.Draw(im, "RGBA")
    
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Left Cyan ambient wash (Voice Input / Telegram / Audio Spectrum)
    for r in range(550, 0, -15):
        alpha = int(45 * (1 - r / 550))
        glow_draw.ellipse([ -140 - r, 160 - r, 400 + r, 700 + r ], fill=(0, 229, 255, alpha))
        
    # Right Amber-Gold ambient wash (Autonomous Execution / TTS Audio Synth / Intel)
    for r in range(550, 0, -15):
        alpha = int(45 * (1 - r / 550))
        glow_draw.ellipse([ 800 - r, 160 - r, 1340 + r, 700 + r ], fill=(223, 186, 107, alpha))
        
    # Cybernetic floor grid
    for y in range(660, height, 25):
        alpha = int(35 * ((y - 660) / (height - 660)))
        glow_draw.line([(0, y), (width, y)], fill=(0, 200, 240, alpha), width=1)
    for x in range(80, width, 75):
        glow_draw.line([(x, 660), (int(600 + (x - 600) * 1.7), height)], fill=(0, 200, 240, 18), width=1)
        
    # 2. Classical Architecture: Columns & Pediment
    # Left Column (Fluted Cyan Marble)
    col_left_x = 140
    col_w = 60
    for fl in range(6):
        fl_x = col_left_x + fl * 10
        glow_draw.line([(fl_x, 130), (fl_x, 790)], fill=(120, 220, 250, 55), width=2)
    glow_draw.rectangle([col_left_x - 15, 110, col_left_x + col_w + 15, 140], fill=(15, 40, 55, 190), outline=(0, 229, 255, 200), width=2)
    glow_draw.rectangle([col_left_x - 20, 770, col_left_x + col_w + 20, 810], fill=(15, 40, 55, 190), outline=(0, 229, 255, 200), width=2)

    # Right Column (Fluted Gold Marble)
    col_right_x = 1000
    for fl in range(6):
        fl_x = col_right_x + fl * 10
        glow_draw.line([(fl_x, 130), (fl_x, 790)], fill=(230, 200, 120, 55), width=2)
    glow_draw.rectangle([col_right_x - 15, 110, col_right_x + col_w + 15, 140], fill=(45, 38, 18, 190), outline=(223, 186, 107, 200), width=2)
    glow_draw.rectangle([col_right_x - 20, 770, col_right_x + col_w + 20, 810], fill=(45, 38, 18, 190), outline=(223, 186, 107, 200), width=2)

    # Top Pediment triangle
    glow_draw.polygon([(600, 70), (110, 130), (1090, 130)], outline=(180, 210, 230, 110), width=2)
    glow_draw.line([(110, 130), (1090, 130)], fill=(0, 229, 255, 140), width=2)

    # 3. Center Piece: Acoustic Hermes Holographic Core & Voice Waves
    center_x = 600
    center_y = 430

    # Large Concentric Acoustic Pulsing Rings (Sound Waves)
    for radius in [180, 240, 300, 360, 420]:
        alpha_ring = max(10, int(90 - radius * 0.18))
        glow_draw.ellipse([center_x - radius, center_y - radius * 0.75, center_x + radius, center_y + radius * 0.75], outline=(0, 229, 255, alpha_ring), width=2)
        glow_draw.ellipse([center_x - radius, center_y - radius * 0.75, center_x + radius, center_y + radius * 0.75], outline=(223, 186, 107, int(alpha_ring * 0.7)), width=1)

    # Central Sphere / Neural Voice Core
    for r in range(130, 0, -8):
        a = int(70 * (1 - r / 130))
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(0, 229, 255, a))
        
    glow_draw.ellipse([center_x - 70, center_y - 70, center_x + 70, center_y + 70], fill=(12, 22, 32, 240), outline=(0, 229, 255, 255), width=3)
    glow_draw.ellipse([center_x - 30, center_y - 30, center_x + 30, center_y + 30], fill=(223, 186, 107, 230), outline=(255, 255, 255, 255), width=2)

    # Audio Waveform Equalizer Bars (Left = Cyan STT Input, Right = Gold TTS Voice Output)
    # Left Audio Bars (Speech-to-Text Input Waveform)
    num_bars = 24
    for i in range(num_bars):
        bx = center_x - 90 - i * 14
        # Calculate dynamic harmonic wave height
        wave_h = int(25 + 65 * math.sin(i * 0.45) * math.cos(i * 0.2) + 30 * math.sin(i * 0.9))
        wave_h = max(12, min(140, abs(wave_h)))
        by_top = center_y - wave_h
        by_bot = center_y + wave_h
        
        col = (0, int(210 + 45 * math.sin(i * 0.3)), 255, 210)
        glow_draw.rectangle([bx - 4, by_top, bx + 4, by_bot], fill=col)
        # Peak dots
        glow_draw.ellipse([bx - 3, by_top - 8, bx + 3, by_top - 2], fill=(255, 255, 255, 240))
        glow_draw.ellipse([bx - 3, by_bot + 2, bx + 3, by_bot + 8], fill=(0, 229, 255, 200))

    # Right Audio Bars (Text-to-Speech Output Waveform)
    for i in range(num_bars):
        bx = center_x + 90 + i * 14
        wave_h = int(25 + 70 * math.sin(i * 0.5) * math.sin(i * 0.25) + 35 * math.cos(i * 0.8))
        wave_h = max(12, min(145, abs(wave_h)))
        by_top = center_y - wave_h
        by_bot = center_y + wave_h
        
        col = (223, int(170 + 40 * math.cos(i * 0.3)), 107, 210)
        glow_draw.rectangle([bx - 4, by_top, bx + 4, by_bot], fill=col)
        # Peak dots
        glow_draw.ellipse([bx - 3, by_top - 8, bx + 3, by_top - 2], fill=(255, 255, 255, 240))
        glow_draw.ellipse([bx - 3, by_bot + 2, bx + 3, by_bot + 8], fill=(223, 186, 107, 200))

    # 4. Laser Neural Branch Lines & Feature Callouts (Telegram / Whisper STT / Hermes Engine / ElevenLabs TTS)
    callouts = [
        # Left side: Voice Ingestion / Telegram Gateway
        ((center_x - 70, center_y - 20), (330, 250), (220, 250), "TELEGRAM AUDIO IN", (0, 229, 255)),
        ((center_x - 70, center_y), (310, 430), (200, 430), "WHISPER / STT FAST", (0, 229, 255)),
        ((center_x - 70, center_y + 20), (330, 610), (220, 610), "SOUL.md PERSONA", (0, 229, 255)),
        
        # Right side: Autonomous Tool Calling & Voice Response
        ((center_x + 70, center_y - 20), (870, 250), (980, 250), "HERMES TOOL CALL", (223, 186, 107)),
        ((center_x + 70, center_y), (890, 430), (1000, 430), "24/7 VPS EXECUTION", (223, 186, 107)),
        ((center_x + 70, center_y + 20), (870, 610), (980, 610), "TTS AUDIO VOICE OUT", (223, 186, 107)),
    ]

    for p_start, p_mid, p_end, label, color in callouts:
        glow_draw.line([p_start, p_mid], fill=(*color, 210), width=3)
        glow_draw.line([p_mid, p_end], fill=(*color, 230), width=3)
        
        # Micro node circles
        glow_draw.ellipse([p_mid[0] - 5, p_mid[1] - 5, p_mid[0] + 5, p_mid[1] + 5], fill=(255, 255, 255, 255))
        glow_draw.ellipse([p_end[0] - 7, p_end[1] - 7, p_end[0] + 7, p_end[1] + 7], fill=(*color, 255), outline=(255, 255, 255, 255), width=2)
        
        # HUD Tag box
        box_w, box_h = 160, 30
        bx = p_end[0] - box_w - 12 if p_end[0] < center_x else p_end[0] + 12
        by = p_end[1] - box_h // 2
        glow_draw.rectangle([bx, by, bx + box_w, by + box_h], fill=(10, 16, 24, 230), outline=(*color, 200), width=1)

    # 5. Floating HUD Badges & Structural Title Banners
    # Badge Top: "JARVIS CORPORATIVO • VOICE AGENT • TELEGRAM GATEWAY"
    glow_draw.rectangle([340, 160, 860, 200], fill=(8, 18, 28, 225), outline=(0, 229, 255, 220), width=1)
    
    # Badge Bottom: "AUTOMAÇÃO EXECUTIVA POR VOZ • HERMES AGENT 24/7"
    glow_draw.rectangle([330, 730, 870, 770], fill=(24, 18, 10, 230), outline=(223, 186, 107, 220), width=1)

    # Composite glow and base
    im.paste(glow_layer, (0, 0), glow_layer)
    
    # 6. Typography rendering
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("arialbd.ttf", 16)
        font_tag = ImageFont.truetype("arialbd.ttf", 12)
        font_badge = ImageFont.truetype("arialbd.ttf", 13)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    final_draw = ImageDraw.Draw(im)
    
    # Text on Top Badge
    final_draw.text((600, 180), "JARVIS CORPORATIVO • VOICE AGENT • TELEGRAM GATEWAY", fill=(0, 229, 255), font=font_badge, anchor="mm")
    
    # Text on Bottom Badge
    final_draw.text((600, 750), "AUTOMAÇÃO EXECUTIVA POR VOZ • HERMES AGENT 24/7", fill=(223, 186, 107), font=font_badge, anchor="mm")

    # Main Hero Title Text (Floating Center Upper & Lower)
    final_draw.text((600, 290), "AGENTE JARVIS POR VOZ", fill=(255, 255, 255), font=font_main, anchor="mm")
    final_draw.text((600, 335), "Controle Sua Empresa por Áudio no Telegram", fill=(0, 229, 255), font=font_sub, anchor="mm")

    # Text inside Branch Boxes
    for p_start, p_mid, p_end, label, color in callouts:
        box_w, box_h = 160, 30
        bx = p_end[0] - box_w - 12 if p_end[0] < center_x else p_end[0] + 12
        by = p_end[1] - box_h // 2
        tx = bx + box_w // 2
        ty = by + box_h // 2
        final_draw.text((tx, ty), label, fill=(240, 245, 250), font=font_tag, anchor="mm")

    # Output path
    static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
    os.makedirs(static_dir, exist_ok=True)
    filename = "jarvis-corporativo-telegram-agentes-ia-voz.jpg"
    target_path = os.path.join(static_dir, filename)
    
    im.save(target_path, "JPEG", quality=95)
    print(f"✅ Capa Jarvis Voice gerada com sucesso em: {target_path} (Tamanho: {im.size})")

if __name__ == "__main__":
    create_jarvis_voice_cover()
