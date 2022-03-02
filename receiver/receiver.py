import serial
import json


with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
    while True:
        js = ser.readline()
        try:
            print(json.loads(js))
        except JSONDecodeError as e:
            print(e)
