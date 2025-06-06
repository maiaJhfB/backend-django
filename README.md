# Projeto Inketrom - Integração de Páginas HTML com Django

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
-#1 - No html(loggin.html), onde houveram mudanças na pagina para que ela referencie a url do django e eantão fosse integrada ao ecossistema
-#2 - No arquivo forms, onde a função LoginForm, serã a responsçável por efetivamente requisitar e extrais os dados
-#3 - No arquivo views, que será responsssável por, puxar a função de requisição do forms, fazer o tratamento e autenticação dos dados, e por fim puxar a função de loggin do django, reponsçável por manter o cadastro ativo durante a navegação do usuário
-4# - E é claro no model que é onde é instanciado o perfil de usuário no banco de dados, que é conectada com o viws atraves da função save que esta sim se liga diretamente a instancia de usuario no banco de dados localizada no models

