#!/bin/env python3


"""Módulo de controle do Wall-e.

Implementa a classe :class:`Movimento` que permite controlar a movimentação do Wall-e em alto nível.
Basta fornecer a velocidade linear e angular.
"""


from .motores import DC, Passo, configura_GPIO
import RPi.GPIO as GPIO
import time


class Movimento():
    """Controlador do movimento do Wall-e.

    Controla e gerencia os motores que movimentam o Wall-e:

    * 2 motores DC, por meio de uma ponte H.
    * 3 motores de passo.

    Além disso, controla um buzzer ativo em nível lógico baixo, usado para sinalização de lixo.

    Para definir a velocidade, use o método :meth:`define_velocidade()`.

    Para indicar que o Wall-e encontrou um lixo, use o método :meth:`sinaliza_lixo()`.
    """

    def __init__(self, pinos_driver_DC: tuple, pinos_motor_passo: tuple, pino_buzzer: int, modo_GPIO: str = "BCM"):
        """Configura os motores usados na movimentação do Wall-e, e o buzzer.

        Configura os motores DC (ponte H) e os motores de passo usados. Deve ser fornecido um vetor com os
        pinos GPIO do motor DC, e outro com os pinos GPIO dos motores de passo. Além disso, é necessário
        informardo pino GPIO do buzzer para configurar o buzzer.

        Parameters
        ----------
        pinos_driver_DC : tuple
            Os pinos GPIO do motor DC. Deve estar no formato (IN1, IN2, IN3, IN4). Observe o método
            :meth:`~codigo.movimento.modulos.motores.DC.__init__()` da classe :class:`~codigo.movimento.modulos.motores.DC`
            para mais informações.

        pinos_motor_passo : tuple
            Os pinos GPIO dos motores de passo. Cada elemento corresponde a um pino usado para controlar um
            motor de passo. Deve estar no formato (pino1, pino2, pino3). Em que, pino1 e pino2 são os usados
            para controlar os braços direito e esquerdo, respectivamente; e pino3 é usado para controlar o pescoço.

        pino_buzzer : int
            O pino GPIO do buzzer.

        modo_GPIO : str
            O modo de configuração dos pinos GPIO. Pode ser "BCM" ou "BOARD".
        """
        # Atributos
        self._sinaliza_lixo = False

        # Modo do GPIO
        configura_GPIO(modo_GPIO)

        # Buzzer
        self._pino_buzzer = pino_buzzer
        GPIO.setup(self._pino_buzzer, GPIO.OUT)
        GPIO.output(self._pino_buzzer, GPIO.HIGH)

        # DC
        self._DC = DC(pinos_driver_DC[0], pinos_driver_DC[1], pinos_driver_DC[2], pinos_driver_DC[3])

        # Motores de passo
        self._pino_passo1 = pinos_motor_passo[0]
        self._pino_passo2 = pinos_motor_passo[1]
        self._pino_passo3 = pinos_motor_passo[2]

        passos = 10
        self._passo1 = Passo(self._pino_passo1, passos)
        self._passo2 = Passo(self._pino_passo2, passos)
        self._passo3 = Passo(self._pino_passo3, passos)

    def define_velocidade(self, velocidade_linear: float, velocidade_angular: float):
        """Define a velocidade linear e angular de movimento do Wall-e.

        O valor de *velocidade_linear* é um número de -100 a 100. Se receber 0, significa que a velocidade
        linear é nula, 100 significa velocidade máxima para frente. Um valor negativo significa que deve se
        mover na direção contrária (para trás).

        O valor de *velocidade_angular* é um número de -100 a 100. Se receber -100, significa que o motor deve
        se mover o máximo possível no sentido horário (visualizando de cima para baixo). 100 significa o máximo
        possível no sentido anti-horário (visualizando de cima para baixo).

        Parameters
        ----------
        velocidade_linear : float
            A velocidade linear de movimento do Wall-e.

        velocidade_angular : float
            A velocidade angular de movimento do Wall-e.
        """
        # Não ajusta velocidade se estiver sinalizando lixo
        if self._sinaliza_lixo:
            return

        # Caso PWM maior seja maior que 100, precisa-se normalizar os duty-cycles, para não utrapassar o limite de 100%.
        mod_vel = abs(velocidade_linear) + abs(velocidade_angular)
        if mod_vel > 100:
            velocidade_linear = velocidade_linear/mod_vel * 99.99999
            velocidade_angular = velocidade_angular/mod_vel * 99.9999

        #cinemática do motor (direito e esquerdo)
        pe = velocidade_linear - velocidade_angular
        pd = velocidade_linear + velocidade_angular

        self._DC.velocidade_motor_D(pd)
        self._DC.velocidade_motor_E(pe)


    def sinaliza_lixo(self):
        """Executa a sinalização de que detectou um lixo.

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
        """
        # Nao ajusta velocidade se já estiver sinalizando lixo
        if self._sinaliza_lixo:
            return

        # Marca que encontrou lixo para não poder mais ajustar as velocidades
        self._sinaliza_lixo = True

        # Velocidade zero quando wall-e encontrar lixo
        self._DC.velocidade_motor_D(0)
        self._DC.velocidade_motor_E(0)

        # Liga o buzzer (nível lógico baixo)
        GPIO.output(self._pino_buzzer, GPIO.LOW)

        # Motores de passo
        self._passo1.inicia(0)
        self._passo2.inicia(90)
        self._passo3.inicia(0)

        # Manda para posição inicial
        self._ajusta_motores_sinalizacao(180, 0, 180)
        self._ajusta_motores_sinalizacao(0, 180, 0)
        self._ajusta_motores_sinalizacao(0, 90, 0)

        # Desliga o buzzer (nível lógico alto)
        GPIO.output(self._pino_buzzer, GPIO.HIGH)

        # Desliga os motores de passo
        self._passo1.desliga()
        self._passo2.desliga()
        self._passo3.desliga()

        # Não está mais identificando lixo, pode mover novamente
        self._sinaliza_lixo = False

    def _ajusta_motores_sinalizacao(self, angulo1 : float, angulo2 : float, angulo3 : float):
        """

        Parameters
        ----------
        angulo1 : float
            O angulo do primeiro motor de passo.

        angulo2 : float
            O angulo do segundo motor de passo.

        angulo3 : float
            O angulo do terceiro motor de passo.
        """

        # Define o angulo de destino para cada um dos servos motores
        self._passo1.define_angulo_destino(angulo1)
        self._passo2.define_angulo_destino(angulo2)
        self._passo3.define_angulo_destino(angulo3)

        # Determina o passo em graus da movimentação dos motores
        for loop in range(0, 18):
            self._passo1.atualiza_angulo()
            self._passo2.atualiza_angulo()
            self._passo3.atualiza_angulo()

            time.sleep(0.1)
