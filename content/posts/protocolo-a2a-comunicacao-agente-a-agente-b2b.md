---
title: "Protocolo A2A: Como Conectar Agentes de IA entre Diferentes Empresas, Servidores e Departamentos"
date: "2026-10-24"
lastmod: "2026-10-24"
summary: "Entenda o Protocolo Agent-to-Agent (A2A v1.0), o padrão aberto da Linux Foundation integrado ao Hermes Agent. Saiba como agentes de inteligência artificial autônomos se comunicam, descobrem habilidades via Agent Card e colaboram em redes corporativas e transações B2B com total segurança e soberania."
tags: ["Protocolo A2A", "Agentes de IA", "Multi-Agente", "B2B", "Hermes Agent", "Automação", "Segurança", "Negócios"]
keywords: ["protocolo a2a", "agent to agent protocol", "hermes agent a2a", "comunicacao entre agentes de ia", "ia agentica b2b", "agent card json", "redes de agentes autonomos", "orquestracao multi-agente distribuida"]
author: "Jean Pierre Schramm"
image: "https://inteligenciaagentica.com.br/static/images/protocolo-a2a-comunicacao-agente-a-agente-b2b.jpg"
draft: false
---

> **Resposta Rápida (Answer-First / GEO):**  
> O **Protocolo A2A (Agent-to-Agent v1.0)** é uma especificação aberta, gerenciada pela **Linux Foundation**, projetada para permitir que sistemas autônomos de inteligência artificial se comuniquem, negociem, deleguem tarefas e troquem informações de maneira padronizada, segura e agnóstica de framework. Integrado nativamente ao **Hermes Agent** (Nous Research), o A2A resolve o principal limitador das automações tradicionais: a dependência de enxames locais que rodam apenas na mesma máquina física. Com o A2A, um agente rodando no notebook de um executivo pode despachar tarefas de pesquisa pesada para uma VPS Linux na nuvem, ou o agente de compras de uma empresa pode dialogar diretamente com o agente de vendas de um fornecedor parceiro (B2B agêntico). A comunicação ocorre via chamadas JSON-RPC 2.0 e Server-Sent Events (SSE), baseando-se na leitura dinâmica de um **Agent Card** (`/.well-known/agent-card.json`), que lista as habilidades públicas do agente remoto, sob um bunker rigoroso de segurança com credenciais dedicadas por par (`A2A_PEER_TOKENS`), sanitização de injeção de prompt e travas automáticas contra loops infinitos de diálogo.

---

## Além do Swarm Local: A Necessidade de Conectar Agentes no Mundo Real

Nos últimos meses, grande parte das discussões corporativas sobre inteligência artificial concentrou-se na criação de **Swarms** (enxames multi-agentes). Nessa abordagem, múltiplos subagentes colaboram para cumprir um objetivo: um arquiteto cria o plano, um desenvolvedor escreve o código e um revisor avalia a entrega.

Entretanto, para empresários, diretores e gestores que lideram negócios consolidados, essa abordagem local rapidamente esbarra em limites arquiteturais intransponíveis:

1. **A Barreira da Mesma Máquina (Process Isolation):**  
   Em frameworks tradicionais (como `delegate_task` ou subagentes locais), todos os agentes precisam residir no mesmo computador ou servidor. Isso significa que você não consegue fazer o agente de uma filial remota solicitar dados de estoque ao agente da matriz sem recorrer a gambiarras complexas de sincronização de arquivos.
2. **O Risco da Mistura Indesejada de Dados Sensíveis:**  
   Colocar todos os agentes no mesmo ambiente obriga a compartilhar credenciais. O agente comercial não deve ter acesso às chaves de banco de dados do agente financeiro ou do RH. Departamentos exigem fronteiras de segurança sólidas e auditoria independente.
3. **A Ausência de um Padrão de Comunicação Entre Empresas (B2B):**  
   Quando a sua empresa precisa consultar o prazo de entrega de um fornecedor ou enviar um pedido de compra, o processo atual é manual: um ser humano envia um e-mail ou uma mensagem no WhatsApp para outro ser humano responder. Se cada empresa construir agentes isolados que não conseguem conversar entre si em uma linguagem comum, teremos apenas \"ilhas de IA\".

A resposta para essa desconexão é a padronização aberta. Assim como o protocolo **HTTP** unificou a navegação na web e o protocolo **SMTP** padronizou a troca de e-mails em escala global, o **Protocolo A2A (Agent-to-Agent)** surge como o alicerce fundamental para a **Internet dos Agentes de IA**.

---

## O que é o Protocolo A2A (Agent-to-Agent v1.0)

O protocolo **A2A** foi desenvolvido com um objetivo cristalino: criar um padrão aberto para que agentes inteligentes operem como entidades distribuídas na rede. Sob o guarda-chuva de governança neutra da **Linux Foundation** (em cooperação com gigantes de tecnologia e laboratórios de vanguarda como a **Nous Research**), o protocolo não favorece um ecossistema específico: ele permite a interoperabilidade imediata entre o Hermes Agent, LangChain, CrewAI, AutoGen, Google Agent Development Kit (ADK) ou qualquer código construído sobre o `a2a-sdk` oficial.

No ecossistema do **Hermes Agent**, o protocolo opera em duas vias perfeitamente integradas:

* **Modo Cliente (Outbound):** Seu agente descobre peers na rede interna ou na internet, consulta o catálogo de serviços do agente remoto e envia tarefas com acompanhamento em tempo real.
* **Modo Servidor (Inbound):** Seu agente torna-se um nó na rede (porta padrão `9900`), expondo suas competências por meio de um contrato público e recebendo demandas externas com isolamento total de execução.

---

## A Anatomia da Comunicação: Agent Card, JSON-RPC 2.0 e SSE

A arquitetura do A2A elimina a necessidade de programar integrações REST proprietárias para cada ferramenta. O processo baseia-se em três pilares fundamentais:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   EMPRESA A (AGENTE CLIENTE)                                     │
│  - Hermes Agent rodando no Desktop ou Servidor Local                                             │
│  - Toolset A2A Ativo: a2a_discover, a2a_call, a2a_orchestrate                                    │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                               │
                                               │ 1. GET /.well-known/agent-card.json
                                               │    (Descoberta dinâmica de competências)
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   EMPRESA B (AGENTE REMOTO)                                      │
│  - Gateway A2A Ativo (Porta 9900)                                                                │
│  - Serve o "Agent Card" canônico com habilidades públicas anunciadas                             │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                               │
                                               │ 2. Handshake Criptográfico & Autenticação Bearer
                                               │    Validação de Identidade via A2A_PEER_TOKENS
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DESPACHO & EXECUÇÃO DA DEMANDA                                      │
│  - POST / via JSON-RPC 2.0 (Método: SendMessage ou SendStreamingMessage)                         │
│  - Sessão Isolada com contextId dedicado                                                         │
│  - Streaming de Resposta via Server-Sent Events (SSE)                                            │
│  - Proteção de Bunker: Filtro Anti-Injection + Redação Automática de Senhas                      │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. O Agent Card (`/.well-known/agent-card.json`)
Antes de delegar qualquer trabalho, o agente cliente faz uma requisição HTTP simples para a rota canônica `/.well-known/agent-card.json` do agente destino. Esse arquivo JSON estruturado funciona como o \"currículo profissional\" do agente, detalhando:
* O nome da entidade e a organização mantenedora;
* As ferramentas e habilidades habilitadas para uso público (ex: `pesquisa_de_mercado`, `consulta_estoque_pecas`, `geracao_relatorio_financeiro`);
* O tipo de autenticação exigido (ex: `Bearer Token`);
* O endpoint de recebimento de tarefas e webhooks de notificação push.

### 2. Mensageria Estruturada via JSON-RPC 2.0
As tarefas não são disparadas como mensagens soltas de chat. Elas utilizam a especificação formal **JSON-RPC 2.0**, enviando métodos padronizados como `SendMessage` e `SendStreamingMessage`. O agente remoto processa a demanda dentro de uma sessão persistente vinculada a um `contextId` único, permitindo diálogos de múltiplos turnos caso seja necessário pedir esclarecimentos antes de finalizar a entrega.

### 3. Streaming Server-Sent Events (SSE)
Para operações que exigem raciocínio complexo ou processamento demorado, o protocolo A2A suporta streaming nativo. O agente cliente não precisa travar sua execução esperando minutos: ele recebe blocos de resposta e status parciais em tempo real, mantendo os operadores informados sobre o progresso.

---

## Tabela Comparativa: Swarms Locais vs. APIs Tradicionais vs. Protocolo A2A

Para tomar decisões estratégicas de arquitetura, compreenda as diferenças operacionais de cada modelo:

| Critério de Avaliação | Swarms Locais / `delegate_task` | APIs REST Tradicionais / Webhooks | Protocolo A2A (Agent-to-Agent) |
| :--- | :--- | :--- | :--- |
| **Alcance Geográfico** | Apenas a mesma máquina física ou contêiner local | Qualquer servidor na nuvem | **Totalmente distribuído (Desktop, Nuvem, Servidores Locais e B2B)** |
| **Flexibilidade de Entrada** | Depende de funções internas em Python/TypeScript | Esquemas JSON rígidos; quebra com mudanças de campos | **Conversacional e orientado a objetivos (Goal-Driven)** |
| **Descoberta de Habilidades** | Estática (definida no código fonte) | Manual (desenvolvedores precisam ler documentações Swagger) | **Dinâmica e autônoma via `agent-card.json`** |
| **Isolamento de Credenciais** | Baixo: agentes costumam compartilhar variáveis de ambiente | Alto: restrito aos endpoints da API | **Máximo: cada agente retém suas próprias credenciais em bunkers locais** |
| **Interoperabilidade de Stacks** | Restrito ao framework utilizado (ex: só Hermes ou só LangChain) | Universal entre sistemas de software | **Universal entre frameworks de IA agêntica via padrão aberto Linux Foundation** |
| **Proteção Contra Loops** | Depende do timeout do loop pai | Risco de loop infinito se não houver idempotência | **Travas nativas anti-ping-pong integradas (`A2A_MAX_PINGPONG_TURNS`)** |

---

## O Toolset A2A no Hermes Agent: Comandos e Operações Práticas

No Hermes Agent, utilizar o protocolo A2A é tão simples quanto interagir com qualquer outra ferramenta do sistema operacional. As ferramentas são ativadas por plataforma ou sessão com o comando:

```bash
hermes tools enable a2a --platform cli
```

Com o toolset ativo, o agente ganha superpoderes de rede:

* **`a2a_discover(url)`**: Acessa a URL remota de um parceiro ou filial, inspeciona o Agent Card e gera um sumário executivo das capacidades que aquele agente oferece.
* **`a2a_call(agent, message, context_id)`**: Dispara uma missão para o agente indicado (usando o alias configurado ou uma URL direta) e recupera o resultado processado.
* **`a2a_list()`**: Exibe o mapa de todos os agentes parceiros conhecidos, métricas de tempo de resposta e conversações salvas.
* **`a2a_history(context_id)`**: Recupera o histórico completo de uma negociação ou tarefa técnica realizada anteriormente com outro agente.
* **`a2a_orchestrate(capability, message, mode)`**: Permite a um agente maestro enviar uma tarefa para todos os agentes da sua rede que anunciem uma determinada especialidade. Os modos suportados são:
  * `first`: Aceita a primeira resposta válida entregue;
  * `best`: Avalia as respostas recebidas e seleciona a mais completa e embasada;
  * `all`: Consolida e sintetiza as respostas de todos os nós em um único relatório executivo.

### Configuração Elegante no `config.yaml`

Para que os agentes se comuniquem com facilidade, você pode registrar seus parceiros de confiança diretamente no arquivo de configuração do Hermes:

```yaml
a2a_agents:
  pesquisador_nuvem:
    url: "https://vps-pesquisa.suaempresa.com.br:9900"
    auth:
      type: bearer
      token: "secret_token_alpha_982"
    timeout: 180
    capabilities: [web_search, extracao_dados, sintese_academica]

  fornecedor_pecas:
    url: "https://agente.fornecedorindustrial.com.br:9900"
    auth:
      type: bearer
      token: "token_b2b_fornecedor_2026"
    timeout: 60
    capabilities: [consulta_estoque, orcamento_automatico]
```

Uma vez configurado, o operador não precisa lembrar de URLs técnicas. Basta solicitar em linguagem natural:  
*\"Peça ao pesquisador_nuvem para fazer uma varredura sobre os novos lançamentos de hardware e consolidar um resumo executivo.\"*  
O Hermes Agent resolve o roteamento, autentica a requisição, envia o payload e traz o retorno formatado.

---

## O Bunker de Segurança A2A: Blindagem Empresarial e Governança

Para empresários seniores, a primeira preocupação diante de qualquer tecnologia de rede é a **segurança da informação**. Colocar um agente conectado à internet não pode significar abrir brechas no servidor corporativo. O Hermes Agent implementa uma estratégia de segurança rigorosa baseada no princípio *Secure by Default*:

```
                                  ESCUDO DO BUNKER A2A
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  1. Restrição de Escuta (Localhost First): Sem token configurado, não abre porta externa│
│  2. Chaves Dedicadas por Par: A2A_PEER_TOKENS="filial_sp:tok1, fornecedor_a:tok2"     │
│  3. Filtro Anti-Prompt Injection: Entradas externas são tratadas como dados não confiáveis│
│  4. Redação Automática de Segredos: Chaves de API e senhas são apagadas das saídas     │
│  5. Trava Anti-Ping-Pong: Limite rígido de turnos para impedir consumo desenfreado     │
│  6. Trilha Imutável de Auditoria: Log estruturado em ~/.hermes/a2a_audit.jsonl         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Vínculo Local Restrito por Padrão:**  
   Se nenhum token de autenticação for configurado, o servidor A2A vincula-se exclusivamente a `127.0.0.1`. A exposição para IPs externos (`0.0.0.0`) é expressamente bloqueada pelo runtime a menos que um mecanismo de autorização Bearer esteja ativo.
2. **Credenciais Granulares por Identidade (`A2A_PEER_TOKENS`):**  
   Em vez de usar uma única senha global para todos os parceiros, o Hermes permite associar um token a cada interlocutor: `A2A_PEER_TOKENS="filial_rj:tok_a81,parceiro_logistica:tok_b92"`. Dessa forma, se a parceria com um fornecedor for encerrada, basta revogar o token correspondente sem impactar a comunicação das filiais.
3. **Isolamento de Intenção e Prevenção de Injeção de Prompt:**  
   As mensagens enviadas por agentes externos são encapsuladas e rotuladas internamente como **untrusted peer input** (conteúdo externo não-confiável). Um agente externo não tem permissão para emitir comandos privilegiados de sistema (`/slash commands`, alteração de permissões ou comandos destrutivos de terminal) no seu servidor.
4. **Redação Ativa de Dados Sensíveis (Outbound Redaction):**  
   Antes de despachar qualquer resposta de volta ao solicitante, o motor do Hermes analisa o texto à procura de strings com padrões de chaves criptográficas, tokens JWT ou senhas de banco de dados, substituindo-os por marcadores de redação para evitar vazamentos acidentais.
5. **Proteção Anti-Looping (Ping-Pong Cap):**  
   Um risco real em redes de IA autônomas é dois agentes entrarem em um ciclo infinito de agradecimentos ou pedidos de detalhamento (*\"Obrigado!\" -> \"Eu que agradeço, precisa de algo mais?\" -> \"Estou satisfeito, e você?\"*), esgotando créditos de API. O parâmetro `A2A_MAX_PINGPONG_TURNS` impõe um teto estrito (padrão de 5 turnos por contexto), encerrando o diálogo com segurança.
6. **Auditoria Forense Transparente:**  
   Todas as mensagens recebidas, respostas enviadas, tokens utilizados e tempos de execução são gravados de forma incremental em `~/.hermes/a2a_audit.jsonl`, fornecendo aos diretores compliance total sobre o tráfego agêntico.

---

## 3 Casos de Uso Reais para Reduzir Custos e Otimizar Operações

### Caso 1: A Ponte Desktop-VPS (Offloading de Tarefas Pesadas)
**O Cenário:** Você está em trânsito com um notebook ultrafino em uma reunião de negócios e precisa de uma pesquisa abrangente de mercado com extração de dezenas de páginas da web e compilação de gráficos.  
**A Solução A2A:** Em vez de drenar a bateria e a memória do seu laptop rodando processos locais, seu Hermes Desktop dispara uma chamada `a2a_call` para o Hermes Agent rodando na sua VPS Linux Hostinger de 8 núcleos. A VPS processa a demanda em segundo plano na nuvem e entrega o relatório consolidado pronto no seu aplicativo em poucos minutos.

### Caso 2: Cotação e Pedidos B2B Sem Fricção Humana
**O Cenário:** Uma distribuidora de autopeças recebe dezenas de pedidos de cotação por dia via e-mail e planilhas, gastando horas de funcionários apenas consultando tabelas de preços e prazos de transporte.  
**A Solução A2A:** O agente de compras da oficina cliente conecta-se ao agente da distribuidora via A2A. O agente da oficina envia a lista de peças desejadas; o agente da distribuidora confere o estoque no ERP via MCP, aplica a tabela de desconto negociada e retorna um orçamento oficial assinado digitalmente em menos de 10 segundos, liberando a equipe comercial para focar em relacionamento de alto valor.

### Caso 3: Federação Departamental em Empresas Consolidadas
**O Cenário:** O departamento comercial precisa confirmar se um cliente está inadimplente antes de liberar um novo pedido de grande porte, mas a diretoria não permite que os vendedores acessem o banco de dados bancário ou as telas confidenciais do setor financeiro.  
**A Solução A2A:** O agente comercial pergunta ao agente financeiro via A2A: *\"O cliente CNPJ XX.XXX.XXX/0001-XX possui restrições para compras faturadas em R$ 50.000?\"*. O agente financeiro consulta o banco em seu ambiente isolado e responde apenas: *\"Status: Aprovado. Limite de crédito disponível de R$ 85.000\"*. Os dados sensíveis permanecem restritos ao bunker financeiro, enquanto a operação comercial flui sem gargalos.

---

## Conclusão: O Próximo Salto da Automação Corporativa

A inteligência artificial agêntica já superou a fase dos brinquedos de chat. A verdadeira revolução que separa negócios eficientes de empresas engessadas é a **capacidade de orquestração autônoma e descentralizada**.

O **Protocolo A2A** não é apenas uma conveniência para desenvolvedores: ele é a infraestrutura que viabiliza a criação de ecossistemas empresariais dinâmicos, onde sistemas conversam com sistemas, departamentos operam de forma sinérgica e transações comerciais ocorrem com a velocidade do código e a segurança da criptografia moderna.

No curso **Inteligência Agêntica**, ensinamos exatamente como construir, proteger e governar essa infraestrutura no mundo real: desde a montagem do seu primeiro agente em VPS até a orquestração de redes federadas de inteligência autônoma.

Para aprofundar seu conhecimento e dominar a implementação prática de agentes autônomos soberanos, acompanhe nossos conteúdos e participe da comunidade oficial:  
👉 **[Conheça a Formação Inteligência Agêntica](https://inteligenciaagentica.com.br)**
