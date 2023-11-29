#!/bin/env python3


"""Converte o modelo para o formato do tensorflow lite.

O diretório onde está o modelo original deve ser informado pelo parâmetro 'MODELO_PATH'.
O arquivo de destino (onde será salvo o modelo no formato tflite) deve ser informado pelo
parâmetro 'MODELO_TFLITE_PATH'.
"""


import tensorflow as tf
import tensorflow.lite as tflite


# Parâmetros do script
MODELO_PATH = "modelo-segmentacao/modelo"
MODELO_TFLITE_PATH = "modelo-segmentacao.tflite"


if __name__ == "__main__":
    # Converte o modelo para o formato tflite. O arquivo será salvo na variável
    # 'modelo_tflite' em formato binário. Deve ser salvo em um arquivo posteriormente.
    conversor = tflite.TFLiteConverter.from_saved_model(MODELO_PATH)
    modelo_tflite = conversor.convert()

    # Salva o modelo no arquivo definido por 'MODELO_TFLITE_PATH'
    with open(MODELO_TFLITE_PATH, "wb") as f:
        f.write(modelo_tflite)
