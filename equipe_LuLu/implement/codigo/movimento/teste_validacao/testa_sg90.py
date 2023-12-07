#!/usr/bin/env python3


"""Testa o motor de passo SG90."""


import fake_RPi
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)

    pwm = GPIO.PWM(22, 50)  # Configura o pino 22 para PWM com frequência de 50Hz
    pwm.start(0)  # Inicializa o PWM com um ciclo de trabalho de 0%

    def angle_to_duty_cycle(angle):
        # Converte o ângulo desejado (entre 0 e 180 graus) em ciclo de trabalho do PWM
        return (angle * 5/ 180) + 5

    try:
        while True:
            # Move o motor do ângulo 0 para 180 graus
            for angle in range(0, 181, 1):
                duty_cycle = angle_to_duty_cycle(angle)
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.1)

            # Move o motor do ângulo 180 para 0 graus
            for angle in range(180, -1, -1):
                duty_cycle = angle_to_duty_cycle(angle)
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.1)

    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
