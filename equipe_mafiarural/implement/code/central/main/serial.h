#ifndef _SERIAL_H_FILE_
#define _SERIAL_H_FILE_

#include "common.h"
#include <Arduino.h>

/**
 * @brief Simple app Serial Wrapper for constructor
 */
class AppSerial
{
public:
	/**
	 * @brief Constructs a new AppSerial object.
	 */
	inline AppSerial()
	{
#ifdef DEBUG_ENABLED
		Serial.begin(SERIAL_BAUD_RATE);
#endif
	}

	/**
	 * @brief Destroys the AppSerial object.
	 */
	~AppSerial() = default;
};

#endif // !_SERIAL_H_FILE_