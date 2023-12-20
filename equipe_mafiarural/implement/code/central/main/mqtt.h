#ifndef _MQTT_H_FILE_
#define _MQTT_H_FILE_

#include "common.h"
#include "flash.h"
#include "relay.h"
#include <painlessMesh.h>
#include <PubSubClient.h>
#include <WiFiClient.h>
#include <stdint.h>

/** Definitions */

/**
 * @brief Time interval for the check and reconnect task for the MQTT connection.
 */
#define MQTT_RECONNECT_INTERVAL 10000

/**
 * @brief Time interval to update current MQTT relay block status
 */
#define MQTT_PUBLISH_STATE_INTERVAL 2000

/**
 * @brief Time interval update main loop of MQTT.
 */
#define MQTT_LOOP_INTERVAL 100

/** Class */

/**
 * @brief The Mqtt class manages the system Mqtt block.
 */
class Mqtt
{
public:
	/**
	 * @brief Constructs a new Mqtt object.
	 */
	Mqtt(Scheduler &appScheduler, painlessMesh &mesh, Flash &flash, Relay &relay);

	/**
	 * @brief Destroys the Mqtt object.
	 */
	~Mqtt();

public:
	/**
	 * @brief Publishes a message to the MQTT broker.
	 */
	void Publish(String topic, String payload);

	/**
	 * @brief Sets up the application environment.
	 */
	void Setup();

private:
	/**
	 * @brief Initializes the MQTT connection.
	 */
	void InitWiFi();

	/**
	 * @brief Initializes the MQTT connection.
	 */
	void InitMQTT();

private:
	/**
	 * @brief Stablish the MQTT connection.
	 */
	void ReconnectMQTT();

	/**
	 * @brief Keeps the MQTT connection alive.
	 */
	void KeepAlive();

	/**
	 * @brief Callback for MQTT messages.
	 */
	void MqttCallback(char *topic, byte *payload, unsigned int length);

	/**
	 * @brief Publishes the relay status to the MQTT broker.
	 */
	void PublishRelayStatus();

private:
	/**
	 * @brief Flash instance
	 */
	Flash &m_Flash;

	/**
	 * @brief Config instance
	 */
	DynamicJsonDocument m_Config;

	/**
	 * @brief Relay instance
	 */
	Relay &m_Relay;

	/**
	 * @brief The WiFi client.
	 */
	WiFiClient m_WiFiClient;

	/**
	 * @brief The MQTT client.
	 */
	PubSubClient m_MqttClient;

	/**
	 * @brief The mesh network.
	 */
	painlessMesh &m_Mesh;

	/**
	 * @brief The task to reconnect MQTT connection.
	 */
	Task m_ReconnectMqttTask;

	/**
	 * @brief The task to keep MQTT connection alive.
	 */
	Task m_KeepAliveTask;

	/**
	 * @brief The task to keep MQTT connection alive.
	 */
	Task m_PublishStateTask;
};

#endif /* _MQTT_H_FILE_ */
