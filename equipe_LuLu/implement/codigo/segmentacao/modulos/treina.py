#!/bin/env python3


"""Funções de treinamento do modelo de segmentação.

A função responsável por treinar os modelos é a função :func:`treina_modelo`.
"""


import tensorflow as tf
from .preprocessamento import funcao_normalizacao, preprocessa_backbone
import time


# ParÂmetros do treinamento
DATASET_TREINAMENTO_PATH = "datasets/treino"
DATASET_VALIDACAO_PATH = "datasets/validacao"
EPOCHS = 60


class _RestauraSeAcuraciaValidacaoForBaixa(tf.keras.callbacks.Callback):
    """Callback usada no treinamento para restaurá-lo se a acurácia de validação for baixa.

    No final de cada época, checa se a acurácia de validação é muito baixa. Se for, restaura o
    modelo para melhor versão e continua o treinamento.
    """

    def __init__(self, acuracia_minima=0.5):
        """Inicializa a classe de callback.

        Parameters
        ----------
        acuracia_minima : float, default=0.5
            A acurácia mínima aceitável para o treinamento. Se for menor do que isso, restaura os
            parâmetros do modelo.
        """
        super().__init__()

        self._acuracia_minima = acuracia_minima
        self._maior_acuracia = 0.0
        self._melhores_pesos = None

    def on_epoch_end(self, epoca, logs=None):
        """Implementa a execução no final de cada época."""
        # Se não tem nenhum peso salvo como os melhores, considera os atuais como tal
        if self._melhores_pesos == None:
            self._melhores_pesos = self.model.get_weights()
            print("\nPrimeira versão do modelo. Salvando os parâmetros...")

        # Se não conseguir ler a acurácia de validação, mostra um erro indicando ser
        # possível que o dataset de treinamento tenha acabado
        acuracia = logs.get("val_accuracy")

        if acuracia == None:
            raise Exception(
                    """
                    Não foi possível ler a acurácia de validação dessa época!

                    Verifique se o dataset de validação não é muito pequeno e terminou antes.
                    Uma dica importante é utilizar o método. 'repeat()' no dataset para fazê-lo repetí-lo do início caso finalize.

                    Para mais informações, consulte: https://www.tensorflow.org/api_docs/python/tf/data/Dataset#repeat
                    """.lstrip(" ")
                    )
            exit(-2)

        # Se o modelo possuir acurácia de validação maior, salva eles
        elif acuracia > self._maior_acuracia:
            self._maior_acuracia = acuracia

            # Atualiza os parâmetros salvos
            print("\n\n\nVersão atual com melhor acurácia! Atualizando os parâmetros salvos.")
            self._melhores_pesos = self.model.get_weights()

        # Restaura o modelo para o anterior caso a acurácia esteja muito baixa
        elif acuracia < self._acuracia_minima:
            self.model.set_weights(self._melhores_pesos)

            print(
            """
            A acurácia da época atual é de {0:.3f}. Menor do que o mínimo de {1:.3f}.
            Restaurando os parâmetros para os salvos.
            """.format(acuracia, self._acuracia_minima).lstrip(" ")
            )


def treina_modelo(
        modelo : tf.keras.Model, path: str = "modelo-segmentacao",
        backbone: bool = False, acuracia_minima: float = None
        ):
    """Treina um modelo do Tensorflow.

    O modelo é dado pelo parâmetro *modelo*. Deve ser um modelo do Tensorflow pré-carregado. O path dos datasets
    usados para treinamento são dados pelo parâmetro 'DATASET_TREINAMENTO_PATH' e 'DATASET_VALIDACAO_PATH'.

    O treinamento será feito usando o método 'fit()' do *modelo* fornecido.

    Essa função foi feita para criar um registro (log) de todos os modelos treinados. Essa pasta é definida pelo parâmetro
    *path*. Será criado um log na pasta definida por <path>log. Por exemplo, se *path="modelo-segmentacao/"*, o
    log será criado na pasta 'modelo-segmentacao/log/'.

    O dataset é preprocessamento antes de ser aplicado ao modelo. O pré-processamento depende se o modelo
    treinado é um backbone ou o modelo de segmentação. Por isso, é necessário informar isso por meio do
    parâmetro *backbone*.

    O parâmetro *acuracia_minima* define a acurácia mínima aceitável para o treinamento. Os parâmetros são
    restaurados para o melhor treinamento se ocorrer da acurácia de validação cair abaixo desse valor. Se
    for None, não haverá uma acurácia mínima nem mesmo a restauração dos parâmetros.

    A modelo com melhor acurácia é salvo no diretório definido por <path>maior-acuracia/. Por exemplo, se
    *path="modelo-segmentacao/"*, o modelo com melhor acurácia será salvo na pasta
    'modelo-segmentacao/maior-acuracia/'

    Parameters
    ----------
    modelo : tf.keras.Model
        O modelo do Tensorflow que será treinado.

    path : str, default="modelo-segmentacao"
        O path da pasta em que os dados relacionados ao modelo serão salvos.

    acuracia_minima : float, default=None
        A acurácia mínima aceitável para o treinamento. Se for menor do que isso, restaura os parâmetros do modelo.

    Notes
    -----
    A acurácia não é medida durante o treinamento do backbone. Portanto, não defina uma acurácia mínima de
    treinamento para ele. Pelo mesmo motivo, não será salvo o modelo do backbone com maior acurácia.
    """
    # Se treinar apenas o backbone, deve usar a função de normalização dedicada a ele
    if backbone:
        funcao_preprocessamento = preprocessa_backbone

    else:
        funcao_preprocessamento = funcao_normalizacao

    # Carrega os datasets gerados com o script 'create.py' e normaliza para treinamento
    dataset_treinamento = tf.data.Dataset.load(DATASET_TREINAMENTO_PATH)
    dataset_treinamento = dataset_treinamento.map(funcao_preprocessamento)

    dataset_validacao = tf.data.Dataset.load(DATASET_VALIDACAO_PATH)
    dataset_validacao = dataset_validacao.map(funcao_preprocessamento)

    # Configura para usar cache, repetir dados e prefetch
    dataset_treinamento = dataset_treinamento.cache().repeat().prefetch(
            buffer_size=tf.data.experimental.AUTOTUNE
            )

    dataset_validacao = dataset_validacao.repeat().prefetch(
            buffer_size=tf.data.experimental.AUTOTUNE
            )

    # Versão mais atual do modelo
    checkpoint = tf.keras.callbacks.ModelCheckpoint(path + "modelo")

    # Checkpoints do modelo. Apenas atualiza o modelo no arquivo "modelos-segmentacao-maior-acuracia"
    # se a acurácia for maior.
    checkpoint_acuracia = tf.keras.callbacks.ModelCheckpoint(
            path + "maior-acuracia", monitor="val_accuracy" , save_best_only=True
            )

    # Cria um log com todas as versões do modelo, mesmo as com menor acurácia.
    i_treino = path + "log/treino-" + time.strftime("%Y-%m-%d-%Hh%Mmin-%Ss")  # Índice do treinamento

    if backbone:
        i_treino += "/epoca:{epoch:03d}-val_loss:{val_loss:.3f}"
    else:
        i_treino += "/epoca:{epoch:03d}-val_loss:{val_loss:.3f}-val_accuracy:{val_accuracy:.3f}"

    checkpoint_log = tf.keras.callbacks.ModelCheckpoint(i_treino)

    # Funções de callback
    funcoes_callback = [checkpoint, checkpoint_log]

    if not backbone:
        funcoes_callback.append(checkpoint_acuracia)

    # Função de callback que reinicia se a acurácia de validação for menor do que um valor mínimo
    if acuracia_minima != None:
        funcoes_callback.append(_RestauraSeAcuraciaValidacaoForBaixa(acuracia_minima))

    # Treina o modelo
    model_history = modelo.fit(
            dataset_treinamento,
            epochs=EPOCHS,
            steps_per_epoch=250,
            validation_data=dataset_validacao,
            validation_steps=32,
            callbacks=funcoes_callback
            )
