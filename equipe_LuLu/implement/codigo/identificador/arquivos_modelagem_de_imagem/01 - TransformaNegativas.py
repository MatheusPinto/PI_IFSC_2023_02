import cv2
import os
from imutils import paths # imultils é Uma série de funções convenientes para facilitar funções básicas de processamento de imagens, como tradução, rotação, redimensionamento, esqueletização e exibição de imagens etc.
import shutil

def listaNegImagem():
    """Listas as imagens negativas.
    
    Transforma as imagens negativas (não-lixo), no formato e cor default do haar-cascade.
    """
    imagemPath = list(paths.list_images('imagens/nao-lixo'))

    # Declarando uma variável para na minha pasta de resultados negativos, renomear todos as imagens de 1 ao total.
    numero = 1

    if not os.path.exists('negativo'):
        os.makedirs('negativo')

    for i in imagemPath:
        i.replace(i, "negativo/"+str(numero)+".png")

        # Copia a imagem para o repositório negativo e troca o nome da imagem do treinamento para: "Negativa n°".
        shutil.copy(i, i.replace(i, "negativo/"+str(numero)+".png"))

        # Trocando a imagem para a escala cor preto e branco, por questão de necessidade do haar cascade.
        img = cv2.imread("negativo/" + str(numero) + ".png", cv2.IMREAD_GRAYSCALE)

        # redimensionando imagem, por questão de recomendação do proprio haar.
        redimensiona = cv2.resize(img, (800, 600))

        # Sobreescrevendo a imagem inicial.
        cv2.imwrite("negativo/" + str(numero) + ".png", redimensiona)

        print(i.replace(i, "neg/"+str(numero)+".png"))
        
        # Passa próxima imagem
        numero += 1

listaNegImagem()