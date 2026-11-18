# Validate Connectivity — Agências (AAP)

## Visão geral

Solução de validação operacional de equipamentos de rede cadastrados em inventários do **Ansible Automation Platform (AAP)**. Executa verificações progressivas para identificar em qual etapa um equipamento deixa de estar apto à automação, consolidando o resultado por host em `final_status`.

A implementação utiliza checks desacoplados por plataforma, com orquestração pelo `validate_host.yml` e consolidação pelo `main.yml`. Os resultados são publicados em **CSV** e **dashboard HTML** no Artifact Store, além de um resumo executivo via `set_stats` no AAP.

**Plataformas implementadas e testadas em DEV:** FortiOS, Cisco IOS/IOS-XE (collection `cisco.ios`) e Cisco ASA (collection `cisco.asa`). O suporte a outras famílias Cisco não deve ser presumido pela simples presença de collections no EE.

## Objetivo

Validar, por equipamento:

1. Resolução DNS, quando aplicável.
2. Conectividade TCP com a porta de gerenciamento (normalmente SSH/22).
3. Autenticação e execução de comando remoto, conforme a plataforma.
4. Reachability operacional, entendido aqui como capacidade de executar um comando remoto — **não** como teste ICMP.

As verificações posteriores dependem do sucesso das etapas anteriores, evitando tentativas desnecessárias.

## Estrutura do repositório

```text
playbooks/validate-connectivity/
├── README.md
├── main.yml
├── validate_host.yml
├── checks/
│   ├── check_dns.yml
│   ├── check_dns_cisco.yml
│   ├── check_connectivity.yml
│   ├── check_connectivity_cisco.yml
│   ├── check_authentication_fortinet.yml
│   ├── check_reachability_fortinet.yml
│   ├── check_authentication_cisco.yml
│   └── check_reachability_cisco.yml
└── templates/
    ├── connectivity_results.csv.j2
    └── connectivity_dashboard.html.j2
```

- **`main.yml`**: identifica hosts do inventário, prepara o grupo de execução, consolida resultados e publica os artefatos.
- **`validate_host.yml`**: executa os checks aplicáveis e classifica cada equipamento.
- **`checks/`**: implementações independentes por etapa e plataforma.
- **`templates/`**: geração do CSV detalhado e dashboard HTML.

## Pipeline de validação

```text
Inventário AAP
    │
    ▼
DNS (quando aplicável)
    │
    ▼
Conectividade TCP
    │ CONNECTED
    ▼
Autenticação e comando remoto
    │ AUTHENTICATED
    ▼
Reachability por comando remoto
    │ SUCCESS
    ▼
READY
    │
    ▼
CSV + Dashboard HTML + set_stats
```

### Checks por plataforma

| Etapa | FortiOS | Cisco IOS / IOS-XE | Cisco ASA |
|---|---|---|---|
| DNS | `check_dns.yml` | `check_dns_cisco.yml` | `check_dns_cisco.yml` |
| TCP | `check_connectivity.yml` | `check_connectivity_cisco.yml` | `check_connectivity_cisco.yml` |
| Autenticação | `check_authentication_fortinet.yml` | `check_authentication_cisco.yml` | `check_authentication_cisco.yml` |
| Reachability | `check_reachability_fortinet.yml` | `check_reachability_cisco.yml` | `check_reachability_cisco.yml` |

**FortiOS:** utiliza conexão SSH e o comando `get system status` para confirmar a capacidade de autenticar e executar comandos remotos. O mesmo comando é utilizado no check de reachability da implementação atual.

**Cisco IOS/IOS-XE e ASA:** utilizam `ansible.netcommon.network_cli`, com os módulos `cisco.ios.ios_command` e `cisco.asa.asa_command`, respectivamente. A autenticação é verificada com `show version`; o check de reachability executa comando operacional remoto (na implementação Cisco discutida, `show clock`).

No check de autenticação Cisco, os resultados de ASA e IOS são registrados separadamente em `cisco_asa_auth_probe` e `cisco_ios_auth_probe`. Isso evita que um registro sobrescreva o outro e produza classificação incorreta.

## Pré-requisitos e configuração no AAP

- Inventário com os equipamentos-alvo e endereços resolvíveis ou IPs válidos.
- Job Template apontando para `playbooks/validate-connectivity/main.yml`.
- Execution Environment com os componentes exigidos pelos checks e acesso à rede de gerenciamento.
- Credencial AAP adequada à plataforma e ao método de conexão configurado.
- Instance Group com capacidade de executar o job e alcançar os equipamentos.
- Acesso ao serviço de Artifact Store, conforme a configuração existente do ambiente.

### Execution Environment

O EE de Telecom/Agências foi atualizado para incluir as collections necessárias. Entre as dependências relevantes estão:

```yaml
collections:
  - name: ansible.netcommon
  - name: cisco.ios
  - name: cisco.asa
  - name: fortinet.fortios
```

O build apresentado também inclui `nmap-ncat` (para a validação TCP), `crypto-policies-scripts` e outras collections de suporte. A imagem deve disponibilizar as dependências transitivas exigidas pelas collections instaladas.

**Compatibilidade SSH legada:** o build do EE utiliza:

```dockerfile
RUN update-crypto-policies --set LEGACY
RUN update-crypto-policies --show
```

Essa configuração foi adotada para compatibilidade com algoritmos antigos de equipamentos de rede. **É uma exceção de segurança**, pois amplia a aceitação de algoritmos criptográficos legados. Sua manutenção deve ser avaliada com a equipe responsável pela segurança, preferencialmente com escopo restrito ao EE necessário.

### Inventário Cisco

Exemplo de variáveis para **ASA**:

```yaml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: cisco.asa.asa
ansible_port: 22
```

Para **IOS/IOS-XE**, usar `ansible_network_os: cisco.ios.ios`. As credenciais e permissões precisam permitir o acesso ao equipamento e a execução dos comandos de consulta.

O `target_platform` deve corresponder à plataforma escolhida pelo fluxo ou Job Template (por exemplo, `ASA`, `IOS`, `IOS-XE` ou `FortiOS`), conforme os valores esperados pelo playbook.

## Resultados e classificação

O fluxo registra o estado de cada etapa e produz um status consolidado por equipamento. Entre os estados finais observados estão:

| `final_status` | Significado |
|---|---|
| `READY` | Verificações aplicáveis concluídas com sucesso. |
| `DNS_FAILED` | Falha na resolução DNS. |
| `CONNECTIVITY_TIMEOUT` | Conexão TCP excedeu o tempo limite. |
| `CONNECTION_REFUSED` | Porta de destino recusou a conexão. |
| `AUTHENTICATION_FAILED` | Não foi possível validar a autenticação ou a execução do comando de autenticação. |
| `PING_FAILED` / `REACHABILITY_FAILED` | Falha na etapa de execução remota/reachability, conforme a classificação da versão em uso. |

**Observação:** o nome `PING_FAILED` é legado; o check de reachability atual não representa necessariamente um ping ICMP.

### Artefatos gerados

- **CSV:** resultado detalhado por host, com identificação, plataforma, porta, estados das verificações, classificação final e metadados de execução.
- **Dashboard HTML:** indicadores consolidados, motivos de falha e detalhamento por host, com filtros.
- **`set_stats`:** resumo executivo disponível na execução do AAP.

Os artefatos são publicados no **Artifact Store** configurado para o ambiente.

## Estado atual e próximos passos

- **FortiOS:** checks de DNS, TCP, autenticação SSH e reachability implementados.
- **Cisco IOS/IOS-XE e ASA:** checks integrados e validados funcionalmente em **DEV** após atualização do EE e correção do registro de variáveis da autenticação.
- **Cisco IOS:** execução de referência em DEV com **239 hosts**, dos quais **171 READY (71,5%)**.
- **Cisco ASA:** execução de referência em DEV com **82 hosts**, dos quais **69 READY (84,1%)**.
- **Pendências:** analisar com a equipe responsável os hosts com falha de conectividade, autenticação ou permissão; avaliar o uso da política criptográfica `LEGACY`; e realizar a homologação para produção.

Os resultados de DEV confirmam o funcionamento do fluxo para diversos equipamentos, mas **não significam que todos os hosts com falha apresentem erro no playbook**. As exceções devem ser avaliadas individualmente a partir dos logs e das permissões de acesso.

---

**Uso interno — Itaú Unibanco. Distribuição não autorizada é proibida.**
