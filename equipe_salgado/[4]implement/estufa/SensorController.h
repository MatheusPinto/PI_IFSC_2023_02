#ifndef SensorController_h
#define SensorController_h

#include <DHT.h>

class SensorController {
private:
  const int LDRpin;
  const int T1592vcc;
  const int T1592pin;
  const int DHTpin;
  DHT dht;

public:
  SensorController(int ldrPin, int t1592vcc, int t1592pin, int dhtPin);
  struct SensorValues {
    int lighting;
    int level;
    int temperature;
    int humidity;
  };
  SensorValues readAllSensors(bool debug = false);

private:
  struct DHT22Value {
    int temperature;
    int humidity;
  };
  int readLDR(bool debug);
  int readT1592(bool debug);
  DHT22Value readDHT22(bool debug);
};

#endif
