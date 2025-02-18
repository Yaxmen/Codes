import subprocess

def check_clamav():
    try:
        # Verifica se o serviço ClamAV está ativo
        result = subprocess.run(['systemctl', 'is-active', 'clamav-daemon'], capture_output=True, text=True)
        
        if result.stdout.strip() == 'active':
            print("O ClamAV está ativo.")
        else:
            print("O ClamAV não está ativo.")
    except FileNotFoundError:
        print("ClamAV não está instalado.")

check_clamav()