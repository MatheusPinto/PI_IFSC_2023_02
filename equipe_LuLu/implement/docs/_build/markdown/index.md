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

<a id="identificacao-de-lixo"></a>

## Identificação de lixo

Módulo responsável por implementar a identificação de lixo.

<a id="id4"></a>

### Submódulos:

| [`codigo.identificacao.modulos`](_autosummary/codigo.identificacao.modulos.md#module-codigo.identificacao.modulos)   |    |
|----------------------------------------------------------------------------------------------------------------------|----|

<a id="id5"></a>

### Scrpipts de teste:

| [`codigo.identificacao.teste`](_autosummary/codigo.identificacao.teste.md#module-codigo.identificacao.teste)   |    |
|----------------------------------------------------------------------------------------------------------------|----|

<a id="movimento"></a>

## Movimento

Modulo que implementa a movimentação do Wall-e. Usado tanto no modo teleoperado quanto no autônomo.

<a id="id6"></a>

### Submódulos:

| [`codigo.movimento.modulos`](_autosummary/codigo.movimento.modulos.md#module-codigo.movimento.modulos)                |    |
|-----------------------------------------------------------------------------------------------------------------------|----|
| [`codigo.movimento.fake_RPi.RPi`](_autosummary/codigo.movimento.fake_RPi.RPi.md#module-codigo.movimento.fake_RPi.RPi) |    |

<a id="id7"></a>

### Scrpipts de teste:

| [`codigo.movimento.teste`](_autosummary/codigo.movimento.teste.md#module-codigo.movimento.teste)   |    |
|----------------------------------------------------------------------------------------------------|----|

<a id="scrpipts-de-teste-da-etapa-de-validacao"></a>

### Scrpipts de teste da etapa de validação:

| [`codigo.movimento.teste_validacao`](_autosummary/codigo.movimento.teste_validacao.md#module-codigo.movimento.teste_validacao)   |    |
|----------------------------------------------------------------------------------------------------------------------------------|----|

<a id="codigo-principal"></a>

## Código principal

O código principal está disponível nos arquivos da interface de usuário e do Wall-e.

| [`codigo`](_autosummary/codigo.md#module-codigo)   |    |
|----------------------------------------------------|----|

Além disso, há alguns scripts de teste para os código como um todo.

| [`codigo.teste`](_autosummary/codigo.teste.md#module-codigo.teste)   |    |
|----------------------------------------------------------------------|----|
