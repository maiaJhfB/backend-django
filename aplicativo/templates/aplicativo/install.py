import sys
import os
import venv
import subprocess

# pra configurar
python_certo = (3, 12)
nome_do_venv = "venv"
arquivo_req = "requirements.txt"

def checa_python():
    print("vendo a versao do python...")
    versao_atual = sys.version_info
    if not (versao_atual.major == python_certo[0] and versao_atual.minor == python_certo[1]):
        print(f"ih, seu python ta zuado. preciso do {python_certo[0]}.{python_certo[1]}.")
        sys.exit(1)
    print("python ta ok.")

def cria_venv():
    print("criando o venv...")
    if os.path.exists(nome_do_venv):
        print("venv ja existe. pulando.")
        return
    try:
        venv.create(nome_do_venv, with_pip=True)
        print("venv criado.")
    except Exception:
        print("deu ruim pra criar o venv.")
        sys.exit(1)

def pega_executavel(nome):
    # ajeita o caminho pra windows, linux ou mac
    if sys.platform == "win32":
        return os.path.join(nome_do_venv, "scripts", f"{nome}.exe")
    else: # pra linux e mac
        return os.path.join(nome_do_venv, "bin", nome)

def instala_os_trecos():
    print("instalando os trecos do requirements...")
    if not os.path.exists(arquivo_req):
        print(f"cade o {arquivo_req}?")
        sys.exit(1)
    
    pip = pega_executavel("pip")
    try:
        subprocess.run([pip, "install", "-r", arquivo_req], check=True)
        print("trecos instalados.")
    except Exception:
        print("falhou pra instalar os trecos.")
        sys.exit(1)

def roda_migrations():
    print("ajeitando o banco de dados...")
    python = pega_executavel("python")
    try:
        subprocess.run([python, "manage.py", "migrate"], check=True)
        print("banco de dados ok.")
    except Exception:
        print("deu ruim nas migrations.")
        sys.exit(1)

# aqui a magica acontece
# checa_python() # deixei comentado como no original
cria_venv()
instala_os_trecos()
roda_migrations()

print("\n--------------------------------")
print("tudo pronto.")
print("pra rodar, faz assim:")
if sys.platform == "win32":
    print("\nno windows:")
    print(f".\\{nome_do_venv}\\scripts\\activate")
    print("python manage.py runserver")
    print("ou so roda o run.py..")

elif sys.platform == "darwin": # macOS é 'darwin'
    print("\nno mac:")
    print(f"bash")
    print(f"source {nome_do_venv}/bin/activate")
    print("python manage.py runserver")
    print("ou so roda o run.py..")

else: # linux
    print("\nno linux:")
    print(f"bash")
    print(f"source {nome_do_venv}/bin/activate")
    print("python manage.py runserver")
    print("ou so roda o run.py..")

print("--------------------------------")