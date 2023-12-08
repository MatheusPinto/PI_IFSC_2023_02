# Código do datasets

Esse diretório possui a implementação dos datasets. Primeiro, é possível criar os datasets com o script [cria_dataset.py](cria_dataset.py).

Há um script para testar o dataset que, basicamente, mostra algumas imagens dele e suas respectivas máscaras: [testa_dataset.py](testa_dataset.py)

A documentação desses scripts está disponível em [documentação dos datasets](../../../docs/_build/markdown/_autosummary/codigo.segmentacao.datasets.md).

Para criar um dataset, é necessário preparar as imagens originais e a máscara em uma pasta. Por exemplo, "data/". As imagens originais devem estar dentro da pasta "data/original" e as máscaras, dentro de "pasta/mascara". Os nomes das imagens devem ser iguais aos das suas respectivas máscaras. Por exemplo, a imagem "pasta/original/1.png" tem uma máscara dada por "pasta/mascara/1.png". Para formar um dataset com essas imagens, basta adicionar a pasta "pasta/" ao diretório "imagens-dataset/". É possível haver mais de uma pasta com imagens e suas máscaras. Por exemplo, "imagens-dataset/pasta1", "imagens-dataset/pasta2" e assim por diante. Para criar o dataset com essas imagens, basta executar o script [cria_dataset.py](cria_dataset.py).

Um exemplo de estrutura do diretório "imagens-dataset" é a seguinte:

```
.
└── imagens-dataset
    ├── data
    │   ├── mascara
    │   │   ├── 0001.png
    │   │   ├── 0002.png
    │   │   └── 0003.png
    │   └── original
    │       ├── 0001.png
    │       ├── 0002.png
    │       └── 0003.png
    ├── pasta1
    │   ├── mascara
    │   │   ├── 0001.png
    │   │   ├── 0002.png
    │   │   └── 0003.png
    │   └── original
    │       ├── 0001.png
    │       ├── 0002.png
    │       └── 0003.png
    └── pasta2
        ├── mascara
        │   ├── 0001.png
        │   ├── 0002.png
        │   └── 0003.png
        └── original
            ├── 0001.png
            ├── 0002.png
            └── 0003.png
```

Para criar as imagens dos datasets, foi usado computação gráfica com o Blender, como descrito na página [CG](CG).


## Dependências

Para executar os códigos desse diretório é necessário ter o Python 3 e os módulos do Tensorflow e Matplotlib.

```shell
pip3 install tensorflow matplotlib
```
