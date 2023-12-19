#ifndef _RULES_H_FILE_
#define _RULES_H_FILE_

#include "common.h"
#include "flash.h"
#include "relay.h"
#include "status.h"
#include <stdint.h>
#include <ArduinoJson.h>

/** Class */

/**
 * @brief The RulesValidator class manages the system rules.
 */
class RulesValidator
{
public:
	/**
	 * @brief Constructs a new RulesValidator object.
	 */
	RulesValidator(Relay &relay, Status &status, Flash &flash);

	/**
	 * @brief Destroys the RulesValidator object.
	 */
	~RulesValidator();

public:
	/**
	 * @brief Validates the rules and make needed actions.
	 */
	void Validate(String path, String unit, uint16_t value);

private:
	/**
	 * @brief Runs a given comparator
	 */
	bool EvaluateComparison(uint16_t l, String op, uint16_t r);

private:
	/**
	 * @brief Last read path for small cache in SD reads
	 */
	String m_LastPath = "";

	/**
	 * @brief Last read rule for cache in SD reads
	 */
	DynamicJsonDocument m_LastRule;

	/**
	 * @brief The flash object.
	 */
	Flash &m_Flash;

	/**
	 * @brief The relay object.
	 */
	Relay &m_Relay;

	/**
	 * @brief The status object.
	 */
	Status &m_Status;
};

#endif /* _RULES_H_FILE_ */
