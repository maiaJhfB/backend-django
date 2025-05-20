from django.shortcuts import render, redirect
from .models import CadastroUser
from .models import Mensagem
from .forms import MensagemForm

# Create your views here.

def cadastrar_pessoa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        pessoa = CadastroUser(nome=nome, email=email)
        pessoa.save()  # salva no banco de dados

        return redirect('sucesso')  # redireciona para outra página

    return render(request, 'cadastro_user.html')

def chat_view(request):
    mensagens = Mensagem.objects.order_by('timestamp')
    
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')
    else:
        form = MensagemForm(initial={'autor': 'cliente'})  # ou 'tatuador'

    return render(request, 'chat.html', {
        'mensagens': mensagens,
        'form': form,
        'contato_nome': 'Maria Clara',  # opcional: pode ser dinâmico
    })