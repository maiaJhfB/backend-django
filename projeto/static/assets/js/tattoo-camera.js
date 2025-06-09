// Tattoo Camera Overlay - Funcionalidade para simular tatuagens usando a webcam
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona evento de clique a todas as imagens de tatuagem
    const tattooImages = document.querySelectorAll('.item-img img');
    
    tattooImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.title = 'Clique para experimentar esta tatuagem';
        
        img.addEventListener('click', function(e) {
            e.preventDefault();
            openTattooCamera(this.src);
        });
    });
    
    // Função para abrir a câmera com a tatuagem selecionada
    function openTattooCamera(tattooSrc) {
        // Criar o modal para a câmera
        const modalHtml = `
            <div id="tattooCameraModal" class="modal fade show" style="display: block; background-color: rgba(0,0,0,0.8);">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Experimente sua tatuagem</h5>
                            <button type="button" class="btn-close" id="closeModal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="camera-container" style="position: relative; width: 100%; max-width: 640px; margin: 0 auto;">
                                <video id="webcamVideo" autoplay playsinline style="width: 100%; height: auto; transform: scaleX(-1);"></video>
                                <canvas id="tattooOverlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></canvas>
                                <div class="controls" style="margin-top: 15px; display: flex; justify-content: space-between;">
                                    <div>
                                        <label for="tattooSize">Tamanho: </label>
                                        <input type="range" id="tattooSize" min="10" max="100" value="50">
                                    </div>
                                    <div>
                                        <label for="tattooOpacity">Opacidade: </label>
                                        <input type="range" id="tattooOpacity" min="10" max="100" value="80">
                                    </div>
                                </div>
                                <div class="position-info" style="margin-top: 10px; text-align: center;">
                                    <p>Arraste a tatuagem para posicioná-la. Use os controles para ajustar tamanho e opacidade.</p>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" id="cancelTattoo">Cancelar</button>
                            <button type="button" class="btn btn-danger" id="takePicture">Tirar Foto</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Adicionar o modal ao corpo do documento
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHtml;
        document.body.appendChild(modalContainer);
        
        // Impedir o scroll da página enquanto o modal estiver aberto
        document.body.style.overflow = 'hidden';
        
        // Referências aos elementos
        const modal = document.getElementById('tattooCameraModal');
        const closeBtn = document.getElementById('closeModal');
        const cancelBtn = document.getElementById('cancelTattoo');
        const takePictureBtn = document.getElementById('takePicture');
        const video = document.getElementById('webcamVideo');
        const canvas = document.getElementById('tattooOverlay');
        const sizeSlider = document.getElementById('tattooSize');
        const opacitySlider = document.getElementById('tattooOpacity');
        
        // Variáveis para controle da tatuagem
        let tattooImage = new Image();
        tattooImage.src = tattooSrc;
        let tattooSize = 50; // percentual do tamanho original
        let tattooOpacity = 0.8;
        let tattooX = 0;
        let tattooY = 0;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        
        // Configurar o canvas
        const ctx = canvas.getContext('2d');
        
        // Iniciar a webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                
                // Ajustar o tamanho do canvas para corresponder ao vídeo após o carregamento
                video.onloadedmetadata = function() {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    
                    // Posicionar a tatuagem no centro inicialmente
                    tattooX = canvas.width / 2;
                    tattooY = canvas.height / 2;
                    
                    // Iniciar o loop de renderização
                    renderTattoo();
                };
            })
            .catch(function(error) {
                alert('Erro ao acessar a câmera: ' + error.message);
                closeModal();
            });
        
        // Função para renderizar a tatuagem sobre o vídeo
        function renderTattoo() {
            if (!video.paused && !video.ended) {
                // Limpar o canvas
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Calcular o tamanho da tatuagem
                const imgWidth = (tattooImage.width * tattooSize / 100);
                const imgHeight = (tattooImage.height * tattooSize / 100);
                
                // Desenhar a tatuagem com a opacidade definida
                ctx.globalAlpha = tattooOpacity;
                ctx.drawImage(
                    tattooImage,
                    tattooX - imgWidth / 2,
                    tattooY - imgHeight / 2,
                    imgWidth,
                    imgHeight
                );
                ctx.globalAlpha = 1.0;
                
                // Continuar o loop de renderização
                requestAnimationFrame(renderTattoo);
            }
        }
        
        // Eventos para arrastar a tatuagem
        canvas.addEventListener('mousedown', function(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            const x = (e.clientX - rect.left) * scaleX;
            const y = (e.clientY - rect.top) * scaleY;
            
            // Verificar se o clique foi sobre a tatuagem
            const imgWidth = (tattooImage.width * tattooSize / 100);
            const imgHeight = (tattooImage.height * tattooSize / 100);
            
            if (
                x >= tattooX - imgWidth / 2 &&
                x <= tattooX + imgWidth / 2 &&
                y >= tattooY - imgHeight / 2 &&
                y <= tattooY + imgHeight / 2
            ) {
                isDragging = true;
                dragStartX = x - tattooX;
                dragStartY = y - tattooY;
            }
        });
        
        canvas.addEventListener('mousemove', function(e) {
            if (isDragging) {
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                const x = (e.clientX - rect.left) * scaleX;
                const y = (e.clientY - rect.top) * scaleY;
                
                tattooX = x - dragStartX;
                tattooY = y - dragStartY;
            }
        });
        
        canvas.addEventListener('mouseup', function() {
            isDragging = false;
        });
        
        canvas.addEventListener('mouseleave', function() {
            isDragging = false;
        });
        
        // Eventos para dispositivos móveis (touch)
        canvas.addEventListener('touchstart', function(e) {
            e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            const x = (e.touches[0].clientX - rect.left) * scaleX;
            const y = (e.touches[0].clientY - rect.top) * scaleY;
            
            // Verificar se o toque foi sobre a tatuagem
            const imgWidth = (tattooImage.width * tattooSize / 100);
            const imgHeight = (tattooImage.height * tattooSize / 100);
            
            if (
                x >= tattooX - imgWidth / 2 &&
                x <= tattooX + imgWidth / 2 &&
                y >= tattooY - imgHeight / 2 &&
                y <= tattooY + imgHeight / 2
            ) {
                isDragging = true;
                dragStartX = x - tattooX;
                dragStartY = y - tattooY;
            }
        });
        
        canvas.addEventListener('touchmove', function(e) {
            e.preventDefault();
            if (isDragging) {
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                const x = (e.touches[0].clientX - rect.left) * scaleX;
                const y = (e.touches[0].clientY - rect.top) * scaleY;
                
                tattooX = x - dragStartX;
                tattooY = y - dragStartY;
            }
        });
        
        canvas.addEventListener('touchend', function(e) {
            e.preventDefault();
            isDragging = false;
        });
        
        // Eventos para os controles deslizantes
        sizeSlider.addEventListener('input', function() {
            tattooSize = parseInt(this.value);
        });
        
        opacitySlider.addEventListener('input', function() {
            tattooOpacity = parseInt(this.value) / 100;
        });
        
        // Função para tirar uma foto
        takePictureBtn.addEventListener('click', function() {
            // Criar um canvas temporário para a captura
            const captureCanvas = document.createElement('canvas');
            captureCanvas.width = video.videoWidth;
            captureCanvas.height = video.videoHeight;
            const captureCtx = captureCanvas.getContext('2d');
            
            // Desenhar o vídeo espelhado (como está sendo exibido)
            captureCtx.save();
            captureCtx.scale(-1, 1);
            captureCtx.drawImage(video, -captureCanvas.width, 0, captureCanvas.width, captureCanvas.height);
            captureCtx.restore();
            
            // Desenhar a tatuagem
            const imgWidth = (tattooImage.width * tattooSize / 100);
            const imgHeight = (tattooImage.height * tattooSize / 100);
            
            captureCtx.globalAlpha = tattooOpacity;
            captureCtx.drawImage(
                tattooImage,
                tattooX - imgWidth / 2,
                tattooY - imgHeight / 2,
                imgWidth,
                imgHeight
            );
            
            // Converter para imagem
            const imageDataURL = captureCanvas.toDataURL('image/png');
            
            // Mostrar a imagem capturada
            showCapturedImage(imageDataURL);
        });
        
        // Função para mostrar a imagem capturada
        function showCapturedImage(imageDataURL) {
            // Parar o vídeo e limpar o canvas
            const stream = video.srcObject;
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            
            // Substituir o conteúdo do modal
            const modalBody = modal.querySelector('.modal-body');
            modalBody.innerHTML = `
                <div style="text-align: center;">
                    <h4>Sua tatuagem virtual</h4>
                    <img src="${imageDataURL}" style="max-width: 100%; border: 1px solid #ddd; margin-top: 10px;">
                    <p style="margin-top: 15px;">Esta é uma simulação de como a tatuagem ficaria. Para fazer a tatuagem real, entre em contato com o tatuador.</p>
                </div>
            `;
            
            // Atualizar os botões do rodapé
            const modalFooter = modal.querySelector('.modal-footer');
            modalFooter.innerHTML = `
                <button type="button" class="btn btn-secondary" id="closeAfterCapture">Fechar</button>
                <a href="#" class="btn btn-danger" id="downloadImage">Baixar Imagem</a>
                <a href="{% url 'chat' %}" class="btn btn-primary">Falar com o Tatuador</a>
            `;
            
            // Adicionar evento para download da imagem
            document.getElementById('downloadImage').addEventListener('click', function(e) {
                e.preventDefault();
                const link = document.createElement('a');
                link.download = 'minha-tatuagem-virtual.png';
                link.href = imageDataURL;
                link.click();
            });
            
            // Adicionar evento para fechar o modal
            document.getElementById('closeAfterCapture').addEventListener('click', closeModal);
        }
        
        // Função para fechar o modal
        function closeModal() {
            // Parar o vídeo se estiver rodando
            const stream = video.srcObject;
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            
            // Remover o modal
            document.body.removeChild(modalContainer);
            document.body.style.overflow = '';
        }
        
        // Eventos para fechar o modal
        closeBtn.addEventListener('click', closeModal);
        cancelBtn.addEventListener('click', closeModal);
    }
});
