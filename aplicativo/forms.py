from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mensagem, PerfilUsuario, Conversa, CadastroTatuador # Import new models

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome de usuário", max_length=150)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

class CadastroUsuarioForm(UserCreationForm):
    primeiro_nome = forms.CharField(label="Seu primeiro nome", max_length=50)
    sobre_nome = forms.CharField(label="Seu sobrenome", max_length=50)
    email = forms.EmailField(label="Seu email", max_length=250)
    
    class Meta:
        model = User
        fields = ['username', 'primeiro_nome', 'sobre_nome', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                usuario=user,
                primeiro_nome=self.cleaned_data['primeiro_nome'],
                sobre_nome=self.cleaned_data['sobre_nome']
            )
        return user

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['texto'] # 'conversa' and 'remetente' will be set in the view
        widgets = {
            'texto': forms.TextInput(attrs={'placeholder': 'Digite sua mensagem...'}),
        }