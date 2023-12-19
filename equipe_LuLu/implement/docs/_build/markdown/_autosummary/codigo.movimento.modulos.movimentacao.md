<a id="codigo-movimento-modulos-movimentacao"></a>

# codigo.movimento.modulos.movimentacao

* **code:**
  [movimentacao.py](../../../../codigo/movimento/modulos/movimentacao.py)

<a id="module-codigo.movimento.modulos.movimentacao"></a>

Módulo de controle do Wall-e.

Implementa a classe [`Movimento`](#codigo.movimento.modulos.movimentacao.Movimento) que permite controlar a movimentação do Wall-e em alto nível.
Basta fornecer a velocidade linear e angular.

<a id="codigo.movimento.modulos.movimentacao.Movimento"></a>

### *class* codigo.movimento.modulos.movimentacao.Movimento(pinos_driver_DC: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pinos_servos: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pino_buzzer: [int](https://docs.python.org/3/library/functions.html#int), modo_GPIO: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'BCM')

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Controlador do movimento do Wall-e.

Controla e gerencia os motores que movimentam o Wall-e:

* 2 motores DC, por meio de uma ponte H.
* 3 servo motores.

Além disso, controla um buzzer ativo em nível lógico baixo, usado para sinalização de lixo.

Para definir a velocidade, use o método [`define_velocidade()`](#codigo.movimento.modulos.movimentacao.Movimento.define_velocidade).

Para indicar que o Wall-e encontrou um lixo, use o método [`sinaliza_lixo()`](#codigo.movimento.modulos.movimentacao.Movimento.sinaliza_lixo). Caso deseje saber
se o Wall-e está sinalizando o lixo, use o método [`esta_sinalizando_lixo()`](#codigo.movimento.modulos.movimentacao.Movimento.esta_sinalizando_lixo).

<a id="codigo.movimento.modulos.movimentacao.Movimento.__init__"></a>

#### \_\_init_\_(pinos_driver_DC: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pinos_servos: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pino_buzzer: [int](https://docs.python.org/3/library/functions.html#int), modo_GPIO: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'BCM')

Configura os motores usados na movimentação do Wall-e, e o buzzer.

Configura os motores DC (ponte H) e os servo motores usados. Deve ser fornecido um vetor com os
pinos GPIO do motor DC, e outro com os pinos GPIO dos servo motores. Além disso, é necessário
informardo pino GPIO do buzzer para configurar o buzzer.

* **Parâmetros:**
  * **pinos_driver_DC** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Os pinos GPIO do motor DC. Deve estar no formato (IN1, IN2, IN3, IN4). Observe o método
    [`__init__()`](codigo.movimento.modulos.motores.md#codigo.movimento.modulos.motores.DC.__init__) da classe [`DC`](codigo.movimento.modulos.motores.md#codigo.movimento.modulos.motores.DC)
    para mais informações.
  * **pinos_servos** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Os pinos GPIO dos servo motores. Cada elemento corresponde a um pino usado para controlar um
    servo motor. Deve estar no formato (pino1, pino2, pino3). Em que, pino1 e pino2 são os usados
    para controlar os braços direito e esquerdo, respectivamente; e pino3 é usado para controlar o pescoço.
  * **pino_buzzer** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O pino GPIO do buzzer.
  * **modo_GPIO** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default="BCM"*) – O modo de configuração dos pinos GPIO. Pode ser “BCM” ou “BOARD”.

<a id="codigo.movimento.modulos.movimentacao.Movimento.define_velocidade"></a>

#### define_velocidade(velocidade_linear: [float](https://docs.python.org/3/library/functions.html#float), velocidade_angular: [float](https://docs.python.org/3/library/functions.html#float))

Define a velocidade linear e angular de movimento do Wall-e.

O valor de *velocidade_linear* é um número de -100 a 100. Se receber 0, significa que a velocidade
linear é nula, 100 significa velocidade máxima para frente. Um valor negativo significa que deve se
mover na direção contrária (para trás).

O valor de *velocidade_angular* é um número de -100 a 100. Se receber -100, significa que o motor deve
se mover o máximo possível no sentido horário (visualizando de cima para baixo). 100 significa o máximo
possível no sentido anti-horário (visualizando de cima para baixo).

* **Parâmetros:**
  * **velocidade_linear** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A velocidade linear de movimento do Wall-e.
  * **velocidade_angular** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A velocidade angular de movimento do Wall-e.

<a id="codigo.movimento.modulos.movimentacao.Movimento.esta_sinalizando_lixo"></a>

#### esta_sinalizando_lixo()

Retorna se a sinalização de lixo está ativa.

Se o Wall-e está sinalizando lixo, retorna True. Caso contrário, retorna False.

* **Retorna:**
  Se o Wall-e está sinalizando lixo.
* **Tipo de retorno:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="codigo.movimento.modulos.movimentacao.Movimento.sinaliza_lixo"></a>

#### sinaliza_lixo()

Executa a sinalização de que detectou um lixo.

Ao detectar um lixo na área, esse método deve ser chamado. O Wall-e sinaliza que detectou o
lixo acionando o buzzer. O buzzer é ativo em nível lógico 0, e desativa em nível lógico 1.

Quando estiver sinalizando que um lixo foi encontrado, o Wall-e não pode se mover. Ou seja, a
velocidade dos motores DC é zerada.

Esse método é sequencial. Ou seja, não é executado na mesma Thread em que é chamado. Não pode ser
executado mais de uma vez simultaneamente. Se isso acontecer, a última chamada desse método será cancelada.
