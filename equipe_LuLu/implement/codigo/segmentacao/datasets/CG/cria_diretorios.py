#!/bin/env python3


"""Cria os diretórios das imagens usadas para criar o dataset.

O diretório será criado conforme o parâmetro 'IMAGENS_DATASET_PATH'. Dentro dele, será
criado o diretório 'original/' onde evem estar as imagens originais (não segmentadas) e o
diretório 'mascara/' onde devem estar as correspondentes máscaras das imagens.

Para que uma máscara seja correspondente a uma imagem, os arquivos devem possuir o mesmo nome,
apenas estarão em diretórios diferentes. Por exemplo, o arquivo 'IMAGENS_DATASET_PATH/mascara/1.png' é a máscara o
arquivo 'IMAGENS_DATASET_PATH/original/1.png'.
"""


import shutil
import os


# Parâmetros do script
IMAGENS_DATASET_PATH = "blender-output"


if __name__ == "__main__":
    # Cria o novo diretório onde estarão as imagens e máscaras
    os.mkdir(IMAGENS_DATASET_PATH)

    # Cria os diretórios das imagens e máscaras novas
    os.mkdir(IMAGENS_DATASET_PATH + "/original")
    os.mkdir(IMAGENS_DATASET_PATH + "/mascara")
