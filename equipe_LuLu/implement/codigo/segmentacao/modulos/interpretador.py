#!/bin/env python3


"""Interpretadores de modelos do tensorflow lite.

Está disponível, neste módulo, um modelo de segmentador semântico de imagens
usado para obter a máscara de uma imagem: :class:`Segmentador`.
"""


from .padronizacao import padroniza_imagem
from tensorflow.math import round as tf_round
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
    >>> mascara = segmentador.retorna_mascara(None)
    >>> imagem_com_segmentacao = segmentador.retorna_imagem_segmentada(None)

    Essa abordagem é mais eficiente, visto que utiliza o resultado do último processamento ao invés de
    re-segmentar a imagem.

    Notes
    -----
    A imagem de entrada deve estar no formato RGB. Atenção porque o OpenCV usa o formato BGR. Para converter
    entre eles, alguns métodos possuem o parâmetro BGR. Por exemplo, o método :meth:`segmenta_imagem()`. Se ele
    for chamado da seguinte forma, a imagem será convertida de BGR para RGB antes de ser segmentada.

    >>> imagem_segmentadaa = segmentador.segmenta_imagem(imagem, BGR=True)
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

        # Formato de saida
        formato = self._saida_info[0]["shape"]
        formato = formato[1:]  # Remove o primeiro eixo (ele é sempre 1 para esse modelo)
        self._formato_saida = tuple(formato)

        # Camada vazia (para completar os canais RGB)
        self._vazio = np.zeros(self._formato_saida[0:2] + (1,), dtype=np.float32)

        # Índice do tensor de entrada e de saída
        self._tensor_entrada_indice = self._entrada_info[0]['index']
        self._tensor_saida_indice = self._saida_info[0]['index']

    def retorna_formato_entrada(self):
        """Retorna o formato de entrada do modelo de segmentadoção.

        As imagens serão redimensionadas para o formato de entrada do segmentador antes de serem fornecidas a ele.
        Esse método fornece esse formato de entrada.

        O formato retornado é do tipo: (linhas, colunas, canais).

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
            imagem = cv.resize(imagem, self._formato_entrada[:2][::-1])

        return imagem

    def define_imagem(self, imagem : np.ndarray, BGR = False):
        """Define a imagem a ser segmentada.

        A imagem deve ser um RGB com o formato (linhas, colunas, canais). Se a imagem for fornecida no
        formato BGR, use o parâmetro *BGR* iagual a True. O segmentador se encarrega de converter para RGB.

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser segmentada.

        BGR : bool, default False
            Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.
        """
        # Apenas define uma nova imagem se não recebeu None. A imagem e suas derivadas são salvas no
        # formato RGB nos atributos '_imagem' e '_imagem_sem_redimensionar'.
        if imagem is not None:
            self._reinicia_iteracao()

            # O segmentador opera com imagens no formato RGB
            if BGR:
                imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)

            # Salva uma versão da imagem sem redimensionar
            self._imagem_sem_redimensionar = imagem
            self._formato_imagem = imagem.shape

            # Redimensionamento
            self._imagem = self.redimensiona_para_entrada(imagem)

    def segmenta_imagem(self, imagem : np.ndarray = None, BGR=False, redimensiona=False):
        """Segmenta a imagem recebida.

        Retorna o resultado do modelo de segmentação sem pós-processamento. Se a imagem for None, será
        retornado o resultado da última segmentação.

        Se *redimensiona* for True, o resultado da segmentação é redimensionado para o tamanho do frame original
        antes de ser retornado. Caso False, o resultado do modelo de segmentação não será redimensionado.

        Parameters
        ----------
        imagem : numpy.ndarray, default None
            A imagem a ser segmentada. Se for None, será retornado o resultado da última segmentação.

        BGR : bool, default False
            Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.

        redimensiona : bool, default False
            Se True, o resultado da segmentação é redimensionado para o tamanho do frame original
            antes de ser retornado. Caso False, o resultado da do modelo de segmentação não será redimensionado.

        Returns
        -------
        numpy.ndarray
            Resultado do modelo de segmentação.
        """
        self.define_imagem(imagem, BGR)

        if redimensiona:
            return self._computa_segmentacao_redimensionada()

        else:
            return self._computa_segmentacao()

    def retorna_mascara(self, imagem : np.ndarray = None, BGR=False, redimensiona=False):
        """Segmenta a imagem recebida e retorna a máscara de objeto colidível.

        Semelhante ao método :meth:`segmenta_imagem()`, mas retorna a máscara de objetos colidíveis.

        Os parâmetros *BGR* e *redimensiona* são equivalentes aos do método :meth:`segmenta_imagem()`.

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser segmentada. Se for None, será retornado a máscara da última segmentação.

        BGR : bool, default False
            Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.

        redimensiona : bool, default False
            Se True, o resultado da segmentação é redimensionado para o tamanho do frame original
            antes de ser retornado. Caso False, o resultado da do modelo de segmentação não será redimensionado.

        Returns
        -------
        numpy.ndarray
            Máscara resultada da segmentação.
        """
        self.define_imagem(imagem, BGR)

        if redimensiona:
            return self._computa_mascara_redimensionada()

        else:
            return self._computa_mascara()

    def retorna_imagem_segmentada(self, imagem, BGR=False, redimensiona=False):
        """Retorna a imagem com a segmentação.

        A imagem é segmentada. O resultado da segmentação é unido a imagem por uma operação de blend.
        O resultado é uma imagem com um filtro de segmentação. A imagem é retornada no formato RGB.

        Os parâmetros *BGR* e *redimensiona* são equivalentes aos do método :meth:`segmenta_imagem()`.

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser segmentada. Se for None, será usado o resultado da última segmentação.

        BGR : bool, default False
            Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.

        redimensiona : bool, default False
            Se True, a imagem com a segmentação é redimensionado para o tamanho do frame recebido originalmente
            antes de ser retornado. Caso False, a imagem com a segmentação será retornada com o formato da
            saída do modelo de segmentação.

        Returns
        -------
        numpy.ndarray
            A imagem com um filtro de segmentação (formato RGB).
        """
        self.define_imagem(imagem, BGR)

        if redimensiona:
            return self._computa_imagem_segmentada_redimensionada()

        else:
            return self._computa_imagem_segmentada()

    def _reinicia_iteracao(self):
        """Reinicia a iteração do segmentador.

        O segmentador é reiniciado para uma nova segmentação. Os dados anteriores são apagados.

        Esse método também pode ser usado para iniciar os atributos referentes a uma iteração.
        """
        # Imagem a ser segmentada
        self._imagem_sem_redimensionar = None
        self._formato_imagem = None
        self._imagem = None

        # Segmentação
        self._resultado_segmentacao = None
        self._resultado_segmentacao_sem_arredondamento = None
        self._resultado_segmentacao_redimensionada = None

        # Máscara
        self._mascara = None
        self._mascara_redimensionada = None

        # Imagem com segmentação
        self._imagem_segmentada = None
        self._imagem_segmentada_redimensionada = None

    def _computa_segmentacao(self):
        """Computa a segmentação da imagem recebida.

        Retorna o resultado do modelo de segmentação sem pós-processamento. Se a imagem for None, será
        retornado o resultado da última segmentação.

        Returns
        -------
        numpy.ndarray
            Resultado do modelo de segmentação.
        """
        # Não é necessário executar esse processo se já foi feito nessa iteração
        if self._resultado_segmentacao is not None:
            return self._resultado_segmentacao

        imagem = self._imagem

        # Preprocessamento da imagem
        imagem = np.array(imagem, dtype=np.float32)
        imagem = padroniza_imagem(imagem)

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
        saida = saida[0]
        
        # Cria o canal faltando para ser um RGB
        if self._formato_saida[2] < 3:
            saida = np.concatenate([saida, self._vazio], axis=2)

        # Salva a versão sem arredondamento da imagem
        self._resultado_segmentacao_sem_arredondamento = saida

        # Salva a versão com arredondamento da imagem
        self._resultado_segmentacao = tf_round(saida)

        return self._resultado_segmentacao

    def _computa_segmentacao_redimensionada(self):
        """Computa a segmentação da imagem e redimensiona para o tamanho do frame original.

        Semelhante ao método :meth:`_computa_segmentacao`, mas o resultado é redimensionado
        para o tamanho do frame original antes de ser retornado.

        Returns
        -------
        numpy.ndarray
            Resultado do modelo de segmentação (redimensionada para o formato original).
        """
        # Não é necessário executar esse processo se já foi feito nessa iteração
        if self._resultado_segmentacao_redimensionada is not None:
            return self._resultado_segmentacao_redimensionada

        self._computa_segmentacao()

        # Redimensiona a imagem e arredonda
        segmentacao = cv.resize(self._resultado_segmentacao_sem_arredondamento, (self._formato_imagem[:2][::-1]))
        self._resultado_segmentacao_redimensionada = tf_round(segmentacao)

        return self._resultado_segmentacao_redimensionada

    def _computa_mascara(self):
        """Computa a máscara de objetos colidíveis.

        Semelhante ao método :meth:`_computa_segmentacao()`, mas retorna apenas máscara de objetos colidíveis.

        Returns
        -------
        numpy.ndarray
            A máscara de objetos colidíveis.
        """
        # Não é necessário executar esse processo se já foi feito nessa iteração
        if self._mascara is not None:
            return self._mascara
        
        self._computa_segmentacao()

        # Remove os canais indesejados. Apenas o segundo canal da imagem (índice 1) contém a máscara desejada (colisões).
        self._mascara = self._resultado_segmentacao[:, :, 1]

        return self._mascara

    def _computa_mascara_redimensionada(self):
        """Computa a máscara de objetos colidíveis e redimensiona ela para o tamanho do frame original.

        Semelhante ao método :meth:`_computa_segmentacao_redimensionada()`, mas retorna apenas máscara de
        objetos colidíveis. 

        Returns
        -------
        numpy.ndarray
            A máscara de objetos colidíveis (redimensionada para o formato do frame original).
        """
        # Não é necessário executar esse processo se já foi feito nessa iteração
        if self._mascara is not None:
            return self._mascara
        
        self._computa_segmentacao_redimensionada()

        # Remove os canais indesejados. Apenas o segundo canal da imagem (índice 1) contém a máscara desejada (colisões).
        self._mascara_redimensionada = self._resultado_segmentacao_redimensionada[:, :, 1]

        return self._mascara_redimensionada

    def _computa_imagem_segmentada(self):
        """Computa a imagem com a segmentação adicionada a ela.

        Semelhante ao método :meth:`_computa_segmentacao()`, mas retorna a imagem original unida ao
        resultado do modelo de segmentação por meio de uma operação de blend.

        Returns
        -------
        numpy.ndarray
            A imagem unida ao resultado do modelo de segmentação.
        """
        # Não é necessário executar esse processo se já foi feito nessa iteração
        if self._imagem_segmentada is not None:
            return self._imagem_segmentada

        resultado = self._computa_segmentacao()

        # Converte o resultado para poder ser unido a imagem
        resultado = np.array(resultado*255, dtype=np.uint8)

        # Junta as imagem com uma operação de blend
        self._imagem_segmentada = cv.addWeighted(self._imagem, 0.5, resultado, 0.5, 0.0)

        return self._imagem_segmentada

    def _computa_imagem_segmentada_redimensionada(self):
        """Computa a imagem com a segmentação adicionada a ela (redimensionada).

        Semelhante ao método :meth:`_computa_segmentacao_redimensionada()`, mas retorna a imagem
        original unida ao resultado do modelo de segmentação por meio de uma operação de blend.

        Returns
        -------
        numpy.ndarray
            A imagem unida ao resultado do modelo de segmentação (redimensionada para o formato
            da imagem original).
        """
        # Não é necessário executar esse processo se já foi feito nessa iteração
        if self._imagem_segmentada_redimensionada is not None:
            return self._imagem_segmentada_redimensionada

        resultado = self._computa_segmentacao_redimensionada()

        # Converte o resultado para poder ser unido a imagem
        resultado = np.array(resultado*255, dtype=np.uint8)

        # Junta as imagens com uma operação de blend
        self._imagem_segmentada_redimensionada = cv.addWeighted(
                self._imagem_sem_redimensionar, 0.5, resultado, 0.5, 0.0
                )

        return self._imagem_segmentada_redimensionada
