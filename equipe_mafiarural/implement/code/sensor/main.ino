
/**
 * Hardware definitions
 */

/** Pins */
#define SENSOR_MQ_5 34
#define SENSOR_MQ_6 39
#define SENSOR_MQ_7 36

/** Definitions */
#define ESP_MAX_ADC_VALUE 4096

/**
 * Globals
 */

/** Value from 0 to 100 representing reading value from sensors */

int sensorMq5Value = 0;
int sensorMq6Value = 0;
int sensorMq7Value = 0;

/**
 * Reads all values from sensors and stores in global scope
 */
void readSensors();

/**
 * Init sector
 */
void setup()
{
	/** Initilizes Serial */
	Serial.begin(9600);

	/** Warm up */
	delay(1000);
	Serial.println("Warm up time");
}

/**
 * Loop sector
 */
void loop()
{
	readSensors();

	Serial.print("MQ5: ");
	Serial.print(sensorMq5Value);
	Serial.print(" / ");
	Serial.print("MQ6: ");
	Serial.print(sensorMq6Value);
	Serial.print(" / ");
	Serial.print("MQ7: ");
	Serial.println(sensorMq7Value);

	delay(500);
}

/**
 * Reads all values from sensors and stores in global scope
 */
void readSensors()
{
	int rawSensorMq5 = analogRead(SENSOR_MQ_5);
	int rawSensorMq6 = analogRead(SENSOR_MQ_6);
	int rawSensorMq7 = analogRead(SENSOR_MQ_7);

	sensorMq5Value = map(
		rawSensorMq5,
		0, ESP_MAX_ADC_VALUE,
		0, 100
	);
	sensorMq6Value = map(
		rawSensorMq6,
		0, ESP_MAX_ADC_VALUE,
		0, 100
	);
	sensorMq7Value = map(
		rawSensorMq7,
		0, ESP_MAX_ADC_VALUE,
		0, 100
	);
}
