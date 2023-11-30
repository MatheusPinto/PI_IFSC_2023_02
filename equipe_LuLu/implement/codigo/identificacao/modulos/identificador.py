#!/bin/env python3


"""Identificador de lixo.

Implementação da identificação de lixo usando a ferramenta de Haar Cascade do OpenCV. Para tal
utilize a classe :class:`Identificador`.
"""


import numpy as np
import cv2 as cv


class Identificador():
    """Classe para identificação de lixo.

    Deve-se fornecer o path do arquivo contendo o modelo de Haar Cascade usado para identificar o
    lixo. Ela localizará o lixo em um frame fornecido e retornará a posição do lixo mais próximo.
    Veja o método :meth:`identifica_lixo_proximo` para mais informações.

    Se deseja identificar todos os lixos do frame, utilize o método :meth:`identifica_lixos`.
    """
 
    def __init__(self, path_modelo : str, formato_imagem : tuple = None):
        """Construtor do modelo de identificação.

        Cria um identificador de lixo. Deve ser fornecido o path do arquivo contendo o modelo de Haar Cascade.

        É possível configurar o formato da imagem (n_linhas, n_colunas) que a imagem deve ter. Se recebido um frame
        com tamanho diferente, ele será redimensionado para o correto.

        Parameters
        ----------
        path_modelo : str
            Caminho para o arquivo contendo o modelo usado para identificar o lixo.

        formato_imagem : (int, int), default=None
            Formato da imagem (n_linhas, n_colunas) que a imagem deve ter. Se recebido um frame com tamanho
            diferente, ele será redimensionado para o correto.
        """
        self._formato_imagem = formato_imagem
        self._classificador = cv.CascadeClassifier(path_modelo)

    def define_frame(self, frame : np.ndarray, imagem_debug : np.ndarray = None):
        """Define o frame usado na identificação.

        É possível definir uma imagem para ser a inicial de debug.

        Parameters
        ----------
        frame : numpy.ndarray
            Frame onde serão identificado o lixo.

        imagem_debug : numpy.ndarray
            Imagem de debug.
        """
        if frame is not None:
            # Ajuste de formato
            if self._formato_imagem is not None:
                frame = cv.resize(frame, self._formato_imagem)

            self._frame = frame
            self._classificacao = None
            self._posicao_mais_proxima = None
            self._img_debug = frame

        if imagem_debug is not None:
            # Ajuste de formato
            if self._formato_imagem is not None:
                imagem_debug = cv.resize(imagem_debug, self._formato_imagem)

            self._img_debug = imagem_debug

    def identifica_lixos(self, frame : np.ndarray, debug=False):
        """Identifica todos os lixos do frame.

        Se *debug=True*, retorna uma imagem com os lixos identificados (um quadrado verde ao redor deles).

        Parameters
        ----------
        frame : numpy.ndarray
            Frame a ser identificado.

        debug : bool, default=False
            Se True, retorna uma imagem com os lixos identificados por um quadrado verde ao redor.

        Returns
        -------
        list or (tuple, numpy.ndarray)
            Lista de tuplas contendo as coordenadas do lixo (x, y, l, a). Se *debug=True*, essa lista estará em
            uma tupla junto da imagem de debug.
        """
        self.define_frame(frame, imagem_debug=frame)

        # Retorna o valor anterior se a operação já foi feita
        if self._classificacao is not None:
            if debug:
                return self._classificacao, self._img_debug
            else:
                return self._classificacao

        # Transformando a imagem da câmera em cinza
        cinza = cv.cvtColor(self._frame, cv.COLOR_BGR2GRAY)

        self._classificacao = self._classificador.detectMultiScale(cinza, minNeighbors=1, minSize=(30,30))

        # Desenha quadrados no frame para identificar os lixos
        if debug:
            for (x, y, l, a) in self._classificacao:
                cv.rectangle(self._img_debug, (x, y), (x + l, y + a), (0, 255, 0), 2)

            return self._classificacao, self._img_debug

        return self._classificacao

    def identifica_lixo_proximo(self, frame : np.ndarray, debug=False):
        """Identifica o lixo mais próximo do frame.

        O lixo mais próximo é o que está mais abaixo da imagem.

        Se *debug=True*, retorna as classificações e a imagem com o debug. Essa imagem é igual a de
        debug retornado pelo método :meth:`identifica_lixos`, mas com um círculo vermelho sobre a
        detecção mais próxima.

        Parameters
        ----------
        frame : numpy.ndarray
            Frame a ser identificado.

        debug : bool, default=False
            Se True, retorna uma imagem com o lixo mais próximo identificado por um círculo vermelho.

        Returns
        -------
        list or (tuple, numpy.ndarray)
            Lista de tuplas contendo as coordenadas do lixo mais próximo (x, y). Se *debug=True*, essa
            lista estará em uma tupla junto da imagem de debug.
        """
        self.define_frame(frame, imagem_debug=frame)

        # Retorna o valor anterior se a operação já foi feita
        if self._posicao_mais_proxima is not None:
            if debug:
                return self._posicao_mais_proxima, self._img_debug
            else:
                return self._posicao_mais_proxima

        # Obtém todos os lixos identificados
        classificacao = self.identifica_lixos(frame, debug=debug)
        imagem = None

        if debug:
            classificacao, imagem = classificacao

        if classificacao == ():
            if debug:
                return None, imagem
            return None

        # Define o objeto mais próximo
        self._posicao_mais_proxima = (0, 0)
        distancia_mais_proxima = 0

        # O objeto mais próximo é o que possui maior y + a. Ou seja, maior posição vertical + altura.
        # Lembre que o valor de y é maior para posições mais baixas do frame
        for (x, y, l, a) in classificacao:
            if y + a > distancia_mais_proxima:
                distancia_mais_proxima = y + a
                self._posicao_mais_proxima = (x + l//2, y + a//2)

        # Se em modo de debug, retorna as classificações e a imagem com debug
        if debug:
            cv.circle(imagem, self._posicao_mais_proxima, 15, (0,0,255), 2)
            return self._posicao_mais_proxima, imagem

        return self._posicao_mais_proxima
