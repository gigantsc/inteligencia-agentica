# -*- coding: utf-8 -*-
"""
Traduz os 326 cases de uso do inglês para pt-BR via API OpenAI-compatible (OMI/9Router).
Processa em lotes de 10 para eficiência. Salva progresso incrementalmente.
"""
import json
import os
import time
import urllib.request

API_URL = os.environ.get("OMI_API_URL", "https://omi.jepierre.com.br/v1/chat/completions")
API_KEY = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
MODEL = "gpt-4o-mini"

INPUT_FILE = "D:/DevCod/inteligencia-agentica/use_cases_raw.json"
OUTPUT_FILE = "D:/DevCod/inteligencia-agentica/use_cases_translated.json"
PROGRESS_FILE = "D:/DevCod/inteligencia-agentica/translation_progress.json"

BATCH_SIZE = 5

SYSTEM_PROMPT = """Você é um tradutor profissional de conteúdo técnico de IA e automação.
Traduza os textos abaixo do inglês para português brasileiro (pt-BR) de forma:
- Natural e humanizada (como um brasileiro escreveria, não tradução literal)
- Mantenha termos técnicos consagrados inalterados: Docker, Telegram, GitHub, API, VPS, deploy, Next.js, PostgreSQL, Redis, WhatsApp, cron, CI/CD, PR, etc.
- Não traduza nomes de ferramentas, frameworks ou serviços
- Tom profissional mas acessível, sem ser robótico
- Nomes de pessoas e usernames ficam inalterados
- Remova citações de autor/data do final dos textos (ex: "— u/username, 2026-06-18, via Reddit.")

Retorne APENAS um array JSON válido com os objetos traduzidos, mantendo a mesma estrutura.
Cada objeto tem: id, title, summary, detail. Traduza title, summary e detail."""


def call_api(messages, retries=3):
    """Chama a API OMI com retry."""
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 4096,
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    for attempt in range(retries):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                # Limpa markdown code fences se presentes
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                return json.loads(content.strip())
        except Exception as e:
            print(f"  Tentativa {attempt+1}/{retries} falhou: {e}")
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
    return None


def load_progress():
    """Carrega progresso salvo anteriormente."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(translated_map):
    """Salva progresso incrementalmente."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_map, f, ensure_ascii=False)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_cases = json.load(f)

    print(f"Total de cases para traduzir: {len(raw_cases)}")

    # Carrega progresso anterior
    translated_map = load_progress()
    already_done = len(translated_map)
    print(f"Já traduzidos anteriormente: {already_done}")

    # Filtra os que faltam
    pending = [c for c in raw_cases if c["id"] not in translated_map]
    print(f"Pendentes: {len(pending)}")

    if not pending:
        print("Todos já traduzidos!")
    else:
        total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE
        for batch_idx in range(total_batches):
            start = batch_idx * BATCH_SIZE
            end = start + BATCH_SIZE
            batch = pending[start:end]

            # Prepara payload compacto para tradução
            batch_payload = []
            for c in batch:
                batch_payload.append({
                    "id": c["id"],
                    "title": c.get("title", ""),
                    "summary": c.get("summary", ""),
                    "detail": c.get("detail", c.get("summary", "")),
                })

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(batch_payload, ensure_ascii=False)},
            ]

            batch_num = batch_idx + 1
            print(f"\n[{batch_num}/{total_batches}] Traduzindo {len(batch)} cases (IDs: {[c['id'][:30] for c in batch]})...")

            result = call_api(messages)

            if result and isinstance(result, list):
                for item in result:
                    item_id = item.get("id")
                    if item_id:
                        translated_map[item_id] = {
                            "title": item.get("title", ""),
                            "summary": item.get("summary", ""),
                            "detail": item.get("detail", ""),
                        }
                save_progress(translated_map)
                print(f"  ✅ Batch {batch_num} OK — total traduzido: {len(translated_map)}")
            else:
                print(f"  ❌ Batch {batch_num} FALHOU — tentando individualmente...")
                # Fallback: tenta 1 a 1
                for c in batch:
                    single_payload = [{
                        "id": c["id"],
                        "title": c.get("title", ""),
                        "summary": c.get("summary", ""),
                        "detail": c.get("detail", c.get("summary", "")),
                    }]
                    single_msg = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": json.dumps(single_payload, ensure_ascii=False)},
                    ]
                    single_result = call_api(single_msg)
                    if single_result and isinstance(single_result, list) and len(single_result) > 0:
                        item = single_result[0]
                        translated_map[c["id"]] = {
                            "title": item.get("title", ""),
                            "summary": item.get("summary", ""),
                            "detail": item.get("detail", ""),
                        }
                        save_progress(translated_map)
                        print(f"    ✅ Individual OK: {c['id'][:40]}")
                    else:
                        print(f"    ❌ Individual FALHOU: {c['id'][:40]}")

            # Rate limiting suave
            time.sleep(0.5)

    # Monta arquivo final com todas as traduções aplicadas
    print(f"\nMontando arquivo final com {len(translated_map)} traduções...")
    final_cases = []
    for c in raw_cases:
        tr = translated_map.get(c["id"])
        if tr:
            c_copy = dict(c)
            c_copy["title"] = tr["title"] or c["title"]
            c_copy["summary"] = tr["summary"] or c.get("summary", "")
            c_copy["detail"] = tr["detail"] or c.get("detail", "")
            final_cases.append(c_copy)
        else:
            final_cases.append(c)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_cases, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo final salvo: {OUTPUT_FILE}")
    print(f"   Traduzidos: {len(translated_map)} / {len(raw_cases)}")


if __name__ == "__main__":
    main()
