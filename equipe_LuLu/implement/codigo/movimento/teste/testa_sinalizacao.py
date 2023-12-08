#!/bin/env python3


"""Testa a sinalização do Wall-e de quando encontra lixo.

Meche os braços e aciona o buzzer.
"""


import teste
import fake_RPi
import modulos.motores
import modulos.movimentacao


if __name__ == "__main__":
    mov = modulos.movimentacao.Movimento(
        (24, 25, 18, 23),
        (22, 27, 17),
        7
    )

    mov.sinaliza_lixo()
    #  mov.sinaliza_lixo()
