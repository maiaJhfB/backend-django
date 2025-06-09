from django.contrib import admin
from .models import PerfilUsuario, CadastroTatuador, Mensagem
# Register your models here.
admin.site.register(PerfilUsuario)
admin.site.register(CadastroTatuador)
admin.site.register(Mensagem)