#!/usr/bin/env python3


"""Zera uma GPIO."""


import RPi.GPIO as GPIO
import time


# Definindo o pino GPIO
pin_gpio = 8

if __name__ == "__main__":
    # Configurando o modo da GPIO
    GPIO.setmode(GPIO.BCM)  # Use BOARD para referenciar o número do pino, ou BCM para referenciar o número GPIO

    # Configurando o pino GPIO como saída
    GPIO.setup(pin_gpio, GPIO.OUT)

    try:
        # Definindo o pino GPIO para o estado lógico baixo (zero)
        GPIO.output(pin_gpio, GPIO.LOW)
        print(f"Pino GPIO {pin_gpio} definido como LOW (zero)")
        time.sleep(10)

    except KeyboardInterrupt:
        pass

    finally:
        # Limpando a configuração da GPIO
        GPIO.cleanup()
        print("Configuração GPIO limpa")
