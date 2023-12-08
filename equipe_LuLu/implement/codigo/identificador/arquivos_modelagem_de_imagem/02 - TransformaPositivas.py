import cv2
import os
from imutils import paths
import shutil

def listaPosImagem():
    """Listas as imagens positivas.
    
    Transforma as imagens positivas (lixo), no formato e cor default do haar-cascade.
    """
    imagemPath = list(paths.list_images('imagens/lixo'))
    
    # Declarando uma variável para na minha pasta de resultados positivos, renomear todos as imagens de 1 ao total.
    numero = 1
    if not os.path.exists('positivo'):
        os.makedirs('positivo')

    for i in imagemPath:
        i.replace(i, "positivo/"+str(numero)+".png")

        # Copia a imagem para o repositório positivo e troca o nome da imagem do treinamento para: "Positivo n°".
        shutil.copy(i, i.replace(i, "positivo/"+str(numero)+".png"))

        # Trocando a imagem para a escala cor preto e branco, por questão de necessidade do haar cascade.
        img = cv2.imread("positivo/" + str(numero) + ".png", cv2.IMREAD_GRAYSCALE)
        
        # redimensionando imagem, por questão de recomendação do proprio haar.
        redimensiona = cv2.resize(img, (100, 100))

        # Sobreescrevendo a imagem inicial.
        cv2.imwrite("positivo/" + str(numero) + ".png", redimensiona)

        print(i.replace(i, "positivo/"+str(numero)+".png"))

        # Passa próxima imagem
        numero += 1

listaPosImagem()

