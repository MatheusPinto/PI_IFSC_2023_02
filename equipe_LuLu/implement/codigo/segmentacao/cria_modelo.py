#!/bin/env python3


"""Cria o modelo de segmentação.

O modelo do backbone será salvo no diretório 'modelo-segmentacao/', e plotado no
em 'plots/modelo-final.png'.

Assim que o modelo é criado, ele já é treinado. Para saber como funciona o
treinamento, veja a função :func:`~codigo.segmentacao.modulos.treina.treina_modelo` do
módulo :mod:`codigo.segmentacao.modulos.treina`.
"""


import modulos.modelo as modelo
import modulos.treina as treina
import tensorflow as tf


if __name__ == "__main__":
    # Cria o modelo
    m = modelo.modelo_unet( (128, 128, 3), 3, 7)

    # Gera o sumário e gráfico do modelo
    m.summary(expand_nested=True)
    tf.keras.utils.plot_model(
            m,
            to_file="plots/modelo-final.png",
            show_shapes=True,
            show_dtype=True,
            show_layer_names=True
            )

    # Compila o modelo
    m.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics="accuracy"
            )

    # Inicia o treinamento do modelo. O modelo é salvo conforme as epocas do treinamento passam.
    treina.treina_modelo(m, "modelo-segmentacao/")
