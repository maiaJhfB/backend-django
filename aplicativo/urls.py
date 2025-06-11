from django.urls import path
from . import views


urlpatterns = [
    # path("", views.index, name="index"), # Já deve estar no projeto/urls.py

    path('cadastro/', views.cadastrar_pessoa, name='cadastro'),
    path('user-preview/', views.user_preview, name='user_preview'),
    path('user/', views.sucesso, name='sucesso'),
    path('editar-nome/', views.editar_nome, name='editar_nome'),
    
    # Chat do Cliente (existente)
    path('chat/', views.chat_view, name='chat'), # Lista conversas para o cliente
    path('chat/<int:artista_id>/', views.chat_view, name='chat_com_artista'), # Chat específico do cliente com artista
    
    # NOVAS URLs para o Chat do Tatuador
    path('artist/chats/', views.artist_chats_list, name='artist_chats_list'), # Lista conversas para o tatuador
    path('artist/chat/<int:conversa_id>/', views.artist_chat_detail, name='artist_chat_detail'), # Chat específico do tatuador com cliente
    
    path('carol/', views.carol_view, name='carol'),
    path('lucas/', views.lucas_view, name='lucas'),
    path('natalia/', views.natalia_view, name='natalia'),
    path('artistas/', views.artistas_view, name='artistas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('termos/', views.termos_view, name='termos'),
    path('executar/', views.executar_comando, name='executar_comando'),
]