# Código da interface e comunicação com o Wall-e.

Os códigos disponíveis nesse diretório são referentes a interface e comunicação do cliente com o Wall-e. Eles utilizam as chaves disponíveis no diretório '../env/comunicacao' que podem ser criadas conforme as instruções no [documento da página anterior](../)

A interface e a comunicação foi feita conforme especificado no [Design](../../../design/comunicacao.md).

Os módulos criados para implementar essa etapa estão no diretório ['modulos/'](modulos/). A documentação deles está disponível em [documentação dos módulos](../../docs/_build/markdown/_autosummary/codigo.interface.modulos.md).

Os scripts de teste estão no diretório ['teste/'](teste/). A documentação deles está disponível em [documentação dos scripts de teste](../../docs/_build/markdown/_autosummary/codigo.interface.teste.md).


## Dependências

É possível rodar os códigos no próprio computador para fins de teste. Para isso, é necessário ter o Python 3 e o módulo do OpenCV (usado para captura de câmera e processamento visual).

O módulo OpenCV podem ser instalado com o seguinte comando:

```shell
pip3 install opencv-python
```

Observações: é importante notar que o OpenSSL não é necessário para executar os códigos principais, apenas para gerar os certificados.
