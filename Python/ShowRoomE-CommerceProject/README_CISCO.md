# Cisco checks — integração inicial

Copie os dois arquivos `.yml` para `playbooks/validate-connectivity/checks/`.

## Inventário de teste (exemplo)

```yaml
all:
  hosts:
    asa_teste:
      ansible_host: 192.0.2.10
      ansible_connection: ansible.netcommon.network_cli
      ansible_network_os: cisco.asa.asa
      ansible_user: usuario
      ansible_port: 22
    ios_teste:
      ansible_host: 192.0.2.11
      ansible_connection: ansible.netcommon.network_cli
      ansible_network_os: cisco.ios.ios
      ansible_user: usuario
      ansible_port: 22
```

Credenciais via AAP Machine credential ou outro mecanismo seguro; não colocar senhas no repositório.

## Chamadas no validate_host.yml

Os exemplos abaixo são trechos a incorporar **após** DNS e conectividade, adaptando aos nomes das variáveis atuais.

```yaml
- name: Cisco | Check authentication
  ansible.builtin.include_tasks:
    file: checks/check_authentication_cisco.yml
  when:
    - dns_status != 'FAILED'
    - connectivity_status == 'SUCCESS'
    - ansible_network_os | default('') in ['cisco.asa.asa', 'cisco.ios.ios']

- name: Cisco | Normalizar authentication
  ansible.builtin.set_fact:
    authentication_status: "{{ check_result.details.authentication_status }}"
    authentication_result: "{{ check_result }}"
  when:
    - dns_status != 'FAILED'
    - connectivity_status == 'SUCCESS'
    - ansible_network_os | default('') in ['cisco.asa.asa', 'cisco.ios.ios']

- name: Cisco | Check reachability
  ansible.builtin.include_tasks:
    file: checks/check_reachability_cisco.yml
  when:
    - authentication_status == 'SUCCESS'
    - ansible_network_os | default('') in ['cisco.asa.asa', 'cisco.ios.ios']

- name: Cisco | Normalizar reachability
  ansible.builtin.set_fact:
    ping_status: "{{ check_result.details.ping_status }}"
    ping_result: "{{ check_result }}"
  when:
    - authentication_status == 'SUCCESS'
    - ansible_network_os | default('') in ['cisco.asa.asa', 'cisco.ios.ios']
```

**Atenção:** os arquivos de check não modificam os dispositivos. O `authentication` usa `show version` como prova de sessão CLI, mas falhas de autorização, prompt, timeout e autenticação podem produzir o mesmo FAILED; inspecione `details.error` antes de classificar a causa definitiva. O `reachability` valida um segundo comando read-only (`show clock`), não ICMP. Em uma etapa futura, alinhar a nomenclatura e classificação ao contrato real dos checks Fortinet.

Collections necessárias no EE: `ansible.netcommon`, `cisco.asa`, `cisco.ios` (e dependências de SSH, normalmente Paramiko ou ansible-pylibssh, conforme a imagem). A execução do inventory source pode usar um EE diferente do Job Template.
