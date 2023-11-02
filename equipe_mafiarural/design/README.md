<!-- PROJECT LOGO -->
<div align="center">
  <h3 align="center">Sistema de Monitoramento de Vazamento de Gás de Cozinha</h3>

  <p align="center">
    <strong>(Design)</strong>
    <br />
</div>

## Índice

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introdução">Introdução</a>
    </li>
    <li>
      <a href="#esquemático-de-funcionamento">Esquemático de Funcionamento</a>
      <ul>
        <li><a href="#módulo-central">Módulo Central</a></li>
        <li><a href="#módulo-de-sensoriamento">Módulo de Sensoriamento</a></li>
      </ul>
    </li>
    <li>
      <a href="#layout-da-placa-de-circuito-impresso">Layout da Placa de Circuito Impresso</a>
      <ul>
        <li><a href="#módulo-central-1">Módulo Central</a></li>
        <li><a href="#módulo-de-sensoriamento-1">Módulo de Sensoriamento</a></li>
      </ul>
    </li>
    <li>
      <a href="#modelo-3d-do-sistema">Modelo 3D do Sistema</a>
    </li>
    <li>
      <a href="#software">Software</a>
    </li>
  </ol>
</details>

---

## Introdução

Este documento detalha o design do projeto de um sistema de monitoramento de vazamento de gás de cozinha. O sistema será composto por um módulo central e dois módulos de sensoriamento.


## Esquemático de Funcionamento

O esquemático abaixo ilustra como funcionará a lógica do sistema. No caso deste projeto, serão utilizados apenas dois sensores que estarão conectados à central via rede, que por sua vez transmitirá os logs de monitoramento para o servidor ThingSpeak. 

<div style="display: flex; width: 100%; align-items: center; justify-content: space-around; gap: 20px;">

<img src="./resources/diagrama.png" alt="Esquemático de Funcionamento" height="300px"/>

</div>
<br />

### Módulo Central


<img src="./hardware/central/imgs/root.png" alt="Esquemático Central" height="300px"/>
<img src="./hardware/central/imgs/fonte-elevador.png" alt="Esquemático Central" height="300px"/>
<img src="./hardware/central/imgs/esp.png" alt="Esquemático Central" height="300px"/>

<br />

### Módulo de Sensoriamento


<img src="./hardware/sensor/imgs/root.png" alt="Esquemático Sensoriamento" height="300px"/>
<img src="./hardware/sensor/imgs/sensors.png" alt="Esquemático Sensoriamento" height="300px"/>
<img src="./hardware/sensor/imgs/elevador.png" alt="Esquemático Sensoriamento" height="300px"/>
<img src="./hardware/sensor/imgs/esp.png" alt="Esquemático Sensoriamento" height="300px"/>

<br />

## Layout da Placa de Circuito Impresso

### Módulo Central

O módulo central terá entrada de 5 -12V e estará posicionada dentro do quadro de distribuição da residência. Para fazer o controle será utilizado um módulo de relés. Para o mantimento da alimentação após o corte de energia haverá uma célula Li-ion de 3.7V, sendo possível a expansão em paralelo para aumentar a capacidade de armazenamento.

<img src="./hardware/central/imgs/layout.png" alt="PCB Central" height="300px"/>
<img src="./hardware/central/imgs/preview-top.png" alt="PCB Central" height="300px"/>
<img src="./hardware/central/imgs/preview-bottom.png" alt="PCB Central" height="300px"/>

<br />


### Módulo de Sensoriamento

O módulo de sensoriamento terá entrada de 5V via microUSB. Para o mantimento da alimentação após o corte de energia haverá uma célula Li-ion de 3.7V, sendo possível a expansão em paralelo para aumentar a capacidade de armazenamento.


<img src="./hardware/sensor/imgs/layout.png" alt="PCB Sensor" height="300px"/>
<img src="./hardware/sensor/imgs/preview-top.png" alt="PCB Sensor" height="300px"/>
<img src="./hardware/sensor/imgs/preview-bottom.png" alt="PCB Sensor" height="300px"/>

<br />


## Modelo 3D do Sistema

Os sensores tem a principal qualidade de possibilitar a opção de o próprio usuário alocar sua posição. O recomendado é o mais próximo possível do chão e da potencial fonte de vazamento, considerando a densidade dos gases que desejamos detectar. No modelo abaixo, há dois sensores: Um posicionado logo ao lado da geladeira e outro acima da pia. A case ilustrada no modelo é apenas ilustrativa, não sendo a versão final do produto. A versão final da case estará disponível após testes com a placa e decisão final de componentes e periféricos.


<img src="./resources/cozinha.png" alt="Cozinha" height="300px"/>

<br />

## Software

A parte de monitoramento de logs e emissão de notificação será feita pelo servidor ThingSpeak. O código para o ESP32 será desenvolvido em C/C++ na IDE do Arduino. Como EXTRA, há a possibilidade de armazenar os comandos de controle em um cartão SD no módulo central, para que seja possível a atuação do sistema em caso de falha de conexão com a internet.