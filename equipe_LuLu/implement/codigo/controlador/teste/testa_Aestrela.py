#!/bin/env python3


"""Script de teste do algorítimo A-estrela.

Utiliza a imagem definida pelo parâmetro *IMAGEM_PATH* como um mapa para o algorítimo A-estrela.

Mostra esse mapa, sua versão expandida, o mapa de custo computado, as regiões checadas pelo A-estrela,
o caminho percorrido pelo algorítimo, além do resultado final (mapa original mais caminho gerado). Todos
esses mapas são concatenados e mostrados em uma única imagem.

O resultado esperado está abaixo:

.. image:: /../../../../codigo/controlador/img/teste-Aestrela.png

Fonte: autoria própria.
"""


import test
import modulos.aestrela as aestrela
import numpy as np
import cv2 as cv


IMAGEM_PATH = "imagens-teste/mapa.png"
POS_FINAL = (1, 1)


if __name__ == "__main__":
    imagem = cv.imread(IMAGEM_PATH)

    if imagem is None:
        print("Não é possível carregar a imagem! abortando programa...")
        exit(1)

    # Cria o mapa com base na imagem
    imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    # Redimensiona para usar no A*
    imagem = cv.resize(imagem, (50, 50))

    # Normaliza o mapa para usar no algorítimo A*
    mapa = imagem//255

    # Posição de início
    pos_inicial = (mapa.shape[0]-1, mapa.shape[1]//2)

    # Aumenta a área das regiões colidíveis (paredes)
    mapa_expandido = cv.GaussianBlur(mapa*255, (19, 19), 5)
    mapa_expandido = np.floor(mapa_expandido/255 + 0.8)
    mapa_expandido = np.array(mapa_expandido, dtype=np.uint8)

    # Máscara de custo
    custo = cv.GaussianBlur(mapa_expandido*255, (21, 21), 7)

    # Processa o mapa
    tracador_caminho = aestrela.AEstrela()
    tracador_caminho.define_mapas(mapa_expandido, custo*5.0)
    mapa_caminho = tracador_caminho.gera_caminho_mapa_smoothing(pos_inicial, POS_FINAL)
    angulo = tracador_caminho.retorna_direcao_inicial(pos_inicial, POS_FINAL, rad=False)

    # Se não consegue traçar um caminho
    if mapa_caminho is None:
        mapa_caminho = np.zeros(mapa.shape, dtype=np.uint8)

    # Mapa com todas as regiões checadas pelo algorítimo
    mapa_checados = tracador_caminho.retorna_mapa_checados()

    # Mostra a imagem resultante
    im0 = cv.hconcat([mapa*255, mapa_expandido*255])
    im1 = cv.hconcat([custo, mapa_checados*255])
    im2 = cv.hconcat([mapa_caminho*255, mapa_caminho*255+mapa*255])

    resultado = cv.vconcat([im0, im1, im2])

    cv.imshow("resultado", resultado)

    # Finaliza o programa quando pressionar 'q'
    while True:
        key = cv.waitKey(1)
        if key==ord('q'):
            break
