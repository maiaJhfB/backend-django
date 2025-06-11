import sys
import os
import subprocess

# pra configurar
nome_do_venv = "venv" # tem que ser o mesmo nome que ta no install.py

def pega_executavel(nome):
    # ajeita o caminho pra windows, linux ou mac
    if sys.platform == "win32":
        return os.path.join(nome_do_venv, "scripts", f"{nome}.exe")
    else: # pra linux e mac
        return os.path.join(nome_do_venv, "bin", nome)

def roda_o_servidor():
    print("mandando o servidor do Django rodar...")
    python = pega_executavel("python")
    try:
        # Popen é pra conseguir parar com Ctrl+C depois
        processo = subprocess.Popen([python, "manage.py", "runserver"])
        processo.wait() # espera o bicho terminar (quando o usuario da um Ctrl+C)
    except KeyboardInterrupt:
        print("\nservidor parou, vlw flw.")
    except Exception as e:
        print(f"ixi, deu ruim pra rodar o servidor: {e}")
        sys.exit(1)

# aqui a magica acontece
if __name__ == "__main__":
    # garante que o script ta no lugar certo
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    roda_o_servidor()