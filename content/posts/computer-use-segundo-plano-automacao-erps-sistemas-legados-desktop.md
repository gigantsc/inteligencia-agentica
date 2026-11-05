---
title: "Computer Use em Segundo Plano: Como Agentes de IA Operam ERPs e Softwares Desktop sem Roubar o Mouse"
date: "2026-11-05"
lastmod: "2026-11-05"
summary: "Descubra como o Hermes Agent utiliza o driver CUA e o contrato No-Foreground para automatizar ERPs legados, sistemas contábeis e softwares Windows em segundo plano, sem APIs e sem interromper o operador humano."
tags: ["Computer Use", "RPA Agêntico", "ERPs Legados", "Hermes Agent", "Automação Corporativa", "Gestão de Negócios"]
keywords: ["computer use agentes ia", "automacao erp sem api", "rpa agentico hermes", "cua driver segundo plano", "no foreground contract", "automacao windows legada"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/computer-use-segundo-plano-automacao-desktop.jpg"
draft: false
---

> **Resposta Rápida (Answer-First / GEO):**  
> O **Computer Use em Segundo Plano (Background CUA)** do ecossistema Hermes Agent resolve o maior gargalo da automação corporativa: interagir com sistemas legados de desktop (como ERPs SAP GUI, TOTVS Protheus, WinThor ou emissores fiscais) que não possuem APIs REST. Ao implementar o rigoroso **No-Foreground Contract** através do `cua-driver`, o agente lê diretamente a árvore de acessibilidade do sistema operacional (Windows UIAutomation, macOS SkyLight ou Linux AT-SPI) e despacha cliques e digitações sintetizados direto para o processo da aplicação (PID), sem sequestrar a tela, sem roubar o foco da janela ativa e sem mover o cursor físico do mouse. Dessa forma, o agente autônomo e o colaborador humano coexistem e trabalham simultaneamente na mesma estação de trabalho ou VPS corporativa.

---

## O Gargalo dos Sistemas Legados nas Empresas Reais

Em empresas consolidadas com faturamento maduro e dezenas de colaboradores — em setores como atacado, logística, varejo, manufatura e serviços —, a maior parte das rotinas operacionais críticas não acontece em plataformas web modernas. 

Elas operam em sistemas desktop desenvolvidos há 10, 15 ou 20 anos:
- **ERPs de grande porte instalados localmente:** SAP GUI, TOTVS Protheus, Linx, Senior Sistemas, Sankhya ou WinThor;
- **Sistemas fiscais e contábeis de governos:** Validadores SPED, emissores de NF-e/NFS-e, programas de remessa bancária CNAB 240/400;
- **Aplicativos legados em Win32, WPF, Delphi ou Java Swing** cujas equipes de desenvolvimento originais sequer existem mais.

Até hoje, quando o diretor de operações ou o empresário buscava automatizar o preenchimento de notas, conferência de ordens de serviço ou conciliação financeira, esbarrava em duas opções dolorosas:

1. **Pagar orçamentos estratosféricos (R$ 50 mil a R$ 200 mil+)** para customizar APIs legadas no fornecedor do ERP — processo que costuma levar meses de burocracia;
2. **Implementar ferramentas de RPA (Robotic Process Automation) tradicional** como UiPath ou Automation Anywhere, que exigem licenças anuais caríssimas e operam travando a máquina: quando o robô roda, a tela fica "possuída", o mouse se move sozinho e nenhum ser humano pode tocar no computador.

Com a evolução dos agentes autônomos no **Hermes Agent**, esse paradigma foi completamente superado pelo conceito de **Computer Use em Segundo Plano**.

---

## O Que É o Contrato "No-Foreground" (Background CUA)?

O grande diferencial da arquitetura de Computer Use do Hermes Agent em relação a outras abordagens do mercado (como a implementação proprietária de Computer Use da Anthropic) reside no **No-Foreground Contract** viabilizado pelo `cua-driver` integrado nativamente como um servidor MCP (*Model Context Protocol*).

Em ferramentas comuns de controle de mouse/teclado (como PyAutoGUI ou scripts baseados em OCR), o software simplesmente assume as coordenadas globais da tela `(X, Y)` e despacha eventos no monitor ativo. Se uma janela de chat pipocar na frente ou se o usuário mover o mouse, a automação erra o clique e corrompe dados.

No Hermes Agent, o `cua-driver` opera em uma camada muito mais profunda do sistema operacional:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          ARQUITETURA BACKGROUND COMPUTER USE                           │
└────────────────────────────────────────────────────────────────────────────────────────┘

     COLABORADOR HUMANO                                    AGENTE HERMES (AUTÔNOMO)
  (Digitando proposta no Word)                       (Lançando faturas no ERP Desktop)
               │                                                      │
               ▼                                                      ▼
  ┌─────────────────────────┐                            ┌─────────────────────────┐
  │   Janela em Foco Ativo  │                            │  Janela em Segundo Plano│
  │     (Microsoft Word)    │                            │    (TOTVS / SAP GUI)    │
  └────────────┬────────────┘                            └────────────┬────────────┘
               │                                                      ▲
               │ Cursor e Foco Intactos                               │ Eventos Direcionados por PID
               │                                                      │ (Sem roubo de foco)
               ▼                                                      │
  ┌───────────────────────────────────────────────────────────────────┴─────────────────┐
  │                       KERNEL & SUBSISTEMAS DO SISTEMA OPERACIONAL                   │
  │                                                                                     │
  │  • Windows: UIAutomation Tree Reader  +  PostMessage / SendInput (Scoped to PID)    │
  │  • macOS:   SkyLight SPIs (SLPSPostEventRecordTo)                                   │
  │  • Linux:   AT-SPI Accessibility Bus  +  Virtual Input                              │
  └─────────────────────────────────────────────────────────────────────────────────────┘
```

### Como cada plataforma garante o isolamento:
1. **No Windows 10/11:** O driver conecta à árvore nativa do **UIAutomation**, identificando cada botão, caixa de seleção, tabela e campo de entrada por identificadores semânticos (AutomationId, Name, ClassName). Os disparos de clique e teclas utilizam `PostMessage` e injeções com escopo restrito ao identificador de processo (PID), sem precisar trazer a janela para o primeiro plano;
2. **No macOS:** Utiliza as APIs internas de acessibilidade (AX) e chamadas do SkyLight (`SLPSPostEventRecordTo`), disparando eventos diretamente ao processo alvo sem deslocar o cursor físico do mouse nem alternar espaços/desktops virtuais;
3. **No Linux (X11 e Wayland):** Conecta ao barramento AT-SPI e despacha eventos sintetizados através de pontes de teclado e ponteiro virtual.

---

## Tabela Comparativa: RPA Tradicional vs. Computer Use Agêntico

| Dimensão | RPA Tradicional (UiPath / Automation Anywhere) | Scripts Simples (PyAutoGUI / Coordenadas) | Computer Use Agêntico (Hermes Agent + CUA) |
|---|---|---|---|
| **Interrupção do Operador** | 🔴 Bloqueia o mouse e a máquina inteira | 🔴 Bloqueia o mouse e falha se a tela mudar | 🟢 **Zero interrupção** (roda 100% em background) |
| **Resiliência a Mudanças de Layout** | 🟡 Frágil (exige remapeamento manual constante) | 🔴 Péssima (qualquer pixel fora quebra o fluxo) | 🟢 **Alta** (compreensão semântica da árvore de UI) |
| **Dependência de Modelo** | N/A (Regras rígidas pré-programadas) | N/A (Scripts estáticos) | 🟢 **Agnóstico:** Claude, GPT-4o, DeepSeek, Ollama |
| **Custo de Licenciamento** | 🔴 R$ 3.000 a R$ 15.000+ por mês por robô | 🟢 Gratuito (mas com alto custo de manutenção) | 🟢 **Open-source**, pagando apenas centavos de API |
| **Tratamento de Exceções** | 🔴 Para e dispara alerta de erro ao menor desvio | 🔴 Trava ou clica no lugar errado | 🟢 **Raciocínio autônomo** para contornar pop-ups e avisos |
| **Segurança e Restrições** | 🟡 Dependente de senhas gravadas na ferramenta | 🔴 Sem qualquer controle de fronteira | 🟢 **Manifesto formal (`bounded mode`)** |

---

## Modelo-Agnóstico: Fuja do Aprisionamento Tecnológico (Vendor Lock-in)

Quando a Anthropic anunciou sua prévia de Computer Use, ela exigiu chamadas proprietárias com endpoints exclusivos da API do Claude 3.5 Sonnet. Isso criou um dilema sério para as empresas: como confiar operações volumosas de milhares de telas por dia em um modelo com custos elevados por milhão de tokens?

O subsistema `computer_use` do Hermes Agent desacoplou o controle de desktop da inferência do modelo:
- Ele traduz ações de tela (ler árvore, capturar screenshot, focar campo, clicar, rolar, digitar texto) em ferramentas padrão no protocolo MCP;
- Qualquer modelo com capacidade nativa de *Tool-Calling* (chamada de ferramentas) pode pilotar o computador;
- Empresas podem utilizar modelos de altíssimo custo-benefício, como **DeepSeek V3** ou **Gemini 2.0 Flash**, ou até mesmo **modelos locais via Ollama/vLLM**, garantindo que nenhum dado confidencial ou tela de cliente saia da rede corporativa local.

---

## Os Três Níveis de Governança e Segurança

Dar acesso ao desktop para uma inteligência artificial exige controles rígidos. No Hermes Agent, isso é gerenciado por três modos de permissão imutáveis durante a inicialização da sessão:

```yaml
# Exemplo de configuração de segurança no ~/.hermes/config.yaml
computer_use:
  permission_mode: bounded
  capability_manifest: ~/.hermes/cua-manifest.yaml
```

### 1. Modo `standard` (Supervisionado / Smart Approvals)
O comportamento padrão do Hermes Agent. Toda ação que envolva comandos potencialmente críticos no sistema operacional exige autorização prévia do usuário ou é avaliada pelo motor de aprovação inteligente. Ideal para tarefas assistidas durante o expediente.

### 2. Modo `bounded` (Manifesto Corporativo Restrito)
O modo perfeito para automações contínuas e fluxos de backoffice em produção. Você define um arquivo formal de capacidades (`cua-manifest.yaml`) especificando:
- A lista exata de executáveis autorizados (ex: `totvs_smartclient.exe`, `saplogon.exe`);
- Os títulos de janelas permitidos;
- As ações de teclado/mouse autorizadas;
- Os perfis de navegador permitidos.

Se o agente sofrer alucinação ou tentar alternar para um aplicativo não listado (como um leitor de e-mails ou terminal desautorizado), o `cua-driver` **aborta a chamada imediatamente na raiz** (*fail-closed*), impedindo qualquer ação fora do escopo.

### 3. Modo `unrestricted` (Isolamento em Sandbox / VM)
Acionado via parâmetro `--yolo` ou `/yolo`. Desativa confirmações interativas para máxima velocidade. Deve ser utilizado **exclusivamente** em containers Docker isolados (como a imagem oficial `nousresearch/hermes-sandbox:desktop`) ou em máquinas virtuais dedicadas e descartáveis.

---

## Diagnóstico e Instalação na Prática

O Hermes Agent inclui ferramentas de verificação instantânea para garantir que os subsistemas de acessibilidade e captura estejam 100% operacionais na sua máquina física ou VPS Windows.

### 1. Ativação do Toolset
Para habilitar o Computer Use em sua sessão interativa ou terminal:

```bash
# Ativar para uma sessão direta
hermes -t computer_use chat

# Ou instalar os binários do driver via gerenciador de pacotes do Hermes
hermes computer-use install
```

### 2. Rodando o Diagnóstico com `doctor`
O comando `hermes computer-use doctor` executa uma auditoria completa na infraestrutura gráfica:

```bash
hermes computer-use doctor
```

Saída típica de validação em ambiente Windows corporativo:
```text
✅ binary_version: cua-driver v0.20.4
✅ platform_supported: Windows 11 Pro 64-bit (build 26100)
✅ session_active: MCP session is active via stdio
✅ uiautomation_capability: UIAutomation backend reachable and registered
✅ screen_capture_capability: Desktop capture available (Display 1: 1920x1080)
✅ input_synthesizer: PostMessage & SendInput background dispatch ready
Status: OPERATIONAL (Ready for background automation)
```

---

## Caso Real de Aplicação: Distribuidora de Medicamentos

Para ilustrar o impacto financeiro dessa tecnologia em operações tradicionais, acompanhe o caso de uma distribuidora com 180 colaboradores no interior de São Paulo.

### O Desafio
A empresa recebia diariamente cerca de 320 pedidos de compra de hospitais e clínicas através de planilhas e e-mails não padronizados. O ERP interno da empresa é uma versão cliente-servidor em Windows desenvolvida na década de 2000, sem qualquer API de integração. 

Para lançar esses pedidos, conferir o estoque físico e gerar os espelhos de notas fiscais, a distribuidora mantinha **4 colaboradores dedicados full-time** apenas digitando códigos de produto, validando lotes e clicando em telas do ERP — consumindo mais de 600 horas de digitação manual todo mês, com frequentes erros de digitação de lote e vencimento.

### A Solução com Hermes Agent & Computer Use
1. **Configuração da VPS Windows:** O Hermes Agent foi instalado em uma instância Windows Server conectada à rede local do ERP;
2. **Definição do Manifesto Bounded:** O arquivo `cua-manifest.yaml` autorizou exclusivamente a execução do executável do ERP (`distrib_erp.exe`) e as telas com cabeçalho "Lançamento de Pedidos" e "Consulta de Lotes";
3. **Agente Triador e Digitador:** Um agente Hermes monitora o recebimento dos pedidos, extrai os itens das ordens de compra, verifica a coerência com as regras de negócio e assume o preenchimento dos campos do ERP diretamente pela árvore de UIAutomation em background;
4. **Alerta e Auditoria:** Ao finalizar cada pedido, o agente envia o comprovante de lançamento e o número da ordem gerada diretamente para o canal de logística no Telegram/WhatsApp corporativo.

### O Resultado
- **Redução de 85% no tempo de faturamento:** O tempo médio de processamento de um pedido hospitalar caiu de 22 minutos para 1 minuto e 40 segundos;
- **Zero erros de digitação:** Eliminação total de devoluções por divergência de lote ou quantidade;
- **Realocação estratégica da equipe:** Os 4 colaboradores deixaram o trabalho mecânico de digitação e foram realocados para atendimento comercial e relacionamento com compradores hospitalares, aumentando o faturamento da distribuidora em 18% no primeiro trimestre.

---

## Como Começar na Sua Empresa

A automação agêntica de telas legadas não é um projeto para daqui a cinco anos — ela é uma realidade técnica disponível hoje. Se a sua empresa possui sistemas antigos que você achava impossível integrar sem gastar fortunas em desenvolvimento, o Computer Use em segundo plano é a chave para destravar a eficiência operacional do seu negócio.

Quer aprender a estruturar agentes autônomos seguros, configurar o `cua-driver` em máquinas Windows, desenhar manifestos corporativos rígidos e construir rotinas de alto impacto para a sua empresa? 

Conheça a formação executiva e prática do curso **[Inteligência Agêntica](https://inteligenciaagentica.com.br)** e junte-se a empresários e gestores que estão colocando agentes autônomos para trabalhar na ponta do negócio com segurança, rentabilidade e soberania de dados.
