import os
import sys
import json
import base64
import urllib.request
import urllib.error

def get_gemini_key():
    # 1. Direct env vars
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key

    # 2. Check auth.json files
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    search_dirs = [
        os.path.expanduser("~/.hermes"),
        os.path.join(local_app_data, "hermes"),
    ]
    
    # Add profile dirs
    profiles_root = os.path.join(local_app_data, "hermes", "profiles")
    if os.path.exists(profiles_root):
        for p in os.listdir(profiles_root):
            p_dir = os.path.join(profiles_root, p)
            if os.path.isdir(p_dir):
                search_dirs.append(p_dir)
                
    for s_dir in search_dirs:
        # auth.json
        auth_file = os.path.join(s_dir, "auth.json")
        if os.path.exists(auth_file):
            try:
                with open(auth_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if "gemini" in k.lower() or "google" in k.lower():
                                if isinstance(v, str) and len(v) > 10:
                                    return v
                                elif isinstance(v, dict) and "api_key" in v:
                                    return v["api_key"]
                                elif isinstance(v, dict) and "token" in v:
                                    return v["token"]
            except Exception:
                pass
                
        # .env
        env_file = os.path.join(s_dir, ".env")
        if os.path.exists(env_file):
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY=") or line.startswith("GOOGLE_API_KEY="):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val:
                                return val
            except Exception:
                pass
                
    return None

def generate_jev_cover():
    api_key = get_gemini_key()
    if not api_key:
        print("❌ Chave GEMINI_API_KEY / GOOGLE_API_KEY não encontrada nos arquivos de configuração.")
        return False
        
    print("🎨 Gerando imagem de capa contextual para Jev (TypeSafe) com Gemini Imagen 3...")
    
    # Prompt: Hermes Cyber-Classicism for Fast Structured Decisions (System 1 / Lightning routing)
    prompt = (
        "High-end duotone artistic composition in the iconic Hermes Agent / Nous Research aesthetic. "
        "A magnificent classical Greco-Roman marble statue bust of Hermes surrounded by ultra-fast optical switching matrices, "
        "luminous decision nodes, binary decision bifurcations (Yes/No, 0/1), and glowing branching crystalline fiber optics. "
        "Dynamic high-speed particle streams and glowing laser pathways representing instant zero-latency routing. "
        "Dramatic chiaroscuro studio lighting, extreme contrast duochromatic color grading with deep obsidian black (#07070A), "
        "vibrant electric neon cyan (#00E5FF) highlights on the left and luminous warm amber-gold highlights (#DFBA6B) on the right. "
        "Fine sculpted marble texture, digital decision matrix aura, architectural depth, clean dark background, 16:9 cinematic aspect ratio, "
        "ultra-detailed 8k masterpiece, neoclassical cyberpunk synthwave elegance, no cheap 3D renders, pure museum-grade digital art."
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
            
            static_dir = r"D:\DevCod\inteligencia-agentica\static\images"
            os.makedirs(static_dir, exist_ok=True)
            
            filename = "jev-typesafe-ia-de-decisao-rapida-hermes.jpg"
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
    success = generate_jev_cover()
    if not success:
        sys.exit(1)
