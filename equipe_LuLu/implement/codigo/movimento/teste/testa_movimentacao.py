#!/bin/env python3


"""Testa a movimentação dos motores DC.

Eles são direcionados para frente.
"""


import teste
import fake_RPi
import modulos.motores
import modulos.movimentacao


if __name__ == "__main__":
    mov = modulos.movimentacao.Movimento(
        (26, 19, 13, 6),
        (21, 20, 16),
        7
    )
    mov.define_velocidade(100, 20)
