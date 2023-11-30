import cv2

    
""" Faz um teste de streaming de video do modelo treinado.

    * Redimendiona frame recebido do streming de video.
    * Transforma a imagem recebida em cinza.
    * Determina os parâmetros úteis para análise da imagem.
    * Sobrescreve um retangulo verde sobre a imagem, caso hája detecção de "lixo".
"""
Camera = cv2.VideoCapture(0)

# 
classificador = cv2.CascadeClassifier('cascade.xml')

while True:
    camera = Camera.read()
    
    # Retorna frame para pasta.
    cv2.imwrite('out.jpg',camera)
    
    # Caso não identifique streaming de vídeo pausa.
    if not camera:
        break

    # Resolução da imagem.
    camera = cv2.resize(camera, (160,120))
    cinza = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)

    # Configuração de identificação de imagem.
    detecta = classificador.detectMultiScale(cinza, minNeighbors=1, minSize=(50,50))

    '''
    Outros tipos de configuração podem ser testadas, redimensionando tamanho de deteção, mudando resolução ou visinhos próximos de detecção

    detecta = classificador.detectMultiScale(cinza, scaleFactor=1.1, minSize=(100, 100))
    detecta = classificador.detectMultiScale(cinza, scaleFactor=1.5, minNeighbors=1, minSize=(150,150))
    detecta = classificador.detectMultiScale (cinza , minNeighbors= 3 , minSize= ( 30 , 30 ))
    
    '''
    
    for (x, y, l, a) in detecta:
        # Desenha na tela um retangulo caso encontra um "lixo" e retorna os parametros da tela.
        cv2.rectangle(camera, (x, y), (x + l, y + a), (0, 255, 0), 2)

    cv2.imshow("Detecção de lixo - Teste", camera)

Camera.release()
cv2.destroyAllWindows()