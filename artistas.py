# popular_artistas.py
import os
import django

# Configura o ambiente Django para que o script possa acessar os modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()

from django.contrib.auth.models import User
from aplicativo.models import CadastroTatuador
from django.conf import settings # Para acessar MEDIA_ROOT

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
            'nome_estudio': 'Vila Prudente - SP',
            'bio': 'Olá! Sou Nathalia e vivo a arte da tatuagem há 12 anos. Tenho um grande apreço pelos clássicos old schools e pela precisão do realismo.',
            'foto_perfil_filename': 'mbr-815x565.jpg' # Nome do arquivo da imagem
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
            'nome_estudio': 'Vila Prudente - SP',
            'bio': 'Prazer! Sou Carolina, bióloga especializada em biossegurança e sua profissional de piercing de confiança. Priorizo a segurança e a higiene em cada procedimento. Venha fazer seu piercing comigo!',
            'foto_perfil_filename': 'mbr-375x250.jpg' # Nome do arquivo da imagem
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
            'nome_estudio': 'Jardim - Santo André',
            'bio': 'Tatuador com 2 anos de experiência, com foco em traços delicados (fine line) e a rica estética oriental. Convido você a discutir sua próxima tatuagem via chat e conhecer meu portfólio nas redes.',
            'foto_perfil_filename': 'mbr-815x611.jpg' # Nome do arquivo da imagem
        }
    },
]

print("Iniciando população de artistas...")

for data in artistas_data:
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    tatuador_info = data['tatuador_info']
    foto_perfil_filename = tatuador_info.get('foto_perfil_filename', '') # Pega o nome do arquivo da foto

    user, created_user = User.objects.get_or_create(username=username, defaults={'first_name': first_name, 'last_name': last_name, 'email': email})
    
    if created_user:
        user.set_password('senha123')
        user.save()
        print(f"  Usuário '{username}' criado com sucesso.")
    else:
        print(f"  Usuário '{username}' já existe.")

    # Tenta pegar o CadastroTatuador existente ou cria um novo
    tatuador, created_tatuador = CadastroTatuador.objects.get_or_create(
        usuario=user,
        defaults={
            'primeiro_nome': tatuador_info['primeiro_nome'],
            'sobre_nome': tatuador_info['sobre_nome'],
            'email': tatuador_info['email'],
            'nome_estudio': tatuador_info['nome_estudio'],
            'bio': tatuador_info['bio'],
            # Define o caminho da foto relativo ao MEDIA_ROOT/artistas_fotos/
            'foto_perfil': os.path.join('artistas_fotos', foto_perfil_filename) if foto_perfil_filename else ''
        }
    )
    
    if not created_tatuador: # Se o tatuador já existia, atualiza a bio e a foto
        updated = False
        if tatuador.bio != tatuador_info['bio']:
            tatuador.bio = tatuador_info['bio']
            updated = True
        
        # Verifica se o caminho da foto no banco de dados é diferente do que queremos setar
        expected_foto_path = os.path.join('artistas_fotos', foto_perfil_filename) if foto_perfil_filename else ''
        if tatuador.foto_perfil.name != expected_foto_path:
            tatuador.foto_perfil.name = expected_foto_path # Define o novo caminho
            updated = True

        if updated:
            tatuador.save()
            print(f"  CadastroTatuador para '{tatuador.primeiro_nome} {tatuador.sobre_nome}' atualizado.")
        else:
            print(f"  CadastroTatuador para '{tatuador.primeiro_nome} {tatuador.sobre_nome}' já existe e está atualizado.")
    else:
        print(f"  CadastroTatuador para '{tatuador.primeiro_nome} {tatuador.sobre_nome}' criado e vinculado ao usuário '{username}'.")

print("População de artistas concluída.")