# Documentação do código em Python

Para gerar a documentação, é utilizado a ferramenta [Sphinx](https://www.sphinx-doc.org/en/master/). É um gerador de documentação bastante usado pela comunidade do Python. Ela gera documentação com base em arquivos [reST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html), mas também permite documentar o código com base nas docstrings dos arquivos, métodos, funções, atributos, entre outros.

Para gerar a documentação, é utilizado a extensão [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) do Sphinx, que converte os estilos padrão de docstrings do Google e do Numpy para os formatos usados pelo Sphinx.

A documentação gerada com o Sphinx é exportada em markdown usando a extensão [sphinx-markdown-builder](https://pypi.org/project/sphinx-markdown-builder/).

A documentação gerada pelo Sphinx para esse projeto está disponível em [documentação do código em Python](_build/markdown/index.md)

Para gerar a documentação, execute o script [cria_documentacao.sh](cria_documentacao.sh).


## Dependências

É necessário instalar o Sphinx e a extensão que implementa o suporte ao markdown.

```sh
pip3 install -U sphinx sphinx-markdown-builder
```

Além disso, como o [Sphinx](https://www.sphinx-doc.org/en/master/) importa os arquivos para ter acesso a sua documentação, é necessário ter todos os módulos necessários para executar todos os códigos instalados. Eles estão listados na [documentação principal do código](../codigo/README.md#dependencias).

**Observação:** O módulo [bpy](https://pypi.org/project/bpy/) não é necessário para executar nenhum código, visto que o [único script que depende dele](../codigo/segmentacao/datasets/CG/define_material.py) apenas é executado pelo [Blender](https://www.blender.org/). Todavia, ele é necessário para gerar a documentação. Instale-o com o seguinte comando:

```shell
pip3 install bpy
```


## Guias de estilo

O [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) suporta dois estilos padrão de documentação: o do Google e o do Numpy. O código desse projeto utiliza o estilo padrão do Numpy, conforme documentado no [Style guide](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) deles.
