#!/bin/env python3


"""Testa o buzzer."""


import test
import fake_RPi
import RPi.GPIO as GPIO
import time


# Define o pino GPIO ao qual o buzzer está conectado
pino_buzzer = 7

if __name__ == "__main__":
    # Configuração inicial da GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pino_buzzer, GPIO.OUT)

    try:
        while True:
            # Liga o buzzer (nível lógico baixo)
            GPIO.output(pino_buzzer, GPIO.LOW)
            print("Buzzer ligado.")
            
            time.sleep(2)
            
            # Desliga o buzzer
            GPIO.output(pino_buzzer, GPIO.HIGH)
            print("Buzzer desligado.")

            time.sleep(2)

    except KeyboardInterrupt:
        # Limpa as configurações da GPIO ao finalizar
        GPIO.cleanup()
