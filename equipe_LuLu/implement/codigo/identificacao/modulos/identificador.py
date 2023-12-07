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

        Cria um identificador de lixo. Deve ser fornecido o path do arquivo contendo o modelo de Haar Cascade pelo parâmetro
        *path_modelo*.

        É possível configurar o formato da imagem (n_colunas, n_linas) que a imagem deve ter. Se recebido um frame
        com tamanho diferente, ele será redimensionado para o correto.

        Parameters
        ----------
        path_modelo : str
            Caminho para o arquivo contendo o modelo usado para identificar o lixo.

        formato_imagem : (int, int), default=None
            Formato da imagem (n_colunas, n_linhas) que a imagem deve ter. Se recebido um frame com tamanho
            diferente, ele será redimensionado para o correto.
        """
        # Se a imagem deve ser redimensionada antes de ser aplicada ao identificador
        if formato_imagem is not None:
            self._imagem_formato_fixo = True
        else:
            self._imagem_formato_fixo = False

        self._formato_imagem = formato_imagem
        self._classificador = cv.CascadeClassifier(path_modelo)

    def define_frame(self, frame : np.ndarray, imagem_debug : np.ndarray = None):
        """Define o frame usado na identificação.

        É possível definir uma imagem para ser a inicial de debug. Se receber um frame com tamanho diferente,
        ele será redimensionado para o definido ao instanciar a classe. Veja o método :meth:`__init__()` para
        informações de como fazer isso. O frame apenas é usado na identificação do lixo após ser redimensionado
        para o formato correto.

        Parameters
        ----------
        frame : numpy.ndarray
            Frame onde serão identificados os lixos.

        imagem_debug : numpy.ndarray
            Imagem de debug.
        """
        # Novo frame definido
        if frame is not None:
            self._reinicia_iteracao()

            # Frame original
            self._frame = frame
            self._formato_frame_original = frame.shape

            # Ajuste de formato
            if self._imagem_formato_fixo:
                self._frame = cv.resize(frame, self._formato_imagem)

            self._formato_frame = self._frame.shape

            # Imagem de debug
            if imagem_debug is None:
                self._img_debug = frame.copy()
                self._formato_img_debug = self._img_debug.shape

        # Definindo uma imagem de debug manualmente
        if imagem_debug is not None:
            self._img_debug = imagem_debug
            self._formato_img_debug = self._img_debug.shape

    def identifica_lixos(self, frame : np.ndarray, debug=False):
        """Identifica todos os lixos do frame.

        Se *debug=True*, desenha os lixos identificados (um retângulo azul-claro ao redor deles) na imagem de debug.
         Veja o método :meth:`_desenha_debug_lixos()` para mais informações.

        Parameters
        ----------
        frame : numpy.ndarray
            Frame a ser identificado.

        debug : bool, default=False
            Se True, identifica os lixos na imagem de debug por um quadrado verde

        Returns
        -------
        list
            Lista de tuplas contendo as coordenadas do lixo (x, y, l, a).
        """
        self.define_frame(frame)

        classificacao = self._calcula_posicoes_lixos()

        # Converte para o formato da imagem original
        classificacao_convertida = []
        if classificacao is not None:
            for (x, y, l, a) in classificacao:
                x, y = self._pos_frame2original((x, y))
                l, a = self._pos_frame2original((l, a))
                classificacao_convertida.append((x, y, l, a))
        
        # Desenha quadrados no frame para identificar os lixos
        if debug:
            self._desenha_debug_lixos()

        return classificacao_convertida

    def identifica_lixo_mais_proximo(self, frame : np.ndarray, debug=False):
        """Identifica o lixo mais próximo do frame.

        O lixo mais próximo é o que está mais abaixo da imagem. Retona sua posição na imagem por
        meio de uma tupla do seguinte tipo: (x, y, l, a, cx, cy). 'x' e 'y' são as posições do ponto superior
        esquerdo do objeto. 'l' e 'a' são largura e altura. 'cx' e 'cy' são as posições do centro do objeto.

        Todos esses valores são do objeto na imagem original (antes de redimensionar).

        Se *debug=True*, desenha um identificador do lixo mais próximo na imagem de debug. Semelhante às identificações do
        método :meth:`identifica_lixos`, mas com um círculo rosa sobre a detecção mais próxima. Veja o método
        :meth:`_desenha_debug_lixo_mais_proximo()` para mais informações.

        Parameters
        ----------
        frame : numpy.ndarray
            Frame a ser identificado.

        debug : bool, default=False
            Se True, identifica lixo mais próximo na imagem de debug por um círculo rosa.

        Returns
        -------
        list
            Coordenadas do lixo mais próximo (x, y, l, a, cx, cy).
        """
        self.define_frame(frame)

        # Obtém todos os lixos identificados
        self.identifica_lixos(frame, debug=debug)

        # Identifica o lixo mais próximo
        pos_mais_proxima = self._calcula_posicao_lixo_mais_proximo()

        # Converte para o formato da imagem original
        if pos_mais_proxima is not None:
            x, y, l, a, cx, cy = pos_mais_proxima
            x, y = self._pos_frame2original((x, y))
            l, a = self._pos_frame2original((l, a))
            cx, cy = self._pos_frame2original((cx, cy))
            pos_mais_proxima = (x, y, l, a, cx, cy)

        # Se em modo de debug, retorna as classificações e a imagem com debug
        if debug:
            self._desenha_debug_lixo_mais_proximo()

        return pos_mais_proxima

    def retorna_imagem_debug(self):
        """Retorna a imagem de debug.

        A imagem de debug pode possuir os identificadores de todos os lixos, assim como do
        lixo mais próximo. Ela é pode ser definida pelo método :meth:`define_frame()`.

        Returns
        -------
        numpy.ndarray
            Imagem de debug.
        """
        return self._img_debug

    def _reinicia_iteracao(self):
        """Reinicia os atributos da identificação.

        O identificador é reiniciado para uma nova iteração. Alguns dados anteriores são apagados.

        Esse método também pode ser usado para iniciar os atributos referentes a uma iteração.

        Uma iteração corresponde a uma nova identificação de objetos em um novo frame.
        """
        # Identificação de todos os lixos
        self._classificacao = None
        self._debug_todos_lixos_feito = False

        # Identificação dos lixos mais próximos
        self._pos_mais_proxima = None
        self._debug_lixo_proximo_feito = False

        # Imagem de debug
        self._img_debug = None
        self._formato_img_debug = None

    def _pos_frame2debug(self, pos: tuple):
        """Transforma as coordenadas do frame usado na identificação para as coordenadas da imagem de debug.

        A conversão ocorre das coordenadas após o redimensionamento do frame. Veja o método :meth:`define_frame`
        para saber mais sobre isso.

        Essas coordenadas são convertidas para equivalentes da imagem de debug. Suponha que o formato do
        frame definido ao instanciar a classe é de 320x240 e a imagem de debug possui formato 640x480. Converter
        o ponto (10, 15) resultará em (20, 30).

        Parameters
        ----------
        pos : tuple
            Coordenadas do frame redimensionado (x, y).

        Returns
        -------
        tuple
            Coordenadas na imagem de debug (x, y).
        """
        y_frame, x_frame = self._formato_frame[:2]
        y_debug, x_debug = self._formato_img_debug[:2]

        y = pos[1] * y_debug // y_frame
        x = pos[0] * x_debug // x_frame

        return x, y

    def _pos_frame2original(self, pos: tuple):
        """Transforma as coordenadas do frame usado na identificação para as coordenadas da imagem original.

        Converte as coordenadas em relação ao frame pós-redimensionado (usado na identificação) para a posição
        respectiva da imagem original.

        Essas coordenadas são convertidas para equivalentes da imagem original. Suponha que o formato do
        frame definido ao instanciar a classe é de 320x240 e a imagem original possui formato 640x480. Converter
        o ponto (10, 15) resultará em (20, 30).

        Parameters
        ----------
        pos : tuple
            Coordenadas do frame redimensionado (x, y).

        Returns
        -------
        tuple
            Coordenadas na imagem original (x, y).
        """
        y_frame, x_frame = self._formato_frame[:2]
        y_original, x_original = self._formato_frame_original[:2]

        y = pos[1] * y_original // y_frame
        x = pos[0] * x_original // x_frame

        return x, y

    def _calcula_posicoes_lixos(self):
        """Retorna as coordenadas dos lixos identificados.

        Retorna uma lista com as coordenadas dos lixos. Cada elemento da lista corresponde á coordenada de um lixo.
        Além disso, as coordenadas possuem o formato (posicao_x, posica_y, largura, altura).

        As posições retornadas são em relação à imagem pós-redimensionamento. Para mais informações sobre o
        redimensionamento dos frames, veja o método :meth:`define_frame` e :meth:`__init__`.

        Returns
        -------
        list
            Lista de tuplas contendo as coordenadas do lixo (x, y, l, a).
        """
        # Retorna o valor anterior se a operação já foi feita
        if self._classificacao is not None:
            return self._classificacao

        # Transformando a imagem da câmera em cinza (o Haar cascade opera com grayscale)
        cinza = cv.cvtColor(self._frame, cv.COLOR_BGR2GRAY)

        # Identifica todos os lixos
        self._classificacao = self._classificador.detectMultiScale(cinza, minNeighbors=1, minSize=(10,10))

        return self._classificacao

    def _desenha_debug_lixos(self):
        """Desenha o debug da identificação de todos os lixos.

        Desenha um retângulo azul claro sobre os lixos identificados.

        Returns
        -------
        numpy.ndarray
            Imagem de debug.
        """
        # Não desenha a identificação dos lixos se já foi feito
        if self._debug_todos_lixos_feito:
            return self._img_debug

        self._debug_todos_lixos_feito = True

        for (x, y, l, a) in self._classificacao:
            # As posições iniciais e finais devem ser convertidas para a imagem de debug
            pos_inicial = self._pos_frame2debug((x, y))
            pos_final = self._pos_frame2debug((x + l, y + a))

            cv.rectangle(self._img_debug, pos_inicial, pos_final, (255, 255, 0), 2)

        return self._img_debug

    def _calcula_posicao_lixo_mais_proximo(self):
        """Retorna a posição do lixo mais próximo.

        Retorna uma tupla com a coordenada do lixo mais próximo. A estrutura da tupla é
        (posicao_x, posica_y, largura, altura, centro_x, centro_y).

        O lixo mais próximo é dado pela distância em relação à borda inferior da imagem. Quanto menor,
        mais próximo do Wall-e ele está.

        A posição retornada é em relação à imagem já redimensionada. Para mais informações sobre o
        redimensionamento dos frames, veja o método :meth:`define_frame()` e :meth:`__init__()`.

        Returns
        -------
        tuple
            Tupla contendo as coordenadas do lixo mais próximo (x, y, l, a, cx, cy).
        """
        # Retorna o valor anterior se a operação já foi feita
        if self._pos_mais_proxima is not None:
            return self._pos_mais_proxima

        classificacao = self._calcula_posicoes_lixos()

        # Se nenhum lixo foi identificado, retorna None
        if len(classificacao) == 0:
            self._pos_mais_proxima = None
            return None

        # Define o objeto mais próximo
        self._pos_mais_proxima = (0, 0)
        distancia_mais_proxima = 0

        # O objeto mais próximo é o que possui maior y + a. Ou seja, maior posição vertical + altura.
        # Lembre que o valor de y é maior para posições mais baixas (próximas da borda inferior) do frame
        for (x, y, l, a) in classificacao:
            if y + a > distancia_mais_proxima:
                distancia_mais_proxima = y + a
                self._pos_mais_proxima = (x, y, l, a, x + l//2, y + a//2)

        return self._pos_mais_proxima

    def _desenha_debug_lixo_mais_proximo(self):
        """Desenha o debug da identificação do lixo mais próximo.

        Desenha um círculo rosa sobre o lixo mais próximo identificado. A definição do lixo mais próximo
        ocorre como descrito no método :meth:`_calcula_posicao_lixo_mais_proximo()`.

        Returns
        -------
        numpy.ndarray
            Imagem de debug.
        """
        # Não desenha a identificação do lixo se já foi feito
        if self._debug_lixo_proximo_feito:
            return self._img_debug

        self._debug_lixo_proximo_feito = True

        # Retorna nada se não encontrou nenhum lixo
        if self._pos_mais_proxima is None:
            return self._img_debug

        # Posição onde deve desenhar o círculo
        (x, y, l, a, cx, cy) = self._pos_mais_proxima
        pos = self._pos_frame2debug((cx, cy))
        formato = self._pos_frame2debug((l, a))
        raio = (formato[0] + formato[1]) // 4

        # Desenha o círculo
        cv.circle(self._img_debug, pos, raio, (100, 100, 255), 2)

        return self._img_debug
