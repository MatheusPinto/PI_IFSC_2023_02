#!/usr/bin/env python3


"""Testa o PWM do L298N (apenas 1 motor)."""



import fake_RPi
import RPi.GPIO as GPIO
import time

# Definição dos pinos do driver L298N
IN1 = 22
IN2 = 27

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)

    # Configuração dos pinos PWM
    pwm_frequency = 100  # Frequência em Hertz
    pwm_a = GPIO.PWM(IN1, pwm_frequency)

    pwm_a.start(0)  # Inicializa o PWM com ciclo de trabalho de 0

    def motor_forward(speed):
        pwm_a.ChangeDutyCycle(speed)

    try:
        while True:
            print("Motor girando para frente")
            motor_forward(50)  # Define a velocidade para 50% (exemplo)
            time.sleep(2)

    except KeyboardInterrupt:
        pwm_a.stop()
        GPIO.cleanup()
