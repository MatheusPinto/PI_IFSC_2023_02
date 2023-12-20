#ifndef _SENSING_H_FILE_
#define _SENSING_H_FILE_

#include "common.h"
#include "painlessMesh.h"
#include <stdint.h>

/** Definitions */

/**
 * @brief Maximum number of sensor readings to average.
 */
#define MAX_SENSOR_AVERAGE (uint8_t)10U

/**
 * @brief Maximum number of connected sensors.
 */
#define MAX_CONNECTED_SENSORS (uint8_t)3U

/**
 * @brief Interval in milliseconds between sensor readings.
 */
#define SENSING_POOLING_INTERVAL_MS (uint16_t)500U

/**
 * @brief Maximum sensor value constant.
 *
 * This macro defines the maximum value that a sensor can produce after its
 * mapping.
 */
#define MAX_SENSOR_VALUE (uint8_t)100U

/** Enums */

/**
 * @brief Enumeration representing sensor units connected to system.
 */
enum SensorUnit
{
	SENSOR_MQ5, /**< MQ5 sensor unit. */
	SENSOR_MQ6, /**< MQ6 sensor unit. */
	SENSOR_MQ7  /**< MQ7 sensor unit. */
};

/** Class */

/**
 * @brief The Sensing class manages the system sensing.
 */
class Sensing
{
public:
	/**
	 * @brief Constructs a new Sensing object.
	 */
	Sensing(Scheduler &appScheduler);

	/**
	 * @brief Destroys the Sensing object.
	 */
	~Sensing();

public:
	/**
	 * @brief Read a given sensor unit value.
	 *
	 * This function reads a value from a specified sensor unit and returns it as
	 * a uint8_t. Value is already treated and its value is given from the last time
	 * the update_units() function was called.
	 *
	 * @param unit The sensor unit from which to read the value (e.g., SENSOR_MQ5, SENSOR_MQ6).
	 * @return uint8_t The value read from the sensor unit, clamped to the range [0, MAX_SENSOR_VALUE].
	 */
	uint8_t Read(SensorUnit unit);

	/**
	 * @brief Read a given sensor unit history.
	 *
	 * This function reads a history from a specified sensor unit and returns it as
	 * a uint8_t*. Value is already treated and its value is given from the last time
	 * the update_units() function was called.
	 *
	 * @param unit The sensor unit from which to read the value (e.g., SENSOR_MQ5, SENSOR_MQ6).
	 * @return uint8_t* The value read from the sensor unit, clamped to the range [0, MAX_SENSOR_VALUE].
	 */
	uint8_t* ReadHistory(SensorUnit unit);

private:
	/**
	 * @brief Performs the pooling of the sensors information and stores in local
	 * states.
	 *
	 * @return void
	 */
	void Update(void);

private:
	/**
	 * @brief Structure to store sensor data and its average value.
	 */
	struct SensorData
	{
		uint8_t values[MAX_SENSOR_AVERAGE];
		uint8_t history[CHART_POINTS];
		uint8_t average;
	};

private:
	/**
	 * @brief Sensors data storage
	 */
	SensorData m_Sensors[MAX_CONNECTED_SENSORS] = {};

	/**
	 * @brief Status system update task
	 */
	Task m_UpdateTask;
};

#endif /* _SENSING_H_FILE_ */
