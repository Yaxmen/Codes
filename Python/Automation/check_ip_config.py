import subprocess

def check_ip_config():
    try:
        # Verifica o arquivo de configuração de rede no Ubuntu/Debian
        with open('/etc/network/interfaces', 'r') as f:
            config = f.read()
        
        if 'dhcp' in config:
            print("O IP é dinâmico (DHCP).")
        elif 'static' in config:
            print("O IP é estático.")
        else:
            print("Configuração de IP não encontrada.")
    except FileNotFoundError:
        print("Arquivo de configuração de rede não encontrado.")

check_ip_config()