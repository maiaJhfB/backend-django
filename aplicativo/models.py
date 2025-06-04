# aplicativo/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    primeiro_nome = models.CharField("Seu primeiro nome", max_length=50)
    sobre_nome = models.CharField("Seu sobrenome", max_length=50)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.primeiro_nome} {self.sobre_nome}"

class CadastroTatuador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tatuador', null=True, blank=True)
    primeiro_nome = models.CharField("Seu primeiro nome", max_length=50)
    sobre_nome = models.CharField("Seu sobrenome", max_length=50)
    email = models.EmailField("Seu email", max_length=250)
    nome_estudio = models.CharField("Nome do seu estúdio", max_length=50)

    def __str__(self):
        return f"{self.primeiro_nome} {self.sobre_nome} - {self.nome_estudio}"

# New model for conversations
class Conversa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversas_iniciadas')
    artista = models.ForeignKey(CadastroTatuador, on_delete=models.CASCADE, related_name='conversas_recebidas')
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'artista') # Ensures only one conversation per user-artist pair

    def __str__(self):
        return f"Conversa entre {self.usuario.username} e {self.artista.primeiro_nome} {self.artista.sobre_nome}"

class Mensagem(models.Model):
    # Adicione null=True, blank=True para permitir valores nulos temporariamente
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens', null=True, blank=True)
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas', null=True, blank=True)
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remetente.username}: {self.texto[:30]}..."