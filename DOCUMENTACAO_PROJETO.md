# Documentação Completa do Projeto InkEtrom

**Versão:** 1.2 (23 de Maio de 2025)

## 1. Introdução

O InkEtrom é uma plataforma web desenvolvida para conectar clientes e tatuadores, oferecendo um ambiente para visualização de portfólios, comunicação e uma ferramenta inovadora de simulação de tatuagens usando realidade aumentada.

Este documento detalha a arquitetura, funcionalidades, tecnologias utilizadas e instruções de uso do projeto até a presente data.

## 2. Arquitetura

O projeto segue uma arquitetura baseada no framework Django para o backend e utiliza HTML, CSS e JavaScript para o frontend. A funcionalidade de simulação de tatuagem emprega tecnologias de visão computacional no lado do cliente (TensorFlow.js, PoseNet) para proporcionar uma experiência interativa.

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Banco de Dados:** SQLite (padrão do Django para desenvolvimento)
- **Visão Computacional (Frontend):** TensorFlow.js, PoseNet
- **Estilização:** Bootstrap (com personalizações)

## 3. Estrutura do Projeto

O código-fonte está organizado da seguinte forma dentro do diretório `/home/ubuntu/nao/`:

```
nao/
├── projeto/                  # Diretório principal do projeto Django
│   ├── aplicativo/           # Aplicação Django principal ("aplicativo")
│   │   ├── migrations/       # Arquivos de migração do banco de dados
│   │   ├── templates/        # Templates HTML específicos da aplicação
│   │   │   └── aplicativo/
│   │   │       ├── *.html    # Arquivos HTML das páginas
│   │   ├── __init__.py
│   │   ├── admin.py          # Configuração do Django Admin
│   │   ├── apps.py
│   │   ├── forms.py          # Formulários Django (Cadastro, Login, etc.)
│   │   ├── models.py         # Modelos do banco de dados (Usuário, Tatuador, etc.)
│   │   ├── tests.py
│   │   ├── urls.py           # URLs específicas da aplicação
│   │   └── views.py          # Lógica de visualização (controllers)
│   ├── projeto/              # Configurações do projeto Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py       # Configurações principais do projeto
│   │   ├── urls.py           # URLs principais do projeto
│   │   └── wsgi.py
│   ├── static/               # Arquivos estáticos (CSS, JS, Imagens)
│   │   ├── assets/
│   │   │   ├── bootstrap/
│   │   │   ├── css/
│   │   │   ├── docs/         # Documentação de funcionalidades específicas
│   │   │   │   ├── tattoo-simulator-advanced-guide.md
│   │   │   │   └── tattoo-simulator-guide.md
│   │   │   ├── images/
│   │   │   │   └── body-parts/ # Imagens para seleção de parte do corpo
│   │   │   ├── js/
│   │   │   │   ├── tattoo-camera.js
│   │   │   │   ├── tattoo-camera-advanced.js
│   │   │   │   ├── tattoo-camera-image2image.js
│   │   │   │   └── tensorflow-models-loader.js
│   │   │   └── ... (outros assets)
│   ├── db.sqlite3            # Banco de dados SQLite
│   └── manage.py             # Utilitário de gerenciamento do Django
├── README.md                 # Instruções básicas e visão geral
└── DOCUMENTACAO_PROJETO.md   # Este arquivo
```

## 4. Funcionalidades Implementadas

### 4.1. Backend (Django)

- **Integração Inicial:** As páginas HTML estáticas originais foram integradas ao sistema de templates do Django.
- **Gerenciamento de URLs:** Rotas definidas em `projeto/urls.py` e `aplicativo/urls.py` para mapear URLs às views correspondentes.
- **Views:** Lógica implementada em `aplicativo/views.py` para renderizar templates, processar formulários e interagir com o banco de dados.
- **Modelos:**
    - `User` (Django Auth): Utilizado para autenticação e gerenciamento básico de usuários.
    - `PerfilUsuario`: Modelo customizado (`aplicativo/models.py`) para armazenar informações adicionais do usuário (vinculado ao `User`).
    - `CadastroTatuador`: Modelo para informações dos tatuadores (atualmente usado para exibir perfis estáticos, pode ser expandido).
- **Formulários:**
    - `UserCreationForm` (Customizado): Para cadastro de novos usuários com validação de senha (`aplicativo/forms.py`).
    - `AuthenticationForm`: Para login de usuários (`aplicativo/forms.py`).
- **Autenticação:** Sistema completo de cadastro, login e logout utilizando o `django.contrib.auth`.
- **Admin:** Interface administrativa do Django (`aplicativo/admin.py`) configurada para gerenciar usuários e perfis.
- **Arquivos Estáticos:** Configuração em `projeto/settings.py` e estrutura em `projeto/static/` para servir CSS, JavaScript e imagens.

### 4.2. Frontend

- **Templates:** Páginas HTML (`aplicativo/templates/aplicativo/`) renderizadas pelo Django, utilizando a linguagem de template do Django (`{% load static %}`, `{% url %}`, etc.).
- **Estilização:** Utilização do framework Bootstrap com personalizações e assets visuais originais mantidos.
- **Páginas Principais:**
    - Index (`index.html`)
    - Cadastro (`cadastro_user.html`)
    - Login (`loggin.html`)
    - Perfis de Tatuadores (`carol.html`, `lucas.html`, `natalia.html`)
    - Página de Artistas (`artistas.html`)
    - Chat (`chat.html` - estrutura básica)
    - Termos de Privacidade (`termos_privacidade.html`)
    - Perfil do Usuário (`user_preview.html` - acessível apenas logado)
- **Navegação Condicional:** O ícone de usuário no cabeçalho redireciona para a página de login se o usuário não estiver autenticado, ou para o perfil (`user_preview.html`) se estiver logado.

### 4.3. Simulador de Tatuagem

Esta é a funcionalidade mais complexa e inovadora do projeto, implementada inteiramente no frontend com JavaScript.

- **Versão Básica (Inicial):**
    - Ao clicar em uma imagem de tatuagem nos perfis dos tatuadores, abria um modal com a webcam.
    - A tatuagem selecionada era sobreposta (overlay) sobre o vídeo.
    - Controles manuais para ajustar tamanho e opacidade.
    - Funcionalidade de arrastar a tatuagem para posicionamento.
    - Captura de foto com a tatuagem sobreposta.
    - Código: `tattoo-camera.js` (substituído pela versão avançada).

- **Versão Avançada (Atual):**
    - **Pré-seleção da Região Corporal:** Antes de abrir a câmera, o usuário seleciona a parte do corpo desejada (antebraço, braço, costas, etc.) em um modal com imagens representativas.
    - **Reconhecimento de Pose:** Utiliza TensorFlow.js e o modelo PoseNet para detectar os pontos-chave do corpo humano no vídeo da webcam em tempo real.
    - **Mapeamento Automático:** A tatuagem é automaticamente posicionada e rotacionada sobre a região corporal detectada, acompanhando os movimentos do usuário.
    - **Simulação Image-to-Image (Realismo):** A tatuagem não é apenas sobreposta, mas integrada visualmente à pele. O sistema simula a adaptação à textura, contornos e iluminação da pele detectada, proporcionando um efeito mais realista.
    - **Controles Adicionais:** Inclui um controle deslizante de "Realismo" para ajustar a intensidade do efeito image-to-image.
    - **Carregamento de Modelos:** Os modelos de IA (PoseNet e o simulador image-to-image) são carregados dinamicamente via JavaScript (`tensorflow-models-loader.js`).
    - **Código Principal:** `tattoo-camera-image2image.js`.
    - **Guia de Uso:** `docs/tattoo-simulator-advanced-guide.md`.

## 5. Tecnologias Utilizadas

- **Python 3.11**
- **Django 5.x**
- **HTML5**
- **CSS3**
- **JavaScript (ES6+)**
- **Bootstrap 5**
- **SQLite3**
- **TensorFlow.js Core (@tensorflow/tfjs)**: Biblioteca para machine learning em JavaScript.
- **TensorFlow.js PoseNet Model (@tensorflow-models/posenet)**: Modelo pré-treinado para detecção de pose humana.
- **WebRTC (getUserMedia API):** Para acesso à câmera do usuário via navegador.
- **HTML Canvas API:** Para renderização do vídeo, overlay da tatuagem e processamento de imagem.
- **Git:** Para controle de versão (repositório no GitHub).
- **ZIP:** Para empacotamento e entrega do projeto.

## 6. Instruções de Instalação e Execução

1.  **Pré-requisitos:**
    *   Python 3.10 ou superior instalado.
    *   `pip` (gerenciador de pacotes Python).
2.  **Descompactar o Projeto:** Extraia o conteúdo do arquivo `.zip` (ex: `nao_tattoo_image2image.zip`) para um diretório de sua escolha.
3.  **Navegar até o Diretório:** Abra um terminal ou prompt de comando e navegue até o diretório do projeto Django:
    ```bash
    cd caminho/para/nao/projeto
    ```
4.  **Instalar Dependências:** Instale o Django (se ainda não estiver instalado):
    ```bash
    pip install django
    ```
    *(Nota: Para um ambiente de produção, é recomendado usar um ambiente virtual e um arquivo `requirements.txt`)*
5.  **Aplicar Migrações:** Crie e aplique as migrações do banco de dados:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Criar um Superusuário (Opcional):** Para acessar a interface administrativa do Django:
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir nome de usuário, email e senha.
7.  **Iniciar o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
8.  **Acessar a Aplicação:** Abra seu navegador e acesse `http://127.0.0.1:8000/`.

## 7. Guia de Uso do Simulador Avançado

Consulte o arquivo `/home/ubuntu/nao/projeto/static/assets/docs/tattoo-simulator-advanced-guide.md` para um guia detalhado sobre como utilizar a funcionalidade de simulação de tatuagem com reconhecimento de região corporal.

## 8. Próximos Passos (Sugestões)

- **Melhorar Modelo Image-to-Image:** Substituir a simulação atual por um modelo real de image-to-image para maior realismo.
- **Expandir Funcionalidades do Chat:** Implementar um sistema de chat em tempo real (ex: usando WebSockets).
- **Agendamento:** Adicionar funcionalidade para agendar sessões com os tatuadores.
- **Banco de Dados:** Migrar para um banco de dados mais robusto (PostgreSQL, MySQL) para produção.
- **Testes Automatizados:** Implementar testes unitários e de integração.
- **Deployment:** Configurar o deploy da aplicação em um servidor de produção (ex: Heroku, AWS, Google Cloud).

