#!/bin/env python3


"""Interpretadores de modelos do tensorflow lite.

Está disponível, neste módulo, um modelo de segmentador semântico de imagens
usado para obter a máscara de uma imagem: :class:`Segmentador`.
"""


import tensorflow.lite as tfl
import cv2 as cv
import numpy as np


class Segmentador():
    """Segmentador de imagens.

    É necessário informar o arquivo do modelo (convertido para tflite) ao inferir o objeto.

    Para segmentar a imagem, use o método :meth:`segmenta_imagem()`. Ele retorna o resultado de
    saída do modelo. Se deseja apenas a máscara de objetos colidíveis, use o método :meth:`retorna_mascara()`.

    Para fins de debug, há um método que retorna a imagem unida ao resultado de processamento por meio
    de uma operação de blend. O método é :meth:`retorna_imagem_segmentada`.

    Para carregar o segmentador, é necessário o modelo de segmentação do Tensorflow Lite, conforme instruído
    pelo método :meth:`__init__()`.

    >>> # Carrega o segmentador
    >>> segmentador = Segmentador(MODELO_TFLITE_PATH, N_THREADS)

    Se a imagem fornecida ao segmentador for None, será retornado o resultado da última segmentação.
    Portanto, é possível fazer o seguinte:

    >>> # Obtém o resultado da segmentação, a máscara, e a combinação do resultado com a imagem original
    >>> imagem_segmentadaa = segmentador.segmenta_imagem(imagem)
    >>> mascara = segmentador.retorna_imagem_segmentada(None)
    >>> imagem_com_segmentacao = segmentador.retorna_imagem_segmentada(None)

    Essa abordagem é mais eficiente, visto que utiliza o resultado do último processamento ao invés de
    re-segmentar a imagem.

    Notes
    -----
    A imagem de entrada deve estar no formato RGB. Atenção porque o OpenCV usa o formato BGR. Para converter
    entre eles, use:

    >>> import cv2 as cv
    >>> imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
    """

    def __init__(self, arquivo_ftlite: str, n_threads=1):
        """Carrega o modelo de segmentação de imagem.

        É necessário informar o arquivo do modelo convertido para o Tensorflow Lite, e o número de threads
        que serão usadas para processar o modelo.

        Parameters
        ----------
        arquivo_ftlite : str
            O arquivo do modelo de segmentação convertido para o Tensorflow Lite.

        n_threads : int, default 1
            O número de threads que serão usadas para processar o modelo. O valor padrão é 1.
        """
        # Carrega o modelo (será usado apenas uma thread para o teste)
        self._interpretador = tfl.Interpreter(model_path=arquivo_ftlite, num_threads=n_threads)

        # Configuração básica do modelo, e informação da entrada e saída do modelo
        self._interpretador.allocate_tensors()
        self._entrada_info = self._interpretador.get_input_details()
        self._saida_info = self._interpretador.get_output_details()

        # Formato de entrada
        formato = self._entrada_info[0]["shape"]
        formato = formato[1:]  # Remove o primeiro eixo (ele é sempre 1 para esse modelo)
        self._formato_entrada = tuple(formato)

        # Índice do tensor de entrada e de saída
        self._tensor_entrada_indice = self._entrada_info[0]['index']
        self._tensor_saida_indice = self._saida_info[0]['index']

    def retorna_formato_entrada(self):
        """Retorna o formato de entrada do segmentador.

        Ele é retornado como uma tupla. O formato da imagem utilizada no método 'segmenta_imagem()'
        deve ser igual ao retornado por essa função. Caso contrário, não funcionará.

        Returns
        -------
        tuple
            O formato de entrada do segmentador.
        """
        return self._formato_entrada

    def redimensiona_para_entrada(self, imagem : np.ndarray):
        """Redimensiona a imagem para o formato de entrada do segmentador.

        A imagem apenas é redimensionada se não estiver no formato de entrada do modelo.
        A imagem de entrada deve estar no formato (linhas, colunas, canais).

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser redimensionada.

        Returns
        -------
        numpy.ndarray
            A imagem redimensionada para o formato de entrada do segmentador.
        """
        if imagem.shape != self._formato_entrada:
            imagem = cv.resize(imagem, self._formato_entrada[:2])

        return imagem

    def segmenta_imagem(self, imagem : np.ndarray = None):
        """Segmenta a imagem recebida.

        Retorna o resultado da segmentação sem pós-processamento. Se a imagem for None, será
        retornado o resultado da última segmentação.

        Parameters
        ----------
        imagem : numpy.ndarray, default None
            A imagem a ser segmentada. Se for None, será retornado o resultado da última segmentação.

        Returns
        -------
        numpy.ndarray
            Imagem resultada do processo de segmentação.
        """
        # Se não foi fornecido imagem, retorna o resultado anterior
        if imagem is None:
            return self._resultado_segmentacao

        # Redimensionamento
        imagem = self.redimensiona_para_entrada(imagem)
        self._imagem = imagem

        # Preprocessamento da imagem
        imagem = np.array(imagem, dtype=np.float32)
        imagem /= 255 # Normalização

        # Preprocessamento da imagem. É necessário normalizar e formatar a saída. O formato de entrada
        # do modelo de segmentação tem a dimensão (1, linhas, colunas, canais), A imagem processada possui
        # formato (linhas, colunas, canais), então é necessário adicionar mais um eixo no começo da imagem.
        imagem = np.expand_dims(imagem, axis=0)

        # Segmenta a imagem do dataset. Define o tensor de entrada e realiza a segmentação. O resultado é posto
        # no atributo 'resultado_segmentacao'
        self._interpretador.set_tensor(self._tensor_entrada_indice, imagem)
        self._interpretador.invoke()
        saida = self._interpretador.get_tensor(self._tensor_saida_indice)

        # A máscara é retornada no formato (1, linhas, colunas, canais).
        # Como há apenas uma imagem, é necessário selecionar o primeiro elemento.
        self._resultado_segmentacao = saida[0]

        return self._resultado_segmentacao

    def retorna_mascara(self, imagem : np.ndarray = None):
        """Segmenta a imagem recebida e retorna a máscara de objeto colidível.

        A segmentação é feita usando o método :meth:`segmenta_imagem`. O resultado é a máscara
        de objetos colidível que ele retorna.

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser segmentada. Se for None, será retornado a máscara da última segmentação.

        Returns
        -------
        numpy.ndarray
            Máscara resultada da segmentação.
        """
        mascara = self.segmenta_imagem(imagem)

        # Remove os canais indesejados. Apenas o segundo canal da imagem (índice 1) contém a máscara desejada.
        mascara = mascara[:, :, 1]

        return mascara

    def retorna_imagem_segmentada(self, imagem):
        """Retorna a imagem com a segmentação.

        A imagem é segmentada. O resultado da segmentação é unido a imagem por uma operação de blend.
        O resultado é uma imagem com um filtro de segmentação.

        A segmentação é feita pelo método :meth:`segmenta_imagem`.

        O formato da imagem retornada é igual ao da entrada do modelo de segmentação.

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser segmentada. Se for None, será usado o resultado da última segmentação.

        Returns
        -------
        numpy.ndarray
            A imagem com um filtro de segmentação.
        """
        # Segmentação da imagem
        resultado = self.segmenta_imagem(imagem)

        # Converte a máscara para poder ser unida a imagem
        resultado = np.array(resultado*255, dtype=np.uint8)

        # Justa as duas imagens
        imagem = cv.addWeighted(self._imagem, 0.5, resultado, 0.5, 0.0)

        return imagem
