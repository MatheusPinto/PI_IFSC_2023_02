#!/bin/env python3


"""Script de teste da interface - servidor.

Captura a imagem de uma câmera, converte para JPG e envia para o
usuário de forma criptografada.

Os comandos recebidos da interface são apresentados na saída padrão.

Deve ser executado junto ao script 'video_interface_client.py'.
"""


import test
import modulos.TLSstream as TLSstream
import modulos.video as video
import cv2 as cv
import numpy as np
import time


# Parâmetros do script
HOST = "127.0.0.1"
PORT_VIDEO = 3000
PORT_COMANDOS = 3001
log_pasta = "log/"
credencias_pasta="../../env/comunicacao"


if __name__ == "__main__":
    # Configuração do enviador de vídeo
    enviador_video = TLSstream.TLSserver(
            credencias_pasta + "/walle.key",
            credencias_pasta + "/walle.crt",
            credencias_pasta + "/client.crt",
            log_file_path = log_pasta + "video-interface-server-video.log"
            )

    enviador_video.connect(HOST, PORT_VIDEO)

    # Configuração do servidor
    recebedor_comandos = TLSstream.TLSserver(
            credencias_pasta + "/walle.key",
            credencias_pasta + "/walle.crt",
            credencias_pasta + "/client.crt",
            log_file_path = log_pasta + "video-interface-server-comandos.log"
            )

    # Função de callback
    def print_dados(self):
        """Apresenta os dados recebidos do cliente."""
        print(self.dados)

    # Configuração da conexão
    recebedor_comandos.recv_set(print_dados)
    recebedor_comandos.connect(HOST, PORT_COMANDOS)

    # Inicialização da câmera
    camera = video.Camera((160, 120), path_arquivo_log=log_pasta + "camera.log")

    while True:
        # Captura um frame da câmera
        print("\n\nRecebendo imagem da câmera...")
        frame = camera.retorna_frame(codificar=True)

        print("Enviando frame...")
        enviador_video.send(frame)

        print("Frame enviado.")
        time.sleep(1)

    # Finaliza o programa
    enviador_video.close()
    recebedor_comandos.close()
    camera.release()
