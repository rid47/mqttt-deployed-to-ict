import uuid
def mac_addr():
    mac_addr = hex(uuid.getnode()).replace('0x', '')
    mac_addr = ':'.join(mac_addr[i : i + 2] for i in range(0, 11, 2))
    print(mac_addr)
    return mac_addr
	
mac_addr()