#include "app.h"
#include <Arduino.h>
#include <ArduinoJson.h>

/** Definitions */

/**
 * @brief Defines the WiFi channel to use
 */
#define WIFI_CHANNEL 6

/**
 * @brief Constructs a new Application object.
 */
Application::Application()
	: m_AppFlash()
	, m_AppRelay(m_AppFlash)
	, m_AppStatus(m_AppScheduler)
	, m_AppRules(m_AppRelay, m_AppStatus, m_AppFlash)
	, m_AppMqtt(m_AppScheduler, m_AppMesh, m_AppFlash, m_AppRelay)
	, m_AppNetwork(m_AppMesh, m_AppStatus, m_AppRules, m_AppMqtt)
{
#ifdef DEBUG_ENABLED
	Serial.println("Application Constructor");
#endif
}

/**
 * @brief Destroys the Application object.
 */
Application::~Application()
{
}

/**
 * @brief Sets up the application environment.
 */
void Application::Setup()
{
	/** Set msgs types in mesh network */
	m_AppMesh.setDebugMsgTypes(ERROR | STARTUP | CONNECTION);

	/** Init mesh */
	m_AppMesh.init(MESH_PREFIX, MESH_PASSWORD, &m_AppScheduler, MESH_PORT, WIFI_AP_STA);

	/** Setup WiFi */
	m_AppMqtt.Setup();

	/** Set central as ROOT node */
	m_AppMesh.setRoot(true);
	/** Advises that mesh network contains a root node */
	m_AppMesh.setContainsRoot(true);

	/** Make Sure app inits with no status */
	m_AppStatus.Clear();
}

/**
 * @brief The main loop of the application.
 */
void Application::Loop()
{
	m_AppMesh.update();
}
