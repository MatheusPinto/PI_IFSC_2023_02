#include "status.h"
#include "hardware.h"
#include <Arduino.h>

/** Enums */

/**
 * @brief Enumeration representing status unit operations modes.
 */
enum StatusUnitMode : uint8_t
{
	STATUS_MODE_FIXED   = 0b00000001U,  /**< status unit will remain active */
	STATUS_MODE_BLINK   = 0b00000010U,  /**< status unit will blink */
	STATUS_MODE_COUNTER = 0b00000100U /**< status unit will blink a certain number of times */
};

/**
 * @brief Constructs a new Status object.
 */
Status::Status(Scheduler &appScheduler)
	: m_UpdateTask(TASK_MILLISECOND * STATUS_LED_POOLING_INTERVAL_MS, TASK_FOREVER, [this]() { this->Update(); })
{
	/** Set pin mode */
	pinMode(STATUS_SUCCESS_LED0_PIN, OUTPUT);
	pinMode(STATUS_SUCCESS_LED1_PIN, OUTPUT);
	pinMode(STATUS_FAIL_LED0_PIN, OUTPUT);

	/** Set initial state */
	digitalWrite(STATUS_SUCCESS_LED0_PIN, LOW);
	digitalWrite(STATUS_SUCCESS_LED1_PIN, LOW);
	digitalWrite(STATUS_FAIL_LED0_PIN, LOW);

	/** Add update task */
	appScheduler.addTask(m_UpdateTask);

	/** Enable update task */
	m_UpdateTask.enable();
}

/**
 * @brief Destroys the Status object.
 */
Status::~Status()
{
}

/**
 * @brief Sets the system status to the specified unit.
 *
 * If other status is already activated it will make a OR operation with the
 * new status, keeping others activated.
 *
 * @param unit The status unit to Set (e.g., STATUS_OK0, STATUS_OK1, STATUS_ERROR).
 *
 */
void Status::Set(StatusUnit unit)
{
	Clear(unit);

	m_StatusControl[unit].mode = STATUS_MODE_FIXED;
	m_StatusControl[unit].enabled = 1;

	UpdateLedStatus();
}

/**
 * @brief Sets the system status to the specified unit with a blink delay.
 *
 * @param unit The status unit to Set (e.g., STATUS_OK0, STATUS_OK1, STATUS_ERROR).
 * @param blinkDelay The delay to use between blinks.
 *
 * This function Sets the system status to the specified unit with the specified
 * blink delay.
 */
void Status::Set(StatusUnit unit, uint16_t blinkDelay)
{
	Clear(unit);

	m_StatusControl[unit].mode = STATUS_MODE_BLINK;
	m_StatusControl[unit].blinkDelay = blinkDelay;
	m_StatusControl[unit].enabled = 1;
	m_StatusControl[unit].elapsed = 0;

	UpdateLedStatus();
}

/**
 * @brief Sets the system status to the specified unit with a blink delay
 * and repetition.
 *
 * @param unit The status unit to Set (e.g., STATUS_OK0, STATUS_OK1, STATUS_ERROR).
 * @param blinkDelay The delay to use between blinks.
 * @param times The number of times to repeat the status change.
 *
 * This function Sets the system status to the specified unit with the specified
 * blink delay and a certain number of repetitions.
 */
void Status::Set(StatusUnit unit, uint16_t blinkDelay, uint16_t times)
{
	Clear(unit);

	m_StatusControl[unit].mode = STATUS_MODE_BLINK | STATUS_MODE_COUNTER;
	m_StatusControl[unit].blinkDelay = blinkDelay;
	m_StatusControl[unit].times = times;
	m_StatusControl[unit].enabled = 1;
	m_StatusControl[unit].elapsed = 0;

	UpdateLedStatus();
}

/**
 * @brief Clears the system status.
 */
void Status::Clear()
{
	for (uint8_t i = 0; i < MAX_CONNECTED_STATUS; i++)
	{
		m_StatusControl[i].mode = 0;
		m_StatusControl[i].enabled = 0;
		m_StatusControl[i].blinkDelay = 0;
		m_StatusControl[i].elapsed = 0;
		m_StatusControl[i].times = 0;
	}

	UpdateLedStatus();
}

/**
 * @brief Clears the status for a specific unit.
 *
 * @param unit The status unit to Clear.
 */
void Status::Clear(StatusUnit unit)
{
	m_StatusControl[unit].mode = 0;
	m_StatusControl[unit].enabled = 0;
	m_StatusControl[unit].blinkDelay = 0;
	m_StatusControl[unit].elapsed = 0;
	m_StatusControl[unit].times = 0;

	UpdateLedStatus();
}

/**
 * @brief Updates leds pins based on current status.
 */
void Status::UpdateLedStatus()
{
	/** Enable or disable based on current status */
	digitalWrite(
		STATUS_SUCCESS_LED0_PIN,
		m_StatusControl[STATUS_OK0].enabled ? HIGH : LOW
	);
	digitalWrite(
		STATUS_SUCCESS_LED1_PIN,
		m_StatusControl[STATUS_OK1].enabled ? HIGH : LOW
	);
	digitalWrite(
		STATUS_FAIL_LED0_PIN,
		m_StatusControl[STATUS_ERROR].enabled ? HIGH : LOW
	);
}

/**
 * @brief Updates the status system.
 */
void Status::Update()
{
	/** Update times and check for changes */
	for (uint8_t i = 0; i < MAX_CONNECTED_STATUS; ++i)
	{
		if (m_StatusControl[i].mode & STATUS_MODE_BLINK)
		{
			m_StatusControl[i].elapsed += STATUS_LED_POOLING_INTERVAL_MS;

			if (m_StatusControl[i].elapsed >= m_StatusControl[i].blinkDelay)
			{
				m_StatusControl[i].elapsed = 0;
				m_StatusControl[i].enabled = !m_StatusControl[i].enabled;

				if (m_StatusControl[i].mode & STATUS_MODE_COUNTER)
				{
					m_StatusControl[i].times--;

					if (m_StatusControl[i].times == 0)
					{
						m_StatusControl[i].mode = 0;
						m_StatusControl[i].enabled = 0;
					}
				}
			}
		}
	}

	UpdateLedStatus();
}
