#!/usr/bin/env python3


"""Testa o PWM do L298N (2 motores)."""


import fake_RPi
import RPi.GPIO as GPIO
import time

# Definição dos pinos do driver L298N
IN1 = 25
IN2 = 24
IN3 = 23  # Pino adicional para o segundo motor
IN4 = 18  # Pino adicional para o segundo motor

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    # Configuração dos pinos PWM para cada motor
    pwm_frequency = 100  # Frequência em Hertz
    pwm_motor_1 = GPIO.PWM(IN1, pwm_frequency)
    pwm_motor_2 = GPIO.PWM(IN2, pwm_frequency)
    pwm_motor_3 = GPIO.PWM(IN3, pwm_frequency)
    pwm_motor_4 = GPIO.PWM(IN4, pwm_frequency)

    pwm_motor_1.start(0)  # Inicializa o PWM com ciclo de trabalho de 0
    pwm_motor_2.start(0)
    pwm_motor_3.start(0)
    pwm_motor_4.start(0)

    def motor_backward(speed):
        pwm_motor_1.ChangeDutyCycle(0)
        pwm_motor_2.ChangeDutyCycle(speed)
        pwm_motor_3.ChangeDutyCycle(0)
        pwm_motor_4.ChangeDutyCycle(speed)

    def motor_forward(speed):
        pwm_motor_1.ChangeDutyCycle(speed)
        pwm_motor_2.ChangeDutyCycle(0)
        pwm_motor_3.ChangeDutyCycle(speed)
        pwm_motor_4.ChangeDutyCycle(0)

    try:
        while True:
            print("Motores girando para frente")
            motor_forward(75)  # Define a velocidade do motor 1 para 50% (exemplo)
            time.sleep(2)
            motor_backward(75)  # Define a velocidade do motor 1 para 50% (exemplo)
            time.sleep(2)

    except KeyboardInterrupt:
        pwm_motor_1.stop()
        pwm_motor_2.stop()
        GPIO.cleanup()
