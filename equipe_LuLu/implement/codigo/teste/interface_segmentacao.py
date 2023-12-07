#!/bin/env python3


"""Script de teste da interface com segmentador.

Executa o segmentador de imagens e mostra os resultados na interface.

Deve ser executado junto ao script 'server.py', que envia os frames capturados pela câmera e
mostra os dados enviados pela interface.
"""


import test
from interface.modulos.interface import Interface
import interface.modulos.TLSstream as TLSstream
import segmentacao.modulos.interpretador as interpretador
import PySide6.QtWidgets as QtWidgets
import cv2 as cv
import numpy as np
import sys


# Parâmetros do script
HOST = "127.0.0.1"
PORT_VIDEO = 3000
PORT_COMANDOS = 3001
log_pasta = "log/"
credencias_pasta = "../env/comunicacao"

MODELO_TFLITE_PATH = "../segmentacao/modelo-segmentacao.tflite"
FORMATO_SAIDA = (640, 480)


if __name__ == "__main__":
    # Carrega o segmentador de imagens (usa apenas uma thread)
    segmentador = interpretador.Segmentador(MODELO_TFLITE_PATH, n_threads=1)

    def video_callback(interface, RGB : np.ndarray, BGR : np.ndarray):
        """Recebe uma imagem, segmenta ela, e mostra na interface.

        O parâmetro *imagem* deve ser uma imagem (array do Numpy) no formato (linhas, colunas, canais).

        Parameters
        ----------
        interface : Interface
            Interface do usuário.

        RGB : numpy.ndarray
            Imagem a ser segmentada.

        BGR : numpy.ndarray
            Versão em BGR da imagem anterior.
        """
        imagem_segmentada = segmentador.retorna_imagem_segmentada(RGB)
        interface.atualiza_frame(imagem_segmentada)

    # Configuração do recebedor de vídeo
    recebedor_video = TLSstream.TLSclient(
            credencias_pasta + "/client.key",
            credencias_pasta + "/client.crt",
            credencias_pasta + "/walle.crt",
            log_file_path = log_pasta + "video-interface-client-video.log"
            )

    recebedor_video.connect(HOST, PORT_VIDEO)

    # Configuração do cliente
    enviador_comandos = TLSstream.TLSclient(
            credencias_pasta + "/client.key",
            credencias_pasta + "/client.crt",
            credencias_pasta + "/walle.crt",
            log_file_path = log_pasta + "video-interface-client-comandos.log"
            )

    enviador_comandos.connect(HOST, PORT_COMANDOS)

    # Configurações da interface de usuário
    app = QtWidgets.QApplication()
    interface = Interface("../interface/interface.ui", recebedor_video, enviador_comandos)
    interface.atualiza_frame_automaticamente = False
    interface.define_video_callback_lista([video_callback])
    interface.show()

    sys.exit(app.exec())
