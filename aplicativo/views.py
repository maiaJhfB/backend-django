# aplicativo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import PerfilUsuario, CadastroTatuador, Mensagem, Conversa
from .forms import MensagemForm, CadastroUsuarioForm, LoginForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
import subprocess

def is_artist_check(user):
    return hasattr(user, 'tatuador') and user.tatuador is not None

# Create your views here.

def index(request):
    return render(request, 'aplicativo/index.html')

def cadastrar_pessoa(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            login(request, user)  # Faz login automático após cadastro
            return redirect('user_preview')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'aplicativo/cadastro_user.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('user_preview')
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = LoginForm()
    
    return render(request, 'aplicativo/loggin.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def chat_view(request, artista_id=None):
    # Esta view é para a interface do CLIENTE
    user = request.user
    
    # Redireciona artista para sua própria interface de chat
    if is_artist_check(user):
        return redirect('artist_chats_list')

    conversas_do_usuario = Conversa.objects.filter(usuario=user).order_by('-ultima_atualizacao')
    
    artista_selecionado = None
    mensagens = []
    current_conversa = None
    
    if artista_id:
        artista_selecionado = get_object_or_404(CadastroTatuador, id=artista_id)
        current_conversa, created = Conversa.objects.get_or_create(
            usuario=user,
            artista=artista_selecionado
        )
        mensagens = Mensagem.objects.filter(conversa=current_conversa).order_by('timestamp')

    if request.method == "POST" and current_conversa: # Só permite enviar se uma conversa está selecionada
        form = MensagemForm(request.POST)
        if form.is_valid():
            nova_msg = form.save(commit=False)
            nova_msg.conversa = current_conversa
            nova_msg.remetente = user # O remetente é o cliente logado
            nova_msg.save()
            current_conversa.ultima_atualizacao = timezone.now()
            return redirect('chat_com_artista', artista_id=artista_id)
    else:
        form = MensagemForm()

    return render(request, 'aplicativo/chat.html', {
        'conversas_do_usuario': conversas_do_usuario,
        'artista_selecionado': artista_selecionado,
        'mensagens': mensagens,
        'form': form,
        'current_user_id': user.id,
        'is_artist': False # Passa a flag para o template
    })

# --- NOVAS VIEWS PARA A INTERFACE DO TATUADOR ---

@login_required
@user_passes_test(is_artist_check, login_url='/login/') # Redireciona se não for artista
def artist_chats_list(request):
    # Esta view lista TODAS as conversas que este artista tem
    user = request.user
    tatuador_perfil = get_object_or_404(CadastroTatuador, usuario=user)
    
    conversas_do_artista = Conversa.objects.filter(artista=tatuador_perfil).order_by('-ultima_atualizacao')
    
    return render(request, 'aplicativo/artist_chats_list.html', {
        'conversas_do_artista': conversas_do_artista,
        'is_artist': True
    })

# aplicativo/views.py

# aplicativo/views.py

# aplicativo/views.py

@login_required
@user_passes_test(is_artist_check, login_url='/login/')
def artist_chat_detail(request, conversa_id):
    user = request.user
    tatuador_perfil = get_object_or_404(CadastroTatuador, usuario=user)
    current_conversa = get_object_or_404(Conversa, id=conversa_id, artista=tatuador_perfil)
    conversas_do_artista = Conversa.objects.filter(artista=tatuador_perfil).order_by('-ultima_atualizacao')
    cliente_chat = current_conversa.usuario
    mensagens = Mensagem.objects.filter(conversa=current_conversa).order_by('timestamp')
    form = MensagemForm()

    if request.method == "POST":
        # Checa se o botão de proposta de teste foi clicado
        if 'action' in request.POST and request.POST['action'] == 'test_proposal':
            Mensagem.objects.create(
                conversa=current_conversa,
                remetente=user,
                imagem_proposta='propostas/tattoo.jpeg' # Usa o caminho da imagem estática
            )
        
        # Se não, trata como texto normal
        else:
            texto_enviado = request.POST.get('texto', '').strip()
            if texto_enviado:
                Mensagem.objects.create(
                    conversa=current_conversa,
                    remetente=user,
                    texto=texto_enviado
                )

        current_conversa.ultima_atualizacao = timezone.now()
        current_conversa.save()
        return redirect('artist_chat_detail', conversa_id=conversa_id)
            
    context = {
        'conversas_do_artista': conversas_do_artista,
        'cliente_chat': cliente_chat,
        'mensagens': mensagens,
        'form': form,
        'current_user_id': user.id,
        'active_chat_id': conversa_id,
    }
    return render(request, 'aplicativo/artist_chat_detail.html', context)

def carol_view(request):
    return render(request, 'aplicativo/carol.html')

def lucas_view(request):
    return render(request, 'aplicativo/lucas.html')

def natalia_view(request):
    return render(request, 'aplicativo/natalia.html')

def artistas_view(request):
    artistas = CadastroTatuador.objects.all() # Fetch all artists
    return render(request, 'aplicativo/artistas.html', {'artistas': artistas})

def termos_view(request):
    return render(request, 'aplicativo/termos_privacidade.html')

def sucesso(request):
    return render(request, 'sucesso.html')

class EditarNomeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

@login_required
def editar_nome(request):
    if request.method == 'POST':
        form = EditarNomeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_preview')  # redireciona para a página do perfil
    else:
        form = EditarNomeForm(instance=request.user)
    
    return render(request, 'aplicativo/editar_nome.html', {'form': form})

@login_required
def user_preview(request):
    return render(request, 'aplicativo/user_preview.html', {
        'usuario': request.user  # envia o usuário logado com o nome atualizado
    })

def executar_comando(request):
    mensagem = ""
    if request.method == 'POST':
        comando = [
            'python3',
            'main.py',
            '--mode', 'webcam',
            '--tattoo', '/Users/marcoscheder/Documents/GitHub/mds/rosa.jpg'
        ]
        try:
            subprocess.Popen(comando)
            mensagem = "Comando iniciado com sucesso!"
        except Exception as e:
            mensagem = f"Erro ao executar: {e}"
    return render(request, 'aplicativo/rodar_script.html', {'mensagem': mensagem})