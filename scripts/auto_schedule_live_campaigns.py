#!/usr/bin/env python3
"""
auto_schedule_live_campaigns.py
Garante que todas as quintas-feiras tenham as 3 campanhas da Live agendadas no Listmonk:
1. Lembrete 30 minutos antes (19:00 BRT)
2. Lembrete 15 minutos antes (19:15 BRT)
3. No Ar (19:30 BRT)
"""

import sys
import datetime
import zoneinfo
import requests

BASE_URL = "https://email.inteligenciaagentica.com.br/api"
COOKIES = {"session": "ia_permanent_system_token_2026"}
LIST_ID = 3  # Inteligência Agêntica - Hermes Agente
TZ = zoneinfo.ZoneInfo("America/Sao_Paulo")

HTML_30MIN = """<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6;">
  <div style="text-align: center; margin-bottom: 24px;">
    <span style="display: inline-block; background-color: #0284c7; color: #ffffff; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; padding: 6px 16px; border-radius: 9999px; box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);">
      ⏳ COMEÇA EM 30 MINUTOS • 19:30H
    </span>
    <h1 style="color: #0f172a; font-size: 22px; font-weight: 800; margin-top: 14px; margin-bottom: 6px;">
      Faltam 30 Minutos para o Encontro ao Vivo!
    </h1>
    <p style="color: #64748b; font-size: 14px; margin: 0;">
      Separe seu bloco de notas e garanta seu lugar na sala.
    </p>
  </div>

  <p style="font-size: 15px;">Olá, <strong>{{ if .Subscriber.FirstName }}{{ .Subscriber.FirstName }}{{ else }}{{ .Subscriber.Name }}{{ end }}</strong>!</p>

  <p style="font-size: 15px;">
    Passando para te lembrar que em exatamente <strong>30 minutos</strong> (às 19:30h de Brasília) iniciaremos nosso <strong>Encontro Semanal ao Vivo da Inteligência Agêntica</strong>.
  </p>

  <!-- Botão de Acesso Principal ao Google Meet -->
  <div style="text-align: center; margin: 30px 0;">
    <a href="https://meet.google.com/cwh-omwb-ezs" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #DFBA6B 0%, #C4973B 100%); color: #07070A !important; text-decoration: none !important; font-weight: 800; font-size: 16px; padding: 18px 38px; border-radius: 12px; box-shadow: 0 4px 16px rgba(223, 186, 107, 0.4); text-transform: uppercase; letter-spacing: 0.05em;">
      👉 ACESSAR SALA NO GOOGLE MEET
    </a>
    <p style="font-size: 13px; color: #64748b; margin-top: 12px;">
      Link fixo da transmissão:<br>
      <a href="https://meet.google.com/cwh-omwb-ezs" style="color: #0284c7; font-weight: 700; word-break: break-all;">https://meet.google.com/cwh-omwb-ezs</a>
    </p>
  </div>

  <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #00E5FF; border-radius: 8px; padding: 18px 20px; margin: 24px 0;">
    <h3 style="margin-top: 0; margin-bottom: 12px; font-size: 15px; font-weight: 700; color: #0f172a;">
      📌 Na aula de hoje você vai ver:
    </h3>
    <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #334155; line-height: 1.8;">
      <li>Como configurar e orquestrar equipes de agentes de IA na prática.</li>
      <li>VPS em produção, Docker Swarm e conexão segura com Cloudflare Tunnels.</li>
      <li>Sessão aberta de tira-dúvidas técnicas e análise de arquitetura ao vivo.</li>
    </ul>
  </div>

  <p style="font-size: 15px;">
    Já deixe a aba do Google Meet aberta. Te vejo às 19:30h!
  </p>

  <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
    <p style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">Jean Pierre Schramm</p>
    <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">JePierre Soluções • Comunidade Inteligência Agêntica</p>
    <p style="margin: 6px 0 0 0; font-size: 13px;">
      <a href="https://inteligenciaagentica.com.br" style="color: #0284c7; text-decoration: none; font-weight: 600;">inteligenciaagentica.com.br</a>
    </p>
  </div>
</div>
"""

HTML_15MIN = """<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6;">
  <div style="text-align: center; margin-bottom: 24px;">
    <span style="display: inline-block; background-color: #f59e0b; color: #07070A; font-size: 11px; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; padding: 6px 16px; border-radius: 9999px; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);">
      🔥 COMEÇA EM 15 MINUTOS • SALA ABERTA
    </span>
    <h1 style="color: #0f172a; font-size: 22px; font-weight: 800; margin-top: 14px; margin-bottom: 6px;">
      A Sala já está Liberada no Google Meet!
    </h1>
    <p style="color: #64748b; font-size: 14px; margin: 0;">
      Estamos nos minutos finais de contagem regressiva para começar.
    </p>
  </div>

  <p style="font-size: 15px;">Olá, <strong>{{ if .Subscriber.FirstName }}{{ .Subscriber.FirstName }}{{ else }}{{ .Subscriber.Name }}{{ end }}</strong>!</p>

  <p style="font-size: 15px;">
    Faltam apenas <strong>15 minutos</strong>! A sala já foi aberta para você testar seu microfone, áudio e conexão.
  </p>

  <!-- Botão de Acesso Principal ao Google Meet -->
  <div style="text-align: center; margin: 30px 0;">
    <a href="https://meet.google.com/cwh-omwb-ezs" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #DFBA6B 0%, #C4973B 100%); color: #07070A !important; text-decoration: none !important; font-weight: 800; font-size: 16px; padding: 18px 38px; border-radius: 12px; box-shadow: 0 4px 16px rgba(223, 186, 107, 0.4); text-transform: uppercase; letter-spacing: 0.05em;">
      👉 ENTRAR NA SALA AGORA (GOOGLE MEET)
    </a>
    <p style="font-size: 13px; color: #64748b; margin-top: 12px;">
      Link fixo da sala:<br>
      <a href="https://meet.google.com/cwh-omwb-ezs" style="color: #0284c7; font-weight: 700; word-break: break-all;">https://meet.google.com/cwh-omwb-ezs</a>
    </p>
  </div>

  <p style="font-size: 15px;">
    Pontualmente às 19:30h iniciamos os trabalhos. Clica no botão acima e já entra na sala!
  </p>

  <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
    <p style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">Jean Pierre Schramm</p>
    <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">JePierre Soluções • Comunidade Inteligência Agêntica</p>
    <p style="margin: 6px 0 0 0; font-size: 13px;">
      <a href="https://inteligenciaagentica.com.br" style="color: #0284c7; text-decoration: none; font-weight: 600;">inteligenciaagentica.com.br</a>
    </p>
  </div>
</div>
"""

HTML_LIVE = """<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6;">
  <div style="text-align: center; margin-bottom: 24px;">
    <span style="display: inline-block; background-color: #ef4444; color: #ffffff; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; padding: 6px 16px; border-radius: 9999px; box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);">
      🔴 AO VIVO AGORA • SALA LIBERADA
    </span>
    <h1 style="color: #0f172a; font-size: 22px; font-weight: 800; margin-top: 14px; margin-bottom: 6px;">
      O Encontro ao Vivo Começou!
    </h1>
    <p style="color: #64748b; font-size: 14px; margin: 0;">
      Entre agora na transmissão para não perder nenhum minuto do conteúdo prático.
    </p>
  </div>

  <p style="font-size: 15px;">Olá, <strong>{{ if .Subscriber.FirstName }}{{ .Subscriber.FirstName }}{{ else }}{{ .Subscriber.Name }}{{ end }}</strong>!</p>

  <p style="font-size: 15px;">
    Acabamos de abrir a sala de transmissão do <strong>Encontro ao Vivo da Inteligência Agêntica</strong> desta quinta-feira.
  </p>

  <!-- Botão de Acesso Principal ao Google Meet -->
  <div style="text-align: center; margin: 30px 0;">
    <a href="https://meet.google.com/cwh-omwb-ezs" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #DFBA6B 0%, #C4973B 100%); color: #07070A !important; text-decoration: none !important; font-weight: 800; font-size: 16px; padding: 18px 38px; border-radius: 12px; box-shadow: 0 4px 16px rgba(223, 186, 107, 0.4); text-transform: uppercase; letter-spacing: 0.05em;">
      👉 ENTRAR NA TRANSMISSÃO AO VIVO (GOOGLE MEET)
    </a>
    <p style="font-size: 13px; color: #64748b; margin-top: 12px;">
      Link fixo da sala:<br>
      <a href="https://meet.google.com/cwh-omwb-ezs" style="color: #0284c7; font-weight: 700; word-break: break-all;">https://meet.google.com/cwh-omwb-ezs</a>
    </p>
  </div>

  <!-- Pauta da Live de Hoje -->
  <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #DFBA6B; border-radius: 8px; padding: 18px 20px; margin: 24px 0;">
    <h3 style="margin-top: 0; margin-bottom: 12px; font-size: 15px; font-weight: 700; color: #0f172a;">
      📌 O que vamos construir juntos hoje:
    </h3>
    <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #334155; line-height: 1.8;">
      <li><strong>Demonstração ao vivo:</strong> Configuração e comando de funcionários digitais autônomos.</li>
      <li><strong>Infraestrutura real:</strong> Deploy e orquestração em VPS com Docker Swarm e segurança.</li>
      <li><strong>Tira-dúvidas na prática:</strong> Análise de casos reais e respostas diretas para os participantes.</li>
    </ul>
  </div>

  <p style="font-size: 14px; color: #475569;">
    ⚠️ <strong>Aviso:</strong> A aula é dinâmica e vamos direto ao código e à prática. Pegue seu bloco de notas e venha com suas perguntas prontas!
  </p>

  <p style="font-size: 15px; margin-top: 20px;">
    Clica no botão acima e vem pra sala do Google Meet. Te espero lá dentro!
  </p>

  <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
    <p style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">Jean Pierre Schramm</p>
    <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">JePierre Soluções • Comunidade Inteligência Agêntica</p>
    <p style="margin: 6px 0 0 0; font-size: 13px;">
      <a href="https://inteligenciaagentica.com.br" style="color: #0284c7; text-decoration: none; font-weight: 600;">inteligenciaagentica.com.br</a>
    </p>
  </div>
</div>
"""

def sync():
    now_brt = datetime.datetime.now(TZ)
    print(f"[{now_brt.strftime('%Y-%m-%d %H:%M:%S')}] Verificando campanhas agendadas no Listmonk...")
    
    # 1. Obter campanhas existentes
    r = requests.get(f"{BASE_URL}/campaigns?per_page=100", cookies=COOKIES)
    if r.status_code != 200:
        print("Erro ao listar campanhas:", r.status_code, r.text)
        return False
    
    campaigns = r.json().get("data", {}).get("results", [])
    existing_scheduled = {}
    for c in campaigns:
        sa = c.get("send_at")
        if sa and c.get("status") in ["scheduled", "running", "finished"]:
            # Armazena por data/hora UTC normalizada
            existing_scheduled[sa] = c["name"]
    
    # 2. Descobrir as próximas 6 quintas-feiras
    thursdays = []
    curr = now_brt.date()
    # se hoje for quinta e ainda não passou das 19:30, considera hoje
    days_ahead = (3 - curr.weekday()) % 7
    if days_ahead == 0 and now_brt.hour >= 20:
        days_ahead = 7
    first_thursday = curr + datetime.timedelta(days=days_ahead)
    
    for i in range(6):
        thursdays.append(first_thursday + datetime.timedelta(weeks=i))
    
    for d in thursdays:
        d_str = d.strftime("%d/%m")
        slots = [
            (19, 0, f"Live {d_str} - Lembrete 30min", f"⏳ Faltam 30 minutos: Nosso Encontro ao Vivo começa às 19:30h ({d_str})", HTML_30MIN),
            (19, 15, f"Live {d_str} - Lembrete 15min", f"🔥 Começa em 15 minutos! Sala liberada para o Encontro ao Vivo ({d_str})", HTML_15MIN),
            (19, 30, f"Live {d_str} - No Ar 19:30h", f"🔴 ESTAMOS AO VIVO: Link do Encontro Inteligência Agêntica ({d_str})", HTML_LIVE),
        ]
        
        for hour, minute, name, subject, body in slots:
            dt_brt = datetime.datetime(d.year, d.month, d.day, hour, minute, 0, tzinfo=TZ)
            if dt_brt <= now_brt:
                continue
                
            dt_utc = dt_brt.astimezone(datetime.timezone.utc)
            send_at_iso = dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            if send_at_iso in existing_scheduled:
                # Já existe campanha agendada para esse horário
                continue
                
            print(f"📅 Agendando nova campanha: '{name}' para {send_at_iso}...")
            payload = {
                "name": name,
                "subject": subject,
                "lists": [LIST_ID],
                "type": "regular",
                "content_type": "html",
                "body": body,
                "send_at": send_at_iso,
                "tags": ["live", "encontro-ao-vivo", "iahermes"]
            }
            
            c_res = requests.post(f"{BASE_URL}/campaigns", json=payload, cookies=COOKIES)
            if c_res.status_code == 200:
                cid = c_res.json().get("data", {}).get("id")
                requests.put(f"{BASE_URL}/campaigns/{cid}/status", json={"status": "scheduled"}, cookies=COOKIES)
                print(f"✅ Agendada com sucesso! ID: {cid}")
            else:
                print(f"❌ Falha ao criar campanha: {c_res.status_code} {c_res.text}")

    print("Verificação concluída!")
    return True

if __name__ == "__main__":
    sync()
