# Guia de Uso - Simulador Avançado de Tatuagem com Reconhecimento de Região Corporal

## Visão Geral
O Simulador Avançado de Tatuagem permite que os usuários experimentem virtualmente como uma tatuagem ficaria em sua pele, com reconhecimento automático da região corporal e adaptação realista da tatuagem à superfície da pele usando tecnologia image-to-image.

## Funcionalidades Principais

1. **Pré-seleção da Região Corporal**:
   - Antes de abrir a câmera, o usuário seleciona a parte do corpo onde deseja aplicar a tatuagem
   - Interface visual com imagens representativas de cada região corporal
   - Opções incluem: antebraço, braço, costas, peito, perna, tornozelo, pulso e pescoço

2. **Reconhecimento Automático da Região**:
   - O sistema utiliza tecnologia de detecção de pose para identificar automaticamente a região selecionada no vídeo
   - A tatuagem é posicionada e adaptada automaticamente à região detectada
   - Ajuste dinâmico conforme o usuário se movimenta

3. **Integração Realista com Image-to-Image**:
   - A tatuagem é adaptada para parecer parte da pele, não apenas sobreposta
   - Ajuste automático de textura, sombreamento e contornos para simular aderência à pele
   - Controle de realismo para personalizar o nível de integração com a pele

4. **Controles Avançados**:
   - **Tamanho**: Ajuste as dimensões da tatuagem
   - **Opacidade**: Controle a intensidade da tatuagem
   - **Realismo**: Ajuste o nível de integração com a pele (efeito image-to-image)

## Como Usar

1. **Seleção da Tatuagem**:
   - Navegue até a página de um tatuador (Natalia ou Lucas)
   - Clique em qualquer imagem de tatuagem que você gostaria de experimentar

2. **Seleção da Região Corporal**:
   - No modal que aparece, clique na parte do corpo onde deseja aplicar a tatuagem
   - Cada opção mostra uma imagem representativa da região

3. **Posicionamento na Câmera**:
   - Após selecionar a região, a câmera será aberta
   - Posicione a parte do corpo selecionada na frente da câmera
   - O sistema detectará automaticamente a região e aplicará a tatuagem

4. **Ajustes Finos**:
   - Use os controles deslizantes para ajustar tamanho, opacidade e realismo
   - Observe como a tatuagem se adapta à sua pele em tempo real
   - A tatuagem seguirá seus movimentos, mantendo-se na região corporal selecionada

5. **Captura da Imagem**:
   - Quando estiver satisfeito com o resultado, clique em "Tirar Foto"
   - O sistema capturará a imagem com a tatuagem integrada à sua pele
   - Você poderá baixar a imagem ou compartilhá-la diretamente

## Requisitos Técnicos
- Navegador moderno com suporte a WebRTC e WebGL (Chrome, Firefox, Edge, Safari)
- Permissão para acessar a webcam do dispositivo
- JavaScript habilitado no navegador
- Conexão à internet para carregamento dos modelos de IA

## Privacidade e Segurança
- Todo o processamento de imagem e detecção ocorre localmente no navegador
- Nenhuma imagem é enviada para servidores externos
- Os modelos de IA são carregados apenas uma vez e armazenados em cache
- Nenhuma imagem é armazenada permanentemente, a menos que você escolha baixá-la

## Dicas para Melhores Resultados
- Use boa iluminação para melhor detecção da região corporal
- Mantenha a parte do corpo selecionada claramente visível na câmera
- Experimente diferentes níveis de realismo para encontrar o efeito mais natural
- Para tatuagens em áreas difíceis de capturar com a webcam, considere usar o chat para discutir com o tatuador

## Solução de Problemas
- **Detecção incorreta**: Reposicione-se na câmera ou ajuste a iluminação
- **Carregamento lento**: Os modelos de IA podem levar alguns segundos para carregar na primeira vez
- **Tatuagem não aparece**: Verifique se a parte do corpo selecionada está visível na câmera
- **Baixa performance**: Reduza o nível de realismo para melhorar a velocidade de processamento

## Suporte
Em caso de problemas com o simulador, entre em contato através do chat ou pelo e-mail InkEtrom@gmail.com
