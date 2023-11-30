## Implementation

Nesta etapa foram implementados parte do hardware e software do sistema de telemetria, controle remoto, apresentação dos dados e receptor da telemetrai e do sistema de aruação remota propostos no conceive.

### Sistema de telemetria embarcada
 Este sistema proposto visa obter os dados, apresentar para o piloto, armazenar e transmitir remotamente para a equipe de monitoração.
 
##### Os sensores são apresentados a seguir com as etapas da implemetação descritas.

###### Sensores analógicos
 
1. Sensores de temperatura (bateria e controlador);
2. Sensor de Tensão;
3. Sensor de Corrente;
4. Sensor de aceleração;

Para implementação destes sensores utilizou-se o conversor AD interno ao microcontrolador. Para tanto algumas precauções devem ser tomadas, tais como instalar um sistema de proteção contra sobre-tensão, garantir uma tensão de referência estável,  filtrar os sinais analógicos e evitar ruidos. 

Para possibilitar maior velocidade e eficiencia na obtenção dos dados e manter o microcontrolador menos saturado com operações de aquisição, foi utilizado o recurso de Acesso Direto a Memória do microcopntrolador. A grosso modo isto permite que o conversor AD atualize o valor da variável diretamente na memória de modo que o CPU do microcontrolador não sofre atraso durante a conversão. 

Como são 5 senssores, são necessários 5 canais de AD:

| Sensor      | Canal | Posição do vetor|
| --------- |----------- |----|
| Temperatura do controlador  | 5 | 0 |
| Temperatura da bateria  | 6 | 1 |
| Tensão da bateria | 7 | 2 |
| Corrente de consumo  | 8 | 3 |
| Nível do acelerador | 9 | 4 |

O Conversor Alalógico digital foi utilizado em sua resolução máxima (12 bits) para obter maior precisão. 

###### Sensor Hall de rotação

Para leitura de rotação utilizando o sensor hall, faz-se necessário utilizar um Timer para obter o tempo entre cada borda de subida do sinal vindo do sensor. A cada rotação da roda, o sensor detecta e gera um sinal digital que possui transição uma vez a cada rotação. Essa transição possui um periodo e portanto uma frequencia. 

O protótipo terá uma velocidade entre 0 (parado) e 40km/h. Sua roda possui cerca de 1,6m de circunferência. Com essas informações podemos calcular o intervalo de rotação e de frequencias que precisaremos medir, isso para adequar a frequencia do Timer do microcontrolador e assim obter melhores resultados. 

Cáculo do intervalo de frequencia:

Velocidade máxima: 40km/h -> 40/3,6 m/s
(Velocidade em m/s)/circunferencia = frequencia
Assim obtemos uma frequencia de cerca de 7Hz. Então o intervalo será de 0,1 Hz e 7 Hz.

O erro obtido será de 0,1Hz * circunferencia = velocidade -> menor que 0,6km/h que é aceitavel para este sistema.

Para permitir a leitura do periodo neste intervalo, faz-se necessário utilizar divisor de frequencia bastante elevado, de modo que permita medir frequencias com precisão até 10Hz e resolução de 0,1Hz. Sendo assim, configuramos o Timer2 Canal 1 no modo Input Capture com Prescaler de 28800 e frequencia de 72Mhz. Assim o tempo de cada contagem será de 1/(72e+6/28800)=0.4ms. Sendo assim no pior caso que será em baixa frequencia, esta configuração não utilizará variáveis acima de 32bits e portanto evitará alto consumo de memória. 

##### Módulo GPS

O módulo GPS possui interface UART para comunicação e uma taxa de 9400bps. Então escolheu-se a interface UART2 para utilizar com o módulo GPS visto que não possui outros recursos conflitantes nestes pinos.

##### Módulo Cartão SD

O modulo de cartão SD utiliza interface SPI, e foi configurada para usar a SPI1 do microcontrolador, bem como o pino PA10 configurado como saída digital para a funcionalidade de chip-select.

##### Módulo transmissor Lora

Assim como o módulo de cartão SD o modulo transmissor Lora utiliza interface SPI, e foi configurada para usar a SPI1 do microcontrolador, bem como o pino PA11 configurado como saída digital para a funcionalidade de chip-select.

##### Módulo RTC

Para obter a data e hora exata da aquisição dos dados e informar ao piloto o tempo restate de corrida, o recurso de real Time Clock foi utilizado. Este recurso está presente no microcontrolador e necessita do cristal de baixa frequencia de 32,768kHz, este está presente na placa de desenvolvimento utilizada.


##### Display

Ao implementar o display Oled de 0,96" notou-se que o tamanho e quantidade de informações seria inviável. Sendo assim, será utilizado um display de 3,5" LCD do fabricante Nextion. Este display possui IDE com interface gráfica para a sua programação, e portanto agilizará o processo. 

A implementação do display está nas fases iniciais, mas viu-se que será possível apresentar npivel de bateria, tempo, velocidade, nível de aceleração.

### Receptor da Telemetria

O receptor utiliará o mesmo módulo sem fio lora e portanto compartilhará grande parte dos recursos implementados de hardware e software. 

Além disso a interface para leitura dos dados será UART que também foi desenvolvida para o GPS e display.

### Atuadores remotamente controlados

Para a implementaçõ dos controles do veículo, será usado básicamente servo motores e saídas digitais do microcontrolador, bem como receptor sem fio. Estes utilizam gpios e recurso de PWM que é facilmente configurável na IDE utilzada. O receptor utilizará interface SPI e novamente compartilhará vários sistemas já elaborados na telemtria embarcada.

### Controle remoto

O controle remoto contará com um transmissor sem fio igual ao sistema de atiação remota, e portanto a sua implementação será compartilhada. O controle contará com botões e potenciometros que já foram desenvolvidos em software nos outros sistemas, portanto sua implementação será rapida.
