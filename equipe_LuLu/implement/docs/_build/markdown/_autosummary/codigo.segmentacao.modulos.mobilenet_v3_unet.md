<a id="module-codigo.segmentacao.modulos.mobilenet_v3_unet"></a>

<a id="codigo-segmentacao-modulos-mobilenet-v3-unet"></a>

# codigo.segmentacao.modulos.mobilenet_v3_unet

Modelo usado para segmentação de imagens.

Modelo: mobilenet_v3_unet

Baseado no código disponível em: [https://www.tensorflow.org/tutorials/images/segmentation](https://www.tensorflow.org/tutorials/images/segmentation)

Para criar o modelo de segmentação, use a função [`cria_mobilenet_v3_unet()`](#codigo.segmentacao.modulos.mobilenet_v3_unet.cria_mobilenet_v3_unet). É recomendado usar a
‘sparse_categorical_crossentropy’ como função de perda. Se usado essa função de perda,
não use apenas 1 canal de saída, use 2 pelo menos. Além disso, essa função de perda necessita
que a máscara de treinamento seja do tipo uint8.

<a id="codigo.segmentacao.modulos.mobilenet_v3_unet._bloco_padrao"></a>

### codigo.segmentacao.modulos.mobilenet_v3_unet.\_bloco_padrao(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Aplica um bloco padrão de convoluções ao modelo.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

Esse bloco será colocado entre as operações de downsample e upsample.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.

<a id="codigo.segmentacao.modulos.mobilenet_v3_unet._bloco_upsample"></a>

### codigo.segmentacao.modulos.mobilenet_v3_unet.\_bloco_upsample(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Bloco que aumenta as dimensões (n_linhas, n_colunas) dos dados, para formar a máscara.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.

<a id="codigo.segmentacao.modulos.mobilenet_v3_unet._conv_2D"></a>

### codigo.segmentacao.modulos.mobilenet_v3_unet.\_conv_2D(x, n_filtros, kernel)

Aplica um bloco de convolução 2D ao modelo.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
  * **kernel** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O tamanho do kernel das convoluções.

<a id="codigo.segmentacao.modulos.mobilenet_v3_unet.cria_mobilenet_v3_unet"></a>

### codigo.segmentacao.modulos.mobilenet_v3_unet.cria_mobilenet_v3_unet(formato_entrada: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), canais_saida=3)

Cria o modelo com mobilenetV3Large como backbone.
