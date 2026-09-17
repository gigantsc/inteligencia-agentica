import os
import sys
import json
import base64
import urllib.request
import urllib.error

def generate_hermes_image(api_key: str):
    print("🎨 Iniciando geração da imagem duocromática estilo Hermes Greco-Romano com Gemini/Imagen 3...")
    
    prompt = (
        "High-end duotone artistic composition in the iconic Hermes Agent / Nous Research aesthetic. "
        "A magnificent classical Greco-Roman marble statue bust of Hermes with subtly detailed winged helmet, "
        "fused with subtle futuristic cybernetic details and glowing fiber-optic circuit traces. "
        "Dramatic chiaroscuro studio lighting, extreme contrast duochromatic color grading with deep obsidian black "
        "and vibrant electric neon cyan (#00E5FF) and luminous amber-gold highlights (#DFBA6B). "
        "Fine sculpted marble texture, digital data aura, clean minimalist background, 16:9 cinematic aspect ratio, "
        "ultra-detailed 8k masterpiece, neoclassical cyberpunk synthwave elegance, no cheesy 3D renders, pure high art."
    )
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
    
    payload = {
        "instances": [
            {"prompt": prompt}
        ],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "outputMimeType": "image/jpeg"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            predictions = data.get("predictions", [])
            if not predictions:
                print("❌ Nenhuma imagem retornada na resposta da API.")
                return False
            
            b64_data = predictions[0].get("bytesBase64Encoded")
            img_bytes = base64.b64decode(b64_data)
            
            # Save into blog static/images
            static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
            os.makedirs(static_dir, exist_ok=True)
            
            filename = "ia-na-nuvem-vps-vs-chatbot-hermes.jpg"
            file_path = os.path.join(static_dir, filename)
            
            with open(file_path, "wb") as f:
                f.write(img_bytes)
            
            print(f"✅ Imagem gerada com sucesso e salva em: {file_path}")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        key = os.environ.get("GEMINI_API_KEY", "")
        
    if not key:
        print("❌ Informe a chave da API Gemini: python generate_cover_gemini.py SUA_CHAVE_AQUI")
        sys.exit(1)
        
    success = generate_hermes_image(key)
    if not success:
        sys.exit(1)
