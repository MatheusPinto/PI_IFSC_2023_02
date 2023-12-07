#!/bin/env python3


"""Testa a identificação de lixo mais próximo em uma imagem.

Semelhante ao script :mod:`~codigo.identificacao.teste.testa_imagem`, mas esse teste mostra os lixos
identificados e qual é o mais proximo.

A imagem é definida pelo parâmetro 'IMAGEM'. O modelo de Haar cascade é definido pelo parâmetro 'CASCADE'.

O teste mostra os lixos identificados e qual é o mais próximo. As marcações são feitas de acordo com os
métodos :meth:`~codigo.identificacao.modulos.identificador.Identificador.identifica_lixo_mais_proximo()`
e :meth:`~codigo.identificacao.modulos.identificador.Identificador.identifica_lixos()`. Ambos da classe
:class:`~codigo.identificacao.modulos.identificador.Identificador`.

Resultado experado:

.. image:: /../../../../codigo/identificacao/img/imagem-identificacao-mais-proxima.png

Fonte: autoria própria.
"""


import teste
import modulos.identificador as identificador
import cv2 as cv
import os


IMAGEM = "imagens-teste/imagem.png"
CASCADE = "../cascade-leite.xml"


if __name__ == "__main__":
    # Inicializa o identificador
    ident_lixo = identificador.Identificador(CASCADE, (160, 120))

    # Carrega a imagem
    frame = cv.imread(IMAGEM)

    # Testa se carregou a imagem
    if frame is None:
        raise Exception(f"Imagem {IMAGEM} não encontrada")

    # Classificação
    classificacao = ident_lixo.identifica_lixo_mais_proximo(frame, debug=True)

    cv.imshow("Frame", ident_lixo.retorna_imagem_debug())

    # Espera até apertar 'q'
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
