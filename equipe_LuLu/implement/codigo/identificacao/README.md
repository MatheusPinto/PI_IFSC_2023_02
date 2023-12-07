# Código do algorítimo de identificação de lixo

Os códigos disponíveis nesse diretório são referentes ao identificador de lixo. O modelo do identificador foi treinado como descrito na [página do treinamento](../identificador).

O módulo [identificador.py](modulos/identificador.py) implementa a classe [Identificador](../../docs/_build/markdown/_autosummary/codigo.identificacao.modulos.identificador.md), responsável por gerenciar a identificação de lixo em alto nível e retornar a posição do lixo mais próximo conforme definido no [design do modo autônomo](../../../design/autonomo.md).

Os módulos criados para implementar esse projeto estão no diretório ['modulos/'](modulos/). A documentação deles está disponível em [documentação dos módulos](../../docs/_build/markdown/_autosummary/codigo.identificacao.modulos.md).

Os scripts de teste estão no diretório ['teste/'](teste/). A documentação deles está disponível em [documentação dos scripts de teste](../../docs/_build/markdown/_autosummary/codigo.identificacao.teste.md).


## Dependências

É possível rodar os códigos para fins de teste. Para isso, é necessário ter o Python 3 e os módulos do OpenCV e Numpy.

O módulo pode ser instalado com o seguinte comando:

```shell
pip3 install opencv-python numpy
```
