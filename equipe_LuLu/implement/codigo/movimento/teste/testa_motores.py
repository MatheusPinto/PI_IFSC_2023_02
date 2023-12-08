#!/bin/env python3


"""Testa os motores DC.

Testa a classe :class:`~codigo.movimento.modulos.motores.DC` que controla os motores DC.
"""

import teste
import fake_RPi
from modulos.motores import configura_GPIO, DC


if __name__ == "__main__":
    configura_GPIO("BOARD")

    dc = DC(8, 25, 24, 18)
    
    print("\nTeste 1.")
    dc.velocidade_motor_E(50)
    dc.velocidade_motor_D(-25)

    print("\nTeste 2.")
    dc.velocidade_motor_E(-12)
    dc.velocidade_motor_D(75)
    
    dc.desliga()


