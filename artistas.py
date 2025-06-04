# criar_artistas.py
import os
import django

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()

from django.contrib.auth.models import User
from aplicativo.models import CadastroTatuador

artistas_data = [
    {
        'username': 'nathalia_mattar',
        'first_name': 'Nathalia',
        'last_name': 'Mattar',
        'email': 'nathalia.mattar@inketrom.com',
        'tatuador_info': {
            'primeiro_nome': 'Nathalia',
            'sobre_nome': 'Mattar',
            'email': 'nathalia.mattar@inketrom.com',
            'nome_estudio': 'Vila Prudente - SP'
        }
    },
    {
        'username': 'carolina_amaral',
        'first_name': 'Carolina',
        'last_name': 'Amaral',
        'email': 'carolina.amaral@inketrom.com',
        'tatuador_info': {
            'primeiro_nome': 'Carolina',
            'sobre_nome': 'Amaral',
            'email': 'carolina.amaral@inketrom.com',
            'nome_estudio': 'Vila Prudente - SP'
            }
        },
    {
        'username': 'lucas_maciel',
        'first_name': 'Lucas',
        'last_name': 'Maciel',
        'email': 'lucas.maciel@inketrom.com',
        'tatuador_info': {
            'primeiro_nome': 'Lucas',
            'sobre_nome': 'Maciel',
            'email': 'lucas.maciel@inketrom.com',
            'nome_estudio': 'Jardim - Santo André'
        }
    },
]

for data in artistas_data:
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    tatuador_info = data['tatuador_info']

    # Tenta pegar o usuário existente ou cria um novo
    user, created_user = User.objects.get_or_create(username=username, defaults={'first_name': first_name, 'last_name': last_name, 'email': email})

    if created_user:
        user.set_password('senha123') # Defina uma senha padrão (muito simples para teste)
        user.save()
        print(f"Usuário '{username}' criado.")
    else:
        print(f"Usuário '{username}' já existe.")

    # Tenta pegar o CadastroTatuador existente ou cria um novo
    tatuador, created_tatuador = CadastroTatuador.objects.get_or_create(
        usuario=user,
        defaults={
            'primeiro_nome': tatuador_info['primeiro_nome'],
            'sobre_nome': tatuador_info['sobre_nome'],
            'email': tatuador_info['email'],
            'nome_estudio': tatuador_info['nome_estudio']
        }
    )

    if created_tatuador:
        print(f"CadastroTatuador para '{tatuador.primeiro_nome} {tatuador.sobre_nome}' criado e vinculado ao usuário '{username}'.")
    else:
        print(f"CadastroTatuador para '{tatuador.primeiro_nome} {tatuador.sobre_nome}' já existe e está vinculado ao usuário '{username}'.")

print("População de artistas concluída.")