<a id="module-codigo.segmentacao.modulos.preprocessamento"></a>

<a id="codigo-segmentacao-modulos-preprocessamento"></a>

# codigo.segmentacao.modulos.preprocessamento

Funções de preprocessamento de imagem.

A função [`funcao_normalizacao()`](#codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao) é usada para normalizar os dados do dataset para poderem
ser usados no treinamento do modelo.

<a id="codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao"></a>

### codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao(imagem, mascara)

Função de normalização das imagens e máscaras.

A imagens originais possuem valores entre 0 e 255 para seus canais. Elas são ajustadas para que cada
valor esteja entre 0.0 e 1.0. (tipo float)

A máscara passa pelo mesmo processo. Além disso, ela é convertida para uint8. Isso é necessário porque a
função de perda do modelo é a ‘sparse_categorical_crossentropy’, e ela necessita que os valores esperados
(máscara) sejam inteiros. Para mais informações, veja:
[https://www.tensorflow.org/api_docs/python/tf/keras/losses/SparseCategoricalCrossentropy](https://www.tensorflow.org/api_docs/python/tf/keras/losses/SparseCategoricalCrossentropy)

* **Parâmetros:**
  * **imagem** (*tf.Tensor*) – A imagem a ser normalizada.
  * **mascara** (*tf.Tensor*) – A máscara a ser preprocessada.
* **Retorna:**
  A imagem e máscara normalizadas.
* **Tipo de retorno:**
  (tf.Tensor, tf.Tensor)

<a id="codigo.segmentacao.modulos.preprocessamento.preprocessa_backbone"></a>

### codigo.segmentacao.modulos.preprocessamento.preprocessa_backbone(imagem: Tensor, mascara: Tensor)

Preprocessa a imagem e a máscara para o backbone.

A normalização é feita pela função [`funcao_normalizacao()`](#codigo.segmentacao.modulos.preprocessamento.funcao_normalizacao). Após isso, a máscara é ajustada
para ser usada no modelo do backbone. Como o backbone é um modelo de classificação, a saída não
é uma imagem, mas sim um tensor unidimensional de escalares indicando uma probabilidade. Por isso,
essa função computa a média dos elementos da máscara e considera ela uma probabilidade.

* **Parâmetros:**
  * **imagem** (*tf.Tensor*) – A imagem a ser normalizada.
  * **mascara** (*tf.Tensor*) – A máscara a ser preprocessada.
* **Retorna:**
  A imagem e máscara preprocessadas.
* **Tipo de retorno:**
  (tf.Tensor, tf.Tensor)
