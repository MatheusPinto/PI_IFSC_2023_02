#include "DeviceController.h"

DeviceController::DeviceController(int coolerPin1, int coolerPin2, int coolerPWM, int ledPin1, int ledPin2, int ledPWM, int bombaPin)
    : COOLERpin1(coolerPin1), COOLERpin2(coolerPin2), COOLERpwm(coolerPWM),
    
      LEDpin1(ledPin1), LEDpin2(ledPin2), LEDpwm(ledPWM), BOMBApin(bombaPin) {
        
  pinMode(COOLERpin1, OUTPUT);
  pinMode(COOLERpin2, OUTPUT);
  pinMode(COOLERpwm, OUTPUT);
  pinMode(LEDpin1, OUTPUT);
  pinMode(LEDpin2, OUTPUT);
  pinMode(LEDpwm, OUTPUT);
  pinMode(BOMBApin, OUTPUT);
  
}

DeviceController::DeviceStatus DeviceController::statusDevice() {
  DeviceStatus retorno;

  retorno.cooler = analogRead(COOLERpwm);
  retorno.led = analogRead(LEDpwm);
  retorno.bomba = digitalRead(BOMBApin);

  return retorno;
}

void DeviceController::controlDevice(int device, int pwm) {
  switch (device) {
    // temperatura
    case 0:
      digitalWrite(COOLERpin1, HIGH);
      digitalWrite(COOLERpin2, LOW);
      analogWrite(COOLERpwm, pwm);
      break;

    // iluminacao
    case 1:
      digitalWrite(LEDpin1, HIGH);
      digitalWrite(LEDpin2, LOW);
      analogWrite(LEDpwm, pwm);
      break;

    // agua
    case 10:
      if (pwm == 0) {
        digitalWrite(BOMBApin, LOW);
        } 
      else if (pwm > 0) {
        digitalWrite(BOMBApin, HIGH);
        }
      break;
      
    default:
      break;
  }
}
