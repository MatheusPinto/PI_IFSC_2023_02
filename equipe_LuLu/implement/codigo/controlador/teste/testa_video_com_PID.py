#!/bin/env python3


"""Testa a checagem de colisão em um vídeo.

O arquivo do vídeo é definido pelo parâmetro 'VIDEO_PATH'.

O resultado é salvo no arquivo dado por 'SAIDA_PATH' com o formato dado por 'FORMATO_SAIDA'.

O resultado esperado está abaixo:

.. image:: /../../../../codigo/controlador/img/video-controlador-com-PID.gif

Fonte: autoria própria.
"""


import test
import modulos.controlador as controlador
import cv2 as cv
import numpy as np
import os
import time


# Parâmetros do script
MODELO_TFLITE_PATH = "../segmentacao/modelo-segmentacao.tflite"
VIDEO_PATH = "video-teste/exemplo.mkv"
SAIDA_PATH = "video-teste/saida_com_PID.mkv"
FORMATO_SAIDA = (640, 480)
TAMANHO_OBJETO = (20, 40)


if __name__ == "__main__":
    # Entrada de frames
    entrada = cv.VideoCapture(VIDEO_PATH)

    # Controlador
    posicoes_esquerda = [
            (-5, -15),
            (-10, -12),
            (-15, -10),
            (-17, -3)
            ]

    ctrl = controlador.Controlador((60, 60), posicoes_esquerda, 4, 15)

    Kp, Ki, Kd = 0.6, 1, 0.003
    ctrl.parametros_PID_linear(Kp, Ki, Kd)

    Kp, Ki, Kd = 0.4, 1, 0.003
    ctrl.parametros_PID_angular(Kp, Ki, Kd)

    # Saída de frames
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    saida = cv.VideoWriter(SAIDA_PATH, fourcc, 15.0, FORMATO_SAIDA)

    n_frames = 0
    ponto_destino = (10, 10) + TAMANHO_OBJETO
    while True:
        ret, frame = entrada.read()
        n_frames += 1

        # Se acabaram os frames do vídeo, finaliza a operação
        if not ret:
            break

        # Atraso esperado do modelo de segmentação
        time.sleep(0.04)

        # Muda a posição de destino para um aleatório a cada 30 frames
        if n_frames % 30 == 0:
            ponto_destino = (np.random.randint(0, 128), np.random.randint(0, 128)) + TAMANHO_OBJETO
        
        # Formatação do mapa
        img_debug = cv.resize(frame, (500, 500))
        mapa = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Normaliza o mapa para usar no algorítimo A*
        mapa = mapa//255

        # Aplica no controlador no modo de debug
        ctrl.define_mapa(mapa, img_debug)
        ctrl.mostra_colisoes(None, debug=True)
        linear, angular, sinalizacao = ctrl.calcula_direcao(None, ponto_destino, debug=True)

        # Mostra o resultado do processamento
        img_debug = ctrl.retorna_imagem_debug()
        cv.imshow("imagem", img_debug)

        key = cv.waitKey(1)
        if key==ord('q'):
            break

        # Escreve o frame no vídeo de saída
        img_debug = cv.resize(img_debug, FORMATO_SAIDA)
        saida.write(img_debug)

    entrada.release()
    saida.release()
