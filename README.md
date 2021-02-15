# ESPUpdateServer

Update Server implemented for ESP8266 devices. The server listen to requests at a given port. When there is a valid update request coming from an ESP8266 device, it checks, if it has updates for that specific device. 

The device version is identified by a 6 digit UUID identifying the device and a three digit version number (e.g. 0.10.0). If the server finds a file greater than the given version number in the folder updates, the new firmware file gets send to the ESP device.

Updates are placed into the update folder in the following format:

<server_dir>/updates/<device_id>/<version_string>