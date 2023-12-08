#!/bin/env python3


"""Continua o treinamento do modelo.

O modelo deve ter sido criado previamento pelo script 'cria_modelo.py'.

É necessário informar o diretório onde o modelo está pelo parâmetro 'MODELO_PATH'.

É possível configurar a acurácia mínima do treinamento pelo parâmetro 'ACURACIA_MINIMA'. Se a acurácia de
validação cair para um valor abaixo desse durante o treinamento, os parãmnetros serão restaurados para o
do modelo de melhor acurácia.

Para saber como funciona o treinamento, veja a função :func:`~modulos.treina.treina_modelo` do
módulo :mod:`modulos.treina`.
"""


import tensorflow as tf
import modulos.treina as treina


# Parâmetros do script
MODELO_PATH = "modelo-segmentacao/"
ACURACIA_MINIMA = 0.8


if __name__ == "__main__":
    # carrega o modelo original
    modelo = tf.keras.models.load_model(MODELO_PATH + "modelo")

    # Treina o modelo
    treina.treina_modelo(modelo, MODELO_PATH, acuracia_minima=ACURACIA_MINIMA)
