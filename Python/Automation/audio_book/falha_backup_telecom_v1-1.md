# Falha de Backup Telecom | Documentação da solução — V1

**Referência operacional:** KB0129466  
**Plataforma:** Ansible Automation Platform (AAP)  
**Status:** MVP de diagnóstico validado em testes; fluxo completo em desenvolvimento  
**Atualização:** 30/10/2026

## 1. Resumo da solução

Automação incremental para apoiar o tratamento de incidentes de **Falha de Backup Telecom**, originados no ItaúMon e acompanhados no ServiceNow. O objetivo final é identificar a causa, executar somente ações previamente autorizadas, validar um novo backup no ItaúMon e registrar a tratativa no ServiceNow. A **V1** concentra-se no diagnóstico não invasivo dos pré-requisitos de SCP em equipamentos Cisco IOS e Cisco ASA, com execução orquestrada pelo AAP.

## 2. Estado atual — V1

- Workflow `WT-TELECOM-FALHA-BACKUP-MVP` estruturado com etapa inicial, identificação/roteamento por plataforma e Jobs de diagnóstico separados para IOS e ASA.
- Identificação de plataforma e encaminhamento para o diagnóstico correspondente testados; os dois caminhos não devem executar o diagnóstico do outro fabricante.
- Execution Environment preparado com as dependências necessárias para os módulos de rede; testes posteriores executaram os Jobs IOS e ASA com **status Success**.
- Consultas de leitura ao equipamento realizadas e resultados publicados em `backup_check_result` no Artifact Store do AAP.
- Cenários observados: **IOS com SCP habilitado** e **ASA com SCP não identificado como habilitado**, conforme as respostas dos comandos nos testes.
- **Limitação conhecida:** um Job com status `Success` indica que o playbook concluiu, não que o backup tenha sido realizado ou que todos os pré-requisitos estejam corretos. A V1 não executa correções, novo backup ou encerramento de incidente.

## 3. Escopo do desenvolvimento

**Entregue nesta V1:** orquestração no AAP; identificação e roteamento IOS/ASA; conectividade com os dispositivos de teste; consulta de configuração SCP; coleta complementar de versão; classificação inicial do SCP; retorno estruturado e publicação de artifacts.

**Evolução gradual:** validação de mudanças recentes de Telecom; verificação do método de autenticação no ItaúMon; ampliação de plataformas (por exemplo, NX-OS e Huawei); avaliação real de armazenamento/flash; aprimoramento das classificações e exceções; integração ItaúMon/ServiceNow; remediações somente com autorização; disparo e confirmação de novo backup; atualização/encerramento condicionado a evidências.

**Sequência operacional:** a KB orienta investigar primeiro mudanças Telecom, depois autenticação no ItaúMon e então SCP. O SCP foi implementado primeiro porque já havia alcance dos equipamentos via inventário e era possível validar rapidamente o diagnóstico. **A implementação incremental não altera a ordem-alvo do fluxo operacional**, que será reorganizada conforme as integrações forem incorporadas.

## 4. Fluxo do workflow no AAP

```text
Entrada manual / parâmetros do Job (V1)
              |
              v
JT-TELECOM-BACKUP-START
  identifica plataforma e publica dados de roteamento
              |
              v
     Roteamento por plataforma
         /             \
   Cisco IOS          Cisco ASA
       |                 |
Diagnóstico IOS     Diagnóstico ASA
       |                 |
Consulta SCP        Consulta SCP
+ consulta versão   + consulta versão
       |                 |
       +--------+--------+
                v
     backup_check_result
     Artifact Store / output
```

**Componentes de referência:** `playbooks/validate-backup/backup_start.yml`, `backup_route.yml` (roteamento), `cisco_ios_check.yml` e `cisco_asa_check.yml`. Os Jobs de roteamento são utilizados para selecionar o ramo adequado no AAP. O desenho final com ItaúMon e ServiceNow permanece pendente de integração.

## 5. Contrato de entrada e saída

### Entrada — parâmetros observados na V1

| Campo | Finalidade |
|---|---|
| `target_host` | Hostname do equipamento alvo, existente no inventário AAP. |
| `ansible_port` | Porta de conexão SSH (nos testes, `22`). |
| `incident_number` | Identificador opcional do incidente; ainda não integrado automaticamente. |

O workflow também propaga internamente `platform` (`cisco_ios` ou `cisco_asa`) e `routing_status` (ex.: `identified`) para selecionar o diagnóstico. Inventário, credencial e Execution Environment são configurados nos Job Templates.

### Saída — artifact `backup_check_result`

| Campo | Significado |
|---|---|
| `host`, `platform` | Equipamento e plataforma diagnosticados. |
| `connection_status` | Resultado da conexão/execução reportado pelo playbook. |
| `diagnostic_status` | Classificação inicial, como `scp_enabled`, `scp_disabled` ou `execution_failed`. |
| `scp_enabled` | Indicador calculado a partir do retorno do comando SCP. |
| `scp_command_output` | Evidência bruta da consulta SCP. |
| `flash_output`, `flash_status` | Saída da consulta complementar; avaliação real de espaço **não implementada** (`not_evaluated`). |
| `backup_status` | Na V1, `not_checked`: não foi solicitado nem validado novo backup. |
| `incident_number` | Referência opcional para futura integração ServiceNow. |
| `error` | Mensagem de erro, quando capturada pelo tratamento de exceções. |

O artifact é publicado com `ansible.builtin.set_stats` (`per_host: false`) e exibido no output do Job. **Não usar `scp_disabled` como prova definitiva quando o dispositivo rejeitar o comando:** essa distinção é uma melhoria prevista.

## 6. Registro do progresso

| Período | Evolução | Situação |
|---|---|---|
| Últimas duas semanas de outubro/2026 | Estruturação do MVP, Jobs e workflow AAP; descoberta do roteamento IOS/ASA e correção do disparo indevido dos dois ramos. | Concluído para V1 |
| Últimas duas semanas de outubro/2026 | Ajustes de Execution Environment e dependências de rede; superação dos erros iniciais de execução. | Concluído para V1 |
| 29–30/10/2026 | Adequação das consultas aos comandos da KB, correções no playbook e testes de diagnóstico com retorno estruturado para IOS e ASA. | Validado nos equipamentos testados |
| Próximas iterações | Integrações ItaúMon/ServiceNow, sequência completa da KB, verificações adicionais e regras de decisão/encerramento. | Pendente |

**Marco da V1:** a automação já identifica a plataforma, executa o diagnóstico de SCP no caminho correspondente e devolve evidências estruturadas. Ainda **não automatiza a resolução integral** do incidente de Falha de Backup.
