# aplicativo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # REMOVA OU COMENTE ESTA LINHA:
    # path("", views.index, name="index"),

    path('cadastro/', views.cadastrar_pessoa, name='cadastro'),
    path('user-preview/', views.user_preview, name='user_preview'),
    path('user/', views.sucesso, name='sucesso'),
    path('editar-nome/', views.editar_nome, name='editar_nome'),
    
    # Updated chat URLs
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:artista_id>/', views.chat_view, name='chat_com_artista'),
    
    path('carol/', views.carol_view, name='carol'),
    path('lucas/', views.lucas_view, name='lucas'),
    path('natalia/', views.natalia_view, name='natalia'),
    path('artistas/', views.artistas_view, name='artistas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('termos/', views.termos_view, name='termos'),
]