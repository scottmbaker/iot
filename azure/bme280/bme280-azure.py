import time

from bme280 import BME280
from smbus import SMBus
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING=open("/etc/azure/device-connection").readline().strip()

MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity},"pressure": {pressure}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def main():
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            temperature = bme280.get_temperature()
            pressure = bme280.get_pressure()
            humidity = bme280.get_humidity()
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, 
                                               humidity=humidity,
                                               pressure=pressure)
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
                message.custom_properties["temperatureAlert"] = "true"
            else:
                message.custom_properties["temperatureAlert"] = "false"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(30)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    main()