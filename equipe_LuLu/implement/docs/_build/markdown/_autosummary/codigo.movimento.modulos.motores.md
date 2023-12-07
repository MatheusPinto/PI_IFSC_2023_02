<a id="codigo-movimento-modulos-motores"></a>

# codigo.movimento.modulos.motores

* **code:**
  [motores.py](../../../../codigo/movimento/modulos/motores.py)

<a id="module-codigo.movimento.modulos.motores"></a>

Módulo de controle dos motores.

Implementa duas classes:

* [`DC`](#codigo.movimento.modulos.motores.DC): controla os motores DC por meio de uma ponte H L298N.
* [`Passo`](#codigo.movimento.modulos.motores.Passo): controla os servo motores.

<a id="codigo.movimento.modulos.motores.DC"></a>

### *class* codigo.movimento.modulos.motores.DC(IN1: [int](https://docs.python.org/3/library/functions.html#int), IN2: [int](https://docs.python.org/3/library/functions.html#int), IN3: [int](https://docs.python.org/3/library/functions.html#int), IN4: [int](https://docs.python.org/3/library/functions.html#int))

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe de controle dos motores DC.

Ao inicializar, deve-se fornecer o número das portas GPIO usadas para controlar o Driver de motor DC.

Para ajustar a velocidade dos motores, utilize os métodos [`velocidade_motor_E()`](#codigo.movimento.modulos.motores.DC.velocidade_motor_E) e [`velocidade_motor_D()`](#codigo.movimento.modulos.motores.DC.velocidade_motor_D)
que controlam, respectivamente, a velocidade dos motores esquerdo e direito.

<a id="codigo.movimento.modulos.motores.DC.__init__"></a>

#### \_\_init_\_(IN1: [int](https://docs.python.org/3/library/functions.html#int), IN2: [int](https://docs.python.org/3/library/functions.html#int), IN3: [int](https://docs.python.org/3/library/functions.html#int), IN4: [int](https://docs.python.org/3/library/functions.html#int))

Configura as portas GPIO da Raspberry Pi que serão usadas para controlar o motor de DC.

Os parâmetros IN1 até IN4 são os números das portas GPIO da Raspberry Pi usadas para controlar o driver L298N.

* **Parâmetros:**
  * **IN1** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número da porta GPIO que controla o motor esquerdo, sentido para frente.
  * **IN2** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número da porta GPIO que controla o motor esquerdo, sentido para trás.
  * **IN3** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número da porta GPIO que controla o motor direito, sentido para frente
  * **IN4** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O número da porta GPIO que controla o motor direito, sentido para trás.

<a id="codigo.movimento.modulos.motores.DC._velocidade_motor"></a>

#### \_velocidade_motor(pwm1, pwm2, velocidade: [float](https://docs.python.org/3/library/functions.html#float))

Ajusta a velocidade de motor do driver.

Os PWM usados para controlar o motor devem ser fornecidos pelos parâmetros *pwm1* e *pwm2*.

O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
100 significa velocidade máxima. Um valor negativo significa que deve se move na direção
contrária (para trás).

* **Parâmetros:**
  * **pwm1** ([*GPIO.PWM*](codigo.movimento.fake_RPi.RPi.GPIO.md#codigo.movimento.fake_RPi.RPi.GPIO.PWM)) – O PWM que controla o motor esquerdo.
  * **pwm2** ([*GPIO.PWM*](codigo.movimento.fake_RPi.RPi.GPIO.md#codigo.movimento.fake_RPi.RPi.GPIO.PWM)) – O PWM que controla o motor direito.
  * **velocidade** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A velocidade do motor.

<a id="codigo.movimento.modulos.motores.DC.desliga"></a>

#### desliga()

Desliga os motores.

Desativa os PWM que controlam a ponte H e libera as GPIO da Raspberry Pi utilizadas. O objeto se torna
inútil depois disso.

<a id="codigo.movimento.modulos.motores.DC.velocidade_motor_D"></a>

#### velocidade_motor_D(velocidade: [float](https://docs.python.org/3/library/functions.html#float))

Ajusta a velocidade do motor direito.

O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
100 significa velocidade máxima. Um valor negativo significa que deve se mover na direção
contrária (para trás).

* **Parâmetros:**
  **velocidade** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A velocidade do motor direito.

<a id="codigo.movimento.modulos.motores.DC.velocidade_motor_E"></a>

#### velocidade_motor_E(velocidade: [float](https://docs.python.org/3/library/functions.html#float))

Ajusta a velocidade do motor esquerdo.

O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
100 significa velocidade máxima. Um valor negativo significa que deve se mover na direção
contrária (para trás).

* **Parâmetros:**
  **velocidade** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A velocidade do motor esquerdo.

<a id="codigo.movimento.modulos.motores.Passo"></a>

### *class* codigo.movimento.modulos.motores.Passo(pino: [int](https://docs.python.org/3/library/functions.html#int), passos: [float](https://docs.python.org/3/library/functions.html#float))

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe de controle de um servo motor SG90.

Ao inicializar, deve ser fornecido o pino GPIO usado para controlar o motor.

A mudança de ângulo do servo motor ocorre gradualmente. Ou sejá, ele não muda de 120° direto
para 180°, mas sim em passos. O valor desses passos são configurados na inicialização do objeto.

Para definir o ângulo do motor, use o método [`define_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.define_angulo_destino) e, para atualizar o ângulo
do motor, use o método [`atualiza_angulo()`](#codigo.movimento.modulos.motores.Passo.atualiza_angulo). A atualização deve ser feita em intervalos de tempo de
forma que não cause mudanças bruscas no ângulo do motor.

Para verificar os ângulos relacionados ao servo motor, há dois métodos:

* retorna_angulo_atual(): retorna o ângulo atual do servo motor.
* retorna_angulo_destino(): retorna o ângulo para qual o servo motor está se direcionando.

<a id="codigo.movimento.modulos.motores.Passo.__init__"></a>

#### \_\_init_\_(pino: [int](https://docs.python.org/3/library/functions.html#int), passos: [float](https://docs.python.org/3/library/functions.html#float))

Configura o servo motor.

Deve ser fornecido o número do *pino* usado para controlar o servo motor. E o número de passos
que serão somados quando o ângulo do motor for atualizado.

Os *passos* são informados em graus. Por exemplo, se passos=3, então sempre que o servo motor
for atualizado pelo método [`atualiza_angulo()`](#codigo.movimento.modulos.motores.Passo.atualiza_angulo) será somado 3 graus ao ângulo atual, até alcançar
o ângulo de destino definido por [`define_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.define_angulo_destino).

* **Parâmetros:**
  * **pino** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O pino GPIO que controla o servo motor.
  * **angulo_inicial** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O ângulo inicial do servo motor.
  * **passos** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O número de passos que serão somados quando o ângulo do motor for atualizado.

<a id="codigo.movimento.modulos.motores.Passo._converte_duty_para_graus"></a>

#### \_converte_duty_para_graus(duty_cycle: [float](https://docs.python.org/3/library/functions.html#float))

Converte o duty cycle do PWM usado pelo motor SG90 para o angulo em graus.

* **Parâmetros:**
  **duty_cycle** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O duty cycle do PWM.

<a id="codigo.movimento.modulos.motores.Passo._converte_graus_para_duty"></a>

#### \_converte_graus_para_duty(angulo: [float](https://docs.python.org/3/library/functions.html#float))

Converte o ângulo em graus para o duty cycle do PWM usado pelo motor SG90.

* **Parâmetros:**
  **angulo** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O angulo em graus.

<a id="codigo.movimento.modulos.motores.Passo.atualiza_angulo"></a>

#### atualiza_angulo()

Atualiza o angulo atual do motor.

O angulo do motor se ajustará gradualmente até alcançar o valor do ângulo de destino. Esse método atualiza
o passo definido na instanciação da classe.

O ângulo de destino é definido pelo método [`define_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.define_angulo_destino). A atualização ocorre em
passos definidos pelo parâmetro *passos* do método de inicialização da classe [`__init__()`](#codigo.movimento.modulos.motores.Passo.__init__):.

<a id="codigo.movimento.modulos.motores.Passo.define_angulo_destino"></a>

#### define_angulo_destino(angulo: [float](https://docs.python.org/3/library/functions.html#float))

Define o ângulo de destino do servo motor.

O ângulo atual do servo motor se ajustará gradualmente até alcançar o valor definido pelo parâmetro *angulo*.
Para realizar uma atualização, use o método [`atualiza_angulo()`](#codigo.movimento.modulos.motores.Passo.atualiza_angulo)

O ângulo é informado em graus.

* **Retorna:**
  O ângulo de destino do servo motor.
* **Tipo de retorno:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="codigo.movimento.modulos.motores.Passo.desliga"></a>

#### desliga()

Desliga o servo motor.

Desativa o PWM que controla os motor e libera a GPIO da Raspberry Pi utilizada. O objeto se torna
inútil depois disso.

<a id="codigo.movimento.modulos.motores.Passo.inicia"></a>

#### inicia(angulo)

Inicia o servo motor.

<a id="codigo.movimento.modulos.motores.Passo.retorna_angulo_atual"></a>

#### retorna_angulo_atual()

Retorna o ângulo atual do servo motor.

É importante notar que, como o ângulo do servo motor varia gradualmente, o valor retornado por esse
método não obrigatoriamente será o definido ao usar o método [`define_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.define_angulo_destino). O ângulo atual
se ajustará gradualmente até chegar ao ângulo configurado por esse método.

Se deseja ler o ângulo selecionado por [`define_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.define_angulo_destino), use o método [`retorna_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.retorna_angulo_destino).

O ângulo é retornado em graus.

* **Retorna:**
  O ângulo atual do servo motor.
* **Tipo de retorno:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="codigo.movimento.modulos.motores.Passo.retorna_angulo_destino"></a>

#### retorna_angulo_destino()

Retorna o ângulo de destino do servo motor.

Por exemplo, se foi usado a função [`define_angulo_destino()`](#codigo.movimento.modulos.motores.Passo.define_angulo_destino) para definir 120°. Essa função retorna 120.

O ângulo é retornado em graus.

* **Retorna:**
  O ângulo de destino do servo motor.
* **Tipo de retorno:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="codigo.movimento.modulos.motores.configura_GPIO"></a>

### codigo.movimento.modulos.motores.configura_GPIO(modo: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'BOARD')

Configura os pinos do Raspberry Pi.

Configura o modo de numeração dos pinos. Se utilizado ‘BOARD’, os pinos se referem aos pinos da área
placa, e não ao número da GPIO. Se utilizado ‘BCM’, os pinos se referem aos números da GPIO, e não aos pinos
da placa.

* **Parâmetros:**
  **modo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – O modo de numeração dos pinos. Pode ser ‘BOARD’ ou ‘BCM’.
