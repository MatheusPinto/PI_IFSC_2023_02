<a id="module-codigo.movimento.modulos.movimentacao"></a>

<a id="codigo-movimento-modulos-movimentacao"></a>

# codigo.movimento.modulos.movimentacao

Módulo de controle do Wall-e.

Implementa a classe [`Movimento`](#codigo.movimento.modulos.movimentacao.Movimento) que permite controlar a movimentação do Wall-e em alto nível.
Basta fornecer a velocidade linear e angular.

<a id="codigo.movimento.modulos.movimentacao.Movimento"></a>

### *class* codigo.movimento.modulos.movimentacao.Movimento(pinos_driver_DC: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pinos_motor_passo: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pino_buzzer: [int](https://docs.python.org/3/library/functions.html#int), modo_GPIO: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'BCM')

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Controlador do movimento do Wall-e.

Controla e gerencia os motores que movimentam o Wall-e:

* 2 motores DC, por meio de uma ponte H.
* 3 motores de passo.

Além disso, controla um buzzer ativo em nível lógico baixo, usado para sinalização de lixo.

Para definir a velocidade, use o método [`define_velocidade()`](#codigo.movimento.modulos.movimentacao.Movimento.define_velocidade).

Para indicar que o Wall-e encontrou um lixo, use o método [`sinaliza_lixo()`](#codigo.movimento.modulos.movimentacao.Movimento.sinaliza_lixo).

<a id="codigo.movimento.modulos.movimentacao.Movimento.__init__"></a>

#### \_\_init_\_(pinos_driver_DC: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pinos_motor_passo: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), pino_buzzer: [int](https://docs.python.org/3/library/functions.html#int), modo_GPIO: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'BCM')

Configura os motores usados na movimentação do Wall-e, e o buzzer.

Configura os motores DC (ponte H) e os motores de passo usados. Deve ser fornecido um vetor com os
pinos GPIO do motor DC, e outro com os pinos GPIO dos motores de passo. Além disso, é necessário
informardo pino GPIO do buzzer para configurar o buzzer.

* **Parâmetros:**
  * **pinos_driver_DC** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Os pinos GPIO do motor DC. Deve estar no formato (IN1, IN2, IN3, IN4). Observe o método
    [`__init__()`](codigo.movimento.modulos.motores.md#codigo.movimento.modulos.motores.DC.__init__) da classe [`DC`](codigo.movimento.modulos.motores.md#codigo.movimento.modulos.motores.DC)
    para mais informações.
  * **pinos_motor_passo** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – Os pinos GPIO dos motores de passo. Cada elemento corresponde a um pino usado para controlar um
    motor de passo. Deve estar no formato (pino1, pino2, pino3). Em que, pino1 e pino2 são os usados
    para controlar os braços direito e esquerdo, respectivamente; e pino3 é usado para controlar o pescoço.
  * **pino_buzzer** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O pino GPIO do buzzer.
  * **modo_GPIO** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – O modo de configuração dos pinos GPIO. Pode ser “BCM” ou “BOARD”.

<a id="codigo.movimento.modulos.movimentacao.Movimento._ajusta_motores_sinalizacao"></a>

#### \_ajusta_motores_sinalizacao(angulo1: [float](https://docs.python.org/3/library/functions.html#float), angulo2: [float](https://docs.python.org/3/library/functions.html#float), angulo3: [float](https://docs.python.org/3/library/functions.html#float))

* **Parâmetros:**
  * **angulo1** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O angulo do primeiro motor de passo.
  * **angulo2** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O angulo do segundo motor de passo.
  * **angulo3** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O angulo do terceiro motor de passo.

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

<a id="codigo.movimento.modulos.movimentacao.Movimento.sinaliza_lixo"></a>

#### sinaliza_lixo()

Executa a sinalização de que detectou um lixo.

Ao detectar um lixo na área, esse método deve ser chamado. O Wall-e sinaliza que detectou o
lixo acionando o buzzer, e mexendo os braços e cabeça.

O movimento dos braços e cabeça é feito por motores de passo. Apenas um motor de passo tem seu
ângulo alterado por vez. Por exemplo: move-se o braço e, apenas após parar de mover o
braço, que pode-se mover o pescoço. A ordem de movimento dos membros do Wall-e é a seguinte:

- Braço esquerdo
- Braço direito
- Cabeça

O buzzer é ativo em nível lógico 0, e desativa em nível lógico 1.

Quando estiver sinalizando que um lixo foi encontrado, o Wall-e não pode se mover. Ou seja, a
velocidade dos motores DC é zerada.

Esse método é sequencial. Ou seja, não é executado na mesma Thread em que é chamado. Não pode ser
executado mais de uma vez ao mesmo tempo. Se isso acontecer, a última chamnada desse ,étodo será cancelada.
