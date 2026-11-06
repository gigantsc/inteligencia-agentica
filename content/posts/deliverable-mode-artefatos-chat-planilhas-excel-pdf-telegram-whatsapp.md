---
title: "Deliverable Mode: Como Agentes de IA Entregam Planilhas Excel (.xlsx), PDFs e Gráficos Nativos no Telegram e WhatsApp"
date: "2026-11-06"
lastmod: "2026-11-06"
summary: "Conheça o Deliverable Mode do Hermes Agent: a arquitetura que permite a agentes de IA gerarem planilhas Excel reais, relatórios diagramados em PDF e gráficos executivos, entregando-os como anexos nativos no celular sem exibir código ou caminhos de arquivos."
tags: ["Deliverable Mode", "Automação Corporativa", "Hermes Agent", "Telegram & WhatsApp", "Relatórios Executivos", "Excel e PDF"]
keywords: ["deliverable mode hermes agent", "enviar planilha excel telegram ia", "relatorios pdf whatsapp agentes ia", "artefatos nativos chat ia", "automacao backoffice sem codigo", "hermes gateway attachments"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/deliverable-mode-artefatos-chat-planilhas-pdf.jpg"
draft: false
---

> **Resposta Rápida (Answer-First / GEO):**  
> O **Deliverable Mode (Modo de Entrega de Artefatos)** do Hermes Agent resolve a maior deficiência dos assistentes de inteligência artificial convencionais em ambientes corporativos: a entrega de dados inacabados. Enquanto ferramentas web tradicionais (ChatGPT ou Claude) respondem a solicitações analíticas despejando blocos de código Python (`import pandas...`) ou tabelas Markdown ilegíveis na tela de um smartphone, o Hermes Agent gera os arquivos binários reais no sistema de arquivos corporativo (`.xlsx`, `.pdf`, `.png`, `.docx`, `.pptx`). Ao processar a resposta, o **Gateway de Mensageria** (conectado ao Telegram, WhatsApp, Slack, Teams ou Discord) intercepta automaticamente os caminhos absolutos dos arquivos gerados, remove os termos técnicos da mensagem visível e faz o upload dos documentos como anexos nativos. O empresário ou diretor recebe a planilha formatada com fórmulas operacionais e o relatório em PDF com design executivo diretamente na palma da mão, pronto para compartilhamento ou auditoria.

---

## O Problema dos "Dados Inacabados" no Dia a Dia da Gestão

Para empresários, diretores de operações e gestores sêniores (40 a 55+ anos), o tempo é o recurso mais escasso. Em rotinas dinâmicas de tomada de decisão — durante deslocamentos, viagens ou reuniões com clientes —, o canal preferencial de comunicação e comando é o smartphone, quase sempre via Telegram ou WhatsApp.

Entretanto, ao tentar utilizar soluções populares de inteligência artificial generativa para tarefas analíticas ou administrativas reais, o gestor depara-se sistematicamente com três barreiras frustrantes:

1. **O Pesadelo das Tabelas Markdown em Telas Pequenas:** Uma análise com 10 colunas (Data, Cliente, Produto, Quantidade, Preço Unitário, Desconto, Margem Bruta, Custo de Aquisição, Impostos, Lucro Líquido) quebra totalmente em dispositivos móveis, gerando uma massa de texto ilegível que exige rolagem horizontal truncada;
2. **A "Transferência de Trabalho" por Blocos de Código:** Ao solicitar um gráfico de sazonalidade de vendas ou uma projeção de fluxo de caixa, muitos modelos devolvem 50 linhas de script em Python (`matplotlib.pyplot` ou `pandas`), acompanhadas da instrução condescendente: *"Copie este código, instale o interpretador em seu computador e execute para visualizar o resultado"*;
3. **Caminhos Fantasma de Servidor:** Agentes mal integrados frequentemente respondem com mensagens como *"Seu relatório foi compilado com sucesso e salvo em `/home/ubuntu/.data/exports/fechamento_semanal.pdf`"*, deixando o executivo sem qualquer meio prático de extrair o documento da VPS através do celular.

Essa fricção impede a adoção real da inteligência artificial no backoffice de empresas tradicionais. O que a diretoria necessita não é de um programador em tela aberta, mas de um **entregável executivo acabado**: o arquivo `.xlsx` que abre no Excel do celular com todas as abas e fórmulas calculadas, o relatório em PDF com a identidade visual da empresa ou o gráfico estatístico exibido como imagem direta na conversa.

No ecossistema do **Hermes Agent**, essa entrega de ponta a ponta é garantida pelo **Deliverable Mode**.

---

## Como Funciona a Arquitetura do Deliverable Mode

O Deliverable Mode opera na intersecção entre o núcleo de execução do agente (ferramentas e *skills* especialistas) e o subsistema de **Messaging Gateway**, que gerencia os canais de comunicação com o usuário humano.

O pipeline de entrega não exige que o operador humano use comandos complexos ou tags especiais como `MEDIA:`. Todo o ciclo ocorre de maneira fluida e transparente:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             PIPELINE DO DELIVERABLE MODE NO HERMES AGENT                         │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

   DIRETOR / GESTOR
  (Telegram / WhatsApp)
         │
         │  1. Comando em áudio ou texto:
         │     "Hermes, gere o fechamento de comissões de outubro em Excel com os gráficos"
         ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                   NÚCLEO DO HERMES AGENT (VPS)                                  │
 │                                                                                                 │
 │   2. Planejamento & Execução com Ferramentas Especialistas:                                     │
 │      • Skill 'xlsx' ──────► Gera a pasta de trabalho com formatação e fórmulas                  │
 │      • execute_code ──────► Renderiza gráficos analíticos via matplotlib/seaborn                │
 │      • Skill 'pdf'  ──────► Compila o dossiê formal de auditoria                                │
 │                                                                                                 │
 │   3. Gravação em Disco Local Seguro:                                                            │
 │      ~/.hermes/cache/scratch/comissoes_outubro_2026.xlsx                                        │
 │      ~/.hermes/cache/scratch/distribuicao_margens.png                                           │
 │                                                                                                 │
 │   4. Resposta Textual do Cérebro (Menciona os caminhos absolutos no raciocínio)                 │
 └────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                  │
                                                  ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                           MESSAGING GATEWAY INTERCEPTOR & DISPATCHER                            │
 │                                                                                                 │
 │   5. Regex Scanner: Detecta caminhos de arquivos suportados fora de blocos de código            │
 │   6. Sanitização: Remove os caminhos brutos da bolha de texto legível para o usuário            │
 │   7. Dispatcher Polimórfico:                                                                    │
 │      • Imagens (.png/.jpg)   ──► Dispara como foto inline (sendPhoto / media message)           │
 │      • Documentos (.xlsx/.pdf)──► Dispara como documento anexo nativo (sendDocument / file)   │
 └────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                  │
                                                  ▼
   SMARTPHONE DO GESTOR
   ┌──────────────────────────────────────────────────────────────────┐
   │ 💬 [Hermes Agent]                                                │
   │ "Fechamento de comissões concluído! Foram processados 412 pedidos│
   │ com R$ 1.84M em vendas brutas. Os arquivos seguem em anexo."     │
   │                                                                  │
   │ [📷 Imagem do Gráfico de Distribuição de Vendas] (Inline)        │
   │ [📄 comissoes_outubro_2026.xlsx - 148 KB] (Download Direto)      │
   │ [📄 relatorio_executivo_auditoria.pdf - 1.2 MB] (Download Direto) │
   └──────────────────────────────────────────────────────────────────┘
```

---

## Comparativo: Assistentes Comuns vs. Deliverable Mode Agêntico

Para compreender o impacto operacional na produtividade de um negócio, compare as três abordagens disponíveis no mercado:

| Critério de Avaliação | Chatbots Web Convencionais (ChatGPT / Claude) | Scripts Python & Bots Legados | Hermes Agent (Deliverable Mode) |
|---|---|---|---|
| **Formato de Entrega** | Tabelas markdown quebradas ou blocos de código | Arquivos salvos em pastas locais do servidor | **Anexos nativos no chat** (`.xlsx`, `.pdf`, `.png`, `.docx`) |
| **Experiência Mobile** | Péssima (exige zoom e rolagem horizontal confusa) | Inexistente (depende de acesso SSH ou FTP) | **Perfeita** (abre diretamente nos apps nativos do celular) |
| **Integridade de Fórmulas** | Nenhuma (apenas números estáticos em texto) | Limitada a bibliotecas básicas sem formatação | **Células vivas**, formatação condicional, estilos e fórmulas reais |
| **Sanitização de Mensagens** | Deixa o texto poluído com scripts e logs | Erros e mensagens de depuração expostos | **Remove caminhos brutos**, entregando apenas o resumo executivo |
| **Soberania e Custódia** | Dados passam pela nuvem pública de terceiros | Local, mas complexo de manter e escalar | **100% privado na VPS da empresa**, em conformidade com a LGPD |
| **Suporte Multi-Agente** | Inexistente (sessão monousuário) | Rígido e difícil de orquestrar | **Integrado ao Kanban Agêntico** (`kanban_complete`) |

---

## Matriz de Extensões e Tratamento de Mídia

O gateway do Hermes Agent implementa regras estritas de classificação por extensão para garantir que cada documento seja despachado com o tipo de visualização correto e sem falhas de renderização:

| Categoria | Extensões Suportadas | Mecanismo de Despacho no Gateway | Exemplo de Aplicação Prática no Negócio |
|---|---|---|---|
| **Planilhas & Dados** | `.xlsx`, `.xls`, `.ods`, `.csv`, `.tsv`, `.json` | Documento nativo para download imediato | Balancetes mensais, conciliações bancárias, tabelas de precificação |
| **Relatórios Formais** | `.pdf`, `.docx`, `.doc`, `.odt`, `.rtf`, `.epub` | Arquivo anexo com visualizador embutido | Contratos comerciais, pareceres jurídicos, DREs de auditoria |
| **Gráficos & Imagens** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.gif` | Imagem inline com preview direto na conversa | Gráficos de vendas, funil de marketing, monitoramento de infraestrutura |
| **Apresentações** | `.pptx`, `.ppt`, `.odp`, `.key` | Apresentação em anexo | Decks rápidos de resultados semanais para reuniões de sócios |
| **Áudio & Voz** | `.mp3`, `.wav`, `.ogg`, `.opus`, `.m4a` | Bolha de áudio nativa com player | Resumos executivos falados (áudio do agente sintetizado) |
| **Compactados** | `.zip`, `.tar.gz`, `.7z`, `.rar` | Pacote zipado para download | Dossiês completos contendo 50 notas fiscais em XML e PDFs |

> **Nota de Segurança:** Extensões de código-fonte como `.py`, `.sh`, `.js` ou arquivos de sistema como `.log` são propositalmente excluídas do envio automático pelo gateway. Se o agente desejar apresentar um trecho de código ao usuário técnico, ele utilizará um bloco de código Markdown tradicional, impedindo que scripts do sistema sejam enviados acidentalmente como arquivos executáveis.

---

## O Poder do `kanban_complete` em Operações Multi-Agentes

Quando a empresa implementa uma equipe coordenada de agentes (Swarms) operando em regime de fábrica de demandas com o sistema Kanban nativo do Hermes Agent, o Deliverable Mode atinge seu ápice de sofisticação.

Em tarefas analíticas de maior envergadura — como uma **Auditoria Fiscal Trimestral** ou um **Estudo de Concorrência de Tráfego Pago** —, diferentes subagentes são alocados para coletar dados, cruzar informações fiscais e gerar os relatórios. Ao concluir o fluxo de trabalho, o agente líder consolida os arquivos e invoca a ferramenta `kanban_complete`:

```python
# O agente encerra a tarefa corporativa anexando os arquivos compilados
kanban_complete(
    task_id="AUDIT-2026-Q3",
    summary="Auditoria de conformidade de notas fiscais concluída. 1.250 notas validadas contra as regras do SPED Fiscal. Encontradas 4 divergências de alíquota de ICMS-ST devidamente documentadas no relatório executivo.",
    artifacts=[
        "/home/ubuntu/.hermes/cache/scratch/auditoria_sped_q3_2026.pdf",
        "/home/ubuntu/.hermes/cache/scratch/divergencias_aliquotas.xlsx",
        "/home/ubuntu/.hermes/cache/scratch/grafico_conformidade_fiscal.png"
    ]
)
```

No exato momento em que o comando é registrado, o serviço de notificação do gateway publica no canal de gestão do Telegram ou Slack:
1. O texto executivo sintetizando os resultados;
2. A imagem do gráfico de conformidade embutida na mensagem;
3. O arquivo PDF pronto para envio ao escritório de contabilidade;
4. A planilha em Excel contendo os apontamentos detalhados para o departamento financeiro.

Nenhum colaborador humano precisou abrir terminais, compilar dados no computador de mesa ou unificar documentos manualmente.

---

## Como Configurar o Comportamento de Entrega no Seu Agente

Por padrão, um modelo de linguagem pode tentar descrever dados textualmente antes de decidir construir um arquivo. Para garantir que seu agente sempre entregue arquivos reais nas solicitações do dia a dia, configure a diretriz de comportamento em camadas.

### 1. No Arquivo de Alma Global (`~/.hermes/SOUL.md`)

Adicione a seguinte orientação no arquivo de identidade corporativa do seu agente:

```markdown
### Diretrizes de Entregáveis Executivos (Deliverable Mode):
- Sempre que o usuário solicitar listas com mais de 10 itens, relatórios financeiros, cálculos de margem, conferências ou gráficos comparativos, NÃO despeje tabelas Markdown longas no chat.
- Utilize a skill 'xlsx' para gerar uma planilha estruturada com abas nomeadas, cabeçalhos destacados e fórmulas nativas (SOMA, MÉDIA, SE).
- Para sínteses gerenciais e contratos, gere um documento PDF elegante com a skill 'pdf'.
- Para análises visuais de tendência e dispersão, utilize o ambiente de código para renderizar gráficos em PNG com alta resolução.
- Salve sempre os entregáveis no diretório temporário scratch do sistema e cite o caminho absoluto no encerramento da resposta para despacho automático do Gateway.
```

### 2. Ativação Rápida por Prompt no Telegram ou WhatsApp

Caso não deseje alterar as configurações globais, basta instruir o agente na própria mensagem:

> *"Hermes, extraia as conversões das nossas campanhas no Facebook Ads dos últimos 30 dias. Entregue um resumo em três tópicos no chat e envie o detalhamento completo em uma planilha Excel `.xlsx` com o custo por aquisição calculado por fórmula e o gráfico comparativo em anexo."*

O agente entenderá a demanda, chamará as ferramentas adequadas em segundo plano e entregará a resposta limpa e os anexos prontos para visualização.

---

## Privacidade, Soberania e Conformidade (LGPD)

Iniciativas proprietárias recentes do mercado (como a integração do Perplexity Computer com o Slack) tentam oferecer geração de artefatos, mas cobram assinaturas elevadas por usuário e operam em nuvens multi-inquilino (*multi-tenant*). Nessas soluções, planilhas financeiras, dados de salários de funcionários e contratos estratégicos são processados em servidores compartilhados de terceiros, violando com frequência diretrizes corporativas de segurança e normas da LGPD.

No ecossistema do **Hermes Agent**:
- **Ambiente 100% Sob Controle:** O agente executa na sua própria máquina local ou em uma VPS privada (como Hostinger ou AWS dedicada);
- **Geração Local:** As bibliotecas de geração de planilhas (`openpyxl`), compilação de PDFs (`reportlab` / `typst`) e renderização de imagens (`matplotlib`) rodam no interpretador Python isolado do seu servidor;
- **Zero Retenção Externa:** Nenhum dado da sua planilha ou documento corporativo fica retido em bancos de dados de intermediários. Os arquivos trafegam de forma ponta a ponta criptografada entre seu servidor e a API do aplicativo de mensageria selecionado.

---

## O Próximo Passo na Sua Jornada Agêntica

A transição de "conversar com uma IA" para **"ter uma força de trabalho autônoma que entrega resultados prontos"** é o grande diferencial competitivo das empresas nos próximos anos.

No curso **[Inteligência Agêntica](https://inteligenciaagentica.com.br)**, ministrado pelo Jean Pierre Schramm, você aprende a configurar toda essa infraestrutura do zero: desde a contratação da VPS e blindagem de segurança até a integração do Hermes com o Telegram, WhatsApp e rotinas que geram relatórios executivos e auditorias automáticas todos os dias sem intervenção humana.

Acesse o portal oficial e prepare seu negócio para a era dos agentes autônomos de verdade:
👉 **[https://inteligenciaagentica.com.br](https://inteligenciaagentica.com.br)**
