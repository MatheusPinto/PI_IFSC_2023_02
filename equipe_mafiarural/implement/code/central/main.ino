
/**
 * Hardware definitions
 */

/** Pins */
#define RELAY_8 2
#define RELAY_7 4
#define RELAY_6 21
#define RELAY_5 22
#define RELAY_4 16
#define RELAY_3 25
#define RELAY_2 26
#define RELAY_1 27

/**
 * Globals
 */

/**
 * Init sector
 */
void setup()
{
	/** Initilizes Serial */
	Serial.begin(9600);

	/** Set pin mode in digital pin */
	pinMode(RELAY_1, OUTPUT);
	pinMode(RELAY_2, OUTPUT);
	pinMode(RELAY_3, OUTPUT);
	pinMode(RELAY_4, OUTPUT);
	pinMode(RELAY_5, OUTPUT);
	pinMode(RELAY_6, OUTPUT);
	pinMode(RELAY_7, OUTPUT);
	pinMode(RELAY_8, OUTPUT);

	/** Default states */
	digitalWrite(RELAY_1, HIGH);
	digitalWrite(RELAY_2, HIGH);
	digitalWrite(RELAY_3, HIGH);
	digitalWrite(RELAY_4, HIGH);
	digitalWrite(RELAY_5, HIGH);
	digitalWrite(RELAY_6, HIGH);
	digitalWrite(RELAY_7, HIGH);
	digitalWrite(RELAY_8, HIGH);

	/** Warm up */
	delay(1000);
	Serial.println("Warm up time");
}

/**
 * Loop sector
 */
void loop()
{
	digitalWrite(RELAY_1, LOW);
	delay(40);
	digitalWrite(RELAY_2, LOW);
	delay(40);
	digitalWrite(RELAY_3, LOW);
	delay(40);
	digitalWrite(RELAY_4, LOW);
	delay(40);
	digitalWrite(RELAY_5, LOW);
	delay(40);
	digitalWrite(RELAY_6, LOW);
	delay(40);
	digitalWrite(RELAY_7, LOW);
	delay(40);
	digitalWrite(RELAY_8, LOW);
	delay(1000);
	digitalWrite(RELAY_1, HIGH);
	delay(40);
	digitalWrite(RELAY_2, HIGH);
	delay(40);
	digitalWrite(RELAY_3, HIGH);
	delay(40);
	digitalWrite(RELAY_4, HIGH);
	delay(40);
	digitalWrite(RELAY_5, HIGH);
	delay(40);
	digitalWrite(RELAY_6, HIGH);
	delay(40);
	digitalWrite(RELAY_7, HIGH);
	delay(40);
	digitalWrite(RELAY_8, HIGH);
	delay(150);
}
