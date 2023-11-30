#include "SensorController.h"

SensorController::SensorController(int ldrPin, int t1592vcc, int t1592pin, int dhtPin)
    : LDRpin(ldrPin), T1592vcc(t1592vcc), T1592pin(t1592pin), DHTpin(dhtPin), dht(dhtPin, DHT22) {
  pinMode(LDRpin, INPUT);
  pinMode(T1592vcc, OUTPUT);
  pinMode(T1592pin, INPUT);
  pinMode(DHTpin, INPUT);
  dht.begin();
}

SensorController::SensorValues SensorController::readAllSensors(bool debug) {
  SensorValues values;

  values.lighting = readLDR(debug);
  values.level = readT1592(debug);

  DHT22Value dhtData = readDHT22(debug);
  values.temperature = dhtData.temperature;
  values.humidity = dhtData.humidity;

  return values;
}

int SensorController::readLDR(bool debug) {
  int ldrValue = analogRead(LDRpin);

  if (debug) {
    Serial.print("\nLuminosidade LDR: ");
    Serial.println(ldrValue);
  }

  return ldrValue;
}

int SensorController::readT1592(bool debug) {
  digitalWrite(T1592vcc, HIGH);
  delay(3);
  int t1592Value = analogRead(T1592pin);
  digitalWrite(T1592vcc, LOW);

  if (debug) {
    Serial.print("Nível de água: ");
    Serial.println(t1592Value);
  }

  return t1592Value;
}

SensorController::DHT22Value SensorController::readDHT22(bool debug) {
  DHT22Value dhtValue;

  dhtValue.temperature = dht.readTemperature();
  dhtValue.humidity = dht.readHumidity();

  if (isnan(dhtValue.humidity) || isnan(dhtValue.temperature)) {
    Serial.println("Erro ao ler o sensor DHT22!\n");
    dhtValue.temperature = 0;
    dhtValue.humidity = 0;
  }

  if (debug) {
    Serial.print("Umidade: ");
    Serial.print(dhtValue.humidity);
    Serial.print(" %\t\n");
    Serial.print("Temperatura: ");
    Serial.print(dhtValue.temperature);
    Serial.println(" °C\n");
  }

  return dhtValue;
}
