#!/bin/env python3


"""Testa os motores de passo.

Testa a classe :class:`~codigo.movimento.modulos.motores.Passo` que controla os motores de passo.
"""


import teste
import fake_RPi
from modulos.motores import configura_GPIO, Passo


if __name__ == "__main__":
    configura_GPIO("BOARD")

    sg90 = Passo(8, 10)
    sg90.inicia(0)

    sg90.define_angulo_destino(180)

    for loop in range(0, 10):
        sg90.atualiza_angulo()
