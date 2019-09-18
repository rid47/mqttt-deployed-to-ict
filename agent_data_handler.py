import json
import pymysql
from pprint import pprint
from datetime import datetime, timedelta

host = "127.0.0.1"
user = "root"
password = ""
db = "srdl"
debug = True


def data_handler(lab_id, msg):
    j_msg = json.loads(msg)
    mac_addr = j_msg['mac_addr']
    # pprint(j_msg)
    cpu_info = {}
    if debug:
        print("-------------------Inside Data Handler Block----------------")
    # idle_flag = 0

        # print(cpu_info)

        # Checking if Device is online or Idle
    try:
        print("-------------------------I'm inside status check block------------------")
        idle_flag = j_msg['idle']
        last_activity = int(idle_flag)
        try:
            last_activity = datetime.utcfromtimestamp(last_activity)
        except:
            last_activity = last_activity * 0.001
            last_activity = datetime.utcfromtimestamp(last_activity)

        last_activity = last_activity + timedelta(hours=6)  # converting utc time to BST
        if debug:
            print("last keyboard/mouse activity on: {}".format(last_activity))

        # selecting threshold
        time_now = datetime.now()
        threshold_time = time_now - timedelta(minutes=30)
        if debug:
            print("threshold time:{}".format(threshold_time))

        # comparing
        latest_one = max(threshold_time, last_activity)
        if debug:
            print(latest_one)

        if latest_one == last_activity:
            print("device online")
            status = "1"
            print(status)
        else:
            print("device idle")
            status = "2"
            print(type(status))
        cpu_info['device_status'] = status
    except KeyError:
        pass




    # try:
    #     cpu_info['device_status'] = j_msg['status']
    # except KeyError:
    #     pass
    try:
        cpu_info['device_model'] = str(j_msg['cpu_info']['model'])
    except KeyError:
        pass
    try:
        cpu_info['brand'] = str(j_msg['cpu_info']['brand'])
    except KeyError:
        pass
    try:
        cpu_info['manufacture'] = str(j_msg['cpu_info']['manufacture'])
    except KeyError:
        pass
    try:
        cpu_info['display'] = str(j_msg['cpu_info']['display'])
    except KeyError:
        pass
    try:
        cpu_info['hardware'] = str(j_msg['cpu_info']['hardware'])
    except KeyError:
        pass
    try:
        cpu_info['android_version'] = str(j_msg['cpu_info']['android_version'])
    except KeyError:
        pass
    try:
        cpu_info['bits'] = str(j_msg['cpu_info']['bits'])
    except KeyError:
        pass
    try:
        cpu_info['hz_advertised'] = str(j_msg['cpu_info']['hz_advertised'])
    except KeyError:
        pass
    try:
        cpu_info['hz_actual'] = str(j_msg['cpu_info']['hz_actual'])
    except KeyError:
        pass
    try:
        cpu_info['network_type'] = str(j_msg['network_info']['network_type'])
    except KeyError:
        pass
    try:
        cpu_info['network_name'] = str(j_msg['network_info']['network_name'])
    except KeyError:
        pass
    try:
        cpu_info['bytes_sent'] = str(j_msg['network_info']['bytes_sent'])
    except KeyError:
        pass
    try:
        cpu_info['bytes_recv'] = str(j_msg['network_info']['bytes_recv'])
    except KeyError:
        pass
    try:
        cpu_info['total_disk'] = str(j_msg['disk_info']['total'])
    except KeyError:
        pass
    try:
        cpu_info['used_disk'] = str(j_msg['disk_info']['used'])
    except KeyError:
        pass
    try:
        cpu_info['percent_disk'] = str(j_msg['disk_info']['percent'])
    except KeyError:
        pass
    try:
        cpu_info['total_memory'] = str(j_msg['memory_info']['total'])
    except KeyError:
        pass
    try:
        cpu_info['available_memory'] = str(j_msg['memory_info']['available'])
    except KeyError:
        pass
    try:
        cpu_info['used_memory'] = str(j_msg['memory_info']['used'])
    except KeyError:
        pass
    try:
        cpu_info['free_memory'] = str(j_msg['memory_info']['free'])
    except KeyError:
        pass
    try:
        cpu_info['processor'] = str(len(j_msg['process_info']))
    except KeyError:
        pass
    if debug:
        print("*******************************")
        #print(j_msg['process_info'])

    try:
        cpu_info['process'] = ''
        for i in j_msg['process_info']:
            # for i in range(10):
            if debug:
                print("inside process info:--------------------------------")
                print(i['name'])
            cpu_info['process'] += i['name']
            if debug:
                print("appended")
            cpu_info['process'] += ","
        # cpu_info['process'].append(i['name'])
        cpu_info['process'] = cpu_info['process'][:-1]
        if debug:
            print(type(cpu_info['process']))
            print(cpu_info['process'])
    except KeyError:
        del cpu_info['process']
    # try:
    #     cpu_info['process'] = ''
    #     for i in j_msg['process_info']:
    #         # for i in range(10):
    #         if debug:
    #             print("inside process info:--------------------------------")
    #             print(i['name'])
    #         cpu_info['process'] += i['name']
    #         if debug:
    #             print("appended")
    #         cpu_info['process'] += ","
    #     # cpu_info['process'].append(i['name'])
    #     cpu_info['process'] = cpu_info['process'][:-1]
    #     if debug:
    #         print(type(cpu_info['process']))
    #         print(cpu_info['process'])
    # except KeyError:
    #     del cpu_info['process']



    sql = "UPDATE srdl_dashboard_device_status SET "
    c = 0;
    for k, v in cpu_info.items():
        # print("key is--------")
        # print(k)
        # print(v)
        # print(type(v))
        # print(len(cpu_info.keys()))
        sql += "`" + k + "`" + " = " + '"' + v + '"'
        #print(sql)
        c += 1
        if c < len(cpu_info.keys()):
            sql += ", "
        else:
            sql += " WHERE `device_id` = " + '"' + mac_addr + '"'

    if debug:
        print(sql)

    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(sql)
        if debug:
            print("executed")
            print(cursor.rowcount)
        conn.commit()
        if debug:
            print("\n")
            print("Data inserted to database")
        # sql3 = "select process from srdl_dashboard_device_status where device_id='d0:17:c2:cb:bd:77'"
        # cursor.execute(sql3)
        # result = cursor.fetchone()
        # print(result)
        cursor.close()
        conn.close()

    except Exception as e:
        print(e)


def offline_data_handler(msg):
    json_dict = json.loads(msg)
    if debug:
        print("I'm in offline data handler")
    for key, value in json_dict.items():
        if key == 'mac_addr':
            mac_addr = value
            if debug:
                print(mac_addr)
        # if key == 'gateway_ip':
        #     gateway_ip = value
        #     if debug:
        #         print(gateway_ip)

    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    sql = "UPDATE srdl_dashboard_device_status SET device_status = %s WHERE device_id = %s"

    try:
        cursor.execute(sql, ('0', mac_addr))
        if debug:
            print("executed")
            print(cursor.rowcount)
        conn.commit()
        if debug:
            print("\n")
            print(" Offline status data updated")
        cursor.close()
        conn.close()

    except pymysql.InternalError as error:
        code, message = error.args
        if debug:
            print(">>>>>>>>>>>>>", code, message)
