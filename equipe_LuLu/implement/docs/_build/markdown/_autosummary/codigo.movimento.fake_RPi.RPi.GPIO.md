<a id="module-codigo.movimento.fake_RPi.RPi.GPIO"></a>

<a id="codigo-movimento-fake-rpi-rpi-gpio"></a>

# codigo.movimento.fake_RPi.RPi.GPIO

Módulo de simulação para o módulo RPi.GPIO.

Permite executar os scripts que dependem do módulo RPi.GPIO fora da Raspberry Pi. Em vez de definir
os nível lógicos das GPIO, apenas mostra na saída padrão o que foi configurado.

Esse módulo não deve ser usado na Raspberry Pi. Apenas no computador de desenvolvimento. Portanto,
não deve ser enviado para a Raspberry Pi ao sincronizar o código.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.BCM"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.BCM *= 'BCM'*

Tipo de identificação dos pinos da Raspberry Pi. Se utilizado, os pinos se referem aos
número da GPIO, e não aos pinos da placa.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.BOARD"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.BOARD *= 'BOARD'*

Tipo de identificação dos pinos da Raspberry Pi. Se utilizado, os pinos se referem aos
pidos da própria placa, e não ao número da GPIO.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.HIGH"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.HIGH *= 1*

Nível lógico alto (3,3V). Para ser usado ao definir o estado da saída de um pino.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.IN"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.IN *= 'IN'*

Configuração do pino como entrada

<a id="codigo.movimento.fake_RPi.RPi.GPIO.LOW"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.LOW *= 0*

Nível lógico baixo (0V). Para ser usado ao definir o estado da saída de um pino.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.OUT"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.OUT *= 'OUT'*

Configuração do pino como saída

<a id="codigo.movimento.fake_RPi.RPi.GPIO.PWM"></a>

### *class* codigo.movimento.fake_RPi.RPi.GPIO.PWM(canal: [int](https://docs.python.org/3/library/functions.html#int), freq: [float](https://docs.python.org/3/library/functions.html#float))

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Simulação de um PWM.

Apenas apresenta os valores de frequẽncia e duty cycle definidos na saída padrão quando eles são ajustados.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.PWM.ChangeDutyCycle"></a>

#### ChangeDutyCycle(duty_cycle: [float](https://docs.python.org/3/library/functions.html#float))

Altera o duty cycle do PWM.

* **Parâmetros:**
  **duty_cycle** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O novo duty cycle do PWM.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.PWM.ChangeFrequency"></a>

#### ChangeFrequency(freq: [float](https://docs.python.org/3/library/functions.html#float))

Altera a frequência do PWM.

* **Parâmetros:**
  **freq** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A nova frequência do PWM.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.PWM.__init__"></a>

#### \_\_init_\_(canal: [int](https://docs.python.org/3/library/functions.html#int), freq: [float](https://docs.python.org/3/library/functions.html#float))

Inicialização.

* **Parâmetros:**
  * **canal** ([*int*](https://docs.python.org/3/library/functions.html#int)) – O canal a ser configurado. Deve ser um número inteiro.
  * **freq** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A frequência do PWM.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.PWM.start"></a>

#### start(duty_cycle: [float](https://docs.python.org/3/library/functions.html#float))

Incia o PWM.

* **Parâmetros:**
  **duty_cycle** ([*float*](https://docs.python.org/3/library/functions.html#float)) – O duty cycle do PWM.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.PWM.stop"></a>

#### stop()

Para o PWM.

<a id="codigo.movimento.fake_RPi.RPi.GPIO._testa_canais"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.\_testa_canais(canais: [int](https://docs.python.org/3/library/functions.html#int) | [list](https://docs.python.org/3/library/stdtypes.html#list) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) = -1, configuracao_do_pino=None)

Checa o modo do módulo e  configuração do pino.

Se o módo do módulo não foi definido, causa uma excessão.

Checa se os *canais* foram configurados de acordo com *configuracao_do_pino*. Caso não seja, resulta em uma excessão.
A *configuracao_do_pino* se refere aos modos [`IN`](#codigo.movimento.fake_RPi.RPi.GPIO.IN) e [`OUT`](#codigo.movimento.fake_RPi.RPi.GPIO.OUT).

Se fornecido um número inteiro em *canais*, checa apenas esse canal. Mas se for fornecido uma lista ou tupla, checa
todos os canais dela.

* **Parâmetros:**
  * **canais** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)*,* *default -1*) – Os canais a serem checados.
  * **configuracao_do_pino** ([`IN`](#codigo.movimento.fake_RPi.RPi.GPIO.IN) ou [`OUT`](#codigo.movimento.fake_RPi.RPi.GPIO.OUT)) – A configuração correta dos canais (para checagem). Pode ser [`IN`](#codigo.movimento.fake_RPi.RPi.GPIO.IN) ou [`OUT`](#codigo.movimento.fake_RPi.RPi.GPIO.OUT).

<a id="codigo.movimento.fake_RPi.RPi.GPIO._testa_modo"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.\_testa_modo()

Checa o modo do módulo.

Se o módo do módulo não foi definido, causa uma excessão.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.cleanup"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.cleanup(canais: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Desliga os canais.

* **Parâmetros:**
  **canais** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)*,* *optional*) – Os canais a serem desligados. Se None, desliga todos os canais.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.getmode"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.getmode()

Retorna o tipo de numeração dos GPIO.

* **Retorna:**
  O tipo de numeração dos pinos GPIO. Pode ser [`BOARD`](#codigo.movimento.fake_RPi.RPi.GPIO.BOARD) ou [`BCM`](#codigo.movimento.fake_RPi.RPi.GPIO.BCM).
* **Tipo de retorno:**
  [`BOARD`](#codigo.movimento.fake_RPi.RPi.GPIO.BOARD) or [`BCM`](#codigo.movimento.fake_RPi.RPi.GPIO.BCM)

<a id="codigo.movimento.fake_RPi.RPi.GPIO.output"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.output(canais: [int](https://docs.python.org/3/library/functions.html#int) | [list](https://docs.python.org/3/library/stdtypes.html#list) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), estado)

Define a saída de um canal.

O canal deve estar onfigurado como ‘GPIO.OUTPUT’ usando a função [`setup()`](#codigo.movimento.fake_RPi.RPi.GPIO.setup).

* **Parâmetros:**
  * **canais** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – O canal cuja saída será definida. Deve ser um número inteiro.
  * **estado** ([`LOW`](#codigo.movimento.fake_RPi.RPi.GPIO.LOW) or [`HIGH`](#codigo.movimento.fake_RPi.RPi.GPIO.HIGH)) – O estado do canal. Pode ser [`LOW`](#codigo.movimento.fake_RPi.RPi.GPIO.LOW) ou [`HIGH`](#codigo.movimento.fake_RPi.RPi.GPIO.HIGH).

<a id="codigo.movimento.fake_RPi.RPi.GPIO.setmode"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.setmode(numeracao)

Define a numeração dos pinos GPIO.

Configura o tipo de identificação dos pinos da Raspberry Pi. Se utilizado [`BOARD`](#codigo.movimento.fake_RPi.RPi.GPIO.BOARD), os pinos
se referem aos pidos da própria placa, e não ao número da GPIO. Se utilizado [`BCM`](#codigo.movimento.fake_RPi.RPi.GPIO.BCM), os pinos
se referem aos número da GPIO, e não aos pinos da placa.

* **Parâmetros:**
  **numeracao** ([`BOARD`](#codigo.movimento.fake_RPi.RPi.GPIO.BOARD) or [`BCM`](#codigo.movimento.fake_RPi.RPi.GPIO.BCM)) – O tipo de numeração dos pinos GPIO. Pode ser [`BOARD`](#codigo.movimento.fake_RPi.RPi.GPIO.BOARD) ou [`BCM`](#codigo.movimento.fake_RPi.RPi.GPIO.BCM).

<a id="codigo.movimento.fake_RPi.RPi.GPIO.setup"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.setup(canais: [int](https://docs.python.org/3/library/functions.html#int) | [list](https://docs.python.org/3/library/stdtypes.html#list) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), config)

Define um canal ou uma lista de canais como entrada ou saída.

Se fornecido um número inteiro em *canais*, o canal desse número será definido com entrada
ou saída, dependendo do parâmetro *config*.

Caso *canais* seja uma lista ou tupla, o canal de cada elemento da lista ou tupla será definido
com entrada ou saída, dependendo do parâmetro *config*.

* **Parâmetros:**
  * **canais** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *or* [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)) – O canal a ser configurado. Deve ser um número inteiro.
  * **config** ([`OUT`](#codigo.movimento.fake_RPi.RPi.GPIO.OUT) or [`IN`](#codigo.movimento.fake_RPi.RPi.GPIO.IN)) – A configuração do canal. Pode ser ‘OUT’ ou ‘IN’.

<a id="codigo.movimento.fake_RPi.RPi.GPIO.setwarnings"></a>

### codigo.movimento.fake_RPi.RPi.GPIO.setwarnings(avisos: [bool](https://docs.python.org/3/library/functions.html#bool))

Ativa ou desativas os avisos.

Essa função não implica em nada no módulo de simulação. Está disponível apenas para conveniência.

* **Parâmetros:**
  **avisos** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Se True, ativa os avisos. Se False, desativa os avisos.
