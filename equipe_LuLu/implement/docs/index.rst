Documentação dos códigos em Python do projeto Lixeira móvel com Wall-e
======================================================================

O código em python está estruturado em módulos que implementam funcionalidades individuais. Cada módulo possui seus próprios submódulos e scripts de teste. Esses módulos são usados pelo programa principal para implementar o Walle.

A seguir, estão os módulos do projeto e seus respectivos submódulos e scripts de teste


Interface
---------

Módulo que implementa a interface de usuário e a comunicação que permite controlar o Wall-e.

Submódulos:
^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.interface.modulos

Scrpipts de teste:
^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.interface.teste


Segmentação
-----------

Módulo responsável por implementar a segmentação de imagens usada na identificação de colisão.

Datasets:
^^^^^^^^^

Esses são os scrptis usados para gerar os datasets de treinamento e validação do modelo de segmentação.

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.segmentacao.datasets
   codigo.segmentacao.datasets.CG

Scripts de treinamento:
^^^^^^^^^^^^^^^^^^^^^^^

Esses são os scripts usados para treinar o modelo de segmentação.

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.segmentacao

Submódulos:
^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.segmentacao.modulos

Scripts de teste:
^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.segmentacao.teste


Controlador
-----------

Módulo que implementa o Controlador do Wall-e no modo autônomo.

Submódulos:
^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.controlador.modulos

Scrpipts de teste:
^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.controlador.teste


Identificação de lixo
---------------------

Módulo responsável por implementar a identificação de lixo.

Submódulos:
^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.identificacao.modulos

Scrpipts de teste:
^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.identificacao.teste


Movimento
---------

Modulo que implementa a movimentação do Wall-e. Usado tanto no modo teleoperado quanto no autônomo.

Submódulos:
^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.movimento.modulos
   codigo.movimento.fake_RPi.RPi

Scrpipts de teste:
^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.movimento.teste

Scrpipts de teste da etapa de validação:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.movimento.teste_validacao


Código principal
----------------

O código principal está disponível nos arquivos da interface de usuário e do Wall-e.

.. autosummary::
   :toctree: _autosummary
   :recursive:

    codigo

Além disso, há alguns scripts de teste para os código como um todo.

.. autosummary::
   :toctree: _autosummary
   :recursive:

   codigo.teste
