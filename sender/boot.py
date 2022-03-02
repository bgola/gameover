from esp import espnow
import uasyncio
import network
import machine
import time
import struct

from bno055 import *

network.WLAN(network.STA_IF).active(True)

BROADCAST = b'\xff\xff\xff\xff\xff\xff'

class SensorCommunication:
    def __init__(self):
        self._i2c = machine.I2C(1, scl=machine.Pin(4), sda=machine.Pin(0), freq=200000, timeout=2000)
        self._led = machine.Pin(22, machine.Pin.OUT)
        self.imu = None 
        self._get_imu()

        self.espnow = espnow.ESPNow()
        self.espnow.init()
        self.espnow.add_peer(BROADCAST)

    def _get_imu(self):
        try:
            self.imu = BNO055(self._i2c)
        except (OSError, RuntimeError) as e:
            print(e)

    def calibrated(self):
        calibrated = False
        try:
            calibrated = self.imu.calibrated()
        except (OSError, RuntimeError) as e:
            print(e)
            calibrated = False
        return calibrated

    def calibration_status(self):
        try:
            status = imu.cal_status()
        except (OSError, RuntimeError) as e:
            print(e)
     
    def get_values(self):
        values = []
        try:
            values = self.imu.euler() + self.imu.lin_acc()
        except (OSError, RuntimeError) as e:
            print(e)
            self._get_imu()
        return values

    def mainloop(self):
        while True:
            time.sleep(1/30)
            values = self.get_values()
            if len(values) == 6:
                print(values)
                self.espnow.send(BROADCAST, struct.pack('ffffff',
                                                        abs(values[0] / 180 - 1),
                                                        abs((values[1]) / 90),
                                                        abs((values[2]) / 180),
                                                        (values[3])/70,
                                                        (values[4])/70,
                                                        (values[5])/70))

sensor = SensorCommunication()
sensor.mainloop()
