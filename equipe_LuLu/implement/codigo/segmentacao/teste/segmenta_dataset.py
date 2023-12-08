#!/bin/env python3


"""Testa a segmentação de imagens do dataset.

As imagens segmentadas são do dataset definido pelo parâmetro 'DATASET_PATH'. O número
de imagens mostradas é definido pelo parâmetro 'N_LINHAS'.

O path do modelo usado é específicado pelo parâmetro 'MODELO_TFLITE_PATH'.

O número de imagens segmentadas por linha é definido pelo parâmetro 'N_LINHAS'.
"""


import test
import modulos.interpretador as interpretador
from tensorflow.data import Dataset
import matplotlib.pyplot as plt


# Parâmetros do script
MODELO_TFLITE_PATH = "../modelo-segmentacao.tflite"
DATASET_PATH = "../datasets/validacao"
N_LINHAS = 5


if __name__ == "__main__":
    # Carrega o segmentador de imagens (usa apenas uma thread)
    interpretador = interpretador.Segmentador(MODELO_TFLITE_PATH, n_threads=1)

    # Carrega o dataset gerado com o script 'create.py'
    dataset = Dataset.load(DATASET_PATH).shuffle(10000)

    # Segmenta as imagens de teste do dataset de validação
    n_linha = 0
    for imagem, mascara in dataset.take(N_LINHAS):
        # Imagem
        plt.subplot(N_LINHAS, 3, n_linha*3+1)
        plt.imshow(imagem[0].numpy().astype("uint8"))
        plt.axis("off")

        # Máscara esperada
        plt.subplot(N_LINHAS, 3, n_linha*3+2)
        plt.imshow(mascara[0].numpy().astype("uint8"))
        plt.axis("off")

        # Gera a mácara da primeira imagem do batch
        mascara = interpretador.segmenta_imagem(imagem[0])

        # Máscara da segmentação
        plt.subplot(N_LINHAS, 3, n_linha*3+3)
        plt.imshow(mascara)
        plt.axis("off")

        # Próxima linha
        n_linha += 1

    # Títulos das colunas
    plt.subplot(N_LINHAS, 3, 1)
    plt.title("Imagem")

    plt.subplot(N_LINHAS, 3, 2)
    plt.title("Esperado")

    plt.subplot(N_LINHAS, 3, 3)
    plt.title("Obtido")

    # Mostra as imagens e as figuras
    plt.show()
