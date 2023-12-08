#!/bin/env python3


"""Script de teste do processamento do mapa feito pelo controlador.

Testa como o controlador processa um mapa dado pelo parâmetro 'IMAGEM_PATH'. O processamento
também depende do ponto de destino do controlador. Defina ele pelo parãmetro 'PONTO_DESTINO'.
Esse ponto é relativo à imagem. Assim, se a imagem possi tamanho de 300x300. O ponto equivalente
ao centro seria dado por (150, 150).

O resultado esperado está abaixo:

.. image:: /../../../../codigo/controlador/img/teste-processamento-mapa-controlador.png

Fonte: autoria própria.
"""


import test
import modulos.controlador as controlador
import numpy as np
import cv2 as cv


IMAGEM_PATH = "imagens-teste/mapa.png"
PONTO_DESTINO = (1, 1)


if __name__ == "__main__":
    imagem = cv.imread(IMAGEM_PATH)

    if imagem is None:
        print("Não é possível carregar a imagem! abortando programa...")
        exit(1)

    # Cria o mapa e a imagem de debug com base na imagem original
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
    imagem = ctrl.retorna_processamento_mapa(mapa, PONTO_DESTINO)

    # Mostra a imagem com os indicadores de colisão e direção
    cv.imshow("debug", imagem)

    while True:
        key = cv.waitKey(1)
        if key==ord('q'):
            break
