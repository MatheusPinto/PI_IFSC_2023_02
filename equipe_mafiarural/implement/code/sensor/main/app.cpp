#include "app.h"
#include <Arduino.h>

/**
 * @brief Constructs a new Application object.
 */
Application::Application()
	: m_AppStatus(m_AppScheduler)
	, m_AppSensing(m_AppScheduler)
	, m_AppNetwork(m_AppMesh, m_AppStatus)
	, m_AppTask(TASK_MILLISECOND * APP_POOLING_INTERVAL_MS, TASK_FOREVER, [this]() { this->RunApp(); })
{
	/** Add update task */
	m_AppScheduler.addTask(m_AppTask);

	/** Enable update task */
	m_AppTask.enable();
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
#ifdef DEBUG_ENABLED
	Serial.begin(SERIAL_BAUD_RATE);
#endif

	/** Set msgs types in mesh network */
	m_AppMesh.setDebugMsgTypes(ERROR | STARTUP);
	/** Init mesh */
	m_AppMesh.init(MESH_PREFIX, MESH_PASSWORD, &m_AppScheduler, MESH_PORT);

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

/**
 * @brief Runs the application main loop task
 */
void Application::RunApp()
{
	/** Fetch last reads from sensor */
	uint8_t mq5 = m_AppSensing.Read(SENSOR_MQ5);
	uint8_t mq6 = m_AppSensing.Read(SENSOR_MQ6);
	uint8_t mq7 = m_AppSensing.Read(SENSOR_MQ7);

	/** Generates message payload */
	MessageSensorData data = {
		.mq5 = mq5,
		.mq5History = "[",
		.mq6 = mq6,
		.mq6History = "[",
		.mq7 = mq7,
		.mq7History = "[",
	};

	/** Copy history to string */
	for (int i = 0; i < CHART_POINTS; ++i)
	{
		data.mq5History += String(m_AppSensing.ReadHistory(SENSOR_MQ5)[i]) + ",";
		data.mq6History += String(m_AppSensing.ReadHistory(SENSOR_MQ6)[i]) + ",";
		data.mq7History += String(m_AppSensing.ReadHistory(SENSOR_MQ7)[i]) + ",";
	}

	/** Remove last comma */
	data.mq5History.setCharAt(data.mq5History.length() - 1, ']');
	data.mq6History.setCharAt(data.mq6History.length() - 1, ']');
	data.mq7History.setCharAt(data.mq7History.length() - 1, ']');

	/** Send data to mesh network */
	m_AppNetwork.SendData(data);
}
