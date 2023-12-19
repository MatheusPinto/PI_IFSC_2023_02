#include "network.h"
#include <Arduino.h>
#include <ArduinoJson.h>

/**
 * @brief Constructs a new NetWork object.
 */
NetWork::NetWork(painlessMesh &mesh, Status &status, RulesValidator& validator, Mqtt& mqtt)
	: m_Mesh(mesh)
	, m_Status(status)
	, m_Validator(validator)
	, m_Mqtt(mqtt)
{
#ifdef DEBUG_ENABLED
	Serial.println("NetWork Constructor");
#endif
	/** Set callbacks */
	m_Mesh.onReceive([this](uint32_t from, String &msg) -> void { this->OnReceive(from, msg); });
	m_Mesh.onNewConnection([this](uint32_t nodeId) -> void { this->OnNewConnection(nodeId); });
	m_Mesh.onChangedConnections([this]() -> void { this->OnChangedConnection(); });
	m_Mesh.onNodeTimeAdjusted([this](int32_t offset) -> void { this->OnNodeTimeAdjusted(offset); });
}

/**
 * @brief Destroys the NetWork object.
 */
NetWork::~NetWork()
{
}

/**
 * @brief Callback function to receive data from other nodes in mesh.
 *
 * @param from The node id from which the message was received.
 * @param msg The message received.
 */
void NetWork::OnReceive(uint32_t from, String& msg)
{
#ifdef DEBUG_ENABLED
	Serial.printf("Received new message from %u: %s\n", from, msg.c_str());
#endif

	/** Parse message */
	DynamicJsonDocument payload(2048);
	DeserializationError error = deserializeJson(payload, msg.c_str());

	/** Check if message is valid */
	if (
		(error.code() != error.Ok) ||
		(!payload.containsKey("message_type")) ||
		(!payload.containsKey("node_id"))
	)
	{
#ifdef DEBUG_ENABLED
		Serial.printf(" - Invalid message received from %u Error  %s\n", from, error.c_str());
#endif
		return;
	}

	switch (payload["message_type"].as<uint8_t>())
	{
	case MESSAGE_REQUEST_FIND_MASTER:
		return OnRequestMaster(from);
	case MESSAGE_REQUEST_SEND_DATA:
		return OnRequestData(from, msg);
	default:
		break;
	}
}

/**
 * @brief Callback function when a new connection is established.
 *
 * @param nodeId The node id of the new connection.
 */
void NetWork::OnNewConnection(uint32_t nodeId)
{
#ifdef DEBUG_ENABLED
	Serial.printf(" - New connection in mesh, nodeId = %u\n", nodeId);
#endif
}

/**
 * @brief Callback function when a connection change its state.
 */
void NetWork::OnChangedConnection()
{
#ifdef DEBUG_ENABLED
	Serial.printf("Changed connections\n");
#endif
}

/**
 * @brief Callback function when network time is adjusted
 * 
 * @param offset Time offset.
 */
void NetWork::OnNodeTimeAdjusted(int32_t offset)
{
#ifdef DEBUG_ENABLED
	Serial.printf("Adjusted time %u. Offset = %d\n", m_Mesh.getNodeTime(), offset);
#endif
}

/**
 * @brief Callback function when some node request a master node.
 * 
 * @param from The node id from which the message was received.
 * @param msg The message received.
 */
void NetWork::OnRequestMaster(uint32_t from)
{
#ifdef DEBUG_ENABLED
	Serial.printf("Received request master message from %u\n", from);
#endif

	DynamicJsonDocument payload(2048);

	/** Packs payload */
	payload["message_type"] = MESSAGE_RESPONSE_FIND_MASTER;
	payload["node_id"] = m_Mesh.getNodeId();

	String msg;
	serializeJson(payload, msg);

	/** Send payload */
	m_Mesh.sendSingle(from, msg.c_str());
}

/**
 * @brief When some node sends data to master.
 * 
 * @param from The node id from which the message was received.
 * @param msg The message received.
 */
void NetWork::OnRequestData(uint32_t from, String &msg)
{
#ifdef DEBUG_ENABLED
	Serial.printf("Received request data message from %u: %s\n", from, msg.c_str());
#endif

	DynamicJsonDocument payload(2048);

	DeserializationError error = deserializeJson(payload, msg.c_str());

	/** Validates data key */
	if (
		(error.code() != error.Ok) ||
		!payload.containsKey("data") ||
		!payload.containsKey("board") ||
		!payload["data"].containsKey("mq5") ||
		!payload["data"].containsKey("mq6") ||
		!payload["data"].containsKey("mq7") ||
		!payload["board"].containsKey("id") ||
		!payload["board"].containsKey("type") ||
		!payload["board"].containsKey("sensor_type")
	)
	{
#ifdef DEBUG_ENABLED
		Serial.printf(" - Invalid message received from %u\n", from);
#endif
		return;
	}

	/** Extracts general node data */
	String uniqueId = payload["board"]["id"].as<String>();
	String boardType = payload["board"]["type"].as<String>();
	String boardSensorType = payload["board"]["sensor_type"].as<String>();

#ifdef DEBUG_ENABLED
	Serial.printf(" - Valid message received from %u\n", from);
	Serial.printf("   - Unique id: %s\n", uniqueId.c_str());
	Serial.printf("   - Board type: %s\n", boardType.c_str());
	Serial.printf("   - Board sensor type: %s\n", boardSensorType.c_str());
#endif

	for (JsonPair unitData : payload["data"].as<JsonObject>())
	{
#ifdef DEBUG_ENABLED
		Serial.printf("   - Unit: %s\n", unitData.key().c_str());
		Serial.printf("     - Value: %d\n", unitData.value().as<uint16_t>());
#endif

		if (String(unitData.key().c_str()).indexOf(".history") == -1)
		{
			String path = boardType + '.' + boardSensorType + ".json";
			path.replace("/", ".");

			m_Validator.Validate(
				path,
				unitData.key().c_str(),
				unitData.value().as<uint16_t>()
			);
		}

		m_Mqtt.Publish(
			boardType + "/" + boardSensorType + "/" + uniqueId.c_str() + "/" + unitData.key().c_str(),
			unitData.value().as<String>().c_str()
		);
	}
}
