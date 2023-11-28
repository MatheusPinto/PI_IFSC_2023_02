#!/bin/env python3


"""Script da interface.

Deve ser executado junto ao script 'walle.py', que envia os frames capturados pela câmera.

Permite o envio de dados comandos do cliente para o Wall-e.
"""


from modulos.interface import Interface
import modulos.TLSstream as TLSstream
import PySide6.QtWidgets as QtWidgets
import cv2 as cv
import numpy as np
import sys


# Parâmetros do script
CONF = "../env/conf"
PORT_VIDEO = 3000
PORT_COMANDOS = 3001
log_pasta = "log/"
credencias_pasta="../env/comunicacao"


if __name__ == "__main__":
    # IP do Wall-e
    exec(open(CONF).read())
    HOST = IP

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
    interface = Interface("interface.ui", recebedor_video, enviador_comandos)
    interface.show()

    sys.exit(app.exec())
