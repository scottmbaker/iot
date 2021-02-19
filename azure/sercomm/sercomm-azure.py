import urllib2, base64
from datetime import datetime
import xml.etree.ElementTree as ET
import threading
import traceback
import time
import json

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

CONNECTION_STRING=open("/etc/azure/device-connection").readline().strip()

INTERVAL = 30

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def get_sercomm():
    httpRequest = urllib2.Request("http://192.168.0.1:8080/cgi-bin/ltestatus.cgi?Command=Status")
    credentials = base64.b64encode('%s:%s' % ("admin", "admin"))
    httpRequest.add_header("Authorization", "Basic %s" % credentials)
    httpResponse = urllib2.urlopen(httpRequest)
    sercommLteStatusXML = httpResponse.read()

    tree = ET.ElementTree(ET.fromstring(sercommLteStatusXML))
    root = tree.getroot()

    data = {"IMSI": root.findall('IMSI')[0].text,
           "MCC": root.findall('MCC')[0].text,
           "MNC": root.findall('MNC')[0].text,
           "IPv4Addr": root.findall('IPv4Addr')[0].text,
           "Band": int(root.findall('Band')[0].text),
           "Bandwidth": root.findall('BandWidth')[0].text,
           "RSSI": int(root.findall('RSSI')[0].text),
           "RSRP": int(root.findall('RSRP')[0].text),
           "RSRQ": int(root.findall('RSRP')[0].text),
           "SINR": int(root.findall('SINR')[0].text),
           "TxBytes": int(root.findall('TxByte')[0].text),
           "TxPackets": int(root.findall('TxPacket')[0].text),
           "RxBytes": int(root.findall('RxByte')[0].text),
           "RxPackets": int(root.findall('RxPacket')[0].text)}

    """
    print ("IMSI: {}".format(root.findall('IMSI')[0].text))
    print ("MCC: {}".format(root.findall('MCC')[0].text))
    print ("MNC: {}".format(root.findall('MNC')[0].text))
    print ("IPv4Addr: {}".format(root.findall('IPv4Addr')[0].text))
    print ("Band: {}".format(root.findall('Band')[0].text))
    print ("Bandwidth: {}".format(root.findall('BandWidth')[0].text))
    print ("RSSI: {}".format(root.findall('RSSI')[0].text))
    print ("RSRP: {}".format(root.findall('RSRP')[0].text))
    print ("RSRQ: {}".format(root.findall('RSRQ')[0].text))
    print ("SINR: {}".format(root.findall('SINR')[0].text))
    print ("TxBytes: {}".format(root.findall('TxByte')[0].text))
    print ("TxPackets: {}".format(root.findall('TxPacket')[0].text))
    print ("RxBytes: {}".format(root.findall('RxByte')[0].text))
    print ("RxPackets: {}".format(root.findall('RxPacket')[0].text))
    """

    return data

def main():
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Start a thread to listen 
        #device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
        #device_method_thread.daemon = True
        #device_method_thread.start()

        while True:
            try:
                data = get_sercomm()
                msg_txt_formatted = json.dumps(data)

                message = Message(msg_txt_formatted)

                message.custom_properties["kind"] = "sercomm"

                # Send the message.
                print( "Sending message: {}".format(message) )
                client.send_message(message)
                print ( "Message successfully sent" )
            except:
                traceback.print_exc()
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    main()
