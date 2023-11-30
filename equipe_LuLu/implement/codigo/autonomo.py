#!/bin/env python3


"""Implementação do modo autônomo.

O controle do Wall-e no modo autônomo pode ser feito usando a classe :class:`Auto`. Deve ser fornecido o
"""


from interface.modulos.TLSstream import TLSclient
from interface.modulos.interface import Interface
from segmentacao.modulos.interpretador import Segmentador
from controlador.modulos.controlador import Controlador
from identificacao.modulos.identificador import Identificador
import cv2 as cv


class Auto():
    """Classe que implementa o controle do Wall-e no modo autônomo.

    Segementa a imagem para obter uma mascara de objetos colidíveis. Identifica o lixo mais próximo e aplica ao controlador.
    Envia as velocidades linear e angular do controlador para o Wall-e.

    Ao iniciar a classe, é necessário fornecer a interface, o enviador de comandos, o
    segmentador de imagens, o controlador e o path do modelo do haar cascade usado para identificar o lixo.

    Para processar uma imagem (modo autônomo), use o método :func:`processa_imagem`.
    """

    def __init__(
            self, interface: Interface, enviador : TLSclient, segmentador : Segmentador
            , controlador : Controlador, path_haar : str
            ):
        """Inicialização da classe.

        Deve-se fornecer a interface gráfica, pois o resultado do processamento será apresentado na interface.
        Deve-se fornecer, o enviador de comandos, para o modo autônomo poder envar comandos para o Wall-e.

        Precisa do segmentador de imagens para obter a máscara de objetos colidíveis. Necessário o path do
        modelo do haar cascade usado para identificar o lixo. O resultado do segmentador e do identificador de objetos
        são aplicados no controlador.

        Parameters
        ----------
        interface : interface
            A interface gráfica do suário.

        enviador : TLSclient
            O enviador de comandos.

        segmentador : Segmentador
            O segmentador de imagens usado para identificar regiões colidíveis.

        controlador : Controlador
            O controlador que determina a velocidade linear e angular no modo autônomo.

        path_haar : str
            O path do modelo do haar cascade usado para identificar o lixo.
        """
        self._interface = interface
        self._enviador = enviador
        self._segmentador = segmentador
        self._controlador = controlador

        self._ident_lixo = Identificador(path_haar)

        self._imagem = None

    def enviar_dados(self, dados: bytes):
        """Envia os dados para o Wall-e.

        Os dados devem estar no formato de bytes.

        Parameters
        ----------
        dados: bytes
            Dados a serem enviados para o Wall-e.
        """
        self._enviador.send(dados)

    def processa_imagem(self, imagem, BGR=False, debug=False):
        """Processamento da imagem (modo autônomo).

        Realiza o processamento do modo autônomo na imagem recebida.

        O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais).

        Parameters
        ----------
        imagem : numpy.ndarray
            A imagem a ser processada.

        BGR : bool, default False
            Se a imagem for no formato BGR.

        debug : bool, default False
            Se a imagem de debug deve ser exibida na interface.
        """
        # Apenas processa a imagem se a anterior já finalizou
        if self._imagem is None:
            self._imagem = imagem
        else:
            return

        # Converte para RGB se estiver no formato BGR
        if BGR:
            imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)

        # Segmentação
        resultado_segmentacao = self._segmentador.retorna_imagem_segmentada(imagem)
        mascara = self._segmentador.retorna_mascara(None)

        # Identificação do lixo
        self._ident_lixo.define_frame(imagem, resultado_segmentacao)
        posicao_mais_proxima, img_debug_IA = self._ident_lixo.identifica_lixo_proximo(None, debug=True)

        # Controlador
        self._controlador.mostra_colisoes(mascara, debug=True)
        linear, angular, imagem = self._controlador.calcula_direcao(None, None, debug=True)

        # Envia a velocidade linera e angular
        self.enviar_dados(f"{linear},{angular}".encode())

        if debug:
            # Junta o resultado da segmentação com o do controlador em uma operação de blend
            imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
            resultado_segmentacao = cv.resize(img_debug_IA, imagem.shape[:2])
            imagem = cv.addWeighted(resultado_segmentacao, 0.5, imagem, 0.5, 0)

            # Apresentação na interface
            self._interface.atualiza_frame(imagem)

        # Permite que o próximo frame seja processado
        self._imagem = None
