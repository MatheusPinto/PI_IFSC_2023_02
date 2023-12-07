#!/bin/env python3


"""Módulo para padronização de imagens.

Não foi colocado junto ao módulo :mod:`~codigo.segmentacao.modulos.preprocessamento` porque o módulo atual será
importado pelo segmentador. Separar ele do de preprocessamento evitar carregar todo o Tensorflow durante a
execução do segmentador.

Para padronizar as imagens, use a função :func:`padroniza_imagem`
"""


from tensorflow.image import per_image_standardization


def padroniza_imagem(imagem):
    """Padroniza a imagem.

    Padroniza a imagem para a entrada do modelo de segmentação. Essa função deve ser usada no tensor da imagem
    usada para o treinamento e no tensor da imagem usada no segmentador.

    Parameters
    ----------
    imagem : tf.Tensor
        A imagem a ser padronizada.

    Returns
    -------
    tf.Tensor
        A imagem padronizada.

    Notes
    -----
    Não utilize essa função na máscara de segmentação. Apenas na imagem original.
    """
    imagem = per_image_standardization(imagem)

    return imagem
