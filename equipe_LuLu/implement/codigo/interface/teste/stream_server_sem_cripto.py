#!/bin/env python3


"""Teste do stream de dados - servidor (sem criptografia).

Funciona da mesma forma que o script 'stream_server.py', mas sem criptografia.

Deve ser executado junto ao script 'stream_client_sem_cripto.py'.
"""


import test
import modulos.TLSstream as TLSstream


# Parâmetros do script
HOST = "127.0.0.1"
PORT = 3000
log_pasta = "log/"
credencias_pasta="../../env/comunicacao"


if __name__ == "__main__":
    # Configuração do servidor
    server = TLSstream.TLSserver(log_file_path = log_pasta + "walle.log")

    # Função de callback
    def print_dados(self):
        """Apresenta os dados recebidos do cliente."""
        print(self.dados)

    # Configuração da conexão
    server.recv_set(print_dados)
    server.connect(HOST, PORT)

    # Espera a entrada de usuário antes de finalizar o servidor
    input()
    server.close()
