<a id="documentacao-dos-codigos-em-python-do-projeto-lixeira-movel-com-wall-e"></a>

# Documentação dos códigos em Python do projeto Lixeira móvel com Wall-e

O código em python está estruturado em módulos que implementam funcionalidades individuais. Cada módulo possui seus próprios submódulos e scripts de teste. Esses módulos são usados pelo programa principal para implementar o Walle.

A seguir, estão os módulos do projeto e seus respectivos submódulos e scripts de teste

<a id="interface"></a>

## Interface

Módulo que implementa a interface de usuário e a comunicação que permite controlar o Wall-e.

<a id="submodulos"></a>

### Submódulos:

| [`codigo.interface.modulos`](_autosummary/codigo.interface.modulos.md#module-codigo.interface.modulos)   |    |
|----------------------------------------------------------------------------------------------------------|----|

<a id="scrpipts-de-teste"></a>

### Scrpipts de teste:

| [`codigo.interface.teste`](_autosummary/codigo.interface.teste.md#module-codigo.interface.teste)   |    |
|----------------------------------------------------------------------------------------------------|----|

<a id="segmentacao"></a>

## Segmentação

Módulo responsável por implementar a segmentação de imagens usada na identificação de colisão.

<a id="datasets"></a>

### Datasets:

Esses são os scrptis usados para gerar os datasets de treinamento e validação do modelo de segmentação.

| [`codigo.segmentacao.datasets`](_autosummary/codigo.segmentacao.datasets.md#module-codigo.segmentacao.datasets)          |    |
|--------------------------------------------------------------------------------------------------------------------------|----|
| [`codigo.segmentacao.datasets.CG`](_autosummary/codigo.segmentacao.datasets.CG.md#module-codigo.segmentacao.datasets.CG) |    |

<a id="scripts-de-treinamento"></a>

### Scripts de treinamento:

Esses são os scripts usados para treinar o modelo de segmentação.

| [`codigo.segmentacao`](_autosummary/codigo.segmentacao.md#module-codigo.segmentacao)   |    |
|----------------------------------------------------------------------------------------|----|

<a id="id1"></a>

### Submódulos:

| [`codigo.segmentacao.modulos`](_autosummary/codigo.segmentacao.modulos.md#module-codigo.segmentacao.modulos)   |    |
|----------------------------------------------------------------------------------------------------------------|----|

<a id="scripts-de-teste"></a>

### Scripts de teste:

| [`codigo.segmentacao.teste`](_autosummary/codigo.segmentacao.teste.md#module-codigo.segmentacao.teste)   |    |
|----------------------------------------------------------------------------------------------------------|----|

<a id="controlador"></a>

## Controlador

Módulo que implementa o Controlador do Wall-e no modo autônomo.

<a id="id2"></a>

### Submódulos:

| [`codigo.controlador.modulos`](_autosummary/codigo.controlador.modulos.md#module-codigo.controlador.modulos)   |    |
|----------------------------------------------------------------------------------------------------------------|----|

<a id="id3"></a>

### Scrpipts de teste:

| [`codigo.controlador.teste`](_autosummary/codigo.controlador.teste.md#module-codigo.controlador.teste)   |    |
|----------------------------------------------------------------------------------------------------------|----|
