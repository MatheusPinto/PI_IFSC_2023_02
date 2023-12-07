#!/bin/env python3


"""Testa a segmentação de um vídeo.

O arquivo do vídeo é definido pelo parâmetro 'VIDEO_PATH'. O resultado é salvo no arquivo dado
por 'SAIDA_PATH' com o formato dado por 'FORMATO_SAIDA'.

O path do modelo usado é definido pelo parâmetro 'MODELO_TFLITE_PATH'.

Utiliza o segmentador.
"""


import test
import modulos.interpretador as interpretador
import tensorflow as tf
import cv2 as cv
import numpy as np
import os
import time


# Parâmetros do script
MODELO_TFLITE_PATH = "../modelo-segmentacao.tflite"
VIDEO_PATH = "video-test/video.mp4"
SAIDA_PATH = "video-test/saida.mp4"
FORMATO_SAIDA = (640, 480)


if __name__ == "__main__":
    # Entrada de frames
    entrada = cv.VideoCapture(VIDEO_PATH)

    # Carrega o segmentador de imagens (usa apenas uma thread)
    segmentador = interpretador.Segmentador(MODELO_TFLITE_PATH, n_threads=1)

    # Saída de frames
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    saida = cv.VideoWriter(SAIDA_PATH, fourcc, 30.0, FORMATO_SAIDA)

    while True:
        ret, frame = entrada.read()

        # Ao acabar os frames do vídeo, finaliza a operação
        if not ret:
            break

        # Segmentação do frame
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = segmentador.retorna_imagem_segmentada(frame, redimensiona=True)

        # Redimensiona para o formato de saída
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        frame = cv.resize(frame, FORMATO_SAIDA)

        # Salva o frame no vídeo de saída
        saida.write(frame)

        # Mostra o vídeo durante o processamento
        cv.imshow("segmenta_video.py", frame)
        key = cv.waitKey(1)
        if key==ord('q'):
            break

    entrada.release()
    saida.release()
