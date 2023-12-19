#!/usr/bin/env python3


"""Testa o serbo motor SG90.

Testa três ao mesmo tempo.
"""


import fake_RPi
import RPi.GPIO as GPIO
import time

# Definição dos pinos dos servo motores
servo1_pin = 17
servo2_pin = 27
servo3_pin = 22

if __name__ == "__main__":
    # Configuração dos pinos
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo1_pin, GPIO.OUT)
    GPIO.setup(servo2_pin, GPIO.OUT)
    GPIO.setup(servo3_pin, GPIO.OUT)

    # Configuração do PWM
    pwm_frequency = 50  # Frequência em Hertz

    # Inicializa os PWMs
    servo1_pwm = GPIO.PWM(servo1_pin, pwm_frequency)
    servo2_pwm = GPIO.PWM(servo2_pin, pwm_frequency)
    servo3_pwm = GPIO.PWM(servo3_pin, pwm_frequency)

    # Inicializa os PWMs com ciclo de trabalho de 0
    servo1_pwm.start(0)
    servo2_pwm.start(0)
    servo3_pwm.start(0)

    def set_servo_position(pwm, angulo):
        duty_cycle = 5 + (angulo * 5 / 180)  # Mapeia 0-100% para 5-10%
        pwm.ChangeDutyCycle(duty_cycle)

    try:
        while True:
            print("Movendo servo 1 para 0 graus")
            set_servo_position(servo1_pwm, 0)  # Exemplo: 10% do ciclo de trabalho

            print("Movendo servo 2 para 90 graus")
            set_servo_position(servo2_pwm, 90)  # Exemplo: 7.5% do ciclo de trabalho

            print("Movendo servo 3 para 180 graus")
            set_servo_position(servo3_pwm, 180)  # Exemplo: 5% do ciclo de trabalho

            time.sleep(1)

            print("Movendo servo 1 para 90 graus")
            set_servo_position(servo1_pwm, 90)  # Exemplo: 10% do ciclo de trabalho

            print("Movendo servo 2 para 180 graus")
            set_servo_position(servo2_pwm, 180)  # Exemplo: 7.5% do ciclo de trabalho

            print("Movendo servo 3 para 0 graus")
            set_servo_position(servo3_pwm, 0)  # Exemplo: 5% do ciclo de trabalho

            time.sleep(1)

            print("Movendo servo 1 para 180 graus")
            set_servo_position(servo1_pwm, 180)  # Exemplo: 10% do ciclo de trabalho

            print("Movendo servo 2 para 0 graus")
            set_servo_position(servo2_pwm, 0)  # Exemplo: 7.5% do ciclo de trabalho

            print("Movendo servo 3 para 90 graus")
            set_servo_position(servo3_pwm, 90)  # Exemplo: 5% do ciclo de trabalho

            time.sleep(1)

    except KeyboardInterrupt:
        servo1_pwm.stop()
        servo2_pwm.stop()
        servo3_pwm.stop()
        GPIO.cleanup()
