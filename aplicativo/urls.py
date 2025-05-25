from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('cadastro/', views.cadastrar_pessoa, name='cadastro'),
    path('user-preview/', views.user_preview, name='user_preview'),
    path('user/', views.sucesso, name='sucesso'),
    path('editar-nome/', views.editar_nome, name='editar_nome'),
    path('chat/', views.chat_view, name='chat'),
    path('carol/', views.carol_view, name='carol'),
    path('lucas/', views.lucas_view, name='lucas'),
    path('natalia/', views.natalia_view, name='natalia'),
    path('artistas/', views.artistas_view, name='artistas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('termos/', views.termos_view, name='termos'),
]