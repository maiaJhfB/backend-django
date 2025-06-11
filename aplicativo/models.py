# aplicativo/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    bio = models.TextField("Bio do artista", blank=True, null=True, help_text="Uma breve descrição sobre o artista e seu estilo.")
    foto_perfil = models.ImageField("Foto de Perfil", upload_to='artistas_fotos/', blank=True, null=True, help_text="Foto de perfil do artista.")

    def __str__(self):
        return f"{self.primeiro_nome} {self.sobre_nome} - {self.nome_estudio}"

class Conversa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversas_iniciadas')
    artista = models.ForeignKey(CadastroTatuador, on_delete=models.CASCADE, related_name='conversas_recebidas')
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'artista')

    def __str__(self):
        return f"Conversa entre {self.usuario.username} e {self.artista.primeiro_nome} {self.artista.sobre_nome}"

# --- AQUI ESTÁ A MUDANÇA PRINCIPAL ---
class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens', null=True, blank=True)
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas', null=True, blank=True)
    texto = models.TextField(blank=True, null=True)  # MUDANÇA: permite que o texto seja nulo
    imagem_proposta = models.ImageField(upload_to='propostas/', blank=True, null=True) # MUDANÇA: adiciona o campo de imagem
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.imagem_proposta:
            return f"Proposta de imagem de {self.remetente.username}"
        return f"{self.remetente.username}: {self.texto[:30]}..."