#!/bin/env python3


"""Testa a identificação de lixo no vídeo capturado pela webcam.

O teste mostra os lixos identificados com quadrados verdes ao seu redor. O lixo mais próximo é
marcado com um círculo vermelho.
"""


import teste
import modulos.identificador as identificador
import cv2 as cv


if __name__ == "__main__":
    # Capturador de video
    cap = cv.VideoCapture(0)

    # Inicializa o identificador
    ident_lixo = identificador.Identificador("../cascade.xml", (160, 120))

    # Captura um frame
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        classificacao, imagem = ident_lixo.identifica_lixo_proximo(frame, debug=True)

        cv.imshow("Frame", imagem)

        # Espera até apertar 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
