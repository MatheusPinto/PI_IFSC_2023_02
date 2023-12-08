#!/usr/bin/env python3


"""Testa o driver L298N.

Usa niveis lógicos fixos. Não usa PWM.
"""


import fake_RPi
import RPi.GPIO as GPIO
import time

# Definição dos pinos do driver L298N
IN1 = 25
IN2 = 8

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)

    def motor_forward():
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)

    def motor_backward():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)

    def motor_stop():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)

    try:
        while True:
            motor_forward()
            print("Motor movendo-se para frente")
            time.sleep(5)

            motor_backward()
            print("Motor movendo-se para trás")
            time.sleep(5)

            motor_stop()
            print("Motor parado")
            time.sleep(5)

    except KeyboardInterrupt:
        motor_stop()
        GPIO.cleanup()

