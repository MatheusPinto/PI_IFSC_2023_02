<a id="codigo-interface-modulos-video"></a>

# codigo.interface.modulos.video

* **code:**
  [video.py](../../../../codigo/interface/modulos/video.py)

<a id="module-codigo.interface.modulos.video"></a>

Módulo de captura de vídeo.

Implementa a captura de frames da webcam. Além disso, é possível codificar os frames em um array de bytes para serem
enviados pela rede; e decodificar esses próprios bytes de volta para o frame original.

Para capturar os frames da câmera, utilize a classe [`Camera`](#codigo.interface.modulos.video.Camera). Essa classe ajusta seu funcionamento para
reconhecer a Webcam automaticamente na Raspberry Pi.

Para codificar e decodificar o frame, utilize as funções [`codifica_frame()`](#codigo.interface.modulos.video.codifica_frame) e [`decodifica_frame()`](#codigo.interface.modulos.video.decodifica_frame). É possível retornar
o frame já codificado pela classe [`Camera`](#codigo.interface.modulos.video.Camera).

<a id="codigo.interface.modulos.video.Camera"></a>

### *class* codigo.interface.modulos.video.Camera(formato_frame: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), erro_ao_falhar: [bool](https://docs.python.org/3/library/functions.html#bool) = False, path_arquivo_log: [str](https://docs.python.org/3/library/stdtypes.html#str) = '')

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe para capturar frames de uma webcam.

Utilize o método [`retorna_frame()`](#codigo.interface.modulos.video.Camera.retorna_frame) para capturar o frame atual da webcam.

<a id="codigo.interface.modulos.video.Camera.__init__"></a>

#### \_\_init_\_(formato_frame: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), erro_ao_falhar: [bool](https://docs.python.org/3/library/functions.html#bool) = False, path_arquivo_log: [str](https://docs.python.org/3/library/stdtypes.html#str) = '')

Inicialização do capturador de frames da cãmera.

É necessário informar o formado do frame capturado da webcam por meio do parâmetro *formato_frame*. Ele
deve ser uma tupla do tipo (n_colunas, n_linhas). Ou seja, informe primeiro a dimensão horizontal (eixo x)
e depois a dimensão vertical (eixo y).

Se *erro_ao_falhar* for True, causa uma exceção se ocorreu erro no reconhecimento ou captura da câmera.

É possível informar um arquivo de log para registrar as mensagens de log. Para isso, informe o caminho
para ele por meio do parâmetro *path_arquivo_log*.

* **Parâmetros:**
  * **formato_frame** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Tamanho e formato do frame. Por exemplo: (640, 480)
  * **erro_ao_falhar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se deve ou não causar uma exceção caso o reconhecimento ou captura da cãmera falhe.
  * **path_arquivo_log** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Caminho para o arquivo de log.

<a id="codigo.interface.modulos.video.Camera.retorna_frame"></a>

#### retorna_frame(codificar: [bool](https://docs.python.org/3/library/functions.html#bool) = False)

Retorna um frame capturado da cãmera.

Se o parâmetro *codificar* for True, será retornado o frame codificado (bytes). A codificação é feita pela função
[`codifica_frame()`](#codigo.interface.modulos.video.codifica_frame). Caso contrário, será retornado o frame em forma de array numpy (uint8).

Se não foi configurado para causar erro ao falhar, mas ocorreu um erro na leitura do frame, será retornado
um frame completamente preto com as dimensões especificadas ao instanciar o objeto.

* **Parâmetros:**
  **codificar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se o frame deve ser codificado ou não.
* **Retorna:**
  A imagem capturada da câmera. Se *codificar* for False, a imagem será um array do numpy do tipo uint8.
  Formato BGR do OpenCV. Caso *codificar* seja True, essa imagem será convertida em um array de bytes antes
  de ser retornada.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) or [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

<a id="codigo.interface.modulos.video.codifica_frame"></a>

### codigo.interface.modulos.video.codifica_frame(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray))

Codifica uma frame de imagem para bytes.

O frame deve ser um array do numpy do tipo uint8, no formato BGR do OpenCV. Ele será convertido para
JPG e formatado como uma lista de bytes. Assim, pode ser enviado pela rede a um recebedor do frame.

Para decodificar essa a imagem codificada, use a função [`decodifica_frame()`](#codigo.interface.modulos.video.decodifica_frame).

* **Parâmetros:**
  **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame a ser codificado.
* **Retorna:**
  Bytes contendo o frame codificado (formato JPG).
* **Tipo de retorno:**
  [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)

<a id="codigo.interface.modulos.video.decodifica_frame"></a>

### codigo.interface.modulos.video.decodifica_frame(frame: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))

Decodifica uma frame de bytes para a imagem.

O frame deve ser uma lista de bytes. Ele será convertido para um array do numpy do tipo uint8 no formato
BGR do OpenCV. Ou seja, a imagem codificada pela função [`codifica_frame()`](#codigo.interface.modulos.video.codifica_frame) pode ser decodificada
e retornada ao seu formato original por meio dessa função.

Se ocorrer um erro na decodificação, retorna None.

* **Parâmetros:**
  **frame** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – Frame a ser decodificado.
* **Retorna:**
  Frame decodificado (array do numpy do tipo uint8). Se ocorreu um erro na decodificação,
  retorna None.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) or None
