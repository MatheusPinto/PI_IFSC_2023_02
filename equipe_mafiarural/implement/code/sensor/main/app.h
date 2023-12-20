#ifndef _APP_H_FILE_
#define _APP_H_FILE_

#include "common.h"
#include "status.h"
#include "sensing.h"
#include "network.h"
#include "painlessMesh.h"

/** Definitions */

#define APP_POOLING_INTERVAL_MS (uint16_t)1000U

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
	 * @brief Runs the application main loop task
	 */
	void RunApp();

private:
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
	 * @brief The status manager of the application.
	 * 
	 * Used to manage the system status.
	 */
	Status m_AppStatus;

	/**
	 * @brief The sensing manager of the application.
	 * 
	 * Used to manage the system sensing.
	 */
	Sensing m_AppSensing;

	/**
	 * @brief The network manager of the application.
	 * 
	 * Used to manage the system network.
	 */
	NetWork m_AppNetwork;

	/**
	 * @brief Application system update task
	 */
	Task m_AppTask;
};

#endif // _APP_H_FILE_
