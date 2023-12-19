<a id="codigo-segmentacao-modulos-modelo"></a>

# codigo.segmentacao.modulos.modelo

* **code:**
  [modelo.py](../../../../codigo/segmentacao/modulos/modelo.py)

<a id="module-codigo.segmentacao.modulos.modelo"></a>

Modelo usado para segmentação de imagens.

Modelo: U-NET

Baseado no código disponível em: [https://pyimagesearch.com/2022/02/21/u-net-image-segmentation-in-keras/](https://pyimagesearch.com/2022/02/21/u-net-image-segmentation-in-keras/)

Para criar o modelo de segmentação, use a função [`modelo_unet()`](#codigo.segmentacao.modulos.modelo.modelo_unet). É recomendado usar a
‘sparse_categorical_crossentropy’ como função de perda. Se usado essa função de perda,
não use apenas 1 canal de saída, use 2 pelo menos. Além disso, essa função de perda necessita
que a máscara de treinamento seja do tipo uint8.

<a id="codigo.segmentacao.modulos.modelo._bloco_conv2D"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_conv2D(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Aplica um bloco de convoluções ao modelo.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
O fluxo final (após passar pelo bloco) será retornado pela função.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
* **Retorna:**
  Tensor com fluxo atual do modelo (após passar pelo bloco).
* **Tipo de retorno:**
  tf.Tensor

<a id="codigo.segmentacao.modulos.modelo._bloco_downsample"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_downsample(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Bloco que reduz as dimensões (n_linhas, n_colunas) dos dados, enquanto extrai informações deles.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
O fluxo final (após passar pelo bloco) será retornado pela função.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
* **Retorna:**
  Tensor com fluxo atual do modelo (após passar pelo bloco).
* **Tipo de retorno:**
  tf.Tensor

<a id="codigo.segmentacao.modulos.modelo._bloco_padrao"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_padrao(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int))

Aplica um bloco padrão de convoluções ao modelo.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
O fluxo final (após passar pelo bloco) será retornado pela função.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

Esse bloco será colocado entre as operações de downsample e upsample.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
* **Retorna:**
  Tensor com fluxo atual do modelo (após passar pelo bloco).
* **Tipo de retorno:**
  tf.Tensor

<a id="codigo.segmentacao.modulos.modelo._bloco_saida"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_saida(x: Tensor, mascaras: [int](https://docs.python.org/3/library/functions.html#int))

Cria a camada de saída do modelo.

Cria a camada de saída do modelo a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
A saída do modelo (com as máscaras) será retornada por essa função.

O número de máscaras é dado por *mascaras*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **mascaras** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de máscaras da saída do modelo.
* **Retorna:**
  Tensor com fluxo atual do modelo e máscaras.
* **Tipo de retorno:**
  tf.Tensor

<a id="codigo.segmentacao.modulos.modelo._bloco_treinamento"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_treinamento(x: Tensor)

Aplica um bloco ajuste ao treinamento ao fluxo atual.

Aplica Dropout no tensor com o fluxo atual do modelo, parâmetro *x*.
Isso melhora o treinamento, evitando overfitting.

O fluxo final (após passar pelo bloco) será retornado pela função.

* **Parâmetros:**
  **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
* **Retorna:**
  Tensor com fluxo atual do modelo (após passar pelo bloco).
* **Tipo de retorno:**
  tf.Tensor

<a id="codigo.segmentacao.modulos.modelo._bloco_upsample"></a>

### codigo.segmentacao.modulos.modelo.\_bloco_upsample(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int), saida_codificador: Tensor)

Bloco que aumenta as dimensões (n_linhas, n_colunas) dos dados, para formar as máscaras.

Cria a camada a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
Sua resolução será aumentada. Após isso, ele será combinado com a *saida_codificador* e, o resultado
será retornado pela função.

O número de filtros usados nas convoluções é determinado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
  * **saida_codificador** (*tf.Tensor*) – Saida do codificador que será concatenada como fluxo atual do modelo.

<a id="codigo.segmentacao.modulos.modelo._codificador"></a>

### codigo.segmentacao.modulos.modelo.\_codificador(x: Tensor, n_filtros: [int](https://docs.python.org/3/library/functions.html#int), n_downsample: [int](https://docs.python.org/3/library/functions.html#int))

Cria o codificador do modelo (camadas de downsample).

Cria o codificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*.
O fluxo final (após passar pelo bloco) será retornado pela função. Assim como uma
lista com todas as saídas do codificador começando pela de maior resolução (equivalente ao fluxo de entrada).

O número de operações de downsample do codificador é definido por *n_downsample*. O número de filtros
(canais) usados nas convoluções é dado por *n_filtros*.

* **Parâmetros:**
  * **x** (*tf.Tensor*) – Tensor com o fluxo atual do modelo.
  * **n_filtros** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de filtros usados nas convoluções do bloco padrão.
  * **n_downsample** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de operações de downsample do codificador.
* **Retorna:**
  * *tf.Tensor* – Tensor com fluxo atual do modelo (depois de passar pelo bloco).
  * *list* – Lista com todas as saídas do codificador (começando pela de maior resolução).

<a id="codigo.segmentacao.modulos.modelo._decodificador"></a>

### codigo.segmentacao.modulos.modelo.\_decodificador(x: Tensor, n_filtros, saidas_codificador)

Cria o decodificador do modelo (camadas de upsample).

Cria o decodificador a partir do tensor com o fluxo atual do modelo, parâmetro *x*, e das saídas do codificador.

É necessário fornecer uma lista com todas as saídas do codificador. O bloco de upsample combina
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

O número de downsample do modelo e, consequentemente, de upsameple é definido pelo parâmetro *n_downsample*.

O formato de entrada deve ser uma tupla do tipo (n_linhas, n_colunas, canais). *n_linhas* e *n_colunas* devem
ser múltiplos de *2^n_downsample*. Por exemplo, se *n_downsample=4*, devem ser múltiplos de 16, como (32, 64, 3).
Nesse caso, a imagem é um RGB. Se deseja usar um grayscale, essa tupla deve ser (32, 32, 1).

O número de saída é definido pelo parâmetro *canais_saida*. Ele determina o número de máscaras de saída do modelo.

* **Parâmetros:**
  * **formato_entrada** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – O formato de entrada do modelo.
  * **canais_saida** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de canais de saída do modelo (número de máscaras).
  * **n_downsample** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número de operações de downsample do codificador.
* **Retorna:**
  O modelo criado.
* **Tipo de retorno:**
  tf.keras.Model
