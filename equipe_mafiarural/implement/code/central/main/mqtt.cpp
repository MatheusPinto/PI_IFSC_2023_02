#include "mqtt.h"
#include <Arduino.h>

/**
 * @brief Constructs a new Mqtt object.
 */
Mqtt::Mqtt(Scheduler &appScheduler, painlessMesh &mesh, Flash &flash, Relay &relay)
	: m_Flash(flash)
	, m_Config(2048)
	, m_Relay(relay)
	, m_MqttClient(m_WiFiClient)
	, m_Mesh(mesh)
	, m_ReconnectMqttTask(TASK_MILLISECOND * MQTT_RECONNECT_INTERVAL, TASK_FOREVER, [this]() { this->ReconnectMQTT(); })
	, m_KeepAliveTask(TASK_MILLISECOND * MQTT_LOOP_INTERVAL, TASK_FOREVER, [this]() { this->KeepAlive(); })
	, m_PublishStateTask(TASK_MILLISECOND * MQTT_PUBLISH_STATE_INTERVAL, TASK_FOREVER, [this]() { this->PublishRelayStatus(); })
{
#ifdef DEBUG_ENABLED
	Serial.println("Mqtt Constructor");
#endif

	m_Config = m_Flash.ReadConfig();

	/** Add tasks */
	appScheduler.addTask(m_KeepAliveTask);
	appScheduler.addTask(m_ReconnectMqttTask);
	appScheduler.addTask(m_PublishStateTask);
}

/**
 * @brief Sets up the application environment.
 */
void Mqtt::Setup()
{
	/** Configure WiFi */
	InitWiFi();

	/** Configure MQTT broker */
	InitMQTT();

	m_KeepAliveTask.enable();
	m_ReconnectMqttTask.enable();
}

/**
 * @brief Destroys the Mqtt object.
 */
Mqtt::~Mqtt()
{
}

/**
 * @brief Initializes the WiFi connection.
 */
void Mqtt::InitWiFi()
{

#ifdef DEBUG_ENABLED
	Serial.println("Starting WiFi");
#endif

	if (
		m_Config.containsKey("wifi") &&
		m_Config["wifi"].containsKey("ssid") &&
		m_Config["wifi"].containsKey("password") &&
		m_Config["wifi"].containsKey("hostname")
	)
	{
		String ssid = m_Config["wifi"]["ssid"].as<String>();
		String password = m_Config["wifi"]["password"].as<String>();
		String hostname = m_Config["wifi"]["hostname"].as<String>();

#ifdef DEBUG_ENABLED
		Serial.println(" - Using WiFi configuration");
		Serial.printf("   - SSID: %s\n", ssid.c_str());
		Serial.printf("   - Hostname: %s\n", hostname.c_str());
#endif

		m_Mesh.stationManual("zenite", "zenite2019");
		m_Mesh.setHostname(hostname.c_str());

		return;
	}

#ifdef DEBUG_ENABLED
	Serial.println(" - No WiFi configuration found");
#endif
}

/**
 * @brief Initializes the MQTT connection.
 */
void Mqtt::InitMQTT()
{

#ifdef DEBUG_ENABLED
	Serial.println("Starting MQTT");
#endif

	if (
		m_Config.containsKey("mqtt") &&
		m_Config["mqtt"].containsKey("host") &&
		m_Config["mqtt"].containsKey("port")
	)
	{
		const char *host = m_Config["mqtt"]["host"].as<String>().c_str();
		uint16_t port = m_Config["mqtt"]["port"].as<uint16_t>();

#ifdef DEBUG_ENABLED
		Serial.println("Broker Details");
		Serial.printf(" - Broker: %s\n", host);
		Serial.printf(" - Port: %d\n", port);
#endif

		m_MqttClient.setServer(host, port);
		m_MqttClient.setCallback(
			[this](char *topic, byte *payload, unsigned int length) {
				this->MqttCallback(topic, payload, length);
			}
		);

		return;
	}
}

/**
 * @brief Stablish the MQTT connection.
 */
void Mqtt::ReconnectMQTT()
{
	if (m_MqttClient.connected())
		return;

#ifdef DEBUG_ENABLED
	Serial.println("Connecting to MQTT...");
#endif

	if (
		(!m_Config.containsKey("mqtt") &&
		!m_Config["mqtt"].containsKey("id") &&
		!m_Config["mqtt"].containsKey("topics")) ||
		!WiFi.isConnected()
	)
	{
#ifdef DEBUG_ENABLED
		Serial.println(" - No MQTT configuration found or no Internet connection");
#endif

		return;
	}

	/** Disable Reconnect Task */
	m_ReconnectMqttTask.disable();

	/** Set MQTT connection parameters */
	const char *mqttId = m_Config["mqtt"]["uniqueId"].as<String>().c_str();

	while (
		!m_MqttClient.connected() &&
		WiFi.isConnected()
	) 
	{
#ifdef DEBUG_ENABLED
		Serial.printf(" - Attempting MQTT connection as %s...\n", mqttId);
#endif

		if (m_MqttClient.connect(mqttId))
		{
	#ifdef DEBUG_ENABLED
			Serial.println("MQTT connected");
	#endif
			/** Subscribe in Relay topics */
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["0"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["1"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["2"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["3"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["4"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["5"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["6"]["in"].as<String>().c_str());
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["relay"]["7"]["in"].as<String>().c_str());
			/** Subscribe in validator topic */
			m_MqttClient.subscribe(m_Config["mqtt"]["topics"]["validator"]["in"].as<String>().c_str());

			/** Enable Publish State Task */
			m_PublishStateTask.enable();
		}
		else
		{
	#ifdef DEBUG_ENABLED
			Serial.println("Failed to connect to MQTT");
			Serial.printf(" - Error: %d\n", m_MqttClient.state());
			Serial.printf(" - WiFi connected: %d\n", WiFi.isConnected());
	#endif
			/** Disable Publish State Task */
			m_PublishStateTask.disable();

			m_MqttClient.disconnect();
		}
	}

	/** Enable Reconnect Task */
	m_ReconnectMqttTask.enable();
}

/**
 * @brief Publishes a message to the MQTT broker.
 */
void Mqtt::Publish(String topic, String payload)
{
	if (!m_MqttClient.connected())
		return;

#ifdef DEBUG_ENABLED
	Serial.printf("Publishing to topic %s: %s\n", topic.c_str(), payload.c_str());
#endif

	m_MqttClient.publish(topic.c_str(), payload.c_str());
}

/**
 * @brief Keeps the MQTT connection alive.
 */
void Mqtt::KeepAlive()
{
	m_MqttClient.loop();
}

/**
 * @brief Publishes the relay status to the MQTT broker.
 */
void Mqtt::PublishRelayStatus()
{
	if (!m_MqttClient.connected())
		return;

	/** Get relay status */
	uint8_t relayStatus = m_Relay.Get();

#ifdef DEBUG_ENABLED
	Serial.printf("Relay status: %d\n", relayStatus);
#endif

	bool relayLocked = m_Relay.IsLocked();

	/** Publish relay status */
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["1"]["out"].as<String>(),
		String(relayStatus & 0b00000010 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["2"]["out"].as<String>(),
		String(relayStatus & 0b00000100 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["3"]["out"].as<String>(),
		String(relayStatus & 0b00001000 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["4"]["out"].as<String>(),
		String(relayStatus & 0b00010000 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["5"]["out"].as<String>(),
		String(relayStatus & 0b00100000 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["6"]["out"].as<String>(),
		String(relayStatus & 0b01000000 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["relay"]["7"]["out"].as<String>(),
		String(relayStatus & 0b10000000 ? "off" : "on")
	);
	Publish(
		m_Config["mqtt"]["topics"]["validator"]["out"].as<String>(),
		String(relayLocked ? "on" : "off")
	);
}

/**
 * @brief Callback for MQTT messages.
 */
void Mqtt::MqttCallback(char *topic, byte *payload, unsigned int length)
{
#ifdef DEBUG_ENABLED
	Serial.printf("Message arrived [%s]: ", topic);
#endif

	/** Extracts payload */
	String msg;
	String topicStr = String(topic);

	for(int i = 0; i < length; ++i) 
	{
		char c = (char)payload[i];
		msg += c;
	}

#ifdef DEBUG_ENABLED
	Serial.println(msg);
#endif

	for (uint8_t i = 0; i < 8; ++i)
	{
		if (topicStr == m_Config["mqtt"]["topics"]["relay"][String(i)]["in"].as<String>())
		{
			if (msg == "on")
			{
				m_Relay.Set((~m_Relay.Get()) | ((uint8_t)(1U << i)));
			}
			else if (msg == "off")
			{
				m_Relay.Set((~m_Relay.Get()) & ~((uint8_t)(1U << i)));
			}

			Publish(
				m_Config["mqtt"]["topics"]["relay"][String(i)]["out"].as<String>(),
				String(m_Relay.Get() & (1 << i) ? "off" : "on")
			);
		}
	}

	if (
		topicStr == m_Config["mqtt"]["topics"]["validator"]["in"].as<String>() &&
		msg == "off"
	)
	{
		#ifdef DEBUG_ENABLED
			Serial.println("Unlocking relay block");
		#endif
		m_Relay.UnLock();

		Publish(
			m_Config["mqtt"]["topics"]["validator"]["out"].as<String>(),
			String("off")
		);
	}
}
