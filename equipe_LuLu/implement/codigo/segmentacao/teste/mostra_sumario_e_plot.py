#!/bin/env python3


"""Mostra o sumário e plot do modelo.

O diretório do modelo deve ser informado pelo parâmetro 'MODELO_PATH'.

O sumário é apresentado na saída padrão, enquanto o plot do modelo é salvo no arquivo especificado
pelo parâmetro 'PLOT_PATH'.
"""


import tensorflow as tf


MODELO_PATH = "../modelo-segmentacao/modelo"
PLOT_PATH = "../plots/modelo-final.png"


if __name__ == "__main__":
    # Carrega o modelo original
    modelo = tf.keras.models.load_model(MODELO_PATH)

    # Gera o sumário e gráfico
    modelo.summary(expand_nested=True)
    tf.keras.utils.plot_model(
            modelo,
            to_file=PLOT_PATH,
            show_shapes=True,
            show_dtype=True,
            show_layer_names=True
            )
