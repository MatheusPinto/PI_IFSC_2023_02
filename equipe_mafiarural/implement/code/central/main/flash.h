#ifndef _FLASH_H_FILE_
#define _FLASH_H_FILE_

#include "common.h"
#include <FS.h>
#include <SD.h>
#include <SPI.h>
#include <stdint.h>
#include <ArduinoJson.h>

/** Class */

/**
 * @brief Manages the flash SD card
 */
class Flash
{
public:
	/**
	 * @brief Constructs a new Flash object.
	 */
	Flash();

	/**
	 * @brief Destroys the Flash object.
	 */
	~Flash();
public:
	/**
	 * @brief Checks if a given file exists in the SD card.
	 * 
	 * @param path The path to write to
	 * @param data The data to write
	 */
	bool Exists(String path);

	/**
	 * @brief Reads a string from the SD card.
	 * 
	 * @param path The path to read from
	 * @return String The read string
	 */
	String Read(String path);

	/**
	 * @brief Reads a Json from the SD card.
	 * 
	 * @param path The path to read from
	 * @return Json from the read string
	 */
	DynamicJsonDocument ReadJson(String path);

public:
	/**
	 * @brief Reads the config file from the SD card.
	 * 
	 * @return DynamicJsonDocument The read config
	 */
	DynamicJsonDocument ReadConfig();

public:
	/**
	 * @brief Marks if SD is already initialized
	 */
	static bool s_HardwareInitialized;

private:
	/**
	 * @brief Marks if the SD card is initialized
	 */
	bool m_IsInitialized = false;
};

#endif /* _FLASH_H_FILE_ */
