#ifndef _NETWORK_H_FILE_
#define _NETWORK_H_FILE_

#include "common.h"
#include "status.h"
#include "painlessMesh.h"
#include <stdint.h>

/** Messages */

/**
 * @brief Message to send data to master.
 */
struct MessageSensorData
{
	uint8_t mq5; /**< MQ5 sensor value. */
	String mq5History; /**< MQ5 sensor value history. */
	uint8_t mq6; /**< MQ6 sensor value. */
	String mq6History; /**< MQ6 sensor value history. */
	uint8_t mq7; /**< MQ7 sensor value. */
	String mq7History; /**< MQ7 sensor value history. */
};

/** Class */

/**
 * @brief The NetWork class manages the system network.
 */
class NetWork
{
public:
	/**
	 * @brief Constructs a new NetWork object.
	 */
	NetWork(painlessMesh &mesh, Status &status);

	/**
	 * @brief Destroys the NetWork object.
	 */
	~NetWork();

public:
	/**
	 * @brief Used to send current sensing module data in mesh network.
	 * 
	 * @param data The data to send.
	 */
	void SendData(MessageSensorData &data);

private:
	/**
	 * @brief Searches for current master node to send data.
	 */
	void SearchMaster();

	/**
	 * @brief Callback function to receive data from other nodes in mesh.
	 *
	 * @param from The node id from which the message was received.
	 * @param msg The message received.
	 */
	void OnReceive(uint32_t from, String &msg);

	/**
	 * @brief Callback function when a new connection is established.
	 *
	 * @param nodeId The node id of the new connection.
	 */
	void OnNewConnection(uint32_t nodeId);

	/**
	 * @brief Callback function when a connection change its state.
	 */
	void OnChangedConnection();

	/**
	 * @brief Callback function when network time is adjusted
	 * 
	 * @param offset Time offset.
	 */
	void OnNodeTimeAdjusted(int32_t offset);

private:
	/**
	 * @brief Parses a received message to request master node.
	 * 
	 * @param master Current master ID to use
	 */
	void OnFoundMasterMessage(uint32_t master);

private:
	/**
	 * @brief The painlessMesh instance.
	 */
	painlessMesh &m_Mesh;

	/**
	 * @brief The status manager of the application.
	 * 
	 * Used to manage the system status.
	 */
	Status &m_Status;

	/**
	 * @brief Current connected master node id.
	 */
	uint32_t m_MasterNodeId;

	/**
	 * @brief Flag to indicate if the node is searching for a master node.
	 */
	bool m_SearchingMaster = false;
};

#endif /* _NETWORK_H_FILE_ */
