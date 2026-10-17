import urllib.request
import urllib.error
import json
import os
import uuid
import time
from datetime import datetime, timezone

api_key = "08d2296b12712bb58fb1d5a84066545a5f9f180242937b5a1ea7753ba1a040a8"
base_url = "https://multip.jepierre.com.br/api/public/v1"
img_path = r"D:\DevCod\inteligencia-agentica\static\images\como-economizar-tokens-hermes-agent-guia-pratico.jpg"

copy_content = """💰 Onde Seus Tokens Estão Indo de Verdade: Como Encontrar o Desperdício no Hermes Agent e Economizar até 90%!

A maioria das pessoas só percebe o desperdício de tokens quando a barra de contexto enche ou quando a fatura da API chega no fim do mês.

O grande erro é tentar resolver adivinhando. No ecossistema agêntico da Nous Research, a regra de ouro é:
👉 Medir ➔ Localizar a camada pesada ➔ Ajustar a camada ➔ Medir novamente.

Reunimos as melhores práticas oficiais para blindar seu orçamento:

1️⃣ Audite a Mochila Inicial: Use hermes prompt-size para descobrir se seu robô já nasce pesado com ferramentas ou instruções que ele nunca usa.
2️⃣ Diagnóstico em Tempo Real: Digite /context all para ver a divisão exata de peso e /usage para checar o custo em dólares.
3️⃣ Isole Tarefas Laterais: Use /btw para dúvidas rápidas sem quebrar o cache de prompt e sem poluir o histórico.
4️⃣ Roteamento Inteligente: Atribua modelos ultrabaratos para tarefas auxiliares (resumo, visão e compressão) e reserve o modelo forte apenas para o raciocínio complexo.

Confira o guia prático completo no nosso blog:
🔗 https://inteligenciaagentica.com.br/blog/como-economizar-tokens-hermes-agent-guia-pratico

#HermesAgent #InteligenciaAgentica #EconomiaDeTokens #CustosIA #Otimizacao #Produtividade #Negocios #PromptCaching"""

def run_publish():
    print("Iniciando tentativa de upload e publicacao no MultiPost...")
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="como-economizar-tokens-hermes-agent-guia-pratico.jpg"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + img_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req_upload = urllib.request.Request(
        f"{base_url}/upload",
        data=body,
        headers={
            "Authorization": api_key,
            "User-Agent": "Postiz-Agent/1.0",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
    )

    with urllib.request.urlopen(req_upload, timeout=20) as resp:
        upload_res = json.loads(resp.read().decode("utf-8"))
        media_id = upload_res.get("id")
        media_path = upload_res.get("path")
        print(f"Media Uploaded: id={media_id}")

    integrations = [
        {"id": "cmp717k9k0001qjp4poohdhcl", "type": "instagram", "post_type": "post"},
        {"id": "cmp76nv4v0009qjp4sv9t8gj9", "type": "facebook", "post_type": "post"},
        {"id": "cmp78kj2f0001ry91ym9g1qse", "type": "threads", "post_type": "post"},
        {"id": "cmp7evz040005ry91qmrzisd1", "type": "linkedin", "post_type": "post"}
    ]

    posts_payload = []
    for inte in integrations:
        posts_payload.append({
            "integration": {"id": inte["id"]},
            "value": [
                {
                    "content": copy_content,
                    "image": [{"id": media_id, "path": media_path}]
                }
            ],
            "settings": {
                "__type": inte["type"],
                "post_type": inte["post_type"]
            }
        })

    create_payload = {
        "type": "now",
        "date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "shortLink": False,
        "tags": [],
        "posts": posts_payload
    }

    req_post = urllib.request.Request(
        f"{base_url}/posts",
        data=json.dumps(create_payload).encode("utf-8"),
        headers={
            "Authorization": api_key,
            "User-Agent": "Postiz-Agent/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(req_post, timeout=20) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("✅ MultiPost Publicado com Sucesso:", json.dumps(res, indent=2))

if __name__ == "__main__":
    try:
        run_publish()
    except Exception as e:
        print("Erro durante execucao:", e)
