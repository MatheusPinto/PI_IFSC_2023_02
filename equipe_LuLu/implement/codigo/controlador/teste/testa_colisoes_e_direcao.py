#!/bin/env python3


"""Script de teste da direção e colisão do controlador.

Checa a colisão e direção em um mapa definido pela imagem do parâmetro *IMAGEM_PATH*. Mostra o resultado visualmente para o usuário.

Tem a mesma funcionalidade dos scripts 'testa_colisao.py' e 'testa_direcao.py' realizados juntos.
"""


import test
import modulos.controlador as controlador
import numpy as np
import cv2 as cv


IMAGEM_PATH = "imagens-teste/mapa.png"


if __name__ == "__main__":
    imagem = cv.imread(IMAGEM_PATH)

    if imagem is None:
        print("Não é possível carregar a imagem! abortando programa...")
        exit(1)

    # Cria o mapa com base na imagem
    imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    # Normaliza o mapa para usar no algorítimo A*
    mapa = imagem//255

    # Controlador
    posicoes_esquerda = [
            (-10, -15),
            (-20, -12),
            (-30, -10)
            ]

    ctrl = controlador.Controlador((50, 50), posicoes_esquerda, 3)

    # Processa a imagem
    lista_colisoes, img_colisoes = ctrl.mostra_colisoes(mapa, debug=True)
    linear, angular, imagem = ctrl.calcula_direcao(None, (1, 1), debug=True)

    # Ajusta o mapa para realizar o blend das imagens
    mapa = cv.cvtColor(mapa*255, cv.COLOR_GRAY2BGR)
    mapa = cv.resize(mapa, (50, 50))

    # Mostra a imagem com os indicadores de colisão e direção
    imagem = cv.addWeighted(imagem, 0.5, mapa, 0.5, 0.0)
    cv.imshow("debug", imagem)

    print("lista de colisões:", lista_colisoes)
    print("Linear: {}, Angular: {}".format(linear, angular))

    while True:
        key = cv.waitKey(1)
        if key==ord('q'):
            break
