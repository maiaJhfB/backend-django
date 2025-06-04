from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilUsuario, CadastroTatuador, Mensagem, Conversa # Import Conversa
from .forms import MensagemForm, CadastroUsuarioForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.utils import timezone


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
    user = request.user
    conversas_do_usuario = Conversa.objects.filter(usuario=user).order_by('-ultima_atualizacao')
    
    current_conversa = None
    artista_selecionado = None
    mensagens = []
    
    if artista_id:
        artista_selecionado = get_object_or_404(CadastroTatuador, id=artista_id)
        current_conversa, created = Conversa.objects.get_or_create(
            usuario=user,
            artista=artista_selecionado
        )
        mensagens = Mensagem.objects.filter(conversa=current_conversa).order_by('timestamp')

    if request.method == "POST" and current_conversa: # Only allow sending messages if a chat is selected
        form = MensagemForm(request.POST)
        if form.is_valid():
            nova_msg = form.save(commit=False)
            nova_msg.conversa = current_conversa
            nova_msg.remetente = user # The logged-in user is the sender
            nova_msg.save()
            current_conversa.ultima_atualizacao = timezone.now() # Update conversation timestamp
            current_conversa.save()
            return redirect('chat_com_artista', artista_id=artista_id) # Redirect to the specific chat
    else:
        form = MensagemForm()

    return render(request, 'aplicativo/chat.html', {
    'conversas_do_usuario': conversas_do_usuario,
    'artista_selecionado': artista_selecionado,
    'mensagens': mensagens,
    'form': form,
    'current_user_id': user.id,
})


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
        fields = ['first_name', 'last_name']

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