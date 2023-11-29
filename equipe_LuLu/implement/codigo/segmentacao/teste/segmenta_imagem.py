#!/bin/env python3


"""Testa a segmentação de imagens.

As imegens devem estar dentro do diretório específicado por 'IMAGENS_PATH'.

O path do modelo usado é específicado pelo parâmetro 'MODELO_TFLITE_PATH'.
"""


import test
import modulos.interpretador as interpretador
import matplotlib.pyplot as plt
import os
import cv2 as cv
import numpy as np


# Parâmetros do script
IMAGENS_PATH = "imagens-test/"
MODELO_TFLITE_PATH = "../modelo-segmentacao.tflite"


if __name__ == "__main__":
    # Carrega o segmentador de imagens (usa apenas uma thread)
    interpretador = interpretador.Segmentador(MODELO_TFLITE_PATH, n_threads=1)

    # Informações das imagens
    arquivos_imagens = os.listdir(IMAGENS_PATH)
    arquivos_imagens.remove(".gitkeep")
    n_imagens = len(arquivos_imagens)

    n_linha = 0
    for arquivo in arquivos_imagens:
        # Carrega a imagem e ajusta o formato
        imagem = cv.imread(IMAGENS_PATH + '/' + arquivo)
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)

        # Segmenta as imagens de teste
        mascara = interpretador.segmenta_imagem(imagem)

        # Mostra a imagem original
        plt.subplot(n_imagens, 2, n_linha*2 + 1)
        plt.imshow(imagem)
        plt.axis("off")

        # Mostra a máscara da imagem
        plt.subplot(n_imagens, 2, n_linha*2 + 2)
        plt.imshow(mascara)
        plt.axis("off")

        # próxima linha
        n_linha += 1

    # Títulos
    plt.subplot(n_imagens, 2, 1)
    plt.title("Imagem")

    plt.subplot(n_imagens, 2, 2)
    plt.title("Resultado")

    # Mostra as imagens e as máscaras
    plt.show()
