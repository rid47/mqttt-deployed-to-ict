# importing required modules
import paho.mqtt.client as mqtt
import uuid
import json
import pymysql
import datetime

debug = True  # set debug = False to disable print command
# DB credentials
debug2 = True # set debug = False to disable important msg.

host = "127.0.0.1"
user = "root"
password = ""
db = "srdl"
client = mqtt.Client(uuid.uuid4().hex)
broker = "broker.hivemq.com"
port = 1883


def on_connect(client, userdata, flags, rc):
    if debug2:
        print("sending_topic is connected with result code " + str(rc))
        print(datetime.datetime.now())


def on_disconnect(client, userdata, rc):
    if debug2:
        print("sending_topic is dis-connected with result code " + str(rc))
        print(datetime.datetime.now())

def on_message(client, userdata, message):
    topic_split = message.topic.split("/")
    mac_id = topic_split[2]
    if debug:
        print(mac_id)
        print(message.payload)
    json_dict = json.loads(message.payload)
    for key, value in json_dict.items():
        if debug:
            print(key)
        if key == "topic" and value == 1:
            if debug:
                print("get the location info from topic_from_db.py")
            get_location(mac_id)


client.on_connect = on_connect  # attach the callback function to the client object
client.on_disconnect = on_disconnect
client.on_message = on_message  # attach the callback function to the client object

client.connect(broker, port, 60)
if debug:
    print("connecting to broker")

client.subscribe("srdl/req_topic/+/", qos=2)
if debug:
    print("subscribed")


# location info from db

def get_location(mac_id):
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    # sql = ''' SELECT id AS lab_id,division_id,district_id,upazilla_id FROM `srdl_dashboard_lab_info` where id = (SELECT `device_mac` FROM `srdl_dashboard_device_reg` WHERE `mac_id`= %s) '''
    sql = '''SELECT division_id,district_id,upazilla_id,lab_id FROM `srdl_dashboard_device_reg` where device_mac = %s'''
    try:
        cursor.execute(sql, mac_id)
        if debug:
            print("executed")
        row = cursor.fetchone()
        if debug:
            print(row)
            print(cursor.rowcount)
            # conn.commit()
            # print("\n")
            # print ("Data inserted to database")
        conn.close()
        publish_location(mac_id, row)


    # except MySQLError as e:
    # print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    except (ProgrammingError, DataError, IntegrityError, NotSupportedError, OperationalError) as e:
        if debug:
            print("Caught an Error:")
            print(e)


# publishing location json to pre defined topic

def publish_location(mac_id, row):
    row['topic'] = 1
    if debug:
        print(row)
    location_info = json.dumps(row)
    if debug:
        print(location_info)
    topic = "srdl/res_topic/" + mac_id + "/"
    if debug:
        print(topic)
    client.publish(topic, location_info)


# client.publish("srdl/res_topic/test","hello")


client.loop_forever()  # to maintain continuous network traffic flow with the broker
