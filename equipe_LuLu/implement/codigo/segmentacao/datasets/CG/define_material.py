#!/bin/env python3


"""Altera os materiais dos objetos entre os materiais originais e as máscaras.

Esse script deve ser executado dentro do Blender na interface de 'Scripting' dele.

Escolha qual material usar alterando o parâmetro 'MATERIAL_INDICE'. O valor 1 aplica
o material original, e 2 aplica a máscara.
"""


import bpy


# Parâmetros do script
MATERIAL_INDICE = 1


if __name__ == "__main__":
    for objeto in bpy.data.collections["Collection"].all_objects:
        # Nome do material no índice escolhido
        nome_material = objeto.material_slots[MATERIAL_INDICE].name

        # Atualiza o material atual para o de escolhido pelo índice
        objeto.active_material_index = 0
        objeto.active_material = bpy.data.materials[nome_material]
