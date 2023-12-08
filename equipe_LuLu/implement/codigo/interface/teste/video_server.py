#!/bin/env python3


"""
Teste do stream de video - servidor.

Captura a imagem de uma câmera, converte para JPG e envia para o
usuário de forma criptografada.

Deve ser executado junto ao script 'video_client.py'.
"""


import test
import modulos.TLSstream as TLSstream
import modulos.video as video
import time


# Parâmetros do script
HOST = "127.0.0.1"
PORT = 3000
log_pasta = "log/"
credencias_pasta="../../env/comunicacao"


if __name__ == "__main__":
    # Configuração do enviador de vídeo
    enviador_video = TLSstream.TLSserver(
            credencias_pasta + "/walle.key",
            credencias_pasta + "/walle.crt",
            credencias_pasta + "/client.crt",
            log_pasta + "video-server.log"
            )

    # Configuração da conexão
    enviador_video.connect(HOST, PORT)

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
    enviadorVideo.close()
    camera.release()
