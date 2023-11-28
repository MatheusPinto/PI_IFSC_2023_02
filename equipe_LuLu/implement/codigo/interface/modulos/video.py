#!/bin/env python3


"""Módulo de captura de vídeo.

Implementa a captura de frames da webcam. Além disso, é possível codificar os frames em um array de bytes para serem
enviados pela rede; e decodificar esses próprios bytes de volta para o frame original.

Para capturar os frames da câmera, utilize a classe :class:`Camera`. Essa classe ajusta seu funcionamento para
reconhecer a Webcam automaticamente na Raspberry Pi.

Para codificar e decodificar o frame, utilize as funções :func:`codifica_frame` e :func:`decodifica_frame`. É possível retornar
o frame já codificado pela classe :class:`Camera`.
"""


from .log import LogFile
import numpy as np
import cv2 as cv
import os


def codifica_frame(frame: np.ndarray) -> bytes:
    """Codifica uma frame de imagem para bytes.

    O frame deve ser um array do numpy do tipo uint8, no formato BGR do OpenCV. Ele será convertido para
    JPG e formatado como uma lista de bytes. Assim, pode ser enviado pela rede a um recebedor do frame.

    Para decodificar essa a imagem codificada, use a função :func:`decodifica_frame`.

    Parameters
    ----------
    frame : numpy.ndarray
        Frame a ser codificado.

    Returns
    -------
    bytes
        Bytes contendo o frame codificado (formato JPG).
    """
    retval, frame = cv.imencode(".jpg", frame)  # Converte para JPG (array do numpy do tipo uint8)
    frame = frame.tobytes()                     # Converte para bytes (lista de bytes)

    return frame


def decodifica_frame(frame: bytes) -> np.ndarray:
    """Decodifica uma frame de bytes para a imagem.

    O frame deve ser uma lista de bytes. Ele será convertido para um array do numpy do tipo uint8 no formato
    BGR do OpenCV. Ou seja, a imagem codificada pela função :func:`codifica_frame` pode ser decodificada
    e retornada ao seu formato original por meio dessa função.

    Se ocorrer um erro na decodificação, retorna None.

    Parameters
    ----------
    frame : bytes
        Frame a ser decodificado.

    Returns
    -------
    numpy.ndarray or None
        Frame decodificado (array do numpy do tipo uint8). Se ocorreu um erro na decodificação,
        retorna None.
    """
    frame = np.frombuffer(frame, dtype=np.uint8)  # Converte para array do numpy do tipo uint8 representando um JPG
    frame = cv.imdecode(frame, cv.IMREAD_COLOR)   # Decodifica de JPG para BGR

    return frame


class Camera():
    """Classe para capturar frames de uma webcam.

    Utilize o método :meth:`retorna_frame()` para capturar o frame atual da webcam.
    """

    def __init__(self, formato_frame: tuple, erro_ao_falhar: bool = False, path_arquivo_log: str = ''):
        """Inicialização do capturador de frames da cãmera.

        É necessário informar o formado do frame capturado da webcam por meio do parâmetro *formato_frame*. Ele
        deve ser uma tupla do tipo (n_colunas, n_linhas). Ou seja, informe primeiro a dimensão horizontal (eixo x)
        e depois a dimensão vertical (eixo y).

        Se *erro_ao_falhar* for True, causa uma exceção se ocorreu erro no reconhecimento ou captura da câmera.

        É possível informar um arquivo de log para registrar as mensagens de log. Para isso, informe o caminho
        para ele por meio do parâmetro *path_arquivo_log*.

        Parameters
        ----------
        formato_frame: tuple
            Tamanho e formato do frame. Por exemplo: (640, 480)

        erro_ao_falhar: bool, default=False
            Se deve ou não causar uma exceção caso o reconhecimento ou captura da cãmera falhe.

        path_arquivo_log: str, default=''
            Caminho para o arquivo de log.
        """
        # Atributos
        self._formato_frame = formato_frame
        self._erro_ao_falhar = erro_ao_falhar

        # Gerenciador de Log
        self._log = LogFile(file_path=path_arquivo_log, prefixo='[Camera] ')

        # Inicialização da câmera. A Raspberry Pi não consegue identificar corretamente a API. Por isso,
        # essa tarefa é feita manualmente.
        if os.uname()[1] == 'raspberrypi':
            self._camera = cv.VideoCapture(0, apiPreference=cv.CAP_V4L2)

        else:
            self._camera = cv.VideoCapture(0)

        # Checa se conseguiu abrir a câmera ou não. Pode resultar em uma exceção se foi configurado para tal
        if not self._camera.isOpened():
            self._log.register("Não foi possível abrir a câmera!")

            if self._erro_ao_falhar:
                raise Exception("Não foi possível abrir a câmera!")

        # Configura a câmera
        else:
            self._camera.set(cv.CAP_PROP_BUFFERSIZE, 1)
            self._camera.set(cv.CAP_PROP_FRAME_WIDTH, formato_frame[0])
            self._camera.set(cv.CAP_PROP_FRAME_HEIGHT, formato_frame[1])

    def retorna_frame(self, codificar: bool = False):
        """Retorna um frame capturado da cãmera.

        Se o parâmetro *codificar* for True, será retornado o frame codificado (bytes). A codificação é feita pela função 
        :func:`codifica_frame`. Caso contrário, será retornado o frame em forma de array numpy (uint8).

        Se não foi configurado para causar erro ao falhar, mas ocorreu um erro na leitura do frame, será retornado
        um frame completamente preto com as dimensões especificadas ao instanciar o objeto.

        Parameters
        ----------
        codificar: bool, default=False
            Se o frame deve ser codificado ou não.

        Returns
        -------
        numpy.ndarray or bytes
            A imagem capturada da câmera. Se *codificar* for False, a imagem será um array do numpy do tipo uint8.
            Formato BGR do OpenCV. Caso *codificar* seja True, essa imagem será convertida em um array de bytes antes
            de ser retornada.
        """
        # Captura o frame
        retval, frame = self._camera.read()

        # Em caso de falha na captura do frame, pode cancelar a operação por meio de uma exceção,
        # ou enviar um frame completamente preto
        if not retval:
            if self._erro_ao_falhar:
                self._log.register("Não foi possível capturar o frame da camera!")

            else:
                frame = np.zeros(self._formato_frame[::-1], dtype=np.uint8)

        # Retorna o frame codificado se *codificar* for True. Caso contrário, retorna o frame normal
        if codificar:
            frame = codifica_frame(frame)

        return frame
