#!/bin/env python3


"""Funções de preprocessamento de imagem.

A função :func:`funcao_normalizacao()` é usada para normalizar os dados do dataset para poderem
ser usados no treinamento do modelo.
"""


import tensorflow as tf


def funcao_normalizacao(imagem, mascara):
    """Função de normalização das imagens e máscaras.

    A imagens originais possuem valores entre 0 e 255 para seus canais. Elas são ajustadas para que cada
    valor esteja entre 0.0 e 1.0. (tipo float)

    A máscara passa pelo mesmo processo. Além disso, ela é convertida para uint8. Isso é necessário porque a
    função de perda do modelo é a 'sparse_categorical_crossentropy', e ela necessita que os valores esperados
    (máscara) sejam inteiros. Para mais informações, veja:
    https://www.tensorflow.org/api_docs/python/tf/keras/losses/SparseCategoricalCrossentropy

    Parameters
    ----------
    imagem : tf.Tensor
        A imagem a ser normalizada.

    mascara : tf.Tensor
        A máscara a ser preprocessada.

    Returns
    -------
    (tf.Tensor, tf.Tensor)
        A imagem e máscara normalizadas.
    """
    # Ajusta a escala das imagens para valores entre 0 e 1
    imagem = tf.keras.layers.Rescaling(1./255)(imagem)
    mascara = tf.keras.layers.Rescaling(1./255)(mascara)

    # Converte a máscara para um valor inteiro de 8bits sem sinal. A função de perda
    # necessita trabalhar com uma máscara de valores entra 0 e 1 do tipo unt8.
    mascara = tf.cast(mascara, dtype=tf.uint8)
    
    return (imagem, mascara)


def preprocessa_backbone(imagem : tf.Tensor, mascara : tf.Tensor):
    """Preprocessa a imagem e a máscara para o backbone.

    A normalização é feita pela função :func:`funcao_normalizacao`. Após isso, a máscara é ajustada
    para ser usada no modelo do backbone. Como o backbone é um modelo de classificação, a saída não
    é uma imagem, mas sim um tensor unidimensional de escalares indicando uma probabilidade. Por isso,
    essa função computa a média dos elementos da máscara e considera ela uma probabilidade.

    Parameters
    ----------
    imagem : tf.Tensor
        A imagem a ser normalizada.

    mascara : tf.Tensor
        A máscara a ser preprocessada.

    Returns
    -------
    (tf.Tensor, tf.Tensor)
        A imagem e máscara preprocessadas.
    """
    imagem, mascara = funcao_normalizacao(imagem, mascara)

    # A máscara deve estar em float32 para funcionar
    mascara = tf.cast(mascara, tf.float32)

    # A máscara será convertida em um tensor com a média de cada canal
    mascara = tf.math.reduce_mean(mascara, axis=(1, 2))

    return (imagem, mascara)
