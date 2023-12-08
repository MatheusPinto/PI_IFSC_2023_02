#!/bin/env python3


"""Teste do stream de dados - cliente.

Envia o seguinte conjunto de bytes para o servidor: b"12345".

O envio ocorre a cada 1 segundo.

Deve ser executado junto ao script 'stream_server.py'.
"""


import test
import modulos.TLSstream as TLSstream
import time


# Parâmetros do script
HOST = "127.0.0.1"
PORT = 3000
log_pasta = "log/"
credencias_pasta="../../env/comunicacao"


if __name__ == "__main__":
    # Configuração do cliente
    client = TLSstream.TLSclient(
            credencias_pasta + "/client.key",
            credencias_pasta + "/client.crt",
            credencias_pasta + "/walle.crt",
            log_pasta + "client.log"
            )

    # Configuração da conexão
    client.connect(HOST, PORT)

    # Envia, continuamente, uma mensagem para o servidor
    while True:
        client.send(b"12345")
        time.sleep(1)

    client.close()
