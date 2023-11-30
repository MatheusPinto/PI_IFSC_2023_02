#!/bin/env python3


"""Módulo de controle dos motores.

Implementa duas classes:

* :class:`DC`: controla os motores DC por meio de uma ponte H L298N.
* :class:`Passo`: Controla os motores de passo.
"""


import RPi.GPIO as GPIO

"""Classe de controle dos motores DC.

Importante: Usa como referência a numeração da placa e não do GPIO
"""


def configura_GPIO(modo: str = "BOARD"):
    """Configura os pinos do Raspberry Pi.

    Parameters
    ----------
    modo : str
        O modo de numeração dos pinos. Pode ser 'BOARD' ou 'BCM'.
    """
    if modo ==  "BOARD":
        GPIO.setmode(GPIO.BOARD)
    else:
        GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)


class DC():
    """Classe de controle dos motores DC.

    Ao inicializar, deve-se fornecer o número das portas GPIO usadas para controlar o Driver de motor DC.

    É possível configurar a velocidade máxima de movimento dos motores por meio do método :meth:`velocidade_maxima()`.

    Para ajustar a velocidade dos motores, utilize os métodos :meth:`velocidade_motor_E()` e :meth:`velocidade_motor_D()`
    que controlam, respectivamente, a velocidade dos motores esquerdo e direito.
    """

    def __init__(self, IN1: int, IN2: int, IN3: int, IN4: int):
        """Configura as portas GPIO da Raspberry Pi que serão usadas para controlar o motor de passo.

        Os parâmetros IN1 até IN4 são os números das portas GPIO da Raspberry Pi usadas para controlar o driver L298N.

        Parameters
        ----------
        IN1 : int
            O número da porta GPIO que controla o motor esquerdo, sentido para frente.

        IN2 : int
            O número da porta GPIO que controla o motor esquerdo, sentido para trás.

        IN3: int
            O número da porta GPIO que controla o motor direito, sentido para frente

        IN4: int
            O número da porta GPIO que controla o motor direito, sentido para trás.
        """
        self._IN1 = IN1
        self._IN2 = IN2
        self._IN3 = IN3
        self._IN4 = IN4

        GPIO.setup(self._IN1, GPIO.OUT)
        GPIO.setup(self._IN2, GPIO.OUT)
        GPIO.setup(self._IN3, GPIO.OUT)
        GPIO.setup(self._IN4, GPIO.OUT)

        freq = 100
        self._pwm_IN1 = GPIO.PWM(self._IN1, freq)
        self._pwm_IN2 = GPIO.PWM(self._IN2, freq)
        self._pwm_IN3 = GPIO.PWM(self._IN3, freq)
        self._pwm_IN4 = GPIO.PWM(self._IN4, freq)

        self._pwm_IN1.start(0)
        self._pwm_IN2.start(0)
        self._pwm_IN3.start(0)
        self._pwm_IN4.start(0)


    def velocidade_motor_E(self, velocidade: float):
        """Ajusta a velocidade do motor esquerdo.

        O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
        100 significa velocidade máxima. Um valor negativo significa que deve se mover na direção
        contrária (para trás).

        Parameters
        ----------
        velocidade : float
            A velocidade do motor esquerdo.
        """
        self._velocidade_motor(self._pwm_IN1, self._pwm_IN2, velocidade)

    def velocidade_motor_D(self, velocidade: float):
        """Ajusta a velocidade do motor direito.

        O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
        100 significa velocidade máxima. Um valor negativo significa que deve se mover na direção
        contrária (para tráis).

        Parameters
        ----------
        velocidade : float
            A velocidade do motor direito.
        """
        self._velocidade_motor(self._pwm_IN3, self._pwm_IN4, velocidade)

    def _velocidade_motor(self, pwm1, pwm2, velocidade: float):
        """Ajusta a velocidade de motor do driver.

        Os pinos GPIO usados para controlar o motor devem ser fornecidos pelos parâmetros *pino1* e *pino2*.

        O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
        100 significa velocidade máxima. Um valor negativo significa que deve se move na direção
        contrária (para trás).

        Parameters
        ----------
        pwm1
            O pino GPIO que controla o motor, sentido para frente.

            O pino GPIO que controla o motor, sentido para trás.

        velocidade : float
            A velocidade do motor.
        """
        dutyDC = abs(velocidade)

        if velocidade > 0:
            pwm1.ChangeDutyCycle(dutyDC)
            pwm2.ChangeDutyCycle(0)
        elif velocidade < 0:
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(dutyDC)
        else:
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)

    def desliga(self):
        """Desliga os motores.

        Desativa os PWM que controlam a ponte H e libera as GPIO da Raspberry Pi utilizadas. O objeto se torna
        inútil depois disso.
        """
        self._pwm_IN1.stop()
        self._pwm_IN2.stop()
        self._pwm_IN3.stop()
        self._pwm_IN4.stop()


class Passo():
    """Classe de controle de um motor de passo.

    Ao inicializar, deve ser fornecido o pino GPIO usado para controlar o motor.

    A mudança de ângulo do motor de passo ocorre gradualmente. Ou sejá, ele não muda de 120° direto
    para 180°, mas sim em passos. O valor desses passos são configurados na inicialização do objeto.

    Para definir o ângulo do motor, use o método :meth:`define_angulo_destino()` e, para atualizar o ângulo
    do motor, use o método :meth:`atualiza_angulo()`. A atualização deve ser feita em intervalos de tempo de
    forma que não cause mudanças bruscas no ângulo do motor.

    Para verificar os ãngulos relacionados ao motor de passo, há dois métodos:

    * retorna_angulo_atual(): retorna o ângulo atual do motor de passo
    * retorna_angulo_destino(): retorna o ângulo para qual o motor de passo está se direcionando
    """

    def __init__(self, pino: int, passos: float):
        """Configura o motor de passo.

        Deve ser fornecido o número do *pino* usado para controlar o motor de passo. E o número de passos
        que serão somados quando o ângulo do motor for atualizado.

        Os *passos* são informados em graus. Por exemplo, se passos=3, então sempre que o motor de passo
        for atualizado pelo método :meth:`atualiza_angulo()` será somado 3 graus ao ângulo atual, até alcançar
        o ângulo de destino definido por :meth:`define_angulo_destino()`.

        Parameters
        ----------
        pino : int
            O pino GPIO que controla o motor de passo.

        angulo_inicial : float
            O ángulo inicial do motor de passo.

        passos : float
            O número de passos que serão somados quando o ángulo do motor for atualizado.
        """
        # Informações do motor de passo
        self._passos = passos/36
        self._pino = pino

        # PWm
        GPIO.setup(self._pino, GPIO.OUT)
        self._pwm = GPIO.PWM(self._pino, 50)

    def retorna_angulo_atual(self):
        """Retorna o ângulo atual do motor de passo.

        É importante notar que, como o ângulo do motor de passo varia gradualmente, o valor retornado por esse
        método não obrigatóriamente será o definido ao usar o método :meth:`define_angulo_destino()`. O ângulo atual
        se ajustará gradualmente até chegar ao ângulo configurado por esse método.

        Se deseja ler o ângulo selecionado por :meth:`define_angulo_destino()`, use o método :meth:`retorna_angulo_destino()`.

        O ângulo é retornado em graus.

        Returns
        -------
        float
            O ángulo atual do motor de passo.
        """
        return self._converte_duty_para_graus(self._duty_atual)  # de 5 a 10% duty, zero o atual e tenho 180.

    def retorna_angulo_destino(self):
        """Retorna o ângulo de destino do motor de passo.

        Por exemplo, se foi usado a função :meth:`define_angulo_destino()` para defineir 120°. Essa função retorna 120.

        O ângulo é retornado em graus.

        Returns
        -------
        float
            O ángulo de destino do motor de passo.
        """
        return self._converte_duty_para_graus(self._duty_destino)

    def define_angulo_destino(self, angulo: float):
        """Define o ângulo de destino do motor de passo.

        O ângulo atual do motor de passo se ajustará aos poucos até alcançar o valor definido pelo parãmetro *angulo*.
        Para realizar uma atualização, use o método :meth:`atualiza_angulo()`

        O ângulo é informado em graus.

        Returns
        -------
        float
            O ángulo de destino do motor de passo.
        """
        self._duty_destino = self._converte_graus_para_duty(angulo)

        # 0,05 á 0,1

    def inicia(self, angulo):
        """Inicia o motor de passo."""
        # Angulo inicial do motor de passo
        self._duty_atual = self._converte_graus_para_duty(angulo)
        self._duty_destino = self._duty_atual

        self._pwm.start(self._duty_atual)

    def atualiza_angulo(self):
        """Atualiza o angulo atual do motor.

        O angulo do motor se ajustará gradualmente até alcançar o valor do ângulo de destino. Esse método atualiza
        o passo definido na instaciação da classe.

        O ângulo de destino é definido pelo método :meth:`define_angulo_destino()`. A atualização ocorre em
        passos definidos pelo parâmetro *passos* do método de inicialização da classe.
        """
        if self._duty_atual < self._duty_destino:
            self._duty_atual = self._duty_atual + self._passos

            if self._duty_atual > self._duty_destino:
                self._duty_atual = self._duty_destino

        elif self._duty_atual > self._duty_destino:
            self._duty_atual = self._duty_atual - self._passos

            if self._duty_atual < self._duty_destino:
                self._duty_atual = self._duty_destino

        self._pwm.ChangeDutyCycle(self._duty_atual)

    def desliga(self):
        """Desliga o motore de passo.

        Desativa os PWM que controlam os motor e libera a GPIO da Raspberry Pi utilizada. O objeto se torna
        inútil depois disso.
        """
        self._pwm.stop()

    def _converte_graus_para_duty(self, angulo: float):
        """Converte o ângulo em graus para o duty cycle do PWM usado pelo motor SG90.

        Parameters
        ----------
        angulo : float
            O angulo em graus.
        """
        return (angulo/36 + 5)

    def _converte_duty_para_graus(self, duty_cycle: float):
        """Converte o duty cycle do PWM usado pelo motor SG90 para o angulo em graus.

        Parameters
        ----------
        duty_cycle : float
            O duty cycle do PWM.
        """
        return (duty_cycle - 5)*36
