#!/bin/env python3


"""Modelo usado para segmentação de imagens.

Modelo: U-NET

Baseado no código disponível em: https://pyimagesearch.com/2022/02/21/u-net-image-segmentation-in-keras/

Para criar o modelo de segmentação, use a função :func:`modelo_unet`. É recomendado usar a
'sparse_categorical_crossentropy' como função de perda. Se usado essa função de perda,
não use apenas 1 canal de saída, use 2 pelo menos. Além disso, essa função de perda necessita
que a máscara de treinamento seja do tipo uint8.
"""


import tensorflow as tf


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
    x = tf.keras.layers.Conv2D(n_filtros, 3, padding="same", activation="relu", kernel_initializer="he_normal")(x)
    x = tf.keras.layers.Conv2D(n_filtros, 3, padding="same", activation="relu", kernel_initializer="he_normal")(x)

    return x

def _bloco_entrada(x : tf.Tensor, n_filtros : int):
    """Bloco de entrada do modelo. Aplicado sobre a imagem inicial.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.
    """
    x = tf.keras.layers.DepthwiseConv2D(
            3, padding="same", depth_multiplier=3, activation="relu", kernel_initializer="he_normal"
            )(x)

    x = tf.keras.layers.Conv2D(n_filtros, 3, padding="same", activation="relu", kernel_initializer="he_normal")(x)

    return x

def _bloco_downsample(x : tf.Tensor, n_filtros : int):
    """Bloco que reduz as dimensões (n_linhas, n_colunas) dos dados, enquanto extrai informações deles.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.
    """
    x = _bloco_padrao(x, n_filtros)
    x = tf.keras.layers.MaxPool2D(2)(x)
    x = tf.keras.layers.Dropout(0.3)(x)

    return x

def _codificador(x : tf.Tensor, n_filtros : int, n_downsample : int):
    """Cria o codificador do modelo (camadas de downsample).

    Cria o codificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    O número de operações de downsample do codificador é definido por *n_downsample*. O número de filtros
    (canais) usados nas convoluções é dado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    n_downsample : int
        O número de operações de downsample do codificador.
    """
    saidas_codificador = []

    for n in range(n_downsample):
        saidas_codificador.append(x)
        x = _bloco_downsample(x, n_filtros)
        n_filtros *= 2  # Os filtros são aumentados conforme prossegue o downsample

    return x, saidas_codificador

def _bloco_upsample(x : tf.Tensor, n_filtros : int, saida_codificador : tf.Tensor):
    """Bloco que aumenta as dimensões (n_linhas, n_colunas) dos dados, para formar a máscara.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    saida_codificador : tf.Tensor
        Saida do codificador que será concatenada como fluxo atual do modelo.
    """
    x = tf.keras.layers.Conv2DTranspose(n_filtros, 3, 2, padding="same")(x)
    x = tf.keras.layers.concatenate([x, saida_codificador])

    x = tf.keras.layers.Dropout(0.3)(x)
    x = _bloco_padrao(x, n_filtros)

    return x

def _decodificador(x, n_filtros, saidas_codificador):
    """Cria o decodificador do modelo (camadas de upsample).

    Cria o decodificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

    É necessário fornecer uma lista com todas as saídas do codificador. O bloco de upsample concatena
    essas saídas com as dos blocos anteriores. O número de blocos de upsample é obtido pelo tamanho
    dessa lista.

    O número de filtros (canais) usados nas convoluções é dado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    saida_codificador : list
        Lista com todas as saídas do codificador. O bloco de upsample concatena essas saídas com as dos
        blocos anteriores.
    """
    for saida_codificador in reversed(saidas_codificador):
        x = _bloco_upsample(x, n_filtros, saida_codificador)
        n_filtros /= 2  # Os filtros são reduzidos conforme prossegue o upsample

    return x

def modelo_unet(formato_entrada, canais_saida=3, n_downsample=4):
    """Cria o modelo uNET.

    O formato de entrada deve ser uma tupla do tipo (n_linhas, n_colunas, canais). *n_linhas* e *n_colunas* devem
    ser múltiplos de *2^n_downsample*. Por exemplo, se *n_downsample=4*, devem ser múltiplos de 16, como (32, 64, 3).
    Nesse caso, a imagem é um RGB. Se deseja usar um grayscale, esse número deve ser 1.

    O número de downsample do modelo e, consequentemente, de upsameple é definido pelo parâmetro *n_downsample*.

    Parameters
    ----------
    formato_entrada : tuple
        O formato de entrada do modelo.

    canais_saida : int
        O número de canais de saída do modelo.

    n_downsample : int
        O número de operações de downsample do codificador.
    """
    # Entrada do modelo
    entrada = tf.keras.layers.Input(shape=formato_entrada)
    x = entrada

    # Bloco de entrada
    x = _bloco_entrada(x, 3)

    # Codificador
    x, saidas_codificador = _codificador(x, 8, n_downsample)

    # Bloco entre o codificador e decodificador
    x = _bloco_padrao(x, 512)

    # Decodificador
    x = _decodificador(x, 512, saidas_codificador)

    # Saída do modelo
    x = _bloco_padrao(x, 32)
    x = tf.keras.layers.Conv2D(canais_saida, 1, padding="same", activation = "softmax")(x)

    return tf.keras.Model(inputs=entrada, outputs=x, name="modelo-completo")
