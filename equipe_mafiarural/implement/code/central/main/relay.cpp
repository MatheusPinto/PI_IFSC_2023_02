#include "relay.h"
#include <Arduino.h>

/**
 * @brief Constructs a new Relay object.
 */
Relay::Relay(Flash &flash)
{
#ifdef DEBUG_ENABLED
	Serial.println("Relay Constructor");
#endif

	/** Set pin mode */
	pinMode(RELAY_0, OUTPUT);
	pinMode(RELAY_1, OUTPUT);
	pinMode(RELAY_2, OUTPUT);
	pinMode(RELAY_3, OUTPUT);
	pinMode(RELAY_4, OUTPUT);
	pinMode(RELAY_5, OUTPUT);
	pinMode(RELAY_6, OUTPUT);
	pinMode(RELAY_7, OUTPUT);

	m_DefaultState = flash.ReadConfig()["startup"]["relay"].as<uint8_t>();

	Reset();
}

/**
 * @brief Destroys the Relay object.
 */
Relay::~Relay()
{
}

/**
 * @brief Sets the relay unit to on.
 */
void Relay::Set(RelayUnit unit)
{
	/** Check if is locked */
	if (IsLocked()) return;

	digitalWrite(unit, LOW);
}

/**
 * @brief Sets the relay unit based on a uint8_t.
 */
void Relay::Set(uint8_t block)
{
	/** Check if is locked */
	if (IsLocked()) return;

	/** Set initial state */
	digitalWrite(RELAY_0, block & 0b00000001 ? LOW : HIGH);
	digitalWrite(RELAY_1, block & 0b00000010 ? LOW : HIGH);
	digitalWrite(RELAY_2, block & 0b00000100 ? LOW : HIGH);
	digitalWrite(RELAY_3, block & 0b00001000 ? LOW : HIGH);
	digitalWrite(RELAY_4, block & 0b00010000 ? LOW : HIGH);
	digitalWrite(RELAY_5, block & 0b00100000 ? LOW : HIGH);
	digitalWrite(RELAY_6, block & 0b01000000 ? LOW : HIGH);
	digitalWrite(RELAY_7, block & 0b10000000 ? LOW : HIGH);
}

/**
 * @brief Gets current state of the relay block.
 */
uint8_t Relay::Get()
{
	/** Get current state */
	uint8_t block = 0;
	block |= digitalRead(RELAY_1) ? 0b00000010 : 0;
	block |= digitalRead(RELAY_2) ? 0b00000100 : 0;
	block |= digitalRead(RELAY_3) ? 0b00001000 : 0;
	block |= digitalRead(RELAY_4) ? 0b00010000 : 0;
	block |= digitalRead(RELAY_5) ? 0b00100000 : 0;
	block |= digitalRead(RELAY_6) ? 0b01000000 : 0;
	block |= digitalRead(RELAY_7) ? 0b10000000 : 0;

	return block;
}

/**
 * @brief Sets the relay unit to default state.
 */
void Relay::Reset()
{
	/** Check if is locked */
	if (IsLocked()) return;

	/** Set initial state */
	Set(m_DefaultState);
}

/**
 * @brief Sets the relay unit to off.
 */
void Relay::Reset(RelayUnit unit)
{
	/** Check if is locked */
	if (IsLocked()) return;

	digitalWrite(unit, HIGH);
}
