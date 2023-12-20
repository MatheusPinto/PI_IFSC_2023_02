#ifndef _HARDWARE_H_FILE_
#define _HARDWARE_H_FILE_

/**
 * Physical board hardware definitions
 */

/** MQ Sensors PINs */
#define SENSOR_MQ_5_PIN (uint8_t)34U
#define SENSOR_MQ_6_PIN (uint8_t)39U
#define SENSOR_MQ_7_PIN (uint8_t)36U

/** Status LEDs PINS */
#define STATUS_SUCCESS_LED0_PIN (uint8_t)22U
#define STATUS_SUCCESS_LED1_PIN (uint8_t)23U
#define STATUS_FAIL_LED0_PIN (uint8_t)21U

/** ESP32 Hardware definitions */
#define ESP_MAX_ADC_VALUE 4096U

#endif /* _HARDWARE_H_FILE_ */
