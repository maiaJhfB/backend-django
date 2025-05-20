from django.urls import path
from django.shortcuts import render
from . import views

urlspatterns = [
    path("",views.index, name="index"),
    path('cadastro/', views.cadastrar_pessoa, name='cadastrar_pessoa'),
    path('sucesso/', lambda request: render(request, 'sucesso.html'), name='sucesso'),
    path('chat/', views.chat_view, name='chat'),
    path('')
    
]