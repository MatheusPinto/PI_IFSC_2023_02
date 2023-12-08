#!/bin/env python3


"""Módulo dedicado ao registro de log.

Os logs são apresentados na saída padrão stdout e salvos em um arquivo pré-configurado.
Para isso, use a classe :class:`LogFile`.
"""


import time
import logging
import os


class LogFile:
    """Apresenta mensagens de log e as registra em um arquivo de log.

    As mensagens são apresentadas na saída padrão. O arquivo onde são salvas é definido pelo
    método :meth:`__init__()`.

    Para registra uma mensagem no log, utilize o método :meth:`register()`.

    É possível configurar um prefixo que será colocado no começo das mensagens de log. Veja o método
    :meth:`__init__()`.

    Examples
    --------
    Registrando um log genérico:

    >>> registrador = log.LogFile("server.log", "[Server] ")
    >>> registrador.register("Mensagem de log...")

    Registrando uma mensagem de erro:

    >>>    try:
    >>>        os.makedirs("diretório/")
    >>> 
    >>>    except FileExistsError:
    >>>        registrador.register("O diretório já existe!", exception=True)
    """

    def __init__(self, file_path='', prefixo=''):
        """Configura o arquivo onde salva a mensagem, e o prefixo delas.

        A mensagem será salva no arquivo fornecido pelo parâmetro *file_path*. Ele é relativo ao diretório
        atual. Também é possível usar um path absoluto, como: '/var/log/server.log'.

        É adicionado um prefixo à mensagem (tanto no arquivo salvo quanto no apresentado na saída padrão),
        definido pelo parâmetro *prefixo*

        Arguments
        ---------
        file_path: str, default=''
            Arquivo onde será registrado a mensagem de log. Se estiver vazio, então não registra nada em arquivo,
            apenas mostra na saída padrão.

        prefixo: str, default=''
            Prefixo que será inserido antes de toda mensagem de log. Por exemplo, pode-se usar "[server] " para
            indicar que é um log de servidor.
        """
        self._file_path = file_path
        self._prefix = prefixo

        # Cria o diretório do arquivo de log
        if file_path != '':
            try:
                os.makedirs(os.path.dirname(file_path))

            except FileExistsError:
                pass

    def register(self, log_msg: str, exception=False):
        """Mostra a mensagem de log e registra ela no arquivo de log.

        Se a mensagem de log corresponde a uma exceção sendo chamada após ela, use o parâmetro *exception=True*.
        Isso mostra a mensagem original da exceção após a de log.

        Arguments
        ---------
        log_msg: str
            Mensagem de log que será apresentada, e salva no arquivo.

        exception: bool, default=False
            Se a mensagem é referente a uma exceção. Se True, mostrará a mensagem da exceção.
        """
        # Apresenta a mensagem de log
        if exception:
            logging.exception(' ' + self._prefix + log_msg)
        else:
            print(self._prefix + log_msg)

        # Escreve a mensagem no arquivo
        if self._file_path != '':
            f = open(self._file_path, 'a')
            f.write(str(time.time()) + ": " + self._prefix + log_msg + '\n')
            f.close()
