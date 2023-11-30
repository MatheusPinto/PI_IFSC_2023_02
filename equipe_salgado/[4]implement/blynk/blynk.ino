/*************************************************************

  This example shows how value can be pushed from Arduino to
  the Blynk App.

  WARNING :
  For this example you'll need Adafruit DHT sensor libraries:
    https://github.com/adafruit/Adafruit_Sensor
    https://github.com/adafruit/DHT-sensor-library

  App dashboard setup:
    Value Display widget attached to V5
    Value Display widget attached to V6
 *************************************************************/

/* Fill-in information from Blynk Device Info here */
#define BLYNK_TEMPLATE_ID "TMPL2hDK5YqQo"
#define BLYNK_TEMPLATE_NAME "Teste"
#define BLYNK_AUTH_TOKEN "L-RXKJ_z_vb6QLuERlDHT_Zff05wGCAT"
/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial


#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#include "Communication.h"
Communication communication;

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "@fbarbozac";
char pass[] = "84038051";

BlynkTimer timer;

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


void recieveProtocol() {
  Communication::Protocol message = communication.readSerial(0);

  switch (message.device) {
    // temperatura
    case 0:
      Blynk.virtualWrite(V7, message.pwm);
      Blynk.virtualWrite(V6, message.sensor);
      Blynk.virtualWrite(V5, message.tsh);
      estufa.temperatura.sensor = message.sensor;
      break;

    // iluminacao
    case 1:
      Blynk.virtualWrite(V8, message.pwm);
      Blynk.virtualWrite(V1, message.sensor);
      Blynk.virtualWrite(V2, message.tsh);
      estufa.luminosidade.sensor = message.sensor;
      break;

    // agua
    case 10:
      Blynk.virtualWrite(V0, message.pwm);
      Blynk.virtualWrite(V3, message.sensor);
      Blynk.virtualWrite(V4, message.tsh);
      estufa.nivel.sensor = message.sensor;
      break;

    default:
      break;
  }
}

BLYNK_WRITE(V7)
{
  estufa.temperatura.pwm = param.asInt();
  
  message.device = 0;
  message.pwm = estufa.temperatura.pwm;
  message.sensor = estufa.temperatura.sensor;
  message.tsh = estufa.temperatura.tsh;

  communication.writeSerial(message);
}
BLYNK_WRITE(V5)
{
  estufa.temperatura.tsh = param.asInt();
  
  message.device = 0;
  message.pwm = estufa.temperatura.pwm;
  message.sensor = estufa.temperatura.sensor;
  message.tsh = estufa.temperatura.tsh;

  communication.writeSerial(message);
}

BLYNK_WRITE(V8)
{
  estufa.luminosidade.pwm = param.asInt(); 
  
  message.device = 1;
  message.pwm = estufa.luminosidade.pwm;
  message.sensor = estufa.luminosidade.sensor;
  message.tsh = estufa.luminosidade.tsh;

  communication.writeSerial(message);
}
BLYNK_WRITE(V2)
{
  estufa.luminosidade.tsh = param.asInt();
  
  message.device = 1;
  message.pwm = estufa.luminosidade.pwm;
  message.sensor = estufa.luminosidade.sensor;
  message.tsh = estufa.luminosidade.tsh;

  communication.writeSerial(message);
}

BLYNK_WRITE(V0)
{
  estufa.nivel.pwm = param.asInt(); 
  
  message.device = 10;
  message.pwm = estufa.nivel.pwm;
  message.sensor = estufa.nivel.sensor;
  message.tsh = estufa.nivel.tsh;

  communication.writeSerial(message);
}
BLYNK_WRITE(V4)
{
  estufa.nivel.tsh = param.asInt();
  
  message.device = 10;
  message.pwm = estufa.nivel.pwm;
  message.sensor = estufa.nivel.sensor;
  message.tsh = estufa.nivel.tsh;

  communication.writeSerial(message);
}

void setup()
{
  Serial.begin(9600);

  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass, "blynk.cloud", 80);
//  /Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass, IPAddress(192,168,1,192), 8080);

  defaultStartup(estufa); 
  
  // Setup a function to be called every second
  timer.setInterval(1000L, recieveProtocol);
}

void loop()
{
  Blynk.run();
  timer.run();
}
