# Projeto NAO - Integração de Páginas HTML com Django

Este documento contém instruções para a execução e manutenção do projeto NAO, que integra páginas HTML ao ecossistema Django.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
projeto/
├── aplicativo/
│   ├── migrations/
│   ├── templates/aplicativo/
│   │   ├── artistas.html
│   │   ├── cadastro_user.html
│   │   ├── carol.html
│   │   ├── chat.html
│   │   ├── index.html
│   │   ├── loggin.html
│   │   ├── lucas.html
│   │   ├── natalia.html
│   │   ├── sucesso_html
│   │   ├── termos_privacidade.html
│   │   └── user_preview.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── projeto/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   └── assets/
│       ├── bootstrap/
│       ├── dropdown/
│       ├── embla/
│       ├── formoid/
│       ├── images/
│       ├── mobirise/
│       ├── smoothscroll/
│       ├── socicon/
│       ├── theme/
│       ├── vimeoplayer/
│       ├── web/
│       └── ytplayer/
└── manage.py
```

## Alterações Realizadas

1. **Correção de Caminhos de Assets**: Todos os arquivos HTML foram atualizados para usar as tags do Django para arquivos estáticos:
   - Adicionado `{% load static %}` no topo de cada arquivo HTML
   - Substituído caminhos relativos como `assets/...` por `{% static 'assets/...' %}`
   - Atualizado links de navegação para usar `{% url 'nome_da_view' %}` em vez de links diretos

2. **Correção do EmailField**: Corrigido o erro no arquivo forms.py, alterando o argumento posicional para nomeado:
   ```python
   # Código com erro:
   email = forms.EmailField("Seu email", max_length=250)
   
   # Código corrigido:
   email = forms.EmailField(label="Seu email", max_length=250)
   ```

3. **Configuração de Arquivos Estáticos**: Configurado o Django para servir arquivos estáticos corretamente:
   - Adicionado configurações em settings.py
   - Criado diretório static/ na raiz do projeto
   - Copiado assets para o diretório static/

4. **Integração de Formulários**: Ajustado os formulários para funcionarem corretamente com o Django:
   - Adicionado {% csrf_token %} nos formulários
   - Configurado campos para corresponder aos modelos

5. **Rotas e Views**: Implementado todas as rotas e views necessárias para as páginas HTML:
   - Corrigido urlpatterns em urls.py
   - Criado views para cada página HTML
   - Implementado lógica para processamento de formulários

## Como Executar o Projeto

1. Descompacte o arquivo zip
2. Navegue até o diretório do projeto: `cd nao/projeto`
3. Execute as migrações:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Inicie o servidor:
   ```
   python manage.py runserver
   ```
5. Acesse: http://127.0.0.1:8000/

## Rotas Disponíveis

- `/` - Página inicial
- `/cadastro/` - Formulário de cadastro
- `/login/` - Página de login
- `/chat/` - Chat com tatuadores
- `/carol/`, `/lucas/`, `/natalia/` - Perfis dos tatuadores
- `/artistas/` - Página de artistas
- `/termos/` - Termos de privacidade
- `/sucesso/` - Visualização de usuário cadastrado

## Observações Importantes

- Todos os arquivos estáticos (CSS, JavaScript, imagens) estão no diretório `static/assets/`
- Os templates HTML estão no diretório `aplicativo/templates/aplicativo/`
- O formulário de cadastro foi ajustado para funcionar corretamente com o Django
- As URLs foram configuradas para usar o sistema de roteamento do Django

#Informações sobre o loggin
- A operação do loggin é o resultado do conjunto de quatro instancias
#1 - No html(loggin.html), onde houveram mudanças na pagina para que ela referencie a url do django e eantão fosse integrada ao ecossistema
#2 = No arquivo forms, onde a função LoginForm, serã a responsçável por efetivamente requisitar e extrais os dados
#3- No arquivo views, que será responsssável por, puxar a função de requisição do forms, fazer o tratamento e autenticação dos dados, e por fim puxar a função de loggin do django, reponsçável por manter o cadastro ativo durante a navegação do usuário

