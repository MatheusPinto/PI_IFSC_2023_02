#include "SensorController.h"
#define LDRpin A0
#define T1592vcc 53   
#define T1592pin A15
#define DHTpin 52
SensorController sensorController(LDRpin, T1592vcc, T1592pin, DHTpin);

#include <DHT.h>
#define DHTTYPE DHT22
DHT dht(DHTpin, DHTTYPE);

#include "DeviceController.h"
#define COOLERpin1 4
#define COOLERpin2 2
#define COOLERpwm 3
#define LEDpin1 7
#define LEDpin2 6
#define LEDpwm 5
#define BOMBApin 50
DeviceController deviceController(COOLERpin1, COOLERpin2, COOLERpwm, LEDpin1, LEDpin2, LEDpwm, BOMBApin);

#include "Communication.h"
Communication communication;

struct Sistema {
  int pwm;
  int sensor;
  int tsh;
};

struct Estufa {
  Sistema luminosidade;
  Sistema temperatura;
  Sistema nivel;
};

Estufa estufa;
Communication::Protocol message;
void setup() {
  Serial.begin(9600);

  dht.begin();
  pinMode(DHTpin, INPUT);

  pinMode(T1592vcc, OUTPUT);
  digitalWrite(T1592vcc, LOW);
  pinMode(T1592pin, INPUT);
  
  pinMode(LDRpin, INPUT);

  pinMode(COOLERpin1,OUTPUT);
  pinMode(COOLERpin2,OUTPUT);
  pinMode(COOLERpwm,OUTPUT);
  pinMode(LEDpin1,OUTPUT);
  pinMode(LEDpin2,OUTPUT);
  pinMode(LEDpwm,OUTPUT);
  pinMode(BOMBApin,OUTPUT);

  estufa = defaultStartup(estufa);
}

void loop(){
  estufa = recieveProtocol(estufa, 1);

  static unsigned long lastTime1 = 0;
  static unsigned long lastTime2 = 0;
  unsigned long currentTime = millis();
  if (currentTime - lastTime2 >= 10000) {
    sendStatus(estufa, 1);
    lastTime2 = currentTime;
  }
}

Estufa defaultStartup(Estufa estufa) {
  estufa.temperatura.pwm = 0;
  estufa.temperatura.sensor = 0;
  estufa.temperatura.tsh = 0;

  estufa.luminosidade.pwm = 0;
  estufa.luminosidade.sensor = 0;
  estufa.luminosidade.tsh = 0;

  estufa.nivel.pwm = 0;
  estufa.nivel.sensor = 0;
  estufa.nivel.tsh = 0;

  return estufa;
}

Estufa recieveProtocol(Estufa estufa, bool debug) {
  Communication::Protocol message = communication.readSerial(debug);
  delay(8000);
  deviceController.controlDevice(message.device, message.pwm);

  switch (message.device) {
    // temperatura
    case 0:
      estufa.temperatura.tsh = message.tsh;
      estufa.temperatura.pwm = message.pwm;

      if(estufa.temperatura.tsh < estufa.temperatura.sensor){
        estufa.temperatura.pwm = 130;
        deviceController.controlDevice(message.device, estufa.temperatura.pwm);
      }
      
      break;

    // iluminacao
    case 1:
      estufa.luminosidade.tsh = message.tsh;
      estufa.luminosidade.pwm = message.pwm;
      
      if(estufa.luminosidade.tsh > estufa.luminosidade.sensor){
        estufa.luminosidade.pwm = 100;
        deviceController.controlDevice(message.device, estufa.luminosidade.pwm);
      }
      
      break;

    // agua
    case 10:
      estufa.nivel.tsh = message.tsh;
      estufa.nivel.pwm = message.pwm;

      if(estufa.nivel.tsh < estufa.nivel.sensor){
        estufa.nivel.pwm = 100;
        deviceController.controlDevice(message.device, estufa.nivel.pwm);
      }
      
      break;

    default:
      break;
  }

  return estufa;
}


void sendStatus(Estufa estufa, bool debug) {
  SensorController::SensorValues sensor = sensorController.readAllSensors(debug);
  
  message.device = 0;
  message.pwm = estufa.temperatura.pwm;
  message.sensor = sensor.temperature;
  message.tsh = estufa.temperatura.tsh;
  
  communication.writeSerial(message);
  
  message.device = 1;
  message.pwm = estufa.luminosidade.pwm;
  message.sensor = sensor.lighting;
  message.tsh = estufa.luminosidade.tsh;
  
  communication.writeSerial(message);
  
  message.device = 10;
  message.pwm = estufa.nivel.pwm;
  message.sensor = sensor.level;
  message.tsh = estufa.nivel.tsh;
  
  communication.writeSerial(message);
}
