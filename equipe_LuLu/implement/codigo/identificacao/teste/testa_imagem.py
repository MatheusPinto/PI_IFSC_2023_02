#!/bin/env python3


"""Testa a identificação de lixo em uma imagem.

O teste mostra os lixos identificados com quadrados verdes ao seu redor. O lixo mais próximo é
marcado com um círculo vermelho.

A imagem é definida pelo parâmetro 'IMAGEM'.
"""


import teste
import modulos.identificador as identificador
import cv2 as cv
import os


IMAGEM = "imagens-teste/imagem.png"


if __name__ == "__main__":
    # Inicializa o identificador
    ident_lixo = identificador.Identificador("../cascade.xml", (160,120))

    # Carrega a imagem
    frame = cv.imread(IMAGEM)

    # Testa se carregou a imagem
    if frame is None:
        raise Exception(f"Imagem {IMAGEM} não encontrada")

    # Classificação
    classificacao, imagem = ident_lixo.identifica_lixo_proximo(frame, debug=True)

    cv.imshow("Frame", imagem)

    # Espera até apertar 'q'
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
