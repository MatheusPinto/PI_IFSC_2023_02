#include "rules.h"
#include <Arduino.h>

/** Definitions */

/**
 * @brief Define the SD card chunk size
 */
#define RULES_PREFIX "/rules/"

/** Class */

/**
 * @brief Constructs a new RulesValidator object.
 */
RulesValidator::RulesValidator(Relay &relay, Status &status, Flash &flash)
	: m_LastRule(2048)
	, m_Flash(flash)
	, m_Relay(relay)
	, m_Status(status)
{
#ifdef DEBUG_ENABLED
	Serial.println("RulesValidator Constructor");
#endif
}

/**
 * @brief Destroys the RulesValidator object.
 */
RulesValidator::~RulesValidator()
{
}

/**
 * @brief Validates the rules and make needed actions.
 */
void RulesValidator::Validate(String path, String unit, uint16_t value)
{
	/** If its already triggered, only app or reset can remove it */
	if (m_Relay.IsLocked())
	{
		return;
	}

	/** Checks if needs to load rule from SD */
	if (m_LastPath != path)
	{
		m_LastPath = path;
		m_LastRule = m_Flash.ReadJson(RULES_PREFIX + path);
	}

	/** If unit is not found skip */
	if (
		!m_LastRule.containsKey("condition") ||
		!m_LastRule["condition"].containsKey(unit)
	)
	{
		return;
	}

	/** Gets the rule */
	uint16_t r = m_LastRule["condition"][unit]["value"].as<uint16_t>();
	String op = m_LastRule["condition"][unit]["comparator"].as<String>();
	uint8_t action = m_LastRule["condition"][unit]["action"].as<uint8_t>();

	/** Checks if rule is triggered */
	if (EvaluateComparison(value, op, r))
	{
#ifdef DEBUG_ENABLED
		Serial.println("Rule triggered");
		Serial.printf(" - Path %s\n", path.c_str());
		Serial.printf(" - Unit %s\n", unit.c_str());
		Serial.printf(" - Value %d\n", value);
		Serial.printf(" - Comparator %s\n", op.c_str());
		Serial.printf(" - Rule value %d\n", r);
#endif
		/** Set error state */
		m_Status.Set(STATUS_ERROR, 500);

		/** Runs action */
		m_Relay.Set(action);

		/** Locks relay block */
		m_Relay.Lock();
	}
}

/**
 * @brief Runs a given comparator
 */
bool RulesValidator::EvaluateComparison(uint16_t l, String op, uint16_t r)
{
	if (op == "==")
		return l == r;
	else if (op == "!=")
		return l != r;
	else if (op == ">")
		return l > r;
	else if (op == ">=")
		return l >= r;
	else if (op == "<")
		return l < r;
	else if (op == "<=")
		return l <= r;

	return false;
}
