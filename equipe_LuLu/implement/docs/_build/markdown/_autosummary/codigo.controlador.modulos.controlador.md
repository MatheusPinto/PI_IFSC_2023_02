<a id="module-codigo.controlador.modulos.controlador"></a>

<a id="codigo-controlador-modulos-controlador"></a>

# codigo.controlador.modulos.controlador

Controlador do direcionamento do Wall-e.

Define a classe [`Controlador`](#codigo.controlador.modulos.controlador.Controlador), responsável por definir a velocidade linear e angular no Wall-e no modo autônomo.

<a id="codigo.controlador.modulos.controlador.Controlador"></a>

### *class* codigo.controlador.modulos.controlador.Controlador(formato_mapa: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) = (60, 60), posicoes_esquerda: [list](https://docs.python.org/3/library/stdtypes.html#list) | [None](https://docs.python.org/3/library/constants.html#None) = None, blocos_tamanho: [int](https://docs.python.org/3/library/functions.html#int) = 3)

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Controlador do Wall-e no modo autônomo.

Ao instanciar um objeto dessa classe, deve ser fornecido os do mapa onde será marcado as colisões e
seus tamanhos. Veja [`__init__()`](#codigo.controlador.modulos.controlador.Controlador.__init__) para mais informações.

Para obter a direção de movimento do Wall-e, use o método [`calcula_direcao()`](#codigo.controlador.modulos.controlador.Controlador.calcula_direcao). Para verificar
onde está ocorrendo a colisão, use o método [`mostra_colisoes()`](#codigo.controlador.modulos.controlador.Controlador.mostra_colisoes).

<a id="codigo.controlador.modulos.controlador.Controlador.__init__"></a>

#### \_\_init_\_(formato_mapa: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) = (60, 60), posicoes_esquerda: [list](https://docs.python.org/3/library/stdtypes.html#list) | [None](https://docs.python.org/3/library/constants.html#None) = None, blocos_tamanho: [int](https://docs.python.org/3/library/functions.html#int) = 3)

Inicialização do controlador.

Cria os atributos da classe. Configura o traçador de caminho e a checagem de colisão. É necessário
informar o formato dos mapas usados pelo controlador. Ao receber um mapa, ele será automaticamente
redimensionado para esse formato contanto que seja bidimensional. O formato do mapa é dado pelo
parâmetro *formato_mapa* e deve ser uma tupla do tipo (n_linhas, n_colunas).

As posições a serem testadas (checagem de colisão) também devem ser informadas na instanciação do objeto.
Eles são informadas em tuplas do tipo (y, x). O parâmetro *posicoes_esquerda* deve ser uma lista de tuplas
contendo as posições dos blocos que serão checados à esquerda do mapa. São posições relativas ao ponto
inicial do mapa. Elas serão espelhadas para obter as posições da direita.

As posições do mapa são checadas em blocos. O tamanho de cada bloco é definido pelo parâmetro *blocos_tamanho*.

* **Parâmetros:**
  * **formato_mapa** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Formato do mapa usado pelo controlador.
  * **posicoes_esquerda** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) – Lista de tuplas contendo as posições dos blocos à esquerda do mapa que serão checadas.
  * **blocos_tamanho** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Tamanho de cada bloco onde será checado a colisão no mapa.

<a id="codigo.controlador.modulos.controlador.Controlador._atualiza_mapa"></a>

#### \_atualiza_mapa(mapa: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray))

Atualiza a mapa do controlador.

Ajusta o tamanho das regões colidíveis, salvando no atributo *\_mapa_expandido*, e gera um mapa
de custo para afastar o trajeto do Wall-e dos objetos colidíveis. Esse mapa é salvo no atributo *\_custo*.

Se o *mapa* for None, não será atualizado.

Limpa a imagem de debug usada nos demais métodos, exceto se *mapa=None*.

* **Parâmetros:**
  **mapa** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Mapa usado para determinar a direção.

<a id="codigo.controlador.modulos.controlador.Controlador._calcula_direcao_objeto"></a>

#### \_calcula_direcao_objeto(pos_final)

Calcula a direção que deve percorrer para alcançar um objeto.

Retorna a velocidade linear e angular que o wall-e deve seguir para continuar se movendo
no modo autônomo.

* **Parâmetros:**
  **pos_final** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Posição de destino do caminho. Onde está o objeto.
* **Retorna:**
  Direção do que o Wall-e deve se mover.
* **Tipo de retorno:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="codigo.controlador.modulos.controlador.Controlador._checa_colisao_bloco"></a>

#### \_checa_colisao_bloco(mapa, pos: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), tamanho)

Checa se houve colisão em um bloco.

A posição onde será checado deve ser uma tupla do tipo (y, x) indicando o ponto superior esquerdo do bloco.

* **Parâmetros:**
  * **mapa** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Mapa onde será checado as colisões.
  * **pos** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Posição do bloco.
  * **tamanho** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Tamanho do bloco.

<a id="codigo.controlador.modulos.controlador.Controlador._checa_colisoes"></a>

#### \_checa_colisoes(debug=False)

Checa as colisões na mapa.

As posições checadas são as definidas ao instanciar o objeto.

Verifica as colisões e retorna uma lista com o identificador de cada colisão (True ou False).

Se *debug* for True, retorna uma imagem com as regiões colidindo marcadas com amarelo, e as regiões não
colidindo marcadas com azul.

* **Parâmetros:**
  **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se True, retorna uma imagem com as regiões colidindo marcadas com amarelo, e as regiões não
  colidindo marcadas com azul. Se False, retorna apenas uma lista com o identificador de cada
  colisão (True ou False).
* **Retorna:**
  * *list* – Lista com o identificador de cada colisão (True ou False).
  * *numpy.ndarray* – Imagem com as regiões colidindo marcadas com amarelo, e as regiões não colidindo marcadas com azul.
    Apenas retornado se *debug* for True.

<a id="codigo.controlador.modulos.controlador.Controlador._cria_imagem_debug"></a>

#### \_cria_imagem_debug()

Cria uma imagem para ser usada nas funções de debug.

Nessa imagem, serão adicionadas as identificações visuais de debug. Como, por exemplo, blocos
indicando as regiões colidindo, ou uma reta indicando a direção a ser seguida.

A imagem será salva no atributo *\_imagem_debug*.

<a id="codigo.controlador.modulos.controlador.Controlador.calcula_direcao"></a>

#### calcula_direcao(mapa: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), pos_objeto: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | [None](https://docs.python.org/3/library/constants.html#None) = None, debug=False)

Calcula a direção que o Wall-e deve se mover.

Retorna a velocidade linear e angular que o wall-e deve seguir para continuar se movendo
no modo autônomo.

Se o *mapa* for None, não será atualizado. Será utilizado a mapa anterior.

Se *debug* for True, retorna uma imagem com uma reta indicando a direção do caminho a seguir.
Se está se movendo na direção de um objeto, o caminho até ele é traçado.

* **Parâmetros:**
  * **mapa** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Mapa usado para determinar a direção. Se None, usa o mapa anterior.
  * **pos_objeto** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)*,* *optional*) – Posição do objeto que onde o Wall-e deve se mover.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se True, retorna uma imagem com uma reta indicando a direção do caminho a seguir.
    Se está se movendo na direção de um objeto, o caminho até ele é traçado.
* **Retorna:**
  * *linear* – Velocidade linear do Wall-e.
  * *angular* – Velocidade angular do Wall-e.
  * *np.ndarray* – Se debug=True, retorna uma imagem com uma reta indicando a direção do caminho.

<a id="codigo.controlador.modulos.controlador.Controlador.mostra_colisoes"></a>

#### mostra_colisoes(mapa: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), debug=False)

Retorna se houve colisões no mapa.

Se o mapa for None, não será atualizado. Será utilizado a mapa anterior.

Se debug=True, retorna uma imagem com as identificações visuais das colisões.

* **Parâmetros:**
  * **mapa** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Mapa onde será checado as colisões. Se None, usa o mapa anterior.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se True, retorna uma imagem do mapa com os identificadores de colisão.
    Se False, retorna apenas um vetor com os identificadores de colisão.
* **Retorna:**
  * *list* – Lista de identificadores de colisão.
  * *numpy.ndarray* – Se debug=True, retorna uma imagem com as identificações visuais das colisões.

<a id="codigo.controlador.modulos.controlador.Controlador.parametros_PID_angular"></a>

#### parametros_PID_angular(Kp: [float](https://docs.python.org/3/library/functions.html#float), Ki: [float](https://docs.python.org/3/library/functions.html#float), Kd: [float](https://docs.python.org/3/library/functions.html#float))

Configura os parâmetros usados pelo PID da velocidade angular.

* **Parâmetros:**
  * **Kp** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Ganho proporcional.
  * **Ki** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Ganho integral.
  * **Kd** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Ganho derivativo.

<a id="codigo.controlador.modulos.controlador.Controlador.parametros_PID_linear"></a>

#### parametros_PID_linear(Kp: [float](https://docs.python.org/3/library/functions.html#float), Ki: [float](https://docs.python.org/3/library/functions.html#float), Kd: [float](https://docs.python.org/3/library/functions.html#float))

Configura os parâmetros usados pelo PID da velocidade linear.

* **Parâmetros:**
  * **Kp** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Ganho proporcional.
  * **Ki** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Ganho integral.
  * **Kd** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Ganho derivativo.

<a id="codigo.controlador.modulos.controlador.Controlador.parametros_custo"></a>

#### parametros_custo(kernel: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), sigma: [int](https://docs.python.org/3/library/functions.html#int), multiplicador: [float](https://docs.python.org/3/library/functions.html#float))

Configura os parâmetros usados para expandir a imagem.

O mapa de custo é gerado e forma semelhante à expansão do mapa (ver método [`parametros_expansao()`](#codigo.controlador.modulos.controlador.Controlador.parametros_expansao)).
Também é usado um filtro gaussiano. A diferença é não haver um offset aplicado a cada ponto, mas sim
uma operação de multiplicação. O valor multiplicado ao mapa é definido pelo parâmetro *multiplicador*.

* **Parâmetros:**
  * **kernel** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Tamanho do kernel do filtro gaussiano usado para gerar o mapa de custo.
  * **sigma** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Sigma do filtro gaussiano usado para gerar o mapa de custo.
  * **multiplicador** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Multiplicador aplicado aos valores do mapa de custo.

<a id="codigo.controlador.modulos.controlador.Controlador.parametros_expansao"></a>

#### parametros_expansao(kernel: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), sigma: [int](https://docs.python.org/3/library/functions.html#int), offset: [float](https://docs.python.org/3/library/functions.html#float))

Configura os parâmetros usados para expandir a imagem.

A expansão do mapa é feita por meio de um filtro gaussiano. Os parâmetros ajustados por esse método
são referentes a esse filtro. O parâmetro *kernel* é o tamanho do kernel, e o parâmetro *sigma* é o
sigma do filtro gaussiano.

O parâmetro *offset* é o valor de offset aplicados aos valores do mapa. Naturalmente, o valor de
uma posição do mapa varia de 0.0 até 1.0. O offset é aplicado a esse valor. Apenas se passar de 1.0,
será considerado região colidível.

* **Parâmetros:**
  * **kernel** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Tamanho do kernel do filtro gaussiano usado para expandir o mapa.
  * **sigma** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Sigma do filtro gaussiano usado para expandir o mapa.
  * **offset** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Offset aplicado aos valores do mapa. Se o valor de um ponto passar de 1.0, será considerado colidível.
