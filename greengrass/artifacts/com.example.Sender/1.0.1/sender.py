from __future__ import print_function
import sys
import datetime
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)


REVISION = "6"


def logSomething(message):
    # Append the message to the log file.
    with open('/tmp/Greengrass_Sender.log', 'a') as f:
        print(str(datetime.datetime.now()) + " " + message, file=f) 


def banner():
    message = f"Hello, {sys.argv[1]}! Current time: {str(datetime.datetime.now())}."
    message += " Greetings from Sender."
    message += " REVISON " + REVISION

    # Print the message to stdout.
    print(message)

    logSomething(message)


def publishToMQTT():
    TIMEOUT = 10

    ipc_client = awsiot.greengrasscoreipc.connect()
                        
    topic = "my/topic"
    message = "Hello, World"
    qos = QOS.AT_LEAST_ONCE

    request = PublishToIoTCoreRequest()
    request.topic_name = topic
    request.payload = bytes(message, "utf-8")
    request.qos = qos

    logSomething("Sending MQTT request")
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(request)

    logSomething("Waiting for MQTT send response")
    future = operation.get_response()
    future.result(TIMEOUT)

    logSomething("MQTT Successful")


def main():
    banner()
    publishToMQTT()


main()
