#ifndef _HARDWARE_H_FILE_
#define _HARDWARE_H_FILE_

/**
 * Physical board hardware definitions
 */

/** SD card PINs */
#define SD_MOSI (uint8_t)23U
#define SD_MISO (uint8_t)19U
#define SD_SCK (uint8_t)18U
#define SD_CS (uint8_t)5U

/** MQ Sensors PINs */
#define RELAY_0 (uint8_t)2U
#define RELAY_1 (uint8_t)4U
#define RELAY_2 (uint8_t)21U
#define RELAY_3 (uint8_t)22U
#define RELAY_4 (uint8_t)16U
#define RELAY_5 (uint8_t)25U
#define RELAY_6 (uint8_t)26U
#define RELAY_7 (uint8_t)27U

/** Status LEDs PINS */
#define STATUS_SUCCESS_LED0_PIN (uint8_t)33U
#define STATUS_SUCCESS_LED1_PIN (uint8_t)32U
#define STATUS_FAIL_LED0_PIN (uint8_t)17U

/** ESP32 Hardware definitions */
#define ESP_MAX_ADC_VALUE 4096U

#endif /* _HARDWARE_H_FILE_ */
