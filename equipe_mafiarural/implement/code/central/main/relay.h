#ifndef _RELAY_H_FILE_
#define _RELAY_H_FILE_

#include "common.h"
#include "hardware.h"
#include "flash.h"
#include <stdint.h>

/** Enums */

/**
 * @brief Enumeration representing relay units.
 */
enum RelayUnit : uint8_t
{
	RELAY_UNIT0 = RELAY_0,
	RELAY_UNIT1 = RELAY_1,
	RELAY_UNIT2 = RELAY_2,
	RELAY_UNIT3 = RELAY_3,
	RELAY_UNIT4 = RELAY_4,
	RELAY_UNIT5 = RELAY_5,
	RELAY_UNIT6 = RELAY_6,
	RELAY_UNIT7 = RELAY_7,
};

/** Class */

/**
 * @brief The Relay class manages the system Relay block.
 */
class Relay
{
public:
	/**
	 * @brief Constructs a new Relay object.
	 */
	Relay(Flash &flash);

	/**
	 * @brief Destroys the Relay object.
	 */
	~Relay();

public:
	/**
	 * @brief Sets the relay unit to on.
	 */
	void Set(RelayUnit unit);

	/**
	 * @brief Sets the relay unit based on a uint8_t.
	 */
	void Set(uint8_t block);

	/**
	 * @brief Gets current state of the relay block.
	 */
	uint8_t Get();

	/**
	 * @brief Sets the relay unit to default state.
	 */
	void Reset();

	/**
	 * @brief Sets the relay unit to off.
	 */
	void Reset(RelayUnit unit);

public:
	/**
	 * @brief Gets if relay block is locked.
	 */
	inline bool IsLocked() const { return m_Locked; }

	/**
	 * @brief Locks relay block.
	 */
	inline void Lock() { m_Locked = true; }

	/**
	 * @brief Unlocks relay block.
	 */
	inline void UnLock() { m_Locked = false; }

private:
	/**
	 * @brief Marks default state of the relay.
	 */
	uint8_t m_DefaultState = 0b00000000;

	/**
	 * @brief Marks if relay block is locked.
	 */
	bool m_Locked = false;
};

#endif /* _RELAY_H_FILE_ */
