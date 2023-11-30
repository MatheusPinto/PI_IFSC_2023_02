#!/bin/env python3


"""Modelo usado para segmentação de imagens.

Modelo: mobilenet_v3_unet

Baseado no código disponível em: https://www.tensorflow.org/tutorials/images/segmentation

Para criar o modelo de segmentação, use a função :func:`cria_mobilenet_v3_unet`. É recomendado usar a
'sparse_categorical_crossentropy' como função de perda. Se usado essa função de perda,
não use apenas 1 canal de saída, use 2 pelo menos. Além disso, essa função de perda necessita
que a máscara de treinamento seja do tipo uint8.
"""


import tensorflow as tf


def _conv_2D(x, n_filtros, kernel):
    """Aplica um bloco de convolução 2D ao modelo.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    kernel : int
        O tamanho do kernel das convoluções.
    """
    x = tf.keras.layers.Conv2D(n_filtros, kernel, padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    return x

def _bloco_padrao(x : tf.Tensor, n_filtros : int):
    """Aplica um bloco padrão de convoluções ao modelo.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Esse bloco será colocado entre as operações de downsample e upsample.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.
    """
    x = _conv_2D(x, n_filtros, 5)
    x = _conv_2D(x, n_filtros, 4)
    x = _conv_2D(x, n_filtros, 3)

    return x

def _bloco_upsample(x : tf.Tensor, n_filtros : int):
    """Bloco que aumenta as dimensões (n_linhas, n_colunas) dos dados, para formar a máscara.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.
    """
    x = tf.keras.layers.Conv2DTranspose(n_filtros, 3, strides=2, padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.ReLU()(x)

    x = _bloco_padrao(x, n_filtros)

    return x


def cria_mobilenet_v3_unet(formato_entrada : tuple, canais_saida=3):
    """Cria o modelo com mobilenetV3Large como backbone."""
    # Entrada do modelo
    entrada = tf.keras.layers.Input(shape=formato_entrada)
    x = entrada

    # Cria o backbone
    entrada_backbone = (formato_entrada[0], formato_entrada[1], 3)
    saida_backbone = (formato_entrada[0]//64, formato_entrada[1]//64, 15)
    n_classes = saida_backbone[0]*saida_backbone[1]*saida_backbone[2]

    backbone = tf.keras.applications.MobileNetV3Large(
            input_shape=entrada_backbone,
            weights=None,
            classifier_activation=None,
            include_preprocessing=False,
            classes=n_classes
            )

    tf.keras.utils.plot_model(
            backbone,
            to_file="plots/backbone.png",
            show_shapes=True,
            show_dtype=True,
            show_layer_names=True
            )

    # Codificador(saídas)
    nomes_das_saidas = [
            "flatten",      # Camada densa 1x1
            "multiply_18",  # 4x4
            "multiply_13",  # 8x8
            "multiply_1",   # 16x16
            "re_lu_6",      # 32x32
            "re_lu_2"       # 64x64
            ]

    saidas_codificador = [backbone.get_layer(nome).output for nome in nomes_das_saidas]

    # Codificador
    codificador = tf.keras.Model(inputs=backbone.input, outputs=saidas_codificador)
    tf.keras.utils.plot_model(
            codificador,
            to_file="plots/codificador.png",
            show_shapes=True,
            show_dtype=True,
            show_layer_names=True
            )
    
    saidas_codificador = codificador(x)

    # Decodificador
    saidas_codificador[0] = tf.keras.layers.Reshape(saida_backbone)(saidas_codificador[0])
    x = saidas_codificador[0]

    filtros = 256
    for saida in saidas_codificador[1:]:
        x = _bloco_upsample(x, filtros)
        filtros /= 2
        x = tf.keras.layers.Concatenate()([x, saida])

    # Último upsample
    x = tf.keras.layers.Conv2DTranspose(8, 3, strides=2, padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.ReLU()(x)

    x = _bloco_padrao(x, 8)
    x = tf.keras.layers.Conv2D(canais_saida, 3, padding="same")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Softmax()(x)

    return tf.keras.Model(inputs=entrada, outputs=x, name="modelo-completo")
