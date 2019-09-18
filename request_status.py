import paho.mqtt.client as mqtt
import json
import uuid
import datetime
from threading import Timer


debug = False  # set debug = False to disable print of all process command
debug2 = True  # set debug = False to disable print of only important msg.
client = mqtt.Client(uuid.uuid4().hex)
broker = "broker.hivemq.com"
port = 1883


def on_connect(client, userdata, flags, rc):
    if debug2:
        print("request_status is connected with result code " + str(rc))
        print(datetime.datetime.now())

def on_disconnect(client, userdata, rc):
    if debug2:
        print("request_status is dis-connected with result code " + str(rc))
        print(datetime.datetime.now())

# Sendig request for data @ specific interval


client.on_connect = on_connect  # attach the callback function to the client object
client.on_disconnect = on_disconnect
client.connect(broker, port, 60)
if debug:
    print("connecting to broker")

request_status = {

    "info": 1,
    "status": 1,
    "idle": 1,
    "cpu": 0,
    "memory": 0,
    "disk": 0,
    "process": 0,
    "network": 0,
}

# converting dict to str

request_status = json.dumps(request_status)


# requesting data @ regular interval


def publish():
    client.publish("srdl/req_info/", request_status)
    if debug:
        print("I'm requesting status from agent software...")
    Timer(10.0, publish).start()  # publish every 30 seconds
    if debug:
        print("Request sent.")


publish()  # initialise the function

client.loop_forever()  # to maintain continuous network traffic flow with the broker
