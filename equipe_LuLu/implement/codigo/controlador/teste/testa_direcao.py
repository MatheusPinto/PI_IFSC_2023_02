#!/bin/env python3


"""Script de teste da direção do controlador.

Testa se o controlador consegue definir corretamente a direção.

O mapa é uma imagem definida pelo parâmetro *IMAGEM_PATH*.
"""


import test
import modulos.controlador as controlador
import numpy as np
import cv2 as cv




if __name__ == "__main__":
    imagem = cv.imread("imagens-teste/mapa.png")

    if imagem is None:
        print("Não é possível carregar a imagem! abortando programa...")
        exit(1)

    # Cria o mapa com base na imagem
    imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    # Normaliza o mapa para usar no algorítimo A*
    mapa = imagem//255

    # Controlador
    posicoes_esquerda = [
            (-5, -12),
            (-10, -9),
            (-15, -7)
            ]

    ctrl = controlador.Controlador((50, 50), posicoes_esquerda, 3)

    # Processa a imagem
    linear, angular, imagem = ctrl.calcula_direcao(mapa, (1, 1), debug=True)

    # Ajusta o mapa para realizar o blend das imagens
    mapa = cv.cvtColor(mapa*255, cv.COLOR_GRAY2BGR)
    mapa = cv.resize(mapa, (50, 50))

    # Mostra a imagem com os indicadores de direção
    imagem = cv.addWeighted(imagem, 0.5, mapa, 0.5, 0.0)
    cv.imshow("debug", imagem)

    print("Linear: {}, Angular: {}".format(linear, angular))

    while True:
        key = cv.waitKey(1)
        if key==ord('q'):
            break
