#!/bin/env python3


"""Script de teste do caminho obtido pelo controlador.

Testa se o controlador consegue traçar o caminho corretamente até o ponto especificado pelo parâmetro *PONTO_DESTINO*.
O mapa é uma imagem definida pelo parâmetro *IMAGEM_PATH*.

O resultado esperado está abaixo:

.. image:: /../../../../codigo/controlador/img/teste-caminho.png

Fonte: autoria própria.
"""


import test
import modulos.controlador as controlador
import numpy as np
import cv2 as cv


IMAGEM_PATH = "imagens-teste/mapa.png"
PONTO_DESTINO = (1, 1, 30, 30)


if __name__ == "__main__":
    imagem = cv.imread(IMAGEM_PATH)

    if imagem is None:
        print("Não é possível carregar a imagem! abortando programa...")
        exit(1)

    # Cria o mapa e a imagem de debug com base na imagem original
    img_debug = cv.resize(imagem, (500, 500))
    imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    # Normaliza o mapa para usar no algorítimo A*
    mapa = imagem//255

    # Controlador
    posicoes_esquerda = [
            (-10, -15),
            (-20, -12),
            ]

    ctrl = controlador.Controlador((50, 50), posicoes_esquerda, 3, 10)

    # Processa a imagem
    ctrl.define_mapa(mapa, img_debug)
    lista_colisoes = ctrl.mostra_colisoes(None, debug=True)
    linear, angular, sinalizacao = ctrl.calcula_direcao(None, PONTO_DESTINO, debug=True)

    # Mostra a imagem com os indicadores de colisão e direção
    cv.imshow("debug", ctrl.retorna_imagem_debug())

    print("lista de colisões:", lista_colisoes)
    print("Linear: {}, Angular: {}, Sinalização: {}".format(linear, angular, sinalizacao))

    while True:
        key = cv.waitKey(1)
        if key==ord('q'):
            break
