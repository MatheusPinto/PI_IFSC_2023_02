#include "flash.h"
#include "hardware.h"
#include <Arduino.h>

/** Definitions */

/**
 * @brief Define the path to config file
 */
#define CONFIG_PATH "/config.json"

/**
 * @brief Define the SD card chunk size
 */
#define SD_CHUNK_SIZE 1048576U

/** Class */

/** Initializes static member */
bool Flash::s_HardwareInitialized = false;

/**
 * @brief Constructs a new Flash object.
 */
Flash::Flash()
{
	/** Initializes SD card */
	if (!Flash::s_HardwareInitialized) {
		pinMode(SD_CS, OUTPUT);

		if (!SD.begin(SD_CS))
		{
	#ifdef DEBUG_ENABLED
			Serial.println("Card Mount Failed");
	#endif
			return;
		}

		Flash::s_HardwareInitialized = true;
	}

	/** Tries to fetch type of card */
	uint8_t cardType = SD.cardType();

	if (cardType == CARD_NONE)
	{
#ifdef DEBUG_ENABLED
		Serial.println("No SD card attached");
#endif
		return;
	}

#ifdef DEBUG_ENABLED
	Serial.print("SD card connected, Card type: ");

	switch (cardType)
	{
	case CARD_MMC:
		Serial.print("MMC");
		break;
	case CARD_SD:
		Serial.print("SDSC");
		break;
	case CARD_SDHC:
		Serial.print("SDHC");
		break;
	default:
		Serial.print("UNKNOWN");
	}

	Serial.printf(
		"SD Card Size: %lluMB\n", SD.cardSize() / SD_CHUNK_SIZE
	);
#endif

	m_IsInitialized = true;
}

/**
 * @brief Destroys the Flash object.
 */
Flash::~Flash()
{
}

/**
 * @brief Checks if a given file exists in the SD card.
 * 
 * @param path The path to write to
 * @param data The data to write
 */
bool Flash::Exists(String path)
{
	if (!m_IsInitialized)
	{
#ifdef DEBUG_ENABLED
		Serial.println("SD card not initialized");
#endif
		return false;
	}

	return SD.exists(path);
}

/**
 * @brief Reads a string from the SD card.
 * 
 * @param path The path to read from
 * @return String The read string
 */
String Flash::Read(String path)
{
	File file = SD.open(path);

	if(!file)
	{
#ifdef DEBUG_ENABLED
		Serial.println("Failed to open file for reading");
		Serial.println(path);
#endif
		return String();
	}

	String data = file.readString();

	/** Closes file */
	file.close();

	return data;
}

/**
 * @brief Reads a Json from the SD card.
 * 
 * @param path The path to read from
 * @return Json from the read string
 */
DynamicJsonDocument Flash::ReadJson(String path)
{
	String data = Read(path);

	/** Parses config file */
	DynamicJsonDocument jsonData(2048);

#ifdef DEBUG_ENABLED
	DeserializationError error =
#endif
	deserializeJson(jsonData, data);

#ifdef DEBUG_ENABLED
	if (error.code() != error.Ok)
	{
		Serial.println("Failed to parse file");
	}
#endif

	return jsonData;
}

/**
 * @brief Reads the config file from the SD card.
 * 
 * @return DynamicJsonDocument The read config
 */
DynamicJsonDocument Flash::ReadConfig()
{
	/** Parses config file */
	DynamicJsonDocument config(2048);

	/** Checks if config file exists */
	if (!Exists(CONFIG_PATH))
	{
#ifdef DEBUG_ENABLED
		Serial.println("Config file not found");
#endif
		return config;
	}

	/** Reads config file */
	String data = Read(CONFIG_PATH);

#ifdef DEBUG_ENABLED
	DeserializationError error =
#endif
	deserializeJson(config, data);

#ifdef DEBUG_ENABLED
	if (error.code() != error.Ok)
	{
		Serial.println("Failed to parse file");
	}
#endif

	return config;
}
