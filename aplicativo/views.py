from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilUsuario, CadastroTatuador, Mensagem
from .forms import MensagemForm, CadastroUsuarioForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms

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
            return redirect('sucesso')
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
                return redirect('sucesso')
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = LoginForm()
    
    return render(request, 'aplicativo/loggin.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def chat_view(request):
    mensagens = Mensagem.objects.order_by('timestamp')
    
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')
    else:
        form = MensagemForm(initial={'autor': 'cliente'})  # ou 'tatuador'

    return render(request, 'aplicativo/chat.html', {
        'mensagens': mensagens,
        'form': form,
        'contato_nome': 'Maria Clara',  # opcional: pode ser dinâmico
    })

def carol_view(request):
    return render(request, 'aplicativo/carol.html')

def lucas_view(request):
    return render(request, 'aplicativo/lucas.html')

def natalia_view(request):
    return render(request, 'aplicativo/natalia.html')

def artistas_view(request):
    return render(request, 'aplicativo/artistas.html')

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