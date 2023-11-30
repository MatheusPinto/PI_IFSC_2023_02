<a id="module-codigo.identificacao.modulos.identificador"></a>

<a id="codigo-identificacao-modulos-identificador"></a>

# codigo.identificacao.modulos.identificador

Identificador de lixo.

Implementação da identificação de lixo usando a ferramenta de Haar Cascade do OpenCV. Para tal
utilize a classe [`Identificador`](#codigo.identificacao.modulos.identificador.Identificador).

<a id="codigo.identificacao.modulos.identificador.Identificador"></a>

### *class* codigo.identificacao.modulos.identificador.Identificador(path_modelo: [str](https://docs.python.org/3/library/stdtypes.html#str), formato_imagem: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe para identificação de lixo.

Deve-se fornecer o path do arquivo contendo o modelo de Haar Cascade usado para identificar o
lixo. Ela localizará o lixo em um frame fornecido e retornará a posição do lixo mais próximo.
Veja o método [`identifica_lixo_proximo()`](#codigo.identificacao.modulos.identificador.Identificador.identifica_lixo_proximo) para mais informações.

Se deseja identificar todos os lixos do frame, utilize o método [`identifica_lixos()`](#codigo.identificacao.modulos.identificador.Identificador.identifica_lixos).

<a id="codigo.identificacao.modulos.identificador.Identificador.__init__"></a>

#### \_\_init_\_(path_modelo: [str](https://docs.python.org/3/library/stdtypes.html#str), formato_imagem: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Construtor do modelo de identificação.

Cria um identificador de lixo. Deve ser fornecido o path do arquivo contendo o modelo de Haar Cascade.

É possível configurar o formato da imagem (n_linhas, n_colunas) que a imagem deve ter. Se recebido um frame
com tamanho diferente, ele será redimensionado para o correto.

* **Parâmetros:**
  * **path_modelo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Caminho para o arquivo contendo o modelo usado para identificar o lixo.
  * **formato_imagem** (*(*[*int*](https://docs.python.org/3/library/functions.html#int)*,* [*int*](https://docs.python.org/3/library/functions.html#int)*)**,* *default=None*) – Formato da imagem (n_linhas, n_colunas) que a imagem deve ter. Se recebido um frame com tamanho
    diferente, ele será redimensionado para o correto.

<a id="codigo.identificacao.modulos.identificador.Identificador.define_frame"></a>

#### define_frame(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), imagem_debug: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Define o frame usado na identificação.

É possível definir uma imagem para ser a inicial de debug.

* **Parâmetros:**
  * **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame onde serão identificado o lixo.
  * **imagem_debug** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Imagem de debug.

<a id="codigo.identificacao.modulos.identificador.Identificador.identifica_lixo_proximo"></a>

#### identifica_lixo_proximo(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), debug=False)

Identifica o lixo mais próximo do frame.

O lixo mais próximo é o que está mais abaixo da imagem.

Se *debug=True*, retorna as classificações e a imagem com o debug. Essa imagem é igual a de
debug retornado pelo método [`identifica_lixos()`](#codigo.identificacao.modulos.identificador.Identificador.identifica_lixos), mas com um círculo vermelho sobre a
detecção mais próxima.

* **Parâmetros:**
  * **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame a ser identificado.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se True, retorna uma imagem com o lixo mais próximo identificado por um círculo vermelho.
* **Retorna:**
  Lista de tuplas contendo as coordenadas do lixo mais próximo (x, y). Se *debug=True*, essa
  lista estará em uma tupla junto da imagem de debug.
* **Tipo de retorno:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) or ([tuple](https://docs.python.org/3/library/stdtypes.html#tuple), [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray))

<a id="codigo.identificacao.modulos.identificador.Identificador.identifica_lixos"></a>

#### identifica_lixos(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), debug=False)

Identifica todos os lixos do frame.

Se *debug=True*, retorna uma imagem com os lixos identificados (um quadrado verde ao redor deles).

* **Parâmetros:**
  * **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame a ser identificado.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se True, retorna uma imagem com os lixos identificados por um quadrado verde ao redor.
* **Retorna:**
  Lista de tuplas contendo as coordenadas do lixo (x, y, l, a). Se *debug=True*, essa lista estará em
  uma tupla junto da imagem de debug.
* **Tipo de retorno:**
  [list](https://docs.python.org/3/library/stdtypes.html#list) or ([tuple](https://docs.python.org/3/library/stdtypes.html#tuple), [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray))
