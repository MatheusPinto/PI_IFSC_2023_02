#include "sensing.h"
#include "hardware.h"
#include <Arduino.h>

/**
 * @brief Constructs a new Sensing object.
 */
Sensing::Sensing(Scheduler &appScheduler)
	: m_UpdateTask(TASK_MILLISECOND * SENSING_POOLING_INTERVAL_MS, TASK_FOREVER, [this]() { this->Update(); })
{
	/** Set pin mode */
	pinMode(SENSOR_MQ_5_PIN, INPUT);
	pinMode(SENSOR_MQ_6_PIN, INPUT);
	pinMode(SENSOR_MQ_7_PIN, INPUT);

	/** Add update task */
	appScheduler.addTask(m_UpdateTask);

	/** Enable update task */
	m_UpdateTask.enable();
}

/**
 * @brief Destroys the Sensing object.
 */
Sensing::~Sensing()
{
}

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
uint8_t Sensing::Read(SensorUnit unit)
{
	return m_Sensors[unit].average;
}

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
uint8_t* Sensing::ReadHistory(SensorUnit unit)
{
	return m_Sensors[unit].history;
}

/**
 * @brief Performs the pooling of the sensors information and stores in local
 * states.
 *
 * @return void
 */
void Sensing::Update()
{
	/** Pool new data */
	int rawValues[MAX_CONNECTED_SENSORS];

	/** ADC readings */
	rawValues[SENSOR_MQ5] = analogRead(SENSOR_MQ_5_PIN);
	rawValues[SENSOR_MQ6] = analogRead(SENSOR_MQ_6_PIN);
	rawValues[SENSOR_MQ7] = analogRead(SENSOR_MQ_7_PIN);

#ifdef DEBUG_ENABLED
	Serial.println("Sensing raw");
	Serial.print("MQ5: ");
	Serial.print(rawValues[SENSOR_MQ5]);
	Serial.print(" | MQ6: ");
	Serial.print(rawValues[SENSOR_MQ6]);
	Serial.print(" | MQ7: ");
	Serial.println(rawValues[SENSOR_MQ7]);
#endif

	/** Update local states for each sensor */
	for (int i = 0; i < MAX_CONNECTED_SENSORS; ++i)
	{
		/** Get sensor instance */
		SensorData &sensor = m_Sensors[i];

		/** AVG buffer */
		uint16_t sum = 0;

		/** Shift and update average */
		for (uint8_t j = 0; j < MAX_SENSOR_AVERAGE - 1; ++j)
		{
			sensor.values[j] = sensor.values[j + 1];
			sum += sensor.values[j];
		}
		sensor.values[MAX_SENSOR_AVERAGE - 1] = map(
			rawValues[i],
			0, ESP_MAX_ADC_VALUE,
			0, MAX_SENSOR_VALUE
		);
		sum += sensor.values[MAX_SENSOR_AVERAGE - 1];

		sensor.average = (uint8_t)(sum / MAX_SENSOR_AVERAGE);

		/** Shift and update history */
		for (uint8_t j = 0; j < CHART_POINTS - 1; ++j)
		{
			sensor.history[j] = sensor.history[j + 1];
		}
		sensor.history[CHART_POINTS - 1] = sensor.average;
	}

#ifdef DEBUG_ENABLED
	Serial.println("Sensing update");
	Serial.print("MQ5: ");
	Serial.print(m_Sensors[SENSOR_MQ5].average);
	Serial.print(" | MQ6: ");
	Serial.print(m_Sensors[SENSOR_MQ6].average);
	Serial.print(" | MQ7: ");
	Serial.println(m_Sensors[SENSOR_MQ7].average);
#endif
}
