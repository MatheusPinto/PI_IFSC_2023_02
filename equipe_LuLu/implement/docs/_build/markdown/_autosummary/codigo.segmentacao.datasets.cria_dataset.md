<a id="codigo-segmentacao-datasets-cria-dataset"></a>

# codigo.segmentacao.datasets.cria_dataset

* **code:**
  [cria_dataset.py](../../../../codigo/segmentacao/datasets/cria_dataset.py)

<a id="module-codigo.segmentacao.datasets.cria_dataset"></a>

Cria o dataset de treino para segmentação.

Utiliza imagens e suas respectivas máscaras na pasta definda pelo parâmetro ‘DATASETS_PATH’ para gerar
um dataset do tensorflow que será usado para treinar o algorítimo de segmentação de imagens. Elas são
carregadas em datasets separados (um para imagens e outro para as máscaras) e unidas depois. Cada
elemento do novo dataset será um conjunto com a imagem original e sua respectiva máscara, nessa ordem.

Para criar um dataset, é necessário preparar as imagens originais e a máscara em uma pasta. Por exemplo,
“data/”. As imagens originais devem estar dentro da pasta “data/original” e as máscaras, dentro de
“pasta/mascara”. Os nomes das imagens devem ser iguais aos das suas respectivas máscaras. Por exemplo, a
imagem “pasta/original/1.png” tem uma máscara dada por “pasta/mascara/1.png”. Para formar um dataset com
essas imagens, basta adicionar a pasta “pasta/” ao diretório dado pelo parâmetro ‘DATASETS_PATH’. É possível
haver mais de uma pasta com imagens e suas máscaras entro desse diretório.

Outro parâmetro importante é o formato das imagens, definido por ‘FORMATO_IMAGENS’. O tamanho das imagens
é uma tupla do tipo (n_linhas, n_colunas), em pixels. Ele será usado no melhoramento do dataset.

O dataset formado é melhorado com as seguintes operações:

- Espelhamento horizontal
- Espelhamento vertical
- Rotação
- Ajuste de brilho
- Ajuste de contraste
- Ajuste de escala

Elas são habilitadas pelos parâmetros ‘ESPELHA_HORIZONTAL’, ‘ESPELHA_VERTICAL’, ‘ROTACAO’, ‘BRILHO’,
‘CONTRASTE’, ‘ESCALA’. Por exemplo, se ‘ESPELHA_HORIZONTAL’ for True, a imagem será espelhada horizontalmente.

<a id="codigo.segmentacao.datasets.cria_dataset.cria_datatset_pasta"></a>

### codigo.segmentacao.datasets.cria_dataset.cria_datatset_pasta(path: [str](https://docs.python.org/3/library/stdtypes.html#str))

Cria um dataset de um conjunto de imagens e suas respectivas máscaras.

As imagens devem estar do diretório dado pelo parâmetro *path*. As imagens originais devem estar dentro
da pasta “<path>/original”, e suas máscaras na pasta “<path>/mascara/”.

Elas serão carregadas e unidas em um dataset do tensorflow em que cada elemnto corrsponde a uma par da
imagem original com sua respectiva máscara.

* **Parâmetros:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – O diretório do conjunto de imagens.

<a id="codigo.segmentacao.datasets.cria_dataset.melhora_dataset"></a>

### codigo.segmentacao.datasets.cria_dataset.melhora_dataset(imagem: Tensor, mascara: Tensor)

Melhora os elementos do dataset.

O melhoramento do dataset consiste em:

- Espelhamento horizontal
- Espelhamento vertical
- Rotação
- Brilho
- Contraste
- Escala

Esses fatores são definidos pelas constantes do script: ‘ESPELHA_VERTICAL’, ‘ESPELHA_HORIZONTAL’,
‘ROTACAO’, ‘BRILHO’, ‘CONTRASTE’ e ‘ESCALA’.

Todos esses fatores são ajustados na imagem original para diversificar o dataset. A máscara
será ajustada para corresponder com a imagem original ajustada.

Essa função foi feita para ser usada junto ao método ‘map()’ do datasets do Tensorflow.

* **Parâmetros:**
  * **imagem** (*tf.Tensor*) – A imagem a ser melhorada.
  * **mascara** (*tf.Tensor*) – A máscara a ser melhorada.
* **Retorna:**
  A imagem e a máscara melhoradas.
* **Tipo de retorno:**
  (tf.Tensor, tf.Tensor)
