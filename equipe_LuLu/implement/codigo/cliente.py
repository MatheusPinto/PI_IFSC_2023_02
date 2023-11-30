#!/bin/env python3


"""Script principal do usuário.

Implemnta o código que é executado do lado do usuário (cliente). Ou seja, implementa a interface
do usuário e o modo autônomo.
"""


from interface.modulos.interface import Interface
import interface.modulos.TLSstream as TLSstream
import segmentacao.modulos.interpretador as interpretador
import controlador.modulos.controlador as controlador
import PySide6.QtWidgets as QtWidgets
import autonomo
import cv2 as cv
import numpy as np
import sys


# Parâmetros do script
CONF = "env/conf"
PORT_VIDEO = 3000
PORT_COMANDOS = 3001
log_pasta = "log/"
credencias_pasta = "env/comunicacao"

MODELO_TFLITE_PATH = "segmentacao/modelo-segmentacao.tflite"
FORMATO_SAIDA = (640, 480)


if __name__ == "__main__":
    # IP do Wall-e
    exec(open(CONF).read())
    HOST = IP

    # Carrega o segmentador de imagens (usa apenas uma thread)
    segmentador = interpretador.Segmentador(MODELO_TFLITE_PATH, n_threads=1)

    # Controlador
    posicoes_esquerda = [
            (-10, -15),
            (-20, -12),
            (-30, -10)
            ]

    ctrl = controlador.Controlador((60, 60), posicoes_esquerda, 4)

    Kp, Ki, Kd = 0.6, 1, 0.003
    ctrl.parametros_PID_linear(Kp, Ki, Kd)

    Kp, Ki, Kd = 0.4, 1, 0.003
    ctrl.parametros_PID_angular(Kp, Ki, Kd)

    # Processamento do vídeo no modo automático
    def video_callback(interface, RGB : np.ndarray, BGR : np.ndarray):
        """Recebe uma imagem, segmenta ela, e mostra na interface.

        O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais).

        Parameters
        ----------
        interface : Interface
            Interface do usuário.

        RGB : numpy.ndarray
            Imagem a ser segmentada.

        BGR : numpy.ndarray
            Versão em BGR da imagem anterior.
        """
        if interface.modo_automatico:
            interface.atualiza_frame_automaticamente = False

            auto.processa_imagem(RGB, debug=True)

        else:
            interface.atualiza_frame_automaticamente = True

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
    interface = Interface("interface/interface.ui", recebedor_video, enviador_comandos)
    interface.define_video_callback_lista([video_callback])
    interface.show()

    auto = autonomo.Auto(interface, enviador_comandos, segmentador, ctrl, "identificacao/cascade.xml")

    sys.exit(app.exec())
