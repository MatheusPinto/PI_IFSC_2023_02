<a id="codigo-identificacao-modulos-identificador"></a>

# codigo.identificacao.modulos.identificador

* **code:**
  [identificador.py](../../../../codigo/identificacao/modulos/identificador.py)

<a id="module-codigo.identificacao.modulos.identificador"></a>

Identificador de lixo.

Implementação da identificação de lixo usando a ferramenta de Haar Cascade do OpenCV. Para tal
utilize a classe [`Identificador`](#codigo.identificacao.modulos.identificador.Identificador).

<a id="codigo.identificacao.modulos.identificador.Identificador"></a>

### *class* codigo.identificacao.modulos.identificador.Identificador(path_modelo: [str](https://docs.python.org/3/library/stdtypes.html#str), formato_imagem: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe para identificação de lixo.

Deve-se fornecer o path do arquivo contendo o modelo de Haar Cascade usado para identificar o
lixo. Ela localizará o lixo em um frame fornecido e retornará a posição do lixo mais próximo.
Veja o método `identifica_lixo_proximo()` para mais informações.

Se deseja identificar todos os lixos do frame, utilize o método [`identifica_lixos()`](#codigo.identificacao.modulos.identificador.Identificador.identifica_lixos).

<a id="codigo.identificacao.modulos.identificador.Identificador.__init__"></a>

#### \_\_init_\_(path_modelo: [str](https://docs.python.org/3/library/stdtypes.html#str), formato_imagem: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Construtor do modelo de identificação.

Cria um identificador de lixo. Deve ser fornecido o path do arquivo contendo o modelo de Haar Cascade pelo parâmetro
*path_modelo*.

É possível configurar o formato da imagem (n_colunas, n_linas) que a imagem deve ter. Se recebido um frame
com tamanho diferente, ele será redimensionado para o correto.

* **Parâmetros:**
  * **path_modelo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Caminho para o arquivo contendo o modelo usado para identificar o lixo.
  * **formato_imagem** (*(*[*int*](https://docs.python.org/3/library/functions.html#int)*,* [*int*](https://docs.python.org/3/library/functions.html#int)*)**,* *default=None*) – Formato da imagem (n_colunas, n_linhas) que a imagem deve ter. Se recebido um frame com tamanho
    diferente, ele será redimensionado para o correto.

<a id="codigo.identificacao.modulos.identificador.Identificador._calcula_posicao_lixo_mais_proximo"></a>

#### \_calcula_posicao_lixo_mais_proximo()

Retorna a posição do lixo mais próximo.

Retorna uma tupla com a coordenada do lixo mais próximo. A estrutura da tupla é
(posicao_x, posica_y, largura, altura, centro_x, centro_y).

O lixo mais próximo é dado pela distância em relação à borda inferior da imagem. Quanto menor,
mais próximo do Wall-e ele está.

A posição retornada é em relação à imagem já redimensionada. Para mais informações sobre o
redimensionamento dos frames, veja o método [`define_frame()`](#codigo.identificacao.modulos.identificador.Identificador.define_frame) e [`__init__()`](#codigo.identificacao.modulos.identificador.Identificador.__init__).

* **Retorna:**
  Tupla contendo as coordenadas do lixo mais próximo (x, y, l, a, cx, cy).
* **Tipo de retorno:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

<a id="codigo.identificacao.modulos.identificador.Identificador._calcula_posicoes_lixos"></a>

#### \_calcula_posicoes_lixos()

Retorna as coordenadas dos lixos identificados.

Retorna uma lista com as coordenadas dos lixos. Cada elemento da lista corresponde á coordenada de um lixo.
Além disso, as coordenadas possuem o formato (posicao_x, posica_y, largura, altura).

As posições retornadas são em relação à imagem pós-redimensionamento. Para mais informações sobre o
redimensionamento dos frames, veja o método [`define_frame()`](#codigo.identificacao.modulos.identificador.Identificador.define_frame) e [`__init__()`](#codigo.identificacao.modulos.identificador.Identificador.__init__).

* **Retorna:**
  Lista de tuplas contendo as coordenadas do lixo (x, y, l, a).
* **Tipo de retorno:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

<a id="codigo.identificacao.modulos.identificador.Identificador._desenha_debug_lixo_mais_proximo"></a>

#### \_desenha_debug_lixo_mais_proximo()

Desenha o debug da identificação do lixo mais próximo.

Desenha um círculo rosa sobre o lixo mais próximo identificado. A definição do lixo mais próximo
ocorre como descrito no método [`_calcula_posicao_lixo_mais_proximo()`](#codigo.identificacao.modulos.identificador.Identificador._calcula_posicao_lixo_mais_proximo).

* **Retorna:**
  Imagem de debug.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.identificacao.modulos.identificador.Identificador._desenha_debug_lixos"></a>

#### \_desenha_debug_lixos()

Desenha o debug da identificação de todos os lixos.

Desenha um retângulo azul claro sobre os lixos identificados.

* **Retorna:**
  Imagem de debug.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

<a id="codigo.identificacao.modulos.identificador.Identificador._pos_frame2debug"></a>

#### \_pos_frame2debug(pos: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple))

Transforma as coordenadas do frame usado na identificação para as coordenadas da imagem de debug.

A conversão ocorre das coordenadas após o redimensionamento do frame. Veja o método [`define_frame()`](#codigo.identificacao.modulos.identificador.Identificador.define_frame)
para saber mais sobre isso.

Essas coordenadas são convertidas para equivalentes da imagem de debug. Suponha que o formato do
frame definido ao instanciar a classe é de 320x240 e a imagem de debug possui formato 640x480. Converter
o ponto (10, 15) resultará em (20, 30).

* **Parâmetros:**
  **pos** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Coordenadas do frame redimensionado (x, y).
* **Retorna:**
  Coordenadas na imagem de debug (x, y).
* **Tipo de retorno:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

<a id="codigo.identificacao.modulos.identificador.Identificador._pos_frame2original"></a>

#### \_pos_frame2original(pos: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple))

Transforma as coordenadas do frame usado na identificação para as coordenadas da imagem original.

Converte as coordenadas em relação ao frame pós-redimensionado (usado na identificação) para a posição
respectiva da imagem original.

Essas coordenadas são convertidas para equivalentes da imagem original. Suponha que o formato do
frame definido ao instanciar a classe é de 320x240 e a imagem original possui formato 640x480. Converter
o ponto (10, 15) resultará em (20, 30).

* **Parâmetros:**
  **pos** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Coordenadas do frame redimensionado (x, y).
* **Retorna:**
  Coordenadas na imagem original (x, y).
* **Tipo de retorno:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)

<a id="codigo.identificacao.modulos.identificador.Identificador._reinicia_iteracao"></a>

#### \_reinicia_iteracao()

Reinicia os atributos da identificação.

O identificador é reiniciado para uma nova iteração. Alguns dados anteriores são apagados.

Esse método também pode ser usado para iniciar os atributos referentes a uma iteração.

Uma iteração corresponde a uma nova identificação de objetos em um novo frame.

<a id="codigo.identificacao.modulos.identificador.Identificador.define_frame"></a>

#### define_frame(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), imagem_debug: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Define o frame usado na identificação.

É possível definir uma imagem para ser a inicial de debug. Se receber um frame com tamanho diferente,
ele será redimensionado para o definido ao instanciar a classe. Veja o método [`__init__()`](#codigo.identificacao.modulos.identificador.Identificador.__init__) para
informações de como fazer isso. O frame apenas é usado na identificação do lixo após ser redimensionado
para o formato correto.

* **Parâmetros:**
  * **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame onde serão identificados os lixos.
  * **imagem_debug** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Imagem de debug.

<a id="codigo.identificacao.modulos.identificador.Identificador.identifica_lixo_mais_proximo"></a>

#### identifica_lixo_mais_proximo(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), debug=False)

Identifica o lixo mais próximo do frame.

O lixo mais próximo é o que está mais abaixo da imagem. Retona sua posição na imagem por
meio de uma tupla do seguinte tipo: (x, y, l, a, cx, cy). ‘x’ e ‘y’ são as posições do ponto superior
esquerdo do objeto. ‘l’ e ‘a’ são largura e altura. ‘cx’ e ‘cy’ são as posições do centro do objeto.

Todos esses valores são do objeto na imagem original (antes de redimensionar).

Se *debug=True*, desenha um identificador do lixo mais próximo na imagem de debug. Semelhante às identificações do
método [`identifica_lixos()`](#codigo.identificacao.modulos.identificador.Identificador.identifica_lixos), mas com um círculo rosa sobre a detecção mais próxima. Veja o método
[`_desenha_debug_lixo_mais_proximo()`](#codigo.identificacao.modulos.identificador.Identificador._desenha_debug_lixo_mais_proximo) para mais informações.

* **Parâmetros:**
  * **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame a ser identificado.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se True, identifica lixo mais próximo na imagem de debug por um círculo rosa.
* **Retorna:**
  Coordenadas do lixo mais próximo (x, y, l, a, cx, cy).
* **Tipo de retorno:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

<a id="codigo.identificacao.modulos.identificador.Identificador.identifica_lixos"></a>

#### identifica_lixos(frame: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), debug=False)

Identifica todos os lixos do frame.

Se *debug=True*, desenha os lixos identificados (um retângulo azul-claro ao redor deles) na imagem de debug.
: Veja o método [`_desenha_debug_lixos()`](#codigo.identificacao.modulos.identificador.Identificador._desenha_debug_lixos) para mais informações.

* **Parâmetros:**
  * **frame** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Frame a ser identificado.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se True, identifica os lixos na imagem de debug por um quadrado verde
* **Retorna:**
  Lista de tuplas contendo as coordenadas do lixo (x, y, l, a).
* **Tipo de retorno:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)

<a id="codigo.identificacao.modulos.identificador.Identificador.retorna_imagem_debug"></a>

#### retorna_imagem_debug()

Retorna a imagem de debug.

A imagem de debug pode possuir os identificadores de todos os lixos, assim como do
lixo mais próximo. Ela é pode ser definida pelo método [`define_frame()`](#codigo.identificacao.modulos.identificador.Identificador.define_frame).

* **Retorna:**
  Imagem de debug.
* **Tipo de retorno:**
  [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)
