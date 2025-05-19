from django.db import models

# Create your models here.
class CadastroUser(models.Model):
    primeiro_nome = models.CharField("Seu primeiro nome", max_length=50)
    sobre_nome = models.CharField("Seu sobrenome", max_length=50)
    email = models.EmailField("Seu email", max_length=250)

    def __str__(self):
        return self.user_text

class CadastroTatuador(models.Model):
    primeiro_nome = models.CharField("Seu primeiro nome", max_length=50)
    sobre_nome = models.CharField("Seu sobrenome", max_length=50)
    email = models.EmailField("Seu email", max_length=250)
    nome_estudio = models.CharField("Nome do seu estúdio", max_length=50)

    def __str__(self):
        return self.tatuador_text