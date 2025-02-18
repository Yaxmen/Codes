import shutil

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    
    print(f"Espaço total: {total // (2**30)} GB")
    print(f"Espaço usado: {used // (2**30)} GB")
    print(f"Espaço livre: {free // (2**30)} GB")

check_disk_space()