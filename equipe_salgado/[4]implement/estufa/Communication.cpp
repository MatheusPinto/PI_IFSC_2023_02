#include "Communication.h"

Communication::Communication() {}

void Communication::writeSerial(const Protocol& message) {
  char device[3];
  char pwmvalue[4];
  char sensorvalue[5];
  char tshvalue[4];

  sprintf(device, "%02d", message.device);
  sprintf(pwmvalue, "%03d", message.pwm);
  sprintf(sensorvalue, "%04d", message.sensor);
  sprintf(tshvalue, "%03d", message.tsh);
  
  Serial.write('s');
  Serial.write(':');
  Serial.write(device[0]);
  Serial.write(device[1]);
  Serial.write(':');
  Serial.write(pwmvalue[0]);
  Serial.write(pwmvalue[1]);
  Serial.write(pwmvalue[2]);
  Serial.write(':');
  Serial.write(sensorvalue[0]);
  Serial.write(sensorvalue[1]);
  Serial.write(sensorvalue[2]);
  Serial.write(sensorvalue[3]);
  Serial.write(':');
  Serial.write(tshvalue[0]);
  Serial.write(tshvalue[1]);
  Serial.write(tshvalue[2]);
  Serial.write(':');
  Serial.write('e');
}

Communication::Protocol Communication::readSerial(bool debug) {
  Protocol retorno;
  char message[19];
  int i = 0;
  
  while (Serial.available()) {
    char receivedChar = Serial.read();
    Serial.write(receivedChar);
    if (receivedChar == 's') {
      i = 0;
      message[i++] = receivedChar;
    } else if(receivedChar == 'e') {
      message[i++] = receivedChar;
      break;
    } else {
      message[i++] = receivedChar;
    }
  }

  if (message[0] == 's' && message[18] == 'e') {
    char devicevalue[3];
    devicevalue[0] = message[2];
    devicevalue[1] = message[3];
    devicevalue[2] = '\0';
    
    char pwmvalue[4];
    pwmvalue[0] = message[5];
    pwmvalue[1] = message[6];
    pwmvalue[2] = message[7];
    pwmvalue[3] = '\0';
    
    char sensorvalue[5];
    sensorvalue[0] = message[9];
    sensorvalue[1] = message[10];
    sensorvalue[2] = message[11];
    sensorvalue[3] = message[12];
    sensorvalue[4] = '\0';

    char tshvalue[4];
    tshvalue[0] = message[14];
    tshvalue[1] = message[15];
    tshvalue[2] = message[16];
    tshvalue[3] = '\0';

    if (debug) {
      Serial.print("Device Value: ");
      Serial.println(devicevalue);
      
      Serial.print("PWM Value: ");
      Serial.println(pwmvalue);
      
      Serial.print("Sensor Value: ");
      Serial.println(sensorvalue);
      
      Serial.print("TSH Value: ");
      Serial.println(tshvalue);
    }

    retorno.device = atoi(devicevalue);
    retorno.pwm = atoi(pwmvalue);
    retorno.sensor = atoi(sensorvalue);
    retorno.tsh = atoi(tshvalue);
    return retorno;
  }
  else{
     retorno.sensor = retorno.tsh = retorno.device = retorno.pwm = 0;
     return retorno;
    }
}

void Communication::printSerial(const char message[18]) {
  for (int j = 0; j < sizeof(message); j++) {
    Serial.print(message[j]);
  }
}
