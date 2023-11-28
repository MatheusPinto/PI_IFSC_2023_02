#!/bin/env python3


"""Módulo com a classe de implementação da interface.

A classe que implementa a interface é a :class:`Interface`. Para iniciá-la, deve-se passar o
path do arquivo de interface do Qt Designer (geralmente possuem a extensão '.ui') como argumento.

A classe :class:`_FiltroDeEventos` é utilizada na implementação da classe :class:`Interface` e não deve
ser usada pelo usuário final.
"""


from .TLSstream import TLSclient
from .video import decodifica_frame
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtUiTools as QtUiTools
import threading
import numpy as np
import cv2 as cv
import time
import math


class Interface(QtWidgets.QMainWindow):
    """Interface gráfica do usuário.

    A inicialização da interface necessita do arquivo de interface desenvolvido com o Qt Designer.

    Deve ser fornecido um recebedor de vídeo para que a interface receba os frames do Wall-e e
    apresente ao usuário. Para enviar os comandos do usuário para o Wall-e, deve ser fornecido um
    recebedor de comandos. Ambos são da classe :class:`TLSclient`.
    """

    def __init__(self, arquivo_ui: str, recebedor_video: TLSclient = None, enviador_comandos: TLSclient = None):
        """Inicialização da interface do usuário.

        Deve-se passar, como argumento, o path do arquivo de interface do Qt Designer.
        Esses arquivos possuem, tipicamente, a extensão '.ui'.

        Parameters
        ----------
        arquivo_ui : str
            Path do arquivo de interface do Qt Designer.

        recebedor_video : TLSclient
            Cliente que recebe os vídeos do Wall-e.

        enviador_comandos : TLSclient
            Cliente que envia os comandos para o Wall-e.
        """
        super().__init__()

        # Atributos principais
        self._recebedor_video = recebedor_video
        self._enviador_comandos = enviador_comandos
        self._interface_ativa = True
        self._tempo_enviador_comandos = time.time() - 1000.0
        self._enviador_comandos_ativo = False
        self.direcao = 50
        self.velocidade = 0
        self.atualiza_frame_automaticamente = True
        self.modo_automatico = False

        # Atributos dos eixos
        self.direcao_y = 0
        self.direcao_x = 0
        self.pode_checar_eixo_x = True
        self.pode_checar_eixo_y = True
        self.ultima_atualizacao_eixo_x = time.time() - 1000.0
        self.ultima_atualizacao_eixo_y = time.time() - 1000.0

        # A interface envia continuamente a direção que o Wall-e deve seguir.
        # Esse atributo determina o tempo em segundos entre cada um desses envios.
        self.delay_enviador = 0.1

        # Carrega o arquivo de interface do Qt Designer
        loader = QtUiTools.QUiLoader()
        arquivo_da_interface = QtCore.QFile(arquivo_ui)
        self._interface = loader.load(arquivo_da_interface, self)
        arquivo_da_interface.close()

        # Configura os eventos (necessário para ler o keyboard)
        self.filtro_de_eventos = _FiltroDeEventos(parent=self)
        self.installEventFilter(self.filtro_de_eventos)

        # Conecta os sinais dos widgets aos slots correspondentes
        self._interface.destroyed.connect(self.close)
        self._interface.Speed.valueChanged.connect(self._velocidade_slot)
        self._interface.Automatic.stateChanged.connect(self._botao_auto_slot)
        self._interface.Halt.clicked.connect(self._botao_desliga_slot)

        self._interface.Joystick.valueChanged.connect(self._joystick_slot)
        self._interface.Joystick.sliderPressed.connect(self._ativa_enviador_comandos)
        self._interface.Joystick.sliderReleased.connect(self._desativa_enviador_comandos)

        # Coloca o Joystick apontando para frente
        self._interface.Joystick.setValue(50)

        # Função de callback para o streaming de vídeo
        if self._recebedor_video != None:
            self._recebedor_video.recv_set(self._video_callback)
            self._video_callback_lista = []

        # Enviador de comandos para o wall-e
        if self._enviador_comandos != None:
            self._thread_enviador = threading.Thread(target=self._loop_envia_comandos)
            self._thread_enviador.start()

    def atualiza_frame(self, imagem : np.ndarray, BGR=False):
        """Atualiza o frame de vídeo da interface do usuário.

        A imagem deve ser um array numpy do tipo uint8 com a estrutura (linhas, colunas, canais).
        As imagens do OpenCV já possuem esse formato. Devem estar no formato RGB para funcionar.
        Caso estejam no formato BGR, use o parâmetro *BGR=True*. Essa informação é necessária
        para que ele seja convertido para RGB antes de ser aplicado na interface.

        O frame recebido é redimensionada se a imagem for muito pequena (menor do que 300px por
        300px) e apresentada na interface.

        Parameters
        ----------
        imagem : numpy.ndarray
            Imagem (array do numpy) que será exibida na interface. Em RGB, ou em BGR se o
            parâmetro *BGR=True*.

        BGR : bool, default False
            Se a imagem está no formato BGR.
        """
        # Conversão de BGR para RGB (Pyside utiliza imagens no formato RGB)
        if BGR:
            imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)

        # Redimensiona a imagem se for muito pequena (menor do que 300px por 300px)
        y = imagem.shape[0]
        x = imagem.shape[1]

        while x < 300 or y < 300:
            y *= 2
            x *= 2

        else:
            imagem = cv.resize(imagem, (y, x))

        # Aplica na interface
        img = QtGui.QImage(imagem, imagem.shape[1], imagem.shape[0], imagem.strides[0], QtGui.QImage.Format_RGB888)
        self._interface.Video.setPixmap(QtGui.QPixmap.fromImage(img))

    def adiciona_velocidade(self, valor, atualiza_barra=True):
        """Adiciona um valor à barra de velocidade do Wall-e.

        Funciona de forma semelhante ao método :meth:`_define_velocidade`. Os parâmetros são os mesmos.
        A diferença e que, em vez do valor recebido pelo método ser definido como o novo valor de
        velocidade, ele é adicionado ao valor atual.

        Parameters
        ----------
        valor : int
            Valor adicionado a velocidade.
        
        atualiza_barra : bool, default True
            Se deve ou não atualizar o barra de velocidade.
        """
        valor = self.velocidade + valor

        if valor > 99:
            self._define_velocidade(99, atualiza_barra)

        elif valor < 0:
            self._define_velocidade(0, atualiza_barra)

        else:
            self._define_velocidade(valor, atualiza_barra)

    def define_video_callback_lista(self, lista_callback : list):
        """Define a lista de funções de callback para o recebimento de imagem.

        Limpa a antiga lista (remove todos os callbacks, menos o padrão).

        As funções devem possuir a seguinte assinatura: *def callback(interface, RGB, BGR)*. *interface* é
        o objeto da interface que chamou a função de callback; e RGB e BGR são as imagens nesses respectivos
        formatos. As imagens são um array numpy do tipo uint8 com formato (linhas, colunas, canais).

        Parameters
        ----------
        lista_callback : list
            Nova lista de callback para o recebimento de imagem.
        """
        self._video_callback_lista = lista_callback

    def adiciona_video_callback(self, callback : callable):
        """Adiciona uma nova função de callback para o recebimento de imagem.

        Funciona da mesma forma que o método :meth:`define_video_callback_lista`, mas adiciona uma função de
        callback em vez de substituir todas.

        Parameters
        ----------
        callback : callable
            Nova função de callback para o recebimento de imagem.
        """
        self._video_callback_lista.append(callback)

    def atualiza_direcao_keyboard(self):
        """Atualiza a direção de movimento do Wall-e com base na tecla pressionada.

        Ao pressionar um teclado, é disparado um evento que o framework Qt recebe e envia para o
        :class:`_FiltroDeEventos`. Esse filtro é responsável por checar qual tecla foi pressionada e ajustar
        os atributos *self.direcao_x* e *self.direcao_y* com base nela. Esse método serve para ler
        os valores desses atributos e ajustar a direção do Wall-e com base neles.
        """
        # Os valores de *self.direcao_x* e *self.direcao_y* servem de referência. Eles podem ser -1, 0 ou 1.
        # São usados como índices da matriz abaixo. O valor obtido dessa matriz será o novo valor da
        # direção do Wall-e.
        valor = [
                [12, 0, 88],     # Joystick embaixo
                [25, None, 75],  # Joystick no meio (vertical)
                [37, 50, 63]     # Joystick em cima
                ][self.direcao_y + 1][self.direcao_x + 1]

        # Se não foi definida nenhuma direção, não atualiza a direção
        if valor != None:
            self._define_direcao(valor)

    def atualiza_enviador_comandos(self):
        """Reinicia o tempo do enviador de comandos.

        Reinicia o tempo para que o enviador de comandos envie os comandos para o wall-e.
        """
        self._tempo_enviador_comandos = time.time()

    def close(self):
        """Finaliza a interface de usuário.

        Depois disso, o objeto se torna inutilizável.
        """
        self._interface_ativa = False

        # Finalização da comunicação
        if self._recebedor_video != None:
            self._recebedor_video.close()

        if self._enviador_comandos != None:
            self._enviador_comandos.close()

        # Finalização das Threads
        self._thread_enviador.join()

        # Fecha a janela
        super().close()

    def _video_callback(self, recebedor_video : TLSclient):
        """Função de callback para o streaming de video.

        O objeto possui uma lista de funções de callback: *_video_callback_lista*. Esse
        método executa todas elas passando, como atributo, o próprio objeto e a imagem
        recebida. Por isso, as funções de callback devem possuir o formato *funcao(interface, RGB, BGR)*.

        A imagem recebida pela interface é um bytearray de um jpg. Esse método converte
        para um array numpy do tipo uint8 com a estrutura (colunas, linhas, canais). A
        imagem é fornecida para as funções de callback em RGB e BGR (padrão do OpenCV).

        Parameters
        ----------
        recebedor_video : TLSclient
            Recebedor de video.
        """
        # Caso o frame recebido tenha sido corrompido, ignora ele.
        if not isinstance(recebedor_video.dados, bytes):
            return -1

        # Conversão dos bytes recebidos para imagem RGB
        jpg = np.frombuffer(recebedor_video.dados, np.uint8)
        BGR = cv.imdecode(jpg, cv.IMREAD_COLOR)
        RGB = cv.cvtColor(BGR, cv.COLOR_BGR2RGB)

        # Atualiza o frame automaticamente
        if self.atualiza_frame_automaticamente:
            self.atualiza_frame(RGB)

        # Funções de callback
        for funcao in self._video_callback_lista:
            funcao(self, RGB, BGR)

    def _define_direcao(self, valor: int, atualiza_joystick=True):
        """Define a direção para onde o Wall-e está se movendo.

        O valor da direção é um número de 0 a 99 (mesma notação usada pelo widget 'Dial' do framework Qt).
        A correlação entre esse valor e a direção pode ser visto na tabela a seguir.

        +-------+----------+
        | Valor | direção  |
        +=======+==========+
        | 0     | Trás     |
        | 25    | Esquerda |
        | 50    | Frente   |
        | 75    | direita  |
        | 100   | Trás     |
        +-------+----------+

        Normalmente, esse método atualiza o joystick para o valor recebido, exceto se o parâmetro
        *atualiza_joystick* seja *False*.

        Parameters
        ----------
        valor : int
            Valor para qual a direção será definida.

        atualiza_joystick : bool
            Se deve ou não atualizar o joystick.
        """
        self.direcao = valor

        if atualiza_joystick:
            self._interface.Joystick.setValue(valor)

    def _envia_texto(self, texto: str, esperar=False):
        """Envia um texto para o Wall-e.

        Não envia uma mensagem se uma anterior ainda estiver sendo enviada. Cancela a operação
        e a mensagem será descartada. Caso *esperar=True*, ao invés de cancelar o envio da
        mensagem, espera até que seja possível enviá-la.

        Parameters
        ----------
        texto : str
            Texto a ser enviado para o Wall-e.

        esperar : bool, default False
            Se deve esperar a mensagem anterior ser enviada, ou cancelar o envio da atual.
        """
        if self._enviador_comandos != None:
            self._enviador_comandos.send(texto.encode(), esperar)

    def _loop_envia_comandos(self):
        """Constantemente envia os comandos de direção e velocidade para o Wall-e.

        O envio da velocidade e direção do Wall-e deve ocorrer continuamente, para permitir que o Wall-e
        pare de se mover caso não receba nenhum comando. Dessa forma, evita o risco do Wall-e se
        mover de forma desgovernada.

        Esse método deve ser executado em uma thread própria.
        """
        while self._interface_ativa:
            time.sleep(self.delay_enviador)

            # Checa se os eixos x e y estão desatualizados há muito tempo
            if not self._enviador_comandos_ativo:
                t = time.time()

                if self.pode_checar_eixo_y and t - self.ultima_atualizacao_eixo_y > 0.1:
                    self.direcao_y = 0

                if self.pode_checar_eixo_x and t - self.ultima_atualizacao_eixo_x > 0.1:
                    self.direcao_x = 0

                self.atualiza_direcao_keyboard()

            # Envia a velocidade e direção para o Wall-e
            if time.time() - self._tempo_enviador_comandos < 0.2 or self._enviador_comandos_ativo:
                # Converte para velocidade linear e angular
                angulo = (75 - self.direcao) * math.pi/50
                linear = int(self.velocidade * math.sin(angulo))
                angular = int(-self.velocidade * math.cos(angulo))

                self._envia_texto(f"{linear},{angular}")
    
    def _ativa_enviador_comandos(self):
        """Ativa o envio de comandos para o Wall-e."""
        self._enviador_comandos_ativo = True

    def _desativa_enviador_comandos(self):
        """Desativa o envio de comandos para o Wall-e."""
        self._enviador_comandos_ativo = False

    def _define_velocidade(self, valor : int, atualiza_barra=True):
        """Define a velocidade do Wall-e.

        O valor da velocidade é um número de 0 a 99. Sendo 0 a velocidade mínima, e 99 a máxima.

        Normalmente, atualiza a barra de velocidade para o valor fornecido, exceto se o parâmetro
        *atualiza_barra* seja *False*.

        Parameters
        ----------
        valor : int
            Valor para qual a velocidade será definida.

        atualiza_barra: bool, default True
            Se deve ou não atualizar o barra de velocidade.
        """
        self.velocidade = valor

        if atualiza_barra:
            self._interface.Speed.setValue(valor)

    def _joystick_slot(self):
        """Implementa o callback do joystick.

        Altera a direção de movimento do Wall-e.
        """
        valor = self._interface.Joystick.value()
        self._define_direcao(valor, False)

    def _velocidade_slot(self):
        """Implementa o callback da barra de velocidade.

        Altera a velocidade de movimento do Wall-e.
        """
        valor = self._interface.Speed.value()
        self._define_velocidade(valor, False)

    def _botao_auto_slot(self):
        """Implementa o callback do botão de controle do modo de operação.

        Altera entre o modo de controle do Wall-e em modo teleoperado ou autônomo.
        """
        if self._interface.Automatic.isChecked():
            self.modo_automatico = True

        else:
            self.modo_automatico = False

    def _botao_desliga_slot(self):
        """Implementa o callback do botão de desligar o Wall-e.

        Essa ação não pode ser desfeita por software. É necessário
        reiniciar o Wall-e diretamente no hardware.
        """
        self._envia_texto("halt", True)


class _FiltroDeEventos(QtCore.QObject):
    """Objeto do Qt que recebe os eventos da janela principal.

    Essa classe é usada apenas para implementar a classe :class:`Interface` e
    não deve ser usada pelo usuário final.
    """

    _tempo_direcao_y = 0
    _tempo_direcao_x = 0

    def eventFilter(self, widget, event):
        """Filtra os eventos e lê apenas os caracteres do teclado e os eventos do mouse.

        Os carácteres 'a', 's', 'w' e 'd' são usados para controlar a direção do joystick.
        Os eventos do mouse são usados para controlar tanto a direção do joystick, quanto a
        barra de velocidade.
        """
        # Apertando um botão
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.text()

            if key == 'w':
                widget.direcao_y = 1
                self.ultima_atualizacao_eixo_y = time.time()
                widget.pode_checar_eixo_y = False

            elif key == 'a':
                widget.direcao_x = -1
                self.ultima_atualizacao_eixo_x = time.time()
                widget.pode_checar_eixo_x = False

            elif key == 's':
                widget.direcao_y = -1
                self.ultima_atualizacao_eixo_y = time.time()
                widget.pode_checar_eixo_y = False

            elif key == 'd':
                widget.direcao_x = 1
                self.ultima_atualizacao_eixo_x = time.time()
                widget.pode_checar_eixo_x = False

            else:
                return False

            # Assim que define o novo botão pressionado, é necessário atualizar a direção de
            # movimento do Wall-e com base nas teclas selecionadas e atualizar o tempo do enviador
            # de comandos (para continuar enviando).
            widget.atualiza_direcao_keyboard()
            widget.atualiza_enviador_comandos()

        # Ao liberar uma tecla, checa se passou tempo o bastante para zerar um dos eixos
        elif event.type() == QtCore.QEvent.KeyRelease:
            key = event.text()
            t = time.time()

            if key == 'a' or key == 'd':
                widget.pode_checar_eixo_x = True

            if key == 'w' or key == 's':
                widget.pode_checar_eixo_y = True
 
        # Movendo o cursor do mouse
        elif event.type() == QtCore.QEvent.Wheel:
            passo = 10
            angulo_do_cursor = event.angleDelta().y()

            # Aumenta a velocidade
            if angulo_do_cursor > 0:
                widget.adiciona_velocidade(passo)

            # Diminui a velocidade
            else:
                widget.adiciona_velocidade(-passo)

        # Finalização da interface (não desliga o Wall-e, apenas a interface gráfica)
        elif event.type() == QtCore.QEvent.Close:
            widget.close()

        return False
