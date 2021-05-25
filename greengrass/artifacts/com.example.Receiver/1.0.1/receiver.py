from __future__ import print_function
import sys
import datetime
import time
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest
)


REVISION = "6"


def logSomething(message):
    # Append the message to the log file.
    with open('/tmp/Greengrass_Receiver.log', 'a') as f:
        print(str(datetime.datetime.now()) + " " + message, file=f) 


def banner():
    message = f"Hello, {sys.argv[1]}! Current time: {str(datetime.datetime.now())}."
    message += " Greetings from Receiver."
    message += " REVISON " + REVISION

    # Print the message to stdout.
    print(message)

    logSomething(message)


class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8")
            logSomething("Received: " + message)
            # Handle message.
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass


def subscribeToMQTT():
    TIMEOUT = 10

    ipc_client = awsiot.greengrasscoreipc.connect()

    topic = "my/topic"
    qos = QOS.AT_MOST_ONCE

    request = SubscribeToIoTCoreRequest()
    request.topic_name = topic
    request.qos = qos
    handler = StreamHandler()
    operation = ipc_client.new_subscribe_to_iot_core(handler)
    future = operation.activate(request)
    future.result(TIMEOUT)

    # Keep the main thread alive, or the process will exit.
    while True:
        time.sleep(10)
                    
    # To stop subscribing, close the operation stream.
    operation.close()


def main():
    banner()
    subscribeToMQTT()


main()
