#!/bin/env python3


"""Módulo de controle dos motores.

Implementa duas classes:

* :class:`DC`: controla os motores DC por meio de uma ponte H L298N.
* :class:`Servo`: controla os servo motores.
"""


import RPi.GPIO as GPIO


def configura_GPIO(modo: str = "BOARD"):
    """Configura os pinos do Raspberry Pi.

    Configura o modo de numeração dos pinos. Se utilizado 'BOARD', os pinos se referem aos pinos da área
    placa, e não ao número da GPIO. Se utilizado 'BCM', os pinos se referem aos números da GPIO, e não aos pinos
    da placa.

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

    Para ajustar a velocidade dos motores, utilize os métodos :meth:`velocidade_motor_E()` e :meth:`velocidade_motor_D()`
    que controlam, respectivamente, a velocidade dos motores esquerdo e direito.
    """

    def __init__(self, IN1: int, IN2: int, IN3: int, IN4: int):
        """Configura as portas GPIO da Raspberry Pi que serão usadas para controlar o motor de DC.

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
        contrária (para trás).

        Parameters
        ----------
        velocidade : float
            A velocidade do motor direito.
        """
        self._velocidade_motor(self._pwm_IN3, self._pwm_IN4, velocidade)

    def _velocidade_motor(self, pwm1, pwm2, velocidade: float):
        """Ajusta a velocidade de motor do driver.

        Os PWM usados para controlar o motor devem ser fornecidos pelos parâmetros *pwm1* e *pwm2*.

        O valor de *velocidade* é um número de -100 a 100. Se receber 0, significa que o motor deve parar,
        100 significa velocidade máxima. Um valor negativo significa que deve se move na direção
        contrária (para trás).

        Parameters
        ----------
        pwm1 : GPIO.PWM
            O PWM que controla o motor esquerdo.

        pwm2 : GPIO.PWM
            O PWM que controla o motor direito.

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


class Servo():
    """Classe de controle de um servo motor SG90.

    Ao inicializar, deve ser fornecido o pino GPIO usado para controlar o motor.

    A mudança de ângulo do servo motor ocorre gradualmente. Ou sejá, ele não muda de 120° direto
    para 180°, mas sim em passos. O valor desses passos são configurados na inicialização do objeto.

    Para definir o ângulo do motor, use o método :meth:`define_angulo_destino()` e, para atualizar o ângulo
    do motor, use o método :meth:`atualiza_angulo()`. A atualização deve ser feita em intervalos de tempo de
    forma que não cause mudanças bruscas no ângulo do motor.

    Para verificar os ângulos relacionados ao servo motor, há dois métodos:

    * retorna_angulo_atual(): retorna o ângulo atual do servo motor.
    * retorna_angulo_destino(): retorna o ângulo para qual o servo motor está se direcionando.
    """

    def __init__(self, pino: int, passos: float):
        """Configura o servo motor.

        Deve ser fornecido o número do *pino* usado para controlar o servo motor. E o número de passos
        que serão somados quando o ângulo do motor for atualizado.

        Os *passos* são informados em graus. Por exemplo, se passos=3, então sempre que o servo motor
        for atualizado pelo método :meth:`atualiza_angulo()` será somado 3 graus ao ângulo atual, até alcançar
        o ângulo de destino definido por :meth:`define_angulo_destino()`.

        Parameters
        ----------
        pino : int
            O pino GPIO que controla o servo motor.

        angulo_inicial : float
            O ângulo inicial do servo motor.

        passos : float
            O número de passos que serão somados quando o ângulo do motor for atualizado.
        """
        # Informações do servo motor
        self._passos = passos/36
        self._pino = pino

        # PWM
        GPIO.setup(self._pino, GPIO.OUT)
        self._pwm = GPIO.PWM(self._pino, 50)

    def retorna_angulo_atual(self):
        """Retorna o ângulo atual do servo motor.

        É importante notar que, como o ângulo do servo motor varia gradualmente, o valor retornado por esse
        método não obrigatoriamente será o definido ao usar o método :meth:`define_angulo_destino()`. O ângulo atual
        se ajustará gradualmente até chegar ao ângulo configurado por esse método.

        Se deseja ler o ângulo selecionado por :meth:`define_angulo_destino()`, use o método :meth:`retorna_angulo_destino()`.

        O ângulo é retornado em graus.

        Returns
        -------
        float
            O ângulo atual do servo motor.
        """
        return self._converte_duty_para_graus(self._duty_atual)

    def retorna_angulo_destino(self):
        """Retorna o ângulo de destino do servo motor.

        Por exemplo, se foi usado a função :meth:`define_angulo_destino()` para definir 120°. Essa função retorna 120.

        O ângulo é retornado em graus.

        Returns
        -------
        float
            O ângulo de destino do servo motor.
        """
        return self._converte_duty_para_graus(self._duty_destino)

    def define_angulo_destino(self, angulo: float):
        """Define o ângulo de destino do servo motor.

        O ângulo atual do servo motor se ajustará gradualmente até alcançar o valor definido pelo parâmetro *angulo*.
        Para realizar uma atualização, use o método :meth:`atualiza_angulo()`

        O ângulo é informado em graus.

        Returns
        -------
        float
            O ângulo de destino do servo motor.
        """
        self._duty_destino = self._converte_graus_para_duty(angulo)

    def inicia(self, angulo):
        """Inicia o servo motor."""
        # Angulo inicial do servo motor
        self._duty_atual = self._converte_graus_para_duty(angulo)
        self._duty_destino = self._duty_atual

        self._pwm.start(self._duty_atual)

    def atualiza_angulo(self):
        """Atualiza o angulo atual do motor.

        O angulo do motor se ajustará gradualmente até alcançar o valor do ângulo de destino. Esse método atualiza
        o passo definido na instanciação da classe.

        O ângulo de destino é definido pelo método :meth:`define_angulo_destino()`. A atualização ocorre em
        passos definidos pelo parâmetro *passos* do método de inicialização da classe :meth:`__init__()`:.
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
        """Desliga o servo motor.

        Desativa o PWM que controla os motor e libera a GPIO da Raspberry Pi utilizada. O objeto se torna
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
