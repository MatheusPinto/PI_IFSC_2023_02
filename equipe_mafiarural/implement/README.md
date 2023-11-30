<!-- PROJECT LOGO -->
<div align="center">
  <h3 align="center">Sistema de Monitoramento de Vazamento de Gás de Cozinha</h3>

  <p align="center">
    <strong>(Implementação)</strong>
    <br />
</div>

## Introdução

Este documento detalha a implementação do projeto de um sistema de monitoramento de vazamento de gás de cozinha. O sistema será composto por um módulo central e módulos de sensoriamento. Na implementação atual, foi feito a implementação de um módulo central e um módulo de sensoriamento.

## Módulo Central

O módulo central é responsável por receber os dados dos módulos de sensoriamento e transmitir os logs de monitoramento para o servidor responsável por realizar a coleta e análise dos dados. O módulo central é composto por um microcontrolador ESP32, com acesso à rede WiFi, e com extensão para se conectar a uma matriz de relés de 8 canais e uma interface para cartão microSD para armaenamento dos logs de monitoramento.

### Da implementação da placa de circuito impresso

#### Placa de circuito impresso Kicad

<img src="./docs/central/circuit/preview-top.png" alt="PCB central" height="300px"/>
<img src="./docs/central/circuit/preview-bottom.png" alt="PCB central" height="300px"/>

#### Placa de circuito impresso fabricada e montada

<img src="./docs/central/circuit/central_bot.jpg" alt="PCB central" height="300px"/>
<img src="./docs/central/circuit/central_top_raw.jpg" alt="PCB central" height="300px"/>
<img src="./docs/central/circuit/central_top.jpg" alt="PCB central" height="300px"/>

#### Bloco de relés e fonte externa

<img src="./docs/central/relay_matrix.jpg" height="300px"/>

<img src="./docs/central/external_supply.jpg" height="300px"/>

#### Das baterias utilizadas

A priori a equipe utilizou uma única célula de bateria de lítio de 3.7V convencional porém esta não performou de forma boa, não sendo capaz de fornecer energia suficiente para o módulo central.

##### Célula de bateria de lítio de 3.7V convencional utilizada no primeiro protótipo

<img src="./docs/batteries/prototype.jpg" height="300px"/>

Apó s a análise do primeiro protótipo, a equipe optou por utilizar uma bateria de lítio de 3.7V de alta capacidade, a bateria foi retirada de um banco de baterias de um notebook dell vostro 5470 que estava inutilizado, a bateria deste notebook é composta de 3 células de bateria de lítio, central é composta de 2 células de bateria de lítio em paralelo, aumentando a capacidade da bateria.

##### Bateria de lítio de 3.7V de alta capacidade utilizada no segundo protótipo

<img src="./docs/batteries/central.jpg" height="300px"/>

##### Realização de carga externa da bateria para testes

Para os primeiros testes foi utilizado um carregador externo para averiguar se as baterias estavam funcionando corretamente e para reduzir tempo de carga usando o carregador integrado dos módulos.

<img src="./docs/batteries/external_charging.jpg" height="300px"/>

### Setor de status

O setor de status é responsável por fornecer informações sobre o estado do módulo central, o setor de status é composto por 3 leds, um led vermelho e 2 leds verdes. Estes leds possuem propósito geral e estão conectados a GPIOs do microcontrolador ESP32.

<img src="./docs/central/circuit/status.png" height="300px"/>

### Setor de controle

O setor de controle é responsável por acionar os relés da matriz de relés, o setor de controle é composto por simples 8 pinos GPIO do microcontrolador ESP32 que são conectados a matriz de relés.


<img src="./docs/central/circuit/control_bot.png" height="300px"/>

<img src="./docs/central/circuit/control_top.png" height="300px"/>

### Setor MicroSD

O setor MicroSD é responsável por fornecer uma interface para cartão microSD para armazenamento dos logs de monitoramento, o setor MicroSD é composto por uma interface para cartão microSD e microcontrolador ESP32 usando o SPI do microcontrolador ESP32.

#### MicroSD shield utilizado

<img src="./docs/central/circuit/micro_sd.jpg" height="300px"/>

#### Interface para cartão microSD

<img src="./docs/central/circuit/micro_bot.png" height="300px"/>
<img src="./docs/central/circuit/micro_top.png" height="300px"/>

### Setor de alimentação

O setor de alimentação é responsável por fornecer energia para o módulo central. O módulo central é alimentado por uma fonte externa conectada a rede 110~220Vac que realiza a conversão para uma tensão 6.5~12Vdc, a tensão da fonte externa por sua vez é regulada para 5V por um regulador de tensão LM7805. A tensão de 5V é utilizada para alimentar o microcontrolador ESP32 e a matriz de relé bem como a tensão de 5V também é utilizada para alimentar o módulo de carga / descarga de bateria baseado na implementação do módulo 134n3p que por sua vez realiza a carga da bateria quando a fonte externa está ativa e a descarga da bateria quando a fonte externa está inativa, mantendo assim a alimentação do módulo central mesmo quando a fonte externa está inativa.


#### Caminho da energia no módulo central

<img src="./docs/central/circuit/energy_path.png">

O caminho da energia do módulo se resume em:
* Fonte externa ligada, nesse cenário a tensão regulada de 5V é fornecida para o módulo central e para o módulo de carga / descarga de bateria que por sua vez carrega a bateria, assim o módulo central é alimentado pela fonte externa e regulado pelo LM7805.
* Fonte externa desligada, nesse cenário por não haver tensão regulada no LM7805, o módulo de carga / descarga de bateria realiza a descarga e elevação da tensão da bateria de 3.7V para 5V, assim o módulo central é alimentado pela bateria.

#### Classificações máximas e determinações de cenários de falha por sobrecarga

Primeiramente, não foi realizado uma análise aprofundada do consumo do módulo central por requerir uma análise profunda de todos os aspectos, porém uma estimativa foi realizada para estipular a carga máxima requerida pelo módulo central.

A estimativa se baseia na análise dos seguintes pontos:
* O microcontrolador ESP32 possui uma corrente máxima de 250mA (Desconsiderando cenário de scan de rede WiFi que segundo fórums e datasheet pode atingir até 0.7A por um período de 10ms), esse dado foi extraído de fóruns e datasheet do microcontrolador considerando um cenário ativo de transmissão de dados via WiFi, segundo os fórums, o consumo médio do microcontrolador é de 80mA em tempo ocioso / em não transmissão de dados via WiFi.
* O consumo médio de um relé (**SRD-05VDC-SL-C**) é de 72mA, esse dado foi extraído de datasheet de relés de 5V. Dado que o módulo de relés é composto por 8 relés, o consumo total do módulo de relés é de 576mA.
  * <img src="./docs/datasheet/relay_general.png">
  * <img src="./docs/datasheet/relay_consumption.png">
* O consumo do módulo de carga / descarga de bateria consegue atingir até 1A em caso de carga máxima, bateria em tensão minima.
  * <img src="./docs/datasheet/bat_max.png">

Assim sendo a estimativa de consumo máxima do módulo central é de 1.8A, considerando o cenário de carga máxima quando a fonte externa está ativa e um consumo médio de 0.8A quando a fonte externa está inativa e o módulo de carga / descarga de bateria está ativo.

Estresses aplicados no regulador de tensão LM7805 são:
* Tensão de entrada: 6.5~12Vdc
* Tensão de saída: 5Vdc
* Corrente máxima: 1.8A

Estresses aplicados no módulo de carga / descarga de bateria são:
* Tensão de entrada: 3.7~5Vdc
* Tenso de saída: 5Vdc
* Corrente máxima: 0.8A

#### Análise de dissipação de calor no LM7805

Primeiramente calculando os estresses aplicados no LM7805 utilizando carga máxima 1.8A com os cenários de estresse minimo, entrada em 6.5V e saída em 5V e estresse máximo, entrada em 12V e saída em 5V.

* Estresse mínimo:

$$
P = (V_{in} - V_{out}) \times I_{out} \\
P = (6.5 - 5) \times 1.8 \\
P = 2.7W
$$

* Estresse máximo:

$$
P = (V_{in} - V_{out}) \times I_{out} \\
P = (12 - 5) \times 1.8 \\
P = 12.6W
$$

Calculando a resistencia térmica total da junção / ambiente para ambos os estresses, utilizando as classificações máximas do LM7805.

<img src="./docs/datasheet/lm7905_max.png">

* Estresse mínimo:

$$
R_{th} = \frac{T_{j(max)} - T_{a}}{P_{d(max)}} \\
R_{th} = \frac{125 - 25}{2.7} \\
R_{th} = 30.37 \frac{^{\circ}C}{W}
$$

* Estresse máximo:

$$
R_{th} = \frac{T_{j(max)} - T_{a}}{P_{d(max)}} \\
R_{th} = \frac{125 - 25}{12.6} \\
R_{th} = 7.93 \frac{^{\circ}C}{W}
$$

Dado que a seguinte condição é válida:

$$
\theta_{jc} < R_{th} < \theta_{ja}
$$

É necessário a utilização de dissipadores de calor para ambos os estresses, porém deve-se considerar que o estresse máximo é o mais crítico, assim sendo, o dissipador de calor deve ser dimensionado para o estresse máximo.

$$
\theta_{SA} = \theta_{ja} - R_{th} \\
\theta_{SA} = 7.93 - 5 \\
\theta_{SA} = 2.93 \frac{^{\circ}C}{W}
$$

Como pode ser visto, a dissipação no ceário de estresse máximo é alta, assim a equipe optou por utilizar uma fonte de 6.5V para reduzir a dissipação de calor no regulador de tensão LM7805.

### Do case do módulo central

....

#### Projeto 3D do case do módulo central no software de modelagem Blender

....

#### Projeto 3D do case do módulo central no software Cura3D para fatiamento

....

#### Case do módulo central em completo

....

#### Módulo central completamente montado

....

#### Software do módulo central

....


## Módulo Sensor

O módulo sensor é responsável por realizar o sensoriamento dos vazamentos de diversos gases, o módulo sensor é composto por um microcontrolador ESP32, com acesso ao módulo central utilizando protocolo ESP-NOW, e com conexão a 3 sensores de gases, sendo estes 1xMQ-5, 1xMQ-6 e 1xMQ-7.

### Da implementação da placa de circuito impresso

#### Placa de circuito impresso Kicad

<img src="./docs/sensor/circuit/preview-top.png" alt="PCB Sensor" height="300px"/>
<img src="./docs/sensor/circuit/preview-bottom.png" alt="PCB Sensor" height="300px"/>

#### Placa de circuito impresso fabricada e montada

<img src="./docs/sensor/circuit/sensor_bot.jpg" alt="PCB Sensor" height="300px"/>
<img src="./docs/sensor/circuit/sensor_top_raw.jpg" alt="PCB Sensor" height="300px"/>
<img src="./docs/sensor/circuit/sensor_top.jpg" alt="PCB Sensor" height="300px"/>

#### Shields MQ usadas e fonte externa

Os sensores foram adquiridos em forma de shields, por ser fácil de encontrar estes, porém a equipe realizou a desmontagem dos shields e soldagem dos sensores diretamente na placa de circuito impresso do módulo sensor.

##### Sensores MQ shield

<img src="./docs/sensor/mqs.jpg" height="300px"/>

#### Quanto a fonte externa para alimentação do módulo sensor

O módulo sensor é alimentado por um carregador de celular de 5V comum, única nota é o fata de o conector utilizado na placa se tratar de um conector micro USB por ser difil a soldagem de conectores USB-C modernos sem métodos avançados de soldagem. Assim cabos de carregadores de celular com conector micro USB são utilizados para alimentar o módulo sensor.

<img src="./docs/sensor/charger.jpg" height="300px"/>

<img src="./docs/sensor/usb.jpg" height="300px"/>

#### Das baterias utilizadas

A priori, assim como na central, a equipe utilizou uma única célula de bateria de lítio de 3.7V convencional porém esta não performou de forma boa, não sendo capaz de fornecer energia suficiente para o módulo de sensor, principalmente devido ao alto consumo dos sensores, de aproximadamente 650mW por sensor utilizado no elemento de aquecimento destes.

##### Célula de bateria de lítio de 3.7V convencional utilizada no primeiro protótipo

<img src="./docs/batteries/prototype.jpg" alt="PCB Sensor" height="300px"/>

Apó s a análise do primeiro protótipo, a equipe optou por utilizar uma bateria de lítio de 3.7V de alta capacidade, assim como no módulo central, a bateria foi retirada de um banco de baterias de um notebook dell vostro 5470 que estava inutilizado, a bateria deste notebook é composta de 3 células de bateria de lítio, a do sensor é composta de 1 célula da bateria de lítio.

##### Bateria de lítio de 3.7V de alta capacidade utilizada no segundo protótipo

<img src="./docs/batteries/sensor.jpg" alt="PCB Sensor" height="300px"/>

### Setor de status

Assim como no módulo central, o setor de status é responsável por fornecer informações sobre o estado do módulo central, o setor de status é composto por 3 leds, um led vermelho e 2 leds verdes. Estes leds possuem propósito geral e estão conectados a GPIOs do microcontrolador ESP32.

<img src="./docs/sensor/circuit/status.png" height="300px"/>

### Setor de sensoriamento

O setor de sensoriamento é responsável por realizar o tratamento da tensão de saída dos sensores e transmitir esses valores para o ADC do microcontrolador ESP32, o setor de sensoriamento é composto por 3 sensores de gases, sendo estes 1xMQ-5, 1xMQ-6 e 1xMQ-7, além disso possui um divisor de tensão para permitir o ajuste para o range de tensão de entrada do ADC do microcontrolador ESP32 e um filtro para reduzir ruídos na tensão de saída dos sensores. Além disso possui uma resistência série com o elemento de aquecimento dos sensores para limitar a corrente de aquecimento dos sensores e evitar sobrecarga no módulo de carga / descarga de bateria responsável por alimentar o módulo sensor.

<img src="./docs/sensor/circuit/sensing_top.png" height="300px"/>

<img src="./docs/sensor/circuit/sensing_bot.png" height="300px"/>

### Setor de alimentação

O setor de alimentação é responsável por fornecer energia para o módulo sensor. Ao contrário do módulo central, o módulo sensor utiliza uma entrada externa ja regulada de 5V usando um carregador de celular em sua micro USB, a tensão de 5V é utilizada para alimentar o microcontrolador ESP32, os sensores e também é utilizada para alimentar o módulo de carga / descarga de bateria baseado na implementação do módulo 134n3p que por sua vez realiza a carga da bateria quando o carregador externo está ativo e a descarga da bateria quando o carregador externo está inativo, mantendo assim a alimentação do módulo sensor mesmo quando o carregador externo está inativo.

#### Caminho da energia no módulo central

<img src="./docs/sensor/circuit/energy_path.png">

O caminho da energia do módulo se resume em:
* Carregador conectado, nesse cenário a tensão de 5V é fornecida para o módulo sensor e para o módulo de carga / descarga de bateria que por sua vez carrega a bateria, assim o módulo central é alimentado pelo carregador externo.
* Carregador desconectado, nesse cenário por não haver tensão de entrada na placa, o módulo de carga / descarga de bateria realiza a descarga e elevação da tensão da bateria de 3.7V para 5V, assim o módulo sensor é alimentado pela bateria.

#### Classificações máximas e determinações de cenários de falha por sobrecarga

Primeiramente, não foi realizado uma análise aprofundada do consumo do módulo sensor por requerir uma análise profunda de todos os aspectos, porém uma estimativa foi realizada para estipular a carga máxima requerida pelo módulo central.

A estimativa se baseia na análise dos seguintes pontos:
* O microcontrolador ESP32 possui uma corrente máxima de 250mA (Desconsiderando cenário de scan de rede WiFi que segundo fórums e datasheet pode atingir até 0.7A por um período de 10ms), esse dado foi extraído de fóruns e datasheet do microcontrolador considerando um cenário ativo de transmissão de dados via WiFi, segundo os fórums, o consumo médio do microcontrolador é de 80mA em tempo ocioso / em não transmissão de dados via WiFi.
* O consumo médio de cada sensor é basicamente a potencia dissipada em seu elemento de aquecimento, assim sendo o consumo médio de cada sensor é de 650mW ou seja 130mA por sensor e um total de 390mA para os 3 sensores.
* O consumo do módulo de carga / descarga de bateria pode ser desconsiderado aqui pois assume-se que o carregador será capaz de alimentar o módulo e fazer as regulações necessárias para manter-se em suas classificações máximas.

Assim sendo a estimativa de consumo máxima do módulo central é de 650mA, considerando o cenário de carga máxima, quando o módulo está totalmente sendo alimentado pela bateria apenas.

Estresses aplicados no módulo de carga / descarga de bateria são:
* Tensão de entrada: 3.7~5Vdc
* Tenso de saída: 5Vdc
* Corrente máxima: 0.65A

Por os valores estarem dentro do suportado pelo módulo de carga / descarga de bateria, não é necessário a utilização de dissipadores de calor.

### Do case do módulo sensor

O case do módulo sensor foi projetado para ser impresso em 3D, o case é composto por 2 partes, uma parte superior e uma parte inferior, a parte superior é responsável por proteger os sensores e a parte inferior é responsável por proteger o módulo de carga / descarga de bateria e o microcontrolador ESP32.

#### Projeto 3D do case do módulo sensor no software de modelagem Blender

<img src="./docs/sensor/case/blender1.png">

<img src="./docs/sensor/case/blender2.png">

<img src="./docs/sensor/case/blender3.png">

#### Projeto 3D do case do módulo sensor no software Cura3D para fatiamento

<img src="./docs/sensor/case/slice.png">

#### Case do módulo sensor em impressão 3D

<img src="./docs/sensor/case/3d_printing1.jpg" height="300px">

<img src="./docs/sensor/case/3d_printing2.jpg" height="300px">


