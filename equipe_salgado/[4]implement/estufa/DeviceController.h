#ifndef DeviceController_h
#define DeviceController_h

#include <Arduino.h>

class DeviceController {
public:
  DeviceController(int coolerPin1, int coolerPin2, int coolerPWM, int ledPin1, int ledPin2, int ledPWM, int bombaPin);

  struct DeviceStatus {
    int led;
    int cooler;
    int bomba;
  };

  DeviceStatus statusDevice();
  void controlDevice(int device, int pwm);

private:
  int COOLERpin1, COOLERpin2, COOLERpwm, LEDpin1, LEDpin2, LEDpwm, BOMBApin;
};

#endif
