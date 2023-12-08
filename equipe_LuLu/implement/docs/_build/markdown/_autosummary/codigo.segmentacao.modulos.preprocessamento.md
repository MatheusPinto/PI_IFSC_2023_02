<a id="codigo-segmentacao-modulos-preprocessamento"></a>

# codigo.segmentacao.modulos.preprocessamento

* **code:**
  [preprocessamento.py](../../../../codigo/segmentacao/modulos/preprocessamento.py)

<a id="module-codigo.segmentacao.modulos.preprocessamento"></a>

Funções de preprocessamento de imagem.

A função [`funcao_normalizacao()`](#codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao) é usada para normalizar os dados do dataset para poderem
ser usados no treinamento do modelo.

<a id="codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao"></a>

### codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao(imagem: Tensor, mascara: Tensor)

Função de normalização das imagens e máscaras.

A imagens originais possuem valores entre 0 e 255 para seus canais. Elas são normalizadas por meio dessa função.
A imagem original é padronizada pela função [`padroniza_imagem()`](codigo.segmentacao.modulos.padronizacao.md#codigo.segmentacao.modulos.padronizacao.padroniza_imagem) do
módulo [`padronizacao()`](codigo.segmentacao.modulos.padronizacao.md#module-codigo.segmentacao.modulos.padronizacao).

A máscara será normalizada entre 0 e 1. Além disso, ela é convertida para uint8. Isso é necessário porque a
função de perda do modelo é a ‘sparse_categorical_crossentropy’, e ela necessita que os valores esperados
(máscara) sejam inteiros. Para mais informações, veja:
[https://www.tensorflow.org/api_docs/python/tf/keras/losses/SparseCategoricalCrossentropy](https://www.tensorflow.org/api_docs/python/tf/keras/losses/SparseCategoricalCrossentropy)

* **Parâmetros:**
  * **imagem** (*tf.Tensor*) – A imagem a ser padronizada.
  * **mascara** (*tf.Tensor*) – A máscara a ser normalizada.
* **Retorna:**
  A imagem e máscara preprocessados.
* **Tipo de retorno:**
  (tf.Tensor, tf.Tensor)

<a id="codigo.segmentacao.modulos.preprocessamento.preprocessa_backbone"></a>

### codigo.segmentacao.modulos.preprocessamento.preprocessa_backbone(imagem: Tensor, mascara: Tensor)

Preprocessa a imagem e a máscara para o backbone.

A normalização é feita pela função [`funcao_normalizacao()`](#codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao). Após isso, a máscara é ajustada
para ser usada no modelo do backbone. O backbone é um modelo de classificação e sua saída não
é uma imagem, mas sim um tensor unidimensional de escalares indicando uma probabilidade. Por isso,
essa função computa a média dos elementos da máscara e considera ela uma probabilidade.

* **Parâmetros:**
  * **imagem** (*tf.Tensor*) – A imagem a ser normalizada.
  * **mascara** (*tf.Tensor*) – A máscara usada para computar a probabilidade do backbone.
* **Retorna:**
  A imagem e a probabilidade extraída da máscara.
* **Tipo de retorno:**
  (tf.Tensor, [float](https://docs.python.org/3/library/functions.html#float))
