#!/bin/env python3


"""Cria os certificados e chaves privadas usadas na comunicação do Wall-e com o usuário.

Atençâo: executar esse script sobrescreverá as chaves anteriores.
"""


import subprocess
import os


# Parâmetros gerais
TIPO="rsa:4096"                           # Tipo de chave que será gerada
diretorio_credenciais="env/comunicacao/"  # Onde será salvo as credenciais do cliente e do Wall-e


def cria_chave(tipo: str, cert_path: str, key_path: str, duracao="365"):
    """
    Cria um certificado e chave privada com o OpenSSL.

    O tipo de chave é definida pelo parâmetro *tipo*. A duração em dias do
    cerificado é definida por *duracao*. Após esse tempo passar, o
    certificado deixará de ser válido. O certificado será salvo com nome
    *cert_path* e a chave privada será salva com nome *key_path*.

    Parameters
    ----------
    tipo: str
        Tipo de chave que será gerada.

    cert_path: str
        Arquivo onde será salvo o certificado.

    key_path: str
        Arquivo onde será salvo a chave privada.

    duracao: str, default="365"
        Duração do certificado em dias.
    """
    subprocess.run([
        "openssl",
        "req",
        "-newkey",
        tipo,
        "-x509",
        "-days",
        duracao,
        "-nodes",
        "-subj",
        "/C=/ST=/L=/O=/CN=",
        "-out",
        cert_path,
        "-keyout",
        key_path
        ])


if __name__ == '__main__':
    # Cria o diretório onde serão salvas as credenciais
    if not os.path.exists(diretorio_credenciais):
        os.makedirs(diretorio_credenciais)

    # Credenciais do cliente
    cria_chave(
            TIPO,
            diretorio_credenciais + "client.crt",
            diretorio_credenciais + "client.key"
            )

    # Credenciais do Wall-e
    cria_chave(
            TIPO,
            diretorio_credenciais + "walle.crt",
            diretorio_credenciais + "walle.key"
            )
