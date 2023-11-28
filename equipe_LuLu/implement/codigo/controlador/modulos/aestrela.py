#!/bin/env python3


"""Implementação do algorítimo de busca A-estrela.

Para utilizar o algorítimo, deve-se criar um objeto da classe :class:`AEstrela`.
"""


import cv2 as cv
import numpy as np
import math
import time


class AEstrela():
    """Implementa o algorítimo A*, para obter o melhor caminho entre dois pontos de um mapa.

    Essa classe permite configurar um objeto que traça o menor caminho entre dois pontos
    em um mapa usando o algoŕitmo A*. Para gerar o caminho, deve ser fornecido um mapa de
    entrada e as posições iniciais e finais do caminho. 

    Os mapas usados nessa implementação são todos matrizes do Numpy do tipo matriz[y][x].
    O eixo y é apresentado primeiro para melhor compatibilidade com o OpenCV. Os pontos
    também usam o formato (y, x). A matriz do mapa que indica as posições permitidas para
    se mover e as que não são permitidas (paredes) utiliza valores do tipo uint8. É possível
    criar uma matriz desse tipo com o seguinte código:

    >>> matriz = numpy.zeros((linhas, colunas), dtype=numpy.uint8)

    Nessa matriz, o valor 0 representa uma região não colidível, e o valor 1 representa
    uma região colidível.

    É necessário fornecer um mapa, e as posições final e inicial para traçar o caminho.

    O mapa é definido pelo método :meth:`define_mapas()`, e os pontos são definidos ao gerar
    o caminho com o método :meth:`gera_caminho()`.

    A implementação permite configurar a quantidade de custo adicionada ao mudar de posição
    na implementação. O parâmetro é o *passo*, definido ao instanciar a classe. Veja
    :meth:`__init__()` para mais informações;

    O custo é computado usando a função heurística baseada na distância entre dois pontos.

    Também é possível usar uma matriz para adicionar valores específicos a função
    de custo em cada ponto do mapa. Veja a documentação do método :meth:`define_mapas()`.

    É possível alterar os mapas e pontos de início/fim de um objeto sem ter que instanciá-lo
    novamente.

    Para fins de debug e verificação do funcionamento, é possível retornar um mapa com todas as
    posições checadas ao gerar um caminho. Veja o método :meth:`retorna_mapa_checados()` para mais
    informações.
    """

    def __init__(self, passo=10):
        """Configura o algorítimo A*.

        O parâmetro *passo* é um peso relacionado ao custo de se movimentar de uma posição para outra adjacente.
        Por exemplo, ao mover da posição (0, 1) para (0, 2), será adicionado um custo de *passo* a esse caminho.

        Parameters
        ----------
        passo : int
            Peso relacionado ao custo de se movimentar de uma posição para outra adjacente.
        """
        self._passo = passo
        self._mapa = None

    def define_mapas(self, mapa, mapa_custo=None):
        """Define o mapa do ambiente onde será traçado o caminho.

        Deve ser forncido um mapa do ambiente onde será traçado o caminho. O mapa é uma matriz do Numpy tipo
        matriz[y][x] de inteiros onde 0 representa um lugar por onde pode ser traçado um caminho e 1, uma
        barreira sólida que não pode ser ultrapassada.

        Também é possível fornecer um mapa de custo cujos valores serão somados a função heurística.
        O mapa é uma matriz do Numpy tipo matriz[y][x] de pontos flutuantes. O valor de cada posição será
        somado a função custo quando computar o custo associado a essa posição. As dimensões do *mapa_custo*
        devem ser iguais às dimensões do *mapa*

        Parameters
        ----------
        mapa : numpy.ndarray
            Mapa da região onde será traçado o caminho.

        mapa_custo : numpy.ndarray
            Mapa de valores a serem somados a função de custo. Deve ter as mesmas dimensões que o *mapa*.

        Warnings
        --------
        Executar esse método apaga o mapa e os resultados anteriores.
        """
        self._mapa_formato = mapa.shape
        self._mapa = mapa.copy()

        # Mapa de custo
        if mapa_custo is not None:
            self._mapa_custo = mapa_custo.copy()

        else:
            self._mapa_custo = None

        # Limpa os resultados
        self._mapa_checado = None
        self._vetor_caminho = None
        self._pos_inicio = None
        self._pos_fim = None

    def gera_caminho(self, pos_inicio, pos_fim):
        """Gera o melhor caminho do ponto inicial até o final no mapa.

        Retorna um vetor com esse caminho. Da posição inicial até a posição anterior ao ponto final.

        As posições devem ser uma tupla do tipo (pos_y, pos_x)

        Parameters
        ----------
        pos_inicial : tuple
            Posição de início no mapa.

        pos_fim : tuple
            Posição de destino do caminho no mapa.

        Returns
        -------
        list
            Vetor com os pontos do caminho.
        """
        # Se o caminho já foi traçado, não é necessário traçá-lo novamente
        if self._pos_inicio == pos_inicio and self._pos_fim == pos_fim:
            return self._vetor_caminho

        # Salva as posições iniciais e finais
        self._pos_inicio = pos_inicio
        self._pos_fim = pos_fim

        # A posição final será salva como um atributo para não ter que ser passada como argumento aos
        # demais métodos.
        self._pos_fim = pos_fim

        # A lista aberta consiste em uma lista com todos os pontos (posições) que devem ser checados para
        # obter o caminho. Cada elemento da lista deve conter as seguintes informações: a posição do ponto,
        # o ponto pai (para poder gerar o caminho), e o custo associado a esse ponto.
        self._lista_aberta = [(pos_inicio, None, 1.0)]

        # Lista onde para todas as posições que já foram checadas devem estar. Após serem checadas, elas são
        # removidas da lista aberta e colocadas nessa lista. Essa lista será usada para traçar o caminho no
        # mapa após ele ser definido.
        self._lista_fechada = []

        # Mapa com todas a posições que não devem mais ser checadas (paredes e as já checadas)
        self._mapa_checado = self._mapa.copy()
        self._mapa_checado[pos_inicio] = 1  # Adiciona uma parede no ponto inicial para não ser checado futuramente

        # Define o caminho e gera seu vetor
        caminho = self._obtem_caminho(pos_inicio)
        self._vetor_caminho = self._gera_vetor_caminho(caminho)

        return self._vetor_caminho

    def gera_caminho_smoothing(self, pos_inicio, pos_fim):
        """Gera o melhor caminho do ponto inicial até o final no mapa, com smoothing.

        Funciona da mesma forma que o método :meth:`gera_caminho()`, mas o caminho será ajustado
        com uma técnica de suavização (smoothing).

        Parameters
        ----------
        pos_inicial : tuple
            Posição de inicio no mapa.

        pos_fim : tuple
            Posição de destino do caminho no mapa.

        Returns
        -------
        list
            Vetor com os pontos do caminho.
        """
        vetor_caminho = self.gera_caminho(pos_inicio, pos_fim)
        vetor_caminho = self._vetor_smoothing(vetor_caminho, 25)

        return vetor_caminho

    def retorna_direcao_inicial(self, pos_inicio, pos_fim, rad=True):
        """Retorna a direção inicial que deve ser seguida para percorrer o caminho.

        Retorna um ângulo em radiano ou em graus, dependendo do parâmetro *rad*. Ele corresponde ao ângulo,
        usando as convenções matemáticas padrões, da abertura entre o eixo x da região inferior do mapa e direção
        do caminho percorrido.

        Parameters
        ----------
        pos_inicio : tuple
            Posição de início no mapa.

        pos_fim : tuple
            Posição de destino do caminho no mapa.

        rad : bool, default True
            Se True, retorna o angulo em radiano. Se False, retorna o angulo em graus.

        Returns
        -------
        float or None
            Ângulo da direção inicial em radiano ou em graus. Se não foi possível
            definir a direção, retorna None.
        """
        vetor_caminho = self.gera_caminho_smoothing(pos_inicio, pos_fim)

        # Se não conseguiu traçar um caminho, retorna None
        if vetor_caminho == None:
            return None

        # Se o caminho é muito pequeno, retorna None
        if len(vetor_caminho) < 3:
            return None
        
        # Distância entre os pontos
        p_fim = np.int16(vetor_caminho[2])
        p_inicio = np.int16(vetor_caminho[0])

        dx = p_fim[1]-p_inicio[1]
        dy = p_fim[0]-p_inicio[0]
        d_pontos = math.sqrt(dx**2 + dy**2)

        # Ângulo entre os pontos em radiano
        angulo = math.acos(dx/d_pontos)

        if rad:
            return angulo

        else:
            # Conversão para graus
            return angulo*180/math.pi

    def gera_caminho_mapa(self, pos_inicio, pos_fim):
        """Gera um mapa do caminho percorrido com o algorítimo A*.

        Retorna um mapa com esse caminho. Esse mapa é um array Numpy do tipo matriz[y][x] de inteiros onde 1
        representa uma posição do caminho traçado, e 0 uma posição fora do caminho.

        As posições devem ser uma tupla do tipo (pos_y, pos_x).

        Parameters
        ----------
        pos_inicio : tuple
            Posição de início no mapa.

        pos_fim : tuple
            Posição de destino do caminho no mapa.

        Returns
        -------
        numpy.ndarray
            Mapa com o caminho percorrido.
        """
        vetor_caminho = self.gera_caminho(pos_inicio, pos_fim)

        return self._gera_mapa_caminho(vetor_caminho)

    def gera_caminho_mapa_smoothing(self, pos_inicio, pos_fim):
        """Gera um mapa do caminho percorrido com o algorítimo A*, com smoothing.

        Funciona da mesma forma que o método :meth:`gera_caminho_mapa`, mas o caminho será ajustado
        com uma técnica de suavização (smoothing).

        Parameters
        ----------
        pos_inicio : tuple
            Posição de inicio no mapa.

        pos_fim : tuple
            Posição de destino do caminho no mapa.

        Returns
        -------
        numpy.ndarray
            Mapa com o caminho percorrido.
        """
        vetor_caminho = self.gera_caminho_smoothing(pos_inicio, pos_fim)

        return self._gera_mapa_caminho_smoothing(vetor_caminho)

    def retorna_mapa_checados(self):
        """Retorna o mapa com todas as posições checadas.

        O mapa é uma matriz do Numpy do tipo matriz[y][x] de inteiros onde 1 representa
        uma posição checada, e 0 uma posição não checada.

        Esse é um método para verificar o funcionamento do algorítimo A*.

        Returns
        -------
        numpy.ndarray
            Mapa com todas as posições checadas.
        """
        return self._mapa_checado

    def _obtem_caminho(self, pos_atual):
        """Obtém o menor caminho entre os pontos.

        Retorna um tupla do tipo (posicao_atual, posicao_pai, custo). A 'posicao_atual' é
        uma tupla contendo a posição (y, x) do último ponto andes de conectar com o ponto
        de destino. A 'posicao_pai' é uma tupla da posição (y, x) do ponto pai (antecedente) ao
        ponto retornado. E o 'custo' é o valor do custo dessa posição (definida pela função
        de custo).

        Parameters
        ----------
        pos_atual : tuple
            Posição atual no mapa.

        Returns
        -------
        tuple or None
            Tupla contendo as informações da posição anterior a de destino. Se não encontrou
            um caminho, retorna None.
        """
        # Se o ponto inicial não puder ser checado, retorna None
        if self._mapa[pos_atual] == 1:
            return None

        while True:
            # Se a lista aberta está vazia, significa que não foi possível traçar um caminho
            if len(self._lista_aberta) == 0:
                return None

            # Ordena a lista conforme o custo para obter o elemento com menor custo
            self._lista_aberta.sort(key=lambda var: var[2])
            ponto = self._lista_aberta[0]

            # Remove o ponto atual da lista aberta e adiciona à fechada
            self._lista_aberta.pop(0)
            self._lista_fechada.append(ponto)

            # Novas posições (pontos)
            direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)] + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            novas_posicoes = [tuple(np.array(ponto[0]) + np.array(direcao)) for direcao in direcoes]

            # Informação se é um deslocamento diagonal
            diagonal = [x[0] != 0 and x[1] != 0 for x in direcoes]
            novas_posicoes = zip(novas_posicoes, diagonal)

            for nova_posicao in novas_posicoes:
                eh_diagonal = nova_posicao[1]
                nova_posicao = nova_posicao[0]

                # Encontrou o ponto final
                if nova_posicao == self._pos_fim:
                    return ponto

                # Adiciona os vizinhos à lista aberta
                elif self._checa_pos_valida(nova_posicao):
                    custo = self._computa_custo(nova_posicao, ponto[2], eh_diagonal)
                    self._lista_aberta.append((nova_posicao, ponto[0], custo))
                    self._mapa_checado[nova_posicao] = 1

    def _gera_vetor_caminho(self, penultimo_ponto):
        """Gera e retorna um vetor com todos os pontos do caminho.

        O primeiro elemento do vetor é o ponto inicial. O último é o ponto de destino (final).

        Ao gerar o caminho, as posições checadas são colocadas no vetor de checados 'vetor_fechado'.
        Assim, é possível acessar a 'posição_pai' por meio desse vetor. Como os elementos desse vetor
        possuem a estrutura (posicao_inicial, posicao_pai, custo), mesma usada no método
        :meth:`_obtem_caminho`, é possível, recursivamente, acessar todos os pontos do caminho
        saltando entre os elementos do 'vetor_fechado'.

        Parameters
        ----------
        penultimo_ponto : tuple
            Ponto anterior ao ponto final. Informações da posição anterior ao ponto final.

        Returns
        -------
        list or None
            Lista com todos os pontos do caminho. Se não foi possível traçar um caminho, retorna None.
        """
        # Se não conseguiu traçar um caminho, retorna None
        if penultimo_ponto == None:
            return None

        vetor_caminho = []
        pos = penultimo_ponto
        while pos[1] != None:
            # Adiciona a posição atual ao vetor
            vetor_caminho.append(pos[0])

            # Altera a variável 'pos' para o pai (antecessor) dela
            pos = [ x for x in self._lista_fechada if x[0] == pos[1]]
            pos = pos[0]

        else:
            # Posição do ponto inicial
            vetor_caminho.append(pos[0])

            # É necessário inverter o vetor antes de retornar para que ele comece pelo ponto
            # inicial e termine no de destino.
            return vetor_caminho[::-1]

    def _ponto_smoothing(self, vetor, indice, n_pontos):
        """Aplica o algorítimo de suavização a um ponto.

        O ponto a ser suavizado é o determinado pelo *indice* do *vetor*. O algorítimo de suavização
        é baseado na média dos seus *n_pontos* adjacentes.

        Parameters
        ----------
        vetor : list
            Vetor com os pontos.

        indice : int
            Indice do ponto no *vetor*.

        n_pontos : int
            Quantidade de pontos adjacentes usados na suavização.

        Returns
        -------
        tuple
            Ponto suavizado.
        """
        valor = (0, 0)
        divisor = 0
        offset = int((n_pontos-1)/2)
        vetor_tamanho = len(vetor)

        # Calcula a média dos elementos próximos do índice (quantidade de elementos próximos é definida por *n_pontos*)
        for n in range(n_pontos):
            i = indice + n - offset

            # Adiciona o ponto ao valor da média apenas se ele existir
            if i >= 0 and i<vetor_tamanho:
                divisor += 1
                valor = (valor[0]+vetor[i][0], valor[1]+vetor[i][1])

        # Divide pelo valor de divisor para obter a média
        valor = (int(valor[0]/divisor), int(valor[1]/divisor))

        return valor

    def _vetor_smoothing(self, vetor, n_pontos):
        """Aplica o algorítimo de suavização aos pontos de um vetor.

        O algorítimo de suavização é o mesmo usado pelo método :meth:`_ponto_smoothing()`.

        Parameters
        ----------
        vetor : list
            Vetor com os pontos.

        n_pontos : int
            Quantidade de pontos adjacentes usados na suavização.

        Returns
        -------
        list
            Lista com os pontos suavizados.
        """
        # Se não conseguiu traçar um caminho, retorna None
        if vetor == None:
            return None

        novo_vetor = []
        offset = int((n_pontos-1)/2)

        # Cada elemento do vetor
        for indice in range(-offset, len(vetor) + offset, 7):
            novo_vetor.append(self._ponto_smoothing(vetor, indice, n_pontos))

        return novo_vetor

    def _vetor_smoothing_media_movel(self, vetor, n_pontos):
        """Aplica o algorítimo de suavização aos pontos de um vetor. Usa média móvel.

        Funciona de forma similar ao método :meth:`_vetor_smoothing()`, mas o algorítimo de suavização
        não é o mesmo do método :meth:`_ponto_smoothing()`. Utiliza média móvel ao invés disso.

        Parameters
        ----------
        vetor : list
            Vetor com os pontos.

        n_pontos : int
            Quantidade de pontos adjacentes usados na suavização.

        Returns
        -------
        list
            Lista com os pontos suavizados por meio de média móvel.

        Note
        ----
        Esse método não está sendo utilizado atualmente pela classe. Foi deixado para caso deseje substituir
        o algoritmo de suavização por esse.
        """
        # Se não conseguiu traçar um caminho, retorna None
        if vetor == None:
            return None

        novo_vetor = []

        valor_total = (0, 0)
        n_valores = 0
        for valor in vetor[::-1]:
            valor_total = (valor_total[0] + valor[0], valor_total[1] + valor[1])
            n_valores += 1

            novo_vetor.append((int(valor_total[0]/n_valores), int(valor_total[1]/n_valores)))

        return novo_vetor[::-1*3]

    def _gera_mapa_caminho(self, vetor_caminho):
        """Retorna um mapa com o menor caminho traçado.

        Retorna um mapa com esse caminho. Esse mapa é um array Numpy do tipo matriz[y][x] de inteiros onde 1
        representa uma posição do caminho traçado, e 0 uma posição fora do caminho.

        As posições devem ser uma tupla do tipo (pos_y, pos_x).

        Esse método deve ser chamado após o :meth:`_obtem_caminho()`. As informações da posição
        relacionada a esse caminho serão usadas para gerar o mapa.

        Parameters
        ----------
        vetor_caminho : list
            Vetor com os pontos do caminho.

        Returns
        -------
        numpy.ndarray
            Mapa com o caminho percorrido.
        """
        # Se não conseguiu traçar um caminho, retorna None
        if vetor_caminho == None:
            return None

        # Mapa inicial (vazio)
        mapa = np.zeros(self._mapa_formato, dtype=np.uint8)

        for pos in vetor_caminho:
            mapa[pos] = 1

        return mapa

    def _gera_mapa_caminho_smoothing(self, vetor_caminho):
        """Retorna um mapa com o menor caminho traçado. Usa o algorítimo de suavização.

        Funciona de forma semelhante ao método :meth:`_gera_mapa_caminho`, mas com o algorítimo de suavização.

        Parameters
        ----------
        vetor_caminho : list
            Vetor com os pontos do caminho.

        Returns
        -------
        numpy.ndarray
            Mapa com o caminho percorrido suavizado.
        """
        # Se não conseguiu traçar um caminho, retorna None
        if vetor_caminho == None:
            return None

        # Mapa inicial (vazio)
        mapa = np.zeros(self._mapa_formato, dtype=np.uint8)

        for n in range(len(vetor_caminho)-1):
            cv.line(mapa, vetor_caminho[n][::-1], vetor_caminho[n+1][::-1], (1, 1, 1), 1)

        return mapa

    def _checa_pos_valida(self, pos):
        """Checa se uma posição é valida para entrar na lista aberta.

        A posíção deve ser uma tupla do tipo (y, x).

        Fatores levados em conta ao checar a validade:

        * se a posição é uma parede (ou já esteve na lista aberta)
        * se a posição pertence ao mapa (não está extrapolando os limites)

        Parameters
        ----------
        pos : tuple
            Posição que será testada.

        Returns
        -------
        bool
            Se a posição é valida para entrar na lista aberta.
        """
        # Se está fora da região do mapa, é considerada inválida
        if (pos[0] >= self._mapa_formato[0] or pos[0] < 0) or (pos[1] >= self._mapa_formato[1] or pos[1] < 0):
            return False

        elif self._mapa_checado[pos] == 1:
            return False

        else:
            return True

    def _computa_custo(self, posicao_atual, custo_anterior, passo_diagonal=False):
        """Computa o custo associado a uma posição do mapa.

        Acumula o custo da posição anterior (pai), mais o custo de um passo (configurado ao
        instanciar o objeto), mais o custo da função heurística e o custo definido pela
        matriz de custo extra (se houver uma).

        Se o passo (mudança de posição) ocorre na diagonal, o custo do passo é 0.414 vezes maior.

        Parameters
        ----------
        posicao_atual : tuple
            Posição atual do ponto.

        custo_anterior : float
            Custo do ponto anterior.

        passo_diagonal : bool
            Se o passo ocorre na diagonal.

        Returns
        -------
        float
            Custo do ponto atual.
        """
        custo = custo_anterior + self._funcao_heuristica(posicao_atual) + self._passo

        # Se esttá na diagonal, o passo é 0.414 vezes maior
        if passo_diagonal:
            custo += self._passo*0.414

        # Aplica o mapa de custo
        if self._mapa_custo is not None:
            custo += self._mapa_custo[posicao_atual]

        return custo

    def _funcao_heuristica(self, pos_atual):
        """Função heurística do modelo.

        Consiste na distância entre os dois pontos (atual e final).

        Parameters
        ----------
        pos_atual : tuple
            Posição ponto atual.

        Returns
        -------
        float
            Custo associado a função heurística.
        """
        return math.sqrt(
                (pos_atual[0] - self._pos_fim[0])**2 +   # Distância do eixo y
                abs(pos_atual[1] - self._pos_fim[1])**2  # Distância do eixo x
                )
