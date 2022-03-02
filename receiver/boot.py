import network, struct, json
from esp import espnow

w0 = network.WLAN(network.STA_IF)
w0.active(True)

e = espnow.ESPNow()
e.init()
BROADCAST = b'\xff\xff\xff\xff\xff\xff'
e.add_peer(BROADCAST)

while True:
    host, msg = e.irecv()
    if msg:
        values = struct.unpack('ffffff', msg)
        values_dict = {
                'px': values[0],
                'py': values[1],
                'pz': values[2],
                'ax': values[3],
                'ay': values[4],
                'az': values[5],
                }
        print(json.dumps(values_dict))

