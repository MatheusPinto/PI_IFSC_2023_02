#!/bin/env python3


"""Segmenta um vídeo.

O arquivo do vídeo é definido pelo parâmetro 'VIDEO_PATH'. Antes dos frames serem segmentados,
eles serão redimensionadas para o formato dado pelo parâmetro 'FORMATO_SAIDA'.

O resultado é salvo no arquivo dado por 'SAIDA_PATH'.
"""


import test
import segmentacao.modulos.interpretador as interpretador
import controlador.modulos.controlador as controlador
import cv2 as cv
import numpy as np
import os
import time


# Parâmetros do script
MODELO_TFLITE_PATH = "../segmentacao/modelo-segmentacao.tflite"
VIDEO_PATH = "video-test/video.mp4"
SAIDA_PATH = "video-test/saida.mp4"
FORMATO_SAIDA = (640, 480)


if __name__ == "__main__":
    # Entrada de frames
    entrada = cv.VideoCapture(VIDEO_PATH)

    # Carrega o segmentador de imagens (usa apenas uma thread)
    segmentador = interpretador.Segmentador(MODELO_TFLITE_PATH, n_threads=1)

    # Formato de entrada do modelo
    formato_entrada = segmentador.retorna_formato_entrada()
    formato_entrada = formato_entrada[:2]    # Apenas o número de linhas e colunas
    formato_entrada = formato_entrada[::-1]  # Inverte para o formato corresponder a (n_colunas, n_linhas)

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

    # Saída de frames
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    saida = cv.VideoWriter(SAIDA_PATH, fourcc, 30.0, FORMATO_SAIDA)

    while True:
        ret, frame = entrada.read()

        # Se acabaram os frames do vídeo, finaliza a operação
        if not ret:
            break

        # Redimensionamento
        frame = cv.resize(frame, formato_entrada)

        # Normalização do frame
        norm_img = np.zeros(formato_entrada)
        frame = cv.normalize(frame,  norm_img, 0, 255, cv.NORM_MINMAX)

        # Segmentação do frame
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mascara = segmentador.retorna_mascara(frame)
        frame = segmentador.retorna_imagem_segmentada(None)

        # Redimensiona para o formato de saída
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        # Ajusta a máscara
        mascara = np.array(mascara + 0.3, dtype=np.uint8)

        # Aplica o controlador no modo de debug
        ctrl.mostra_colisoes(mascara, debug=True)
        linear, angular, imagem_colisoes = ctrl.calcula_direcao(None, None, debug=True)

        # Operação de blend do frame com o resultado do debug
        imagem_colisoes = cv.resize(imagem_colisoes, frame.shape[:2][::-1])
        frame = cv.addWeighted(frame, 0.5, imagem_colisoes, 0.5, 0.0)

        # Mostra o resultado do processamento
        cv.imshow("imagem", frame)

        key = cv.waitKey(1)
        if key==ord('q'):
            break

        # Escreve o frame no vídeo de saída
        frame = cv.resize(frame, FORMATO_SAIDA)
        saida.write(frame)

    entrada.release()
    saida.release()
