from django.shortcuts import render
from .models import CadastroUser
# Create your views here.

def index(request):
    return render(request,"aplicativo/index.html")