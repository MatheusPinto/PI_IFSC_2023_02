#ifndef _STATUS_H_FILE_
#define _STATUS_H_FILE_

#include "common.h"
#include <painlessMesh.h>
#include <stdint.h>

/** Definitions */

/**
 * @brief Maximum number of status units
 */
#define MAX_CONNECTED_STATUS (uint8_t)3U

/**
 * @brief Status LED pooling interval in milliseconds
 */
#define STATUS_LED_POOLING_INTERVAL_MS (uint16_t)100

/** Enums */

/**
 * @brief Enumeration representing status unit types.
 * 
 * Status units are used to indicate different system states or conditions.
 */
enum StatusUnit : uint8_t
{
	STATUS_OK0,  /**< Status responsible to activate LED success 0. */
	STATUS_OK1,  /**< Status responsible to activate LED success 1. */
	STATUS_ERROR /**< Status responsible to activate LED fail. */
};

/** Class */

/**
 * @brief The Status class manages the system status.
 */
class Status
{
public:
	/**
	 * @brief Constructs a new Status object.
	 */
	Status(Scheduler &appScheduler);

	/**
	 * @brief Destroys the Status object.
	 */
	~Status();

public:
	/**
	 * @brief Sets the system status to the specified unit.
	 * 
	 * If other status is already activated it will make a OR operation with the
	 * new status, keeping others activated.
	 *
	 * @param unit The status unit to set (e.g., STATUS_OK0, STATUS_OK1, STATUS_ERROR).
	 *
	 */
	void Set(StatusUnit unit);

	/**
	 * @brief Sets the system status to the specified unit with a blink delay.
	 *
	 * @param unit  The status unit to set (e.g., STATUS_OK0, STATUS_OK1, STATUS_ERROR).
	 * @param blinkDelay The delay to use between blinks.
	 *
	 * This function sets the system status to the specified unit with the specified
	 * blink delay.
	 */
	void Set(StatusUnit unit, uint16_t blinkDelay);

	/**
	 * @brief Sets the system status to the specified unit with a blink delay
	 * and repetition.
	 *
	 * @param unit  The status unit to set (e.g., STATUS_OK0, STATUS_OK1, STATUS_ERROR).
	 * @param blinkDelay The delay to use between blinks.
	 * @param times The number of times to repeat the status change.
	 *
	 * This function sets the system status to the specified unit with the specified
	 * blink delay and a certain number of repetitions.
	 */
	void Set(StatusUnit unit, uint16_t blinkDelay, uint16_t times);

	/**
	 * @brief Clears the system status.
	 */
	void Clear();

	/**
	 * @brief Clears the status for a specific unit.
	 * 
	 * @param unit The status unit to clear.
	 */
	void Clear(StatusUnit unit);

private:
	/**
	 * @brief Updates the status system.
	 */
	void Update();

	/**
	 * @brief Updates leds pins based on current status.
	 */
	void UpdateLedStatus();

private:
	/**
	 * @brief Structure to store status data
	 */
	struct StatusControl
	{
		uint8_t mode;
		uint8_t enabled;
		uint16_t blinkDelay;
		uint16_t elapsed;
		uint16_t times;
	};

private:
	/**
	 * @brief The status control structure.
	 */
	StatusControl m_StatusControl[MAX_CONNECTED_STATUS];

	/**
	 * @brief Status system update task
	 */
	Task m_UpdateTask;
};

#endif /* _STATUS_H_FILE_ */
