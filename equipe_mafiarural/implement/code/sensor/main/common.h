#ifndef _COMMON_H_FILE_
#define _COMMON_H_FILE_

/**
 * General defintions for the sensor module, this file MUST be modified to
 * match the specifics purpose of the module, make sure to change the
 * BOARD_UNIQUE_ID and BOARD_TYPE
 */

/** -- Device */

/**
 * @brief Comment this line to disable debug messages.
 */
#define DEBUG_ENABLED

/**
 * @brief Defines the baud rate of the serial port.
 */
#define SERIAL_BAUD_RATE 115200

/** -- Board Typing */

/**
 * @brief Defines a UNIQUE ID for this board to be used to identify in the network.
 */
#define BOARD_UNIQUE_ID "7f32eebc35b74390"

/**
 * @brief Defines if this board is a master node or a slave node.
 */
#define BOARD_TYPE "node"

/**
 * @brief Defines the type of sensor of this board.
 */
#define BOARD_SENSOR_TYPE "sensor/gas"

/**
 * @brief Amount of points for the chart
 */
#define CHART_POINTS 20


/** -- Network Section */

/**
 * @brief Defines the name of the mesh network.
 */
#define MESH_PREFIX "19dd4de928864aed"

/**
 * @brief Defines the password of the mesh network.
 */
#define MESH_PASSWORD "ed2855619c2a4b88"

/**
 * @brief Defines the port of the mesh network.
 */
#define MESH_PORT 35555

/** ---- Messages */

/**
 * Messages IDs
 * 
 * All messages must have a message type to be identified by the receiver and to
 * identify the intention of the sender.
 * 
 * The message type is a 8-bit unsigned integer, the first bit is used to indicate
 * if the message is a request or a response, the remaining 7 bits are used to
 * identify the message type.
 * 
 * For request messages, the first bit must be 0, for response messages, the first
 * bit must be 1.
 * 
 * For example, the message type 0b00000001 is a request message, and the message
 * type 0b10000001 is a response message.
 */

/**
 * @brief Defines the message id to request master node.
 */
#define MESSAGE_REQUEST_FIND_MASTER (uint8_t)0b00000001U

/**
 * @brief Defines the message id to response master node.
 */
#define MESSAGE_RESPONSE_FIND_MASTER (uint8_t)0b10000001U

/**
 * @brief Defines the message id to send data to master node.
 */
#define MESSAGE_REQUEST_SEND_DATA (uint8_t)0x00000010U

/**
 * @brief Defines the message id to response data to master node.
 */
#define MESSAGE_RESPONSE_SEND_DATA (uint8_t)0b10000010U

#endif /* _COMMON_H_FILE_ */
