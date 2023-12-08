#!/bin/env python3


"""Testa a exibição das imagens do dataset.

Exibe as primeiras 'N_IMAGENS' do dataset e suas máscaras. As imagens aparecem na coluna
da esquerda, e as máscaras na coluna da direita.

Defina o path do dataset com o parâmetro 'DATASET_PATH'.
"""


import tensorflow as tf
import matplotlib.pyplot as plt


# Parâmetros do script
DATASET_PATH = "treino"
N_IMAGENS = 5


if __name__ == "__main__":
    # Carrega o dataset gerado com o script 'create.py'
    dataset = tf.data.Dataset.load(DATASET_PATH)

    for imagem, mascara in dataset.take(1):
        imagem = imagem[0].numpy()
        mascara = mascara[0].numpy()

    # Mostra as imagens e suas máscaras. Será separado em duas colunas, as imagens na coluna
    # da esquerda, e as máscaras na coluna da direita. Preenche uma linha por vez.
    linha = 0  # Linha atual
    for imagem, mascara in dataset.take(N_IMAGENS):
        # Imagem
        plt.subplot(N_IMAGENS, 2, linha*2+1)
        plt.imshow(imagem[0].numpy().astype("uint8"))
        plt.axis("off")

        # Máscara
        plt.subplot(N_IMAGENS, 2, linha*2+2)
        plt.imshow(mascara[0].numpy().astype("uint8"))
        plt.axis("off")

        # Próxima linha
        linha += 1

    # Inseri os títulos das colunas
    plt.subplot(N_IMAGENS, 2, 1)
    plt.title("Imagens")

    plt.subplot(N_IMAGENS, 2, 2)
    plt.title("Máscaras")

    # Mostra as imagens e as figuras
    plt.show()

    # Mostra as principais informações do dataset
    imagem = next(iter(dataset))[0]            # Primeira imagem do dataset (separada da máscara)
    n_batches = dataset.cardinality().numpy()  # Número de batches do dataset
    tamanho_batch = imagem.shape[0]            # Número de elementos (imagem + máscara) de um batch

    # Informações do dataset
    print("DATATSET - INFO ")
    print("Path:", DATASET_PATH)
    print("Número de batches:", n_batches)
    print("Tamanho de um batch:", tamanho_batch)
    print("Número aproximado de elementos:", n_batches * tamanho_batch)
