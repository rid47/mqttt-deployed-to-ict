# Updating device status upon data receive
import paho.mqtt.client as mqtt
import json
import uuid
import datetime
from agent_data_handler import data_handler, offline_data_handler

debug = False  # set debug = False to disable print command
debug2 = True

client = mqtt.Client(uuid.uuid4().hex)
broker = "broker.hivemq.com"
port = 1883


def on_connect(client, userdata, flags, rc):
    if debug2:
        print("agent_listener is connected with result code " + str(rc))
        print(datetime.datetime.now())


def on_disconnect(client, userdata, rc):
    if debug2:
        print("agent_listener is dis-connected with result code " + str(rc))
        print(datetime.datetime.now())

def on_message(client, userdata, message):
    if debug:
        print('\n')
    topic_split = message.topic.split("/")
    if topic_split[1] == "res_offline":
        if debug:
            print("device offline")
        offline_data_handler(message.payload)

    if topic_split[1] == "res_info":
        lab_id = topic_split[5]
        # print("division: {} ,district: {} ,upazilla: {} ,lab_id: {}".format(division,district,upazilla,lab_id))
        if debug:
            print("lab_id: {}".format(lab_id))
            print(message.payload)
        data_handler(lab_id, message.payload)


client.on_connect = on_connect  # attach the callback function to the client object
client.on_disconnect = on_disconnect
client.on_message = on_message  # attach the callback function to the client object

client.connect(broker, port, 60)
if debug:
    print("connecting to broker")

# client.loop_start() #start the loop


client.subscribe([("srdl/res_info/+/+/+/+/+/", 2), ("srdl/res_offline/+/", 2)])
# client.subcribe("srdl/res_offline/+",qos=2)
if debug:
    print("subscribed")

client.loop_forever()  # to maintain continuous network traffic flow with the broker
