#!/bin/env python3


"""Implementação do modo autônomo.

O controle do Wall-e no modo autônomo pode ser feito usando a classe :class:`Auto`.
Integra todos os componentes do modo autônomo:

- Segmentador
- Controlador
- Identificador
"""


from interface.modulos.TLSstream import TLSclient
from interface.modulos.interface import Interface
from segmentacao.modulos.interpretador import Segmentador
from controlador.modulos.controlador import Controlador
from identificacao.modulos.identificador import Identificador
import cv2 as cv
import numpy as np


class Auto():
    """Classe que implementa o controle do Wall-e no modo autônomo.

    Segmenta a imagem para obter uma máscara de objetos colidíveis. Identifica o lixo mais próximo.
    Aplica essas informações ao controlador. As velocidades linear e angular retornadas pelo controlador
    são enviadas para o Wall-e. Assim como o sinal de identificação de lixo.

    Ao iniciar a classe, é necessário fornecer a interface, o enviador de comandos, o
    segmentador de imagens, o controlador e o path do modelo do haar cascade usado para identificar o lixo.

    Para processar uma imagem (modo autônomo), use o método :func:`processa_imagem()`.
    """

    def __init__(
            self, interface: Interface, enviador : TLSclient, segmentador : Segmentador
            , ctrl : Controlador, path_haar : str = None
            ):
        """Inicialização da classe.

        Deve-se fornecer a interface gráfica, pois o resultado do processamento será apresentado na interface.
        Deve-se fornecer, o enviador de comandos, para o modo autônomo poder enviar comandos para o Wall-e. A
        apresentação dos resultados na interface e o envio de comandos para o Wall-e já é feito pelo método
        :meth:`processa_imagem()`. Não é necessário código externo para isso.

        Precisa do segmentador de imagens para obter a máscara de objetos colidíveis. Necessário o path do
        modelo do Haar Cascade usado para identificar o lixo. A instanciação do identificador de lixos é feita
        automaticamente, basta fornecer o arquivo do Haar Cascade.

        Parameters
        ----------
        interface : Interface
            A interface gráfica do suário.

        enviador : TLSclient
            O enviador de comandos.

        segmentador : Segmentador
            O segmentador de imagens usado para identificar regiões colidíveis.

        ctrl : Controlador
            O controlador que determina a velocidade linear e angular no modo autônomo.

        path_haar : str, default None
            O path do modelo do Haar Cascade usado para identificar o lixo.
        """
        self._interface = interface
        self._enviador = enviador
        self._segmentador = segmentador
        self._ctrl = ctrl

        if path_haar is not None:
            self._ident_lixo = Identificador(path_haar, (128, 128))
        
        else:
            self._ident_lixo = None

        # Imagens inicias
        self._BGR = None
        self._RGB = None

    def _envia_texto(self, texto: str):
        """Envia um texto para o Wall-e.

        O texto é convertido em bytes antes de ser enviado para o Wall-e.

        Parameters
        ----------
        texto : bytes
            Texto a ser enviado para o Wall-e.
        """
        self._enviador.send(texto.encode())

    def processa_imagem(self, imagem, BGR=False, debug=False):
        """Processamento da imagem (modo autônomo).

        Realiza o processamento do modo autônomo na imagem recebida. Segmenta a imagem recebida, obtém
        o objeto mais próximo, aplica ao controlador para definir a velocidade linear, angular e se deve
        sinalizar lixo. Os comandos para controlar o Wall-e levando isso em conta já são enviados para o
        Wall-e por meio desse método. Não é necessário código externo para tal.

        O frame processado (com ou sem debug) será exibido na interface. Isso também é feito por esse método
        e não é necessário código externo para tal.

        O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais). O
        OpenCV já usa esse formato por padrão. A princípio, dever do tipo RGB. Más é possível que seja do
        tipo BGR, contanto que o parâmetro *BGR* seja definido como True.

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser processada.

        BGR : bool, default False
            Se a imagem está no formato BGR.

        debug : bool, default False
            Se a imagem de debug deve ser exibida na interface. Caso seja false, exibe a imagem normal.
        """
        # Apenas processa a imagem se a anterior já finalizou
        if self._BGR is None:
            self._BGR = imagem
        else:
            return

        # Conversão de formato de imagens. Deve ser fornecido ela tanto em BGR, quanto em RGB,
        if BGR:
            self._RGB = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
            self._BGR = imagem
        else:
            self._BGR = cv.cvtColor(imagem, cv.COLOR_RGB2BGR)
            self._RGB = imagem

        # Segmentação
        img_debug = self._segmentador.retorna_imagem_segmentada(self._RGB, redimensiona=True)
        mascara = self._segmentador.retorna_mascara(None, redimensiona=True)

        if debug:
            # A imagem retornada pelo segmentador possui formato BGR, mas as demais operações
            # devem ser feitas com imagens no formato BGR. Esse processamento não faz sentido
            # no caso de *debug* ser False, já que a imagem não será usada.
            img_debug = cv.cvtColor(img_debug, cv.COLOR_RGB2BGR)

        # Identificação do lixo
        posicao = None
        if self._ident_lixo is not None:
            self._ident_lixo.define_frame(self._BGR, img_debug)
            posicao = self._ident_lixo.identifica_lixo_mais_proximo(None, debug=debug)

            # Troca o eixo x e y no ponto. O identificador de lixo e o controlador usam notações diferentes de pontos.
            if posicao is not None:
                x, y, l, a, cx, cy = posicao
                posicao = (cy, cx, l, a)

        # Controlador
        mascara = np.uint8(mascara)
        self._ctrl.define_mapa(mascara, img_debug)
        self._ctrl.mostra_colisoes(None, debug=debug)
        linear, angular, sinalizacao = self._ctrl.calcula_direcao(None, posicao, debug=debug)

        # Caso a sinalização esteja ativa, avisa para o Wall-e sinalizar o lixo. Caso contrário,
        # envia a velocidade linear e angular para o Wall-e.
        if sinalizacao:
            self._envia_texto("lixo")
        else:
            self._envia_texto(f"{linear},{angular}")

        # Apresentação na interface
        if debug:
            img_debug = cv.cvtColor(self._ctrl.retorna_imagem_debug(), cv.COLOR_BGR2RGB)
            self._interface.atualiza_frame(img_debug)

        else:
            self._interface.atualiza_frame(self._RGB)

        # Permite que o próximo frame seja processado
        self._BGR = None
        self._RGB = None
