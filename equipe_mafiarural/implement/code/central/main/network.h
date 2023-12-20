#ifndef _NETWORK_H_FILE_
#define _NETWORK_H_FILE_

#include "common.h"
#include "status.h"
#include "rules.h"
#include "mqtt.h"
#include <painlessMesh.h>
#include <stdint.h>

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
	NetWork(painlessMesh &mesh, Status &status, RulesValidator& validator, Mqtt& mqtt);

	/**
	 * @brief Destroys the NetWork object.
	 */
	~NetWork();
private:
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
	 * @brief Callback function when some node request a master node.
	 * 
	 * @param from The node id from which the message was received.
	 */
	void OnRequestMaster(uint32_t from);

	/**
	 * @brief When some node sends data to master.
	 * 
	 * @param from The node id from which the message was received.
	 * @param msg The message received.
	 */
	void OnRequestData(uint32_t from, String &msg);

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
	 * @brief The rules validator of the application.
	 */
	RulesValidator &m_Validator;

	/**
	 * @brief The MQTT manager of the application.
	 */
	Mqtt &m_Mqtt;
};

#endif /* _NETWORK_H_FILE_ */
