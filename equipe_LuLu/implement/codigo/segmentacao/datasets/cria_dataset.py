#!/bin/env python3


"""Cria o dataset de treino para segmentação.

Utiliza imagens e suas respectivas máscaras na pasta definda pelo parâmetro 'DATASETS_PATH' para gerar
um dataset do tensorflow que será usado para treinar o algorítimo de segmentação de imagens. Elas são
carregadas em datasets separados (um para imagens e outro para as máscaras) e unidas depois. Cada
elemento do novo dataset será um conjunto com a imagem original e sua respectiva máscara, nessa ordem.

Para criar um dataset, é necessário preparar as imagens originais e a máscara em uma pasta. Por exemplo,
"data/". As imagens originais devem estar dentro da pasta "data/original" e as máscaras, dentro de
"pasta/mascara". Os nomes das imagens devem ser iguais aos das suas respectivas máscaras. Por exemplo, a
imagem "pasta/original/1.png" tem uma máscara dada por "pasta/mascara/1.png". Para formar um dataset com
essas imagens, basta adicionar a pasta "pasta/" ao diretório dado pelo parâmetro 'DATASETS_PATH'. É possível
haver mais de uma pasta com imagens e suas máscaras entro desse diretório.

Outro parâmetro importante é o formato das imagens, definido por 'FORMATO_IMAGENS'. O tamanho das imagens
é uma tupla do tipo (n_linhas, n_colunas), em pixels. Ele será usado no melhoramento do dataset.
"""


import tensorflow as tf
import matplotlib.pyplot as plt
import shutil
import os


# Parâmetros do script
DATASETS_PATH = "imagens-dataset"
TREINO_PATH = "treino"
VALIDACAO_PATH = "validacao"
FORMATO_IMAGENS = (128, 128)  # (n_colunas, n_linhas)
TAMANHO_BATCH = 16


def melhora_dataset(imagem : tf.Tensor, mascara : tf.Tensor):
    """Melhora os elementos do dataset.

    O melhoramento do dataset consiste em:
    - Espelhamento horizontal
    - Espelhamento vertical
    - Rotação
    - Brilho
    - Contraste

    Todos esses fatores são ajustados na imagem original para diversificar o dataset. A máscara
    será ajustada para corresponder com a imagem original ajustada.

    Essa função foi feita para ser usada junto ao método 'map()' do datasets do Tensorflow.

    Parameters
    ----------
    imagem : tf.Tensor
        A imagem a ser melhorada.

    mascara : tf.Tensor
        A máscara a ser melhorada.

    Returns
    -------
    (tf.Tensor, tf.Tensor)
        A imagem e a máscara melhoradas.
    """
    # Redimensiona para o formato definido por FORMATO_IMAGENS
    imagem = tf.image.resize(imagem, FORMATO_IMAGENS)
    mascara = tf.image.resize(mascara, FORMATO_IMAGENS)

    # Espelhamento na horizontal
    if tf.random.uniform(()) > 0.5:
        imagem = tf.image.flip_left_right(imagem)
        mascara = tf.image.flip_left_right(mascara)

    # Espelhamento na vertical
    if tf.random.uniform(()) > 0.5:
        imagem = tf.image.flip_up_down(imagem)
        mascara = tf.image.flip_up_down(mascara)

    # Rotação
    sentido_rotacao = tf.random.uniform((), minval=0, maxval=4, dtype=tf.int32)
    while sentido_rotacao > 0:
        sentido_rotacao -= 1
        imagem = tf.image.rot90(imagem)
        mascara = tf.image.rot90(mascara)

    # Brilho
    if tf.random.uniform(()) < 0.5:
        imagem = tf.image.random_brightness(imagem, max_delta=0.8)

    # Contraste
    if tf.random.uniform(()) < 0.5:
        imagem = tf.image.random_contrast(imagem, lower=0.6, upper=0.8)

    # Ajuste de escala (operação de crop)
    if tf.random.uniform(()) < 0.25:
        # Escolhe aleatoriamente as coordenadas de início para o crop
        crop_formato = (90, 90)
        start_x = tf.random.uniform(shape=[], maxval=imagem.shape[1] - crop_formato[0], dtype=tf.int32)
        start_y = tf.random.uniform(shape=[], maxval=imagem.shape[2] - crop_formato[1], dtype=tf.int32)

        # Realiza operação de crop na imagem e máscara
        imagem = tf.image.crop_to_bounding_box(imagem, start_x, start_y, crop_formato[0], crop_formato[1])
        mascara = tf.image.crop_to_bounding_box(mascara, start_x, start_y, crop_formato[0], crop_formato[1])

        # Redimensiona para o formato original
        imagem = tf.image.resize(imagem, FORMATO_IMAGENS)
        mascara = tf.image.resize(mascara, FORMATO_IMAGENS)

    return (imagem, mascara)


def cria_datatset_pasta(path: str):
    """Cria um dataset de um conjunto de imagens e suas respectivas máscaras.

    As imagens devem estar do diretório dado pelo parâmetro *path*. As imagens originais devem estar dentro
    da pasta "<path>/original", e suas máscaras na pasta "<path>/mascara/".

    Elas serão carregadas e unidas em um dataset do tensorflow em que cada elemnto corrsponde a uma par da
    imagem original com sua respectiva máscara.

    Parameters
    ----------
    path : str
        O diretório do conjunto de imagens.
    """
    # Cria os dataset das imagens e máscaras individualmente (serão unidos depois). A opção shuffle=false é
    # importante para que o dataset não seja randomizado antes de se unir às máscaras. Isso permite ligar
    # cada imagem a sua respectiva máscara.
    dataset_imagens = tf.keras.utils.image_dataset_from_directory(
        path + "/original",
        label_mode=None,
        color_mode="rgb",
        batch_size=TAMANHO_BATCH,
        image_size=FORMATO_IMAGENS,
        shuffle=False,
    )

    # As máscaras estão no formato grayscale. (branco significa que é colidível e preto, que NÃO é colidível)
    dataset_mascaras = tf.keras.utils.image_dataset_from_directory(
        path + "/mascara",
        label_mode=None,
        color_mode="grayscale",
        batch_size=TAMANHO_BATCH,
        image_size=FORMATO_IMAGENS,
        shuffle=False,
    )

    # Junta os dois datasets. Cada elemento do novo dataset será uma tupla dos elementos de
    # mesmo índice dos datasets 'dataset_imagens' e 'dataset_mascaras'. Exemplo: (imagem, mascara)
    dataset = tf.data.Dataset.zip(dataset_imagens, dataset_mascaras)

    return dataset


if __name__ == "__main__":
    # Cria o dataset inicial com uma das pastas de imagens
    pastas_imagens = os.listdir(DATASETS_PATH)
    pastas_imagens.remove(".gitkeep")
    dataset = cria_datatset_pasta(DATASETS_PATH + '/' + pastas_imagens[0])

    # Adiciona, ao dataset, as demais pastas
    for pasta in pastas_imagens[1:]:
        novo_datatset = cria_datatset_pasta(DATASETS_PATH + '/' + pasta)
        dataset = dataset.concatenate(novo_datatset)

    # Cria o dataset de validação
    dataset_validacao = dataset.shuffle(10000).take(200)

    try:
        shutil.rmtree(VALIDACAO_PATH)  # Remove o dataset antigo

    except FileNotFoundError:  # Se ainda não existe o dataset
        pass

    dataset_validacao.save(VALIDACAO_PATH)


    # Melhora o dataset
    dataset = dataset.map(melhora_dataset)

    # Aleatoriza a ordem dos elementos do dataset
    dataset = dataset.shuffle(10000)

    # Apaga o antigo dataset e salva o novo
    try:
        shutil.rmtree(TREINO_PATH)  # Remove o dataset antigo

    except FileNotFoundError:  # Se ainda não existe o dataset
        pass

    dataset.save(TREINO_PATH)
