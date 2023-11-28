#!/bin/env python3


"""Controlador do direcionamento do Wall-e.

Define a classe :class:`Controlador`, responsável por definir a velocidade linear e angular no Wall-e no modo autônomo.
"""


from simple_pid import PID
from .aestrela import AEstrela
import numpy as np
import cv2 as cv
import time
import math


class Controlador():
    """Controlador do Wall-e no modo autônomo.

    Ao instanciar um objeto dessa classe, deve ser fornecido os do mapa onde será marcado as colisões e
    seus tamanhos. Veja :meth:`__init__()` para mais informações.

    Para obter a direção de movimento do Wall-e, use o método :meth:`calcula_direcao`. Para verificar
    onde está ocorrendo a colisão, use o método :meth:`mostra_colisoes`.
    """

    def __init__(self, formato_mapa : tuple = (60, 60), posicoes_esquerda : list = None, blocos_tamanho : int = 3):
        """Inicialização do controlador.

        Cria os atributos da classe. Configura o traçador de caminho e a checagem de colisão. É necessário
        informar o formato dos mapas usados pelo controlador. Ao receber um mapa, ele será automaticamente
        redimensionado para esse formato contanto que seja bidimensional. O formato do mapa é dado pelo
        parâmetro *formato_mapa* e deve ser uma tupla do tipo (n_linhas, n_colunas).

        As posições a serem testadas (checagem de colisão) também devem ser informadas na instanciação do objeto.
        Eles são informadas em tuplas do tipo (y, x). O parâmetro *posicoes_esquerda* deve ser uma lista de tuplas
        contendo as posições dos blocos que serão checados à esquerda do mapa. São posições relativas ao ponto
        inicial do mapa. Elas serão espelhadas para obter as posições da direita.

        As posições do mapa são checadas em blocos. O tamanho de cada bloco é definido pelo parâmetro *blocos_tamanho*.

        Parameters
        ----------
        formato_mapa : tuple
            Formato do mapa usado pelo controlador.

        posicoes_esquerda : list
            Lista de tuplas contendo as posições dos blocos à esquerda do mapa que serão checadas.

        blocos_tamanho : int
            Tamanho de cada bloco onde será checado a colisão no mapa.
        """
        # Atributos
        self._formato_mapa = formato_mapa
        self._blocos_tamanho = blocos_tamanho
        self._pos_inicial = (formato_mapa[0] - 1, formato_mapa[1]//2)  # Posição inicial

        # Atributos padrão do ajuste do mapa (deve funcionar bem para mapas de 60 por 60)
        self._expansao_kernel = (19, 19)
        self._expansao_sigma = 5
        self._expansao_offset = 0.8
        self._custo_kernel = (21, 21)
        self._custo_sigma = 7
        self._custo_multiplicador = 5.0

        # Controle da velocidade linear e angular
        self._vel_linear = 0.0
        self._vel_angular = 0.0
        self._PID_linear = None
        self._PID_angular = None

        # Configuração do traçador de caminho
        self._tracador_caminho = AEstrela()

        # Configuração da checagem de colisão
        if posicoes_esquerda is not None:
            # Posições dos blocos que serão checados (relativa à posição inicial)
            posicoes_direita = [(pos[0], -pos[1]) for pos in posicoes_esquerda]

            # Converte as posições para absolutas. O tamanho dos blocos deforma a posição das
            # colunas (eixo x). Esse offset é para corrigir isso.
            offset = -blocos_tamanho//2
            pos_inicial = self._pos_inicial

            self._blocos_esquerda = [(pos[0]+pos_inicial[0], pos[1]+pos_inicial[1] + offset) for pos in posicoes_esquerda]
            self._blocos_direita = [(pos[0]+pos_inicial[0], pos[1]+pos_inicial[1] + offset) for pos in posicoes_direita]
            self._blocos = self._blocos_esquerda + self._blocos_direita

            # O número de blocos é necessário para poder separar entre esquerda e direita.
            # self._blocos[:self._n_blocos//2] são os blocos da esquerda.
            # self._blocos[self._n_blocos//2:] são os blocos da direita.
            self._n_blocos = len(self._blocos)

    def parametros_expansao(self, kernel : tuple, sigma : int, offset : float):
        """Configura os parâmetros usados para expandir a imagem.

        A expansão do mapa é feita por meio de um filtro gaussiano. Os parâmetros ajustados por esse método
        são referentes a esse filtro. O parâmetro *kernel* é o tamanho do kernel, e o parâmetro *sigma* é o
        sigma do filtro gaussiano.

        O parâmetro *offset* é o valor de offset aplicados aos valores do mapa. Naturalmente, o valor de
        uma posição do mapa varia de 0.0 até 1.0. O offset é aplicado a esse valor. Apenas se passar de 1.0,
        será considerado região colidível.

        Parameters
        ----------
        kernel : tuple
            Tamanho do kernel do filtro gaussiano usado para expandir o mapa.

        sigma : int
            Sigma do filtro gaussiano usado para expandir o mapa.

        offset : float
            Offset aplicado aos valores do mapa. Se o valor de um ponto passar de 1.0, será considerado colidível.
        """
        self._expansao_kernel = kernel
        self._expansao_sigma = sigma
        self._expansao_offset = offset

    def parametros_custo(self, kernel : tuple, sigma : int, multiplicador : float):
        """Configura os parâmetros usados para expandir a imagem.

        O mapa de custo é gerado e forma semelhante à expansão do mapa (ver método :meth:`parametros_expansao`).
        Também é usado um filtro gaussiano. A diferença é não haver um offset aplicado a cada ponto, mas sim
        uma operação de multiplicação. O valor multiplicado ao mapa é definido pelo parâmetro *multiplicador*.

        Parameters
        ----------
        kernel : tuple
            Tamanho do kernel do filtro gaussiano usado para gerar o mapa de custo.

        sigma : int
            Sigma do filtro gaussiano usado para gerar o mapa de custo.

        multiplicador : float
            Multiplicador aplicado aos valores do mapa de custo.
        """
        self._custo_kernel = kernel
        self._custo_sigma = sigma
        self._custo_multiplicador = multiplicador

    def parametros_PID_linear(self, Kp : float, Ki : float, Kd : float):
        """Configura os parâmetros usados pelo PID da velocidade linear.

        Parameters
        ----------
        Kp : float
            Ganho proporcional.

        Ki : float
            Ganho integral.

        Kd : float
            Ganho derivativo.
        """
        if self._PID_linear == None:
            self._PID_linear = PID(Kp, Ki, Kd)
            self._PID_linear.output_limits = (-100, 100)
        else:
            self._PID_linear.tunings = (Kp, Ki, Kd)

    def parametros_PID_angular(self, Kp : float, Ki : float, Kd : float):
        """Configura os parâmetros usados pelo PID da velocidade angular.

        Parameters
        ----------
        Kp : float
            Ganho proporcional.

        Ki : float
            Ganho integral.

        Kd : float
            Ganho derivativo.
        """
        if self._PID_angular == None:
            self._PID_angular = PID(Kp, Ki, Kd)
            self._PID_angular.output_limits = (-100, 100)
        else:
            self._PID_angular.tunings = (Kp, Ki, Kd)

    def calcula_direcao(self, mapa: np.ndarray, pos_objeto: tuple = None, debug=False):
        """Calcula a direção que o Wall-e deve se mover.

        Retorna a velocidade linear e angular que o wall-e deve seguir para continuar se movendo
        no modo autônomo.

        Se o *mapa* for None, não será atualizado. Será utilizado a mapa anterior.

        Se *debug* for True, retorna uma imagem com uma reta indicando a direção do caminho a seguir.
        Se está se movendo na direção de um objeto, o caminho até ele é traçado.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa usado para determinar a direção. Se None, usa o mapa anterior.

        pos_objeto : tuple, optional
            Posição do objeto que onde o Wall-e deve se mover.

        debug : bool, default False
            Se True, retorna uma imagem com uma reta indicando a direção do caminho a seguir.
            Se está se movendo na direção de um objeto, o caminho até ele é traçado.

        Returns
        -------
        linear
            Velocidade linear do Wall-e.

        angular
            Velocidade angular do Wall-e.

        np.ndarray
            Se debug=True, retorna uma imagem com uma reta indicando a direção do caminho.
        """
        # A direção inicial é para frente
        linear = 100
        angular = 0

        # Checagem de colisão. Afasta o Wall-e de objetos colidíveis. Se tiver mais colisões a esquerde,
        # direciona para direita e vice-versa
        self._atualiza_mapa(mapa)
        colisoes = self._checa_colisoes()

        n_colisoes_esquerda = colisoes[:self._n_blocos//2].count(True)
        n_colisoes_direita = colisoes[self._n_blocos//2:].count(True)

        # Colidindo à esquerda
        alcancar_objeto = False  # Se o Wall-e pretende alcançar um objeto

        if n_colisoes_esquerda > 0 and n_colisoes_direita == 0:
            linear = 100
            angular = -50  # Movimenta para direita

        # Colidindo à direita
        elif n_colisoes_esquerda == 0 and n_colisoes_direita > 0:
            linear = 100
            angular = 50  # Movimenta para esquerda

        # Colidindo tanto à esquerda quanto à direita
        elif n_colisoes_esquerda > 0 and n_colisoes_direita > 0:
            if self._vel_angular < 0:
                linear = 0
                angular = -100  # Movimenta para direita
            else:
                linear = 0
                angular = 100  # Movimenta para esquerda

        # Não colidindo, calcula a direção que deve seguir para alcançar algum objeto no mapa
        elif pos_objeto != None:
            direcao_objeto = self._calcula_direcao_objeto(pos_objeto)

            # Se definiu um caminho para o objeto
            if direcao_objeto != None:
                linear = -int(100 * math.cos(direcao_objeto))
                angular = int(100 * math.sin(direcao_objeto))

                alcancar_objeto = True

        # Aplica os PID à velocidade linear e angular
        if self._PID_linear != None:
            self._PID_linear.setpoint = linear

            self._vel_linear = self._PID_linear(self._vel_linear)
            linear = int(self._vel_linear)

        if self._PID_angular != None:
            self._PID_angular.setpoint = angular

            self._vel_angular = self._PID_angular(self._vel_angular)
            angular = int(self._vel_angular)
    
        if not debug:
            return linear, angular

        # Cria uma imagem com uma reta indicando a direção do caminho
        else:
            # Cria a imagem de debug
            self._cria_imagem_debug()

            # Caminho traçado pelo A*
            if alcancar_objeto:
                mapa_caminho = self._tracador_caminho.gera_caminho_mapa_smoothing(self._pos_inicial, pos_objeto)
                mapa_caminho = cv.cvtColor(mapa_caminho*255, cv.COLOR_GRAY2BGR)
                self._imagem_debug = cv.add(self._imagem_debug, mapa_caminho)

            # Ajusta o tamanho da reta
            dx = - angular * self._formato_mapa[1] // 500
            dy = - linear * self._formato_mapa[0] // 500

            # Posições da linha e círculo do indicador de direção
            pos_meio = (self._formato_mapa[1]//2, self._formato_mapa[0]//2)
            pos_final = (
                    pos_meio[0] + dy,  # Posição do eico y
                    pos_meio[1] + dx   # Posição do eixo x
                    )

            # Desenha o indicador de direção. É importante notar que o formato usado para o ponto é do tipo
            # (y, x), mas os argumentos da função do OpenCV usa formato (x, y). Portanto, é necessário
            # convertê-los antes de desenhar a linha
            cv.line(self._imagem_debug, pos_meio[::-1], pos_final[::-1], (255, 0, 255), 1)
            cv.circle(self._imagem_debug, pos_meio[::-1], 2, (255, 0, 255), cv.FILLED)

            return linear, angular, self._imagem_debug

    def mostra_colisoes(self, mapa : np.ndarray, debug=False):
        """Retorna se houve colisões no mapa.

        Se o mapa for None, não será atualizado. Será utilizado a mapa anterior.

        Se debug=True, retorna uma imagem com as identificações visuais das colisões.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa onde será checado as colisões. Se None, usa o mapa anterior.

        debug : bool, default False
            Se True, retorna uma imagem do mapa com os identificadores de colisão.
            Se False, retorna apenas um vetor com os identificadores de colisão.

        Returns
        -------
        list
            Lista de identificadores de colisão.

        numpy.ndarray
            Se debug=True, retorna uma imagem com as identificações visuais das colisões.
        """
        self._atualiza_mapa(mapa)

        return self._checa_colisoes(debug=debug)

    def _atualiza_mapa(self, mapa : np.ndarray):
        """Atualiza a mapa do controlador.

        Ajusta o tamanho das regões colidíveis, salvando no atributo *_mapa_expandido*, e gera um mapa
        de custo para afastar o trajeto do Wall-e dos objetos colidíveis. Esse mapa é salvo no atributo *_custo*.

        Se o *mapa* for None, não será atualizado.

        Limpa a imagem de debug usada nos demais métodos, exceto se *mapa=None*.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa usado para determinar a direção.
        """
        if mapa is not None:
            # Ajusta a mapa para ser usada no algorítimo controlador
            if mapa.shape != self._formato_mapa:
                mapa = cv.resize(mapa, self._formato_mapa)

            self._mapa = mapa

            # Aumenta a área das regiões colidíveis (paredes)
            self._mapa_expandido = cv.GaussianBlur(mapa*255, self._expansao_kernel, self._expansao_sigma)
            self._mapa_expandido = np.floor(self._mapa_expandido/255 + self._expansao_offset)
            self._mapa_expandido = np.array(self._mapa_expandido, dtype=np.uint8)

            # Mapa de custo
            self._custo = cv.GaussianBlur(self._mapa_expandido*255, self._custo_kernel, self._custo_sigma)
            self._custo = self._custo*5.0

            # Limpa a imagem de debug
            self._imagem_debug = None

    def _cria_imagem_debug(self):
        """Cria uma imagem para ser usada nas funções de debug.

        Nessa imagem, serão adicionadas as identificações visuais de debug. Como, por exemplo, blocos
        indicando as regiões colidindo, ou uma reta indicando a direção a ser seguida.

        A imagem será salva no atributo *_imagem_debug*.
        """
        if self._imagem_debug is None:
            self._imagem_debug = np.zeros(self._formato_mapa + (3,), dtype=np.uint8)

    def _checa_colisao_bloco(self, mapa, pos: tuple, tamanho):
        """Checa se houve colisão em um bloco.

        A posição onde será checado deve ser uma tupla do tipo (y, x) indicando o ponto superior esquerdo do bloco.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa onde será checado as colisões.

        pos : tuple
            Posição do bloco.

        tamanho : int
            Tamanho do bloco.
        """
        # Extrai a região que será checada do mapa
        regiao = mapa[pos[0]:pos[0]+tamanho, pos[1]:pos[1]+tamanho]

        # Calcula a média dos valores dessa região
        regiao = np.reshape(regiao, -1)
        media = np.mean(regiao)

        # Considerá que colidiu se mais da metade da região for colidível
        return media > 0.5

    def _checa_colisoes(self, debug=False):
        """Checa as colisões na mapa.

        As posições checadas são as definidas ao instanciar o objeto.

        Verifica as colisões e retorna uma lista com o identificador de cada colisão (True ou False).

        Se *debug* for True, retorna uma imagem com as regiões colidindo marcadas com amarelo, e as regiões não
        colidindo marcadas com azul.

        Parameters
        ----------
        debug : bool, default False
            Se True, retorna uma imagem com as regiões colidindo marcadas com amarelo, e as regiões não
            colidindo marcadas com azul. Se False, retorna apenas uma lista com o identificador de cada
            colisão (True ou False).

        Returns
        -------
        list
            Lista com o identificador de cada colisão (True ou False).

        numpy.ndarray
            Imagem com as regiões colidindo marcadas com amarelo, e as regiões não colidindo marcadas com azul.
            Apenas retornado se *debug* for True.
        """
        # Checa a colisão
        colisoes = []
        for pos in self._blocos:
            colisoes.append(self._checa_colisao_bloco(self._mapa, pos, self._blocos_tamanho))

        if debug:
            # Cria a imagem de debug
            self._cria_imagem_debug()

            for info in zip(self._blocos, colisoes):
                # info[0] é a posição do bloco.
                # info[1] é um booleano indicando se colidiu ou não.

                # Usa a cor amarelo se houver colisão, e a azul se não houver
                cor = None
                if info[1]:
                    cor = (0, 255, 255)
                else:
                    cor = (255, 0, 0)

                # Desenha o retângulo. É importante notar que o formato usado para o ponto é do tipo (y, x), mas
                # os argumentos da função do OpenCV usa formato (x, y). Portanto, é necessário convertê-los
                # antes de desenhar o quadrado.
                pos_final = (info[0][0]+self._blocos_tamanho, info[0][1] + self._blocos_tamanho)
                cv.rectangle(self._imagem_debug, info[0][::-1], pos_final[::-1], cor, cv.FILLED)

            return colisoes, self._imagem_debug

        else:
            return colisoes

    def _calcula_direcao_objeto(self, pos_final):
        """Calcula a direção que deve percorrer para alcançar um objeto.

        Retorna a velocidade linear e angular que o wall-e deve seguir para continuar se movendo
        no modo autônomo.

        Parameters
        ----------
        pos_final : tuple
            Posição de destino do caminho. Onde está o objeto.

        Returns
        -------
        float
            Direção do que o Wall-e deve se mover.
        """
        # Calcula a direção do que o Wall-e deve se mover
        self._tracador_caminho.define_mapas(self._mapa_expandido, self._custo)
        direcao = self._tracador_caminho.retorna_direcao_inicial(self._pos_inicial, pos_final, rad=True)

        # Se não conseguiu traçar um caminho, retorna None
        if direcao == None:
            return None

        return direcao
