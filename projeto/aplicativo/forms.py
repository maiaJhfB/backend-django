from django import forms
from .models import Mensagem

class Name_cadastroForm(forms.Form):
    nome = forms.CharField(label="Your name", max_length=100)

class Senha_cadastroForm(forms.Form):
    senha = forms.CharField(label="Your name", max_length=100)

class Email_cadastroForm(forms.Form):
    email = forms.EmailField("Seu email", max_length=250)

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['autor', 'texto']
        widgets = {
            'texto': forms.TextInput(attrs={'placeholder': 'Digite sua mensagem...'}),
            'autor': forms.HiddenInput(),
        }
        
