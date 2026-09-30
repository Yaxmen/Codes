# Assessment e Roadmap das Automações Telecom

## 1. Contexto

Este documento consolida o diagnóstico inicial das automações
relacionadas ao domínio de **Telecom / Links com Falha**, com foco em
entender a arquitetura atual, identificar oportunidades de melhoria e
estabelecer um método de priorização para evolução dos fluxos.

O levantamento inicial indica um cenário híbrido:

-   parte das automações está implementada no **ServiceNow Flow
    Designer**;
-   automações como **BADLINK** e **High CPU/Memory** possuem execução
    no **AAP / Ansible Automation Platform**;
-   existem relações entre diferentes tipos de eventos e a categoria
    agregadora **Links com Falha** que ainda precisam ser detalhadas;
-   alguns fluxos apresentam falhas, demora de execução ou necessidade
    de atuação manual da operação.

> **Importante:** neste momento, o objetivo não é assumir que os fluxos
> do ServiceNow devem ser migrados para Ansible. A arquitetura alvo
> deverá ser consequência do assessment técnico e operacional.

------------------------------------------------------------------------

## 2. Objetivo

O assessment busca responder principalmente às seguintes perguntas:

1.  Quais automações existem atualmente?
2.  Onde cada automação é executada?
3.  Qual evento dispara cada fluxo?
4.  Quais sistemas e equipamentos participam da execução?
5.  Quais automações dependem de outras automações ou eventos?
6.  Onde estão os principais pontos de falha?
7.  Quais etapas ainda exigem intervenção manual?
8.  Qual é o tempo e esforço operacional associado a cada fluxo?
9.  O que deve permanecer no ServiceNow?
10. O que faz sentido executar no AAP?
11. Quais fluxos podem operar em modelo híbrido?
12. Quais oportunidades devem ser priorizadas?

------------------------------------------------------------------------

## 3. Cenário atual

### ServiceNow / Flow Designer

O levantamento inicial indica que a maior parte das automações do
backlog de **Links com Falha** está concentrada no Flow Designer.

Entre os eventos identificados estão, por exemplo:

-   OSPF neighbor state change;
-   OSPF interface state change;
-   equipamento sem resposta / equipamento down;
-   HSRP state changed;
-   BGP neighborship is down;
-   BFD session down;
-   uptime reset occurred;
-   outros eventos relacionados à conectividade.

O detalhamento de cada fluxo ainda precisa ser realizado com os
respectivos owners e com a operação.

### AAP / Ansible

Até o momento foram identificadas automações no Ansible para:

-   BADLINK;
-   High CPU / Memory.

O **BADLINK** está sendo utilizado como primeiro case técnico do
assessment e como referência para definição de padrões que poderão ser
reaproveitados em outros fluxos.

------------------------------------------------------------------------

## 4. Volumetria inicial

A base analisada possui **25.875 registros**.

O Top 10 concentra aproximadamente **67,63%** da base.

  Evento                                               Quantidade   \% da base
  -------------------------------------------------- ------------ ------------
  bad link detected                                         5.446       21,05%
  ospf neighbor state change                                4.373       16,90%
  device has stopped responding - equipamento down          2.584        9,99%
  ospf interface state change                               1.459        5,64%
  ipsla exceeded threshold - packets lost                   1.255        4,85%
  bgp neighborship is down                                    927        3,58%
  hsrp state changed                                          459        1,77%
  interface errors exceeded threshold                         379        1,46%
  jnx ldp lsp down                                            335        1,29%
  uptime reset occurred                                       283        1,09%

Os dois principais eventos, **BADLINK** e **OSPF neighbor state
change**, representam juntos aproximadamente **37,95% da base**.

A volumetria será utilizada como um dos critérios de priorização, mas
**não deverá ser analisada isoladamente**.

------------------------------------------------------------------------

## 5. Hierarquia e dependências

Um dos pontos que ainda precisa ser validado é a relação entre **Links
com Falha** e os diferentes eventos associados.

É necessário distinguir pelo menos três possibilidades:

``` text
Links com Falha
│
├── agrupamento de volumetria
│
├── correlação entre eventos
│
└── dependência técnica entre automações
```

Eventos como BADLINK, OSPF, HSRP, BGP e outros podem contribuir para a
volumetria consolidada da categoria, mas isso não significa
necessariamente que exista dependência técnica entre os respectivos
workflows.

Essa relação deverá ser confirmada durante o discovery.

------------------------------------------------------------------------

## 6. Case inicial: BADLINK

O BADLINK foi escolhido como primeiro fluxo para análise e melhoria.

Fluxo lógico observado:

``` text
Evento BADLINK
      |
      v
Consulta ao Itaumon
      |
      v
Classificação / Elegibilidade
      |
      +-----------------------+
      |                       |
      v                       v
     LAN                     WAN
      |                       |
      v                       v
BADLINK-LAN            tratamento correspondente
      |
      v
Identificação do equipamento
      |
      v
Coleta da interface
      |
      v
Classificação do estado
      |
      v
Decisão sobre o incidente
      |
      v
Atualização do ServiceNow
```

------------------------------------------------------------------------

## 7. Refactor realizado no BADLINK

Até o momento foram trabalhados três pontos principais do fluxo.

### 7.1 Consulta ao Itaumon

A consulta foi organizada para publicar um contrato de saída explícito:

``` yaml
itaumon_link_result:
  registered: true|false
  matched_side: ""
  message: ""
  link: {}
```

Isso reduz dependências implícitas entre etapas e facilita o consumo do
resultado pelos próximos playbooks.

------------------------------------------------------------------------

### 7.2 Elegibilidade BADLINK-LAN

A elegibilidade passou a consumir diretamente o resultado estruturado da
consulta.

Regra atual:

``` text
registered = true
    -> link cadastrado no Itaumon
    -> classificado como WAN
    -> não elegível para BADLINK-LAN

registered = false
    -> link não cadastrado no Itaumon
    -> classificado como LAN
    -> elegível para BADLINK-LAN
```

O resultado também é publicado de forma estruturada:

``` yaml
badlink_lan_eligibility:
  eligible: true|false
  link_type: LAN|WAN
  registered_itaumon: true|false
  reason: "..."
```

------------------------------------------------------------------------

### 7.3 Fluxo BADLINK

O playbook principal foi estruturado para separar:

-   identificação do equipamento;
-   execução do `show interface`;
-   classificação do status;
-   decisão sobre o incidente;
-   tratamento das falhas;
-   publicação do resultado para os próximos nós do workflow.

Também foram introduzidas categorias de falha para melhorar a
rastreabilidade.

Exemplos:

``` text
FALHA_EXECUTION_ENVIRONMENT
COMANDO_SHOW_INTERFACE_INVALIDO
KEY_SSH_INCOMPATIVEL
AUTENTICACAO_SSH_RECUSADA
TIMEOUT_SSH
CONEXAO_SSH_RECUSADA
REDE_INALCANCAVEL
ERRO_HOST_KEY_SSH
FALHA_CONEXAO_SSH
FALHA_VALIDACAO
FALHA_DIAGNOSTICO
```

------------------------------------------------------------------------

## 8. Ganhos obtidos até o momento

O ganho do refactor não deve ser interpretado apenas como redução de
tempo de execução.

O principal ganho atual é **estrutural**.

### Contratos mais claros entre etapas

Consulta, elegibilidade e BADLINK passam a publicar resultados
estruturados, reduzindo dependências implícitas entre os playbooks.

### Melhor rastreabilidade

O workflow consegue informar com maior precisão:

-   onde ocorreu a falha;
-   qual tarefa falhou;
-   qual categoria de erro foi identificada;
-   se houve conexão com o equipamento;
-   qual resultado deve ser utilizado pelos próximos nós.

### Separação entre falha técnica e falha da automação

O fluxo passa a diferenciar problemas como:

``` text
equipamento inacessível
SSH recusado
timeout
problema de autenticação
comando inválido
falha do Execution Environment
falha de diagnóstico
```

Isso evita tratar todos os cenários simplesmente como uma falha genérica
do job.

### Maior previsibilidade

Os próximos nós do workflow recebem contratos conhecidos e podem tomar
decisões de forma mais determinística.

### Base para reutilização

O padrão criado no BADLINK pode ser avaliado como referência para outras
automações Telecom.

------------------------------------------------------------------------

## 9. Arquitetura: princípio de decisão

O assessment não parte da premissa:

``` text
Flow Designer -> migrar tudo -> Ansible
```

A decisão deve ser feita individualmente por fluxo.

Possíveis resultados:

``` text
                     +----------------+
                     | Automação atual |
                     +--------+-------+
                              |
                              v
                      +---------------+
                      |   Assessment  |
                      +-------+-------+
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
          MANTER          REFATORAR         HÍBRIDO
      arquitetura atual   arquitetura atual  SN + AAP
                                               |
                                               v
                                            MIGRAR
                                      quando houver ganho
                                      técnico comprovado
```

------------------------------------------------------------------------

## 10. Critérios de priorização

A volumetria é importante, mas não suficiente.

A priorização deverá considerar:

``` text
PRIORIDADE =
    volumetria
  + esforço manual
  + taxa de falha
  + tempo de resolução
  + impacto operacional
  + potencial de automação
```

Uma automação com menor volumetria pode ter prioridade maior caso
apresente alto esforço manual ou impacto operacional relevante.

------------------------------------------------------------------------

## 11. Roadmap

### Fase 1 --- Discovery

Objetivo: entender o ecossistema atual.

Levantar:

-   eventos;
-   workflows;
-   owners;
-   sistemas envolvidos;
-   equipamentos;
-   entradas;
-   saídas;
-   dependências;
-   ações realizadas;
-   integrações;
-   tratamento de erro;
-   intervenção manual.

**Entregável:** mapa AS-IS das automações Telecom.

------------------------------------------------------------------------

### Fase 2 --- Assessment

Objetivo: identificar gargalos técnicos e operacionais.

Avaliar:

-   taxa de falha;
-   causas das falhas;
-   tempo médio de execução;
-   tempo de tratamento manual;
-   retries;
-   dependências externas;
-   duplicação de lógica;
-   observabilidade;
-   responsabilidade ServiceNow × AAP.

**Entregável:** matriz de problemas e oportunidades.

------------------------------------------------------------------------

### Fase 3 --- Priorização

Cruzar:

-   volumetria;
-   esforço operacional;
-   impacto;
-   taxa de falha;
-   complexidade;
-   potencial de automação.

Classificar os candidatos para evolução.

**Entregável:** backlog priorizado.

------------------------------------------------------------------------

### Fase 4 --- Evolução

Para cada fluxo, decidir entre:

-   manter;
-   refatorar;
-   adotar arquitetura híbrida;
-   migrar.

O BADLINK será utilizado como primeiro case para validar o modelo.

**Entregável:** roadmap técnico de implementação.

------------------------------------------------------------------------

## 12. Próximos passos

### Arquitetura

-   [ ] Mapear ServiceNow Flow Designer × AAP.
-   [ ] Identificar integrações entre as plataformas.
-   [ ] Validar responsabilidades de cada camada.
-   [ ] Entender como os workflows são acionados.
-   [ ] Identificar contratos de entrada e saída.

### Hierarquia

-   [ ] Validar o significado de **Links com Falha**.
-   [ ] Identificar se existe dependência técnica entre os eventos.
-   [ ] Separar correlação, agregação de volumetria e dependência de
    workflow.

### Operação

-   [ ] Identificar owners de cada automação.
-   [ ] Entender o processo manual executado quando a automação falha.
-   [ ] Levantar principais causas de falha.
-   [ ] Levantar tempo gasto pela operação.
-   [ ] Identificar pontos de resistência e limitações conhecidas das
    automações atuais.

### Dados

-   [ ] Cruzar volumetria com taxa de falha.
-   [ ] Cruzar volumetria com esforço manual.
-   [ ] Identificar reincidência de incidentes.
-   [ ] Identificar automações com maior potencial de redução
    operacional.

### BADLINK

-   [x] Estruturar consulta ao Itaumon.
-   [x] Estruturar elegibilidade LAN/WAN.
-   [x] Validar execução isolada.
-   [x] Validar execução dentro do workflow.
-   [x] Melhorar contrato entre etapas.
-   [x] Estruturar tratamento e categorização de falhas.
-   [ ] Consolidar métricas antes/depois.
-   [ ] Validar comportamento com operação.
-   [ ] Utilizar o padrão como referência para o próximo fluxo
    candidato.

------------------------------------------------------------------------

## 13. Matriz de assessment

Para cada automação analisada, registrar:

  Campo               Descrição
  ------------------- ---------------------------------------
  Evento              Evento que origina o incidente
  Categoria           Agrupamento funcional
  Volumetria          Quantidade de incidentes
  Plataforma atual    Flow Designer / AAP / híbrido
  Owner               Responsável atual
  Trigger             Como a automação é iniciada
  Entrada             Dados recebidos
  Ações               Etapas executadas
  Sistemas            Sistemas consultados
  Equipamentos        Tipos/fabricantes envolvidos
  Dependências        Outros workflows ou integrações
  Saída               Resultado produzido
  Taxa de sucesso     Execuções concluídas
  Taxa de falha       Execuções com erro
  Principais falhas   Categorias mais frequentes
  Ação manual         Procedimento da operação
  Tempo manual        Esforço aproximado
  Impacto             Impacto operacional
  Oportunidade        Problema identificado
  Recomendação        Manter / refatorar / híbrido / migrar
  Prioridade          Definida após assessment

------------------------------------------------------------------------

## 14. Visão de evolução

O objetivo final não é simplesmente aumentar a quantidade de automações.

O objetivo é construir um ecossistema no qual as automações Telecom
sejam:

-   previsíveis;
-   observáveis;
-   rastreáveis;
-   resilientes;
-   desacopladas quando possível;
-   reutilizáveis;
-   integradas corretamente ao processo de incidentes;
-   capazes de reduzir efetivamente a intervenção manual.

O BADLINK representa o primeiro passo desse processo e deverá servir
como aprendizado para a evolução das demais oportunidades do backlog.

------------------------------------------------------------------------

## Status

> **Assessment em andamento.**
>
> As informações documentadas representam o entendimento atual e deverão
> ser refinadas conforme o discovery técnico e operacional avançar.
