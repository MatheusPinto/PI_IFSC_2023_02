<a id="codigo-interface-modulos-interface"></a>

# codigo.interface.modulos.interface

* **code:**
  [interface.py](../../../../codigo/interface/modulos/interface.py)

<a id="module-codigo.interface.modulos.interface"></a>

Módulo com a classe de implementação da interface.

A classe que implementa a interface é a [`Interface`](#codigo.interface.modulos.interface.Interface). Para iniciá-la, deve-se passar o
path do arquivo de interface do Qt Designer (geralmente possuem a extensão ‘.ui’) como argumento.

A classe [`_FiltroDeEventos`](#codigo.interface.modulos.interface._FiltroDeEventos) é utilizada na implementação da classe [`Interface`](#codigo.interface.modulos.interface.Interface) e não deve
ser usada pelo usuário final.

<a id="codigo.interface.modulos.interface.Interface"></a>

### *class* codigo.interface.modulos.interface.Interface(arquivo_ui: [str](https://docs.python.org/3/library/stdtypes.html#str), recebedor_video: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient) | [None](https://docs.python.org/3/library/constants.html#None) = None, enviador_comandos: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Base: `QMainWindow`

<a id="codigo.interface.modulos.interface.Interface.__init__"></a>

#### \_\_init_\_(arquivo_ui: [str](https://docs.python.org/3/library/stdtypes.html#str), recebedor_video: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient) | [None](https://docs.python.org/3/library/constants.html#None) = None, enviador_comandos: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Inicialização da interface do usuário.

Deve-se passar, como argumento, o path do arquivo de interface do Qt Designer.
Esses arquivos possuem, tipicamente, a extensão ‘.ui’.

* **Parâmetros:**
  * **arquivo_ui** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Path do arquivo de interface do Qt Designer.
  * **recebedor_video** ([*TLSclient*](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient)) – Cliente que recebe os vídeos do Wall-e.
  * **enviador_comandos** ([*TLSclient*](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient)) – Cliente que envia os comandos para o Wall-e.

<a id="codigo.interface.modulos.interface.Interface._ativa_enviador_comandos"></a>

#### \_ativa_enviador_comandos()

Ativa o envio de comandos para o Wall-e.

<a id="codigo.interface.modulos.interface.Interface._botao_auto_slot"></a>

#### \_botao_auto_slot()

Implementa o callback do botão de controle do modo de operação.

Altera entre o modo de controle do Wall-e em modo teleoperado ou autônomo.

<a id="codigo.interface.modulos.interface.Interface._botao_desliga_slot"></a>

#### \_botao_desliga_slot()

Implementa o callback do botão de desligar o Wall-e.

Essa ação não pode ser desfeita por software. É necessário
reiniciar o Wall-e diretamente no hardware.

<a id="codigo.interface.modulos.interface.Interface._define_direcao"></a>

#### \_define_direcao(valor: [int](https://docs.python.org/3/library/functions.html#int), atualiza_joystick=True)

Define a direção para onde o Wall-e está se movendo.

O valor da direção é um número de 0 a 99 (mesma notação usada pelo widget ‘Dial’ do framework Qt).
A correlação entre esse valor e a direção pode ser visto na tabela a seguir.

| Valor                          | direção                                           |
|--------------------------------|---------------------------------------------------|
| 0<br/>25<br/>50<br/>75<br/>100 | Trás<br/>Esquerda<br/>Frente<br/>direita<br/>Trás |

Normalmente, esse método atualiza o joystick para o valor recebido, exceto se o parâmetro
*atualiza_joystick* seja *False*.

* **Parâmetros:**
  * **valor** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Valor para qual a direção será definida.
  * **atualiza_joystick** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Se deve ou não atualizar o joystick.

<a id="codigo.interface.modulos.interface.Interface._define_velocidade"></a>

#### \_define_velocidade(valor: [int](https://docs.python.org/3/library/functions.html#int), atualiza_barra=True)

Define a velocidade do Wall-e.

O valor da velocidade é um número de 0 a 99. Sendo 0 a velocidade mínima, e 99 a máxima.

Normalmente, atualiza a barra de velocidade para o valor fornecido, exceto se o parâmetro
*atualiza_barra* seja *False*.

* **Parâmetros:**
  * **valor** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Valor para qual a velocidade será definida.
  * **atualiza_barra** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default True*) – Se deve ou não atualizar o barra de velocidade.

<a id="codigo.interface.modulos.interface.Interface._desativa_enviador_comandos"></a>

#### \_desativa_enviador_comandos()

Desativa o envio de comandos para o Wall-e.

<a id="codigo.interface.modulos.interface.Interface._envia_texto"></a>

#### \_envia_texto(texto: [str](https://docs.python.org/3/library/stdtypes.html#str), esperar=False)

Envia um texto para o Wall-e.

Não envia uma mensagem se uma anterior ainda estiver sendo enviada. Cancela a operação
e a mensagem será descartada. Caso *esperar=True*, ao invés de cancelar o envio da
mensagem, espera até que seja possível enviá-la.

* **Parâmetros:**
  * **texto** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Texto a ser enviado para o Wall-e.
  * **esperar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se deve esperar a mensagem anterior ser enviada, ou cancelar o envio da atual.

<a id="codigo.interface.modulos.interface.Interface._joystick_slot"></a>

#### \_joystick_slot()

Implementa o callback do joystick.

Altera a direção de movimento do Wall-e.

<a id="codigo.interface.modulos.interface.Interface._loop_envia_comandos"></a>

#### \_loop_envia_comandos()

Constantemente envia os comandos de direção e velocidade para o Wall-e.

O envio da velocidade e direção do Wall-e deve ocorrer continuamente, para permitir que o Wall-e
pare de se mover caso não receba nenhum comando. Dessa forma, evita o risco do Wall-e se
mover de forma desgovernada.

Esse método deve ser executado em uma thread própria.

<a id="codigo.interface.modulos.interface.Interface._velocidade_slot"></a>

#### \_velocidade_slot()

Implementa o callback da barra de velocidade.

Altera a velocidade de movimento do Wall-e.

<a id="codigo.interface.modulos.interface.Interface._video_callback"></a>

#### \_video_callback(recebedor_video: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient))

Função de callback para o streaming de video.

O objeto possui uma lista de funções de callback: *\_video_callback_lista*. Esse
método executa todas elas passando, como atributo, o próprio objeto e a imagem
recebida. Por isso, as funções de callback devem possuir o formato *funcao(interface, RGB, BGR)*.

A imagem recebida pela interface é um bytearray de um jpg. Esse método converte
para um array numpy do tipo uint8 com a estrutura (colunas, linhas, canais). A
imagem é fornecida para as funções de callback em RGB e BGR (padrão do OpenCV).

* **Parâmetros:**
  **recebedor_video** ([*TLSclient*](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient)) – Recebedor de video.

<a id="codigo.interface.modulos.interface.Interface.adiciona_velocidade"></a>

#### adiciona_velocidade(valor, atualiza_barra=True)

Adiciona um valor à barra de velocidade do Wall-e.

Funciona de forma semelhante ao método [`_define_velocidade()`](#codigo.interface.modulos.interface.Interface._define_velocidade). Os parâmetros são os mesmos.
A diferença e que, em vez do valor recebido pelo método ser definido como o novo valor de
velocidade, ele é adicionado ao valor atual.

* **Parâmetros:**
  * **valor** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Valor adicionado a velocidade.
  * **atualiza_barra** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default True*) – Se deve ou não atualizar o barra de velocidade.

<a id="codigo.interface.modulos.interface.Interface.adiciona_video_callback"></a>

#### adiciona_video_callback(callback: callable)

Adiciona uma nova função de callback para o recebimento de imagem.

Funciona da mesma forma que o método [`define_video_callback_lista()`](#codigo.interface.modulos.interface.Interface.define_video_callback_lista), mas adiciona uma função de
callback em vez de substituir todas.

* **Parâmetros:**
  **callback** (*callable*) – Nova função de callback para o recebimento de imagem.

<a id="codigo.interface.modulos.interface.Interface.atualiza_direcao_keyboard"></a>

#### atualiza_direcao_keyboard()

Atualiza a direção de movimento do Wall-e com base na tecla pressionada.

Ao pressionar um teclado, é disparado um evento que o framework Qt recebe e envia para o
[`_FiltroDeEventos`](#codigo.interface.modulos.interface._FiltroDeEventos). Esse filtro é responsável por checar qual tecla foi pressionada e ajustar
os atributos *self.direcao_x* e *self.direcao_y* com base nela. Esse método serve para ler
os valores desses atributos e ajustar a direção do Wall-e com base neles.

<a id="codigo.interface.modulos.interface.Interface.atualiza_enviador_comandos"></a>

#### atualiza_enviador_comandos()

Reinicia o tempo do enviador de comandos.

Reinicia o tempo para que o enviador de comandos envie os comandos para o wall-e.

<a id="codigo.interface.modulos.interface.Interface.atualiza_frame"></a>

#### atualiza_frame(imagem: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), BGR=False)

Atualiza o frame de vídeo da interface do usuário.

A imagem deve ser um array numpy do tipo uint8 com a estrutura (linhas, colunas, canais).
As imagens do OpenCV já possuem esse formato. Devem estar no formato RGB para funcionar.
Caso estejam no formato BGR, use o parâmetro *BGR=True*. Essa informação é necessária
para que ele seja convertido para RGB antes de ser aplicado na interface.

O frame recebido é redimensionada se a imagem for muito pequena (menor do que 300px por
300px) e apresentada na interface.

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Imagem (array do numpy) que será exibida na interface. Em RGB, ou em BGR se o
    parâmetro *BGR=True*.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem está no formato BGR.

<a id="codigo.interface.modulos.interface.Interface.close"></a>

#### close()

Finaliza a interface de usuário.

Depois disso, o objeto se torna inutilizável.

<a id="codigo.interface.modulos.interface.Interface.define_video_callback_lista"></a>

#### define_video_callback_lista(lista_callback: [list](https://docs.python.org/3/library/stdtypes.html#list))

Define a lista de funções de callback para o recebimento de imagem.

Limpa a antiga lista (remove todos os callbacks, menos o padrão).

As funções devem possuir a seguinte assinatura: *def callback(interface, RGB, BGR)*. *interface* é
o objeto da interface que chamou a função de callback; e RGB e BGR são as imagens nesses respectivos
formatos. As imagens são um array numpy do tipo uint8 com formato (linhas, colunas, canais).

* **Parâmetros:**
  **lista_callback** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) – Nova lista de callback para o recebimento de imagem.

<a id="codigo.interface.modulos.interface._FiltroDeEventos"></a>

### *class* codigo.interface.modulos.interface.\_FiltroDeEventos

Base: `QObject`

<a id="codigo.interface.modulos.interface._FiltroDeEventos.eventFilter"></a>

#### eventFilter(widget, event)

Filtra os eventos e lê apenas os caracteres do teclado e os eventos do mouse.

Os carácteres ‘a’, ‘s’, ‘w’ e ‘d’ são usados para controlar a direção do joystick.
Os eventos do mouse são usados para controlar tanto a direção do joystick, quanto a
barra de velocidade.
