#!/bin/env python3


"""Script principal do Wall-e.

Realiza o streaming de vídeo. Recebe a direção do cliente e aplica no movimento do Wall-e. Além de executar os
comandos recebidos do Wall-e: desligar e sinalizar que encontrou lixo.
"""


import fake_RPi
import interface.modulos.video as video
import interface.modulos.TLSstream as TLSstream
import movimento.modulos.movimentacao as movimentacao
import cv2 as cv
import numpy as np
from threading import Thread
import time
import os


# Parâmetros do script
CONF = "env/conf"
PORT_VIDEO = 3000
PORT_COMANDOS = 3001
log_pasta = "log/"
credencias_pasta="env/comunicacao"

GPIO_motor_DC = [24, 25, 23, 18]
GPIO_motor_passo = [22, 27, 17]
GPIO_buzzer = 7


if __name__ == "__main__":
    # IP do Wall-e
    exec(open(CONF).read())
    HOST = IP

    # Configuração do enviador de vídeo
    enviador_video = TLSstream.TLSserver(
            credencias_pasta + "/walle.key",
            credencias_pasta + "/walle.crt",
            credencias_pasta + "/client.crt",
            log_file_path = log_pasta + "video-interface-server-video.log"
            )

    tempo_parar_motor = time.time()

    enviador_video.connect(HOST, PORT_VIDEO)

    # Configuração do servidor
    recebedor_comandos = TLSstream.TLSserver(
            credencias_pasta + "/walle.key",
            credencias_pasta + "/walle.crt",
            credencias_pasta + "/client.crt",
            log_file_path = log_pasta + "video-interface-server-comandos.log"
            )

    # Função de callback do recebimento de comandos
    def callback_recebimento(self):
        """Apresenta os dados recebidos do cliente."""
        dados = self.dados.decode("utf-8")
        if dados == "halt":
            os.system("shutdown now")

        if dados == "sinalizar":
            mov.sinaliza_lixo()

        else:
            # Atualiza o tempo de atualização para que o movimento do wall-e não seja desligado.
            global tempo_parar_motor
            tempo_parar_motor = time.time()

            # As velocidades são recebidas no formato "linear,angular". É necessário separá-las
            # e converter para float antes de aplicar ao motor
            linear, angular = dados.split(',')
            linear = (float(linear))
            angular = (float(angular))

            print(linear, angular)
            mov.define_velocidade(linear, angular)

    # Configuração da conexão
    recebedor_comandos.recv_set(callback_recebimento)
    recebedor_comandos.connect(HOST, PORT_COMANDOS)

    # Controlador do movimento do Wall-e
    mov = movimentacao.Movimento(GPIO_motor_DC, GPIO_motor_passo, GPIO_buzzer)

    # Inicialização da câmera
    camera = video.Camera((160, 120), path_arquivo_log=log_pasta + "camera.log")

    # Cria uma thread para parar o movimento do Wall-e se ficar muito tempo sem receber instruções
    def parar_movimento():
        """Para o movimento do Wall-e se ficar muito tempo sem receber instruções."""
        global tempo_parar_motor
        while True:
            if time.time() - tempo_parar_motor > 1.5:
                tempo_parar_motor = time.time()
                mov.define_velocidade(0, 0)

            time.sleep(1)

    tread_parar_movimento = Thread(target=parar_movimento)
    tread_parar_movimento.start()

    while True:
        # Captura um frame da câmera
        frame = camera.retorna_frame(codificar=True)

        # Envia o frame
        enviador_video.send(frame)

    # Finaliza o programa
    enviador_video.close()
    recebedor_comandos.close()
    camera.release()
