<a id="codigo-segmentacao-modulos-interpretador"></a>

# codigo.segmentacao.modulos.interpretador

* **code:**
  [interpretador.py](../../../../codigo/segmentacao/modulos/interpretador.py)

<a id="module-codigo.segmentacao.modulos.interpretador"></a>

Interpretadores de modelos do tensorflow lite.

Está disponível, neste módulo, um modelo de segmentador semântico de imagens
usado para obter a máscara de uma imagem: [`Segmentador`](#codigo.segmentacao.modulos.interpretador.Segmentador).

<a id="codigo.segmentacao.modulos.interpretador.Segmentador"></a>

### *class* codigo.segmentacao.modulos.interpretador.Segmentador(arquivo_ftlite: [str](https://docs.python.org/3/library/stdtypes.html#str), n_threads=1)

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Segmentador de imagens.

É necessário informar o arquivo do modelo (convertido para tflite) ao inferir o objeto.

Para segmentar a imagem, use o método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem). Ele retorna o resultado de
saída do modelo. Se deseja apenas a máscara de objetos colidíveis, use o método [`retorna_mascara()`](#codigo.segmentacao.modulos.interpretador.Segmentador.retorna_mascara).

Para fins de debug, há um método que retorna a imagem unida ao resultado de processamento por meio
de uma operação de blend. O método é [`retorna_imagem_segmentada()`](#codigo.segmentacao.modulos.interpretador.Segmentador.retorna_imagem_segmentada).

Para carregar o segmentador, é necessário o modelo de segmentação do Tensorflow Lite, conforme instruído
pelo método [`__init__()`](#codigo.segmentacao.modulos.interpretador.Segmentador.__init__).

```pycon
>>> # Carrega o segmentador
>>> segmentador = Segmentador(MODELO_TFLITE_PATH, N_THREADS)
```

Se a imagem fornecida ao segmentador for None, será retornado o resultado da última segmentação.
Portanto, é possível fazer o seguinte:

```pycon
>>> # Obtém o resultado da segmentação, a máscara, e a combinação do resultado com a imagem original
>>> imagem_segmentadaa = segmentador.segmenta_imagem(imagem)
>>> mascara = segmentador.retorna_mascara(None)
>>> imagem_com_segmentacao = segmentador.retorna_imagem_segmentada(None)
```

Essa abordagem é mais eficiente, visto que utiliza o resultado do último processamento ao invés de
re-segmentar a imagem.

### Notas

A imagem de entrada deve estar no formato RGB. Atenção porque o OpenCV usa o formato BGR. Para converter
entre eles, alguns métodos possuem o parâmetro BGR. Por exemplo, o método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem). Se ele
for chamado da seguinte forma, a imagem será convertida de BGR para RGB antes de ser segmentada.

```pycon
>>> imagem_segmentadaa = segmentador.segmenta_imagem(imagem, BGR=True)
```

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.__init__"></a>

#### \_\_init_\_(arquivo_ftlite: [str](https://docs.python.org/3/library/stdtypes.html#str), n_threads=1)

Carrega o modelo de segmentação de imagem.

É necessário informar o arquivo do modelo convertido para o Tensorflow Lite, e o número de threads
que serão usadas para processar o modelo.

* **Parâmetros:**
  * **arquivo_ftlite** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – O arquivo do modelo de segmentação convertido para o Tensorflow Lite.
  * **n_threads** ([*int*](https://docs.python.org/3/library/functions.html#int)*,* *default 1*) – O número de threads que serão usadas para processar o modelo. O valor padrão é 1.

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._computa_imagem_segmentada"></a>

#### \_computa_imagem_segmentada()

Computa a imagem com a segmentação adicionada a ela.

Semelhante ao método [`_computa_segmentacao()`](#codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao), mas retorna a imagem original unida ao
resultado do modelo de segmentação por meio de uma operação de blend.

* **Retorna:**
  A imagem unida ao resultado do modelo de segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._computa_imagem_segmentada_redimensionada"></a>

#### \_computa_imagem_segmentada_redimensionada()

Computa a imagem com a segmentação adicionada a ela (redimensionada).

Semelhante ao método [`_computa_segmentacao_redimensionada()`](#codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao_redimensionada), mas retorna a imagem
original unida ao resultado do modelo de segmentação por meio de uma operação de blend.

* **Retorna:**
  A imagem unida ao resultado do modelo de segmentação (redimensionada para o formato
  da imagem original).
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._computa_mascara"></a>

#### \_computa_mascara()

Computa a máscara de objetos colidíveis.

Semelhante ao método [`_computa_segmentacao()`](#codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao), mas retorna apenas máscara de objetos colidíveis.

* **Retorna:**
  A máscara de objetos colidíveis.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._computa_mascara_redimensionada"></a>

#### \_computa_mascara_redimensionada()

Computa a máscara de objetos colidíveis e redimensiona ela para o tamanho do frame original.

Semelhante ao método [`_computa_segmentacao_redimensionada()`](#codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao_redimensionada), mas retorna apenas máscara de
objetos colidíveis.

* **Retorna:**
  A máscara de objetos colidíveis (redimensionada para o formato do frame original).
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao"></a>

#### \_computa_segmentacao()

Computa a segmentação da imagem recebida.

Retorna o resultado do modelo de segmentação sem pós-processamento. Se a imagem for None, será
retornado o resultado da última segmentação.

* **Retorna:**
  Resultado do modelo de segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao_redimensionada"></a>

#### \_computa_segmentacao_redimensionada()

Computa a segmentação da imagem e redimensiona para o tamanho do frame original.

Semelhante ao método [`_computa_segmentacao()`](#codigo.segmentacao.modulos.interpretador.Segmentador._computa_segmentacao), mas o resultado é redimensionado
para o tamanho do frame original antes de ser retornado.

* **Retorna:**
  Resultado do modelo de segmentação (redimensionada para o formato original).
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador._reinicia_iteracao"></a>

#### \_reinicia_iteracao()

Reinicia a iteração do segmentador.

O segmentador é reiniciado para uma nova segmentação. Os dados anteriores são apagados.

Esse método também pode ser usado para iniciar os atributos referentes a uma iteração.

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.define_imagem"></a>

#### define_imagem(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), BGR=False)

Define a imagem a ser segmentada.

A imagem deve ser um RGB com o formato (linhas, colunas, canais). Se a imagem for fornecida no
formato BGR, use o parâmetro *BGR* iagual a True. O segmentador se encarrega de converter para RGB.

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser segmentada.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.redimensiona_para_entrada"></a>

#### redimensiona_para_entrada(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray))

Redimensiona a imagem para o formato de entrada do segmentador.

A imagem apenas é redimensionada se não estiver no formato de entrada do modelo.
A imagem de entrada deve estar no formato (linhas, colunas, canais).

* **Parâmetros:**
  **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser redimensionada.
* **Retorna:**
  A imagem redimensionada para o formato de entrada do segmentador.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.retorna_formato_entrada"></a>

#### retorna_formato_entrada()

Retorna o formato de entrada do modelo de segmentadoção.

As imagens serão redimensionadas para o formato de entrada do segmentador antes de serem fornecidas a ele.
Esse método fornece esse formato de entrada.

O formato retornado é do tipo: (linhas, colunas, canais).

* **Retorna:**
  O formato de entrada do segmentador.
* **Tipo de retorno:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.retorna_imagem_segmentada"></a>

#### retorna_imagem_segmentada(imagem, BGR=False, redimensiona=False)

Retorna a imagem com a segmentação.

A imagem é segmentada. O resultado da segmentação é unido a imagem por uma operação de blend.
O resultado é uma imagem com um filtro de segmentação. A imagem é retornada no formato RGB.

Os parâmetros *BGR* e *redimensiona* são equivalentes aos do método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem).

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser segmentada. Se for None, será usado o resultado da última segmentação.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.
  * **redimensiona** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se True, a imagem com a segmentação é redimensionado para o tamanho do frame recebido originalmente
    antes de ser retornado. Caso False, a imagem com a segmentação será retornada com o formato da
    saída do modelo de segmentação.
* **Retorna:**
  A imagem com um filtro de segmentação (formato RGB).
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.retorna_mascara"></a>

#### retorna_mascara(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) | [None](https://docs.python.org/3/library/constants.html#None) = None, BGR=False, redimensiona=False)

Segmenta a imagem recebida e retorna a máscara de objeto colidível.

Semelhante ao método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem), mas retorna a máscara de objetos colidíveis.

Os parâmetros *BGR* e *redimensiona* são equivalentes aos do método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem).

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser segmentada. Se for None, será retornado a máscara da última segmentação.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.
  * **redimensiona** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se True, o resultado da segmentação é redimensionado para o tamanho do frame original
    antes de ser retornado. Caso False, o resultado da do modelo de segmentação não será redimensionado.
* **Retorna:**
  Máscara resultada da segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem"></a>

#### segmenta_imagem(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) | [None](https://docs.python.org/3/library/constants.html#None) = None, BGR=False, redimensiona=False)

Segmenta a imagem recebida.

Retorna o resultado do modelo de segmentação sem pós-processamento. Se a imagem for None, será
retornado o resultado da última segmentação.

Se *redimensiona* for True, o resultado da segmentação é redimensionado para o tamanho do frame original
antes de ser retornado. Caso False, o resultado do modelo de segmentação não será redimensionado.

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)*,* *default None*) – A imagem a ser segmentada. Se for None, será retornado o resultado da última segmentação.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem for fornecida no formato BGR. Caso False, considera que foi fornecido no RGB.
  * **redimensiona** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se True, o resultado da segmentação é redimensionado para o tamanho do frame original
    antes de ser retornado. Caso False, o resultado da do modelo de segmentação não será redimensionado.
* **Retorna:**
  Resultado do modelo de segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)
