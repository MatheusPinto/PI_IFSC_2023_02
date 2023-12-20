#!/bin/env python3


"""Controlador do direcionamento do Wall-e.

Define a classe :class:`Controlador`, responsável por definir a velocidade linear e angular do Wall-e no
modo autônomo. Além de definir se o Wall-e deve ativar a sinalização.
"""


from simple_pid import PID
from .aestrela import AEstrela
import numpy as np
import cv2 as cv
import time
import math


class Controlador():
    """Controlador do Wall-e no modo autônomo.

    O controlador possui um sistema de checagem de colisão e de direcionamento do Wall-e de forma que o
    Wall-e privilegia evitar colidir e, se está em uma direção segura, procurar por lixo. Além disso, se
    o Wall-e estiver muito próximo do lixo identificado, para e ativa a sinalização. Mais informações de
    como o direcionamento funciona pode ser obtido na documentação do método :meth:`_calcula_velocidades()`.

    Quando o Wall-e está muito próximo do objeto, ele para e ativa a sinalização. Informações de como o
    controlador computa isso estão descritas no método :meth:`_calcula_sinalizacao()`.

    O controlador possui alguns parâmetros que devem ser definidos. Por exemplo, ao instanciar a classe, deve
    ser informado o tamanho do mapa usado pelo controlador. Se for recebido um mapa com formato diferente,
    o controlador redimensiona ele para o formato correto.

    Também deve ser informado os parâmetros relacionados à checagem de colisão: as posições e tamanho dos
    blocos usados para checar as colisões. Além disso, é necessário informar a distância mínima entre o objeto
    e o Wall-e antes que a sinalização seja acionada. Consulte a documentação do método :meth:`__init__()`
    para mais informações.

    O seguinte exemplo inicia o controlador para usar mapas de 60x60, com os blocos definidos por
    *posicoes_esquerda* e com tamanho (lados) de 3 blocos. A distância mínima do objeto para o
    Wall-e é de 10 blocos do mapa.

    >>> posicoes_esquerda = [
    >>>     (-5, -15),
    >>>     (-10, -12),
    >>>     (-15, -10),
    >>>     (-17, -3)
    >>>     ]

    >>> controlador = Controlador((60, 60), posicoes_esquerda, 3, 10)

    Agora quanto aos parâmetros opcionais, é possível especificar os parâmetros usados para expandir os mapas
    de regiões colidíveis com o método :meth:`parametros_expansao()` e os parâmetros usados para gerar a matriz
    de custo por meio do método :meth:`parametros_custo()`

    São aplicados dois controladores PID nas velocidades linear e angula (um para cada). Seus parâmetros
    podem ser configurados pelos métodos :meth:`parametros_PID_linear()` e :meth:`parametros_PID_angular()`. Se
    esses métodos não forem chamados, então o controlador não usa os controladores PID.

    Para obter a direção de movimento do Wall-e, use o método :meth:`calcula_direcao()`. Ele também informa
    se o Wall-e deve acionar a sinalização.

    Para verificar onde está ocorrendo a colisão, use o método :meth:`mostra_colisoes()`.

    Para checar o processamento do mapa atual, use o método :meth:`retorna_processamento_mapa()`.
    """

    def __init__(
            self, formato_mapa : tuple = (60, 60),
            posicoes_esquerda : list = None, blocos_tamanho : int = 3,
            distancia_minima : int = 0
            ):
        """Inicialização do controlador.

        Cria os atributos da classe. Configura o traçador de caminho e a checagem de colisão. É necessário
        informar o formato dos mapas usados pelo controlador. Ao receber um mapa, ele será automaticamente
        redimensionado para esse formato contanto que seja bidimensional. O formato do mapa é dado pelo
        parâmetro *formato_mapa* e deve ser uma tupla do tipo (n_linhas, n_colunas).

        As posições a serem testadas (checagem de colisão) também devem ser informadas na instanciação do objeto.
        Eles são informadas em tuplas do tipo (y, x). O parâmetro *posicoes_esquerda* deve ser uma lista de tuplas
        contendo as posições dos blocos que serão checados à esquerda do mapa. São posições relativas ao ponto
        inicial do mapa. Por exemplo, se o ponto inicial é (25, 25), e o parâmetro *posicoes_esquerda* é [(-10, -5)],
        então será configurado um bloco com centro em (15,20).

        As posições da esquerda são espelhadas para obter as posições da direita. Então informe apenas as posições
        da esquerda.

        Essas posições são checadas em blocos. O tamanho de cada bloco (largura e altura) é definido pelo
        parâmetro *blocos_tamanho*.

        Deve-se configurar a distância mínima entre os objetos detectados (mais próximo) e o Wall-e. Para isso, use o
        parâmetro *distancia_minima*. Se a distância entre o objeto e o Wall-e for menor que *distancia_minima*, a
        sinalização será acionada conforme descrito no método :meth:`_calcula_sinalizacao()`.

        Parameters
        ----------
        formato_mapa : tuple
            Formato do mapa usado pelo controlador.

        posicoes_esquerda : list
            Lista de tuplas contendo as posições dos blocos à esquerda do mapa que serão checadas.

        blocos_tamanho : int
            Tamanho de cada bloco onde será checado a colisão no mapa.

        distancia_minima : int
            Distância mínima entre os objetos detectados e o Wall-e.
        """
        # Atributos
        self._formato_mapa = formato_mapa
        self._blocos_tamanho = blocos_tamanho
        self._pos_inicial = (formato_mapa[0] - 1, formato_mapa[1]//2)  # Posição inicial
        self._distancia_minima = distancia_minima

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

        # Limpa os atributos da iteração
        self._reinicia_iteracao()

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

        O mapa de custo é gerado e forma semelhante à expansão do mapa (ver método :meth:`parametros_expansao()`).
        Também é usado um filtro gaussiano. A diferença é não haver um offset aplicado a cada ponto, mas sim
        uma operação de multiplicação. O valor multiplicado ao mapa é definido pelo parâmetro *multiplicador*.

        O mapa de custo trabalha com valores de ponto flutuante. Diferente do mapa de colisões.

        O mapa de custo é aplicado diretamente ao algorítmo A-estrela pelo método
        :meth:`~codigo.controlador.modulos.aestrela.AEstrela.define_mapas()` da classe
        :meth:`~codigo.controlador.modulos.aestrela.AEstrela`. Veja a documentação do módulo
        :mod:`~codigo.controlador.modulos.aestrela` para mais informações.

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

        A funcionalidade dos PID é suavizar a velocidade linear.

        Parameters
        ----------
        Kp : float
            Ganho proporcional.

        Ki : float
            Ganho integral.

        Kd : float
            Ganho derivativo.
        """
        # Se não existir o PID, cria-o
        if self._PID_linear == None:
            self._PID_linear = PID(Kp, Ki, Kd)
            self._PID_linear.output_limits = (-100, 100)

        else:
            self._PID_linear.tunings = (Kp, Ki, Kd)

    def parametros_PID_angular(self, Kp : float, Ki : float, Kd : float):
        """Configura os parâmetros usados pelo PID da velocidade angular.

        A funcionalidade dos PID é suavizar a velocidae angular.

        Parameters
        ----------
        Kp : float
            Ganho proporcional.

        Ki : float
            Ganho integral.

        Kd : float
            Ganho derivativo.
        """
        # Se não existir o PID, cria-o
        if self._PID_angular == None:
            self._PID_angular = PID(Kp, Ki, Kd)
            self._PID_angular.output_limits = (-100, 100)

        else:
            self._PID_angular.tunings = (Kp, Ki, Kd)

    def calcula_direcao(self, mapa: np.ndarray, pos_objeto: tuple = None, debug=False):
        """Calcula a direção na qual o Wall-e deve se mover.

        Retorna a velocidade linear e angular que o Wall-e deve seguir para continuar se movendo
        no modo autônomo. Além de um booleano indicando se deve sinalizar a presença de lixo ou não.

        A posição do objeto que o Wall-e deve seguir é dada pelo parâmetro *pos_objeto*. Ela é uma tupla do tipo
        (cy, cx, altura, largura), em que 'cy' e 'cx' representam a posição do centro do objeto, e 'altura' e
        'largura' o tamanho do objeto.

        Se o *mapa* for None, não será atualizado. Será utilizado a mapa anterior. O processamento continua de onde parou.

        Se *debug* for True, será desenhado indicadores de direção e caminho na imagem de debug, como definido pelo método
        :meth:`_desenha_debug_direcao()`.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa usado para determinar os caminhos possíveis. Se None, usa o mapa anterior.

        pos_objeto : tuple, optional
            Posição do objeto para onde o Wall-e deve se mover. Onde está o objeto que deve ser seguido.

        debug : bool, default False
            Se True, desenha os indicadores de direção e caminho na imagem de debug.

        Returns
        -------
        linear
            Velocidade linear do Wall-e.

        angular
            Velocidade angular do Wall-e.
        """
        # Atualiza o mapa
        self.define_mapa(mapa)

        # Remove a região do objeto do mapa
        if pos_objeto is not None:
            cx, xy = self._pos_original2mapa(pos_objeto[:2])
            altura, largura = self._pos_original2mapa(pos_objeto[2:])
            self._remove_regiao_objeto((cx, xy, altura, largura))

        # Converte a posição para a do mapa
        if pos_objeto is not None:
            pos = self._pos_original2mapa(pos_objeto[:2])
            tamanho = self._pos_original2dbg(pos_objeto[2:])
            pos_objeto = (pos + tamanho)

        # Calcula as velocidades linear e angular e verifica se deve sinalizar o objeto
        linear, angular = self._calcula_velocidades(pos_objeto)
        sinalizacao = self._calcula_sinalizacao(pos_objeto)

        if debug:
            self._desenha_debug_direcao(pos_objeto)

        return linear, angular, sinalizacao

    def mostra_colisoes(self, mapa : np.ndarray, debug=False):
        """Retorna se houve colisões no mapa.

        A identificação de colisão é retornada como uma lista de booleanos indicando as colisões
        dos blocos definidos ao instanciar a classe (veja a documentação do método :meth:`__init__()`
        para mais informações).

        Cada elemento da lista corresponde a colisão em um bloco definido ao instanciar o objeto. O primeiro
        elemento corresponde ao primeiro bloco do parâmetro *posicoes_esquerda*. É importante notar as posições
        da direita (derivadas a partir das posições da esquerda) também são retornadas por esse método. Elas
        estão no final da lista.

        Para separar as colisões à esquerda da direta, use:

        >>> colisoes = controlador.mostra_colisoes(mapa)
        >>> colisoes_esquerda = colisoes[0:len(colisoes)//2]
        >>> colisoes_direita = colisoes[len(colisoes)//2:]

        Se o mapa for None, não será atualizado. Será utilizado a mapa anterior.

        Se *debug=True*, desenha os identificadores de colisão na imagem de debug. Veja a documentação do método
        :meth:`_desenha_debug_colisoes()`.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa onde será checado as colisões. Se None, usa o mapa anterior.

        debug : bool, default False
            Se True, desenha os identificadores de colisão na imagem de debug.

        Returns
        -------
        list
            Lista de identificadores de colisão.
        """
        self.define_mapa(mapa)

        colisoes = self._checa_colisoes()

        if debug:
            self._desenha_debug_colisoes()

        return colisoes

    def retorna_processamento_mapa(self, mapa : np.ndarray, pos_objeto : tuple = None):
        """Retorna o processamento do mapa.

        Computa o processamento do mapa pelo algorítimo A-estrela e retorna uma imagem de debug com os seguintes resultados:
        
        - Mapa original redimensionado
        - Mapa expandido
        - Mapa de custo
        - Mapa com as posições checadas
        - Mapa do caminho percorrido
        - Mapa original com as posições do caminho percorrido

        Esse método é usado para debug.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa que será processado.

        pos_objeto : tuple, default None
            Posição do objeto no mapa.

        Returns
        -------
        numpy.ndarray
            Imagem de debug com os resultados do processamento do mapa.
        """
        self.define_mapa(mapa)

        # Converte a posição
        pos_objeto = self._pos_original2mapa(pos_objeto)

        # Ajusta o mapa de custo
        mapa_custo = self._custo/self._custo_multiplicador
        mapa_custo = mapa_custo.astype(np.uint8)

        # Caminho traçado pelo A*
        self._tracador_caminho.define_mapas(self._mapa_expandido, self._custo)
        mapa_caminho = self._tracador_caminho.gera_caminho_mapa_smoothing(self._pos_inicial, pos_objeto)
        mapa_checados = self._tracador_caminho.retorna_mapa_checados()

        # Se não consegue traçar um caminho
        if mapa_caminho is None:
            mapa_caminho = np.zeros(self._mapa.shape, dtype=np.uint8)

        # Junta as imagens e retorna
        img0 = cv.hconcat([self._mapa*255, self._mapa_expandido*255])
        img1 = cv.hconcat([mapa_custo, mapa_checados*255])
        img2 = cv.hconcat([mapa_caminho*255, mapa_caminho*255+self._mapa*255])

        return cv.vconcat([img0, img1, img2])

    def define_mapa(self, mapa : np.ndarray = None, imagem_debug : np.ndarray = None):
        """Define o mapa do controlador.

        O mapa é expandido para evitar que o Wall-e se aproxime demais da região colidível. Além disso,
        é gerado um mapa de custo a apartir desse mapa expandido. Para saber mais sobre a expansão e o
        mapa de custo, veja os métodos :meth:`parametros_expansao()` e :meth:`parametros_custo()`.

        Se o *mapa* for None, não será atualizado. Será utilizado o mapa anterior. For fornecido um novo mapa,
        o fluxo do controlador é reiniciado, inclusindo a antiga imagem de debug.

        É possível passar uma image de debug pelo parâmetro *imagem_debug* para que o controlador possa
        mostrar as informações. Se não for fornecida, será criado uma imagem de debug vazia. A imagem de debug
        deve ser estar de acordo com o padrão do OpenCV e ser do tipo BGR.

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa usado para determinar a direção.

        imagem_debug : numpy.ndarray
            Imagem onde serão desenhadas os registros de debug. Veja os métodos
            :meth:`_desenha_debug_colisoes()` e :meth:`_desenha_debug_direcao()` para mais informações.
        """
        # Um novo mapa indica que os dados anteriores devem ser apagados e recalculados
        if mapa is not None:
            # Apaga os dados da iteracao anterior
            self._reinicia_iteracao()

            # salva o formato original do mapa
            self._formato_mapa_recebido = mapa.shape

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
            self._custo = self._custo.astype(np.float32)*self._custo_multiplicador

            # Limpa a imagem de debug
            if imagem_debug is None:
                self._imagem_debug = np.zeros(self._formato_mapa + (3,), dtype=np.uint8)
                self._formato_img_debug = self._imagem_debug.shape

        # Usa a imagem de debug definida
        if imagem_debug is not None:
            self._imagem_debug = imagem_debug
            self._formato_img_debug = self._imagem_debug.shape

    def mapa_vazio(self, fomato : tuple):
        """Retorna um mapa vazio com o formato especificado.
        
        Usando o mapa retornado por esse metodo como parâmetro, pode-se ignorar a checagem de colisão.
        Basta fornecêlo ao controlador. Por exemplo:

        >>> controlador.define_mapa(controlador.mapa_vazio((120, 160)))

        O formato do mapa, específicado por *formato*, é o formato antes do redimensionamento do mapa.
        Lembre que o mapa recebido pelo controlador é redimensionado para o formato específicado ao
        instanciar o objeto. Veja o método :meth:`__init__()` para mais informações.

        Parameters
        ----------
        fomato : tuple
            Formato da mapa (linhas, colunas).

        Returns
        -------
        numpy.ndarray
            Mapa vazio com o formato de *fomato*.
        """
        return np.zeros(fomato, dtype=np.uint8)

    def retorna_imagem_debug(self):
        """Retorna a imagem de debug.

        Retorna a imagem de debug com os resultados do processamento do mapa. Veja o método
        :meth:`_desenha_debug_colisoes()` e :meth:`_desenha_debug_direcao()` para mais informações.

        Returns
        -------
        numpy.ndarray
            Imagem de debug.
        """
        return self._imagem_debug

    def _reinicia_iteracao(self):
        """Reinicia a iteração do controlador.

        O controlador é reiniciado para uma nova iteração. Alguns dados anteriores são apagados.

        Esse método também pode ser usado para iniciar os atributos referentes a uma iteração.

        Uma iteração corresponde a uma nova checagem de colisão, de direção, de sinalização em um novo mapa fornecido.
        """
        # Mapas
        self._formato_mapa_recebido = None
        self._mapa = None
        self._mapa_expandido = None
        self._custo = None

        # Checagem de colisões
        self._colisoes = None
        self._debug_colisoes_adicionado = False
        self._regiao_removida = False

        # Checagem de direção
        self._linear = None
        self._angular = None
        self._direcao = None
        self._pos_final = None
        self._debug_direcao_adicionado = False

        # Checagem de sinalização
        self._sinalizacao = None

        # Debug
        self._imagem_debug = None

    def _pos_original2mapa(self, pos: tuple):
        """Transforma uma posição da imagem original para a do mapa.

        O parâmetro *pos* deve ser uma tupla do tipo (y, x). O resultado também assume esse formato.

        Parameters
        ----------
        pos : tuple
            Posição na imagem original.

        Returns
        -------
        tuple
            Posição no mapa.
        """
        y_mapa, x_mapa = self._formato_mapa
        y_img, x_img = self._formato_mapa_recebido[:2]

        x = pos[1] * x_mapa // x_img
        y = pos[0] * y_mapa // y_img

        return y, x

    def _pos_mapa2dbg(self, pos: tuple):
        """Transforma uma posição do mapa para a imagem de debug.

        O parâmetro *pos* deve ser uma tupla do tipo (y, x). O resultado também assume esse formato.

        Parameters
        ----------
        pos : tuple
            Posição no mapa.

        Returns
        -------
        tuple
            Posição na imagem de debug.
        """
        y_mapa, x_mapa = self._formato_mapa
        y_img, x_img = self._formato_img_debug[:2]

        x = pos[1] * x_img // x_mapa
        y = pos[0] * y_img // y_mapa

        return y, x

    def _pos_original2dbg(self, pos: tuple):
        """Transforma uma posição da imagem original para a de debug.

        O parâmetro *pos* deve ser uma tupla do tipo (y, x). O resultado também assume esse formato.

        Parameters
        ----------
        pos : tuple
            Posição na imagem original.

        Returns
        -------
        tuple
            Posição na imagem de debug.
        """
        y_dbg, x_dbg = self._formato_img_debug[:2]
        y_img, x_img = self._formato_mapa_recebido[:2]

        x = pos[1] * x_dbg // x_img
        y = pos[0] * y_dbg // y_img

        return y, x

    def _checa_colisao_bloco(self, pos: tuple, tamanho):
        """Checa se houve colisão em um bloco.

        A posição onde será checado deve ser uma tupla do tipo (y, x) indicando o ponto superior esquerdo do bloco.
        O tamanho do bloco é dado pelo parâmetro *tamanho*. Esse é o valor da altura e largura do bloco.

        Parameters
        ----------
        pos : tuple
            Posição do bloco.

        tamanho : int
            Tamanho do bloco. Altura e largura.

        Returns
        -------
        True se houve colisão, False caso contrário.
        """
        # Extrai a região que será checada do mapa
        regiao = self._mapa[pos[0]:pos[0]+tamanho, pos[1]:pos[1]+tamanho]

        # Calcula a média dos valores dessa região
        regiao = np.reshape(regiao, -1)
        media = np.mean(regiao)

        # Considerá que colidiu se mais da metade da região for colidível
        return media > 0.5

    def _checa_colisoes(self):
        """Checa as colisões no mapa.

        As posições checadas são as definidas ao instanciar o objeto. Assim como o tamanho do bloco.

        Verifica as colisões e retorna uma lista com o identificador de cada colisão (True ou False).

        Returns
        -------
        list
            Lista com o identificador de cada colisão (True ou False).

        """
        # Não reprocessa as colisões se isso já foi feito
        if self._colisoes is not None:
            return self._colisoes

        # Checa a colisão
        colisoes = []
        for pos in self._blocos:
            colisoes.append(self._checa_colisao_bloco(pos, self._blocos_tamanho))

        # Salva as colisões no atributo
        self._colisoes = colisoes

        return colisoes

    def _desenha_debug_colisoes(self):
        """Desenha as colisões na imagem de debug.

        As regiões colidindo são marcadas com amarelo, e as regiões não colidindo marcadas com azul.
        A imagem de debug é retornada.

        Returns
        -------
        numpy.ndarray
            Imagem de debug.
        """
        # Não adiciona o debug das colisões mais de uma vez
        if self._debug_colisoes_adicionado:
            return self._imagem_debug

        colisoes = self._checa_colisoes()

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

            # Conversão dos pontos para o formato da imagem
            pos_inicial = self._pos_mapa2dbg(info[0])
            pos_final = self._pos_mapa2dbg(pos_final)

            cv.rectangle(self._imagem_debug, pos_inicial[::-1], pos_final[::-1], cor, cv.FILLED)

        self._debug_colisoes_adicionado = True

        return self._imagem_debug

    def _calcula_sinalizacao(self, pos_objeto: tuple = None):
        """Verifica se o Wall-e deve acionar a sinalização.
        
        A sinalização é ativada quando o objeto chega mais perto do Wall-e do que a distância mínima
        definida ao instanciar a classe. Veja o método :meth:`__init__()`.

        A posição do objeto deve ser uma tupla do tipo (centro_y, centro_x, altura, largura). Além disso,
        se trata da posição em relação ao mapa após o redimensionamento. Por exemplo, se o mapa original
        possui tamanho de 300x300, mas ao ser aplicado como mapa do controlador é redimensionada para 60x60,
        a posição que indica o centro é dada por 30x30.

        Se está muito perto do Wall-e, o atributo *self._sinalizacao* é definido como True. Caso contrário,
        como False.

        Se a posição for None, não é checado a sinalização e o resultado é automaticamente False.

        Parameters
        ----------
        pos_objeto : tuple
            Posição do objeto no mapa.

        Returns
        -------
        bool
            Verdadeiro se o Wall-e deve acionar a sinalização.
        """
        # Não calcula a sinalização se isso foi feito
        if self._sinalizacao is not None and self._pos_final == pos_objeto:
            return self._sinalizacao

        # Não tem objeto no mapa
        if pos_objeto is None:
            self._sinalacao = False
            return False

        # Se o objeto alcança a distância mínima, então deve ativar a sinalização.
        self._sinalizacao = pos_objeto[0] > self._formato_mapa[0] - self._distancia_minima

        return self._sinalizacao

    def _calcula_velocidades(self, pos_objeto: tuple = None):
        """Calcula as velocidades lineares e angulares do Wall-e no modo autônomo.

        O primeiro fator considerado é se o objeto está muito próximo do Wall-e. Se sim, o Wall-e
        permanece parado e ativa a sinalização. Caso contrário, o comportamento do controlador é definido
        pelo seguinte diagrama:

        .. image:: /../../../../codigo/controlador/img/controlador.svg

        Fonte: autoria própria.

        Considera a checagem de colisão e a posição do objeto. Se estiver identificando colisão, o
        Wall-e é direcionado de forma a evitá-la. Caso contrário tenta traçar um caminho até o objeto e,
        se conseguiu, direciona o Wall-e até esse objeto.

        Se for configurado previamente, aplica dois controladores PID para as velocidades lineares e angulares
        (um para cada). Eles servem para suavizar as mudanças nos valores de velocidade linear e angular.

        Parameters
        ----------
        pos_objeto : tuple
            Posição do objeto no mapa. Se None, desconsidera o processamento do caminho até o objeto e a sinalização.

        Returns
        -------
        int
            Velocidade linear do Wall-e.

        int
            Velocidade angular do Wall-e.
        """
        # Não reprocessa a direção se já foi feito
        if self._linear is not None and self._pos_final == pos_objeto:
            if debug:
                return self._linear, self._angular, self._direcao_imagem
            else:
                return self._linear, self._angular

        # A direção inicial é para frente
        linear = 100
        angular = 0

        # Checagem de colisão. Afasta o Wall-e de objetos colidíveis. Se tiver mais colisões a esquerda,
        # direciona para direita e vice-versa
        colisoes = self._checa_colisoes()

        n_colisoes_esquerda = colisoes[:self._n_blocos//2].count(True)
        n_colisoes_direita = colisoes[self._n_blocos//2:].count(True)

        # Se o Wall-e pretende alcançar um objeto. Isso é necessário para saber se o caminho deve ser
        # mostrado na tela no modo de debug
        self._alcancar_objeto = False  

        # Colidindo à esquerda
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
            # Se o objeto estiver muito próximo do Wall-e, deve parar
            if self._calcula_sinalizacao(pos_objeto):
                linear = 0
                angular = 0

            # Objeto está longe o bastante do Wall-e para continuar a andar
            else:
                direcao_objeto = self._calcula_direcao_objeto(pos_objeto[:2])

                # Se definiu um caminho para o objeto
                if direcao_objeto != None:
                    linear = int(100 * math.sin(direcao_objeto))
                    angular = -int(100 * math.cos(direcao_objeto))

                    self._alcancar_objeto = True  # Mostra o caminho no modo de debug

        # Aplica os PID à velocidade linear e angular
        if self._PID_linear != None:
            self._PID_linear.setpoint = linear  # Velocidade linear desejada

            self._vel_linear = self._PID_linear(self._vel_linear)
            linear = int(self._vel_linear)

        if self._PID_angular != None:
            self._PID_angular.setpoint = angular  # Velocidade angular desejada

            self._vel_angular = self._PID_angular(self._vel_angular)
            angular = int(self._vel_angular)

        # Identificação do lixo. Se estiver muito próximo, o Wall-e deve parar
        if self._calcula_sinalizacao(pos_objeto):
            linear = 0
            angular = 0

        self._linear = linear
        self._angular = angular

        return linear, angular

    def _remove_regiao_objeto(self, pos_objeto):
        """Remove a região colidível ao redor do objeto do mapa.

        A posiçao do objeto deve ser uma tupla do tipo (centro_y, centro_x, altura, largura).
        Todas referentes a posição no mapa.

        Parameters
        ----------
        pos_objeto : tuple
            Posição do objeto no mapa.
        """
        # Não remove a região se isso já foi feito
        if self._regiao_removida:
            return

        cy, cx, h, w = pos_objeto
        h, w = h + 2, w + 2  # Evitar erros caso o tamanho do objeto seja muito pequeno
        y, x = cy - h // 2, cx - w // 2

        # Correção no caso de y ser negativo
        if y < 0:
            h, y = h+y, 0

        # Correção no caso da altura ser maior do que o máximo
        maximo = self._mapa_expandido.shape[0]
        if y+h > maximo:
            h = maximo - y

        # Correção no caso da largura ser maior do que o máximo
        maximo = self._mapa_expandido.shape[1]
        if x+w > maximo:
            w = maximo - x

        # Correção no caso de x ser negativo
        if x < 0:
            w, x = w+x, 0

        # Remove a região
        self._mapa_expandido[y:y+h, x:x+w] = np.zeros((h, w), dtype=np.uint8)

    def _calcula_direcao_objeto(self, pos_final):
        """Calcula a direção que deve percorrer para alcançar um objeto.

        Retorna a direção (ângulo em radianos) que o Wall-e deve se mover para alcançar o objeto.

        Parameters
        ----------
        pos_final : tuple
            Posição de destino do caminho. Onde está o objeto.

        Returns
        -------
        float
            Direção do que o Wall-e deve se mover. O angulo em radianos.
        """
        # Não reprocessa a direção se isso já foi feito
        if self._direcao is not None and self._pos_final == pos_final:
            return self._direcao

        # Calcula a direção do que o Wall-e deve se mover. O traçador retorna None se não conseguir traçar um caminho
        self._tracador_caminho.define_mapas(self._mapa_expandido, self._custo)
        direcao = self._tracador_caminho.retorna_direcao_inicial(self._pos_inicial, pos_final, rad=True)

        # Salva a direção e posição em atributos
        self._direcao = direcao
        self._pos_final = pos_final

        return direcao

    def _desenha_debug_direcao(self, pos_objeto):
        """Desenha a direção do caminho que deve seguir na imagem de debug.

        Desenha a direção do caminho que o Wall-e deve seguir na imagem de debug. Será um desenho de uma reta em
        que a dimensão no eixo 'y' representa a velocidade linear, e a dimensão no eixo 'x' representa a velocidade angular.

        Além disso, desenha o caminho que o Wall-e deve seguir na imagem de debug, caso tenha conseguido traçar um
        caminho. Ele será desenhado em branco.

        Também desenha um '+' na posição do objeto. As dimensões do objeto também são mostradas na imagem de debug.

        Se estiver sinalizando a identificação do lixo, escreve a mensagem "Sinalizando!" com letras azuis.

        Parameters
        ----------
        pos_objeto : tuple
            Posição de destino do caminho. Onde está o objeto que deve ser seguido.

        Returns
        -------
        np.ndarray
            Imagem de debug com o indicador da velocidade linear e angular que o Wall-e deve seguir.
            Se conseguiu traçar um caminho entre o ponto de início e a *pos_objeto*, mostra esse caminho também.
        """
        # Não adiciona o debug da direção mais de uma vez
        if self._debug_direcao_adicionado:
            return self._imagem_debug

        # Caminho traçado pelo A* (apenas se conseguiu traçar)
        if self._alcancar_objeto:
            mapa_caminho = self._tracador_caminho.gera_caminho_mapa_smoothing(self._pos_inicial, pos_objeto[:2])

            # O mapa do caminho deve ser convertido para BGR e redimensionado antes de ser adicionado a imagem de debug
            mapa_caminho = cv.cvtColor(mapa_caminho*255, cv.COLOR_GRAY2BGR)
            mapa_caminho = cv.resize(mapa_caminho, (self._formato_img_debug[:2][::-1]))

            self._imagem_debug = cv.bitwise_or(self._imagem_debug, mapa_caminho)

        # Ajusta o tamanho da reta
        dx = - self._angular * self._formato_mapa[1] // 500
        dy = - self._linear * self._formato_mapa[0] // 500

        # Posições da linha e círculo do indicador de direção
        pos_meio = (self._formato_mapa[1]//2, self._formato_mapa[0]//2)
        pos_final = (
                pos_meio[0] + dy,  # Posição do eico y
                pos_meio[1] + dx   # Posição do eixo x
                )

        # Converte as posições para a imagem de debug
        pos_meio = self._pos_mapa2dbg(pos_meio)
        pos_final = self._pos_mapa2dbg(pos_final)

        # Desenha o indicador de direção. É importante notar que o formato usado para o ponto é do tipo
        # (y, x), mas os argumentos da função do OpenCV usa formato (x, y). Portanto, é necessário
        # convertê-los antes de desenhar a linha
        espessura_linha = self._formato_img_debug[0] // 60 + 1
        raio_circulo = self._formato_img_debug[0] // 50 + 1
        cv.line(self._imagem_debug, pos_meio[::-1], pos_final[::-1], (255, 0, 255), espessura_linha)
        cv.circle(self._imagem_debug, pos_meio[::-1], raio_circulo, (255, 0, 255), cv.FILLED)

        if pos_objeto is not None:
            # Desenha um '+' na posição do objeto
            pos_marcador = self._pos_mapa2dbg(pos_objeto[:2])
            cv.drawMarker(
                    self._imagem_debug, pos_marcador[::-1], (200, 0, 200),
                    cv.MARKER_CROSS, espessura_linha*3, espessura_linha
                    )

            # Desenha um retângulo ao redor do marcador
            pos_inicial = (pos_marcador[0]-pos_objeto[2]//2, pos_marcador[1]-pos_objeto[3]//2)
            pos_final = (pos_marcador[0]+pos_objeto[2]//2, pos_marcador[1]+pos_objeto[3]//2)
            cv.rectangle(self._imagem_debug, pos_inicial[::-1], pos_final[::-1], (200, 0, 200), espessura_linha//4+1)

        # Escreve uma mensagem de sinalização quando o Wall-e está próximo do lixo
        if self._calcula_sinalizacao(pos_objeto):
            escala_fonte = self._formato_img_debug[1] / 500
            cv.putText(
                    self._imagem_debug, "Sinalizando!", (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                    escala_fonte, (255, 0, 0), espessura_linha//4+1, cv.LINE_AA
                    )

        self._debug_direcao_adicionado = True

        return self._imagem_debug
