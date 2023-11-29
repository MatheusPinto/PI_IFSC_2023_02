<a id="module-codigo.segmentacao.modulos.modelo"></a>

<a id="codigo-segmentacao-modulos-modelo"></a>

# codigo.segmentacao.modulos.modelo

Modelo usado para segmentação de imagens.

Modelo: U-NET

Baseado no código disponível em: [https://pyimagesearch.com/2022/02/21/u-net-image-segmentation-in-keras/](https://pyimagesearch.com/2022/02/21/u-net-image-segmentation-in-keras/)

Para criar o modelo de segmentação, use a função [`modelo_unet()`](#codigo.segmentacao.modulos.modelo.modelo_unet). É recomendado usar a
‘sparse_categorical_crossentropy’ como função de perda. Se usado essa função de perda,
não use apenas 1 canal de saída, use 2 pelo menos. Além disso, essa função de perda necessita
que a máscara de treinamento seja do tipo uint8.

<a id="codigo.segmentacao.modulos.modelo._bloco_downsample"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_downsample(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Bloco que reduz as dimensões (n_linhas, n_colunas) dos dados, enquanto extrai informações deles.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.

<a id="codigo.segmentacao.modulos.modelo._bloco_entrada"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_entrada(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Bloco de entrada do modelo. Aplicado sobre a imagem inicial.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.

<a id="codigo.segmentacao.modulos.modelo._bloco_padrao"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_padrao(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Aplica um bloco padrão de convoluções ao modelo.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

Esse bloco será colocado entre as operações de downsample e upsample.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.

<a id="codigo.segmentacao.modulos.modelo._bloco_upsample"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_upsample(x, n_filtros, saida_codificador)

Bloco que aumenta as dimensões (n_linhas, n_colunas) dos dados, para formar a máscara.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
  * **saida_codificador** (*tf.Tensor*) – Saida do codificador que será concatenada como fluxo atual do modelo.

<a id="codigo.segmentacao.modulos.modelo._codificador"></a>

### codigo.segmentacao.modulos.modelo.\_codificador(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int), n_downsample: [int](https://docs.python.org/3/library/functions.html#int))

Cria o codificador do modelo (camadas de downsample).

Cria o codificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

O número de operações de downsample do codificador é definido por *n_downsample*. O número de filtros
(canais) usados nas convoluções é dado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
  * **n_downsample** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de operações de downsample do codificador.

<a id="codigo.segmentacao.modulos.modelo._decodificador"></a>

### codigo.segmentacao.modulos.modelo.\_decodificador(x, n_filtros, saidas_codificador)

Cria o decodificador do modelo (camadas de upsample).

Cria o decodificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*.

É necessário fornecer uma lista com todas as saídas do codificador. O bloco de upsample concatena
essas saídas com as dos blocos anteriores. O número de blocos de upsample é obtido pelo tamanho
dessa lista.

O número de filtros (canais) usados nas convoluções é dado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
  * **saida_codificador** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) – Lista com todas as saídas do codificador. O bloco de upsample concatena essas saídas com as dos
    blocos anteriores.

<a id="codigo.segmentacao.modulos.modelo.modelo_unet"></a>

### codigo.segmentacao.modulos.modelo.modelo_unet(formato_entrada, canais_saida=3, n_downsample=4)

Cria o modelo uNET.

O formato de entrada deve ser uma tupla do tipo (n_linhas, n_colunas, canais). *n_linhas* e *n_colunas* devem
ser múltiplos de *2^n_downsample*. Por exemplo, se *n_downsample=4*, devem ser múltiplos de 16, como (32, 64, 3).
Nesse caso, a imagem é um RGB. Se deseja usar um grayscale, esse número deve ser 1.

O número de downsample do modelo e, consequentemente, de upsameple é definido pelo parâmetro *n_downsample*.

* **Parâmetros:**
  * **formato_entrada** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – O formato de entrada do modelo.
  * **canais_saida** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de canais de saída do modelo.
  * **n_downsample** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de operações de downsample do codificador.
