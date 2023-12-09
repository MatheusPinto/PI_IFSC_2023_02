#ifndef Communication_h
#define Communication_h

#include <Arduino.h>

class Communication {
public:
  struct Protocol {
    int device;
    int pwm;
    int sensor;
    int tsh;
  };

  Communication();

  void writeSerial(const Protocol& message);
  Protocol readSerial(bool debug);
  void printSerial(const char message[18]);
};

#endif
