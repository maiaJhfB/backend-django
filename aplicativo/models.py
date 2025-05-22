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

class Mensagem(models.Model):
    autor = models.CharField(max_length=20)  # "cliente" ou "tatuador"
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.autor}: {self.texto[:30]}..."