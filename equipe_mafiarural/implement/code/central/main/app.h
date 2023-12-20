#ifndef _APP_H_FILE_
#define _APP_H_FILE_

#include "common.h"
#include "serial.h"
#include "flash.h"
#include "relay.h"
#include "status.h"
#include "rules.h"
#include "network.h"
#include "mqtt.h"
#include <painlessMesh.h>

/** Class */

/**
 * @brief The Application class manages the main functionality of the program.
 *
 * This class is responsible for initializing, running, and cleaning up the
 * application.
 */
class Application
{
public:
	/**
	 * @brief Constructs a new Application object.
	 */
	Application();

	/**
	 * @brief Destroys the Application object.
	 */
	~Application();

public:
	/**
	 * @brief Sets up the application environment.
	 */
	void Setup();

	/**
	 * @brief The main loop of the application.
	 */
	void Loop();

private:
	/**
	 * @brief App serial wrapper
	 */
	AppSerial m_AppSerial;

	/**
	 * @brief The mesh network manager of the application.
	 * 
	 * Used to manage the mesh network.
	 */
	painlessMesh m_AppMesh;

	/**
	 * @brief The main scheduler of the application.
	 * 
	 * Used to schedule tasks to run at specific intervals and to allow it to
	 * operate together with the ESP32's WiFi stack.
	 */
	Scheduler m_AppScheduler;

	/**
	 * @brief The flash manager of the application.
	 * 
	 * Used to manage the system flash.
	 */
	Flash m_AppFlash;

	/**
	 * @brief The relay manager of the application.
	 * 
	 * Used to manage the system relay.
	 */
	Relay m_AppRelay;

	/**
	 * @brief The status manager of the application.
	 * 
	 * Used to manage the system status.
	 */
	Status m_AppStatus;

	/**
	 * @brief The rules manager of the application.
	 * 
	 * Used to manage the system rules.
	 */
	RulesValidator m_AppRules;

	/**
	 * @brief The MQTT manager of the application.
	 * 
	 * Used to manage the system MQTT.
	 */
	Mqtt m_AppMqtt;

	/**
	 * @brief The network manager of the application.
	 * 
	 * Used to manage the system network.
	 */
	NetWork m_AppNetwork;
};

#endif // _APP_H_FILE_
