# Documentação do código em Python

Para gerar a documentação, é utilizado a ferramenta Sphinx. É um gerador de documentação bastante usado pela comunidade do Python. Ela gera documentaçao com base em arquivos [reST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html), mas também permite documentar o código com base nas docstrings dos arquivos, métodos, funções, atributos, entre outros.

Para gerar a documentação, é utilizado a extensão [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) do Sphinx, que converte os estilos padrão de docstrings do Google e do Numpy para os formatos usados pelo Sphinx.

A documentação gerada com o Sphinx é exportada em markdown usando a extensão [sphinx-markdown-builder](https://pypi.org/project/sphinx-markdown-builder/).

A documentação gerada pelo Sphinx para esse projeto está disponível em [documentação do código em Python](_build/markdown/index.md)

## Dependências

É necessário instalar o Sphinx e a extensão que implementa o suporte ao markdown.

```sh
pip3 install -U sphinx sphinx-markdown-builder
```


## Guias de estilo

O [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) suporta dois estilos padrão de documentação: o do Google e o do Numpy. O código desse projeto utiliza o estilo padrão do Numpy, conforme documentado no [Style guide](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) deles.
