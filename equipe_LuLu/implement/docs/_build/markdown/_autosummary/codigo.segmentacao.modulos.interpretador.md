<a id="module-codigo.segmentacao.modulos.interpretador"></a>

<a id="codigo-segmentacao-modulos-interpretador"></a>

# codigo.segmentacao.modulos.interpretador

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
>>> mascara = segmentador.retorna_imagem_segmentada(None)
>>> imagem_com_segmentacao = segmentador.retorna_imagem_segmentada(None)
```

Essa abordagem é mais eficiente, visto que utiliza o resultado do último processamento ao invés de
re-segmentar a imagem.

### Notas

A imagem de entrada deve estar no formato RGB. Atenção porque o OpenCV usa o formato BGR. Para converter
entre eles, use:

```pycon
>>> import cv2 as cv
>>> imagem = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
```

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.__init__"></a>

#### \_\_init_\_(arquivo_ftlite: [str](https://docs.python.org/3/library/stdtypes.html#str), n_threads=1)

Carrega o modelo de segmentação de imagem.

É necessário informar o arquivo do modelo convertido para o Tensorflow Lite, e o número de threads
que serão usadas para processar o modelo.

* **Parâmetros:**
  * **arquivo_ftlite** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – O arquivo do modelo de segmentação convertido para o Tensorflow Lite.
  * **n_threads** ([*int*](https://docs.python.org/3/library/functions.html#int)*,* *default 1*) – O número de threads que serão usadas para processar o modelo. O valor padrão é 1.

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

Retorna o formato de entrada do segmentador.

Ele é retornado como uma tupla. O formato da imagem utilizada no método ‘segmenta_imagem()’
deve ser igual ao retornado por essa função. Caso contrário, não funcionará.

* **Retorna:**
  O formato de entrada do segmentador.
* **Tipo de retorno:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.retorna_imagem_segmentada"></a>

#### retorna_imagem_segmentada(imagem)

Retorna a imagem com a segmentação.

A imagem é segmentada. O resultado da segmentação é unido a imagem por uma operação de blend.
O resultado é uma imagem com um filtro de segmentação.

A segmentação é feita pelo método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem).

O formato da imagem retornada é igual ao da entrada do modelo de segmentação.

* **Parâmetros:**
  **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser segmentada. Se for None, será usado o resultado da última segmentação.
* **Retorna:**
  A imagem com um filtro de segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.retorna_mascara"></a>

#### retorna_mascara(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Segmenta a imagem recebida e retorna a máscara de objeto colidível.

A segmentação é feita usando o método [`segmenta_imagem()`](#codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem). O resultado é a máscara
de objetos colidível que ele retorna.

* **Parâmetros:**
  **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser segmentada. Se for None, será retornado a máscara da última segmentação.
* **Retorna:**
  Máscara resultada da segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.segmentacao.modulos.interpretador.Segmentador.segmenta_imagem"></a>

#### segmenta_imagem(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Segmenta a imagem recebida.

Retorna o resultado da segmentação sem pós-processamento. Se a imagem for None, será
retornado o resultado da última segmentação.

* **Parâmetros:**
  **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)*,* *default None*) – A imagem a ser segmentada. Se for None, será retornado o resultado da última segmentação.
* **Retorna:**
  Imagem resultada do processo de segmentação.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)
