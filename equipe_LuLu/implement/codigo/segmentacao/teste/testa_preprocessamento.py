#!/bin/env python3


"""Testa o preprocessamento do dataset.

O dataset deve ser informado pelo parâmetro 'DATASET_PATH'.
O resultado desse script são os tensores de imagem e de máscara preprocessados.
Informações relevantes como o formato e o dtype dos tensores são apresentadas na saída padrão.
"""


import test
import modulos.preprocessamento as pre
import tensorflow as tf


# Parâmetros do script
DATASET_PATH = "../datasets/validacao"


if __name__ == "__main__":
    # Carrega o dataset e recebe um batch dele
    dataset = tf.data.Dataset.load(DATASET_PATH).shuffle(10000)
    batch = dataset.take(1)
    imagem, mascara = next(iter(batch))

    # Preprocessamento da função de normalização
    nova_imagem, nova_mascara = pre.funcao_normalizacao(imagem, mascara)
    print("Normalização (imagem):", "Formato:", nova_imagem.shape, "dtype:", nova_imagem.dtype)
    print("Normalização (máscara):", "Formato:", nova_mascara.shape, "dtype:", nova_mascara.dtype)

    # Preprocessamento do backbone
    nova_imagem, nova_mascara = pre.preprocessa_backbone(imagem, mascara)
    print("Codificador (imagem):", "Formato:", nova_imagem.shape, "dtype:", nova_imagem.dtype)
    print("Codificador (máscara):", "Formato:", nova_mascara.shape, "dtype:", nova_mascara.dtype)
    print("Nova máscara: ", nova_mascara)
