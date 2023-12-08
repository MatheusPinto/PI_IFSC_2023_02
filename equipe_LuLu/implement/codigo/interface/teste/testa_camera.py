#!/bin/env python3


"""Teste da câmera.

Lista todos os backend disponíveis para a câmera.
"""


import test
import cv2 as cv


index = 0
if __name__ == "__main__":
    while True:
        camera = cv.VideoCapture(index)

        # Não foi possível encontrar o backend, então para o teste.
        if not camera.isOpened():
            print("Não foi possível abrir a câmera! Terminando o programa...\n")
            break

        # Apresenta os backends disponíveis
        print(index, "-->", camera.getBackendName())
        camera.release()
        index += 1
