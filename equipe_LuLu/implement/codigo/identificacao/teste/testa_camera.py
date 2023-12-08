#!/bin/env python3


"""Testa a identificação de lixo no vídeo capturado pela webcam.

O teste mostra os lixos identificados e qual é o mais próximo. As marcações são feitas de acordo com os
métodos :meth:`~codigo.identificacao.modulos.identificador.Identificador.identifica_lixo_mais_proximo()`
e :meth:`~codigo.identificacao.modulos.identificador.Identificador.identifica_lixos()`. Ambos da classe
:class:`~codigo.identificacao.modulos.identificador.Identificador`.

O modelo de Haar cascade é definido pelo parâmetro 'CASCADE'.

Resultado experado:

.. image:: /../../../../codigo/identificacao/img/teste-deteccao-webcam.gif

Fonte: autoria própria.
"""


import teste
import modulos.identificador as identificador
import cv2 as cv


CASCADE = "../cascade-leite.xml"


if __name__ == "__main__":
    # Capturador de video
    cap = cv.VideoCapture(0)

    # Inicializa o identificador
    ident_lixo = identificador.Identificador(CASCADE, (160, 120))

    # Captura um frame
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        classificacao = ident_lixo.identifica_lixo_mais_proximo(frame, debug=True)

        cv.imshow("Frame", ident_lixo.retorna_imagem_debug())

        # Espera até apertar 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
