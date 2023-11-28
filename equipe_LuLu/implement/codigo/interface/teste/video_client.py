#!/bin/env python3


"""Teste do stream de video - cliente.

Recebe o vídeo do servidor e mostra na interface do OpenCV.

Deve ser executado junto ao script 'video_server.py'.
"""


import test
import modulos.TLSstream as TLSstream
import modulos.video as video
import numpy as np
import cv2 as cv


# Parâmetros do script
HOST = "127.0.0.1"
PORT = 3000
log_pasta = "log/"
credencias_pasta="../../env/comunicacao"


if __name__ == "__main__":
    # O frame inicial é uma imagem preta
    frame = np.zeros((120, 160), np.uint8)

    # Configuração do recebedor de vídeo
    recebedorVideo = TLSstream.TLSclient(
            credencias_pasta + "/client.key",
            credencias_pasta + "/client.crt",
            credencias_pasta + "/walle.crt",
            log_pasta + "video-client.log"
            )

    # Função de callback do recebedor de vídeo
    def video_frame_recv(self):
        """Salva a imagem recebida em um arquivo com o nome 'out.jpg'."""
        print("\n\nFrame recebido...")

        if not isinstance(self.dados, bytes):
            print("Frame corrompido!")
            return -1

        # Conversão dos bytes recebidos para imagem
        print("Convertendo para RGB...")
        global frame
        frame = video.decodifica_frame(self.dados)

    # Configuração da conexão
    recebedorVideo.recv_set(video_frame_recv)
    recebedorVideo.connect(HOST, PORT)

    # Espera até que o usuário aperte 'q' para finalizar o programa
    while True:
        cv.imshow("Frame", frame)
        key = cv.waitKey(1)
        if key==ord('q'):
            break

    recebedorVideo.close()
