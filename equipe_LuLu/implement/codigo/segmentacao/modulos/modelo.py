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


ATIVACAO = "relu"


def _bloco_treinamento(x : tf.Tensor):
    """Aplica um bloco ajuste ao treinamento ao fluxo atual.

    Aplica Dropout no tensor com o fluxo atual do modelo, parâmetro *x*.
    Isso melhora o treinamento, evitando overfitting.

    O fluxo final (após passar pelo bloco) será retornado pela função.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    Returns
    -------
    tf.Tensor
        Tensor com fluxo atual do modelo (após passar pelo bloco).
    """
    x = tf.keras.layers.Dropout(0.3)(x)

    return x

def _bloco_conv2D(x : tf.Tensor, n_filtros : int):
    """Aplica um bloco de convoluções ao modelo.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
    O fluxo final (após passar pelo bloco) será retornado pela função.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    Returns
    -------
    tf.Tensor
        Tensor com fluxo atual do modelo (após passar pelo bloco).
    """
    x = tf.keras.layers.Conv2D(n_filtros, 3, padding="same", activation=ATIVACAO, kernel_initializer="he_normal")(x)
    x = _bloco_treinamento(x)

    return x

def _bloco_padrao(x : tf.Tensor, n_filtros : int):
    """Aplica um bloco padrão de convoluções ao modelo.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
    O fluxo final (após passar pelo bloco) será retornado pela função.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Esse bloco será colocado entre as operações de downsample e upsample.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    Returns
    -------
    tf.Tensor
        Tensor com fluxo atual do modelo (após passar pelo bloco).
    """
    x = _bloco_conv2D(x, n_filtros)

    return x

def _bloco_downsample(x : tf.Tensor, n_filtros : int):
    """Bloco que reduz as dimensões (n_linhas, n_colunas) dos dados, enquanto extrai informações deles.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
    O fluxo final (após passar pelo bloco) será retornado pela função.

    O número de filtros usados nas convoluções é determinado por *n_filtros*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    n_filtros : int
        O número de filtros usados nas convoluções do bloco padrão.

    Returns
    -------
    tf.Tensor
        Tensor com fluxo atual do modelo (após passar pelo bloco).
    """
    # Downsample por meio de MaxPool2D
    x = tf.keras.layers.MaxPool2D(2)(x)

    x = _bloco_padrao(x, n_filtros)

    return x

def _codificador(x : tf.Tensor, n_filtros : int, n_downsample : int):
    """Cria o codificador do modelo (camadas de downsample).

    Cria o codificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
    O fluxo final (após passar pelo bloco) será retornado pela função. Assim como uma
    lista com todas as saídas do codificador começando pela de maior resolução (equivalente ao fluxo de entrada).

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

    Returns
    -------
    tf.Tensor
        Tensor com fluxo atual do modelo (depois de passar pelo bloco).

    list
        Lista com todas as saídas do codificador (começando pela de maior resolução).
    """
    saidas_codificador = []

    for n in range(n_downsample):
        x = _bloco_downsample(x, n_filtros)
        saidas_codificador.append(x)
        n_filtros = n_filtros*2  # O número de filtros aumenta conforme prossegue o downsample

    return saidas_codificador[-1], saidas_codificador[:-1]

def _bloco_upsample(x : tf.Tensor, n_filtros : int, saida_codificador : tf.Tensor):
    """Bloco que aumenta as dimensões (n_linhas, n_colunas) dos dados, para formar as máscaras.

    Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
    Sua resolução será aumentada. Após isso, ele será combinado com a *saida_codificador* e, o resultado
    será retornado pela função.

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
    # Upsample por meio de convolução transposta
    x = tf.keras.layers.Conv2DTranspose(n_filtros, 3, 2, padding="same", activation=ATIVACAO)(x)
    x = _bloco_treinamento(x)

    # Combinar com a saída do codificador
    x = tf.keras.layers.concatenate([x, saida_codificador])

    x = _bloco_padrao(x, n_filtros)

    return x

def _decodificador(x : tf.Tensor, n_filtros, saidas_codificador):
    """Cria o decodificador do modelo (camadas de upsample).

    Cria o decodificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*, e das saídas do codificador.

    É necessário fornecer uma lista com todas as saídas do codificador. O bloco de upsample combina
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
        n_filtros = n_filtros//2  # O número de filtros será reduzido conforme prossegue o upsample

    return x

def _bloco_saida(x : tf.Tensor, mascaras : int):
    """Cria a camada de saída do modelo.

    Cria a camada de saída do modelo a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
    A saída do modelo (com as máscaras) será retornada por essa função.

    O número de máscaras é dado por *mascaras*.

    Parameters
    ----------
    x : tf.Tensor
        Tensor com o fluxo atual do modelo.

    mascaras : int
        O número de máscaras da saída do modelo.

    Returns
    -------
    tf.Tensor
        Tensor com fluxo atual do modelo e máscaras.
    """
    # Último upsample
    x = tf.keras.layers.Conv2DTranspose(4, 3, 2, padding="same", activation=ATIVACAO)(x)
    x = _bloco_treinamento(x)

    # Define o número de canais de saída
    x = tf.keras.layers.Conv2D(mascaras, 1, padding="same", activation = "softmax")(x)
    x = _bloco_treinamento(x)

    return x


def modelo_unet(formato_entrada, canais_saida=3, n_downsample=4):
    """Cria o modelo uNET.

    O número de downsample do modelo e, consequentemente, de upsameple é definido pelo parâmetro *n_downsample*.

    O formato de entrada deve ser uma tupla do tipo (n_linhas, n_colunas, canais). *n_linhas* e *n_colunas* devem
    ser múltiplos de *2^n_downsample*. Por exemplo, se *n_downsample=4*, devem ser múltiplos de 16, como (32, 64, 3).
    Nesse caso, a imagem é um RGB. Se deseja usar um grayscale, essa tupla deve ser (32, 32, 1).

    O número de saída é definido pelo parâmetro *canais_saida*. Ele determina o número de máscaras de saída do modelo.

    Parameters
    ----------
    formato_entrada : tuple
        O formato de entrada do modelo.

    canais_saida : int
        O número de canais de saída do modelo (número de máscaras).

    n_downsample : int
        O número de operações de downsample do codificador.

    Returns
    -------
    tf.keras.Model
        O modelo criado.
    """
    # Entrada do modelo
    entrada = tf.keras.layers.Input(shape=formato_entrada)
    x = entrada

    # Codificador
    x, saidas_codificador = _codificador(x, 4, n_downsample)

    # Decodificador
    x = _decodificador(x, 128, saidas_codificador)

    #  Bloco antes da saída do modelo
    x = _bloco_saida(x, canais_saida)

    return tf.keras.Model(inputs=entrada, outputs=x, name="modelo-completo")
