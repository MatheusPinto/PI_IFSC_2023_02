#!/bin/env python3


"""Adiciona o path da versão de simulação do módulo RPi.GPIO.

Permite usar uma versão falsa do módulo FRPi.GPIO para executar
os scripts que dependem desse módulo foradeuma Raspberry Pi.

Inclua esse script antes de incluir o módulo RPi.GPIO.
"""


import sys


# Adiciona o diretório base onde está a versão falsa do RPi.GPIO para poder incluí-lo
sys.path.append("../fake_RPi")
