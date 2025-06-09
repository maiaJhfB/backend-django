// Tattoo Camera Overlay com Reconhecimento de Região Corporal
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona evento de clique a todas as imagens de tatuagem
    const tattooImages = document.querySelectorAll('.item-img img');
    
    tattooImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.title = 'Clique para experimentar esta tatuagem';
        
        img.addEventListener('click', function(e) {
            e.preventDefault();
            openBodyPartSelector(this.src);
        });
    });
    
    // Função para abrir o seletor de parte do corpo
    function openBodyPartSelector(tattooSrc) {
        // Criar o modal para seleção da parte do corpo
        const modalHtml = `
            <div id="bodyPartSelectorModal" class="modal fade show" style="display: block; background-color: rgba(0,0,0,0.8);">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Selecione a parte do corpo para a tatuagem</h5>
                            <button type="button" class="btn-close" id="closeBodyPartModal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="body-part-container" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">
                                <div class="body-part-option" data-part="forearm" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/forearm.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Antebraço</p>
                                </div>
                                <div class="body-part-option" data-part="upperarm" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/upperarm.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Braço</p>
                                </div>
                                <div class="body-part-option" data-part="back" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/back.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Costas</p>
                                </div>
                                <div class="body-part-option" data-part="chest" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/chest.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Peito</p>
                                </div>
                                <div class="body-part-option" data-part="leg" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/leg.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Perna</p>
                                </div>
                                <div class="body-part-option" data-part="ankle" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/ankle.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Tornozelo</p>
                                </div>
                                <div class="body-part-option" data-part="wrist" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/wrist.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Pulso</p>
                                </div>
                                <div class="body-part-option" data-part="neck" style="cursor: pointer; text-align: center; padding: 10px; border: 2px solid #ddd; border-radius: 8px; width: 150px;">
                                    <img src="/static/assets/images/body-parts/neck.jpg" style="width: 100%; height: auto; margin-bottom: 10px;">
                                    <p>Pescoço</p>
                                </div>
                            </div>
                            <div class="instructions" style="margin-top: 20px; text-align: center;">
                                <p>Clique na parte do corpo onde você deseja aplicar a tatuagem.</p>
                                <p>O sistema reconhecerá automaticamente essa região quando você abrir a câmera.</p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" id="cancelBodyPartSelection">Cancelar</button>
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
        const modal = document.getElementById('bodyPartSelectorModal');
        const closeBtn = document.getElementById('closeBodyPartModal');
        const cancelBtn = document.getElementById('cancelBodyPartSelection');
        const bodyPartOptions = document.querySelectorAll('.body-part-option');
        
        // Função para fechar o modal
        function closeModal() {
            document.body.removeChild(modalContainer);
            document.body.style.overflow = '';
        }
        
        // Eventos para fechar o modal
        closeBtn.addEventListener('click', closeModal);
        cancelBtn.addEventListener('click', closeModal);
        
        // Adicionar evento de clique às opções de parte do corpo
        bodyPartOptions.forEach(option => {
            option.addEventListener('click', function() {
                const bodyPart = this.getAttribute('data-part');
                closeModal();
                openTattooCamera(tattooSrc, bodyPart);
            });
            
            // Adicionar efeito de hover
            option.addEventListener('mouseover', function() {
                this.style.borderColor = '#a95b18';
            });
            
            option.addEventListener('mouseout', function() {
                this.style.borderColor = '#ddd';
            });
        });
    }
    
    // Função para carregar o modelo de detecção de pose
    async function loadPoseDetectionModel() {
        // Carregar o modelo PoseNet do TensorFlow.js
        return await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            inputResolution: { width: 640, height: 480 },
            multiplier: 0.75
        });
    }
    
    // Função para abrir a câmera com a tatuagem selecionada
    async function openTattooCamera(tattooSrc, bodyPart) {
        // Criar o modal para a câmera
        const modalHtml = `
            <div id="tattooCameraModal" class="modal fade show" style="display: block; background-color: rgba(0,0,0,0.8);">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Experimente sua tatuagem - ${getBodyPartName(bodyPart)}</h5>
                            <button type="button" class="btn-close" id="closeModal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="camera-container" style="position: relative; width: 100%; max-width: 640px; margin: 0 auto;">
                                <video id="webcamVideo" autoplay playsinline style="width: 100%; height: auto; transform: scaleX(-1);"></video>
                                <canvas id="tattooOverlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></canvas>
                                <div id="loadingIndicator" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: rgba(0,0,0,0.7); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                                    <div class="spinner-border text-light" role="status">
                                        <span class="visually-hidden">Carregando...</span>
                                    </div>
                                    <p style="margin-top: 10px;">Carregando modelo de detecção...</p>
                                </div>
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
                                    <p>Posicione a parte do corpo selecionada na frente da câmera.</p>
                                    <p>O sistema detectará automaticamente a região e aplicará a tatuagem.</p>
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
        const loadingIndicator = document.getElementById('loadingIndicator');
        const sizeSlider = document.getElementById('tattooSize');
        const opacitySlider = document.getElementById('tattooOpacity');
        
        // Variáveis para controle da tatuagem
        let tattooImage = new Image();
        tattooImage.src = tattooSrc;
        let tattooSize = 50; // percentual do tamanho original
        let tattooOpacity = 0.8;
        let poseDetectionModel = null;
        let detectedKeypoints = null;
        
        // Configurar o canvas
        const ctx = canvas.getContext('2d');
        
        // Iniciar a webcam
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            
            // Ajustar o tamanho do canvas para corresponder ao vídeo após o carregamento
            video.onloadedmetadata = function() {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                
                // Carregar o modelo de detecção de pose
                loadPoseDetectionModel().then(model => {
                    poseDetectionModel = model;
                    loadingIndicator.style.display = 'none';
                    
                    // Iniciar o loop de renderização
                    detectPoseAndRender();
                }).catch(error => {
                    console.error('Erro ao carregar o modelo de detecção de pose:', error);
                    loadingIndicator.innerHTML = `
                        <p>Erro ao carregar o modelo de detecção.</p>
                        <p>Você ainda pode posicionar a tatuagem manualmente.</p>
                        <button class="btn btn-primary" id="continueWithoutDetection">Continuar</button>
                    `;
                    document.getElementById('continueWithoutDetection').addEventListener('click', function() {
                        loadingIndicator.style.display = 'none';
                        renderTattooManually();
                    });
                });
            };
        } catch (error) {
            alert('Erro ao acessar a câmera: ' + error.message);
            closeModal();
        }
        
        // Função para detectar a pose e renderizar a tatuagem
        async function detectPoseAndRender() {
            if (!video.paused && !video.ended) {
                // Detectar a pose
                if (poseDetectionModel) {
                    try {
                        const pose = await poseDetectionModel.estimateSinglePose(video, {
                            flipHorizontal: true
                        });
                        
                        detectedKeypoints = pose.keypoints;
                        
                        // Renderizar a tatuagem na parte do corpo selecionada
                        renderTattooOnBodyPart(bodyPart, detectedKeypoints);
                    } catch (error) {
                        console.error('Erro na detecção de pose:', error);
                    }
                }
                
                // Continuar o loop de renderização
                requestAnimationFrame(detectPoseAndRender);
            }
        }
        
        // Função para renderizar a tatuagem manualmente (fallback)
        function renderTattooManually() {
            // Variáveis para controle manual
            let tattooX = canvas.width / 2;
            let tattooY = canvas.height / 2;
            let isDragging = false;
            let dragStartX = 0;
            let dragStartY = 0;
            
            function render() {
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
                    requestAnimationFrame(render);
                }
            }
            
            // Eventos para arrastar a tatuagem
            canvas.addEventListener('mousedown', function(e) {
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                const x = (e.clientX - rect.left) * scaleX;
                const y = (e.clientY - rect.top) * scaleY;
                
                isDragging = true;
                dragStartX = x - tattooX;
                dragStartY = y - tattooY;
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
                
                isDragging = true;
                dragStartX = x - tattooX;
                dragStartY = y - tattooY;
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
            
            // Iniciar o loop de renderização
            render();
        }
        
        // Função para renderizar a tatuagem na parte do corpo selecionada
        function renderTattooOnBodyPart(bodyPart, keypoints) {
            if (!keypoints) return;
            
            // Limpar o canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Calcular o tamanho da tatuagem
            const imgWidth = (tattooImage.width * tattooSize / 100);
            const imgHeight = (tattooImage.height * tattooSize / 100);
            
            // Obter as coordenadas da parte do corpo selecionada
            const bodyPartCoordinates = getBodyPartCoordinates(bodyPart, keypoints);
            
            if (bodyPartCoordinates) {
                // Aplicar transformações para adaptar a tatuagem à parte do corpo
                ctx.save();
                
                // Posicionar no ponto de referência
                ctx.translate(bodyPartCoordinates.x, bodyPartCoordinates.y);
                
                // Rotacionar se necessário
                if (bodyPartCoordinates.angle) {
                    ctx.rotate(bodyPartCoordinates.angle);
                }
                
                // Aplicar curvatura se necessário
                if (bodyPartCoordinates.curvature) {
                    // Implementação simplificada de curvatura - na prática, seria mais complexo
                    // e usaria transformações não lineares ou meshes
                }
                
                // Desenhar a tatuagem com a opacidade definida
                ctx.globalAlpha = tattooOpacity;
                ctx.drawImage(
                    tattooImage,
                    -imgWidth / 2,
                    -imgHeight / 2,
                    imgWidth,
                    imgHeight
                );
                
                ctx.restore();
                ctx.globalAlpha = 1.0;
                
                // Opcional: desenhar pontos de referência para debug
                if (false) { // Altere para true para visualizar os pontos de referência
                    drawKeypoints(keypoints);
                }
            } else {
                // Fallback: renderizar no centro se não conseguir detectar a parte do corpo
                ctx.globalAlpha = tattooOpacity;
                ctx.drawImage(
                    tattooImage,
                    canvas.width / 2 - imgWidth / 2,
                    canvas.height / 2 - imgHeight / 2,
                    imgWidth,
                    imgHeight
                );
                ctx.globalAlpha = 1.0;
            }
        }
        
        // Função para obter as coordenadas da parte do corpo selecionada
        function getBodyPartCoordinates(bodyPart, keypoints) {
            if (!keypoints) return null;
            
            // Mapear as partes do corpo para os keypoints correspondentes
            const keypointMap = {
                forearm: {
                    getCoordinates: () => {
                        const wrist = findKeypoint('leftWrist', keypoints) || findKeypoint('rightWrist', keypoints);
                        const elbow = findKeypoint('leftElbow', keypoints) || findKeypoint('rightElbow', keypoints);
                        
                        if (wrist && elbow) {
                            const midX = (wrist.position.x + elbow.position.x) / 2;
                            const midY = (wrist.position.y + elbow.position.y) / 2;
                            const angle = Math.atan2(elbow.position.y - wrist.position.y, elbow.position.x - wrist.position.x);
                            
                            return {
                                x: midX,
                                y: midY,
                                angle: angle,
                                width: distance(wrist.position, elbow.position),
                                height: distance(wrist.position, elbow.position) / 3
                            };
                        }
                        return null;
                    }
                },
                upperarm: {
                    getCoordinates: () => {
                        const elbow = findKeypoint('leftElbow', keypoints) || findKeypoint('rightElbow', keypoints);
                        const shoulder = findKeypoint('leftShoulder', keypoints) || findKeypoint('rightShoulder', keypoints);
                        
                        if (elbow && shoulder) {
                            const midX = (elbow.position.x + shoulder.position.x) / 2;
                            const midY = (elbow.position.y + shoulder.position.y) / 2;
                            const angle = Math.atan2(shoulder.position.y - elbow.position.y, shoulder.position.x - elbow.position.x);
                            
                            return {
                                x: midX,
                                y: midY,
                                angle: angle,
                                width: distance(elbow.position, shoulder.position),
                                height: distance(elbow.position, shoulder.position) / 2
                            };
                        }
                        return null;
                    }
                },
                back: {
                    getCoordinates: () => {
                        const leftShoulder = findKeypoint('leftShoulder', keypoints);
                        const rightShoulder = findKeypoint('rightShoulder', keypoints);
                        const leftHip = findKeypoint('leftHip', keypoints);
                        const rightHip = findKeypoint('rightHip', keypoints);
                        
                        if (leftShoulder && rightShoulder && leftHip && rightHip) {
                            const midShoulderX = (leftShoulder.position.x + rightShoulder.position.x) / 2;
                            const midShoulderY = (leftShoulder.position.y + rightShoulder.position.y) / 2;
                            const midHipX = (leftHip.position.x + rightHip.position.x) / 2;
                            const midHipY = (leftHip.position.y + rightHip.position.y) / 2;
                            
                            return {
                                x: (midShoulderX + midHipX) / 2,
                                y: (midShoulderY + midHipY) / 2,
                                angle: Math.atan2(midHipY - midShoulderY, midHipX - midShoulderX) + Math.PI / 2,
                                width: distance({x: leftShoulder.position.x, y: leftShoulder.position.y}, 
                                               {x: rightShoulder.position.x, y: rightShoulder.position.y}),
                                height: distance({x: midShoulderX, y: midShoulderY}, 
                                                {x: midHipX, y: midHipY})
                            };
                        }
                        return null;
                    }
                },
                chest: {
                    getCoordinates: () => {
                        const leftShoulder = findKeypoint('leftShoulder', keypoints);
                        const rightShoulder = findKeypoint('rightShoulder', keypoints);
                        const leftHip = findKeypoint('leftHip', keypoints);
                        const rightHip = findKeypoint('rightHip', keypoints);
                        
                        if (leftShoulder && rightShoulder && leftHip && rightHip) {
                            const midShoulderX = (leftShoulder.position.x + rightShoulder.position.x) / 2;
                            const midShoulderY = (leftShoulder.position.y + rightShoulder.position.y) / 2;
                            const midHipX = (leftHip.position.x + rightHip.position.x) / 2;
                            const midHipY = (leftHip.position.y + rightHip.position.y) / 2;
                            
                            return {
                                x: (midShoulderX + midHipX) / 2,
                                y: midShoulderY + (midHipY - midShoulderY) / 3,
                                angle: 0,
                                width: distance({x: leftShoulder.position.x, y: leftShoulder.position.y}, 
                                               {x: rightShoulder.position.x, y: rightShoulder.position.y}),
                                height: distance({x: midShoulderX, y: midShoulderY}, 
                                                {x: midHipX, y: midHipY}) / 2
                            };
                        }
                        return null;
                    }
                },
                leg: {
                    getCoordinates: () => {
                        const knee = findKeypoint('leftKnee', keypoints) || findKeypoint('rightKnee', keypoints);
                        const hip = findKeypoint('leftHip', keypoints) || findKeypoint('rightHip', keypoints);
                        
                        if (knee && hip) {
                            const midX = (knee.position.x + hip.position.x) / 2;
                            const midY = (knee.position.y + hip.position.y) / 2;
                            const angle = Math.atan2(hip.position.y - knee.position.y, hip.position.x - knee.position.x);
                            
                            return {
                                x: midX,
                                y: midY,
                                angle: angle,
                                width: distance(knee.position, hip.position) / 2,
                                height: distance(knee.position, hip.position)
                            };
                        }
                        return null;
                    }
                },
                ankle: {
                    getCoordinates: () => {
                        const ankle = findKeypoint('leftAnkle', keypoints) || findKeypoint('rightAnkle', keypoints);
                        const knee = findKeypoint('leftKnee', keypoints) || findKeypoint('rightKnee', keypoints);
                        
                        if (ankle && knee) {
                            return {
                                x: ankle.position.x,
                                y: ankle.position.y,
                                angle: 0,
                                width: distance(ankle.position, knee.position) / 3,
                                height: distance(ankle.position, knee.position) / 3
                            };
                        }
                        return null;
                    }
                },
                wrist: {
                    getCoordinates: () => {
                        const wrist = findKeypoint('leftWrist', keypoints) || findKeypoint('rightWrist', keypoints);
                        
                        if (wrist) {
                            return {
                                x: wrist.position.x,
                                y: wrist.position.y,
                                angle: 0,
                                width: canvas.width / 10,
                                height: canvas.width / 10
                            };
                        }
                        return null;
                    }
                },
                neck: {
                    getCoordinates: () => {
                        const leftShoulder = findKeypoint('leftShoulder', keypoints);
                        const rightShoulder = findKeypoint('rightShoulder', keypoints);
                        const nose = findKeypoint('nose', keypoints);
                        
                        if (leftShoulder && rightShoulder && nose) {
                            const midShoulderX = (leftShoulder.position.x + rightShoulder.position.x) / 2;
                            const midShoulderY = (leftShoulder.position.y + rightShoulder.position.y) / 2;
                            
                            return {
                                x: midShoulderX,
                                y: midShoulderY - (midShoulderY - nose.position.y) / 3,
                                angle: Math.PI / 2,
                                width: distance({x: leftShoulder.position.x, y: leftShoulder.position.y}, 
                                               {x: rightShoulder.position.x, y: rightShoulder.position.y}) / 2,
                                height: (midShoulderY - nose.position.y) / 2
                            };
                        }
                        return null;
                    }
                }
            };
            
            // Obter as coordenadas da parte do corpo selecionada
            if (keypointMap[bodyPart]) {
                return keypointMap[bodyPart].getCoordinates();
            }
            
            return null;
        }
        
        // Função auxiliar para encontrar um keypoint pelo nome
        function findKeypoint(name, keypoints) {
            return keypoints.find(kp => kp.part === name);
        }
        
        // Função auxiliar para calcular a distância entre dois pontos
        function distance(point1, point2) {
            return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
        }
        
        // Função auxiliar para desenhar os keypoints (para debug)
        function drawKeypoints(keypoints) {
            keypoints.forEach(keypoint => {
                if (keypoint.score > 0.5) {
                    ctx.fillStyle = 'red';
                    ctx.beginPath();
                    ctx.arc(keypoint.position.x, keypoint.position.y, 5, 0, 2 * Math.PI);
                    ctx.fill();
                    
                    ctx.fillStyle = 'white';
                    ctx.font = '12px Arial';
                    ctx.fillText(keypoint.part, keypoint.position.x + 5, keypoint.position.y - 5);
                }
            });
        }
        
        // Função para obter o nome da parte do corpo
        function getBodyPartName(bodyPart) {
            const names = {
                forearm: 'Antebraço',
                upperarm: 'Braço',
                back: 'Costas',
                chest: 'Peito',
                leg: 'Perna',
                ankle: 'Tornozelo',
                wrist: 'Pulso',
                neck: 'Pescoço'
            };
            
            return names[bodyPart] || bodyPart;
        }
        
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
            
            // Copiar o conteúdo do canvas de overlay
            captureCtx.drawImage(canvas, 0, 0);
            
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
                    <h4>Sua tatuagem virtual - ${getBodyPartName(bodyPart)}</h4>
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
                link.download = `tatuagem-virtual-${bodyPart}.png`;
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
