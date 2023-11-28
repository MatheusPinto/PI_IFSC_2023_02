#!/bin/env python3


"""Script de teste da interface - cliente.

Recebe os frames do servidor e mostra na interface gráfica. Além disso, mostra os dados
do frame na saída padrão.

Deve ser executado junto ao script 'video_interface_server.py', que envia os
frames capturados pela câmera.
"""


import test
from modulos.interface import Interface
import modulos.TLSstream as TLSstream
import PySide6.QtWidgets as QtWidgets
import cv2 as cv
import numpy as np
import sys


# Parâmetros do script
HOST = "127.0.0.1"
PORT_VIDEO = 3000
PORT_COMANDOS = 3001
log_pasta = "log/"
credencias_pasta="../../env/comunicacao"


def video_callback(interface, RGB: np.ndarray, BGR : np.ndarray):
    """Recebe uma imagem e mostra os dados.

    O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais).

    Parameters
    ----------
    RGB : numpy.ndarray
        Imagem cujos dados serão apresentados.

    BGR : numpy.ndarray
        Versão em BGR da imagem anterior
    """
    print("Frame recebido -> Formato: ", RGB.shape, "; tipo de dados: ", RGB.dtype)


if __name__ == "__main__":
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
    interface = Interface("../interface.ui", recebedor_video, enviador_comandos)
    interface.adiciona_video_callback(video_callback)
    interface.show()

    sys.exit(app.exec())
