#include "network.h"
#include <Arduino.h>
#include <ArduinoJson.h>

/**
 * @brief Constructs a new NetWork object.
 */
NetWork::NetWork(painlessMesh &mesh, Status &status)
	: m_Mesh(mesh)
	, m_Status(status)
{
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
 * @brief Used to send current sensing module data in mesh network.
 *
 * @param data The data to send.
 */
void NetWork::SendData(MessageSensorData &data)
{
	/** Check if there is a master */
	if (m_SearchingMaster || !m_Mesh.isConnected(m_MasterNodeId))
	{
		/** Broadcast again for a new master */
		return SearchMaster();
	}

	/** Change status to blink 100ms */
	m_Status.Set(STATUS_OK0, 100);

	DynamicJsonDocument payload(1024);

	/** Packs general mesh details */
	payload["message_type"] = MESSAGE_REQUEST_SEND_DATA;
	payload["node_id"] = m_Mesh.getNodeId();


	/** Pack board details */
	payload["board"]["id"] = BOARD_UNIQUE_ID;
	payload["board"]["type"] = BOARD_TYPE;
	payload["board"]["sensor_type"] = BOARD_SENSOR_TYPE;

	/** Packs sensor data */
	payload["data"]["mq5"] = data.mq5;
	payload["data"]["mq5.history"] = data.mq5History;
	payload["data"]["mq6"] = data.mq6;
	payload["data"]["mq6.history"] = data.mq6History;
	payload["data"]["mq7"] = data.mq7;
	payload["data"]["mq7.history"] = data.mq7History;

	String msg;
	serializeJson(payload, msg);

#ifdef DEBUG_ENABLED
	Serial.printf("Sending data to %u: %s\n", m_MasterNodeId, msg.c_str());
#endif

	/** Send payload */
	m_Mesh.sendSingle(m_MasterNodeId, msg.c_str());

	/** Clear status */
	m_Status.Clear(STATUS_OK0);
}

/**
 * @brief Searches for current master node to send data.
 */
void NetWork::SearchMaster()
{
#ifdef DEBUG_ENABLED
	Serial.printf("Searching master\n");
#endif
	/** Change status to blink 500ms */
	m_Status.Set(STATUS_ERROR, 500);
	/** Clear connected status */
	m_Status.Clear(STATUS_OK1);

	/** Set searching master flag */
	m_SearchingMaster = true;

	DynamicJsonDocument payload(1024);

	/** Packs payload */
	payload["message_type"] = MESSAGE_REQUEST_FIND_MASTER;
	payload["node_id"] = m_Mesh.getNodeId();

	String msg;
	serializeJson(payload, msg);

	/** Broadcast payload */
	m_Mesh.sendBroadcast(msg.c_str());
}

/**
 * @brief Callback function to receive data from other nodes in mesh.
 *
 * @param from The node id from which the message was received.
 * @param msg The message received.
 */
void NetWork::OnReceive(uint32_t from, String &msg)
{
#ifdef DEBUG_ENABLED
	Serial.printf("Received new message from %u: %s\n", from, msg.c_str());
#endif

	/** Parse message */
	DynamicJsonDocument payload(1024);
	DeserializationError error = deserializeJson(payload, msg.c_str());

	/** Check if message is valid */
	if (
		error.code() != error.Ok ||
		!payload.containsKey("message_type") ||
		!payload.containsKey("node_id")
	)
	{
#ifdef DEBUG_ENABLED
		Serial.printf(" - Invalid message received from %u\n", from);
#endif
		return;
	}

	switch (payload["message_type"].as<uint8_t>())
	{
	case MESSAGE_RESPONSE_FIND_MASTER:
		return OnFoundMasterMessage(payload["node_id"].as<uint32_t>());
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
 * @brief Parses a received message to request master node.
 * 
 * @param master Current master ID to use
 */
void NetWork::OnFoundMasterMessage(uint32_t master)
{
	/** Clear error status */
	m_Status.Clear(STATUS_ERROR);

	/** Change status to fixed */
	m_Status.Set(STATUS_OK1);

	/** Set searching master flag */
	m_SearchingMaster = false;

	/** Set master node id */
	m_MasterNodeId = master;
}
